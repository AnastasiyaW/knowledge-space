---
title: SQL & Databases
type: MOC
---

# SQL & Databases

## SQL Language Fundamentals
- [[select-fundamentals]] - SELECT, WHERE, ORDER BY, LIMIT, CASE expressions, keyset pagination
- [[aggregate-functions-group-by]] - COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING
- [[joins-and-set-operations]] - INNER, LEFT, RIGHT, FULL, CROSS, self-JOIN, UNION, INTERSECT, EXCEPT
- [[subqueries-and-ctes]] - scalar/correlated subqueries, EXISTS, CTEs, recursive CTEs
- [[window-functions]] - ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running totals, frame specification
- [[dml-insert-update-delete]] - INSERT, UPDATE, DELETE, TRUNCATE, UPSERT, batch operations

## Schema and Data Modeling
- [[ddl-schema-management]] - CREATE TABLE, ALTER TABLE, DROP, constraints, foreign keys, ENUM
- [[data-types-and-nulls]] - MySQL/PostgreSQL data types, NULL three-valued logic, string/date/numeric functions
- [[schema-design-normalization]] - 1NF-3NF, relationships (1:1, 1:M, M:M), denormalization, PK strategies

## Transactions and Concurrency
- [[transactions-and-acid]] - ACID properties, isolation levels, read phenomena, pessimistic vs optimistic
- [[concurrency-and-locking]] - PostgreSQL/MySQL lock types, deadlocks, advisory locks, two-phase locking
- [[distributed-transactions]] - 2PC, Saga pattern, double-booking prevention, hash tables

## Storage and Index Internals
- [[database-storage-internals]] - pages, heaps, row vs column store, TOAST, write amplification, SSD vs HDD
- [[btree-and-index-internals]] - B-Tree vs B+Tree, page splits, UUID impact, bloom filters, clustered indexes
- [[index-strategies]] - composite, covering, partial indexes, SARGable predicates, CREATE INDEX CONCURRENTLY

## Query Optimization
- [[query-optimization-explain]] - EXPLAIN/ANALYZE, plan operators, cost model, monitoring extensions
- [[database-cursors]] - client-side vs server-side cursors, batch processing, when to use which

## PostgreSQL Administration
- [[postgresql-mvcc-vacuum]] - MVCC, VACUUM, autovacuum, HOT updates, dead tuples, process architecture
- [[postgresql-configuration-tuning]] - postgresql.conf, memory, WAL, planner params, pgbench, pg_hba.conf
- [[postgresql-wal-durability]] - WAL internals, checkpoints, fsync, synchronous_commit, crash recovery
- [[postgresql-data-loading]] - COPY, FDW (postgres_fdw, file_fdw, ogr_fdw), pgloader, bulk load optimization

## MySQL Administration
- [[mysql-innodb-engine]] - InnoDB internals, storage engines (MyISAM, MEMORY, Archive), LSM-Tree, RocksDB

## High Availability and Replication
- [[connection-pooling]] - PgBouncer, ProxySQL, pool sizing, pooling modes, application-level pools
- [[replication-fundamentals]] - streaming/logical replication, sync/async, monitoring, pg_rewind
- [[postgresql-ha-patroni]] - Patroni, etcd, HAProxy, failover, switchover, K8s operators
- [[backup-and-recovery]] - pg_dump, pg_basebackup, pg_probackup, WAL-G, PITR, data checksums

## Scaling and Distribution
- [[partitioning-and-sharding]] - horizontal/vertical partitioning, sharding, consistent hashing
- [[distributed-databases]] - Citus, CockroachDB, Greenplum, YugabyteDB, ClickHouse, OLTP vs OLAP
- [[caching-redis-memcached]] - Redis, Memcached, cache patterns (aside, write-through, write-behind)

## Security and Infrastructure
- [[database-security]] - SQL injection, TLS/SSL, encryption, roles, privileges, least privilege
- [[postgresql-docker-kubernetes]] - Docker, StatefulSet, Helm, Zalando/Crunchy operators, GKE
- [[infrastructure-as-code]] - Terraform, Ansible, cloud managed PostgreSQL, installation guides
