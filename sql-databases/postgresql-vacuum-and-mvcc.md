---
title: PostgreSQL MVCC, VACUUM, and Dead Tuples
category: concepts
tags: [postgresql, mvcc, vacuum, autovacuum, dead-tuples, transaction-id, wraparound, bloat]
---

# PostgreSQL MVCC, VACUUM, and Dead Tuples

PostgreSQL implements concurrency control via MVCC (Multi-Version Concurrency Control). Each UPDATE creates a new tuple version; DELETE marks tuples as dead. VACUUM reclaims space from dead tuples. Understanding this mechanism is essential for maintaining PostgreSQL performance.

## Key Facts

- **MVCC** means every row version (tuple) has `xmin` (transaction that created it) and `xmax` (transaction that deleted/updated it)
- UPDATE = INSERT new version + mark old version dead (sets xmax on old tuple). This is why UPDATE is expensive in PostgreSQL
- DELETE marks tuple dead (sets xmax) but does NOT reclaim space - VACUUM does that
- **Dead tuples** accumulate from UPDATEs and DELETEs. They waste disk space and slow down index scans
- **VACUUM** reclaims dead tuple space for reuse (within the same table). Does NOT return space to OS (use VACUUM FULL for that, but it locks the table)
- **Autovacuum** runs automatically. Triggers based on: `autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor * n_live_tup`
- **Transaction ID wraparound** - PostgreSQL uses 32-bit transaction IDs (4 billion). Must VACUUM to freeze old tuples before IDs wrap around. If VACUUM can't keep up, PostgreSQL shuts down to prevent data corruption
- See [[transactions-and-acid]] for isolation levels that depend on MVCC
- See [[indexes-and-btree]] for how dead tuples cause index bloat

## Patterns

### Checking dead tuples and bloat

```sql
-- Dead tuples per table
SELECT relname, n_dead_tup, n_live_tup,
       round(n_dead_tup::numeric / GREATEST(n_live_tup, 1) * 100, 1) AS dead_pct,
       last_vacuum, last_autovacuum, last_analyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Table bloat estimation
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
       pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS table_size,
       pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;

-- Transaction ID age (monitor for wraparound prevention)
SELECT datname, age(datfrozenxid) AS xid_age,
       pg_size_pretty(pg_database_size(datname)) AS db_size
FROM pg_database
ORDER BY age(datfrozenxid) DESC;
-- WARNING at 200M, shutdown at 2B. If approaching 1B, investigate VACUUM issues.
```

### Autovacuum tuning

```sql
-- Default autovacuum trigger:
-- threshold (50) + scale_factor (0.2) * live_tuples
-- For 1M row table: triggers after 200,050 dead tuples

-- Per-table tuning for high-churn tables
ALTER TABLE hot_table SET (
    autovacuum_vacuum_scale_factor = 0.01,     -- 1% instead of 20%
    autovacuum_vacuum_threshold = 1000,
    autovacuum_analyze_scale_factor = 0.005
);

-- Autovacuum workers configuration (postgresql.conf)
-- autovacuum_max_workers = 3 (default) - increase for many tables
-- autovacuum_vacuum_cost_delay = 2ms (default 20ms in PG <12) - lower = more aggressive
-- autovacuum_vacuum_cost_limit = 200 (default) - higher = more work per cycle
```

### Manual VACUUM operations

```sql
-- Regular VACUUM (reclaims space for reuse, non-blocking)
VACUUM VERBOSE tablename;

-- VACUUM ANALYZE (also updates statistics)
VACUUM ANALYZE tablename;

-- VACUUM FULL (reclaims space to OS, but LOCKS TABLE - avoid in production)
VACUUM FULL tablename;

-- Alternative to VACUUM FULL: pg_repack (online, no lock)
-- pg_repack --table=tablename --dbname=mydb
```

### HOT updates (Heap-Only Tuples)

```sql
-- HOT optimization: if UPDATE doesn't change any indexed column AND
-- new tuple fits on the same page, PostgreSQL uses HOT update
-- (no index update needed, much faster)

-- Check HOT update ratio
SELECT relname, n_tup_upd, n_tup_hot_upd,
       round(n_tup_hot_upd::numeric / GREATEST(n_tup_upd, 1) * 100, 1) AS hot_pct
FROM pg_stat_user_tables
WHERE n_tup_upd > 0
ORDER BY n_tup_upd DESC;

-- Maximize HOT updates:
-- 1. Increase fillfactor (leave room on pages for new versions)
ALTER TABLE hot_table SET (fillfactor = 80);
-- 2. Avoid unnecessary indexes on frequently updated columns
```

## Gotchas

- **Long-running transactions block VACUUM** - VACUUM cannot remove tuples visible to any active transaction. A single idle-in-transaction session can prevent cleanup across entire database
- **VACUUM FULL locks the table** - exclusive lock for the entire duration. For large tables, use pg_repack instead
- **Autovacuum lag on large tables** - default settings may be too conservative for tables with millions of rows. Per-table tuning is essential
- **Index bloat** - regular VACUUM reclaims heap pages but index bloat requires REINDEX or pg_repack. Dead index entries accumulate between VACUUMs
- **Transaction ID wraparound** - if `age(datfrozenxid)` exceeds ~2 billion, PostgreSQL enters single-user mode to force VACUUM. Monitor this metric in production
- **Temporary tables** - not subject to autovacuum; manually VACUUM if long-lived temporary tables accumulate dead tuples

## See Also

- [[transactions-and-acid]] - how MVCC enables different isolation levels
- [[postgresql-configuration-tuning]] - VACUUM and autovacuum related settings
- [PostgreSQL VACUUM docs](https://www.postgresql.org/docs/current/sql-vacuum.html)
- [PostgreSQL routine maintenance](https://www.postgresql.org/docs/current/routine-vacuuming.html)
