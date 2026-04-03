---
title: PostgreSQL WAL and Durability
category: concepts
tags: [sql-databases, postgresql, wal, write-ahead-log, durability, checkpoint, fsync, crash-recovery]
---

# PostgreSQL WAL and Durability

The Write-Ahead Log (WAL) is the foundation of crash recovery and replication in PostgreSQL. It ensures committed transactions survive any failure by writing changes to a sequential log before modifying data pages.

## How WAL Works

1. Transaction modifies data in shared_buffers (memory)
2. WAL record written to WAL buffers
3. On COMMIT, WAL flushed to disk (sequential write - fast)
4. Actual data pages written lazily by background writer/checkpointer
5. On crash: replay WAL from last checkpoint to reconstruct committed state

WAL segments are 16MB files by default. MySQL InnoDB equivalent: "redo log."

## Key Parameters

```sql
-- WAL detail level
wal_level = replica    -- minimal | replica | logical
-- 'minimal' = crash recovery only
-- 'replica' = streaming replication support
-- 'logical' = logical replication/decoding

-- Durability vs performance
synchronous_commit = on
-- 'on' (default): WAL flushed to disk on each commit (safest)
-- 'off': buffered, async flush. 3x faster, risk ~600ms of lost commits on crash
-- 'remote_apply': WAL applied on replica before confirming

-- Full page writes (torn page protection)
full_page_writes = on  -- write full page to WAL on first modification after checkpoint

-- WAL compression
wal_compression = on   -- reduces WAL size, slight CPU overhead
```

## Checkpoints

Checkpoint: background process flushes all dirty pages to disk, writes checkpoint record to WAL. After checkpoint, older WAL can be recycled.

```sql
-- Checkpoint frequency controls
max_wal_size = '4GB'          -- trigger checkpoint when WAL reaches this size
checkpoint_timeout = '5min'    -- max time between checkpoints
checkpoint_completion_target = 0.9  -- spread I/O over 90% of interval
```

## OS Cache and fsync

OS caches write operations in memory (page cache). Power failure before cache flush = data loss even if database "wrote" the data.

- `fsync()` forces physical disk write - expensive
- Battery-backed write cache (BBWC) on RAID controllers makes fsync fast
- `wal_sync_method = fdatasync` (Linux default) or `open_datasync`

## Durability vs Performance Trade-offs

| Setting | Behavior | Risk |
|---------|----------|------|
| `synchronous_commit = on` | WAL flushed per commit | None - full durability |
| `synchronous_commit = off` | WAL buffered, async flush | Lose last ~600ms of commits |
| Batch commits | Group multiple commits into one fsync | Higher throughput, slight per-tx risk |
| Dedicated WAL disk | Separate disk for WAL files | 2-30x write improvement |

## WAL for Replication

```sql
-- Required for streaming replication
wal_level = replica
max_wal_senders = 10
```

WAL segments streamed to replicas for continuous replication. WAL archiving enables PITR (Point-in-Time Recovery).

## Comparison with Other Databases

| Database | Mechanism | Notes |
|----------|-----------|-------|
| PostgreSQL | WAL (16MB segments) | Sequential log + lazy data writes |
| MySQL InnoDB | Redo log | Similar to WAL, fixed-size circular log |
| Redis | RDB + AOF (optional) | In-memory by design, durability opt-in |
| MongoDB | Journal (WiredTiger) | Checkpoint every 60s or 2GB |
| Cassandra | Commit log + memtable | WAL equivalent + SSTable flush |

## Gotchas

- `synchronous_commit = off` risks losing only the last ~600ms of committed transactions, NOT data corruption
- `full_page_writes = on` roughly doubles WAL size but prevents torn page corruption
- WAL archiving failures break backup chains - monitor `archive_command` success
- Large `max_wal_size` reduces checkpoint frequency but increases recovery time after crash
- Data checksums (`initdb -k` or `pg_checksums`) detect silent corruption but add ~1-2% read overhead

## See Also

- [[transactions-and-acid]] - ACID durability property
- [[backup-and-recovery]] - WAL archiving for PITR
- [[replication-fundamentals]] - WAL-based streaming replication
- [[postgresql-configuration-tuning]] - WAL parameter tuning
