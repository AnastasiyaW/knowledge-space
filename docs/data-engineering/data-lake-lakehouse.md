---
title: Data Lake and Lakehouse
category: concepts
tags: [data-engineering, data-lake, lakehouse, delta-lake, iceberg, hudi]
---

# Data Lake and Lakehouse

A data lake stores all data types without strict schema (schema-on-read). A lakehouse combines data lake storage flexibility with DWH capabilities like ACID transactions and SQL access.

## Data Lake

### What It Stores
- **Structured:** Database tables, CSV
- **Semi-structured:** JSON, XML, Avro
- **Unstructured:** Logs, video, images, text

### Advantages
- Scalable (add nodes horizontally)
- Economical (built on open-source: Hadoop, S3)
- Universal (all data types in one system)
- Fast hypothesis testing (no upfront schema design)

### Disadvantages
- Low data quality without governance controls
- Can become a "data swamp" without cataloging
- Difficulty determining data value

### Modern Pattern
1. Data Lake collects all raw data
2. DWH (or Lakehouse) stores processed analytical data

## Data Lakehouse

Combines Data Lake storage with DWH capabilities:
- Metadata catalogs and schemas
- ACID transaction support
- SQL access to data
- Optimized for both BI and ML workloads

## Open Table Formats

| Technology | Key Features |
|-----------|--------------|
| **Delta Lake** | ACID transactions, time travel, schema evolution, Z-ordering |
| **Apache Iceberg** | Hidden partitioning, partition evolution, snapshot isolation, vendor-neutral |
| **Apache Hudi** | Upserts, incremental processing, record-level changes, compaction |

All three provide:
- ACID semantics on object storage (S3, GCS, ADLS)
- Schema evolution without rewriting data
- Time travel / snapshot queries
- Metadata management for query optimization

## Key Facts
- S3 is 5-10x cheaper than HDFS for storage
- Lakehouse enables running BI and ML on the same data without copying
- Separation of storage and compute allows independent scaling
- Implementations: Databricks (Delta Lake), Snowflake, Apache Iceberg on Spark/Trino

## Gotchas
- Data Lake without governance becomes "data swamp" - always catalog and document
- Table formats require a query engine that understands them (Spark, Trino, Flink)
- Time travel has storage cost - old snapshots must be periodically cleaned
- Schema evolution does not mean schema-less - define schemas for discoverability

## See Also
- [[dwh-architecture]] - DWH comparison and evolution
- [[file-formats]] - Parquet, ORC, Avro details
- [[data-governance-catalog]] - preventing data swamp
- [[cloud-data-platforms]] - cloud implementations
