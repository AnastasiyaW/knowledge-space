---
title: "Recherche vectorielle à grande échelle"
category: reference
tags: [vector-search, faiss, elasticsearch, embeddings, ann, ivfflat, knn, sqlite, hybrid-search]
level: 3
source_sha256: 3c21f841e0813d5932a4388bf689759f9293376152a2ba7ae1bad3c7ffea6f86
translation: machine
translated_at: '2026-10-24'
---
# Recherche vectorielle à grande échelle {#vector-search-at-scale}

Passer de la recherche de similarité basée sur des embeddings, de quelques dizaines de milliers à plusieurs millions de vecteurs. Couvre les backends de stockage, les types d'index, les architectures hybrides et les chemins de migration.

## Faits clés {#key-facts}

- FAISS FlatIP : recherche exacte, O(n) par requête, tous les vecteurs en RAM - limite atteinte vers ~100K vecteurs pour la latence, ~10M pour la RAM
- FAISS IVFFlat : approximatif, ~95 % de rappel, 10x plus rapide - nécessite un entraînement sur des données représentatives avant utilisation
- SQLite comme magasin de métadonnées vectorielles remplace les registres JSON : recherche en O(1), écritures transactionnelles, pas de chargement complet au démarrage
- Elasticsearch `dense_vector` avec kNN prend en charge la recherche approximative comme exacte et permet le filtrage hybride
- Règle empirique : <100K vecteurs → FlatIP exact ; 100K-10M → IVFFlat ; >10M → HNSW (Faiss ou base de données vectorielle dédiée)
- Motif EXIF/métadonnées comme source de vérité : SQLite et les index de recherche sont des caches reconstructibles

## Architecture de stockage {#storage-architecture}

### Seuils d'échelle {#scale-thresholds}

| Échelle | Coût RAM (float32, 768-d) | Backend recommandé |
|---------|---------------------------|--------------------|
| <100K vecteurs | 300 Mo | FAISS FlatIP (exact) |
| 100K-1M | 3 Go | FAISS IVFFlat (approximatif) |
| 1M-10M | 30 Go | FAISS IVFFlat + persistance sur disque |
| >10M | trop volumineux pour la RAM | Base de données vectorielle dédiée (Weaviate, Qdrant, Milvus) |

### SQLite comme couche de métadonnées {#sqlite-as-metadata-layer}

Remplacer les registres JSON par SQLite supprime le chargement complet au démarrage et permet des recherches en O(1).

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

### Index FAISS avec persistance sur disque {#faiss-index-with-disk-persistence}

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

**Paramètres IVFFlat :**
- `n_lists` = `sqrt(n)` est une bonne valeur par défaut (compromis entre vitesse et rappel)
- `index.nprobe = 10` au moment de la recherche contrôle le compromis rappel/vitesse (plus élevé = plus précis, plus lent)
- L'entraînement nécessite un échantillon représentatif ; ajouter des vecteurs après l'entraînement ne réentraîne pas les centroïdes

## Intégration kNN d'Elasticsearch {#elasticsearch-knn-integration}

### Mapping de l'index {#index-mapping}

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

### Requête hybride : filtre + kNN {#hybrid-query-filter-knn}

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

### Synchronisation de SQLite vers Elasticsearch {#sync-from-sqlite-to-elasticsearch}

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

## Pipelines de clustering par similarité {#similarity-clustering-pipelines}

### Affectation de domaines par K-means (FAISS GPU) {#k-means-domain-assignment-faiss-gpu}

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

### Clustering Leiden multi-résolution (Explorer) {#multi-resolution-leiden-clustering-explorer}

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

## Motif de migration (registre JSON → SQLite) {#migration-pattern-json-registry-sqlite}

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

## Chiffres de performance (référence) {#performance-numbers-reference}

| Opération | Échelle | Durée | Notes |
|-----------|---------|-------|-------|
| Construction FAISS (FlatIP) | 100K vecteurs, 768-d | ~2s | CPU |
| Construction FAISS (IVFFlat) | 1M vecteurs, 768-d | ~3,5 min | Inclut le scroll ES |
| Sauvegarde FAISS vers ES | 1M domaines | ~10 min | lots via update_by_query |
| Projection UMAP | 430K x 768-d | ~20 min | CPU |
| Leiden (1 résolution) | 430K sommets | ~40s | igraph CPU |
| Requête kNN ES | — | 5-15ms | par requête |
| Upsert SQLite | — | <1ms | par ligne |
| Scroll ES de 170K noms de fichiers | — | ~2 min | scroll avec taille 1000 |

## Estimations de taille pour 1M de vecteurs {#data-size-estimates-at-1m-vectors}

| Composant | Taille |
|-----------|--------|
| SQLite (768-d + 1024-d + métadonnées) | ~8 Go |
| FAISS FlatIP csd.index (768-d) | 3 Go de RAM |
| FAISS IVFFlat csd.index | 300 Mo de RAM + 3 Go sur disque |
| Elasticsearch (dense_vector 768-d) | ~10 Go sur disque |
| Registre JSON (obsolète) | >100 Mo, chargement complet au démarrage |

## Pièges {#gotchas}

- **IVFFlat nécessite un entraînement avant l'ajout de vecteurs** - appeler `index.add()` sans `index.train()` au préalable produit silencieusement des résultats erronés pour IVFFlat. Vérifiez toujours `index.is_trained` avant d'ajouter des vecteurs
- **Le scroll ES est lent pour les reprises** - charger plus de 170K identifiants de documents via scroll pour vérifier ce qui est déjà indexé prend plus de 2 minutes. Mieux vaut stocker le statut d'indexation dans SQLite et ignorer complètement le scroll ES
- **save_domains_to_es est le goulot d'étranglement** - mettre à jour le champ domain_id un cluster à la fois via update_by_query est lent (655 clusters × plusieurs lots = plus de 10 minutes). Utilisez plutôt une mise à jour groupée avec `update_by_query` et un `script` filtrant par plage de cluster_id
- **UMAP sur plus de 400K points nécessite un échantillonnage** - un UMAP complet sur 430K x 768-d prend 15 à 20 min sur CPU. Pour les explorateurs interactifs, utilisez un échantillonnage stratifié (5K-10K points) avec des affectations de clusters précalculées ; le canvas du navigateur gère bien 5K éléments mais peine au-delà de 10K nœuds DOM
- **Chargement mmap vs chargement complet de FAISS** - `IO_FLAG_MMAP` offre un temps de démarrage quasi nul, mais les premières requêtes sont plus lentes (défauts de page). Utilisez mmap pour les serveurs qui reçoivent des requêtes dès le démarrage ; utilisez le chargement complet pour les traitements par lots
- **nprobe d'IVFFlat doit être défini au moment de la requête** - la valeur par défaut nprobe=1 donne un rappel médiocre. Définissez `index.nprobe = 64` (ou `nlist/4`) pour les requêtes en production

## Voir aussi {#see-also}

- [[data-science/dimensionality-reduction]] - UMAP, PCA, t-SNE
- [[data-engineering/apache-kafka]] - pipeline d'embeddings en flux
- [[data-engineering/etl-elt-pipelines]] - pipelines d'embeddings par lots
- [[data-science/recommender-systems]] - filtrage collaboratif basé sur l'ANN
