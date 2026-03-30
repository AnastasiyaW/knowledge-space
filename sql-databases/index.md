---
title: SQL & Databases
type: MOC
---

# SQL & Databases

## SQL Syntax & Querying
- [[select-fundamentals]] - SELECT clause ordering, WHERE, GROUP BY, HAVING, LIMIT, pagination patterns
- [[joins-and-set-operations]] - INNER/LEFT/RIGHT/FULL/CROSS/LATERAL joins, UNION, INTERSECT, EXCEPT
- [[common-table-expressions]] - WITH clause, recursive CTEs, materialization, writeable CTEs
- [[subqueries-and-derived-tables]] - Scalar, correlated, EXISTS/IN/ANY/ALL, derived tables
- [[window-functions]] - ROW_NUMBER, RANK, LAG/LEAD, running totals, frame clauses, named windows
- [[dml-insert-update-delete]] - INSERT/UPDATE/DELETE patterns, UPSERT, MERGE, RETURNING, COPY/LOAD DATA

## Schema & Data Modeling
- [[schema-design-data-types]] - Type selection, SERIAL vs IDENTITY, UUID, JSONB, ENUM, timestamps
- [[data-integrity-constraints]] - PK, FK, UNIQUE, CHECK, EXCLUDE, normalization, deferrable constraints
- [[views-and-materialized-views]] - Views, materialized views, updatable views, security barriers
- [[stored-procedures-functions]] - PL/pgSQL functions, procedures, triggers, audit patterns

## Query Optimization
- [[indexes-and-btree]] - B-tree, GIN, GiST, BRIN, covering indexes, composite index order, partial indexes
- [[query-optimization-explain]] - EXPLAIN ANALYZE, scan types, join algorithms, plan reading

## PostgreSQL Internals & Operations
- [[transactions-and-acid]] - ACID properties, isolation levels, MVCC overview, deadlocks, serializable
- [[postgresql-vacuum-and-mvcc]] - MVCC mechanics, dead tuples, VACUUM, autovacuum tuning, wraparound prevention
- [[postgresql-configuration-tuning]] - shared_buffers, work_mem, WAL, PgBouncer, monitoring queries
- [[database-storage-internals]] - Pages, heap, TOAST, WAL, tablespaces, file layout

## High Availability & Scaling
- [[postgresql-replication-ha]] - Streaming/logical replication, Patroni, etcd, HAProxy, failover
- [[postgresql-backup-pitr]] - pg_dump, pg_basebackup, PITR, pg_probackup, WAL-G
- [[postgresql-partitioning]] - Declarative partitioning, RANGE/LIST/HASH, pg_partman, Citus sharding

## MySQL Specifics
- [[mysql-innodb-specifics]] - Clustered index, buffer pool, redo/undo logs, gap locks, configuration

## Security
- [[database-security-roles]] - Roles, GRANT/REVOKE, pg_hba.conf, Row-Level Security, MySQL users
