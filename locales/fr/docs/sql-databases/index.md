---
title: "SQL et bases de données"
type: MOC
level: 3
source_sha256: 4e1e189ab8d90823ca3b807aa594ab945ebc5e5e01a79013ac0832f4fffb6757
translation: machine
translated_at: '2026-10-24'
---
# SQL et bases de données {#sql-databases}

## Fondamentaux du langage SQL {#sql-language-fundamentals}
- [[select-fundamentals]] - SELECT, WHERE, ORDER BY, LIMIT, expressions CASE, pagination par clé (keyset pagination)
- [[aggregate-functions-group-by]] - COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING
- [[joins-and-set-operations]] - INNER, LEFT, RIGHT, FULL, CROSS, auto-jointure (self-JOIN), UNION, INTERSECT, EXCEPT
- [[subqueries-and-ctes]] - sous-requêtes scalaires/corrélées, EXISTS, CTE, CTE récursives
- [[window-functions]] - ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, totaux cumulés, spécification de cadre (frame)
- [[dml-insert-update-delete]] - INSERT, UPDATE, DELETE, TRUNCATE, UPSERT, opérations par lots

## Schéma et modélisation des données {#schema-and-data-modeling}
- [[ddl-schema-management]] - CREATE TABLE, ALTER TABLE, DROP, contraintes, clés étrangères, ENUM
- [[data-types-and-nulls]] - types de données MySQL/PostgreSQL, logique ternaire de NULL, fonctions sur chaînes, dates et numériques
- [[schema-design-normalization]] - 1NF à 3NF, relations (1:1, 1:N, N:M), dénormalisation, stratégies de clé primaire

## Transactions et concurrence {#transactions-and-concurrency}
- [[transactions-and-acid]] - propriétés ACID, niveaux d'isolation, phénomènes de lecture, pessimiste vs optimiste
- [[concurrency-and-locking]] - types de verrous PostgreSQL/MySQL, interblocages (deadlocks), verrous consultatifs (advisory locks), verrouillage à deux phases
- [[distributed-transactions]] - 2PC, pattern Saga, prévention des doubles réservations, tables de hachage

## Stockage et fonctionnement interne des index {#storage-and-index-internals}
- [[database-storage-internals]] - pages, heaps, stockage par lignes vs par colonnes, TOAST, amplification d'écriture, SSD vs HDD
- [[btree-and-index-internals]] - B-Tree vs B+Tree, éclatements de pages (page splits), impact des UUID, filtres de Bloom, index groupés (clustered)
- [[index-strategies]] - index composites, couvrants, partiels, prédicats SARGables, CREATE INDEX CONCURRENTLY

## Optimisation des requêtes {#query-optimization}
- [[query-optimization-explain]] - EXPLAIN/ANALYZE, opérateurs de plan, modèle de coût, extensions de supervision
- [[database-cursors]] - curseurs côté client vs côté serveur, traitement par lots, quand utiliser l'un ou l'autre

## Administration PostgreSQL {#postgresql-administration}
- [[postgresql-mvcc-vacuum]] - MVCC, VACUUM, autovacuum, mises à jour HOT, tuples morts, architecture des processus
- [[postgresql-configuration-tuning]] - postgresql.conf, mémoire, WAL, paramètres du planificateur, pgbench, pg_hba.conf
- [[postgresql-wal-durability]] - fonctionnement interne du WAL, checkpoints, fsync, synchronous_commit, reprise après incident
- [[postgresql-data-loading]] - COPY, FDW (postgres_fdw, file_fdw, ogr_fdw), pgloader, optimisation du chargement en masse

## Administration MySQL {#mysql-administration}
- [[mysql-innodb-engine]] - fonctionnement interne d'InnoDB, moteurs de stockage (MyISAM, MEMORY, Archive), LSM-Tree, RocksDB

## Haute disponibilité et réplication {#high-availability-and-replication}
- [[connection-pooling]] - PgBouncer, ProxySQL, dimensionnement des pools, modes de pooling, pools au niveau applicatif
- [[replication-fundamentals]] - réplication en flux (streaming) et logique, synchrone/asynchrone, supervision, pg_rewind
- [[postgresql-ha-patroni]] - Patroni, etcd, HAProxy, basculement (failover), bascule contrôlée (switchover), opérateurs K8s
- [[backup-and-recovery]] - pg_dump, pg_basebackup, pg_probackup, WAL-G, PITR, sommes de contrôle des données (data checksums)

## Mise à l'échelle et distribution {#scaling-and-distribution}
- [[partitioning-and-sharding]] - partitionnement horizontal/vertical, sharding, hachage consistant
- [[distributed-databases]] - Citus, CockroachDB, Greenplum, YugabyteDB, ClickHouse, OLTP vs OLAP
- [[caching-redis-memcached]] - Redis, Memcached, patterns de cache (cache-aside, write-through, write-behind)

## Sécurité et infrastructure {#security-and-infrastructure}
- [Sécurité des bases de données](database-security.md) - injection SQL, TLS/SSL, chiffrement, rôles, privilèges, moindre privilège
- [[postgresql-docker-kubernetes]] - Docker, StatefulSet, Helm, opérateurs Zalando/Crunchy, GKE
- [[infrastructure-as-code]] - Terraform, Ansible, PostgreSQL managé dans le cloud, guides d'installation

## Références complémentaires {#additional-references}

- [[advanced-patterns]] - patterns SQL avancés au-delà du CRUD de base - fonctions de fenêtrage pour l'analytique, sous-requêtes corrélées
