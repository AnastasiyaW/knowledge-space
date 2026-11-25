---
title: "Formats de fichiers pour le Big Data"
category: reference
tags: [data-engineering, parquet, orc, avro, file-formats, columnar]
level: 2
source_sha256: 16cc63ca23429f4b5a02a14b86cc3cebc8e5922cbaf40b716536d1dae8b1bf20
translation: machine
translated_at: '2026-10-24'
---
# Formats de fichiers pour le Big Data {#file-formats-for-big-data}

Le choix du bon format de fichier influence fortement l'efficacité du stockage, les performances des requêtes et la compatibilité au sein de l'écosystème Hadoop/Spark.

## Comparaison des formats {#format-comparison}

| Format | Type | Splittable | Schéma | Compression | Usage recommandé |
|--------|------|-----------|--------|-------------|----------|
| **Text/CSV** | Ligne | Oui (non compressé) | Non | Externe | Échange de données simple |
| **SequenceFile** | Ligne (KV binaire) | Oui | Non | Bloc/Enregistrement | Données intermédiaires MapReduce |
| **Avro** | Ligne (binaire) | Oui | Intégré | Bloc | Évolution de schéma, streaming |
| **ORC** | Colonnaire | Oui | Intégré | Par colonne | Analytique optimisée pour Hive |
| **Parquet** | Colonnaire | Oui | Intégré | Par colonne | Analytique inter-écosystèmes |

## Parquet vs CSV {#parquet-vs-csv}

| Fonctionnalité | Parquet | CSV |
|---------|---------|-----|
| Préservation du schéma | Oui (noms + types) | Non (types perdus) |
| Compression | Intégrée, colonnaire | Aucune par défaut |
| Taille | Beaucoup plus petite | Plus volumineuse |
| Sûreté des types | Une date reste une Date | Une date devient une String |
| Predicate pushdown | Oui | Non |
| Élagage de colonnes (column pruning) | Oui | Non |

## Quand utiliser quoi {#when-to-use-what}

| Format | Cas d'usage |
|--------|----------|
| **Parquet** | Par défaut pour l'analytique. Compatible avec Spark, Presto, Hive, Impala |
| **ORC** | Charges de travail optimisées pour Hive. Meilleure compression que Parquet dans Hive |
| **Avro** | Évolution de schéma, messages Kafka, ingestion en streaming |
| **CSV/JSON** | Échange de données, APIs, zones de transit lisibles par un humain |

## Points clés {#key-facts}
- Les formats colonnaires (Parquet, ORC) ne lisent que les colonnes nécessaires, ce qui est essentiel pour les tables analytiques larges
- Predicate pushdown : le moteur de requête transmet le filtre à la couche de stockage, qui ne lit que les groupes de lignes (row groups) correspondants
- Parquet et ORC prennent tous deux en charge les structures de données imbriquées
- Avro est le standard pour la sérialisation des messages Kafka avec Schema Registry
- Privilégier systématiquement Parquet/ORC pour le big data ; réserver CSV à l'échange de données

## Pièges à éviter {#gotchas}
- Un CSV lu avec `inferSchema=True` dans Spark parcourt l'intégralité du fichier, ce qui est lent sur de gros volumes
- Les fichiers Parquet ne sont pas lisibles par un humain : conservez des copies CSV pour le débogage
- Les codecs de compression (Snappy, GZIP, ZSTD) influencent le compromis entre vitesse de lecture et taille des fichiers
- ORC est étroitement lié à Hive ; Parquet est plus neutre vis-à-vis de l'écosystème

## Voir aussi {#see-also}
- [[hadoop-hdfs]] - couche de stockage
- [[apache-spark-core]] - formats de lecture/écriture Spark
- [[clickhouse-engines]] - compression ClickHouse
- [[data-lake-lakehouse]] - formats de tables ouverts (Delta, Iceberg, Hudi)
