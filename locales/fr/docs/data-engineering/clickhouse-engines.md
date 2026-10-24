---
title: "Moteurs de tables ClickHouse"
category: reference
tags: [data-engineering, clickhouse, mergetree, engines, optimization]
level: 3
source_sha256: 967fa6185540395908a712db8081ed787e590241d0397a7de43c62a9f51d1810
translation: machine
translated_at: '2026-10-24'
---
# Moteurs de tables ClickHouse {#clickhouse-table-engines}

Chaque table ClickHouse nécessite un ENGINE. Le moteur détermine le format de stockage, le comportement de fusion et les opérations prises en charge. La famille MergeTree est la base de l'usage en production.

## Famille MergeTree {#mergetree-family}

Les données sont insérées par parts, puis les parts sont fusionnées en arrière-plan. C'est plus efficace que de réécrire les données à chaque insertion.

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

## Guide de sélection du moteur {#engine-selection-guide}

| Moteur | Cas d'usage |
|--------|----------|
| **MergeTree** | Par défaut pour la plupart des scénarios |
| **ReplacingMergeTree** | Upserts, conservation de la dernière version |
| **SummingMergeTree** | Sommes pré-agrégées à l'écriture |
| **AggregatingMergeTree** | Pré-agrégation arbitraire |
| **CollapsingMergeTree** | Suppression logique, annulation |
| **VersionedCollapsingMergeTree** | Suppression logique indépendante de l'ordre |

### ReplacingMergeTree {#replacingmergetree}

```sql
ENGINE = ReplacingMergeTree(version)  -- keeps row with max version
ORDER BY user_id
```

- Déduplication selon la **clé de tri**, et non la PRIMARY KEY
- La déduplication a lieu pendant les fusions en arrière-plan, **pas immédiatement**
- Forcer : `OPTIMIZE TABLE ... FINAL` ou `SELECT ... FROM table FINAL`
- Sans `ver` : conserve la dernière ligne insérée

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

**Sensible à l'ordre :** insérer la ligne originale (sign=1) avant son annulation (sign=-1).

### VersionedCollapsingMergeTree {#versionedcollapsingmergetree}

```sql
ENGINE = VersionedCollapsingMergeTree(sign, version)
```

Même version + signes opposés = collapse. Indépendant de l'ordre (sûr en multi-thread).

## Compression {#compression}

### Algorithmes {#algorithms}

| Algorithme | Idéal pour |
|-----------|---------|
| LZ4 | Par défaut, rapide |
| ZSTD | Compression plus forte, plus lent |
| LZ4HC | LZ4 avec une meilleure compression |

### Codecs (au niveau de la colonne) {#codecs-column-level}

| Codec | Idéal pour |
|-------|---------|
| Delta | Séquences monotones (horodatages) |
| DoubleDelta | Séquences évoluant lentement |
| Gorilla | Colonnes flottantes à faibles variations |
| T64 | Colonnes entières/datetime |

```sql
CREATE TABLE optimized (
    user_id UInt32 CODEC(ZSTD),
    order_date DateTime CODEC(Delta, LZ4),
    amount Float64 CODEC(Gorilla),
    product_id UInt32 CODEC(DoubleDelta, ZSTD)
) ENGINE = MergeTree() ...;
```

**Règle :** définir d'abord les types de données corrects, puis ajouter les codecs.

## Index de saut {#skip-indexes}

```sql
ALTER TABLE t ADD INDEX idx_amount (amount) TYPE minmax GRANULARITY 1;
-- Types: minmax, set(N), bloom_filter
```

## Famille Log (hors production) {#log-family-non-production}

| Moteur | Usage |
|--------|-----|
| TinyLog | Débogage, très petites tables |
| Log | Petites tables, lecture parallèle |
| StripeLog | Petites tables, meilleure insertion |

**N'utilisez jamais les moteurs Log en production.**

## Moteurs d'intégration {#integration-engines}

```sql
ENGINE = PostgreSQL('host:port', 'database', 'table', 'user', 'password');
ENGINE = S3('https://s3.example.com/bucket/*.parquet', 'Parquet');
```

Pris en charge : PostgreSQL, MySQL, HDFS, Kafka, S3, JDBC, ODBC.

## Pièges {#gotchas}
- ReplacingMergeTree sert au nettoyage en arrière-plan, pas à garantir strictement l'unicité
- AggregatingMergeTree : impossible d'insérer des valeurs brutes, utiliser les fonctions `*State`
- CollapsingMergeTree : les insertions désordonnées peuvent ne pas se collapser correctement
- Des types de données corrects économisent plus d'espace que les codecs seuls (189 Mo -> 171 Mo -> 142 Mo)

## Voir aussi {#see-also}
- [[clickhouse]] - Vue d'ensemble de ClickHouse et patterns de requêtes
- [[dwh-architecture]] - Architecture OLAP
