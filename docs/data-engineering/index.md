---
title: Data Engineering
type: MOC
---

# Data Engineering

## Pipeline Patterns
- [[etl-and-elt]] - ETL vs ELT, incremental loads, CDC, idempotency, orchestrator integration
- [[data-quality]] - Schema validation, row/aggregate tests, dbt tests, Great Expectations, observability

## Storage & Architecture
- [[data-warehouse]] - DWH concepts, OLAP vs OLTP, layered architecture, cloud vs on-prem
- [[data-lake]] - Raw data storage, zones pattern, lakehouse (Delta/Iceberg), schema-on-read
- [[data-platform-architecture]] - End-to-end platform design, Lambda/Kappa, ML lifecycle, technology stacks

## Data Modeling
- [[data-modeling]] - Star/snowflake schema, fact/dimension tables, SCD types, surrogate keys
- [[normalization]] - Normal forms (1NF-3NF-BCNF), denormalization trade-offs, OLTP vs OLAP design

## Distributed Processing
- [[hadoop-ecosystem]] - HDFS, YARN, MapReduce, Hive Metastore, ecosystem overview
- [[hdfs]] - NameNode/DataNode, replication, block storage, HA architecture, small files problem
- [[mapreduce]] - Map/Shuffle/Reduce phases, combiners, partitioners, key-value model
- [[apache-spark]] - SparkSession, RDD, DataFrame, lazy evaluation, deploy modes, spark-submit
- [[spark-sql-and-dataframes]] - SQL API, DataFrame operations, Catalyst optimizer, UDFs, window functions
- [[spark-ml]] - Pipeline API, Transformer/Estimator, VectorAssembler, cross-validation, model persistence

## Orchestration
- [[apache-airflow]] - DAGs, operators, sensors, XCom, scheduling, Jinja templating, execution_date

## Databases for DE
- [[clickhouse]] - Column-oriented OLAP, MergeTree engines, array functions, LowCardinality, batch inserts
- [[postgresql-for-data-engineering]] - Indexes, partitioning, PL/pgSQL, COPY, query optimization, MERGE
- [[greenplum-and-mpp]] - MPP architecture, distribution policies, gpfdist, resource management

## Infrastructure
- [[data-formats]] - Parquet, ORC, Avro, CSV, JSON - comparison, compression, predicate pushdown
- [[partitioning-and-sharding]] - Range/list/hash partitioning, sharding strategies, replication, co-location
