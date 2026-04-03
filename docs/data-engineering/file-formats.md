---
title: File Formats for Big Data
category: reference
tags: [data-engineering, parquet, orc, avro, file-formats, columnar]
---

# File Formats for Big Data

Choosing the right file format significantly impacts storage efficiency, query performance, and compatibility across the Hadoop/Spark ecosystem.

## Format Comparison

| Format | Type | Splittable | Schema | Compression | Best For |
|--------|------|-----------|--------|-------------|----------|
| **Text/CSV** | Row | Yes (uncompressed) | No | External | Simple interchange |
| **SequenceFile** | Row (binary KV) | Yes | No | Block/Record | MR intermediate data |
| **Avro** | Row (binary) | Yes | Embedded | Block | Schema evolution, streaming |
| **ORC** | Columnar | Yes | Embedded | Column-level | Hive-optimized analytics |
| **Parquet** | Columnar | Yes | Embedded | Column-level | Cross-ecosystem analytics |

## Parquet vs CSV

| Feature | Parquet | CSV |
|---------|---------|-----|
| Schema preservation | Yes (names + types) | No (types lost) |
| Compression | Built-in, columnar | None by default |
| Size | Much smaller | Larger |
| Type safety | Date stays Date | Date becomes String |
| Predicate pushdown | Yes | No |
| Column pruning | Yes | No |

## When to Use What

| Format | Use Case |
|--------|----------|
| **Parquet** | Default for analytics. Works with Spark, Presto, Hive, Impala |
| **ORC** | Hive-optimized workloads. Better compression than Parquet in Hive |
| **Avro** | Schema evolution, Kafka messages, streaming ingest |
| **CSV/JSON** | Data exchange, APIs, human-readable staging |

## Key Facts
- Columnar formats (Parquet, ORC) read only needed columns - critical for wide analytical tables
- Predicate pushdown: query engine pushes filter to storage layer, reading only matching row groups
- Parquet and ORC both support nested data structures
- Avro is the standard for Kafka message serialization with Schema Registry
- Always prefer Parquet/ORC for big data; use CSV only for interchange

## Gotchas
- CSV with `inferSchema=True` in Spark reads the entire file - slow on large data
- Parquet files are not human-readable - keep CSV copies for debugging
- Compression codecs (Snappy, GZIP, ZSTD) affect read speed vs file size tradeoff
- ORC is tightly coupled with Hive; Parquet is more ecosystem-neutral

## See Also
- [[hadoop-hdfs]] - storage layer
- [[apache-spark-core]] - Spark read/write formats
- [[clickhouse-engines]] - ClickHouse compression
- [[data-lake-lakehouse]] - open table formats (Delta, Iceberg, Hudi)
