---
title: ETL/ELT Pipelines
category: concepts
tags: [data-engineering, etl, elt, pipelines, data-integration]
---

# ETL/ELT Pipelines

ETL (Extract-Transform-Load) and ELT (Extract-Load-Transform) are the two fundamental patterns for moving data from source systems into analytical storage. The distinction lies in where transformation happens - outside or inside the target system.

## ETL vs ELT

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform location | External engine (Spark, Python) | Inside target DWH (SQL) |
| Best for | Complex transformations, legacy systems | Cloud DWH with strong compute |
| Latency | Higher (extra hop) | Lower |
| Flexibility | More control over transformation | Relies on target SQL capabilities |
| Modern tools | Spark, Airflow + Python | dbt, Snowflake, BigQuery |

## Three Steps

1. **Extract (E):** Pull data from sources, validate against specs, stage in intermediate area
2. **Transform (T):** Format conversion, encoding normalization, aggregation, cleansing, deduplication, business logic
3. **Load (L):** Write transformed data + metadata to target system (DWH, data mart, lake)

## Data Layers Architecture

```php
Sources -> [STG/Raw] -> [Core/DDS] -> [Marts] -> BI/Analytics
```

| Layer | Purpose |
|-------|---------|
| **Staging / Raw / ODS** | Raw data from sources, minimal transformation, preserves original format. Decouples extraction from transformation |
| **Core / DDS (Integration)** | Cleansed, integrated, historically tracked data. Data Vault, 3NF, or dimensional modeling applied here |
| **Mart / Presentation** | Business-ready aggregated views (star schema, flat tables). Each mart serves specific consumers |

## Pipeline Processing Modes

| Mode | Latency | Complexity | Best For |
|------|---------|-----------|----------|
| **Batch** | Minutes to hours | Low | BI, reporting, historical analysis |
| **Micro-batch** | Seconds to minutes | Medium | Near-real-time dashboards |
| **Stream** | Milliseconds | High | Fraud detection, monitoring, real-time features |

### Lambda Architecture
- **Batch layer:** complete, accurate data with higher latency
- **Speed layer:** real-time approximations
- **Serving layer:** merges both for queries

## Patterns

### Typical Spark ETL

```python
from pyspark.sql import SparkSession, functions as f

spark = SparkSession.builder.appName("etl").getOrCreate()

# Extract
df = spark.read.csv("s3a://bucket/raw/*.csv", header=True, schema=schema)

# Transform
result = (df
    .filter(f.col("vendor_id").isNotNull())
    .groupBy("vendor_id", f.to_date("pickup_datetime").alias("dt"))
    .agg(
        f.sum("total_amount").alias("sum_amount"),
        f.avg("tip_amount").alias("avg_tips")
    )
)

# Load
result.write.mode("overwrite").parquet("s3a://bucket/mart/daily_summary/")
```

### Write Modes
- `overwrite` - replace existing data
- `append` - add to existing data
- `ignore` - skip if data exists
- `error` (default) - fail if data exists

### Python Data Migration Script

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://user:pass@host:port/db')
df = pd.read_sql("SELECT * FROM source WHERE dt BETWEEN %s AND %s", engine, params=[start_dt, end_dt])
df.to_sql('target_table', engine, if_exists='append', index=False)
```

## Key Facts
- **Idempotency** is critical: re-running a pipeline with same inputs must produce same outputs. Use `overwrite` mode or delete-before-insert
- **Incremental loads** process only new/changed data using watermarks, CDC, or last-modified timestamps
- **Early filtering** pushes filters close to source to reduce data volume
- **Schema-first:** define explicit schemas rather than relying on inference
- **Partitioned writes** (`partitionBy("year", "month")`) enable efficient downstream reads

## Gotchas
- Airflow `schedule_interval` defines interval between runs, not run time. DAG with `@daily` and `start_date=2024-01-01` first runs on `2024-01-02`
- `catchup=True` (default) backfills all missed intervals since `start_date` - can flood the system
- SCD2 joins across satellites with different change frequencies cause Cartesian explosion on date ranges
- Small files problem: too many partitions create tiny files, degrading HDFS/S3 performance

## See Also
- [[apache-airflow]] - pipeline orchestration
- [[apache-spark-core]] - distributed processing engine
- [[dwh-architecture]] - target storage architecture
- [[data-quality]] - pipeline validation
- [[data-lake-lakehouse]] - modern storage targets
