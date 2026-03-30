---
title: MySQL InnoDB Specifics
category: reference
tags: [mysql, innodb, clustered-index, buffer-pool, redo-log, undo-log, gap-lock, auto-increment]
---

# MySQL InnoDB Specifics

InnoDB is the default (and recommended) storage engine for MySQL. Understanding InnoDB's clustered index, buffer pool, locking model, and redo/undo log architecture is essential for MySQL performance tuning and debugging.

## Key Facts

- **Clustered index** - InnoDB stores table data physically ordered by primary key. Every table has a clustered index (PK, or first unique NOT NULL, or hidden row ID)
- **Secondary index** stores the PK value as row pointer. Lookup via secondary index = two B-tree traversals (secondary -> PK -> data)
- **Buffer pool** - InnoDB's main cache for data and index pages. Equivalent to PostgreSQL's shared_buffers but manages everything (no reliance on OS page cache). Set to ~70-80% of available RAM
- **Redo log** (ib_logfile*) - WAL equivalent. Ensures durability. Circular log files. Size affects checkpoint frequency
- **Undo log** - stores old row versions for MVCC and rollback. Lives in system tablespace or separate undo tablespaces
- **Gap locks** - InnoDB locks gaps between index records at REPEATABLE READ to prevent phantom reads. This is different from PostgreSQL's snapshot-based phantom prevention
- See [[transactions-and-acid]] for InnoDB transaction isolation behavior
- See [[indexes-and-btree]] for InnoDB index internals

## Patterns

### InnoDB configuration essentials

```ini
# my.cnf / my.ini
[mysqld]
# Buffer pool (most important setting)
innodb_buffer_pool_size = 12G        # 70-80% of RAM for dedicated MySQL server
innodb_buffer_pool_instances = 8     # reduce contention (1 per GB)

# Redo log
innodb_redo_log_capacity = 4G       # MySQL 8.0.30+ (replaces innodb_log_file_size)
# Pre-8.0.30: innodb_log_file_size = 1G, innodb_log_files_in_group = 2

# I/O
innodb_io_capacity = 2000           # SSD (default 200 for HDD)
innodb_io_capacity_max = 4000       # SSD burst
innodb_flush_method = O_DIRECT      # avoid double-buffering with OS cache

# Concurrency
innodb_thread_concurrency = 0       # let InnoDB manage (recommended)

# Durability
innodb_flush_log_at_trx_commit = 1  # full ACID (0=fastest, 1=safest, 2=compromise)
sync_binlog = 1                     # sync binary log on commit
```

### Monitoring InnoDB

```sql
-- Buffer pool usage
SELECT
    pool_id, pool_size * 16 / 1024 AS pool_size_mb,
    free_buffers * 16 / 1024 AS free_mb,
    database_pages * 16 / 1024 AS data_mb,
    modified_db_pages * 16 / 1024 AS dirty_mb
FROM information_schema.INNODB_BUFFER_POOL_STATS;

-- Buffer pool hit ratio (should be >99%)
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
-- hit ratio = 1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)

-- InnoDB status (comprehensive)
SHOW ENGINE INNODB STATUS\G

-- Lock waits
SELECT * FROM information_schema.INNODB_LOCK_WAITS;
-- MySQL 8.0+
SELECT * FROM performance_schema.data_lock_waits;

-- Long-running transactions
SELECT trx_id, trx_state, trx_started, trx_query
FROM information_schema.INNODB_TRX
ORDER BY trx_started;
```

### InnoDB locking behavior

```sql
-- Gap lock example at REPEATABLE READ
-- Given index on (department): values 'eng', 'hr', 'sales'
SELECT * FROM employees WHERE department = 'hr' FOR UPDATE;
-- This locks: the 'hr' record AND the gaps before/after 'hr'
-- Inserts into the gap (e.g., 'finance') are BLOCKED

-- Record lock only (skip gap lock)
SELECT * FROM employees WHERE id = 5 FOR UPDATE;
-- PK lookup: no gap lock, only record lock

-- Shared lock (SELECT ... FOR SHARE, previously LOCK IN SHARE MODE)
SELECT * FROM accounts WHERE id = 1 FOR SHARE;

-- Skip locked rows (MySQL 8.0+)
SELECT * FROM tasks WHERE status = 'pending'
ORDER BY id LIMIT 1
FOR UPDATE SKIP LOCKED;  -- useful for queue pattern
```

### Primary key design for InnoDB

```sql
-- GOOD: auto-increment PK (sequential inserts, no page splits)
CREATE TABLE events (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BAD: random UUID PK (random inserts, constant page splits, large secondary indexes)
CREATE TABLE events_bad (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),  -- DON'T DO THIS
    event_type VARCHAR(50)
);

-- COMPROMISE: ordered UUID (UUID v7 or custom binary-sorted UUID)
-- Use BINARY(16) for storage efficiency
CREATE TABLE events_better (
    id BINARY(16) PRIMARY KEY,
    event_type VARCHAR(50)
);
```

## Gotchas

- **Clustered index = table** - changing the PK requires rebuilding the entire table. Choose PK carefully at design time
- **Secondary index size** - every secondary index stores the PK value. A 36-byte CHAR UUID PK means every secondary index entry is 36+ bytes larger. Use integer PKs when possible
- **innodb_flush_log_at_trx_commit = 2** - writes redo log to OS buffer on commit (not disk). 100x faster but can lose 1 second of transactions on OS crash. Use 2 for replicas, 1 for primary
- **Gap locks cause unexpected blocking** - common source of lock wait timeouts. Use READ COMMITTED isolation to eliminate gap locks (but lose phantom prevention)
- **Online DDL** - many ALTER TABLE operations in MySQL 8.0+ are online (no table lock), but some still require table copy (changing PK, changing column type). Check MySQL docs for each operation
- **Buffer pool warmup** - after restart, buffer pool is cold. Enable `innodb_buffer_pool_dump_at_shutdown` and `innodb_buffer_pool_load_at_startup` for faster recovery
- **UTF-8 indexing** - `utf8mb4` uses up to 4 bytes per character. A VARCHAR(255) column with utf8mb4 uses 1020 bytes in index key calculation, which may exceed the 3072-byte index prefix limit

## See Also

- [[indexes-and-btree]] - InnoDB B-tree and covering index details
- [[transactions-and-acid]] - InnoDB locking vs PostgreSQL MVCC
- [MySQL InnoDB docs](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)
- [MySQL InnoDB configuration](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html)
