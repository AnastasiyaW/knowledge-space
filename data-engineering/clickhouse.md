---
title: ClickHouse
category: concepts
tags: [clickhouse, olap, columnar, mergetree, analytics, column-oriented]
---

# ClickHouse

ClickHouse is an open-source column-oriented OLAP database management system. It is designed for real-time analytical queries on large datasets (billions of rows), delivering sub-second response times through columnar storage, vectorized execution, and aggressive data compression.

## Key Facts

- **Column-oriented**: stores each column separately on disk. Analytical queries reading 5 out of 100 columns only scan 5% of data. Ideal for [[data-warehouse]] workloads
- **MergeTree engine family**: the core table engine. Data is written in parts (sorted by primary key), merged in background. Variants:
  - `MergeTree` - base engine with sorting, primary key index, TTL
  - `ReplacingMergeTree` - deduplicates rows by sorting key (eventual, not immediate)
  - `SummingMergeTree` - auto-aggregates numeric columns during merge
  - `AggregatingMergeTree` - stores intermediate aggregation states
  - `CollapsingMergeTree` / `VersionedCollapsingMergeTree` - handles updates via sign column
- **Log engines**: SimpleLog, TinyLog, StripeLog. For small temporary tables, no indexing or merging
- **Integration engines**: connect to external systems (MySQL, PostgreSQL, Kafka, S3, HDFS) as virtual tables
- SQL syntax close to MySQL/PostgreSQL with extensions: `arrayJoin`, `groupArray`, `groupUniqArray`, `quantile`, `any`, `argMax`, `argMin`
- **Sparse primary index**: not a B-tree. Stores one index entry per granule (8192 rows by default). Enables fast range scans but not single-row lookups
- Compression: LZ4 (default, fast) or ZSTD (better ratio). Column homogeneity enables 5-10x compression vs row-oriented databases
- Optimized for throughput, not latency. Batch inserts recommended (1000+ rows); single-row inserts create excessive parts

## Patterns

### Table creation with MergeTree

```sql
CREATE TABLE events (
    event_date  Date,
    event_time  DateTime,
    user_id     UInt64,
    event_type  LowCardinality(String),
    platform    LowCardinality(String),
    revenue     Float64
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, user_id)
TTL event_date + INTERVAL 1 YEAR;
```

### Analytical queries

```sql
-- CTR by platform
SELECT
    platform,
    countIf(event_type = 'click') AS clicks,
    countIf(event_type = 'view') AS views,
    clicks / views AS ctr
FROM events
WHERE event_date >= '2026-03-01'
GROUP BY platform
ORDER BY ctr DESC;

-- Array aggregation: unique platforms per ad
SELECT
    ad_id,
    arraySort(groupUniqArray(platform)) AS platforms,
    uniqExact(platform) AS platform_count
FROM ads_data
GROUP BY ad_id;

-- Quantile
SELECT quantile(0.95)(ctr) AS p95_ctr FROM ads_stats;
```

### ReplacingMergeTree for deduplication

```sql
CREATE TABLE users (
    user_id   UInt64,
    name      String,
    updated_at DateTime
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY user_id;

-- Query with forced dedup (before merge completes)
SELECT * FROM users FINAL WHERE user_id = 123;
```

## Gotchas

- `SELECT *` without LIMIT on a table with millions of rows will transfer massive data to client. Always use `LIMIT` or filter on partition key
- `FINAL` keyword forces deduplication for ReplacingMergeTree but is slow on large tables. Design queries to tolerate eventual deduplication when possible
- ClickHouse JOINs load the right table into memory. For large-large joins, use `JOIN` with subqueries or dictionary tables. Physical joins (using sorted merge) available in newer versions
- `LowCardinality(String)` dramatically reduces memory usage for columns with <10k distinct values (enums, categories). Always use it for categorical data
- INSERT must be batched. Each INSERT creates a new data part; too many small inserts cause "Too many parts" error. Use Buffer engine or batch at application level
- ClickHouse is NOT a replacement for OLTP databases. No row-level UPDATE/DELETE (only ALTER TABLE mutations, which are heavy background operations)

## See Also

- [[data-warehouse]] - ClickHouse as OLAP engine
- [[data-formats]] - columnar storage benefits
- [[postgresql-for-data-engineering]] - comparison with row-oriented OLTP
- https://clickhouse.com/docs/en/ - ClickHouse documentation
