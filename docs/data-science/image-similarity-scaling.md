---
title: "Image Similarity at Scale: Architecture Decisions from 430K to 50M"
description: "Concrete migration path and infrastructure decisions for image similarity systems scaling from hundreds of thousands to tens of millions of vectors - vector DBs, storage, training pipelines"
---

# Image Similarity at Scale: Architecture Decisions from 430K to 50M

Infrastructure and architecture decisions for image similarity systems as they grow. Each threshold triggers different bottlenecks. Make forward-compatible decisions early - the cost of retrofitting grows non-linearly.

## Hard Limits by Scale

### Elasticsearch HNSW

| Scale | RAM (int8, 3 indices, 768-d) | p99 kNN latency | Filtered kNN | Verdict |
|---|---|---|---|---|
| 430K | ~2 GB | <50ms | OK | Comfortable |
| 5M | ~24 GB | 80-150ms | Degrades | Watchable, GC pressure |
| 10M | ~48 GB | 150-300ms | Slow | Upper comfort boundary |
| 50M | ~240 GB | 500-1500ms | Poor | Not recommended |

ES formula: `num_vectors × (dims + 4)` per index + 30% HNSW graph overhead. Java GC pauses blow p99 under concurrent load - Qdrant (Rust) does not have this problem.

**ES stays for 430K-5M. Migrate between 5-10M.**

### File System Layout

NTFS/ext4 performance collapses past ~100K entries per directory. At 50M flat files: Explorer never opens, DIR takes hours, backup fails.

**Do this NOW at 430K:**

```python
import hashlib
import os
import shutil

def get_shard_path(base_dir, pin_id, filename):
    """2-level hex sharding: base/ab/cd/pin-abcdef.jpg"""
    hash_prefix = hashlib.md5(str(pin_id).encode()).hexdigest()[:4]
    return os.path.join(base_dir, hash_prefix[:2], hash_prefix[2:], filename)

def migrate_flat_to_sharded(source_dir, target_dir):
    """Migrate 430K files in minutes. At 10M: hours. At 50M: days."""
    for filename in os.listdir(source_dir):
        pin_id = filename.split('-')[1].split('.')[0]
        dest = get_shard_path(target_dir, pin_id, filename)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(os.path.join(source_dir, filename), dest)
```

Result: 65,536 leaf folders, ~760 files per folder at 50M. This is manageable on every filesystem.

### Database

- **SQLite**: single global write lock. Fine for 430K with sequential workers. Breaks when embedding + scraping + cleanup run concurrently at 5M+.
- **PostgreSQL at 5M**: `pg_loader` migration in an afternoon if schema is PostgreSQL-compatible now.
- **50M: PostgreSQL + Parquet snapshots** for 2.5B edges (200 GB). PostgreSQL for live queries, Parquet for training.

---

## Vector DB at 50M Scale

### Qdrant (recommended for single-team projects)

Rust-based, no GC, consistent p99. Key capabilities at 50M:

```yaml
# Single-machine Qdrant with int8 + on-disk storage
# 64 GB RAM box handles 400M int8 vectors (on-disk HNSW, RAM for index + quantised vecs)

# Collection config for 50M × 256-d projection head output
vectors_config:
  size: 256
  distance: Cosine
  quantization_config:
    scalar:
      type: int8
      always_ram: true  # keep quantised vecs in RAM, originals on disk
hnsw_config:
  m: 16
  ef_construct: 200
  on_disk: true  # HNSW graph on NVMe, not RAM
```

Self-hosted cost at 50M (Hetzner AX102, 128 GB RAM, 2x 1.92 TB NVMe): ~$130/month. Managed Qdrant Cloud for same: ~$450-1200/month.

ACORN algorithm (2025) handles tight-filter kNN much better than ES: adaptively switches between graph traversal and brute-force based on filter selectivity.

### pgvectorscale (single-system option)

If metadata is already in PostgreSQL, consolidate:

```sql
-- pgvectorscale: DiskANN index
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

CREATE TABLE pin_embeddings (
    pin_id BIGINT PRIMARY KEY,
    projection_vec VECTOR(256)
);

CREATE INDEX ON pin_embeddings USING diskann (projection_vec);
-- Published benchmark: 471 QPS at 99% recall on 50M × 768-d Cohere vectors
```

One system instead of two. Trades some raw performance for operational simplicity.

