---
title: Data Warehouse Architecture
category: concepts
tags: [data-engineering, dwh, data-warehouse, olap, oltp, architecture]
---

# Data Warehouse Architecture

A data warehouse (DWH) is a subject-oriented, integrated, non-volatile, time-variant collection of data organized to support decision-making (Bill Inmon). DWH exists because OLTP and OLAP workloads are fundamentally incompatible in one system.

## OLTP vs OLAP

| Characteristic | OLTP | OLAP |
|---------------|------|------|
| Purpose | Transaction processing | Analytical queries |
| Queries | Simple, frequent, identical | Complex, infrequent, ad-hoc |
| Users | Many concurrent | Few analysts |
| Data | Current, operational | Historical, aggregated |
| Operations | Read/write (CRUD) | Mostly read |
| Latency | Micro/milliseconds | Seconds to minutes |
| Examples | PostgreSQL, MySQL (per-service) | Snowflake, ClickHouse, Greenplum |

## DWH Properties (Inmon)

| Property | Meaning |
|----------|---------|
| **Subject-oriented** | Covers specific business domains; irrelevant data excluded |
| **Integrated** | No contradictions between data from different sources |
| **Non-volatile** | Data only appended, never modified or deleted |
| **Time-variant** | Maintains maximum historical depth |

## DWH Layers

```rust
Sources -> Staging Area -> Central Warehouse -> Data Marts -> BI/Analytics
```

| Layer | Purpose |
|-------|---------|
| **Staging Area** | Raw data landing, cleansing, normalization before loading |
| **MDM (Master Data)** | Reference/lookup data ensuring consistency |
| **Central Warehouse** | Historical, subject-oriented, integrated data |
| **Data Marts / Cubes** | Specialized views for specific analytical tasks |

## Design Approaches

### Kimball (Bottom-Up)
- DWH = collection of data marts
- Design marts per consumer need (star schema)
- Fast to deliver business value
- **Drawbacks:** marts may define metrics differently; hard to standardize

### Inmon (Top-Down)
- Build enterprise DWH first (3NF), then derive marts
- Single source of truth, better consistency
- **Drawbacks:** longer initial development, more complex

### Data Vault 2.0
- Handles many sources with different schemas
- Append-only, full auditability
- Business rules isolated in mart layer
- See [[data-vault]] for details

## Platform Evolution

```rust
Gen 1: RDBMS DWH (Oracle, DB2) - 1990s
  -> Rigid schema, ETL, batch only

Gen 2: Hadoop ecosystem (HDFS + MapReduce) - 2007+
  -> Data Lake, schema-on-read, horizontal scale

Gen 3: Cloud DWH + Lakehouse - 2015+
  -> Snowflake, Databricks, BigQuery
  -> ELT, auto-scaling, separation of compute/storage

Gen 4: Data Mesh / Data Products - 2020+
  -> Domain-owned data, self-serve platform, federated governance
```

## Choosing Architecture

| Scenario | Recommended |
|----------|-------------|
| Small company, structured data, BI focus | Cloud DWH (Snowflake, BigQuery) |
| Mixed data types, ML workloads | Data Lakehouse (Databricks, Iceberg) |
| Enterprise, many sources, compliance | DWH + Data Lake hybrid |
| Real-time + batch analytics | Lambda/Kappa with streaming layer |
| Many autonomous data teams | Data Mesh with self-serve platform |

## Gotchas
- Star schema denormalization trades storage for query performance - acceptable for OLAP
- Data Vault adds many joins - mart layer must pre-join for acceptable query performance
- OLTP databases should never be queried directly for analytics - always replicate to DWH
- Batch window must complete before business hours - monitor and alert on SLA breaches
- Data Lake without governance becomes "data swamp"

## See Also
- [[data-modeling]] - normalization theory
- [[dimensional-modeling]] - Kimball star/snowflake schemas
- [[data-vault]] - Data Vault methodology
- [[data-lake-lakehouse]] - lake and lakehouse patterns
- [[cloud-data-platforms]] - cloud DWH implementations
