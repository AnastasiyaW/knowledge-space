---
title: PostgreSQL MVCC and VACUUM
category: concepts
tags: [sql-databases, postgresql, mvcc, vacuum, autovacuum, dead-tuples, hot-update, write-amplification, bloat]
---

# PostgreSQL MVCC and VACUUM

PostgreSQL uses Multi-Version Concurrency Control (MVCC) where readers never block writers and vice versa. The trade-off is dead tuples from UPDATE/DELETE that must be cleaned up by VACUUM.

## MVCC Mechanics

Every UPDATE creates a new row version (tuple) in the heap. The old version is marked dead but remains until VACUUM removes it. DELETE marks the tuple dead but doesn't reclaim space. Each transaction sees a consistent snapshot based on its isolation level.

## VACUUM

VACUUM reclaims space from dead tuples and updates statistics for the query planner.

**Regular VACUUM:** Marks dead tuple space as reusable within the table. Does NOT return space to the OS. Allows concurrent reads and writes (SHARE UPDATE EXCLUSIVE lock).

**VACUUM FULL:** Rewrites the entire table, returning space to OS. Blocks ALL access (ACCESS EXCLUSIVE lock). Use only when table is severely bloated.

**Autovacuum:** Background process that runs VACUUM automatically based on dead tuple thresholds. Never disable - stale statistics cause bad query plans and table/index bloat.

## Key Facts

- HOT (Heap-Only Tuple) update avoids index updates if: (1) updated columns not indexed AND (2) new tuple fits on same page
- Autovacuum configuration: `autovacuum_vacuum_threshold` + `autovacuum_vacuum_scale_factor * reltuples`
- `pg_stat_user_tables.n_dead_tup` shows dead tuple count per table
- VACUUM also updates the visibility map (needed for index-only scans)
- PostgreSQL processes: postmaster, backend (per connection), background writer, WAL writer, checkpointer, autovacuum launcher, stats collector

## Patterns

### Monitoring Bloat and Dead Tuples
```sql
-- Dead tuples per table
SELECT schemaname, relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::numeric / GREATEST(n_live_tup, 1) * 100, 2) AS dead_pct,
  last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Table bloat estimation
SELECT * FROM pgstattuple('my_table');

-- Check shared buffer contents
CREATE EXTENSION pg_buffercache;
```

### Autovacuum Tuning
```sql
-- Per-table autovacuum settings for high-churn tables
ALTER TABLE hot_table SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- trigger at 1% dead tuples (default 20%)
  autovacuum_analyze_scale_factor = 0.01,
  autovacuum_vacuum_cost_delay = 0        -- no throttling for this table
);
```

### Adding Column with Default (Pre-PG11)
```sql
-- Pre-PG11: batch update to avoid full table rewrite
ALTER TABLE big_table ADD COLUMN new_col INTEGER;
-- Then batch-update in chunks of 10-100K rows:
UPDATE big_table SET new_col = 42 WHERE id BETWEEN 1 AND 100000;
VACUUM big_table;  -- between batches
-- Finally: ALTER TABLE big_table ALTER COLUMN new_col SET DEFAULT 42;
-- PG 11+: ADD COLUMN with DEFAULT is instant (no rewrite)
```

## PostgreSQL Architecture (Processes)

| Process | Role |
|---------|------|
| Postmaster | Main daemon, forks backends |
| Backend | One per connection - parsing, planning, execution |
| Background Writer | Periodically flushes dirty pages to disk |
| WAL Writer | Flushes WAL buffers to disk |
| Checkpointer | Ensures consistent disk state at checkpoint intervals |
| Autovacuum Launcher | Spawns vacuum workers |
| Stats Collector | Gathers query statistics for optimizer |
| WAL Sender/Receiver | Streaming replication |

Shared memory: shared_buffers (page cache), WAL buffers, lock tables, proc array.

## Gotchas

- Never disable autovacuum - causes stale statistics, bloat, and performance degradation
- VACUUM FULL requires exclusive lock and doubles disk space temporarily
- Long-running transactions prevent VACUUM from cleaning tuples they might still see (transaction ID wraparound risk)
- `idle_in_transaction_session_timeout` prevents long-idle transactions from blocking VACUUM
- Write amplification: UPDATE of any column rewrites entire tuple + updates all indexes (unless HOT)
- Uber's Postgres-to-MySQL migration was motivated by write amplification with many secondary indexes

## See Also

- [[transactions-and-acid]] - MVCC and isolation levels
- [[database-storage-internals]] - pages, heaps, write amplification
- [[concurrency-and-locking]] - lock types during VACUUM
- [[query-optimization-explain]] - stale statistics causing bad plans