### When to Use What

| Need | Choice |
|---|---|
| 430K-5M, already on ES | Stay on ES |
| 50M, single team | Qdrant (self-hosted) |
| 50M, need PostgreSQL for metadata too | pgvectorscale |
| 100M+ QPS at scale | Milvus |
| Never | Managed Pinecone/Zilliz ($3-6K/month vs $300 self-hosted) |

---

## Training Pipeline at Scale

### Precomputed Feature Cache (critical at 5M+)

At 50M images, per-epoch backbone inference costs ~$600/epoch-round. The fix: extract once, train the projection head on cached features.

```python
# Stage 1: one-time feature extraction
# Output: sharded Parquet, ~200 GB float16 for 50M images × 3 backbones

import pyarrow as pa
import pyarrow.parquet as pq
from torch.utils.data import DataLoader

def extract_features_to_parquet(
    image_ids, image_loader, clip_model, csd_model, dinov3_model,
    output_dir, shard_size=1_000_000
):
    batch_records = []
    for pin_id, img in image_loader:
        clip_vec = clip_model.encode(img)
        csd_vec = csd_model.encode(img)
        dinov3_vec = dinov3_model.encode(img)
        color_vec = extract_color_features(img)
        batch_records.append({
            'pin_id': pin_id, 'clip': clip_vec, 'csd': csd_vec,
            'dinov3': dinov3_vec, 'color': color_vec
        })
        if len(batch_records) >= shard_size:
            write_parquet_shard(batch_records, output_dir)
            batch_records = []

# Stage 2: training (runs in minutes, not hours)
# Load feature Parquet, join with edge pairs, train MLP head only
```

**Training time with precomputed features:**

| Scale | Training time | GPU cost |
|---|---|---|
| 430K | ~2h H100 | $5 |
| 5M | ~8h H100 | $20 |
| 50M | ~30h H100 | $80 |
| 50M (raw images, no cache) | ~500h H100 | $1,500 |

**Design the feature cache now at 430K.** It takes 1 day to implement. Retrofitting the training loop at 10M takes 2 weeks.

### MoCo Memory Bank for 50M

In-batch negatives (batch 1024) are too small at 50M. MoCo-style memory bank gives 65K negatives on single GPU:

```python
class MoCoSimilarityTrainer:
    def __init__(self, model, queue_size=65536, momentum=0.999, temperature=0.07):
        self.model = model
        self.model_k = copy.deepcopy(model)  # momentum encoder
        self.queue = F.normalize(torch.randn(queue_size, 256), dim=1)
        self.queue_ptr = 0
        self.momentum = momentum
        self.temperature = temperature

    def update_momentum_encoder(self):
        for p, pk in zip(self.model.parameters(), self.model_k.parameters()):
            pk.data = self.momentum * pk.data + (1 - self.momentum) * p.data

    def infonce_with_queue(self, q, k):
        """q, k: L2-normalised [B, D]. Queue: [Q, D]."""
        l_pos = torch.einsum('nd,nd->n', q, k).unsqueeze(-1)  # [B, 1]
        l_neg = torch.einsum('nd,qd->nq', q, self.queue.clone().detach())  # [B, Q]
        logits = torch.cat([l_pos, l_neg], dim=1) / self.temperature
        labels = torch.zeros(q.size(0), dtype=torch.long, device=q.device)
        loss = F.cross_entropy(logits, labels)
        self._dequeue_and_enqueue(k)
        return loss
```

Batch 256 + 65K queue = 65K effective negatives per step. Fits single GPU. No need for 4096+ batch size.

---

## Storage Architecture at 50M

### Object Storage Comparison (25 TB for 50M × 500 KB images)

| Provider | Monthly cost | Egress | Notes |
|---|---|---|---|
| Wasabi | ~$175 | Free | 90-day minimum retention lock |
| Cloudflare R2 | ~$375 | Zero | Best for hot/CDN tier |
| Backblaze B2 | ~$375 | 3x free | Good backup tier |
| AWS S3 Standard | ~$575 + egress | $0.09/GB | Never for this workload |

**Two-tier at 50M:**
1. Wasabi: original full-res images (cold archive)
2. Cloudflare R2: thumbnails (236px + 474px) - 50M × 50 KB = 2.5 TB = $37/month

Total storage: ~$215/month for everything at 50M.

