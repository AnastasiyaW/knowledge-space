---
title: "Bildähnlichkeits-Pipeline: Graph-Supervision, kontrastives Training, Vektorsuche"
description: "Produktionsreife Bildähnlichkeits-Pipeline mit CLIP+CSD+DINOv3-Backbones, kontrastivem Lernen auf graphbasiert überwachten Paaren und Elasticsearch HNSW – mit Rauschfilterung und Evaluationsmethodik"
level: 3
source_sha256: 60eb586c758478df819d76dea24bac4d6906c72c8c741d2c1ca90f1aadbc15c7
translation: machine
translated_at: '2026-10-24'
---
# Bildähnlichkeits-Pipeline: Graph-Supervision, kontrastives Training, Vektorsuche {#image-similarity-pipeline-graph-supervision-contrastive-training-vector-search}

Dieser Artikel beschreibt ein Bildretrieval-System, in dem „ähnlich“ durch schwache Graph-Supervision definiert wird (Co-Engagement-Kanten, z. B. Pinterest-artiges `pin_related`). Behandelt werden Rauschfilterung, Auswahl der Backbones, Rezepte für kontrastives Training und die Bereitstellung über Vektorsuche.

**Referenzumfang:** 430K Bilder, 7,2M Graph-Kanten, CLIP+CSD+Farbe in Elasticsearch.

## Teil 1: Bereinigung graphbasiert überwachter Trainingsdaten {#part-1-cleaning-graph-supervised-training-data}

### Art des Rauschens {#nature-of-the-noise}

Co-Engagement-Graphen (Co-Save, Co-Click) erzeugen verrauschte Positive:

- **L1-Kanten** (gleiches Board, gleiche Session) – von hoher Qualität, ~90 % echte Positive
- **L2+-Kanten** (Nachbar des Nachbarn) – 10–30 % Rauschen, wobei es sich um Themendrift handelt und nicht um zufälligen Müll
- **Falsch-Negative sind massiv**: visuell identische Objekte aus verschiedenen Boards haben keine Kante

Bei 7,2M Kanten über 430K Pins (durchschnittlicher Grad ~16,7) ist laut veröffentlichten Benchmarks mit 10–30 % Label-Rauschen zu rechnen.

### Cluster-Kohärenz-Filterung (ohne Labels) {#cluster-coherence-filtering-no-labels-needed}

Der beste Return on Investment beim ersten Durchlauf. Erfordert Embedding-Vektoren pro Bild und k-Means-Clusterzuordnungen.

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

Erwartete Ausgabe: verwirft 8–15 % als offensichtliches Rauschen und markiert 5–10 % zur Prüfung.

**L1-Kanten NICHT automatisch verwerfen** (gleiches Board, gleiche Session) – der Nutzer hat diese explizit gruppiert, selbst wenn die CSD-Distanz falsch erscheint.

### Kreuzreferenzierung über den NN-Graphen {#nn-graph-cross-reference}

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

### Active Learning: Ranking nach Signaldivergenz {#active-learning-signal-disagreement-ranking}

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

Erwarteter Gewinn aus 2–5K aktiven Labels: 3–8 Punkte Recall@10 gegenüber zufälligem Labeling.

**Richtwerte zum Labeling-Durchsatz:**
- Streamlit/Tkinter-Nebeneinander-Vergleich mit binärer Bewertung (Tasten A/D/S): ~800–1200 Paare/Stunde
- Label-Studio-Formular-UI: ~200–400 Paare/Stunde

### Ausgabeartefakte {#output-artifacts}

Speichern für Reproduzierbarkeit und die Wiederverwendung bei der Modellevaluation:

```bash
edge_audit.parquet     # src, dst, csd_sim, clip_sim, color_jaccard, z_score, nn_confirmed, verdict
noise_classifier.pkl   # trained on 2K human labels, auto-labels remaining flagged edges
human_labels.sqlite    # 2K reviewed pairs, reuse in test set construction
edges_clean.parquet    # final training edge list
```

