---
title: HBase
category: tools
tags: [data-engineering, hbase, nosql, columnar, hadoop, key-value]
---

# HBase

HBase is a columnar NoSQL store within the Hadoop ecosystem, designed for billions of rows and millions of columns. Runs on top of HDFS. No SQL - uses API methods (GET, PUT, SCAN, DELETE).

## Data Model

```
Table
  |-- Row Key (primary access path, binary sorted)
  |-- Column Family 1
  |     |-- column1: value (timestamp v3)
  |     |-- column1: value (timestamp v2)  <- versioning
  |     |-- column2: value
  |-- Column Family 2
        |-- columnA: value
```

## Key Concepts

| Concept | Details |
|---------|---------|
| **Row Key** | Unique ID, ALL access by row key or key range |
| **Column Family** | Defined at creation. Groups columns with shared properties (compression, TTL, versions) |
| **Versioning** | Built-in. Multiple versions per cell with timestamps. Configurable per family |
| **Binary storage** | All values stored in binary. App handles serialization |
| **Free schema** | Columns added dynamically within existing column families |

## HBase vs RDBMS

| Feature | HBase | RDBMS |
|---------|-------|-------|
| Schema | Flexible | Fixed |
| Scale | Billions of rows | Limited (unless MPP) |
| Access pattern | Key/key-range lookups | Arbitrary SQL |
| Joins | Not natively | Full support |
| Transactions | Row-level atomic | ACID across tables |
| Query language | API calls | SQL |

## Properties
- Column families stored separately on HDFS
- Efficient for key-based and key-range lookups
- TTL for automatic data expiration
- MapReduce integration (input/output)
- Versions stored in descending order (newest first)

## Gotchas
- No SQL - all access through GET, PUT, SCAN, DELETE API
- Row key design is critical - poor key design leads to hotspots
- Column families must be defined at table creation
- Not suitable for arbitrary analytical queries (use Hive/Spark on top)

## See Also
- [[hadoop-hdfs]] - underlying storage
- [[clickhouse]] - alternative columnar OLAP
- [[data-lake-lakehouse]] - NoSQL in data platform context
