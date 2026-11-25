---
title: "Bases de données SQL distribuées"
category: concepts
tags: [sql-databases, distributed, cockroachdb, citus, greenplum, yugabytedb, mpp, olap, sharding]
level: 4
source_sha256: 1f5d0de7bad695144cf15b81586be3e0326997c5cfce931b67e73dbf901539b1
translation: machine
translated_at: '2026-10-24'
---
# Bases de données SQL distribuées {#distributed-sql-databases}

Lorsque PostgreSQL sur un serveur unique atteint ses limites, les bases de données distribuées offrent une mise à l'échelle horizontale. Chacune présente des compromis différents entre cohérence, complexité et adéquation à la charge de travail.

## Comparaison {#comparison}

| Caractéristique | Citus | CockroachDB | Greenplum | YugabyteDB |
|---------|-------|-------------|-----------|------------|
| Base | Extension PG | Personnalisé (protocole PG) | Fork de PG | Personnalisé (protocole PG) |
| Cohérence | Par shard | Sérialisable | Par segment | Sérialisable |
| Idéal pour | SaaS multi-locataire | OLTP géo-distribué | Analytique/DWH | OLTP distribué |
| OLTP | Bon | Bon | Faible | Bon |
| OLAP | Bon | Moyen | Excellent | Moyen |
| Complexité | Faible (extension) | Moyenne | Élevée (produit séparé) | Moyenne |

## Citus (extension PostgreSQL) {#citus-postgresql-extension}

Rachetée par Microsoft (2019). Transforme un PostgreSQL unique en base de données distribuée.

### Types de tables {#table-types}
- **Distribuée :** shardée par hachage sur les workers selon la colonne de distribution
- **Référence :** répliquée sur tous les workers (tables de dimensions/de référence)
- **Locale :** uniquement sur le coordinateur

```sql
-- Create distributed table
SELECT create_distributed_table('events', 'tenant_id');

-- Queries automatically routed to relevant shard
SELECT count(*) FROM events WHERE tenant_id = 42;

-- Cross-shard queries supported but slower
SELECT tenant_id, count(*) FROM events GROUP BY tenant_id;
```

**Depuis Citus 11.0 :** les requêtes peuvent être exécutées depuis n'importe quel nœud. `citus.shard_replication_factor` vaut 1 par défaut (pas de tolérance aux pannes).

## CockroachDB {#cockroachdb}

SQL distribué compatible PostgreSQL. Multi-maître, sharding automatique, isolation sérialisable.

```bash
# 3-node cluster
cockroach start --certs-dir=certs --advertise-addr=node1 --join=node1,node2,node3
cockroach init --certs-dir=certs --host=node1
```

Géo-distribué : 9 nœuds répartis sur 3 régions. Nécessite une synchronisation horaire (tolérance de dérive de 500 ms). Multi-maître : les écritures effectuées dans une région sont visibles dans toutes les autres.

## Greenplum MPP {#greenplum-mpp}

SGBDR MPP open source basé sur PostgreSQL. Stockage en colonnes, traitement massivement parallèle.

### Architecture {#architecture}
- **Hôte maître :** point d'entrée, coordinateur SQL, ne contient aucune donnée utilisateur
- **Hôtes de segments :** 2 à 8 segments PostgreSQL par hôte, primaire + miroir
- **Interconnexion :** réseau dédié à haut débit

### Types de stockage {#storage-types}

| Type | Idéal pour |
|------|----------|
| Heap | UPDATE/DELETE/INSERT concurrents |
| Append-Optimized (AO) | Chargements par lots + analytique, rarement mis à jour |
| Orienté ligne | SELECT larges, charges mixtes |
| Orienté colonne | SELECT étroits sur de grandes tables, agrégations |

### Règles de performance {#performance-rules}
- Vitesse = cœurs CPU / volume de données par nœud
- 1 requête = 1 cœur maximum par segment
- Vitesse du cluster = vitesse du segment le plus lent : une distribution équilibrée est critique
- Concevoir un modèle en insertion seule ; tronquer la partition journalière avant chargement

## OLTP vs OLAP {#oltp-vs-olap}

**OLTP :** normalisé, taux élevé d'insertions/mises à jour, nombreux utilisateurs concurrents, transactions courtes, indexé pour un accès rapide. Architecture trois tiers.

**OLAP :** rapports sur données historiques, stockage en colonnes, tables de faits dénormalisées avec dimensions, mises à jour peu fréquentes, lectures d'agrégation rapides.

## MPP (Massive Parallel Processing) {#mpp-massive-parallel-processing}

Données et calcul distribués entre un nœud leader et des nœuds workers. Architecture shared-nothing.

**Avantages :** traitement rapide de gros volumes, mise à l'échelle horizontale aisée, tolérance aux pannes via la mise en miroir.
**Inconvénients :** besoins en ressources élevés, peu performant pour de nombreuses requêtes simples, déséquilibre de la distribution entre segments.

## ClickHouse {#clickhouse}

Base OLAP orientée colonnes (C++, Yandex). Traitement vectorisé des requêtes, compression efficace, réplication et sharding intégrés. Dialecte SQL riche avec les types JSON, IP, UUID et Array. Intégration avec Kafka, MySQL et PostgreSQL.

## Autres solutions {#other-solutions}

- **YugabyteDB :** SQL distribué compatible PG avec isolation sérialisable
- **Postgres-BDR / Bucardo :** multi-maître utilisant la réplication logique
- **Shardman (Postgres Pro) :** sharding basé sur les FDW, distribution par hachage uniquement, limitations importantes
- **Arenadata DB :** distribution commerciale russe de Greenplum

## Points clés {#key-facts}

- PostgreSQL n'est PAS conçu pour le big data : les transactions/WAL freinent les opérations volumineuses, et il n'intègre pas de sharding
- Citus est le chemin le plus simple d'un PostgreSQL unique vers un système distribué
- CockroachDB offre la cohérence la plus forte (sérialisable) entre nœuds distribués
- Greenplum excelle en analytique mais est peu adapté à l'OLTP
- La clé de sharding doit avoir une cardinalité élevée et une distribution uniforme

## Pièges {#gotchas}

- Citus : `shard_replication_factor = 1` (valeur par défaut) signifie l'absence de tolérance aux pannes pour chaque shard
- CockroachDB : tolérance de dérive temporelle de 500 ms - synchronisation NTP obligatoire
- Greenplum : 1 cœur par requête et par segment limite le parallélisme fin des requêtes
- Shardman : pas de ALTER TABLE (sauf owner/NULL/ADD column), pas de clés étrangères, transport en SELECT uniquement
- La réplication multi-maître implique une résolution de conflits complexe : à éviter sauf si réellement nécessaire

## Voir aussi {#see-also}

- [[partitioning-and-sharding]] - concepts de partitionnement et de sharding sur serveur unique
- [[replication-fundamentals]] - la réplication en flux comme alternative plus simple
- [[postgresql-ha-patroni]] - haute disponibilité sans distribution
- [[caching-redis-memcached]] - couche de cache pour réduire la charge de la base de données
