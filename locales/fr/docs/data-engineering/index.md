---
title: "Ingénierie des données"
type: MOC
level: 3
source_sha256: 406d798e48001556f3deaf261af8f0ad482d54b626c4e9897e9bb49ab4c64525
translation: machine
translated_at: '2026-10-24'
---
# Ingénierie des données {#data-engineering}

Base de connaissances couvrant l'ETL/ELT, les pipelines de données, l'entrepôt de données, le calcul distribué et la stack data moderne.

## Concepts et architecture {#concepts-and-architecture}

- [[etl-elt-pipelines|ETL/ELT]] - ETL vs ELT, conception de pipelines, modes de traitement, idempotence
- [[dwh-architecture]] - OLTP vs OLAP, couches du DWH, Kimball vs Inmon, évolution des plateformes
- [[data-modeling]] - normalisation (1NF-3NF), diagrammes ER, clés, modèles de déduplication
- [[dimensional-modeling]] - schéma en étoile/flocon, tables de faits/dimensions, conception Kimball
- [[data-vault]] - Hub/Link/Satellite, Data Vault 2.0, modélisation par ancres
- [[scd-patterns]] - dimensions à évolution lente, logique de merge SCD2
- [[data-lake-lakehouse]] - data lake, lakehouse, Delta Lake, Iceberg, Hudi
- [[data-quality]] - dimensions de qualité, observabilité, supervision, alerting
- [[data-governance-catalog]] - DAMA DMBOK, catalogue de données, conformité RGPD
- [[data-lineage-metadata]] - types de lignage, catégories de métadonnées, Prometheus+Grafana
- [[file-formats]] - comparaison Parquet, ORC, Avro, CSV

## Traitement distribué {#distributed-processing}

- [[apache-spark-core]] - architecture Spark, modèle d'exécution, optimiseur Catalyst
- [[pyspark-dataframe-api]] - opérations sur les DataFrames, schémas, E/S, Spark SQL
- [[spark-optimization]] - partitionnement, gestion du skew, broadcast joins, AQE
- [[spark-streaming]] - Structured Streaming, micro-batch, DStreams
- [[apache-kafka]] - streaming d'événements, PubSub, topics, groupes de consommateurs
- [[mapreduce]] - paradigme Map/Reduce, shuffle, Hadoop Streaming

## Stockage et bases de données {#storage-and-databases}

- [[hadoop-hdfs]] - architecture HDFS, blocs, réplication, problème des petits fichiers
- [[apache-hive]] - SQL sur Hadoop, Metastore, stratégies de jointure (MapJoin, SMB)
- [[hbase]] - NoSQL en colonnes, row key, column families, versionnement
- [[clickhouse]] - OLAP en colonnes, partitions, granules, clé primaire, fonctions
- [[clickhouse-engines]] - famille MergeTree, compression, index de saut
- [[greenplum-mpp]] - architecture MPP, distribution, opérateurs de motion
- [[postgresql-administration]] - transactions, MVCC, PL/pgSQL, optimisation des requêtes
- [[mongodb-nosql]] - document store, théorème CAP, pipelines d'agrégation

## Infrastructure et outils {#infrastructure-and-tools}

- [[apache-airflow]] - orchestration de DAG, opérateurs, TaskFlow API, XCom
- [[cloud-data-platforms]] - AWS/GCP/Azure, Snowflake, BigQuery, S3
- [[docker-for-de]] - conteneurs, Dockerfile, docker-compose
- [[kubernetes-for-de]] - architecture K8s, Spark sur K8s, Helm
- [[yarn-resource-management]] - YARN vs JobTracker, files d'attente, ordonnanceurs

## Transversal {#cross-cutting}

- [[mlops-feature-store]] - MLflow, feature stores, model serving, CRISP-DM
- [[sql-for-de]] - fonctions de fenêtrage, CTE, requêtes récursives, optimisation
- [[python-for-de]] - accès aux bases de données, Pandas, programmation fonctionnelle, tests

## Liens vers d'autres sujets {#cross-topic-links}

- [[sql-databases/index]] - référence SQL approfondie
- [[python/index]] - fondamentaux du langage Python
- [[devops/index]] - CI/CD, infrastructure as code
- [[architecture/index]] - patterns de conception de systèmes
- [[data-science/index]] - ML et analytique
- [[bi-analytics/index]] - outils BI et tableaux de bord

## Références complémentaires {#additional-references}

- [[vector-search-at-scale]] - Passage à l'échelle de la recherche de similarité basée sur les embeddings, de quelques dizaines de milliers à plusieurs millions de vecteurs