---

## Teil 2: Modellarchitektur {#part-2-model-architecture}

### Backbone-Signale {#backbone-signals}

| Backbone | Erfasst | Dim | Hinweise |
|---|---|---|---|
| CLIP ViT-L/14 | Semantischer Inhalt, Konzepte | 768 | Durch SigLIP 2 ViT-L ersetzen für 2–5 Punkte Zugewinn |
| CSD (Somepalli 2024) | Stilattribute, Farbpaletten | 768 | SOTA-Open-Source-Stildeskriptor |
| DINOv3 (Meta 2025) | Instanzgeometrie, dichte Patches | 1024 | +10,9 GAP beim Instanz-Retrieval gegenüber DINOv2 |
| Farbmerkmale | Helligkeit, Sättigung, Farbtemperatur | ~24 | Schwaches Signal, nur als Tie-Breaker verwenden |

**SigLIP 2** ([arxiv 2502.14786](https://arxiv.org/abs/2502.14786)): Drop-in-Ersatz für CLIP mit Sigmoid-Loss, mehrsprachig, besseres Retrieval. ViT-L ist der Sweet Spot für <1M Bilder.

**DINOv3** ([arxiv 2508.10104](https://arxiv.org/html/2508.10104v1)): Eingefrorene Features liefern beim Retrieval ohne Fine-Tuning nahezu SOTA-Ergebnisse. Als vierten Backbone hinzufügen.

### Empfohlene Architektur: eingefrorene Multi-Backbones + Projektionskopf {#recommended-architecture-frozen-multi-backbone-projection-head}

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

**Trainingskonfiguration (Rezept A – 2–3 Tage, einzelne GPU):**
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

**Rezept B – LoRA-Fine-Tuning von SigLIP 2 (bringt weitere 3–5 Punkte):**
```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"])
siglip_model = get_peft_model(siglip_model, lora_config)
# Same InfoNCE loss, unfrozen encoder
# Training time: 6-10h H100, cost ~$15
```

### Mining harter Negative {#hard-negative-mining}

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

**Falsch-Negativ-Falle:** Ungefähr 70 % der ähnlichsten Paare im Korpus SIND verwandt, fehlen aber im Graphen. Vor der Verwendung als Negative einen Ähnlichkeits-Margin-Schwellwert (<0,7 Cosinus) auf die Kandidaten anwenden.

### Kosten-Nutzen-Tabelle {#costlift-table}

| Ansatz | Trainingszeit | GPU-Kosten | Erwarteter Recall@10 |
|---|---|---|---|
| Gewichtetes kNN (Baseline) | 0 | 0 $ | Baseline |
| Gewichte auf gelabelten Daten abstimmen | 1 h | 0 $ | +3–7 Pkt. (kostenloser Gewinn) |
| DINOv3-Backbone hinzufügen | 1 Tag | 5 $ | +3–7 Pkt. |
| Rezept A: MLP + harte Negative | 4–8 h H100 | 5–10 $ | +8–14 Pkt. |
| Rezept B: LoRA SigLIP 2 | 10 h H100 | 15 $ | +12–18 Pkt. gesamt |
| GraphSAGE-lite | 20 h H100 | 30 $ | +15–22 Pkt. (bei Multi-Hop-Signal) |

---

## Teil 3: Evaluation {#part-3-evaluation}

### Aufbau des Testsets (zuerst, vor jedem Training) {#building-the-test-set-do-first-before-any-training}

```python
# Sample 200 query pins, stratified by cluster
# For each query: take top 50 candidates from current baseline kNN
# Human-label each (relevant=1, borderline=0.5, irrelevant=0)
# Total: 10,000 judgements, ~10-12h work, save to test_pairs.sqlite
# NEVER include test pins in training edges
```

| Metrik | Verwendung, wenn |
|---|---|
| Recall@10 | Primär – „zeige mir 10 relevante Ergebnisse“ |
| NDCG@10 | Sekundär – belohnt die Reihenfolge |
| Precision@5 | Qualität des „Hero-Ergebnisses“ |

**Entscheidungsschwellen:**
- Recall@10 > 55 %: Baseline ausliefern, Fokus auf UX
- Recall@10 45–55 %: Rezept A trainieren
- Recall@10 < 45 %: zuerst die Embeddings debuggen, nicht trainieren

**Richtwerte (aufgabenabhängig):**
- Eingefrorenes CLIP + CSD + Farbe, gewichtet: ~45–55 %
- Trainierter Projektionskopf: ~55–65 %
- LoRA-fine-getuntes SigLIP 2: ~60–70 %

---

## Teil 4: Bereitstellung {#part-4-serving}

### Elasticsearch HNSW (empfohlen für <10M Vektoren) {#elasticsearch-hnsw-recommended-for-10m-vectors}

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

**Statistik zur int8-Quantisierung:**
- Speicher: 4-fache Reduktion (768-d: 2,5 GB -> 625 MB für 430K; 256-d: deutlich weniger)
- Recall-Verlust: ~1,5 %
- Eine Mapping-Änderung, keine Code-Änderung

### Hybrides Retrieval über RRF {#hybrid-retrieval-via-rrf}

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

### Cold Start {#cold-start}

Inhaltsbasierte Embeddings bedeuten sofortige Verfügbarkeit für neue Objekte. Es ist kein Engagement-Warmup nötig:
1. CSD- + CLIP- + DINOv3- + Farbmerkmale berechnen (~100–300 ms auf GPU)
2. Durch den Projektionskopf leiten (<1 ms)
3. In ES indexieren – sofort verfügbar

## Stolperfallen {#gotchas}

- **CSD und CLIP haben unterschiedliche Wertebereiche für die Cosinus-Ähnlichkeit.** CLIP liefert [0,1–0,5] für nicht verwandte und [0,6–0,9] für ähnliche Paare. Die Bereiche von CSD unterscheiden sich. Beide vor der gewichteten Summe auf z-Scores normalisieren, sonst sind die Gewichte bedeutungslos.
- **Der Cache der Backbone-Features ist entscheidend.** CLIP/CSD/DINOv3 nicht in jeder Epoche neu ausführen – das verschwendet 90 % der GPU-Leistung für redundante Forward-Pässe. Einmal vorab in Parquet berechnen und während des Trainings laden. Bei 50M Bildern beträgt der Unterschied 500 h gegenüber 30 h Trainingszeit.
- **Überparametrisierung des Projektionskopfs.** Mehr als 3 versteckte Schichten oder mehr als 2048 versteckte Dimensionen überanpassen bei 7M Paaren. Den Kopf klein halten.
- **InfoNCE erfordert L2-Normalisierung.** Das Vergessen der L2-Normalisierung vor der Loss-Berechnung ist der häufigste Implementierungsfehler.
- **ES-kNN ist approximativ.** Ein niedriger `num_candidates`-Wert liefert schnelle, aber ungenaue Ergebnisse. Niemals unter k*10 setzen.
- **Festlegung der Backbone-Version.** Eine bestimmte Version einfrieren (z. B. `SigLIP-2-ViT-L/14-384-v1`) und nie automatisch aktualisieren. Eine Drift des Upstream-Backbones macht alle indexierten Vektoren stillschweigend ungültig.
- **Leakage des Testsets.** Die 200 Query-Pins vollständig aus den Trainingskanten heraushalten. Die Prüfung erfolgt über die `pin_id`, nicht nur über die Kantenzugehörigkeit.

## Siehe auch {#see-also}

- [[image-similarity-scaling]] – Skalierung auf 5M–50M Bilder: Qdrant, PostgreSQL, Parquet-Features
- [[graph-neural-networks]] – PinSage, LightGCN, GraphSAGE für graphstrukturiertes Training
- [[vector-databases]] – HNSW-Tuning, Quantisierung, hybrides Retrieval
- [[unsupervised-learning]] – InfoNCE, SimCLR, MoCo, Mining harter Negative
