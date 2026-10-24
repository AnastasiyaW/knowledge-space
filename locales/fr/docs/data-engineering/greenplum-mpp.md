---
title: "Greenplum et architecture MPP"
category: tools
tags: [data-engineering, greenplum, mpp, distributed-database, parallel-processing]
level: 3
source_sha256: 163a2870f4d1e311ea5f4a3381738724e756087532a6af0f5cc8d50c4a958aa2
translation: machine
translated_at: '2026-10-24'
---
# Greenplum et architecture MPP {#greenplum-and-mpp-architecture}

Greenplum est une base de données analytique MPP (Massive Parallel Processing) basée sur PostgreSQL. Elle utilise une architecture shared-nothing où chaque nœud possède son propre CPU, sa mémoire et son disque.

## Architecture {#architecture}

```php
Client -> Master (QD: Query Dispatcher)
              |
    +---------+---------+
    Segment1  Segment2  Segment3  (QE: Query Executors)
    (mirror)  (mirror)  (mirror)
```

- **Master (QD) :** accepte les requêtes, construit le plan, le distribue aux segments et agrège les résultats. Ne stocke PAS les données utilisateur
- **Segments (QE) :** stockent les données et exécutent en parallèle. Chacun est une instance PostgreSQL
- **Miroirs :** copies de secours pour la tolérance aux pannes

## Opérateurs Motion {#motion-operators}

| Opérateur | Fonction | Coût |
|-----------|----------|------|
| **Redistribute Motion** | Redistribue les données selon une clé de hachage | Élevé |
| **Broadcast Motion** | Copie complète d'une petite table sur tous les segments | Moyen |
| **Gather Motion** | Rassemble les résultats sur le master | Faible |

## Stratégies de distribution {#distribution-strategies}

```sql
-- Hash distribution (best for JOIN keys)
CREATE TABLE orders (...) DISTRIBUTED BY (order_id);

-- Random (default)
CREATE TABLE logs (...) DISTRIBUTED RANDOMLY;

-- Replicated (small dimension tables)
CREATE TABLE countries (...) DISTRIBUTED REPLICATED;
```

### Optimisation clé {#key-optimization}

Distribuez les deux tables d'une jointure selon la clé de jointure pour éliminer le Redistribute Motion :

```sql
ALTER TABLE lineitem SET DISTRIBUTED BY (l_orderkey);
ALTER TABLE orders SET DISTRIBUTED BY (o_orderkey);
-- Redistribute Motion disappears from EXPLAIN plan
```

## ANALYZE (critique) {#analyze-critical}

```sql
ANALYZE table_name;
```

**Exécutez toujours ANALYZE après des modifications massives de données.** L'optimiseur de Greenplum dépend des statistiques. Sans statistiques à jour après INSERT/UPDATE, l'optimiseur utilise des estimations obsolètes, ce qui conduit à des plans sous-optimaux.

**PostgreSQL effectue un ANALYZE automatique de façon raisonnable. Greenplum NE LE FAIT PAS - un ANALYZE explicite est requis.**

## Greenplum vs PostgreSQL : index {#greenplum-vs-postgresql-indexes}

- PostgreSQL : créer un index -> l'optimiseur l'utilise -> requêtes plus rapides
- Greenplum : créer un index -> **l'optimiseur l'ignore** (il préfère un parcours séquentiel sur les segments)

```sql
-- Force index usage (rarely needed)
SET seq_page_cost = 100;
SET random_page_cost = 1;
SET optimizer = off;  -- GPORCA ignores hints
```

En MPP, un parcours séquentiel sur de nombreux segments est souvent plus rapide qu'une recherche par index.

## Compression (TPC-H lineitem, scale=10) {#compression-tpc-h-lineitem-scale10}

| Stockage | Taille |
|----------|--------|
| Orienté lignes (par défaut) | 34 Go |
| Lignes + compression | 11 Go |
| Colonnes + compression | 7,5 Go |

## Types de tables {#table-types}

| Type | Persistance | Journalisée | Visibilité |
|------|-------------|-------------|------------|
| Permanente | Survit au redémarrage | Oui (WAL) | Toutes les sessions |
| Temporaire | Session uniquement | Non | Session courante |
| Non journalisée | Survit à la session, perdue en cas de crash | Non | Toutes les sessions |
| Externe | Données hors de la base (S3, HDFS via PXF) | N/A | Toutes les sessions |

## Pièges {#gotchas}

- Les index sont rarement utiles dans Greenplum - le parcours séquentiel domine
- ANALYZE doit être exécuté manuellement après les opérations massives
- Les tables externes n'ont pas de statistiques - l'optimiseur estime heuristiquement
- La latence réseau détruit les performances d'un cluster réparti entre datacenters
- L'optimiseur GPORCA ignore les hints - il faut le désactiver pour forcer l'utilisation d'un index

## Voir aussi {#see-also}
- [[dwh-architecture]] - contexte de conception DWH
- [[cloud-data-platforms]] - alternatives modernes (Snowflake, BigQuery)
- [[spark-optimization]] - concepts d'optimisation distribuée similaires
