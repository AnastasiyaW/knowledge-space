---
title: "Bildähnlichkeit im großen Maßstab: Architekturentscheidungen von 430K bis 50M"
description: "Konkreter Migrationspfad und Infrastrukturentscheidungen für Bildähnlichkeitssysteme, die von Hunderttausenden auf Dutzende Millionen Vektoren wachsen – Vektor-DBs, Speicher, Trainingspipelines"
level: 4
source_sha256: 886536882ba688a2b2f28a9a5d6c01e90982344b4808d7f2229eb198e75fa3e2
translation: machine
translated_at: '2026-10-24'
---
# Bildähnlichkeit im großen Maßstab: Architekturentscheidungen von 430K bis 50M {#image-similarity-at-scale-architecture-decisions-from-430k-to-50m}

Infrastruktur- und Architekturentscheidungen für wachsende Bildähnlichkeitssysteme. Jeder Schwellenwert löst andere Engpässe aus. Treffen Sie früh zukunftskompatible Entscheidungen, denn die Kosten für nachträgliche Umbauten wachsen nicht-linear.

## Harte Grenzen nach Umfang {#hard-limits-by-scale}

### Elasticsearch HNSW {#elasticsearch-hnsw}

| Umfang | RAM (int8, 3 Indizes, 768-d) | p99-kNN-Latenz | Gefilterte kNN | Bewertung |
|---|---|---|---|---|
| 430K | ~2 GB | <50ms | OK | Komfortabel |
| 5M | ~24 GB | 80-150ms | Verschlechtert sich | Beobachtbar, GC-Druck |
| 10M | ~48 GB | 150-300ms | Langsam | Obere Komfortgrenze |
| 50M | ~240 GB | 500-1500ms | Schlecht | Nicht empfohlen |

ES-Formel: `num_vectors × (dims + 4)` pro Index + 30 % HNSW-Graph-Overhead. Java-GC-Pausen lassen p99 unter gleichzeitiger Last explodieren. Qdrant (Rust) hat dieses Problem nicht.

**ES bleibt für 430K-5M. Migration zwischen 5-10M.**

### Dateisystem-Layout {#file-system-layout}

NTFS/ext4-Performance bricht ab etwa 100K Einträgen pro Verzeichnis ein. Bei 50M flachen Dateien öffnet sich der Explorer nie, `DIR` dauert Stunden und Backups scheitern.

**Jetzt bei 430K umsetzen:**

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

Ergebnis: 65.536 Blattordner, ~760 Dateien pro Ordner bei 50M. Das ist auf jedem Dateisystem handhabbar.

### Datenbank {#database}

- **SQLite**: globale Schreibsperre. Für 430K mit sequenziellen Workern in Ordnung. Bricht zusammen, wenn Embedding, Scraping und Bereinigung bei 5M+ gleichzeitig laufen.
- **PostgreSQL bei 5M**: `pg_loader`-Migration an einem Nachmittag, sofern das Schema jetzt PostgreSQL-kompatibel ist.
- **50M: PostgreSQL + Parquet-Snapshots** für 2,5 Mrd. Kanten (200 GB). PostgreSQL für Live-Abfragen, Parquet für Training.

---

## Vektor-DB bei 50M {#vector-db-at-50m-scale}

### Qdrant (empfohlen für Projekte mit einem Team) {#qdrant-recommended-for-single-team-projects}

Rust-basiert, ohne GC, konsistenter p99. Zentrale Fähigkeiten bei 50M:

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

Selbst gehostete Kosten bei 50M (Hetzner AX102, 128 GB RAM, 2x 1,92 TB NVMe): ~$130/Monat. Verwaltetes Qdrant Cloud für dieselbe Last: ~$450-1200/Monat.

Der ACORN-Algorithmus (2025) behandelt eng gefilterte kNN-Abfragen deutlich besser als ES. Er wechselt adaptiv zwischen Graph-Traversierung und Brute-Force, abhängig von der Filterselektivität.

### pgvectorscale (Einzelsystem-Option) {#pgvectorscale-single-system-option}

Wenn Metadaten bereits in PostgreSQL liegen, konsolidieren Sie:

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

Ein System statt zwei. Das tauscht etwas Rohleistung gegen betriebliche Einfachheit.

