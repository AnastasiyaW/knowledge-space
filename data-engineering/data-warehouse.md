---
title: Data Warehouse
category: concepts
tags: [dwh, olap, oltp, dimensional-modeling, analytics, bi]
---

# Data Warehouse

A data warehouse (DWH) is a central repository of structured, cleaned, integrated data optimized for analytical queries and reporting. Unlike operational databases ([[postgresql-for-data-engineering]]), a DWH prioritizes read-heavy analytical workloads (OLAP) over transactional consistency (OLTP).

## Key Facts

- **DWH principles**: data must have strict structure, maintain consistency, always be ready for consumption (pre-aggregated or modeled)
- **OLTP vs OLAP**: OLTP handles many small transactions with row-level access; OLAP handles few complex queries scanning large column ranges
- Column-oriented storage (e.g., [[clickhouse]], Redshift, BigQuery) dramatically accelerates OLAP: reads only needed columns, compresses similar-type data 5-10x better
- **Data mart** - a subset of the DWH focused on a single business domain (marketing, finance). Built as views or materialized tables on top of the DWH
- **Layered architecture**: raw/landing -> staging -> DWH (core) -> data marts
- Cloud DWH (BigQuery, Snowflake, Redshift) separate storage from compute, enabling elastic scaling and pay-per-query pricing
- On-prem DWH ([[greenplum-and-mpp]], Vertica) use MPP (Massively Parallel Processing) architecture to distribute queries across nodes

## Patterns

### Three-layer DWH architecture

```
Sources (OLTP, APIs, logs)
    |
    v
[Raw Layer]          -- as-is copies, append-only
    |
    v
[Staging/ODS Layer]  -- cleaned, deduplicated, typed
    |
    v
[DWH Core Layer]     -- dimensional model (star/snowflake schema)
    |
    v
[Data Marts]         -- domain-specific aggregations
```

### OLAP vs OLTP comparison

| Characteristic | OLTP | OLAP |
|---|---|---|
| Query pattern | Short, row-level | Long, column scans |
| Users | Application, many concurrent | Analysts, few concurrent |
| Data model | Normalized (3NF) | Denormalized (star/snowflake) |
| Storage | Row-oriented | Column-oriented |
| Optimization | Index on PK/FK | Partitioning, columnar compression |

## Gotchas

- Do not use DWH for real-time queries with <100ms latency; use OLTP databases or caching layers
- "Data Warehouse" and "Data Lake" are not competing concepts - modern architectures use both. DWH stores curated, modeled data; [[data-lake]] stores raw everything
- Slowly Changing Dimensions (SCD) require explicit handling - see [[data-modeling]] for Type 1/2/3 patterns
- Cloud DWH costs can explode with poorly written queries scanning full tables. Always use `WHERE` filters on partitioned columns

## See Also

- [[data-modeling]] - star schema, snowflake schema, SCD
- [[data-lake]] - complementary storage for raw/unstructured data
- [[clickhouse]] - column-oriented OLAP engine
- [[greenplum-and-mpp]] - on-prem MPP data warehouse
- https://cloud.google.com/bigquery/docs - BigQuery documentation
- https://docs.snowflake.com/ - Snowflake documentation
