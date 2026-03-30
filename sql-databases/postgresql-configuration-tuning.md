---
title: PostgreSQL Configuration and Performance Tuning
category: reference
tags: [postgresql, configuration, tuning, shared-buffers, work-mem, wal, connections, pgbouncer]
---

# PostgreSQL Configuration and Performance Tuning

PostgreSQL performance depends on proper configuration of memory, WAL, checkpointing, connections, and OS-level settings. The defaults are intentionally conservative to work on any hardware.

## Key Facts

- **shared_buffers** - PostgreSQL's internal buffer cache. Recommended: 25% of total RAM (rarely beneficial above 40%). Default is extremely low (128MB)
- **work_mem** - memory per sort/hash operation (per query, per operation). Default 4MB. Multiply by max_connections * operations_per_query to estimate total memory usage
- **effective_cache_size** - hint to the query planner about OS page cache size. Set to ~75% of total RAM. Does NOT allocate memory
- **max_connections** - default 100. Each connection uses ~10MB of RAM. Use connection pooling (PgBouncer) instead of increasing this
- **wal_buffers** - WAL write buffer. Default -1 (auto: 1/32 of shared_buffers, max 16MB). Rarely needs manual tuning
- **maintenance_work_mem** - memory for VACUUM, CREATE INDEX, ALTER TABLE. Set higher than work_mem (e.g., 512MB-1GB)
- Configuration file: `postgresql.conf`. Override per-session with `SET`. Some require restart, others reload
- See [[query-optimization-explain]] for how configuration affects planner decisions
- See [[postgresql-vacuum-and-mvcc]] for autovacuum tuning parameters

## Patterns

### Essential parameters (16GB RAM server example)

```ini
# Memory
shared_buffers = 4GB              # 25% of RAM
effective_cache_size = 12GB       # 75% of RAM
work_mem = 64MB                   # per sort/hash op (be careful)
maintenance_work_mem = 1GB        # for VACUUM, CREATE INDEX
huge_pages = try                  # use OS huge pages if available

# WAL
wal_level = replica               # minimum for replication/PITR
max_wal_size = 2GB                # checkpoint trigger
min_wal_size = 512MB
wal_compression = on              # reduce WAL volume

# Checkpoints
checkpoint_completion_target = 0.9  # spread checkpoint I/O
checkpoint_timeout = 15min          # max time between checkpoints

# Connections
max_connections = 200             # use PgBouncer for >200 clients
# Better: max_connections = 50 + PgBouncer in transaction mode

# Query planner
random_page_cost = 1.1            # SSD (default 4.0 for HDD)
effective_io_concurrency = 200    # SSD (default 1 for HDD)

# Parallelism
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
```

### PgBouncer connection pooling

```ini
# pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Pool modes:
# session    - connection held for entire client session (safest, least efficient)
# transaction - connection returned to pool after each transaction (recommended)
# statement  - connection returned after each statement (breaks multi-statement transactions)
pool_mode = transaction

max_client_conn = 1000      # max client connections to PgBouncer
default_pool_size = 25      # connections per (user, database) pair to PostgreSQL
reserve_pool_size = 5       # extra connections when pool is exhausted
```

### Checking current configuration

```sql
-- Show single setting
SHOW shared_buffers;
SHOW work_mem;

-- Show all non-default settings
SELECT name, setting, unit, source
FROM pg_settings
WHERE source != 'default'
ORDER BY name;

-- Check if setting requires restart
SELECT name, setting, pending_restart
FROM pg_settings
WHERE pending_restart;

-- Apply config reload (no restart)
SELECT pg_reload_conf();
-- Or: pg_ctl reload -D /var/lib/postgresql/data
```

### Monitoring key metrics

```sql
-- Buffer cache hit ratio (should be >99%)
SELECT
    sum(blks_hit) * 100.0 / sum(blks_hit + blks_read) AS cache_hit_ratio
FROM pg_stat_database;

-- Active connections
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Long-running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Table I/O statistics
SELECT relname,
       seq_scan, seq_tup_read,
       idx_scan, idx_tup_fetch,
       n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
ORDER BY seq_tup_read DESC;
```

## Gotchas

- **work_mem is per-operation, not per-query** - a single complex query with 5 sorts and 3 hash joins can use `5 * work_mem + 3 * work_mem = 8 * work_mem`. With 200 connections, 64MB work_mem could use 100GB+ total
- **shared_buffers too high is wasteful** - PostgreSQL relies on the OS page cache for the remaining buffer. Setting shared_buffers to 50%+ of RAM leaves too little for OS cache
- **max_connections is not a pool** - each PostgreSQL connection is a separate OS process (~10MB each). 1000 connections = 10GB just for connection overhead. Use PgBouncer
- **random_page_cost = 4 is HDD default** - for SSD, set to 1.1-1.5. Leaving it at 4 makes the planner avoid index scans when they would be faster on SSD
- **Restart vs reload** - `shared_buffers`, `max_connections`, `wal_level`, `huge_pages` require restart. Most other settings need only `pg_reload_conf()`
- **Don't blindly copy configs** - tools like PGTune give starting points, but actual tuning requires monitoring real workload

## See Also

- [[postgresql-vacuum-and-mvcc]] - autovacuum configuration
- [[postgresql-replication-ha]] - WAL settings for replication
- [PostgreSQL resource consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html)
- [PGTune - config calculator](https://pgtune.leopard.in.ua/)
