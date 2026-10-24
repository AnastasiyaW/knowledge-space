---
title: "Vektorsuche in großem Maßstab"
category: reference
tags: [vector-search, faiss, elasticsearch, embeddings, ann, ivfflat, knn, sqlite, hybrid-search]
level: 3
source_sha256: 3c21f841e0813d5932a4388bf689759f9293376152a2ba7ae1bad3c7ffea6f86
translation: machine
translated_at: '2026-10-24'
---
# Vektorsuche in großem Maßstab {#vector-search-at-scale}

Skalierung einer embedding-basierten Ähnlichkeitssuche von zehntausenden auf Millionen von Vektoren. Behandelt Speicher-Backends, Indextypen, Hybridarchitekturen und Migrationspfade.

## Kernfakten {#key-facts}

- FAISS FlatIP: exakte Suche, O(n) pro Abfrage, alle Vektoren im RAM - wird ab ca. 100K Vektoren bei der Latenz und ab ca. 10M beim RAM zum Problem
- FAISS IVFFlat: approximativ, ca. 95 % Recall, 10x schneller - muss vor der Verwendung auf repräsentativen Daten trainiert werden
- SQLite als Metadaten-Speicher für Vektoren ersetzt JSON-Registries: O(1)-Lookup, transaktionale Schreibvorgänge, kein vollständiges Laden beim Start
- Elasticsearch `dense_vector` mit kNN unterstützt sowohl approximative als auch exakte Suche und ermöglicht hybride Filterung
- Faustregel: <100K Vektoren → FlatIP exakt; 100K-10M → IVFFlat; >10M → HNSW (Faiss oder dedizierte Vektor-DB)
- Muster EXIF/Metadaten als maßgebliche Quelle: SQLite und Suchindizes sind Caches, die neu aufgebaut werden können

## Speicherarchitektur {#storage-architecture}

### Skalierungsschwellen {#scale-thresholds}

| Umfang | RAM-Bedarf (768-d float32) | Empfohlenes Backend |
|-------|--------------------------|---------------------|
| <100K Vektoren | 300 MB | FAISS FlatIP (exakt) |
| 100K-1M | 3 GB | FAISS IVFFlat (approximativ) |
| 1M-10M | 30 GB | FAISS IVFFlat + Persistenz auf Festplatte |
| >10M | zu groß für den RAM | Dedizierte Vektor-DB (Weaviate, Qdrant, Milvus) |

### SQLite als Metadatenschicht {#sqlite-as-metadata-layer}

Das Ersetzen von JSON-Registries durch SQLite eliminiert das vollständige Laden beim Start und ermöglicht O(1)-Lookups.

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

### FAISS-Index mit Persistenz auf Festplatte {#faiss-index-with-disk-persistence}

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

**IVFFlat-Parameter:**
- `n_lists` = `sqrt(n)` ist ein guter Standardwert (Abwägung zwischen Geschwindigkeit und Recall)
- `index.nprobe = 10` steuert zur Suchzeit den Kompromiss zwischen Recall und Geschwindigkeit (höher = genauer, langsamer)
- Das Training erfordert eine repräsentative Stichprobe; das Hinzufügen von Vektoren nach dem Training trainiert die Zentroide nicht neu

## Elasticsearch-kNN-Integration {#elasticsearch-knn-integration}

### Index-Mapping {#index-mapping}

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

### Hybridabfrage: Filter + kNN {#hybrid-query-filter-knn}

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

### Synchronisation von SQLite nach Elasticsearch {#sync-from-sqlite-to-elasticsearch}

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

## Pipelines für Ähnlichkeitsclustering {#similarity-clustering-pipelines}

### K-Means-Zuweisung von Domänen (FAISS GPU) {#k-means-domain-assignment-faiss-gpu}

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

### Multi-Resolution-Leiden-Clustering (Explorer) {#multi-resolution-leiden-clustering-explorer}

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

## Migrationsmuster (JSON-Registry → SQLite) {#migration-pattern-json-registry-sqlite}

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

