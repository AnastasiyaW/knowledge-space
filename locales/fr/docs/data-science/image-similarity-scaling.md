---
title: "Similarité d'images à grande échelle : décisions d'architecture de 430K à 50M"
description: "Parcours de migration concret et décisions d'infrastructure pour les systèmes de similarité d'images qui passent de centaines de milliers à des dizaines de millions de vecteurs : bases de données vectorielles, stockage, pipelines d'entraînement"
level: 4
source_sha256: 886536882ba688a2b2f28a9a5d6c01e90982344b4808d7f2229eb198e75fa3e2
translation: machine
translated_at: '2026-10-24'
---
# Similarité d'images à grande échelle : décisions d'architecture de 430K à 50M {#image-similarity-at-scale-architecture-decisions-from-430k-to-50m}

Décisions d'infrastructure et d'architecture pour les systèmes de similarité d'images au fur et à mesure de leur croissance. Chaque seuil déclenche des goulots d'étranglement différents. Prenez tôt des décisions compatibles avec la suite : le coût de la refonte croît de façon non linéaire.

## Limites strictes par échelle {#hard-limits-by-scale}

### HNSW dans Elasticsearch {#elasticsearch-hnsw}

| Échelle | RAM (int8, 3 index, 768-d) | Latence kNN p99 | kNN filtré | Verdict |
|---|---|---|---|---|
| 430K | ~2 Go | <50ms | OK | Confortable |
| 5M | ~24 Go | 80-150ms | Se dégrade | Surveillable, pression sur le GC |
| 10M | ~48 Go | 150-300ms | Lent | Limite supérieure du confort |
| 50M | ~240 Go | 500-1500ms | Mauvais | Non recommandé |

Formule ES : `num_vectors × (dims + 4)` par index + 30 % de surcharge du graphe HNSW. Les pauses du GC Java font exploser le p99 sous charge concurrente ; Qdrant (en Rust) n'a pas ce problème.

**ES reste pertinent pour 430K-5M. Migrez entre 5 et 10M.**

### Organisation du système de fichiers {#file-system-layout}

Les performances de NTFS/ext4 s'effondrent au-delà d'environ 100K entrées par répertoire. À 50M de fichiers à plat, l'Explorateur ne s'ouvre plus, `DIR` prend des heures et la sauvegarde échoue.

**À faire MAINTENANT, à 430K :**

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

Résultat : 65 536 dossiers feuilles, environ 760 fichiers par dossier à 50M. C'est gérable sur tous les systèmes de fichiers.

### Base de données {#database}

- **SQLite** : un verrou d'écriture global. Suffisant pour 430K avec des workers séquentiels. Se casse dès que l'embedding, le scraping et le nettoyage tournent en parallèle à partir de 5M.
- **PostgreSQL à 5M** : migration avec `pg_loader` en un après-midi si le schéma est déjà compatible PostgreSQL.
- **50M : PostgreSQL + snapshots Parquet** pour 2,5 milliards d'arêtes (200 Go). PostgreSQL pour les requêtes en production, Parquet pour l'entraînement.

---

## Base de données vectorielle à l'échelle de 50M {#vector-db-at-50m-scale}

### Qdrant (recommandé pour les projets d'une seule équipe) {#qdrant-recommended-for-single-team-projects}

Écrit en Rust, sans GC, avec un p99 stable. Principales capacités à 50M :

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

Coût auto-hébergé à 50M (Hetzner AX102, 128 Go de RAM, 2x 1,92 To NVMe) : environ 130 $/mois. Qdrant Cloud géré pour la même capacité : environ 450 à 1200 $/mois.

L'algorithme ACORN (2025) gère bien mieux les kNN à filtres sélectifs que ES : il bascule de façon adaptative entre parcours de graphe et force brute selon la sélectivité du filtre.

### pgvectorscale (option système unique) {#pgvectorscale-single-system-option}

Si les métadonnées sont déjà dans PostgreSQL, consolidez :

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

Un seul système au lieu de deux. Cela sacrifie une partie des performances brutes au profit de la simplicité opérationnelle.