### Wann was verwenden {#when-to-use-what}

| Bedarf | Wahl |
|---|---|
| 430K-5M, bereits auf ES | Bei ES bleiben |
| 50M, ein Team | Qdrant (selbst gehostet) |
| 50M, PostgreSQL auch für Metadaten nötig | pgvectorscale |
| 100M+ QPS im großen Maßstab | Milvus |
| Nie | Verwaltetes Pinecone/Zilliz ($3-6K/Monat statt $300 selbst gehostet) |

---

## Trainingspipeline im großen Maßstab {#training-pipeline-at-scale}

### Vorberechneter Feature-Cache (kritisch ab 5M+) {#precomputed-feature-cache-critical-at-5m}

Bei 50M Bildern kosten Backbone-Inferenzen pro Epoche ~$600 pro Durchlauf. Die Lösung: einmal extrahieren und den Projection Head auf den gecachten Features trainieren.

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

**Trainingszeit mit vorberechneten Features:**

| Umfang | Trainingszeit | GPU-Kosten |
|---|---|---|
| 430K | ~2h H100 | $5 |
| 5M | ~8h H100 | $20 |
| 50M | ~30h H100 | $80 |
| 50M (Rohbilder, ohne Cache) | ~500h H100 | $1.500 |

**Den Feature-Cache jetzt bei 430K entwerfen.** Die Implementierung dauert einen Tag. Eine nachträgliche Umstellung der Trainingsschleife bei 10M dauert zwei Wochen.

### MoCo-Memory-Bank für 50M {#moco-memory-bank-for-50m}

In-Batch-Negatives (Batch 1024) sind bei 50M zu klein. Eine MoCo-artige Memory-Bank liefert 65K Negatives auf einer einzelnen GPU:

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

Batch 256 + 65K-Queue = 65K effektive Negatives pro Schritt. Passt auf eine einzelne GPU. Keine Batch-Größe von 4096+ nötig.

---

## Speicherarchitektur bei 50M {#storage-architecture-at-50m}

### Vergleich Objektspeicher (25 TB für 50M × 500 KB Bilder) {#object-storage-comparison-25-tb-for-50m-500-kb-images}

| Anbieter | Monatliche Kosten | Egress | Hinweise |
|---|---|---|---|
| Wasabi | ~$175 | Kostenlos | 90-Tage-Mindestaufbewahrung (Retention Lock) |
| Cloudflare R2 | ~$375 | Null | Am besten für Hot-/CDN-Tier |
| Backblaze B2 | ~$375 | 3x kostenlos | Gute Backup-Stufe |
| AWS S3 Standard | ~$575 + Egress | $0,09/GB | Für diese Last nie |

**Zweistufig bei 50M:**
1. Wasabi: Originalbilder in voller Auflösung (Kaltarchiv)
2. Cloudflare R2: Thumbnails (236px + 474px), 50M × 50 KB = 2,5 TB = $37/Monat

Gesamtspeicher: ~$215/Monat für alles bei 50M.

### Graph-Kantenspeicher bei 2,5 Mrd. Kanten {#graph-edge-storage-at-25b-edges}

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

Parquet-Snapshots auf Wasabi/R2 für Trainingslesevorgänge über den gesamten Datensatz. Das vermeidet, die Live-DB zu überlasten.

---

## Migrationspfad {#migration-path}

### Phase 0 (JETZT, bei 430K): zukunftskompatibles Setup {#phase-0-now-at-430k-forward-compatible-setup}

1. **Datei-Sharding**: auf 2-stufiges Hex-Layout migrieren. Minuten bei 430K, Tage bei 50M.
2. **Feature-Cache-Pipeline**: Backbone-Ausgaben pro Batch in Parquet schreiben. Auch wenn es jetzt ungenutzt bleibt, richtig entwerfen.
3. **VectorIndex-Abstraktion**: eine einzelne Klasse, die heute ES kapselt und morgen Qdrant.

```python
class VectorIndex:
    """Abstraction over ES / Qdrant / pgvector. Change backend, not callers."""
    def upsert(self, id: str, vector: np.ndarray, metadata: dict): ...
    def knn_search(self, query_vec: np.ndarray, k: int, filters: dict) -> list: ...
    def hybrid_search(self, query_vec: np.ndarray, sparse_query: dict, k: int) -> list: ...
```

