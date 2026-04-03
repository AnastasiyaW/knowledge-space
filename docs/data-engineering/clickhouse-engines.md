---
title: ClickHouse Table Engines
category: reference
tags: [data-engineering, clickhouse, mergetree, engines, optimization]
---

# ClickHouse Table Engines

Every ClickHouse table requires an ENGINE. The engine determines storage format, merge behavior, and supported operations. MergeTree family is the core for production use.

## MergeTree Family

Data inserted in parts, parts merged in background. More efficient than rewriting on every insert.

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

## Engine Selection Guide

| Engine | Use Case |
|--------|----------|
| **MergeTree** | Default for most scenarios |
| **ReplacingMergeTree** | Upserts, keeping latest version |
| **SummingMergeTree** | Pre-aggregated sums on write |
| **AggregatingMergeTree** | Arbitrary pre-aggregation |
| **CollapsingMergeTree** | Soft delete, cancellation |
| **VersionedCollapsingMergeTree** | Order-independent soft delete |

### ReplacingMergeTree

```sql
ENGINE = ReplacingMergeTree(version)  -- keeps row with max version
ORDER BY user_id
```

- Dedup by **sorting key**, not PRIMARY KEY
- Dedup happens during background merges - **not immediate**
- Force: `OPTIMIZE TABLE ... FINAL` or `SELECT ... FROM table FINAL`
- Without `ver`: keeps last inserted row

### SummingMergeTree

```sql
ENGINE = SummingMergeTree()          -- sums all numeric non-key columns
ENGINE = SummingMergeTree((col1))    -- sums only specified columns
```

### AggregatingMergeTree

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

### CollapsingMergeTree

```sql
ENGINE = CollapsingMergeTree(sign)  -- 1 = active, -1 = cancelled
```

**Order-sensitive:** insert original (sign=1) before cancellation (sign=-1).

### VersionedCollapsingMergeTree

```sql
ENGINE = VersionedCollapsingMergeTree(sign, version)
```

Same version + opposite signs = collapse. Order-independent (multi-threaded safe).

## Compression

### Algorithms

| Algorithm | Best For |
|-----------|---------|
| LZ4 | Default, fast |
| ZSTD | Higher compression, slower |
| LZ4HC | LZ4 with better compression |

### Codecs (column-level)

| Codec | Best For |
|-------|---------|
| Delta | Monotonic sequences (timestamps) |
| DoubleDelta | Slowly changing sequences |
| Gorilla | Float columns with small changes |
| T64 | Integer/datetime columns |

```sql
CREATE TABLE optimized (
    user_id UInt32 CODEC(ZSTD),
    order_date DateTime CODEC(Delta, LZ4),
    amount Float64 CODEC(Gorilla),
    product_id UInt32 CODEC(DoubleDelta, ZSTD)
) ENGINE = MergeTree() ...;
```

**Rule:** Correct data types FIRST, then add codecs.

## Skip Indexes

```sql
ALTER TABLE t ADD INDEX idx_amount (amount) TYPE minmax GRANULARITY 1;
-- Types: minmax, set(N), bloom_filter
```

## Log Family (Non-Production)

| Engine | Use |
|--------|-----|
| TinyLog | Debugging, tiny tables |
| Log | Small tables, parallel read |
| StripeLog | Small tables, better insert |

**Never use Log engines in production.**

## Integration Engines

```sql
ENGINE = PostgreSQL('host:port', 'database', 'table', 'user', 'password');
ENGINE = S3('https://s3.example.com/bucket/*.parquet', 'Parquet');
```

Supported: PostgreSQL, MySQL, HDFS, Kafka, S3, JDBC, ODBC.

## Gotchas
- ReplacingMergeTree is for background cleanup, not strict uniqueness
- AggregatingMergeTree: cannot insert raw values - use `*State` functions
- CollapsingMergeTree: out-of-order inserts may not collapse correctly
- Correct data types save more space than codecs alone (189 MB -> 171 MB -> 142 MB)

## See Also
- [[clickhouse]] - ClickHouse overview and query patterns
- [[dwh-architecture]] - OLAP architecture
