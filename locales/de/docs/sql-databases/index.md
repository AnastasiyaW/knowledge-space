---
title: "SQL & Datenbanken"
type: MOC
level: 3
source_sha256: 4e1e189ab8d90823ca3b807aa594ab945ebc5e5e01a79013ac0832f4fffb6757
translation: machine
translated_at: '2026-10-24'
---
# SQL & Datenbanken {#sql-databases}

## SQL-Grundlagen {#sql-language-fundamentals}
- [[select-fundamentals]] - SELECT, WHERE, ORDER BY, LIMIT, CASE-Ausdrücke, Keyset-Paginierung
- [[aggregate-functions-group-by]] - COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING
- [[joins-and-set-operations]] - INNER, LEFT, RIGHT, FULL, CROSS, Self-JOIN, UNION, INTERSECT, EXCEPT
- [[subqueries-and-ctes]] - skalare/korrelierte Subqueries, EXISTS, CTEs, rekursive CTEs
- [[window-functions]] - ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, laufende Summen, Frame-Spezifikation
- [[dml-insert-update-delete]] - INSERT, UPDATE, DELETE, TRUNCATE, UPSERT, Batch-Operationen

## Schema- und Datenmodellierung {#schema-and-data-modeling}
- [[ddl-schema-management]] - CREATE TABLE, ALTER TABLE, DROP, Constraints, Fremdschlüssel, ENUM
- [[data-types-and-nulls]] - Datentypen von MySQL/PostgreSQL, NULL-Logik mit drei Wahrheitswerten, String-/Datums-/numerische Funktionen
- [[schema-design-normalization]] - 1NF-3NF, Beziehungen (1:1, 1:M, M:M), Denormalisierung, PK-Strategien

## Transaktionen und Nebenläufigkeit {#transactions-and-concurrency}
- [[transactions-and-acid]] - ACID-Eigenschaften, Isolationsstufen, Lesephänomene, pessimistisch vs. optimistisch
- [[concurrency-and-locking]] - Sperrtypen in PostgreSQL/MySQL, Deadlocks, Advisory Locks, Two-Phase Locking
- [[distributed-transactions]] - 2PC, Saga-Muster, Verhinderung von Doppelbuchungen, Hash-Tabellen

## Storage- und Index-Interna {#storage-and-index-internals}
- [[database-storage-internals]] - Pages, Heaps, Row- vs. Column-Store, TOAST, Write Amplification, SSD vs. HDD
- [[btree-and-index-internals]] - B-Tree vs. B+Tree, Page Splits, Auswirkung von UUIDs, Bloom-Filter, geclusterte Indizes
- [[index-strategies]] - zusammengesetzte, abdeckende, partielle Indizes, SARGable-Prädikate, CREATE INDEX CONCURRENTLY

## Query-Optimierung {#query-optimization}
- [[query-optimization-explain]] - EXPLAIN/ANALYZE, Plan-Operatoren, Kostenmodell, Monitoring-Erweiterungen
- [[database-cursors]] - clientseitige vs. serverseitige Cursor, Batch-Verarbeitung, wann welcher verwendet wird

## PostgreSQL-Administration {#postgresql-administration}
- [[postgresql-mvcc-vacuum]] - MVCC, VACUUM, Autovacuum, HOT-Updates, Dead Tuples, Prozessarchitektur
- [[postgresql-configuration-tuning]] - postgresql.conf, Speicher, WAL, Planer-Parameter, pgbench, pg_hba.conf
- [[postgresql-wal-durability]] - WAL-Interna, Checkpoints, fsync, synchronous_commit, Crash-Recovery
- [[postgresql-data-loading]] - COPY, FDW (postgres_fdw, file_fdw, ogr_fdw), pgloader, Optimierung von Bulk-Loads

## MySQL-Administration {#mysql-administration}
- [[mysql-innodb-engine]] - InnoDB-Interna, Storage-Engines (MyISAM, MEMORY, Archive), LSM-Tree, RocksDB

## Hochverfügbarkeit und Replikation {#high-availability-and-replication}
- [[connection-pooling]] - PgBouncer, ProxySQL, Pool-Dimensionierung, Pooling-Modi, anwendungsseitige Pools
- [[replication-fundamentals]] - Streaming- und logische Replikation, synchron/asynchron, Monitoring, pg_rewind
- [[postgresql-ha-patroni]] - Patroni, etcd, HAProxy, Failover, Switchover, K8s-Operatoren
- [[backup-and-recovery]] - pg_dump, pg_basebackup, pg_probackup, WAL-G, PITR, Data Checksums

## Skalierung und Verteilung {#scaling-and-distribution}
- [[partitioning-and-sharding]] - horizontale/vertikale Partitionierung, Sharding, konsistentes Hashing
- [[distributed-databases]] - Citus, CockroachDB, Greenplum, YugabyteDB, ClickHouse, OLTP vs. OLAP
- [[caching-redis-memcached]] - Redis, Memcached, Cache-Muster (Cache-Aside, Write-Through, Write-Behind)

## Sicherheit und Infrastruktur {#security-and-infrastructure}
- [Database Security](database-security.md) - SQL-Injection, TLS/SSL, Verschlüsselung, Rollen, Berechtigungen, Least Privilege
- [[postgresql-docker-kubernetes]] - Docker, StatefulSet, Helm, Zalando-/Crunchy-Operatoren, GKE
- [[infrastructure-as-code]] - Terraform, Ansible, verwaltetes PostgreSQL in der Cloud, Installationsanleitungen

## Weiterführende Referenzen {#additional-references}

- [[advanced-patterns]] - Fortgeschrittene SQL-Muster jenseits von CRUD - Window Functions für Analysen, korrelierte Subqueries