### Quel choix selon le besoin {#when-to-use-what}

| Besoin | Choix |
|---|---|
| 430K-5M, déjà sur ES | Rester sur ES |
| 50M, équipe unique | Qdrant (auto-hébergé) |
| 50M, PostgreSQL nécessaire aussi pour les métadonnées | pgvectorscale |
| 100M+ QPS à grande échelle | Milvus |
| Jamais | Pinecone/Zilliz gérés (3-6K $/mois contre 300 $ en auto-hébergement) |

---

## Pipeline d'entraînement à grande échelle {#training-pipeline-at-scale}

### Cache de features précalculées (critique à partir de 5M) {#precomputed-feature-cache-critical-at-5m}

À 50M d'images, l'inférence du backbone par époque coûte environ 600 $ par passage complet. La solution : extraire une seule fois, puis entraîner la tête de projection sur les features en cache.

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

**Durée d'entraînement avec features précalculées :**

| Échelle | Durée d'entraînement | Coût GPU |
|---|---|---|
| 430K | ~2h H100 | 5 $ |
| 5M | ~8h H100 | 20 $ |
| 50M | ~30h H100 | 80 $ |
| 50M (images brutes, sans cache) | ~500h H100 | 1 500 $ |

**Concevez le cache de features dès maintenant, à 430K.** Il faut un jour pour l'implémenter. Refactoriser la boucle d'entraînement à 10M prend 2 semaines.

### Banque mémoire MoCo pour 50M {#moco-memory-bank-for-50m}

Les négatifs intra-batch (batch de 1024) sont trop peu nombreux à 50M. Une banque mémoire de type MoCo fournit 65K négatifs sur un seul GPU :

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

Batch de 256 + file de 65K = 65K négatifs effectifs par étape. Tient sur un seul GPU. Inutile de recourir à un batch de 4096 ou plus.

---

## Architecture de stockage à 50M {#storage-architecture-at-50m}

### Comparatif du stockage objet (25 To pour 50M × 500 Ko d'images) {#object-storage-comparison-25-tb-for-50m-500-kb-images}

| Fournisseur | Coût mensuel | Sortie de données | Remarques |
|---|---|---|---|
| Wasabi | ~175 $ | Gratuite | Verrouillage de rétention minimal de 90 jours |
| Cloudflare R2 | ~375 $ | Nulle | Idéal pour le niveau chaud/CDN |
| Backblaze B2 | ~375 $ | 3x gratuite | Bon niveau de sauvegarde |
| AWS S3 Standard | ~575 $ + sortie | 0,09 $/Go | À éviter pour cette charge |

**Deux niveaux à 50M :**
1. Wasabi : images originales pleine résolution (archive froide)
2. Cloudflare R2 : miniatures (236px + 474px), soit 50M × 50 Ko = 2,5 To = 37 $/mois

Stockage total : environ 215 $/mois pour l'ensemble à 50M.

### Stockage des arêtes du graphe à 2,5 milliards d'arêtes {#graph-edge-storage-at-25b-edges}

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

Snapshots Parquet sur Wasabi/R2 pour les lectures de l'ensemble complet lors de l'entraînement : on évite ainsi de saturer la base en production.

---

## Parcours de migration {#migration-path}

### Phase 0 (MAINTENANT, à 430K) : mise en place compatible avec la suite {#phase-0-now-at-430k-forward-compatible-setup}

1. **Sharding des fichiers** : migrer vers une organisation hexadécimale à deux niveaux. Quelques minutes à 430K, quelques jours à 50M.
2. **Pipeline de cache de features** : écrire les sorties du backbone en Parquet par lot. Inutilisé pour l'instant, mais à concevoir correctement dès le départ.
3. **Abstraction VectorIndex** : une classe unique encapsulant ES aujourd'hui et Qdrant demain.

```python
class VectorIndex:
    """Abstraction over ES / Qdrant / pgvector. Change backend, not callers."""
    def upsert(self, id: str, vector: np.ndarray, metadata: dict): ...
    def knn_search(self, query_vec: np.ndarray, k: int, filters: dict) -> list: ...
    def hybrid_search(self, query_vec: np.ndarray, sparse_query: dict, k: int) -> list: ...
```

