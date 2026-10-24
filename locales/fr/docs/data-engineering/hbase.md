---
title: "HBase"
category: tools
tags: [data-engineering, hbase, nosql, columnar, hadoop, key-value]
level: 2
source_sha256: 63f49e4fe6fe4700ad91cdc880155c0bbca4d0ac61e09e4b0a1349c50570fc5f
translation: machine
translated_at: '2026-10-24'
---
# HBase {#hbase}

HBase est un magasin NoSQL en colonnes au sein de l'écosystème Hadoop, conçu pour des milliards de lignes et des millions de colonnes. Il fonctionne au-dessus de HDFS. Pas de SQL : il utilise des méthodes d'API (GET, PUT, SCAN, DELETE).

## Modèle de données {#data-model}

```text
Table
  |-- Row Key (primary access path, binary sorted)
  |-- Column Family 1
  |     |-- column1: value (timestamp v3)
  |     |-- column1: value (timestamp v2)  <- versioning
  |     |-- column2: value
  |-- Column Family 2
        |-- columnA: value
```

## Concepts clés {#key-concepts}

| Concept | Détails |
|---------|---------|
| **Row Key** | Identifiant unique, tous les accès se font par clé de ligne ou plage de clés |
| **Column Family** | Définie à la création. Regroupe des colonnes partageant des propriétés (compression, TTL, versions) |
| **Versioning** | Intégré. Plusieurs versions par cellule avec horodatages. Configurable par famille |
| **Stockage binaire** | Toutes les valeurs sont stockées en binaire. La sérialisation est à la charge de l'application |
| **Schéma libre** | Colonnes ajoutées dynamiquement au sein des familles de colonnes existantes |

## HBase vs RDBMS {#hbase-vs-rdbms}

| Fonctionnalité | HBase | RDBMS |
|----------------|-------|-------|
| Schéma | Flexible | Fixe |
| Échelle | Milliards de lignes | Limitée (sauf MPP) |
| Mode d'accès | Recherches par clé / plage de clés | SQL arbitraire |
| Jointures | Non natives | Support complet |
| Transactions | Atomiques au niveau de la ligne | ACID entre tables |
| Langage de requête | Appels API | SQL |

## Propriétés {#properties}
- Les familles de colonnes sont stockées séparément sur HDFS
- Efficace pour les recherches par clé et par plage de clés
- TTL pour l'expiration automatique des données
- Intégration MapReduce (entrée/sortie)
- Versions stockées par ordre décroissant (la plus récente en premier)

## Pièges à éviter {#gotchas}
- Pas de SQL : tous les accès passent par l'API GET, PUT, SCAN, DELETE
- La conception de la clé de ligne est critique : une mauvaise conception entraîne des hotspots
- Les familles de colonnes doivent être définies à la création de la table
- Peu adapté aux requêtes analytiques arbitraires (utiliser Hive/Spark par-dessus)

## Voir aussi {#see-also}
- [[hadoop-hdfs]] - stockage sous-jacent
- [[clickhouse]] - OLAP en colonnes alternatif
- [[data-lake-lakehouse]] - NoSQL dans le contexte de la plateforme de données