## Performance-Kennzahlen (Referenz) {#performance-numbers-reference}

| Operation | Umfang | Zeit | Anmerkungen |
|-----------|-------|------|-------------|
| FAISS-Build (FlatIP) | 100K Vektoren, 768-d | ca. 2 s | CPU |
| FAISS-Build (IVFFlat) | 1M Vektoren, 768-d | ca. 3,5 min | inkl. ES-Scroll |
| FAISS-Speicherung in ES | 1M Domänen | ca. 10 min | update_by_query-Batches |
| UMAP-Projektion | 430K x 768-d | ca. 20 min | CPU |
| Leiden (1 Auflösung) | 430K Knoten | ca. 40 s | igraph CPU |
| ES-kNN-Abfrage | — | 5-15 ms | pro Abfrage |
| SQLite-Upsert | — | <1 ms | pro Zeile |
| ES-Scroll für 170K Dateinamen | — | ca. 2 min | Scroll mit size 1000 |

## Schätzung der Datengrößen bei 1M Vektoren {#data-size-estimates-at-1m-vectors}

| Komponente | Größe |
|-----------|------|
| SQLite (768-d + 1024-d + Metadaten) | ca. 8 GB |
| FAISS FlatIP csd.index (768-d) | 3 GB RAM |
| FAISS IVFFlat csd.index | 300 MB RAM + 3 GB Festplatte |
| Elasticsearch (768-d dense_vector) | ca. 10 GB Festplatte |
| JSON-Registry (veraltet) | >100 MB, vollständiges Laden beim Start |

## Fallstricke {#gotchas}

- **IVFFlat muss vor dem Hinzufügen von Vektoren trainiert werden** - der Aufruf von `index.add()` ohne vorheriges `index.train()` liefert bei IVFFlat stillschweigend falsche Ergebnisse. Prüfe immer `index.is_trained`, bevor du Vektoren hinzufügst
- **ES-Scroll ist für Wiederaufnahme-Muster langsam** - das Laden von über 170K Dokument-IDs per Scroll, um zu prüfen, was bereits indexiert ist, dauert mehr als 2 Minuten. Besser: Indexierungsstatus in SQLite speichern und den ES-Scroll komplett überspringen
- **save_domains_to_es ist der Engpass** - das Aktualisieren des Feldes domain_id jeweils für einen Cluster per update_by_query ist langsam (655 Cluster × mehrere Batches = über 10 Minuten). Verwende stattdessen ein Bulk-Update mit `update_by_query` und einem `script`, das über einen cluster_id-Bereich filtert
- **UMAP auf über 400K Punkten benötigt Sampling** - vollständiges UMAP auf 430K x 768-d dauert auf der CPU 15-20 Minuten. Für interaktive Explorer verwende geschichtetes Sampling (5K-10K Punkte) mit vorberechneten Clusterzuordnungen; der Browser-Canvas verarbeitet 5K gut, hat aber ab etwa 10K DOM-Knoten Probleme
- **FAISS-mmap-Laden vs. vollständiges Laden** - `IO_FLAG_MMAP` ermöglicht nahezu null Startzeit, die ersten Abfragen sind aber langsamer (Page Faults). Verwende mmap für Server, die direkt nach dem Start Abfragen erhalten; verwende das vollständige Laden für Batch-Jobs
- **IVFFlat-nprobe muss zur Abfragezeit gesetzt werden** - der Standardwert nprobe=1 liefert einen schlechten Recall. Setze für Produktionsabfragen `index.nprobe = 64` (oder `nlist/4`)

## Siehe auch {#see-also}

- [[data-science/dimensionality-reduction]] - UMAP, PCA, t-SNE
- [[data-engineering/apache-kafka]] - Streaming-Pipeline für Embeddings
- [[data-engineering/etl-elt-pipelines]] - Batch-Pipelines für Embeddings
- [[data-science/recommender-systems]] - kollaboratives Filtern auf Basis von ANN
