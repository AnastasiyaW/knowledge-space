---
title: Query Optimization and EXPLAIN
category: concepts
tags: [sql-databases, explain, explain-analyze, query-plan, optimizer, sequential-scan, index-scan, postgresql, mysql, performance]
---

# Query Optimization and EXPLAIN

EXPLAIN reveals how the database plans to execute a query. EXPLAIN ANALYZE executes it and shows actual metrics. Understanding plan operators and cost model is essential for diagnosing slow queries.

## EXPLAIN Output

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM orders WHERE user_id = 42;
```

Key output fields:
- **cost:** startup_cost..total_cost in arbitrary units (NOT milliseconds)
- **rows:** estimated rows returned (based on table statistics)
- **width:** average row size in bytes
- **actual time:** milliseconds (only in ANALYZE), first_row..total
- **loops:** how many times this node executed
- **Buffers:** shared hit (cache) vs read (disk)

### Cost Units (PostgreSQL)
```toml
seq_page_cost = 1.0       -- baseline: sequential page read
random_page_cost = 4.0    -- random page read (lower to 1.1-2.0 for SSD)
cpu_tuple_cost = 0.01     -- processing one row
cpu_index_tuple_cost = 0.005
cpu_operator_cost = 0.0025
```

## Plan Node Types

| Operator | Description | Performance Notes |
|----------|-------------|-------------------|
| Seq Scan | Full table scan | Cost proportional to table size |
| Index Scan | B+Tree lookup + heap fetch | 2+ I/Os per row (index + heap) |
| Index Only Scan | All data from index, no heap | Fastest - requires covering index + clean visibility map |
| Bitmap Index Scan | Build bitmap, read pages sequentially | Good for moderate selectivity |
| Nested Loop Join | For each outer row, scan inner | Good when inner has index or is small |
| Hash Join | Build hash from smaller table, probe | Good for large equality joins |
| Merge Join | Both sorted, merge-sort traversal | Good when inputs already sorted |
| Sort | External sort if > work_mem | Creates temp files when memory insufficient |
| Aggregate | GROUP BY processing | Hash or sort-based |
| Gather | Parallel query coordination | |

## Visualization Tools

- https://explain.tensor.ru - interactive plan visualization
- https://tatiyants.com/pev - plan visualizer
- https://explain.depesz.com - detailed analysis

## Query Optimization Checklist

### SQL Level
- Use UNION ALL instead of UNION when duplicates acceptable
- Select only needed columns (avoid `SELECT *`)
- Avoid DISTINCT when possible (often signals bad JOIN)
- For composite indexes, include the first column in queries
- Use EXISTS/IN where applicable
- Small tables: full scan is faster than index scan (fits in one page)
- Functions on indexed columns disable index usage

### Database Level
- Run `ANALYZE` regularly for fresh statistics
- Tune `work_mem` for complex queries with sorts/hashes
- Set `random_page_cost = 1.1-2.0` for SSD storage
- Increase `default_statistics_target` for better cardinality estimates
- Enable `pg_stat_statements` to find slow/frequent queries

### Architecture Level
- Add connection pooler when max_connections > 100-200
- Consider read replicas for read-heavy workloads
- Materialized views for repeated heavy aggregations
- Partition large tables by date/range
- Batch large DML operations

## Patterns

### Diagnosing Stale Statistics
```sql
-- Compare estimated vs actual rows - large discrepancy = stale stats
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'active';
-- If estimated: 100, actual: 50000 -> run ANALYZE
ANALYZE orders;
```

### Forcing Index Use (Testing Only)
```sql
-- PostgreSQL: disable seq scan to test if index would help
SET enable_seqscan = off;
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;
RESET enable_seqscan;

-- MySQL: force specific index
SELECT * FROM orders FORCE INDEX (idx_user_id) WHERE user_id = 42;
```

### Monitoring Extensions
```sql
-- pg_stat_statements: find slowest/most frequent queries
CREATE EXTENSION pg_stat_statements;
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;

-- auto_explain: automatically log slow query plans
ALTER SYSTEM SET auto_explain.log_min_duration = '1s';
```

### Deferred Joins (MySQL Optimization)

When paginating with OFFSET on large tables, the database still reads and discards rows:
```sql
-- SLOW: reads and discards 100000 rows
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000;

-- FAST: deferred join - only fetch IDs first, then join for data
SELECT p.* FROM posts p
INNER JOIN (
    SELECT id FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000
) AS sub ON p.id = sub.id;
-- Inner query uses covering index (id, created_at), outer fetches full rows only for 20 results
```

### Cursor-Based Pagination (Alternative to OFFSET)

```sql
-- Instead of OFFSET (scans discarded rows):
SELECT * FROM posts ORDER BY id DESC LIMIT 20 OFFSET 100000;

-- Use cursor (seeks directly via index):
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 20;
-- O(1) seek vs O(N) scan - cursor pagination is constant time regardless of page depth
```

### Timestamps vs Booleans Pattern

```sql
-- Instead of boolean columns with unclear semantics:
ALTER TABLE orders ADD COLUMN is_shipped BOOLEAN DEFAULT FALSE;

-- Use timestamp - carries both state AND timing:
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMP NULL;
-- NULL = not shipped, non-NULL = shipped (and you know when)
-- WHERE shipped_at IS NOT NULL = WHERE is_shipped = TRUE
-- Bonus: indexable, sortable, auditable
```

### Summary Tables for Expensive Aggregations

```sql
-- Instead of running COUNT(*) GROUP BY on millions of rows:
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY,
    order_count INT,
    total_revenue DECIMAL(12,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate periodically or via trigger
INSERT INTO daily_stats (date, order_count, total_revenue)
SELECT DATE(created_at), COUNT(*), SUM(amount)
FROM orders
WHERE DATE(created_at) = CURRENT_DATE
ON CONFLICT (date) DO UPDATE SET
    order_count = EXCLUDED.order_count,
    total_revenue = EXCLUDED.total_revenue,
    updated_at = CURRENT_TIMESTAMP;
```

### EXPLAIN Red Flags to Watch For

| Red Flag | Meaning | Action |
|----------|---------|--------|
| Seq Scan on large table | Missing or unused index | Add index, check SARGability |
| Rows estimate way off | Stale statistics | `ANALYZE table` |
| Sort with disk | `work_mem` too low | Increase `work_mem` or add sorted index |
| Nested Loop with Seq Scan inner | Missing index on join column | Add index on inner table's join key |
| Hash Join spilling to disk | `work_mem` too low for hash table | Increase `work_mem` |

## Gotchas

- EXPLAIN ANALYZE actually executes the query (including DML!) - wrap in transaction and ROLLBACK
- Plans for 1000-row tables don't extrapolate to millions - planner costs are non-linear
- Single-page tables always get sequential scan regardless of indexes
- EXPLAIN ANALYZE timing excludes network transfer and format conversion
- High `join_collapse_limit` value improves plan but slows planning for many-table JOINs
- After VACUUM, visibility map updated -> Index Only Scan may replace Seq Scan
- MySQL `EXPLAIN` shows estimated plan; `EXPLAIN ANALYZE` (8.0.18+) shows actual execution - always use ANALYZE for real diagnosis
- `SELECT *` prevents index-only scans - specify only needed columns to enable covering index use
- Correlated subqueries execute once per outer row - rewrite as JOIN or use lateral join when possible

## See Also

- [[index-strategies]] - creating and choosing indexes
- [[btree-and-index-internals]] - understanding scan types
- [[postgresql-configuration-tuning]] - planner parameters
- [[postgresql-mvcc-vacuum]] - VACUUM and statistics freshness