4. **Abstraction des URL d'images** : helper `get_image_url(pin_id)`, point unique où remplacer le système de fichiers par S3/R2 plus tard.
5. **Schéma SQLite compatible PostgreSQL** : utiliser des types de colonnes stricts, éviter les particularités de SQLite. Avec un schéma compatible, la migration `pg_loader` prend un après-midi ; sans, elle prend des semaines.

### Phase 1 (1-5M, environ 6 mois) {#phase-1-1-5m-6-months}

1. Migration vers PostgreSQL pour les métadonnées et les arêtes
2. Stockage froid Wasabi pour les originaux
3. Passer le cache de features en Parquet comme support principal (et non EXIF)
4. Pilote Qdrant avec un échantillon de 1M, comparaison de latence avec ES

### Phase 2 (10-50M) {#phase-2-10-50m}

1. Migration complète vers Qdrant via bascule d'alias
2. Niveau chaud R2 pour les miniatures
3. Boucle d'entraînement MoCo
4. Extraction de features distribuée (4 GPU = 25h de temps réel contre 100h sur un seul GPU)

---

## Synthèse des coûts {#cost-summary}

| Échelle | Serveurs | Stockage | Entraînement/mois | Total/mois |
|---|---|---|---|---|
| 430K | ~20 $ VPS | ~0 $ en local | ~5 $/run | **~20-25 $** |
| 5M | ~95 $ (PG + ES) | ~35 $ Wasabi | ~20 $/run | **~130-150 $** |
| 50M | ~185 $ (Qdrant + PG) | ~215 $ | ~80 $/run | **~400-600 $** |
| 50M géré | ~2000-5000 $ base vectorielle | ~500 $ | ~80 $/run | **~2600-5600 $** |

L'auto-hébergement revient 5 à 10 fois moins cher que le géré à 50M.

## Pièges courants {#gotchas}

- **Les suppressions dans HNSW sont logiques.** Les vecteurs supprimés laissent des arêtes fantômes dans le graphe. ES nécessite un merge/optimize périodique si vous supprimez plus de 10 % des données. Qdrant gère mieux ce cas, mais il requiert aussi une optimisation périodique.
- **Le versionnement des modèles est critique.** Lorsque vous réentraînez et réindexez, gardez les vecteurs anciens et nouveaux accessibles pour les tests A/B. Schéma : `projection_v1`, `projection_v2`. Déployer sans test A/B fait perdre toute mesure de la qualité.
- **La version gratuite d'ES limite les fonctionnalités kNN.** Certaines options HNSW en int8 nécessitent une offre payante. Vérifiez la licence avant de concevoir autour d'elles.
- **Le verrou d'écriture unique de SQLite apparaît plus tôt qu'attendu.** À 5M, avec 3 workers concurrents ou plus (scraper + embedder + nettoyage), vous verrez « database is locked » sous charge soutenue, même en mode WAL.
- **La génération des miniatures se fait une seule fois.** Générez les miniatures de 236px et 474px pendant l'ingestion et mettez-les en cache pour toujours. Ne les régénérez pas à la diffusion : c'est le principal facteur de latence de service à grande échelle.
- **Mise en garde sur le benchmark pgvectorscale.** Le benchmark 471 QPS contre 41 QPS pour Qdrant utilise le cas d'usage optimal de pgvectorscale. Avec une forte concurrence et des filtres complexes, l'approche ACORN de Qdrant l'emporte généralement. Testez les deux selon votre profil d'accès.

## Voir aussi {#see-also}

- [[image-similarity-pipeline]] - construction du pipeline : filtrage du bruit, entraînement, évaluation
- [[vector-databases]] - réglage de HNSW, quantification, RRF hybride
- [[unsupervised-learning]] - MoCo, SimCLR, extraction de négatifs difficiles à grande échelle
- [[pandas-eda]] - Parquet, magasins de features, jeux de données en flux
