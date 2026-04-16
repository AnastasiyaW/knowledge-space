---
title: "Image Similarity Pipeline: Graph Supervision, Contrastive Training, Vector Search"
description: "Production-grade image similarity pipeline using CLIP+CSD+DINOv3 backbones, contrastive learning on graph-supervised pairs, and Elasticsearch HNSW - with noise filtering and evaluation methodology"
---

# Image Similarity Pipeline: Graph Supervision, Contrastive Training, Vector Search

Building an image retrieval system where "similar" is defined by weak graph supervision (co-engagement edges, e.g., Pinterest-style `pin_related`). Covers noise filtering, backbone selection, contrastive training recipes, and serving via vector search.

**Reference scale:** 430K images, 7.2M graph edges, CLIP+CSD+color in Elasticsearch.

## Part 1: Cleaning Graph-Supervised Training Data

### Nature of the Noise

Co-engagement graphs (co-save, co-click) generate noisy positives:

- **L1 edges** (same board, same session) - high-quality, ~90% true positives
- **L2+ edges** (neighbour-of-neighbour) - 10-30% noise, topic drift not random garbage
- **False negatives are massive**: visually identical items from different boards have no edge

At 7.2M edges over 430K pins (~16.7 avg degree), expect 10-30% label noise by published benchmarks.

### Cluster-Coherence Filtering (no labels needed)

Best ROI first pass. Requires embedding vectors per image and k-means cluster assignments.

```python
import numpy as np
from scipy import stats

def cluster_coherence_filter(edges, embeddings, cluster_ids, z_threshold_drop=-3, z_threshold_flag=-2):
    """
    edges: list of (src_id, dst_id)
    embeddings: {id: np.array} - CSD or CLIP vectors
    cluster_ids: {id: int}
    Returns: (confirmed, flagged, dropped)
    """
    from sklearn.metrics.pairwise import cosine_similarity

    cluster_edges = {}  # cluster_id -> list of (src, dst, similarity)
    for src, dst in edges:
        sim = cosine_similarity([embeddings[src]], [embeddings[dst]])[0][0]
        cid = cluster_ids[src]
        cluster_edges.setdefault(cid, []).append((src, dst, sim))

    confirmed, flagged, dropped = [], [], []
    for cid, edge_list in cluster_edges.items():
        sims = [e[2] for e in edge_list]
        if len(sims) < 10:
            confirmed.extend(edge_list)
            continue
        z_scores = stats.zscore(sims)
        for (src, dst, sim), z in zip(edge_list, z_scores):
            if z < z_threshold_drop:
                dropped.append((src, dst, sim, z))
            elif z < z_threshold_flag:
                flagged.append((src, dst, sim, z))
            else:
                confirmed.append((src, dst, sim, z))

    return confirmed, flagged, dropped
```

Expected output: drops 8-15% as obvious noise, flags 5-10% for review.

**Do NOT auto-drop L1 edges** (same board, same session) - user explicitly grouped these even if CSD distance looks wrong.

### NN-Graph Cross-Reference

```python
def nn_graph_partition(pin_ids, edges, es_client, k=50):
    """
    Partition edges into: confirmed (in both pin_related AND CSD kNN),
    drop_candidate (in pin_related but NOT in CSD kNN),
    add_candidate (in CSD kNN but NOT in pin_related)
    Typical ratio: 60% confirmed, 25% drop-candidate, 15% add-candidate
    """
    edge_set = set((a, b) for a, b in edges)
    confirmed, drop_candidate, add_candidate = [], [], []

    for pin_id in pin_ids:
        # kNN query to ES for this pin's CSD vector
        knn_results = es_client.knn_search(pin_id, k=k, field="csd_vec")
        knn_set = set(r['_id'] for r in knn_results)

        for neighbor_id in knn_set:
            if (pin_id, neighbor_id) in edge_set:
                confirmed.append((pin_id, neighbor_id))
            else:
                add_candidate.append((pin_id, neighbor_id))

        for src, dst in edge_set:
            if src == pin_id and dst not in knn_set:
                drop_candidate.append((src, dst))

    return confirmed, drop_candidate, add_candidate
```

### Active Learning: Signal Disagreement Ranking

```python
def signal_disagreement_rank(edges, clip_vecs, csd_vecs, color_jaccard_fn):
    """Rank edges by variance across similarity signals.
    High variance = model uncertainty = most informative for labeling.
    Target 2-5K labels from the top of this ranking.
    """
    from sklearn.metrics.pairwise import cosine_similarity

    scores = []
    for src, dst in edges:
        csd_sim = cosine_similarity([csd_vecs[src]], [csd_vecs[dst]])[0][0]
        clip_sim = cosine_similarity([clip_vecs[src]], [clip_vecs[dst]])[0][0]
        color_sim = color_jaccard_fn(src, dst)
        variance = np.var([csd_sim, clip_sim, color_sim])
        scores.append((src, dst, variance, csd_sim, clip_sim, color_sim))

    return sorted(scores, key=lambda x: -x[2])  # highest variance first
```

