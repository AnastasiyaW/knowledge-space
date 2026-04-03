---
title: Index Strategies
category: concepts
tags: [sql-databases, index, composite-index, covering-index, partial-index, sargable, index-only-scan, create-index-concurrently]
---

# Index Strategies

Indexes accelerate reads but slow writes. Choosing which indexes to create, their column order, and type is critical for production performance.

## Index Scan Types (PostgreSQL)

| Scan Type | Description | When Used |
|-----------|-------------|-----------|
| Sequential Scan | Read entire heap page by page | No usable index, large result fraction, small table |
| Index Scan | Traverse B+Tree, fetch heap pages for matches | Selective query, few matching rows |
| Index-Only Scan | Return data from index without heap access | All columns in index (covering), visibility map clean |
| Bitmap Index Scan | Build bitmap of matching pages, read sequentially | Moderate selectivity, multiple indexes combinable |

## Key Facts

- Composite index on (a, b, c) usable for WHERE a=1, WHERE a=1 AND b=2, but NOT for WHERE b=2 alone
- Covering index includes all columns query needs - eliminates heap access entirely
- Partial/filtered index: index only rows matching a condition (smaller, faster to maintain)
- SARGable: `WHERE col = 5` uses index; `WHERE YEAR(col) = 2024` does NOT (function on column)
- Each index adds overhead to INSERT/UPDATE/DELETE - avoid over-indexing in OLTP

## Patterns

### Composite Index
```sql
-- Column order matters: equality columns first, then range
CREATE INDEX idx_orders ON orders (status, created_at);
-- Usable for: WHERE status = 'active' AND created_at > '2024-01-01'
-- Usable for: WHERE status = 'active'
-- NOT usable for: WHERE created_at > '2024-01-01' (skips leftmost column)
```

### Covering Index (Index-Only Scan)
```sql
-- PostgreSQL: INCLUDE for non-key columns in leaf pages
CREATE INDEX idx_orders_covering ON orders (user_id) INCLUDE (amount, status);
-- Query can be answered entirely from index:
SELECT amount, status FROM orders WHERE user_id = 42;
```

### Partial/Filtered Index
```sql
-- Index only active users (much smaller than full index)
CREATE INDEX idx_active_users ON users (email) WHERE status = 'active';
-- Only used when query includes WHERE status = 'active'
```

### CREATE INDEX CONCURRENTLY
```sql
-- PostgreSQL: build index without blocking DML
CREATE INDEX CONCURRENTLY idx_name ON table (column);
-- Takes longer, two table scans, can't run in transaction, may fail (cleanup required)

-- MySQL equivalent: online DDL
ALTER TABLE t ADD INDEX idx_name (column), ALGORITHM=INPLACE, LOCK=NONE;
```

### Generating Test Data
```sql
-- PostgreSQL: generate millions of rows for index testing
INSERT INTO grades (g) SELECT floor(random() * 100) FROM generate_series(1, 10000000);
```

## Optimizer Index Selection

When multiple indexes exist, optimizer estimates cost using:
- Table size and statistics from `pg_stats`
- Index selectivity (what fraction of rows match)
- Correlation (physical ordering vs index ordering)
- Cost parameters (`seq_page_cost`, `random_page_cost`)

Hint mechanisms: `pg_hint_plan` extension (PostgreSQL), `USE INDEX`/`FORCE INDEX` (MySQL). Generally trust the optimizer unless EXPLAIN ANALYZE shows it's wrong.

## SQL Server Specifics

- **Columnstore indexes:** Column-oriented storage for OLAP. Rows grouped into rowgroups (~1M rows), batch mode processing (~900 rows at once). Combinable with rowstore indexes.
- **Hash indexes:** Memory-optimized tables only. O(1) point lookups, not for ranges.
- **Included columns:** Non-key columns in leaf for covering without affecting sort order.

## Gotchas

- Standard `CREATE INDEX` acquires ShareLock (PostgreSQL) - blocks INSERT/UPDATE/DELETE
- CONCURRENTLY can fail and leave invalid index - must DROP and retry
- Index-only scan in PostgreSQL requires visibility map to be clean - run VACUUM first
- Too many indexes on write-heavy tables dramatically slow INSERT/UPDATE/DELETE
- Bitmap scans combine multiple indexes (AND/OR) - sometimes two mediocre indexes beat one perfect one
- MySQL InnoDB secondary indexes always do double lookup through clustered index

## See Also

- [[btree-and-index-internals]] - B+Tree structure and page splits
- [[query-optimization-explain]] - reading EXPLAIN output to verify index use
- [[concurrency-and-locking]] - lock implications of index creation
- [[postgresql-configuration-tuning]] - cost parameters affecting index selection
