---
title: "Apache Hive"
category: tools
tags: [data-engineering, hive, sql-on-hadoop, metastore, data-warehouse]
level: 3
source_sha256: 132758362f0bc89d6ee8bc135eb1ac7d6d553d4b8f2eb54342a17d07c370035c
translation: machine
translated_at: '2026-10-24'
---
# Apache Hive {#apache-hive}

Hive est un système d'entrepôt SQL-on-Hadoop. Il traduit les requêtes SQL en jobs MapReduce/Tez/Spark. Ce n'est pas une base de données : c'est une couche de traduction de requêtes au-dessus des données HDFS.

## Architecture {#architecture}

```php
Hive Client (CLI/JDBC/Thrift)
       |
   Hive Driver -> Compiler (uses Metastore) -> Executor -> HDFS
```

- **Metastore :** schémas de tables, types de colonnes, informations de partitionnement, configuration SerDe. Adossé à un SGBDR (MySQL/PostgreSQL)
- **Compilateur :** traduit HiveQL en DAG MapReduce/Tez à partir des métadonnées
- **Driver :** reçoit les requêtes SQL, orchestre la compilation et l'exécution

## Types de tables {#table-types}

| Type | Comportement de DROP TABLE |
|------|-------------------|
| **Managed** | Supprime les métadonnées ET les données |
| **External** | Supprime uniquement les métadonnées, les données restent sur HDFS/S3 |

## Stratégies de JOIN {#join-strategies}

### Reduce Side Join (par défaut) {#reduce-side-join-default}
- Les mappers émettent la clé de jointure et la valeur des deux tables
- Les reducers reçoivent les clés correspondantes et effectuent la jointure
- Convient aux tables petites à moyennes. Échoue pour deux très grandes tables (OOM)

### Map Side Join (MapJoin) {#map-side-join-mapjoin}
- La petite table est chargée dans une HashMap, distribuée via HDFS
- Chaque Mapper joint sa partition de la grande table avec celle-ci
- Pas d'étape Reduce nécessaire pour la jointure
- Hint : `SELECT /*+ MAPJOIN(small_table) */ ...`

### Sort-Merge-Bucket Join (SMB) {#sort-merge-bucket-join-smb}
- Le plus efficace pour deux grandes tables
- **Prérequis :**
  1. Les deux tables sont bucketisées par clé de jointure (`CLUSTERED BY`)
  2. Les nombres de buckets doivent être multiples (2:4, 5:10)
  3. Configuration : `hive.auto.convert.sortmerge.join=true`
- Jointure entièrement en phase Map : pas de shuffle, pas de reduce

## Spécificités de Hive {#hive-specifics}
- Utilise HiveQL (SQL avec extensions)
- Transactions : format ORC uniquement, fichiers delta appliqués à la lecture, la compaction fusionne les fichiers
- Pas de BEGIN/COMMIT/ROLLBACK : auto-commit par instruction
- Colonnes virtuelles : `INPUT__FILE__NAME`, `BLOCK__OFFSET__INSIDE__FILE`

## Pièges {#gotchas}
- Jointure SMB : si les données sont insérées sans forcer le bucketing, des résultats silencieusement faux apparaissent (pire que des erreurs). Toujours définir `hive.enforce.bucketing=true`
- Les requêtes complexes (JOIN + GROUP BY) génèrent plusieurs jobs MapReduce chaînés
- Hive est progressivement remplacé par Spark SQL et Trino/Presto pour les requêtes interactives
- Le Metastore reste largement utilisé comme catalogue de schémas (même sans requêtes Hive)

## Voir aussi {#see-also}
- [[hadoop-hdfs]] - stockage sous-jacent
- [[mapreduce]] - moteur d'exécution
- [[apache-spark-core]] - alternative moderne
- [[file-formats]] - format ORC pour Hive