### Graph Edge Storage at 2.5B Edges

```sql
-- PostgreSQL: live queries ("what's related to pin X?")
CREATE TABLE pin_related (
    src_id BIGINT NOT NULL,
    dst_id BIGINT NOT NULL,
    weight FLOAT DEFAULT 1.0,
    hop_level SMALLINT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX ON pin_related (src_id) INCLUDE (dst_id, weight);

-- 2.5B rows ~ 200 GB. PostgreSQL handles this fine.
-- Add partitioning by src_id hash if needed.
```

Parquet snapshots on Wasabi/R2 for training full-dataset reads - avoids crushing live DB.

---

## Migration Path

### Phase 0 (NOW, at 430K) - Forward-Compatible Setup

1. **File sharding**: migrate to 2-level hex layout. Minutes at 430K, days at 50M.
2. **Feature cache pipeline**: write backbone outputs to Parquet per batch. Even unused now - design it right.
3. **VectorIndex abstraction**: single class wrapping ES today, Qdrant tomorrow.

```python
class VectorIndex:
    """Abstraction over ES / Qdrant / pgvector. Change backend, not callers."""
    def upsert(self, id: str, vector: np.ndarray, metadata: dict): ...
    def knn_search(self, query_vec: np.ndarray, k: int, filters: dict) -> list: ...
    def hybrid_search(self, query_vec: np.ndarray, sparse_query: dict, k: int) -> list: ...
```

4. **Image URL abstraction**: `get_image_url(pin_id)` helper - single place to swap filesystem for S3/R2 later.
5. **PostgreSQL-compatible SQLite schema**: use strict column types, no SQLite-isms. `pg_loader` migration takes an afternoon with compatible schema, weeks without.

### Phase 1 (1-5M, ~6 months)

1. PostgreSQL migration for metadata + edges
2. Wasabi cold storage for originals
3. Move feature cache to Parquet as primary (not EXIF)
4. Pilot Qdrant with 1M sample vs ES, compare latency

### Phase 2 (10-50M)

1. Full Qdrant migration via alias swap
2. R2 hot tier for thumbnails
3. MoCo training loop
4. Distributed feature extraction (4 GPUs = 25h wall-clock vs 100h single-GPU)

---

## Cost Summary

| Scale | Servers | Storage | Training/month | Total/month |
|---|---|---|---|---|
| 430K | ~$20 VPS | ~$0 local | ~$5/run | **~$20-25** |
| 5M | ~$95 (PG + ES) | ~$35 Wasabi | ~$20/run | **~$130-150** |
| 50M | ~$185 (Qdrant + PG) | ~$215 | ~$80/run | **~$400-600** |
| 50M managed | ~$2000-5000 vector DB | ~$500 | ~$80/run | **~$2600-5600** |

Self-hosted is 5-10x cheaper than managed at 50M.

## Gotchas

- **HNSW deletes are soft.** Deleted vectors leave ghost edges in the graph. ES requires periodic merge/optimise if you delete >10% of data. Qdrant handles this better but still needs periodic optimization.
- **Model versioning is critical.** When you retrain and re-index, keep old and new vectors accessible for A/B testing. Schema: `projection_v1`, `projection_v2`. Rolling out without A/B loses all quality measurement.
- **ES free tier limits kNN features.** Some int8 HNSW options require paid tier. Check license before designing around them.
- **SQLite single-writer lock hits earlier than expected.** At 5M with 3+ concurrent workers (scraper + embedder + cleanup) you will see "database is locked" under sustained load even with WAL mode.
- **Thumbnail generation is one-time.** Generate 236px + 474px thumbnails during ingestion and cache forever. Don't regenerate on serve - this is the biggest serving latency contributor at scale.
- **pgvectorscale benchmark caveat.** The 471 QPS vs 41 QPS Qdrant benchmark uses pgvectorscale's sweet spot. At high concurrency and with complex filters, Qdrant's ACORN approach typically wins. Test both for your access pattern.

## See Also

- [[image-similarity-pipeline]] - building the pipeline: noise filtering, training, evaluation
- [[vector-databases]] - HNSW tuning, quantization, hybrid RRF
- [[unsupervised-learning]] - MoCo, SimCLR, hard negative mining at scale
- [[pandas-eda]] - Parquet, feature stores, streaming datasets
