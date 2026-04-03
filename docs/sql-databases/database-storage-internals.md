---
title: Database Storage Internals
category: concepts
tags: [sql-databases, storage, pages, heap, row-store, column-store, toast, io, disk]
---

# Database Storage Internals

Understanding how databases store and retrieve data on disk is fundamental to performance optimization. Every query ultimately translates to disk I/O operations on pages.

## Storage Architecture

### Pages
The smallest unit of I/O. Reading one row = reading entire page. All rows on that page become available in buffer pool.

| RDBMS | Page Size |
|-------|-----------|
| PostgreSQL | 8 KB |
| MySQL InnoDB | 16 KB |
| SQL Server | 8 KB |

With 1000 rows at 3 rows/page, you get ~334 pages. A full table scan reads all 334 pages.

### Heap
Unordered collection of pages where table data lives. New rows appended to end (no inherent ordering). Full heap scan (sequential scan) reads every page - expensive for selective queries.

### Row_ID / Tuple_ID
Internal system identifier for each row:
- **MySQL InnoDB:** row_id = primary key (clustered index)
- **PostgreSQL:** `ctid` = (page_number, offset) pointing to physical location

### I/O Operations
One I/O reads one or more pages. Goal: minimize I/O count. Some I/Os served from OS cache (no disk hit). I/O is the primary cost metric for query performance.

**SSD vs HDD:** SSD random reads ~0.1ms vs HDD ~10ms (100x faster). SSD sequential only ~4x faster than random (vs HDD 100x). This changes optimization strategies - random I/O less costly on SSD.

## Row vs Column Store

**Row-Oriented (OLTP default):** Entire row stored together on same page.
- Good for: `SELECT * FROM emp WHERE id = 1` (all columns, one row)
- Bad for: `SELECT SUM(salary) FROM emp` (reads all columns to access one)
- Examples: PostgreSQL, MySQL, Oracle, SQL Server

**Column-Oriented (OLAP/analytics):** Each column stored separately.
- Good for: `SUM(salary)` - reads only salary column, ignores everything else
- Bad for: `SELECT * WHERE id = 1` - must read from every column file
- Examples: ClickHouse, Redshift, BigQuery, Parquet files
- Better compression (same-type data compresses well)

## TOAST (PostgreSQL)

The Oversized-Attribute Storage Technique. Row version must fit in one 8KB page.

- Large values automatically compressed and/or moved to separate TOAST table
- TOAST table has its own index
- Read only when large attribute accessed
- Unchanged TOAST parts not duplicated on row UPDATE
- `SELECT *` forces fetch + decompress of all TOAST columns

## Write Amplification

A single logical write causing multiple physical writes.

**PostgreSQL:** Updating any column rewrites entire tuple (new version in heap). All indexes pointing to old tuple must create new entries. HOT (Heap-Only Tuple) update avoids index updates if: (1) updated columns not indexed AND (2) new tuple fits on same page.

**MySQL InnoDB:** UPDATE modifies tuple in-place (if fits on page). Secondary indexes only updated if indexed column changes. Significantly less write amplification for UPDATE-heavy workloads.

**Uber's migration (2016):** Primary motivation was Postgres write amplification with many secondary indexes. MySQL's in-place updates reduced write I/O. Postgres has since improved with HOT updates.

## Key Facts

- Page size determines B+Tree fanout - larger pages = more keys per node = shallower tree
- PostgreSQL stores row locks in tuple header, not in memory
- Full page writes (`full_page_writes = on`) prevent torn page problem but double WAL size
- OS page cache can serve reads without disk I/O - `effective_cache_size` tells planner about this
- `O_DIRECT` bypasses OS cache for database-controlled caching

## Disk Storage Details

- Data stored as files managed by filesystem (ext4, XFS, NTFS)
- SSD changes optimization: `random_page_cost` should be 1.1-2.0 (vs 4.0 for HDD)
- NVMe: `effective_io_concurrency = 500-1000`; SATA SSD: 200; HDD: number of spindles

## Gotchas

- `SELECT *` kills performance by fetching TOAST columns and preventing index-only scans
- Adding columns to table silently degrades existing `SELECT *` queries
- Memory-mapped I/O (mmap) vs buffered I/O: PostgreSQL uses buffered I/O through shared_buffers
- OS can cache writes in memory - `fsync()` forces physical disk write

## See Also

- [[btree-and-index-internals]] - index data structures and page splits
- [[postgresql-mvcc-vacuum]] - dead tuples and space reclamation
- [[postgresql-wal-durability]] - write-ahead log for crash recovery
- [[query-optimization-explain]] - understanding I/O costs in query plans
