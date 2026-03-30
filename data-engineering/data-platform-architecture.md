---
title: Data Platform Architecture
category: concepts
tags: [architecture, data-platform, lambda, kappa, batch, streaming, components]
---

# Data Platform Architecture

A modern data platform integrates data ingestion, storage, processing, orchestration, and serving layers into a cohesive system. Understanding the overall architecture helps data engineers make technology choices and design scalable, maintainable pipelines.

## Key Facts

- **Key components**: data sources, ingestion layer, storage layer ([[data-lake]] / [[data-warehouse]]), processing layer ([[apache-spark]], SQL engines), orchestration layer ([[apache-airflow]]), serving layer (BI tools, APIs, ML models)
- **Batch processing**: scheduled processing of accumulated data. High throughput, high latency (minutes to hours). Tools: Spark, SQL-based transforms, dbt
- **Stream processing**: continuous processing of data as it arrives. Low latency (seconds to minutes). Tools: Kafka Streams, Flink, Spark Structured Streaming
- **Lambda architecture**: parallel batch + streaming paths. Batch layer for accuracy, speed layer for low latency, serving layer merges results. Complex to maintain (duplicate logic)
- **Kappa architecture**: streaming-only. All data flows through a streaming platform (Kafka). Reprocessing done by replaying the stream. Simpler than Lambda but requires stream processing maturity
- **ML lifecycle integration**: Raw Data -> Prep Data (feature engineering with Spark/pandas) -> Training (TensorFlow/PyTorch/Spark ML) -> Deploy (microservice/Spark Streaming/lambda) -> Monitor (drift detection)
- **Design approaches**: top-down (Inmon - enterprise DWH first, then data marts) vs bottom-up (Kimball - build data marts first, DWH emerges from conformed dimensions)
- Model staleness: production models degrade over time as data distributions shift. Build monitoring and retraining pipelines alongside serving

## Patterns

### Modern data platform layers

```
[Data Sources]          [Ingestion]         [Storage]           [Processing]        [Serving]
 OLTP databases    -->  CDC/Debezium   -->  Raw Zone (S3)  -->  Spark/dbt      -->  BI dashboards
 APIs              -->  Airflow tasks  -->  Data Lake      -->  SQL engines    -->  ML models
 Event streams     -->  Kafka          -->  Data Warehouse -->  Feature store  -->  APIs
 Files/logs        -->  File transfer  -->  Lakehouse      -->  Aggregations   -->  Reporting
```

### Technology stack example

```
Orchestration:     Apache Airflow / Dagster / Prefect
Ingestion:         Kafka + Debezium (CDC), Airbyte (API/DB), custom scripts
Storage:           S3 (data lake) + Snowflake/ClickHouse (DWH)
Processing:        Apache Spark (heavy transforms), dbt (SQL transforms)
Data Quality:      Great Expectations / dbt tests / Soda
ML Platform:       MLflow + Spark ML / PyTorch
Visualization:     Apache Superset / Metabase / Tableau
Metadata:          Hive Metastore / DataHub / Amundsen
```

### Distributed ML architecture

```
Parameter Server (model state)
    |
    +-- Worker 1 (data shard 1) ---> train local model ---> sync gradients
    +-- Worker 2 (data shard 2) ---> train local model ---> sync gradients
    +-- Worker 3 (data shard 3) ---> train local model ---> sync gradients
    |
    v
 Merged Model --> Evaluate --> Deploy as microservice
```

## Gotchas

- Lambda architecture requires maintaining the same business logic in two codebases (batch + streaming). Prefer Kappa or unified frameworks (Spark Structured Streaming) to avoid divergence
- "Build the data lake first, analysts will figure it out" never works. Without governance, catalog, and clear zones, a lake becomes a swamp
- Data platform is not just technology: organizational structure matters. Centralized data team bottlenecks; domain-oriented teams (data mesh) distribute ownership but require standards
- Start simple: PostgreSQL + Airflow + dbt covers most early-stage needs. Add Spark/Kafka when data volume or latency requirements demand it
- Metadata management (lineage, cataloging, documentation) is boring but essential. Build it from day one, not as an afterthought

## See Also

- [[data-warehouse]] - structured analytical storage
- [[data-lake]] - raw data storage
- [[etl-and-elt]] - pipeline patterns
- [[apache-airflow]] - orchestration
- [[apache-spark]] - distributed processing
- https://www.databricks.com/glossary/data-lakehouse - Lakehouse architecture
