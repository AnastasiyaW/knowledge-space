---
title: "Pipeline de similarité d'images : supervision par graphe, entraînement contrastif, recherche vectorielle"
description: "Pipeline de similarité d'images en production, basé sur les backbones CLIP+CSD+DINOv3, l'apprentissage contrastif sur des paires supervisées par graphe, et HNSW d'Elasticsearch, avec filtrage du bruit et méthodologie d'évaluation"
level: 3
source_sha256: 60eb586c758478df819d76dea24bac4d6906c72c8c741d2c1ca90f1aadbc15c7
translation: machine
translated_at: '2026-10-24'
---
# Pipeline de similarité d'images : supervision par graphe, entraînement contrastif, recherche vectorielle {#image-similarity-pipeline-graph-supervision-contrastive-training-vector-search}

Construction d'un système de recherche d'images où la notion de « similaire » est définie par une supervision faible issue d'un graphe (arêtes de co-engagement, par exemple `pin_related` à la manière de Pinterest). Couvre le filtrage du bruit, le choix du backbone, les recettes d'entraînement contrastif et le service via la recherche vectorielle.

**Échelle de référence :** 430K images, 7,2M d'arêtes de graphe, CLIP+CSD+couleur dans Elasticsearch.

## Partie 1 : nettoyage des données d'entraînement supervisées par graphe {#part-1-cleaning-graph-supervised-training-data}

### Nature du bruit {#nature-of-the-noise}

Les graphes de co-engagement (co-sauvegarde, co-clic) génèrent des positifs bruités :

- **Arêtes L1** (même tableau, même session) : de haute qualité, ~90 % de vrais positifs
- **Arêtes L2+** (voisin de voisin) : 10 à 30 % de bruit, dérive thématique plutôt que déchets aléatoires
- **Les faux négatifs sont massifs** : des éléments visuellement identiques provenant de tableaux différents n'ont aucune arête entre eux

Avec 7,2M d'arêtes sur 430K pins (degré moyen d'environ 16,7), il faut s'attendre à 10 à 30 % de bruit d'étiquetage selon les benchmarks publiés.

### Filtrage par cohérence de clusters (sans étiquettes) {#cluster-coherence-filtering-no-labels-needed}

Meilleur retour sur investissement pour une première passe. Nécessite un vecteur d'embedding par image et les affectations de clusters k-means.

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

Sortie attendue : élimine 8 à 15 % comme bruit évident, signale 5 à 10 % pour revue.

**Ne PAS supprimer automatiquement les arêtes L1** (même tableau, même session) : l'utilisateur a explicitement regroupé ces éléments, même si la distance CSD semble incorrecte.

### Recoupement avec le graphe de plus proches voisins {#nn-graph-cross-reference}

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

### Apprentissage actif : classement par désaccord des signaux {#active-learning-signal-disagreement-ranking}

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

Gain attendu avec 2 à 5K étiquettes actives : 3 à 8 points de Recall@10 par rapport à un étiquetage aléatoire.

**Guide de débit d'étiquetage :**
- Binaire côte à côte dans Streamlit/Tkinter (touches A/D/S) : ~800 à 1200 paires/heure
- Interface de formulaire Label Studio : ~200 à 400 paires/heure

### Artefacts de sortie {#output-artifacts}

À sauvegarder pour la reproductibilité et la réutilisation dans l'évaluation des modèles :

```bash
edge_audit.parquet     # src, dst, csd_sim, clip_sim, color_jaccard, z_score, nn_confirmed, verdict
noise_classifier.pkl   # trained on 2K human labels, auto-labels remaining flagged edges
human_labels.sqlite    # 2K reviewed pairs, reuse in test set construction
edges_clean.parquet    # final training edge list
```

---

## Partie 2 : architecture du modèle {#part-2-model-architecture}

### Signaux des backbones {#backbone-signals}

| Backbone | Capture | Dim | Remarques |
|---|---|---|---|
| CLIP ViT-L/14 | Contenu sémantique, concepts | 768 | Remplacer par SigLIP 2 ViT-L pour un gain de 2 à 5 points |
| CSD (Somepalli 2024) | Attributs de style, palettes de couleurs | 768 | Descripteur de style open-source à l'état de l'art |
| DINOv3 (Meta 2025) | Géométrie d'instance, patchs denses | 1024 | +10,9 GAP en recherche d'instances par rapport à DINOv2 |
| Caractéristiques couleur | Luminosité, saturation, température | ~24 | Signal faible, à utiliser uniquement comme départageur |

