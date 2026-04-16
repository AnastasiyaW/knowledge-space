---
title: Big Data and ML Architecture
category: concepts
tags: [bigdata, machine-learning, data-pipeline, etl, data-lake, data-warehouse, mlops]
---

# Big Data and ML Architecture

Architecture for processing large data volumes and integrating ML models into production. The architect chooses appropriate processing platforms, designs data pipelines, and ensures data governance.

## Data Processing Paradigms

| Paradigm | Processing | Technologies | Best For |
|----------|-----------|--------------|----------|
| **Batch** | Scheduled intervals, large volumes | Hadoop, Spark, Hive | ETL, reports, historical analysis |
| **Stream** | Continuous, real-time | Kafka Streams, Flink, Storm | Fraud detection, real-time recs |

### Lambda Architecture
Combines batch and stream. Batch layer (accurate), speed layer (real-time), serving layer merges both. **Drawback:** maintaining two codebases.

### Kappa Architecture
Only stream processing for everything. Reprocessing by replaying stream. Simpler but not for all workloads.

## Data Storage Solutions

| Solution | Approach | Technologies | Risk |
|----------|----------|-------------|------|
| **Data Lake** | Raw data, schema-on-read | HDFS, S3, Azure Data Lake | "Data swamp" without governance |
| **Data Warehouse** | Processed, schema-on-write | Snowflake, BigQuery, Redshift, ClickHouse | Rigid schema changes |
| **Data Lakehouse** | Lake flexibility + warehouse structure | Delta Lake, Apache Iceberg, Hudi | Newer, less mature |

### Data Modeling Approaches

| Model | Loading | Change Tracking | Best For |
|-------|---------|----------------|----------|
| **Inmon (3NF)** | Complex (dependency order) | Poor | Already normalized sources |
| **Kimball (Star)** | Simpler | SCD Type 2 adds complexity | Simple analytics |
| **Data Vault** | Simplest (independent loads) | Native (satellites + timestamps) | Evolving, changing data |
| **Anchor Model** | Most flexible | Most flexible | Extreme flexibility needs |

## ETL vs ELT

| Approach | Process | Best For |
|----------|---------|----------|
| **ETL** | Transform before loading | Traditional DWH |
| **ELT** | Load raw, transform in target | Modern cloud DWH (leverage scalable compute) |

## ML Pipeline

```php
Data collection -> Preparation/cleaning -> Feature engineering ->
  Model training -> Evaluation -> Deployment -> Monitoring/retraining
```

### Model Serving Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Batch prediction** | Pre-compute predictions | Recommendations, risk scores |
| **Real-time inference** | Online prediction via API | Search, fraud detection |
| **Edge inference** | On-device | Mobile, IoT |
| **Embedded model** | Model within app code | Lightweight predictions |

### MLOps
Applying DevOps to ML: version control for data + models, automated training pipelines, A/B testing for deployment, monitoring model drift.

**Feature Store:** Centralized ML features repository. Consistency between training and serving. Products: Feast, Tecton, Vertex AI Feature Store.

## Data Pipeline Architecture Example

```bash
[Source 1C] --> [Kafka topic] --> [Airflow orchestrator] --> [DWH (PostgreSQL)]
[Source CRM] --> [Kafka topic] -->                               |
[External API] --> [API Fetcher] -->                             |
                                                          [Data Marts]
                                                               |
                                                          [BI Dashboard]
```

**Key decisions:**
- Internal systems **push** changes to Kafka (source knows when data changes)
- External API: **pull** (our system fetches periodically)
- Airflow for ETL orchestration (monitoring, retries, error handling)
- Custom PHP/Python scripts strongly discouraged - use proper orchestration

## Technology Stack

| Category | Technologies |
|----------|-------------|
| Batch processing | Hadoop, Spark, Hive |
| Stream processing | Kafka Streams, Flink, Spark Streaming |
| Storage | HDFS, S3, Delta Lake |
| Data warehouse | Snowflake, BigQuery, Redshift, ClickHouse |
| Orchestration | Airflow, Prefect, Dagster |
| ML platforms | MLflow, Kubeflow, SageMaker, Vertex AI |
| Data quality | Great Expectations, dbt tests |

## Architecture Considerations

- **Volume** - TB vs PB determines storage and processing choices
- **Velocity** - real-time drives streaming vs batch
- **Variety** - structured/semi-structured/unstructured affects storage
- **Data governance** - privacy (GDPR), access control, audit trails, lineage
- **Cost** - right-sizing compute, storage tiering, spot instances
- **Data quality** - garbage in = garbage out. Validate at pipeline entry

## Gotchas

- **Data lake without governance** becomes "data swamp" - nobody can find or trust data
- **Real-time not always needed** - daily batch may suffice for director checking morning reports
- **Source data changes retroactively** - sales data can change for 1+ year (refunds, recalculations). Design for immutable history (Data Vault)
- **Pull from source DB is risky** - you don't know about all data changes, schema changes break scripts. Prefer push model

## See Also

- [[kafka-architecture]] - Event streaming for data pipelines
- [[database-selection]] - OLTP vs OLAP, database types
- [[distributed-systems-fundamentals]] - Partitioning, replication for big data
- [[devops-cicd]] - MLOps as extension of DevOps
