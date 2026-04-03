---
title: PostgreSQL Configuration and Tuning
category: reference
tags: [sql-databases, postgresql, configuration, tuning, shared-buffers, work-mem, postgresql-conf, pgbench, performance]
---

# PostgreSQL Configuration and Tuning

PostgreSQL performance depends heavily on proper configuration. Default settings are conservative and suited for development, not production workloads.

## Config File Locations

| OS | Path |
|----|------|
| Ubuntu | `/etc/postgresql/15/main/postgresql.conf` |
| CentOS | `/var/lib/pgsql-15/data/postgresql.conf` |
| macOS | `/usr/local/var/postgres/postgresql.conf` |
| Windows | `C:\Program Files\PostgreSQL\15\data\postgresql.conf` |

Related files: `pg_hba.conf` (authentication), `pg_ident.conf` (user mapping).

## Viewing and Changing Parameters

```sql
SHOW config_file;
SHOW shared_buffers;
SELECT current_setting('max_connections');

-- Persistent change (writes to postgresql.auto.conf, does NOT apply immediately)
ALTER SYSTEM SET shared_buffers = '2GB';
-- Then reload or restart:
SELECT pg_reload_conf();  -- for sighup-context params
-- pg_ctl restart          -- for postmaster-context params

-- Session-level (temporary)
SET work_mem = '256MB';

-- Reset
ALTER SYSTEM RESET shared_buffers;
```

### Parameter Context Types
- `internal` - cannot change (compile-time)
- `postmaster` - requires server restart
- `sighup` - re-read config files (no restart)
- `superuser` - changeable at runtime by superuser
- `user` - changeable at runtime by any user

## Key Performance Parameters

### Memory

| Parameter | Description | Starting Value |
|-----------|-------------|----------------|
| `shared_buffers` | Main page cache | 25% of RAM |
| `effective_cache_size` | Planner hint for total cache (OS + PG) | 75% of RAM |
| `work_mem` | Per-operation sort/hash memory | 10-64MB |
| `maintenance_work_mem` | VACUUM, CREATE INDEX | 256MB-1GB |
| `temp_buffers` | Temporary table memory | Default |
| `huge_pages` | Use huge pages if available | `try` |

**Memory formula:** `shared_buffers + (work_mem + temp_buffers) * max_connections` must not exceed RAM.

**WARNING:** Each sort/hash gets its own work_mem, and a single query may have multiple. `work_mem * active_connections * operations_per_query` must fit in RAM.

### WAL and Checkpoints
| Parameter | Description | Starting Value |
|-----------|-------------|----------------|
| `max_wal_size` | Max WAL between checkpoints | 4-16GB |
| `checkpoint_completion_target` | Spread I/O over checkpoint interval | 0.9 |
| `wal_compression` | Compress WAL records | on |
| `synchronous_commit` | WAL sync on commit | on (safest) |

### Query Planner
| Parameter | Description | Starting Value |
|-----------|-------------|----------------|
| `random_page_cost` | Random page read cost | 1.1-2.0 (SSD) |
| `effective_io_concurrency` | Concurrent I/O requests | 200 (SSD), 500-1000 (NVMe) |
| `default_statistics_target` | Rows sampled for statistics | 100-500 |
| `jit` | JIT compilation | on for analytics |

### Connections
| Parameter | Description | Starting Value |
|-----------|-------------|----------------|
| `max_connections` | Max client connections | 50-200 (use pooler) |
| `idle_in_transaction_session_timeout` | Kill idle transactions | 5-30 min |
| `statement_timeout` | Max query duration | application-specific |

## Network Access

```bash
# postgresql.conf
listen_addresses = '*'

# pg_hba.conf - allow remote connections
host  all  all  0.0.0.0/0  scram-sha-256

sudo pg_ctlcluster 15 main restart
```

## Benchmarking with pgbench

```bash
# Initialize test database (~1.5M rows)
pgbench -h HOST -p 5432 -U postgres -i -s 15 benchmark

# Run test: 50 clients, 2 threads, report every 60s, run 3 minutes
pgbench -h HOST -p 5432 -U postgres -c 50 -j 2 -P 60 -T 180 benchmark
```

## Auto-Tuning Tools

- **pgtune.leopard.in.ua** - web calculator based on hardware specs
- **pgconfigurator.cybertec.at** - advanced configuration generator
- **timescaledb-tune** - CLI tool for automated tuning

## Gotchas

- Default `shared_buffers = 128MB` is far too low for production
- `random_page_cost = 4.0` (default) penalizes index scans on SSD - lower to 1.1-2.0
- Increasing `max_connections` beyond 200 without a pooler causes context switching overhead
- `effective_cache_size` doesn't allocate memory - it's a planner hint
- Same parameter appearing multiple times: last value wins in config file
- `ALTER SYSTEM SET` writes to `postgresql.auto.conf`, overriding `postgresql.conf`

## See Also

- [[connection-pooling]] - PgBouncer when max_connections is insufficient
- [[postgresql-wal-durability]] - WAL tuning details
- [[query-optimization-explain]] - planner cost parameters
- [[postgresql-mvcc-vacuum]] - autovacuum configuration
