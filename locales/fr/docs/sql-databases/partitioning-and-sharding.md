---
title: "Partitionnement et sharding"
category: concepts
tags: [sql-databases, partitioning, sharding, consistent-hashing, horizontal-partitioning, postgresql, billion-rows]
level: 4
source_sha256: a2a7f417c6821899519786a8c71b76a6ee2b67bd45fdc7ad3beed25dceea1336
translation: machine
translated_at: '2026-10-24'
---
# Partitionnement et sharding {#partitioning-and-sharding}

Le partitionnement découpe une grande table en segments physiques plus petits sur le même serveur. Le sharding répartit les données sur plusieurs serveurs. Ces deux stratégies permettent de gérer des tables qui dépassent la capacité d'un seul serveur.

## Hiérarchie des stratégies (privilégier la plus simple) {#strategy-hierarchy-prefer-simpler-first}

1. **Revoir le modèle de données** - éviter complètement la table de milliard de lignes
2. **Indexation** - index B-tree/LSM pour réduire la recherche
3. **Partitionnement** - découper la table sur le même serveur
4. **Sharding** - répartir sur plusieurs serveurs
5. **MapReduce** - traitement parallèle par force brute (dernier recours)

## Partitionnement horizontal {#horizontal-partitioning}

```sql
-- PostgreSQL: range partitioning
CREATE TABLE grades (id SERIAL NOT NULL, g INTEGER NOT NULL)
PARTITION BY RANGE (g);

CREATE TABLE g_00_35 PARTITION OF grades FOR VALUES FROM (0) TO (35);
CREATE TABLE g_35_60 PARTITION OF grades FOR VALUES FROM (35) TO (60);
CREATE TABLE g_60_80 PARTITION OF grades FOR VALUES FROM (60) TO (80);
CREATE TABLE g_80_100 PARTITION OF grades FOR VALUES FROM (80) TO (100);

-- Index on partitioned table (applies to all partitions)
CREATE INDEX g_idx ON grades (g);
```

### Types de partitionnement {#partition-types}

| Type | Clé | Usage optimal |
|------|-----|---------------|
| Range | Dates, plages d'identifiants | Séries temporelles, archivage (DROP des anciennes partitions) |
| List | Valeurs discrètes (pays, statut) | Données catégorielles |
| Hash | Hash de la valeur de la colonne | Distribution uniforme quel que soit le motif des données |
| Composite | Range + Hash | Plage de dates puis hash par utilisateur au sein de la plage |

### Élagage des partitions (partition pruning) {#partition-pruning}
```sql
-- EXPLAIN shows only relevant partition scanned
EXPLAIN ANALYZE SELECT count(*) FROM grades WHERE g = 30;
-- Scans only g_00_35 partition
```

### Partitionnement vertical {#vertical-partitioning}
Répartir les colonnes dans des tables séparées. Les colonnes fréquemment consultées dans une table, les gros BLOB/textes dans une autre. Cela réduit la taille des pages, donc plus de lignes par page et moins d'E/S.

## Sharding {#sharding}

Répartir les données sur plusieurs serveurs de bases de données. Chaque shard possède ses propres partitions et index.

### Consistent hashing {#consistent-hashing}
```javascript
// Hash key to determine shard
const crypto = require('crypto');
const hash = crypto.createHash('md5').update(urlId).digest('hex');
const shardIndex = parseInt(hash.substring(0, 8), 16) % NUM_SHARDS;
```

Ajouter ou retirer un shard ne redistribue que les clés du shard adjacent (et non toutes les clés).

### Choix de la clé de sharding {#sharding-key-selection}
Point critique pour une distribution équilibrée. Mauvais exemple : sharder par langue alors que 90 % des utilisateurs parlent anglais, ce qui fait subir une charge dix fois supérieure à un shard. Utiliser des clés à forte cardinalité et à distribution uniforme.

### Compromis du sharding {#sharding-trade-offs}

**Avantages :** mise à l'échelle horizontale, index plus petits par shard, isolation de sécurité, localité des données.

**Inconvénients :** complexité du routage côté client, transactions inter-shards (nécessitant 2PC ou une cohérence à terme), jointures inter-shards impossibles en SQL, modifications de schéma sur tous les shards, shards en point chaud.

## Points clés {#key-facts}

- La clé de partitionnement DOIT être incluse dans la clé primaire et les contraintes d'unicité
- L'extension `pg_partman` automatise la création et la rétention des partitions
- Le sharding doit être le dernier recours : essayer d'abord les réplicas en lecture, le cache, le pooling, l'optimisation puis le partitionnement
- Les requêtes cross-partition parcourent TOUTES les partitions (pire qu'une table non partitionnée en l'absence d'élagage)
- Déplacer une ligne d'une partition à une autre (UPDATE de la clé de partitionnement) est coûteux

## Pièges {#gotchas}

- Sur-partitionnement : trop de partitions = surcharge de métadonnées, nombreux petits fichiers
- Fast-path des verrous faibles de PostgreSQL : 16 emplacements par backend, les requêtes fortement partitionnées peuvent les dépasser
- Dans PostgreSQL, les contraintes d'unicité doivent inclure la clé de partitionnement
- Les clés étrangères référençant des tables partitionnées présentent des limitations
- Le resharding nécessite une migration des données et peut entraîner une indisponibilité
- Les agrégations cross-shard (COUNT, SUM) exigent d'interroger tous les shards puis de fusionner les résultats

## Voir aussi {#see-also}

- [[btree-and-index-internals]] - comportement des index avec les partitions
- [[distributed-databases]] - Citus, CockroachDB pour le sharding automatique
- [[query-optimization-explain]] - élagage des partitions dans EXPLAIN
- [[database-storage-internals]] - implications des partitions au niveau des pages
