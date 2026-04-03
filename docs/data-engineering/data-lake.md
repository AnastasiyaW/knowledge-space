---
title: Data Lake
category: concepts
tags: [data-lake, lakehouse, raw-data, unstructured, s3, hdfs]
---

# Data Lake

A data lake is a centralized repository that stores all types of data (structured, semi-structured, unstructured) in their raw format at any scale. Unlike a [[data-warehouse]], data does not need to be cleaned or structured before ingestion.

## Key Facts

- **Core principles**: easily add new sources, accept all data types (CSV, JSON, images, video, audio), store everything that ever arrives, derive new features from historical data
- Data lake stores raw data first, processes later (schema-on-read), while DWH requires schema-on-write
- Better suited for data scientists who need to explore raw data and engineer features without waiting for DWH team to model new attributes
- Common storage backends: HDFS (on-prem), Amazon S3, Google Cloud Storage, Azure Data Lake Storage
- **Data Lakehouse** (Delta Lake, Apache Iceberg, Apache Hudi) combines lake flexibility with DWH features: ACID transactions, schema enforcement, time travel, optimized reads via statistics and Z-ordering
- **Zones** pattern: Landing/Raw -> Cleansed/Refined -> Curated/Business. Each zone progressively adds structure and quality guarantees
- Risk: without governance, a data lake becomes a "data swamp" - uncatalogued, untrusted, undocumented

## Patterns

### Data Lake zones on S3

```
s3://data-lake/
    raw/                    # as-is from sources, partitioned by date
        source=crm/
            dt=2026-03-30/
                users.json
        source=events/
            dt=2026-03-30/
                clicks.parquet
    refined/                # cleaned, typed, deduplicated
        users/
            dt=2026-03-30/
                part-00000.parquet
    curated/                # business-ready aggregations
        user_activity_daily/
            dt=2026-03-30/
                part-00000.parquet
```

### Delta Lake table creation (PySpark)

```python
df.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("dt") \
    .save("s3://data-lake/refined/users")

# Time travel - read previous version
spark.read.format("delta").option("versionAsOf", 5).load(path)
```

## Gotchas

- Data lake does NOT mean "dump and forget." Without metadata catalog (Glue Catalog, Hive Metastore, Unity Catalog), data becomes undiscoverable
- Small files problem: thousands of tiny files degrade query performance on HDFS/S3. Use compaction (e.g., `OPTIMIZE` in Delta Lake) or write in larger batches
- Raw zone should be immutable (append-only). Never modify raw data - apply transformations in downstream zones
- Access control is harder than in RDBMS. Use IAM policies + lake-level ACLs (Lake Formation, Unity Catalog) rather than per-file permissions

## See Also

- [[data-warehouse]] - structured analytical storage
- [[hdfs]] - distributed file system for on-prem data lakes
- [[data-formats]] - Parquet, Avro, ORC for efficient lake storage
- https://delta.io/ - Delta Lake documentation
- https://iceberg.apache.org/ - Apache Iceberg documentation
