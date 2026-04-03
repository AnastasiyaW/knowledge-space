---
title: MySQL InnoDB and Storage Engines
category: concepts
tags: [sql-databases, mysql, innodb, myisam, storage-engine, clustered-index, redo-log]
---

# MySQL InnoDB and Storage Engines

MySQL supports pluggable storage engines. InnoDB (default since 5.5) provides ACID transactions, row-level locking, and crash recovery. Understanding engine differences is essential for MySQL administration.

## Storage Engine Comparison

| Engine | Transactions | Locking | Crash Recovery | Notes |
|--------|-------------|---------|----------------|-------|
| **InnoDB** | Yes (ACID) | Row-level | Redo log | Default since 5.5. MVCC, FK support |
| **MyISAM** | No | Table-level | REPAIR TABLE | Legacy. Fast reads, no crash recovery |
| **MEMORY/HEAP** | No | Table-level | N/A (RAM only) | Data lost on restart. Temp tables |
| **Archive** | No | Row-level | N/A | INSERT + SELECT only. High compression |

## InnoDB Architecture

- **Clustered index on PK:** Data physically sorted by primary key. Every table has one.
- **Secondary indexes:** Leaf stores PK value (not row pointer). Lookup requires double hop: secondary index -> find PK -> clustered index -> row data.
- **Redo log:** WAL equivalent. Circular log for crash recovery.
- **Buffer pool:** In-memory cache for data and index pages.
- **MVCC:** Read-committed and repeatable-read via undo logs (row versioning).

### InnoDB vs PostgreSQL Write Behavior

| Operation | InnoDB | PostgreSQL |
|-----------|--------|------------|
| UPDATE | In-place if fits on page | Creates new tuple (full row copy) |
| Secondary index on UPDATE | Only updated if indexed column changes | All indexes updated (unless HOT) |
| Row locking | In memory (lock manager) | In tuple header (xmax field) |

InnoDB has significantly less write amplification for UPDATE-heavy workloads with many secondary indexes.

## MySQL-Specific Lock Types

- **Gap lock:** Locks gap between index records at REPEATABLE READ. Prevents phantom reads.
- **Next-key lock:** Gap + record lock. Default for RR in InnoDB.
- **Insert intention lock:** Allows concurrent inserts at different positions within same gap.
- **MDL (Metadata Lock):** DDL acquires exclusive MDL, blocks until all DML finishes.
- **SX Lock (8.0.20+):** Shared-exclusive for online DDL. Allows concurrent reads AND writes during certain ALTER TABLE operations.

## LSM-Tree Engines

**RocksDB (MyRocks):** Write-optimized LSM-tree engine for MySQL. All writes are sequential (append to WAL + memtable). Background compaction merges SSTables. Better write throughput than InnoDB for write-heavy workloads. Used by Facebook.

**B+Tree vs LSM-Tree:**
- B+Tree (InnoDB): read-optimized, in-place updates, random I/O for writes
- LSM-Tree (RocksDB): write-optimized, sequential writes, read amplification from multiple SSTables

## Key Facts

- InnoDB auto-creates clustered index on PK. Without explicit PK, uses first unique NOT NULL index or hidden 6-byte row_id
- `utf8` in MySQL is 3-byte (no emoji) - always use `utf8mb4`
- `SERIAL` = `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`
- Backtick quotes for identifiers: `` `table` ``, `` `column` ``
- `SHOW ENGINES;` lists available storage engines
- MyISAM is not recommended for new applications

## MySQL Monitoring

```sql
SHOW DATABASES;
SHOW TABLES;
DESCRIBE table_name;
SHOW TABLE STATUS;              -- engine, rows, data/index size
SHOW ENGINE INNODB STATUS\G     -- detailed InnoDB metrics
SELECT VERSION();
```

## Gotchas

- Random UUID as InnoDB PK: worst case - clustered index AND all secondary indexes inherit randomness
- MDL cascade: ALTER TABLE waits for long SELECT, then new SELECTs queue behind ALTER
- InnoDB default isolation is REPEATABLE READ (gap locks can cause unexpected blocking)
- Connection cost: one thread per connection. Use ProxySQL or application pooling for scaling.
- `TRUNCATE TABLE` resets AUTO_INCREMENT in MySQL (unlike PostgreSQL)
- MyISAM `REPAIR TABLE` is not automatic - data can be lost without intervention

## See Also

- [[btree-and-index-internals]] - clustered vs non-clustered indexes
- [[concurrency-and-locking]] - InnoDB lock types
- [[transactions-and-acid]] - isolation levels in MySQL vs PostgreSQL
- [[connection-pooling]] - ProxySQL for MySQL connection management