**SigLIP 2** ([arxiv 2502.14786](https://arxiv.org/abs/2502.14786)) : remplacement direct de CLIP avec une perte sigmoïde, multilingue, meilleure recherche. ViT-L est le compromis optimal pour moins de 1M d'images.

**DINOv3** ([arxiv 2508.10104](https://arxiv.org/html/2508.10104v1)) : les caractéristiques gelées sont quasi à l'état de l'art en recherche sans fine-tuning. À ajouter comme quatrième backbone.

### Architecture recommandée : multi-backbone gelé + tête de projection {#recommended-architecture-frozen-multi-backbone-projection-head}

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

**Configuration d'entraînement (Recette A : 2 à 3 jours, GPU unique) :**
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

**Recette B : fine-tuning LoRA de SigLIP 2 (apporte 3 à 5 points supplémentaires) :**
```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"])
siglip_model = get_peft_model(siglip_model, lora_config)
# Same InfoNCE loss, unfrozen encoder
# Training time: 6-10h H100, cost ~$15
```

### Extraction de négatifs difficiles {#hard-negative-mining}

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

**Piège des faux négatifs :** environ 70 % des paires les plus similaires de votre corpus SONT liées mais absentes du graphe. Appliquer un seuil de marge de similarité (<0,7 en cosinus) aux candidats avant de les traiter comme négatifs.

### Tableau coût / gain {#costlift-table}

| Approche | Durée d'entraînement | Coût GPU | Recall@10 attendu |
|---|---|---|---|
| kNN pondéré (baseline) | 0 | 0 $ | référence |
| Ajuster les poids sur des données étiquetées | 1 h | 0 $ | +3 à 7 pts (gain gratuit) |
| Ajouter le backbone DINOv3 | 1 jour | 5 $ | +3 à 7 pts |
| Recette A : MLP + négatifs difficiles | 4 à 8 h H100 | 5 à 10 $ | +8 à 14 pts |
| Recette B : LoRA SigLIP 2 | 10 h H100 | 15 $ | +12 à 18 pts au total |
| GraphSAGE-lite | 20 h H100 | 30 $ | +15 à 22 pts (si signal multi-sauts) |

---

## Partie 3 : évaluation {#part-3-evaluation}

### Construction de l'ensemble de test (à faire en premier, avant tout entraînement) {#building-the-test-set-do-first-before-any-training}

```python
# Sample 200 query pins, stratified by cluster
# For each query: take top 50 candidates from current baseline kNN
# Human-label each (relevant=1, borderline=0.5, irrelevant=0)
# Total: 10,000 judgements, ~10-12h work, save to test_pairs.sqlite
# NEVER include test pins in training edges
```

| Métrique | Usage |
|---|---|
| Recall@10 | Principale : « montrer 10 résultats pertinents » |
| NDCG@10 | Secondaire : valorise l'ordre |
| Precision@5 | Qualité du « résultat phare » |

**Seuils de décision :**
- Recall@10 > 55 % : livrer la baseline, se concentrer sur l'UX
- Recall@10 entre 45 et 55 % : entraîner la Recette A
- Recall@10 < 45 % : déboguer les embeddings d'abord, ne pas entraîner

**Ordres de grandeur de référence (dépendants de la tâche) :**
- CLIP gelé + CSD + couleur pondérés : ~45 à 55 %
- Tête de projection entraînée : ~55 à 65 %
- SigLIP 2 fine-tuné en LoRA : ~60 à 70 %

---

## Partie 4 : mise en service {#part-4-serving}

### HNSW d'Elasticsearch (recommandé pour moins de 10M de vecteurs) {#elasticsearch-hnsw-recommended-for-10m-vectors}

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

**Statistiques de quantification int8 :**
- Mémoire : réduction par 4 (768 dimensions : 2,5 Go -> 625 Mo pour 430K ; 256 dimensions : bien moins)
- Perte de rappel : ~1,5 %
- Un seul changement de mapping, aucun changement de code

### Recherche hybride via RRF {#hybrid-retrieval-via-rrf}

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

### Démarrage à froid {#cold-start}

Un embedding basé sur le contenu rend les nouveaux éléments disponibles immédiatement. Aucune phase de chauffe liée à l'engagement n'est nécessaire :
1. Calculer les caractéristiques CSD + CLIP + DINOv3 + couleur (~100 à 300 ms sur GPU)
2. Passer par la tête de projection (<1 ms)
3. Indexer dans ES : disponible immédiatement

## Pièges courants {#gotchas}

- **CSD et CLIP ont des plages de valeurs de similarité cosinus différentes.** CLIP : [0,1 à 0,5] pour les éléments non liés, [0,6 à 0,9] pour les éléments similaires. Les plages de CSD diffèrent. Normaliser les deux en scores z avant la somme pondérée, sinon vos poids n'auront aucun sens.
- **Le cache des caractéristiques des backbones est essentiel.** Ne pas exécuter CLIP/CSD/DINOv3 à chaque époque : cela gaspille 90 % du GPU en passes avant redondantes. Précalculer une seule fois dans du Parquet, puis charger pendant l'entraînement. À 50M d'images, la différence est de 500 h contre 30 h d'entraînement.
- **Sur-paramétrage de la tête de projection.** Plus de 3 couches cachées ou une dimension cachée supérieure à 2048 provoquent un surapprentissage sur 7M de paires. La garder petite.
- **InfoNCE exige une normalisation L2.** Oublier la norme L2 avant le calcul de la perte est le bug d'implémentation n° 1.
- **Le kNN d'ES est approximatif.** Un `num_candidates` faible donne des résultats rapides mais imprécis. Ne jamais descendre en dessous de k*10.
- **Épinglage des versions des backbones.** Figer une version précise (par exemple `SigLIP-2-ViT-L/14-384-v1`) et ne jamais la mettre à jour automatiquement. La dérive en amont du backbone invalide silencieusement tous les vecteurs indexés.
- **Fuite de l'ensemble de test.** Exclure totalement les 200 pins de requête des arêtes d'entraînement. Vérifier par pin_id, pas seulement par appartenance aux arêtes.

## Voir aussi {#see-also}

- [[image-similarity-scaling]] - passage à l'échelle de 5M à 50M d'images : Qdrant, PostgreSQL, caractéristiques Parquet
- [[graph-neural-networks]] - PinSage, LightGCN, GraphSAGE pour l'entraînement sur données structurées en graphe
- [[vector-databases]] - réglage de HNSW, quantification, recherche hybride
- [[unsupervised-learning]] - InfoNCE, SimCLR, MoCo, extraction de négatifs difficiles
