---
title: Query Optimization and EXPLAIN
category: concepts
tags: [sql, explain, explain-analyze, query-plan, optimizer, sequential-scan, index-scan, postgresql, mysql]
---

# Query Optimization and EXPLAIN

EXPLAIN reveals how the database engine plans to execute a query. EXPLAIN ANALYZE actually executes the query and shows real timing. Understanding execution plans is essential for diagnosing slow queries and choosing the right indexes.

## Key Facts

- **EXPLAIN** shows the planned execution without running the query. **EXPLAIN ANALYZE** runs the query and shows actual vs estimated metrics
- PostgreSQL EXPLAIN output: nested tree of plan nodes. Each node shows estimated startup cost, total cost, rows, and width
- MySQL EXPLAIN output: tabular format showing tables, join types, key used, rows examined, Extra info
- The optimizer chooses between scan types: Sequential Scan, Index Scan, Index Only Scan, Bitmap Index Scan (PostgreSQL), Bitmap Heap Scan
- **Cost** in PostgreSQL is in arbitrary units (default: seq_page_cost=1.0, random_page_cost=4.0). Lower is better
- Key MySQL EXPLAIN columns: `type` (ALL=full scan, ref=index lookup, eq_ref=unique lookup, range), `rows`, `Extra`
- See [[indexes-and-btree]] for creating indexes to improve plans
- See [[postgresql-configuration-tuning]] for settings that affect optimizer behavior

## Patterns

### PostgreSQL EXPLAIN

```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
-- Output example:
-- Index Scan using idx_orders_customer on orders  (cost=0.42..8.44 rows=5 width=64)
--   Index Cond: (customer_id = 42)

-- EXPLAIN ANALYZE with buffers and timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT c.name, COUNT(o.id)
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.name;

-- JSON format (better for programmatic analysis)
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT ...;
```

### Scan types (PostgreSQL)

```
Seq Scan           - full table scan, reads every page
Index Scan         - traverse B-tree, fetch heap tuples (random I/O)
Index Only Scan    - B-tree has all needed columns (no heap access). Requires visibility map up-to-date (VACUUM)
Bitmap Index Scan  - scan index, build bitmap of pages, then scan heap pages in order. Used for medium selectivity
Bitmap Heap Scan   - follows Bitmap Index Scan to fetch actual rows
```

### Join algorithms

```
Nested Loop        - for each outer row, scan inner (fast for small outer, indexed inner)
Hash Join          - build hash table from inner, probe with outer (fast for equi-joins on larger datasets)
Merge Join         - merge two sorted inputs (fast when both sides are pre-sorted or indexed)
```

### MySQL EXPLAIN key columns

```sql
EXPLAIN SELECT * FROM orders WHERE status = 'active' AND customer_id = 5;
-- type: ref (index lookup), const (unique), range, ALL (full scan)
-- key: which index used
-- rows: estimated rows examined
-- Extra: "Using index" (covering), "Using where" (post-filter),
--        "Using filesort" (sort without index), "Using temporary" (temp table)
```

### Common optimization patterns

```sql
-- Force index usage (PostgreSQL)
SET enable_seqscan = off;  -- for testing only, not production

-- Force index usage (MySQL)
SELECT * FROM orders FORCE INDEX (idx_status) WHERE status = 'active';

-- Check for slow queries (PostgreSQL)
SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;

-- Check for missing indexes (PostgreSQL)
SELECT relname, seq_scan, idx_scan, seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
```

## Gotchas

- **EXPLAIN ANALYZE actually runs the query** - for destructive operations (DELETE, UPDATE), wrap in a transaction and ROLLBACK: `BEGIN; EXPLAIN ANALYZE DELETE ...; ROLLBACK;`
- **Row estimates can be wildly wrong** - if `ANALYZE` hasn't been run recently, statistics are stale. Run `ANALYZE tablename;` to refresh
- **Index Scan vs Seq Scan threshold** - if a query returns >5-10% of the table, the optimizer may choose Seq Scan even with an index available (sequential I/O is faster than many random lookups)
- **Sort operation = no suitable index** - if EXPLAIN shows "Sort" node, the ORDER BY is not served by an index. Consider adding a matching index
- **Nested loop with large outer** - if both sides of a Nested Loop are large, performance degrades quadratically. The optimizer should pick Hash or Merge Join instead; if it doesn't, check statistics
- **MySQL "Using filesort"** - does not necessarily mean disk sort (name is historical). It means a sort operation not served by an index

## See Also

- [[indexes-and-btree]] - creating the right indexes based on EXPLAIN findings
- [[postgresql-configuration-tuning]] - optimizer-related configuration parameters
- [PostgreSQL EXPLAIN docs](https://www.postgresql.org/docs/current/sql-explain.html)
- [MySQL EXPLAIN docs](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)
- [explain.depesz.com](https://explain.depesz.com/) - PostgreSQL EXPLAIN plan visualizer
