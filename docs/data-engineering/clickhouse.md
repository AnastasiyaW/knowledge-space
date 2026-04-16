---
title: ClickHouse
category: tools
tags: [data-engineering, clickhouse, olap, columnar, analytics, database]
---

# ClickHouse

ClickHouse is a columnar DBMS for OLAP workloads. Created at Yandex for Yandex.Metrica (13 trillion records, 20 billion events/day). Optimized for throughput over latency - billions of rows/sec, ~50ms latency acceptable, ~100 queries/sec per server.

## When to Use ClickHouse

| Profile | Fit |
|---------|-----|
| Log management (flat wide tables, append-only) | Excellent |
| Time series (streaming inserts, simple aggregations) | Excellent |
| Analytical DWH (star/snowflake, ETL inserts) | Good |
| Highly normalized DWH (Data Vault, frequent changes) | Poor |

## What ClickHouse is NOT
Not a full RDBMS: no transactions, no consistency guarantees, no cursors, no stored procedures, no UNIQUE/FOREIGN KEY constraints. PRIMARY KEY does NOT enforce uniqueness. Partial UPDATE/DELETE only (async mutations via ALTER TABLE).

## Columnar Storage

Data stored column-by-column. Reading 3 columns from a wide table reads ~3% of data vs full row scan. Sorted columns compress dramatically via RLE.

**Rule:** Fewer columns in SELECT = less I/O. Always specify needed columns, avoid `SELECT *`.

## Physical Storage

```php
Table
  -> Partitions (independent file groups on disk)
    -> Granules (default 8192 rows)
      -> Files: primary.idx, [column].mrk2, [column].bin
```

### Partition Guidelines
- Attribute MUST appear in queries - otherwise no partition pruning
- Size: few GB to 150 GB per partition
- Typical: `PARTITION BY toYYYYMM(date_column)`

```sql
SELECT partition, formatReadableSize(sum(bytes))
FROM system.parts WHERE table = 'my_table'
GROUP BY partition;
```

## Primary Key and Granules

**Critical rule:** Primary key works left-to-right. For `ORDER BY (a, b, c)`:
- Filter by `a` - uses index
- Filter by `a AND b` - uses index
- Filter by `b` alone - **cannot use index**, reads all granules

**PK in ClickHouse != PK in relational:** No uniqueness, no FK references. Purely an optimization for read performance.

## DML

```sql
INSERT INTO table VALUES (...), (...);
INSERT INTO table SELECT ... FROM other_table;

-- Async mutations (not instant!)
ALTER TABLE table UPDATE col = val WHERE condition;
ALTER TABLE table DELETE WHERE condition;
OPTIMIZE TABLE table FINAL;  -- force merge
```

## ClickHouse-Specific Functions

### Approximate vs Exact Counting

| Function | Accuracy | Performance |
|----------|----------|-------------|
| `uniq()` | Approximate (HyperLogLog) | Fast |
| `uniqExact()` | Exact | Slow, high memory |
| `uniqCombined()` | Hybrid | Balanced |

### Aggregate Suffixes

```sql
sumIf(amount, status = 'completed')   -- conditional sum
countIf(id, type = 'click')           -- conditional count
avgIf(score, score > 0)               -- conditional average
```

### Quantiles

```sql
SELECT quantile(0.5)(price) AS median_approx FROM prices;
SELECT quantileExact(0.5)(salary) AS median_exact FROM employees;
SELECT quantiles(0.25, 0.5, 0.75)(price) AS quartiles FROM prices;
```

## Extended JOINs

| Type | Behavior |
|------|----------|
| LEFT SEMI JOIN | Left rows that have match (no right columns) |
| LEFT ANTI JOIN | Left rows with NO match |
| LEFT ANY JOIN | One random match from right |
| ASOF JOIN | Match by nearest ordered value |

### ASOF JOIN

```sql
SELECT m.time, m.value, e.event
FROM metrics m
ASOF LEFT JOIN events e
  ON m.user_id = e.user_id AND m.time >= e.time;
```

## Query Analysis

```sql
EXPLAIN PLAN indexes = 1 SELECT ...;
```

**Optimal:** filter on BOTH partition key AND primary key for two-stage pruning.

## Gotchas
- UPDATE/DELETE are async mutations - not designed for frequent single-row ops
- ReplacingMergeTree dedup happens during merges - not immediate; use `SELECT ... FINAL`
- Primary key does NOT enforce uniqueness
- UDFs significantly slow down ClickHouse
- Always use correct data types (UInt32 not String for IDs) for compression

## See Also
- [[clickhouse-engines]] - MergeTree family and engine selection
- [[dwh-architecture]] - ClickHouse as OLAP layer
- [[sql-for-de]] - SQL patterns