Expected lift from 2-5K active labels: 3-8 points Recall@10 vs random labeling.

**Labeling throughput guide:**
- Streamlit/Tkinter side-by-side binary (A/D/S keys): ~800-1200 pairs/hour
- Label Studio form UI: ~200-400 pairs/hour

### Output Artifacts

Save for reproducibility and model eval reuse:

```bash
edge_audit.parquet     # src, dst, csd_sim, clip_sim, color_jaccard, z_score, nn_confirmed, verdict
noise_classifier.pkl   # trained on 2K human labels, auto-labels remaining flagged edges
human_labels.sqlite    # 2K reviewed pairs, reuse in test set construction
edges_clean.parquet    # final training edge list
```

---

## Part 2: Model Architecture

### Backbone Signals

| Backbone | Captures | Dim | Notes |
|---|---|---|---|
| CLIP ViT-L/14 | Semantic content, concepts | 768 | Swap for SigLIP 2 ViT-L for 2-5 point lift |
| CSD (Somepalli 2024) | Style attributes, color palettes | 768 | SOTA open-source style descriptor |
| DINOv3 (Meta 2025) | Instance geometry, dense patches | 1024 | +10.9 GAP on instance retrieval vs DINOv2 |
| Color features | Brightness, saturation, temperature | ~24 | Weak signal, use as tie-breaker only |

