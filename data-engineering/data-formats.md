---
title: Data Formats
category: concepts
tags: [parquet, avro, orc, csv, json, serialization, columnar, compression]
---

# Data Formats

Choosing the right data format determines storage efficiency, query performance, and interoperability across the data engineering stack. Column-oriented formats (Parquet, ORC) dominate analytical workloads, while row-oriented formats (Avro, JSON, CSV) serve streaming and interchange use cases.

## Key Facts

- **Apache Parquet**: columnar format, de facto standard for [[data-lake]] and [[apache-spark]]. Supports nested types, predicate pushdown, column pruning, multiple compression codecs (Snappy default, ZSTD, LZ4, GZIP)
- **Apache ORC**: columnar format, native to Hive ecosystem. Built-in lightweight indexes (min/max/count per stripe), ACID support in Hive. Slightly better compression than Parquet on some workloads
- **Apache Avro**: row-oriented, schema embedded in file header (self-describing). Compact binary encoding. Primary use: Kafka messages, data serialization with schema evolution. Supports schema evolution (add/remove fields with defaults)
- **CSV**: universal interchange format, no schema, no types, no compression (by default). Human-readable but inefficient for large datasets
- **JSON/JSONB**: semi-structured, self-describing. Verbose (field names repeated per record). Good for APIs and config, poor for analytics at scale
- **Compression codecs**: Snappy (fast, moderate ratio), ZSTD (excellent ratio, good speed), LZ4 (fastest, lower ratio), GZIP (best ratio, slow). Choose based on read-vs-write tradeoff
- **Predicate pushdown**: columnar formats embed min/max statistics per column chunk. Query engines skip chunks that cannot contain matching rows, reducing I/O dramatically

## Patterns

### Format comparison matrix

| Feature | Parquet | ORC | Avro | CSV | JSON |
|---|---|---|---|---|---|
| Orientation | Columnar | Columnar | Row | Row | Row |
| Schema | Embedded | Embedded | Embedded | None | Self-describing |
| Compression | Excellent | Excellent | Good | None (raw) | Poor |
| Nested types | Yes | Yes | Yes | No | Yes |
| Schema evolution | Limited | Limited | Full | N/A | Flexible |
| Best for | Analytics, DW | Hive, analytics | Streaming, Kafka | Interchange | APIs |
| Splittable | Yes | Yes | Yes | Yes (uncompressed) | No |

### Writing Parquet in PySpark

```python
df.write \
    .mode("overwrite") \
    .option("compression", "zstd") \
    .partitionBy("dt") \
    .parquet("s3://bucket/data/events/")
```

### Writing Parquet in Python (PyArrow)

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.Table.from_pandas(df)
pq.write_table(table, 'output.parquet', compression='zstd')

# Read with column selection (column pruning)
table = pq.read_table('output.parquet', columns=['user_id', 'revenue'])
```

### Avro with schema evolution

```json
{
    "type": "record",
    "name": "Event",
    "fields": [
        {"name": "event_id", "type": "string"},
        {"name": "user_id", "type": "long"},
        {"name": "event_type", "type": "string"},
        {"name": "metadata", "type": ["null", "string"], "default": null}
    ]
}
```

## Gotchas

- CSV parsing is deceptively complex: quoting, escaping, encoding (UTF-8 vs Latin-1), newlines in fields, varying delimiters. Always specify dialect explicitly
- Parquet files should be 128 MB - 1 GB each for optimal performance. Too many small files cause metadata overhead; too large files reduce parallelism
- `inferSchema=True` in Spark for CSV/JSON reads the file twice and may guess wrong types. Always provide explicit schema for production
- JSON Lines (JSONL, one JSON object per line) is splittable and parallelizable; standard JSON (single array) is not. Prefer JSONL for big data
- Parquet does NOT support appending rows to existing files. "Append mode" in Spark creates new Parquet files in the same directory
- Avro schema evolution requires careful management: removing a required field without a default breaks backward compatibility

## See Also

- [[data-lake]] - format selection for lake storage
- [[apache-spark]] - native Parquet support
- [[clickhouse]] - columnar storage engine
- https://parquet.apache.org/docs/ - Apache Parquet documentation
- https://avro.apache.org/docs/ - Apache Avro documentation
