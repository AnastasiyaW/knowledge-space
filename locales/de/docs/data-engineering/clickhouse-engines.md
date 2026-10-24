---
title: "ClickHouse-Tabellen-Engines"
category: reference
tags: [data-engineering, clickhouse, mergetree, engines, optimization]
level: 3
source_sha256: 967fa6185540395908a712db8081ed787e590241d0397a7de43c62a9f51d1810
translation: machine
translated_at: '2026-10-24'
---
>
---
title: ClickHouse-Tabellen-Engines
category: reference
tags: [data-engineering, clickhouse, mergetree, engines, optimization]
---

# ClickHouse-Tabellen-Engines {#clickhouse-table-engines}

Jede ClickHouse-Tabelle benötigt eine ENGINE. Die Engine bestimmt das Speicherformat, das Merge-Verhalten und die unterstützten Operationen. Die MergeTree-Familie ist der Kern für den Produktivbetrieb.

## MergeTree-Familie {#mergetree-family}

Daten werden in Teilen (Parts) eingefügt und die Teile im Hintergrund zusammengeführt. Das ist effizienter als bei jedem Insert neu zu schreiben.

```sql
CREATE TABLE events (
    event_date Date,
    event_time DateTime,
    user_id UInt32,
    event_type String,
    event_value Float32
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (user_id, event_date)
PRIMARY KEY (user_id)
SETTINGS index_granularity = 8192;
```

## Leitfaden zur Engine-Auswahl {#engine-selection-guide}

| Engine | Anwendungsfall |
|--------|----------|
| **MergeTree** | Standard für die meisten Szenarien |
| **ReplacingMergeTree** | Upserts, Beibehalten der neuesten Version |
| **SummingMergeTree** | Vorab aggregierte Summen beim Schreiben |
| **AggregatingMergeTree** | Beliebige Vorab-Aggregation |
| **CollapsingMergeTree** | Soft Delete, Stornierung |
| **VersionedCollapsingMergeTree** | Reihenfolgeunabhängiges Soft Delete |

### ReplacingMergeTree {#replacingmergetree}

```sql
ENGINE = ReplacingMergeTree(version)  -- keeps row with max version
ORDER BY user_id
```

- Deduplizierung anhand des **Sortierschlüssels**, nicht des PRIMARY KEY
- Deduplizierung erfolgt während der Hintergrund-Merges - **nicht sofort**
- Erzwingen: `OPTIMIZE TABLE ... FINAL` oder `SELECT ... FROM table FINAL`
- Ohne `ver`: Es bleibt die zuletzt eingefügte Zeile erhalten

### SummingMergeTree {#summingmergetree}

```sql
ENGINE = SummingMergeTree()          -- sums all numeric non-key columns
ENGINE = SummingMergeTree((col1))    -- sums only specified columns
```

### AggregatingMergeTree {#aggregatingmergetree}

```sql
CREATE TABLE user_activity (
    user_id UInt32,
    session_count AggregateFunction(sum, UInt32)
) ENGINE = AggregatingMergeTree()
ORDER BY user_id;

-- Insert with *State functions
INSERT INTO user_activity
SELECT user_id, sumState(CAST(sessions AS UInt32))
FROM raw_data GROUP BY user_id;

-- Read with *Merge functions
SELECT user_id, sumMerge(session_count) FROM user_activity GROUP BY user_id;
```

### CollapsingMergeTree {#collapsingmergetree}

```sql
ENGINE = CollapsingMergeTree(sign)  -- 1 = active, -1 = cancelled
```

**Reihenfolgeabhängig:** Die ursprüngliche Zeile (sign=1) muss vor der Stornierung (sign=-1) eingefügt werden.

### VersionedCollapsingMergeTree {#versionedcollapsingmergetree}

```sql
ENGINE = VersionedCollapsingMergeTree(sign, version)
```

Gleiche Version + entgegengesetzte Vorzeichen = Kollabierung. Reihenfolgeunabhängig (sicher bei Multi-Threading).

## Komprimierung {#compression}

### Algorithmen {#algorithms}

| Algorithmus | Geeignet für |
|-----------|---------|
| LZ4 | Standard, schnell |
| ZSTD | Höhere Kompression, langsamer |
| LZ4HC | LZ4 mit besserer Kompression |

### Codecs (spaltenbezogen) {#codecs-column-level}

| Codec | Geeignet für |
|-------|---------|
| Delta | Monotone Folgen (Zeitstempel) |
| DoubleDelta | Langsam veränderliche Folgen |
| Gorilla | Float-Spalten mit kleinen Änderungen |
| T64 | Integer-/Datetime-Spalten |

```sql
CREATE TABLE optimized (
    user_id UInt32 CODEC(ZSTD),
    order_date DateTime CODEC(Delta, LZ4),
    amount Float64 CODEC(Gorilla),
    product_id UInt32 CODEC(DoubleDelta, ZSTD)
) ENGINE = MergeTree() ...;
```

**Regel:** Zuerst korrekte Datentypen wählen, danach Codecs hinzufügen.

## Skip-Indizes {#skip-indexes}

```sql
ALTER TABLE t ADD INDEX idx_amount (amount) TYPE minmax GRANULARITY 1;
-- Types: minmax, set(N), bloom_filter
```

## Log-Familie (nicht für den Produktivbetrieb) {#log-family-non-production}

| Engine | Verwendung |
|--------|-----|
| TinyLog | Debugging, sehr kleine Tabellen |
| Log | Kleine Tabellen, paralleles Lesen |
| StripeLog | Kleine Tabellen, bessere Inserts |

**Log-Engines niemals im Produktivbetrieb verwenden.**

## Integrations-Engines {#integration-engines}

```sql
ENGINE = PostgreSQL('host:port', 'database', 'table', 'user', 'password');
ENGINE = S3('https://s3.example.com/bucket/*.parquet', 'Parquet');
```

Unterstützt: PostgreSQL, MySQL, HDFS, Kafka, S3, JDBC, ODBC.

## Fallstricke {#gotchas}
- ReplacingMergeTree dient der Bereinigung im Hintergrund, nicht einer strikten Eindeutigkeit
- AggregatingMergeTree: Rohwerte können nicht direkt eingefügt werden - `*State`-Funktionen verwenden
- CollapsingMergeTree: Nicht in der richtigen Reihenfolge eingefügte Zeilen werden unter Umständen nicht korrekt kollabiert
- Korrekte Datentypen sparen mehr Speicher als Codecs allein (189 MB -> 171 MB -> 142 MB)

## Siehe auch {#see-also}
- [[clickhouse]] - ClickHouse-Überblick und Abfragemuster
- [[dwh-architecture]] - OLAP-Architektur
