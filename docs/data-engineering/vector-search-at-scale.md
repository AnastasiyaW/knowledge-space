---
title: Vector Search at Scale
category: reference
tags: [vector-search, faiss, elasticsearch, embeddings, ann, ivfflat, knn, sqlite, hybrid-search]
---

# Vector Search at Scale

Scaling embedding-based similarity search from tens of thousands to millions of vectors. Covers storage backends, index types, hybrid architectures, and migration paths.

## Key Facts

- FAISS FlatIP: exact search, O(n) per query, all vectors in RAM - breaks at ~100K vectors for latency, ~10M for RAM
- FAISS IVFFlat: approximate, ~95% recall, 10x faster - requires training on representative data before use
- SQLite as vector metadata store replaces JSON registries: O(1) lookup, transactional writes, no full-load on startup
- Elasticsearch `dense_vector` with kNN supports both approximate and exact search, enables hybrid filtering
- Rule of thumb: <100K vectors → FlatIP exact; 100K-10M → IVFFlat; >10M → HNSW (Faiss or dedicated vector DB)
- EXIF/metadata as source of truth pattern: SQLite and search indexes are caches that can be rebuilt

## Storage Architecture

### Scale Thresholds

| Scale | RAM Cost (768-d float32) | Recommended Backend |
|-------|--------------------------|---------------------|
| <100K vectors | 300 MB | FAISS FlatIP (exact) |
| 100K-1M | 3 GB | FAISS IVFFlat (approximate) |
| 1M-10M | 30 GB | FAISS IVFFlat + disk persistence |
| >10M | too large for RAM | Dedicated vector DB (Weaviate, Qdrant, Milvus) |

### SQLite as Metadata Layer

Replacing JSON registries with SQLite eliminates full-load-on-startup and enables O(1) lookups.

```sql
CREATE TABLE embeddings (
    filepath TEXT PRIMARY KEY,
    folder   TEXT NOT NULL,
    md5      TEXT,
    csd_vec  BLOB,          -- float32 array as raw bytes
    vgg_vec  BLOB,
    color_json TEXT,
    color_tags TEXT,        -- comma-separated for fast LIKE queries
    brightness REAL,
    saturation REAL,
    temperature TEXT,
    embedded_at TEXT        -- ISO timestamp
);

CREATE INDEX idx_folder ON embeddings(folder);
CREATE INDEX idx_brightness ON embeddings(brightness);
```

```python
import sqlite3, numpy as np

def upsert(db: sqlite3.Connection, filepath: str, vec: np.ndarray, meta: dict):
    db.execute("""
        INSERT OR REPLACE INTO embeddings (filepath, csd_vec, color_tags, brightness)
        VALUES (?, ?, ?, ?)
    """, (filepath, vec.astype(np.float32).tobytes(), meta["color_tags"], meta["brightness"]))
    db.commit()

def iter_vectors(db: sqlite3.Connection, dim: int):
    for row in db.execute("SELECT filepath, csd_vec FROM embeddings WHERE csd_vec IS NOT NULL"):
        yield row[0], np.frombuffer(row[1], dtype=np.float32).reshape(dim)
```

### FAISS Index with Disk Persistence

```python
import faiss, numpy as np

def build_index(vecs: np.ndarray, n_lists: int = None) -> faiss.Index:
    n, d = vecs.shape
    if n < 100_000:
        index = faiss.IndexFlatIP(d)   # exact, keep in RAM
    else:
        n_lists = n_lists or int(np.sqrt(n))
        quantizer = faiss.IndexFlatIP(d)
        index = faiss.IndexIVFFlat(quantizer, d, n_lists, faiss.METRIC_INNER_PRODUCT)
        index.train(vecs)
    index.add(vecs)
    return index

# Persist to disk, reload with mmap
faiss.write_index(index, "vectors.faiss")
index = faiss.read_index("vectors.faiss", faiss.IO_FLAG_MMAP)  # zero-copy load
```

**IVFFlat parameters:**
- `n_lists` = `sqrt(n)` is a good default (balance between speed and recall)
- `index.nprobe = 10` at search time controls recall vs speed (higher = more accurate, slower)
- Training requires a representative sample; adding vectors after training does not retrain centroids

## Elasticsearch kNN Integration

### Index Mapping

```json
{
  "mappings": {
    "properties": {
      "filepath": {"type": "keyword"},
      "folder":   {"type": "keyword"},
      "color_tags": {"type": "keyword"},
      "brightness": {"type": "float"},
      "saturation": {"type": "float"},
      "temperature": {"type": "keyword"},
      "csd_vector": {
        "type": "dense_vector",
        "dims": 768,
        "similarity": "cosine",
        "index": true
      },
      "embedded_at": {"type": "date"}
    }
  }
}
```

### Hybrid Query: Filter + kNN

```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def search_filtered_knn(query_vec: list, color_tags: list, k: int = 20):
    return es.search(index="images", body={
        "knn": {
            "field": "csd_vector",
            "query_vector": query_vec,
            "k": k,
            "num_candidates": k * 10,
            "filter": {
                "terms": {"color_tags": color_tags}
            }
        }
    })

def facets_aggregation():
    return es.search(index="images", body={
        "size": 0,
        "aggs": {
            "by_folder": {"terms": {"field": "folder", "size": 100}},
            "by_color":  {"terms": {"field": "color_tags", "size": 50}}
        }
    })
```

### Sync from SQLite to Elasticsearch

