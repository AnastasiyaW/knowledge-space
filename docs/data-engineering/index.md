---
title: Data Engineering
type: MOC
---

# Data Engineering

Knowledge base covering ETL/ELT, data pipelines, data warehousing, distributed computing, and the modern data stack.

## Concepts and Architecture

- [[etl-elt-pipelines]] - ETL vs ELT, pipeline design, processing modes, idempotency
- [[dwh-architecture]] - OLTP vs OLAP, DWH layers, Kimball vs Inmon, platform evolution
- [[data-modeling]] - normalization (1NF-3NF), ER diagrams, keys, deduplication patterns
- [[dimensional-modeling]] - star/snowflake schema, fact/dimension tables, Kimball design
- [[data-vault]] - Hub/Link/Satellite, Data Vault 2.0, anchor modeling
- [[scd-patterns]] - slowly changing dimensions, SCD2 merge logic
- [[data-lake-lakehouse]] - data lake, lakehouse, Delta Lake, Iceberg, Hudi
- [[data-quality]] - quality dimensions, observability, monitoring, alerting
- [[data-governance-catalog]] - DAMA DMBOK, data catalog, GDPR compliance
- [[data-lineage-metadata]] - lineage types, metadata categories, Prometheus+Grafana
- [[file-formats]] - Parquet, ORC, Avro, CSV comparison

## Distributed Processing

- [[apache-spark-core]] - Spark architecture, execution model, Catalyst optimizer
- [[pyspark-dataframe-api]] - DataFrame operations, schemas, I/O, Spark SQL
- [[spark-optimization]] - partitioning, skew handling, broadcast joins, AQE
- [[spark-streaming]] - Structured Streaming, micro-batch, DStreams
- [[apache-kafka]] - event streaming, PubSub, topics, consumer groups
- [[mapreduce]] - Map/Reduce paradigm, shuffle, Hadoop Streaming

## Storage and Databases

- [[hadoop-hdfs]] - HDFS architecture, blocks, replication, small files problem
- [[apache-hive]] - SQL-on-Hadoop, Metastore, join strategies (MapJoin, SMB)
- [[hbase]] - columnar NoSQL, row key, column families, versioning
- [[clickhouse]] - columnar OLAP, partitions, granules, primary key, functions
- [[clickhouse-engines]] - MergeTree family, compression, skip indexes
- [[greenplum-mpp]] - MPP architecture, distribution, motion operators
- [[postgresql-administration]] - transactions, MVCC, PL/pgSQL, query optimization
- [[mongodb-nosql]] - document store, CAP theorem, aggregation pipelines

## Infrastructure and Tools

- [[apache-airflow]] - DAG orchestration, operators, TaskFlow API, XCom
- [[cloud-data-platforms]] - AWS/GCP/Azure, Snowflake, BigQuery, S3
- [[docker-for-de]] - containers, Dockerfile, docker-compose
- [[kubernetes-for-de]] - K8s architecture, Spark on K8s, Helm
- [[yarn-resource-management]] - YARN vs JobTracker, queues, schedulers

## Cross-Cutting

- [[mlops-feature-store]] - MLflow, feature stores, model serving, CRISP-DM
- [[sql-for-de]] - window functions, CTEs, recursive queries, optimization
- [[python-for-de]] - database access, Pandas, functional programming, testing

## Cross-Topic Links

- [[sql-databases/index]] - deep SQL reference
- [[python/index]] - Python language fundamentals
- [[devops/index]] - CI/CD, infrastructure as code
- [[architecture/index]] - system design patterns
- [[data-science/index]] - ML and analytics
- [[bi-analytics/index]] - BI tools and dashboards