**SigLIP 2** ([arxiv 2502.14786](https://arxiv.org/abs/2502.14786)): drop-in replacement for CLIP with sigmoid loss, multilingual, better retrieval. ViT-L sweet spot for <1M images.

**DINOv3** ([arxiv 2508.10104](https://arxiv.org/html/2508.10104v1)): frozen features are near-SOTA on retrieval without fine-tuning. Add as fourth backbone.

### Recommended Architecture: Frozen Multi-Backbone + Projection Head

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimilarityProjectionHead(nn.Module):
    def __init__(self, input_dim=1560, hidden_dim=1024, output_dim=256):
        super().__init__()
        # input_dim = CLIP(768) + CSD(768) + color(24) = 1560
        # Add DINOv3(1024) -> input_dim = 2584
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 512),
            nn.GELU(),
            nn.Linear(512, output_dim),
        )

    def forward(self, x):
        return F.normalize(self.net(x), dim=-1)


def infonce_loss(q, k_pos, k_neg, temperature=0.07):
    """
    q: [B, D], k_pos: [B, D], k_neg: [B, K, D]
    All L2-normalized.
    """
    logits_pos = (q * k_pos).sum(-1, keepdim=True) / temperature
    logits_neg = torch.einsum('bd,bkd->bk', q, k_neg) / temperature
    logits = torch.cat([logits_pos, logits_neg], dim=1)  # [B, 1+K]
    labels = torch.zeros(q.size(0), dtype=torch.long, device=q.device)
    return F.cross_entropy(logits, labels)
```

**Training config (Recipe A - 2-3 days, single GPU):**
```python
# Precompute backbone features first (saves per-epoch re-running)
# Load: clip_vecs[pin_id], csd_vecs[pin_id], dinov3_vecs[pin_id], color_vecs[pin_id]

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=3)

# Batch: (pin_a_features, pin_b_features) from cleaned edges
# Hard negatives: K=4 samples from same cluster as pin_a, not in edges
# Effective batch: 1024+ (bigger = more in-batch negatives = better)
# Epochs: 3-5
# H100 training time: 2-4 hours
# Expected Recall@10 lift: +5-10 points over weighted-kNN baseline
```

**Recipe B - LoRA fine-tune SigLIP 2 (adds 3-5 more points):**
```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"])
siglip_model = get_peft_model(siglip_model, lora_config)
# Same InfoNCE loss, unfrozen encoder
# Training time: 6-10h H100, cost ~$15
```

### Hard Negative Mining

```python
def sample_hard_negatives(batch_ids, cluster_ids, edge_set, all_ids_by_cluster, K=4, margin=0.7):
    """
    For each pin, sample K negatives from same cluster that:
    1. Are NOT in edge_set (true negatives only)
    2. Have similarity < margin (avoid false negatives)
    """
    hard_negs = []
    for pin_id in batch_ids:
        cid = cluster_ids[pin_id]
        candidates = [x for x in all_ids_by_cluster[cid]
                     if (pin_id, x) not in edge_set and x != pin_id]
        hard_negs.append(np.random.choice(candidates, K, replace=False))
    return np.array(hard_negs)
```

**False negative trap:** ~70% of top-similar pairs in your corpus ARE related but missing from the graph. Apply similarity margin threshold (<0.7 cosine) to candidates before treating as negatives.

### Cost/Lift Table

| Approach | Training time | GPU cost | Expected Recall@10 |
|---|---|---|---|
| Weighted kNN (baseline) | 0 | $0 | baseline |
| Tune weights on labeled data | 1h | $0 | +3-7 pts (free win) |
| Add DINOv3 backbone | 1 day | $5 | +3-7 pts |
| Recipe A: MLP + hard negatives | 4-8h H100 | $5-10 | +8-14 pts |
| Recipe B: LoRA SigLIP 2 | 10h H100 | $15 | +12-18 pts total |
| GraphSAGE-lite | 20h H100 | $30 | +15-22 pts (if multi-hop signal) |

---

## Part 3: Evaluation

### Building the Test Set (do first, before any training)

```python
# Sample 200 query pins, stratified by cluster
# For each query: take top 50 candidates from current baseline kNN
# Human-label each (relevant=1, borderline=0.5, irrelevant=0)
# Total: 10,000 judgements, ~10-12h work, save to test_pairs.sqlite
# NEVER include test pins in training edges
```

| Metric | Use when |
|---|---|
| Recall@10 | Primary - "show me 10 relevant results" |
| NDCG@10 | Secondary - rewards ordering |
| Precision@5 | "Hero result" quality |

**Decision thresholds:**
- Recall@10 > 55%: ship the baseline, focus on UX
- Recall@10 45-55%: train Recipe A
- Recall@10 < 45%: debug embeddings first, don't train

**Ballpark benchmarks (task-dependent):**
- Frozen CLIP + CSD + color weighted: ~45-55%
- Trained projection head: ~55-65%
- LoRA fine-tuned SigLIP 2: ~60-70%

---

## Part 4: Serving

### Elasticsearch HNSW (recommended for <10M vectors)

```json
// dense_vector mapping with int8 quantisation
{
  "mappings": {
    "properties": {
      "projection_vec": {
        "type": "dense_vector",
        "dims": 256,
        "index": true,
        "similarity": "cosine",
        "index_options": {
          "type": "int8_hnsw",
          "m": 32,
          "ef_construction": 200
        }
      }
    }
  }
}
```

```python
# kNN query with num_candidates tuning
body = {
    "knn": {
        "field": "projection_vec",
        "query_vector": query_embedding.tolist(),
        "k": 10,
        "num_candidates": 200  # never below k*10
    }
}
```

**int8 quantisation stats:**
- Memory: 4x reduction (768-d: 2.5 GB -> 625 MB for 430K; 256-d: much less)
- Recall drop: ~1.5%
- One mapping change, no code change

### Hybrid Retrieval via RRF

```python
# ES Reciprocal Rank Fusion: dense visual + sparse tag signals
body = {
    "retriever": {
        "rrf": {
            "retrievers": [
                {"knn": {"field": "projection_vec", "query_vector": vec, "k": 50}},
                {"standard": {"query": {"terms": {"color_tags": query_tags}}}},
                {"standard": {"query": {"terms": {"mood_tags": query_moods}}}}
            ],
            "rank_constant": 60,
            "rank_window_size": 100
        }
    }
}
# Expected lift: 5-15% NDCG over dense-only for visual similarity
```

### Cold Start

Content-based embedding = immediate availability for new items. No engagement warmup needed:
1. Compute CSD + CLIP + DINOv3 + color features (~100-300ms on GPU)
2. Pass through projection head (<1ms)
3. Index in ES - available immediately

## Gotchas

- **CSD and CLIP have different operating ranges for cosine similarity.** CLIP [0.1-0.5] for unrelated, [0.6-0.9] for similar. CSD ranges differ. Normalize both to z-scores before weighted sum, or your weights will be meaningless.
- **Backbone feature cache is critical.** Don't run CLIP/CSD/DINOv3 every epoch - this wastes 90% of GPU on redundant forward passes. Precompute once to Parquet, load during training. At 50M images the difference is 500h vs 30h of training.
- **Projection head over-parameterization.** >3 hidden layers or >2048 hidden dim overfits 7M pairs. Keep it small.
- **InfoNCE requires L2 normalization.** Forgetting the L2 norm before loss computation is the #1 implementation bug.
- **ES kNN is approximate.** Low `num_candidates` gives fast but imprecise results. Never set below k*10.
- **Backbone version pinning.** Freeze a specific version (e.g., `SigLIP-2-ViT-L/14-384-v1`) and never auto-update. Upstream backbone drift silently invalidates all indexed vectors.
- **Test set leakage.** Hold out the 200 query pins completely from training edges. Check by pin_id, not just edge membership.

## See Also

- [[image-similarity-scaling]] - scaling to 5M-50M images: Qdrant, PostgreSQL, Parquet features
- [[graph-neural-networks]] - PinSage, LightGCN, GraphSAGE for graph-structured training
- [[vector-databases]] - HNSW tuning, quantization, hybrid retrieval
- [[unsupervised-learning]] - InfoNCE, SimCLR, MoCo, hard negative mining