```python
from elasticsearch.helpers import bulk

def sync_to_es(db, es, index: str, batch_size: int = 500):
    def actions():
        for row in db.execute("SELECT filepath, folder, csd_vec, color_tags, brightness FROM embeddings"):
            vec = np.frombuffer(row[2], dtype=np.float32).tolist() if row[2] else None
            yield {
                "_index": index,
                "_id": row[0],
                "_source": {
                    "filepath": row[0],
                    "folder": row[1],
                    "csd_vector": vec,
                    "color_tags": (row[3] or "").split(","),
                    "brightness": row[4],
                }
            }
    bulk(es, actions(), chunk_size=batch_size)
```

## Similarity Clustering Pipelines

### K-means Domain Assignment (FAISS GPU)

```python
def build_domains(index: faiss.Index, n_clusters: int = None):
    n = index.ntotal
    n_clusters = n_clusters or int(np.sqrt(n))
    
    # Extract all vectors from index
    vecs = faiss.rev_swig_ptr(index.get_xb(), n * index.d).reshape(n, index.d)
    
    kmeans = faiss.Kmeans(index.d, n_clusters, niter=20, gpu=True)
    kmeans.train(vecs)
    
    _, labels = kmeans.index.search(vecs, 1)  # assign each vector to cluster
    return labels.flatten()
```

### Multi-Resolution Leiden Clustering (Explorer)

```python
import igraph as ig
import leidenalg

def leiden_at_resolution(knn_graph: ig.Graph, gamma: float) -> list:
    partition = leidenalg.find_partition(
        knn_graph,
        leidenalg.CPMVertexPartition,
        resolution_parameter=gamma
    )
    return partition.membership

def build_explorer(vecs: np.ndarray, resolutions: list = None):
    if resolutions is None:
        resolutions = [round(0.1 + i * 0.25, 2) for i in range(20)]  # 0.1 to 5.0
    
    # Build kNN graph via FAISS
    d = vecs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(faiss.normalize_L2(vecs.copy()))
    k = 15
    distances, indices = index.search(vecs, k + 1)  # +1 to exclude self
    
    edges = [(i, int(indices[i, j])) for i in range(len(vecs)) for j in range(1, k + 1)]
    g = ig.Graph(n=len(vecs), edges=edges)
    
    return {gamma: leiden_at_resolution(g, gamma) for gamma in resolutions}
```

## Migration Pattern (JSON Registry → SQLite)

```python
import json, sqlite3

def migrate_json_to_sqlite(registry_path: str, db_path: str):
    with open(registry_path) as f:
        registry = json.load(f)
    
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS embeddings (filepath TEXT PRIMARY KEY, ...)")
    
    for filepath, data in registry.items():
        vec = np.array(data["embedding"], dtype=np.float32)
        conn.execute("INSERT OR REPLACE INTO embeddings (filepath, csd_vec) VALUES (?, ?)",
                     (filepath, vec.tobytes()))
    
    conn.commit()
    print(f"Migrated {len(registry)} entries")
```

## Performance Numbers (Reference)

| Operation | Scale | Time | Notes |
|-----------|-------|------|-------|
| FAISS build (FlatIP) | 100K vectors, 768-d | ~2s | CPU |
| FAISS build (IVFFlat) | 1M vectors, 768-d | ~3.5 min | Includes ES scroll |
| FAISS save to ES | 1M domains | ~10 min | update_by_query batches |
| UMAP projection | 430K x 768-d | ~20 min | CPU |
| Leiden (1 resolution) | 430K vertices | ~40s | igraph CPU |
| ES kNN query | — | 5-15ms | per query |
| SQLite upsert | — | <1ms | per row |
| ES scroll 170K filenames | — | ~2 min | scroll with 1000 size |

## Data Size Estimates at 1M Vectors

| Component | Size |
|-----------|------|
| SQLite (768-d + 1024-d + metadata) | ~8 GB |
| FAISS FlatIP csd.index (768-d) | 3 GB RAM |
| FAISS IVFFlat csd.index | 300 MB RAM + 3 GB disk |
| Elasticsearch (768-d dense_vector) | ~10 GB disk |
| JSON registry (deprecated) | >100 MB, full-load-on-start |

## Gotchas

- **IVFFlat requires training before adding vectors** - calling `index.add()` without `index.train()` first silently produces wrong results for IVFFlat. Always check `index.is_trained` before adding
- **ES scroll is slow for resume patterns** - loading 170K+ document IDs via scroll to check what's already indexed takes 2+ minutes. Better: store indexed status in SQLite and skip ES scroll entirely
- **save_domains_to_es is the bottleneck** - updating domain_id field one cluster at a time via update_by_query is slow (655 clusters × multiple batches = 10+ minutes). Use bulk update with `update_by_query` with `script` filtering by cluster_id range instead
- **UMAP on 400K+ points needs sampling** - full UMAP on 430K x 768-d takes 15-20 min on CPU. For interactive explorers, use stratified sampling (5K-10K points) with pre-computed cluster assignments; browser canvas handles 5K well but struggles past 10K DOM nodes
- **FAISS mmap load vs full load** - `IO_FLAG_MMAP` gives near-zero startup time but first queries are slower (page faults). Use mmap for servers that receive queries immediately after start; use full load for batch jobs
- **IVFFlat nprobe must be set at query time** - default nprobe=1 gives poor recall. Set `index.nprobe = 64` (or `nlist/4`) for production queries

## See Also

- [[data-science/dimensionality-reduction]] - UMAP, PCA, t-SNE
- [[data-engineering/apache-kafka]] - streaming embeddings pipeline
- [[data-engineering/etl-elt-pipelines]] - batch embedding pipelines
- [[data-science/recommender-systems]] - ANN-based collaborative filtering