4. **Bild-URL-Abstraktion**: `get_image_url(pin_id)`-Helper. Eine einzige Stelle, um das Dateisystem später gegen S3/R2 zu tauschen.
5. **PostgreSQL-kompatibles SQLite-Schema**: strikte Spaltentypen verwenden, keine SQLite-Eigenheiten. Mit kompatiblem Schema dauert die `pg_loader`-Migration einen Nachmittag, ohne es Wochen.

### Phase 1 (1-5M, ~6 Monate) {#phase-1-1-5m-6-months}

1. PostgreSQL-Migration für Metadaten und Kanten
2. Wasabi-Kaltspeicher für Originale
3. Feature-Cache als Parquet als primärer Speicher (nicht EXIF)
4. Qdrant-Pilot mit 1M-Stichprobe gegen ES, Latenzen vergleichen

### Phase 2 (10-50M) {#phase-2-10-50m}

1. Vollständige Qdrant-Migration per Alias-Swap
2. R2-Hot-Tier für Thumbnails
3. MoCo-Trainingsschleife
4. Verteilte Feature-Extraktion (4 GPUs = 25h Laufzeit vs. 100h auf einer GPU)

---

## Kostenübersicht {#cost-summary}

| Umfang | Server | Speicher | Training/Monat | Gesamt/Monat |
|---|---|---|---|---|
| 430K | ~$20 VPS | ~$0 lokal | ~$5/Lauf | **~$20-25** |
| 5M | ~$95 (PG + ES) | ~$35 Wasabi | ~$20/Lauf | **~$130-150** |
| 50M | ~$185 (Qdrant + PG) | ~$215 | ~$80/Lauf | **~$400-600** |
| 50M verwaltet | ~$2000-5000 Vektor-DB | ~$500 | ~$80/Lauf | **~$2600-5600** |

Selbst gehostet ist bei 50M 5-10x günstiger als verwaltet.

## Stolpersteine {#gotchas}

- **HNSW-Löschungen sind weich.** Gelöschte Vektoren hinterlassen Geister-Kanten im Graphen. ES erfordert periodisches Merge/Optimieren, wenn mehr als 10 % der Daten gelöscht werden. Qdrant handhabt das besser, braucht aber trotzdem periodische Optimierung.
- **Modellversionierung ist entscheidend.** Wenn Sie neu trainieren und neu indexieren, halten Sie alte und neue Vektoren für A/B-Tests zugänglich. Schema: `projection_v1`, `projection_v2`. Ein Rollout ohne A/B-Test verliert jede Qualitätsmessung.
- **Das kostenlose ES-Tier schränkt kNN-Features ein.** Einige int8-HNSW-Optionen erfordern das kostenpflichtige Tier. Prüfen Sie die Lizenz, bevor Sie Designs darauf aufbauen.
- **Die Single-Writer-Sperre von SQLite greift früher als erwartet.** Bei 5M mit 3+ gleichzeitigen Workern (Scraper, Embedder, Bereinigung) sehen Sie unter Dauerlast "database is locked", auch im WAL-Modus.
- **Thumbnail-Erzeugung ist einmalig.** 236px- und 474px-Thumbnails beim Import erzeugen und dauerhaft cachen. Nicht bei der Auslieferung neu erzeugen. Das ist der größte Latenzfaktor bei der Auslieferung im großen Maßstab.
- **Vorbehalt zum pgvectorscale-Benchmark.** Der Benchmark mit 471 QPS vs. 41 QPS für Qdrant nutzt den Sweet Spot von pgvectorscale. Bei hoher Parallelität und komplexen Filtern gewinnt typischerweise Qdrants ACORN-Ansatz. Testen Sie beide für Ihr Zugriffsmuster.

## Siehe auch {#see-also}

- [[image-similarity-pipeline]] - Aufbau der Pipeline: Rauschfilterung, Training, Evaluation
- [[vector-databases]] - HNSW-Tuning, Quantisierung, Hybrid-RRF
- [[unsupervised-learning]] - MoCo, SimCLR, Hard-Negative-Mining im großen Maßstab
- [[pandas-eda]] - Parquet, Feature Stores, Streaming-Datasets
