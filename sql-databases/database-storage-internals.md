---
title: Database Storage Internals
category: concepts
tags: [sql, storage, pages, tablespace, toast, wal, heap, fsm, postgresql, mysql, innodb]
---

# Database Storage Internals

Understanding how databases store data physically - pages, heaps, tablespaces, WAL, TOAST - helps diagnose performance issues and make informed design decisions. PostgreSQL and MySQL/InnoDB use fundamentally different storage architectures.

## Key Facts

- **Page** (block) - the fundamental I/O unit. PostgreSQL: 8KB default. MySQL/InnoDB: 16KB default. All reads/writes operate on full pages
- **Heap** (PostgreSQL) - unordered collection of pages containing row data. New rows inserted into any page with free space (tracked by FSM - Free Space Map)
- **Clustered storage** (InnoDB) - data stored in B-tree ordered by primary key. PostgreSQL heap is NOT clustered (CLUSTER command reorders once but does not maintain order)
- **TOAST** (The Oversized Attribute Storage Technique) - PostgreSQL mechanism for storing large values (>2KB). Automatically compresses and/or stores out-of-line. Transparent to queries
- **WAL** (Write-Ahead Log) / **Redo log** - sequential log of all changes, written before data pages. Ensures crash recovery. Foundation for replication and PITR
- **Tablespace** - logical storage location mapping to filesystem directory. Useful for placing tables/indexes on different disks
- See [[postgresql-vacuum-and-mvcc]] for how dead tuples affect storage
- See [[indexes-and-btree]] for index storage structures

## Patterns

### PostgreSQL storage inspection

```sql
-- Page layout inspection (pageinspect extension)
CREATE EXTENSION pageinspect;

-- View page header
SELECT * FROM page_header(get_raw_page('users', 0));

-- View tuple headers on a page
SELECT lp, t_xmin, t_xmax, t_ctid, t_infomask
FROM heap_page_items(get_raw_page('users', 0));

-- Table and index sizes
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS table_data,
    pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename)) AS indexes,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)
        - pg_relation_size(schemaname || '.' || tablename)
        - pg_indexes_size(schemaname || '.' || tablename)) AS toast_and_other
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;

-- Database total size
SELECT pg_size_pretty(pg_database_size('mydb'));

-- TOAST tables
SELECT c.relname AS table_name,
       pg_size_pretty(pg_relation_size(c.reltoastrelid)) AS toast_size
FROM pg_class c
WHERE c.reltoastrelid != 0 AND c.relnamespace = 'public'::regnamespace
ORDER BY pg_relation_size(c.reltoastrelid) DESC;
```

### Tablespace management

```sql
-- PostgreSQL: create tablespace on fast SSD
CREATE TABLESPACE fast_ssd LOCATION '/mnt/ssd/pg_data';

-- Move table to specific tablespace
ALTER TABLE hot_data SET TABLESPACE fast_ssd;

-- Move index to specific tablespace
ALTER INDEX idx_hot_data SET TABLESPACE fast_ssd;

-- Default tablespace for new objects
SET default_tablespace = 'fast_ssd';

-- MySQL/InnoDB: file-per-table tablespace (default since 5.6.6)
-- innodb_file_per_table = ON
-- Each table stored in its own .ibd file
-- General tablespace:
CREATE TABLESPACE ts1 ADD DATAFILE 'ts1.ibd' ENGINE=InnoDB;
CREATE TABLE orders (...) TABLESPACE ts1;
```

### PostgreSQL file structure

```
$PGDATA/
  base/                    # database directories (by OID)
    16384/                 # database OID
      16385                # table file (relation OID)
      16385.1              # extension file (>1GB tables)
      16385_fsm            # free space map
      16385_vm             # visibility map
  global/                  # cluster-wide tables
  pg_wal/                  # WAL segments (16MB each)
  pg_tblspc/               # tablespace symlinks
  pg_stat_tmp/             # statistics collector temp
  postgresql.conf          # configuration
  pg_hba.conf              # authentication
```

### InnoDB file structure

```
# File-per-table mode (default)
/var/lib/mysql/
  ibdata1                  # system tablespace (undo logs, change buffer, etc.)
  ib_logfile0, ib_logfile1 # redo logs (pre-8.0.30)
  #innodb_redo/            # redo logs (8.0.30+)
  mydb/
    users.ibd              # table data + indexes (file-per-table)
    orders.ibd
```

### Data file management

```sql
-- PostgreSQL: data directory location
SHOW data_directory;

-- File path for a specific table
SELECT pg_relation_filepath('users');  -- e.g., 'base/16384/16385'

-- Check disk usage growth
SELECT pg_size_pretty(pg_database_size('mydb'));

-- MySQL: data directory
SHOW VARIABLES LIKE 'datadir';

-- InnoDB tablespace info
SELECT * FROM information_schema.INNODB_TABLESPACES
WHERE name LIKE 'mydb/%';
```

## Gotchas

- **PostgreSQL table bloat from no VACUUM** - dead tuples consume space in the heap but are invisible to queries. VACUUM marks space as reusable but does NOT shrink the file. Only VACUUM FULL or pg_repack shrinks files
- **1GB file segments** - PostgreSQL splits table files at 1GB boundaries. A 10GB table has 10 segment files. This is transparent to queries
- **TOAST compression** - large TEXT/JSONB values are automatically compressed with pglz (or lz4 in PG 14+). TOAST has its own table and indexes, adding overhead for very wide rows
- **InnoDB page splits** - when a page is full and a new row must be inserted in order, InnoDB splits the page. Random PK inserts (UUID) cause excessive page splits
- **WAL disk usage** - WAL files accumulate during base backups, replication lag, or when archive_command fails. Monitor pg_wal directory size. In PostgreSQL 13+, `wal_keep_size` replaces `wal_keep_segments`
- **Moving tablespaces** - ALTER TABLE SET TABLESPACE copies all data. For large tables, this takes time and briefly locks the table (PostgreSQL). Plan during maintenance windows

## See Also

- [[postgresql-vacuum-and-mvcc]] - dead tuple management and storage reclamation
- [[postgresql-configuration-tuning]] - storage-related configuration parameters
- [PostgreSQL database physical storage](https://www.postgresql.org/docs/current/storage.html)
- [MySQL InnoDB tablespace](https://dev.mysql.com/doc/refman/8.0/en/innodb-tablespace.html)
