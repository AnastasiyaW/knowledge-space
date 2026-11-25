---
title: "Data Engineering"
type: MOC
level: 3
source_sha256: 406d798e48001556f3deaf261af8f0ad482d54b626c4e9897e9bb49ab4c64525
translation: machine
translated_at: '2026-10-24'
---
# Data Engineering {#data-engineering}

Wissensdatenbank zu ETL/ELT, Datenpipelines, Data Warehousing, verteilter Datenverarbeitung und dem modernen Data Stack.

## Konzepte und Architektur {#concepts-and-architecture}

- [[etl-elt-pipelines]] - ETL vs. ELT, Pipeline-Design, Verarbeitungsmodi, Idempotenz
- [[dwh-architecture]] - OLTP vs. OLAP, DWH-Schichten, Kimball vs. Inmon, Plattformentwicklung
- [[data-modeling]] - Normalisierung (1NF-3NF), ER-Diagramme, Schlüssel, Deduplizierungsmuster
- [[dimensional-modeling]] - Stern-/Schneeflockenschema, Fakten- und Dimensionstabellen, Kimball-Design
- [[data-vault]] - Hub/Link/Satellite, Data Vault 2.0, Anchor Modeling
- [[scd-patterns]] - langsam veränderliche Dimensionen, SCD2-Merge-Logik
- [[data-lake-lakehouse]] - Data Lake, Lakehouse, Delta Lake, Iceberg, Hudi
- [[data-quality]] - Qualitätsdimensionen, Observability, Monitoring, Alerting
- [[data-governance-catalog]] - DAMA DMBOK, Data Catalog, DSGVO-Konformität
- [[data-lineage-metadata]] - Lineage-Typen, Metadaten-Kategorien, Prometheus+Grafana
- [[file-formats]] - Vergleich Parquet, ORC, Avro, CSV

## Verteilte Verarbeitung {#distributed-processing}

- [[apache-spark-core]] - Spark-Architektur, Ausführungsmodell, Catalyst Optimizer
- [[pyspark-dataframe-api]] - DataFrame-Operationen, Schemas, I/O, Spark SQL
- [[spark-optimization]] - Partitionierung, Skew-Behandlung, Broadcast Joins, AQE
- [[spark-streaming]] - Structured Streaming, Micro-Batch, DStreams
- [[apache-kafka]] - Event Streaming, PubSub, Topics, Consumer Groups
- [[mapreduce]] - Map/Reduce-Paradigma, Shuffle, Hadoop Streaming

## Speicher und Datenbanken {#storage-and-databases}

- [[hadoop-hdfs]] - HDFS-Architektur, Blöcke, Replikation, Small-Files-Problem
- [[apache-hive]] - SQL-on-Hadoop, Metastore, Join-Strategien (MapJoin, SMB)
- [[hbase]] - spaltenorientiertes NoSQL, Row Key, Column Families, Versionierung
- [[clickhouse]] - spaltenorientiertes OLAP, Partitionen, Granules, Primärschlüssel, Funktionen
- [[clickhouse-engines]] - MergeTree-Familie, Kompression, Skip Indizes
- [[greenplum-mpp]] - MPP-Architektur, Verteilung, Motion-Operatoren
- [[postgresql-administration]] - Transaktionen, MVCC, PL/pgSQL, Abfrageoptimierung
- [[mongodb-nosql]] - Dokumentenspeicher, CAP-Theorem, Aggregation Pipelines

## Infrastruktur und Tools {#infrastructure-and-tools}

- [[apache-airflow]] - DAG-Orchestrierung, Operatoren, TaskFlow API, XCom
- [[cloud-data-platforms]] - AWS/GCP/Azure, Snowflake, BigQuery, S3
- [[docker-for-de]] - Container, Dockerfile, docker-compose
- [[kubernetes-for-de]] - K8s-Architektur, Spark on K8s, Helm
- [[yarn-resource-management]] - YARN vs. JobTracker, Queues, Scheduler

## Querschnittsthemen {#cross-cutting}

- [[mlops-feature-store]] - MLflow, Feature Stores, Model Serving, CRISP-DM
- [[sql-for-de]] - Fensterfunktionen, CTEs, rekursive Abfragen, Optimierung
- [[python-for-de]] - Datenbankzugriff, Pandas, funktionale Programmierung, Testing

## Querverweise auf andere Themen {#cross-topic-links}

- [[sql-databases/index]] - SQL-Referenz im Detail
- [[python/index]] - Grundlagen der Python-Sprache
- [[devops/index]] - CI/CD, Infrastructure as Code
- [[architecture/index]] - Muster für Systemdesign
- [[data-science/index]] - ML und Analytik
- [[bi-analytics/index]] - BI-Tools und Dashboards

## Weitere Referenzen {#additional-references}

- [[vector-search-at-scale]] - Skalierung von embedding-basierter Ähnlichkeitssuche von zehntausenden bis zu Millionen von Vektoren
