---
title: Spark Streaming
category: tools
tags: [data-engineering, spark, streaming, structured-streaming, micro-batch]
---

# Spark Streaming

Spark Streaming processes real-time data via micro-batching - incoming stream is split into small batch jobs processed by Spark Core. Structured Streaming (recommended) treats the stream as an unbounded DataFrame.

## Two Approaches

| | Classic DStreams | Structured Streaming |
|---|---|---|
| Abstraction | Stream as micro-batch RDDs | Stream as infinite DataFrame |
| Side effects | Allowed | Input -> transform -> output only |
| API | Lower-level | Same DataFrame API as batch |
| Status | Legacy | **Recommended** |

## Structured Streaming Pattern

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("streaming").getOrCreate()

# Source (Kafka)
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:9092") \
    .option("subscribe", "topic_name") \
    .load()

# Process
result = df.selectExpr("CAST(value AS STRING)")

# Sink
query = result.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
```

## DStreams API (Legacy)

```python
from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, batchDuration=1)  # 1-second ticks
# Define source, transformations
ssc.start()
ssc.awaitTermination()
```

## Delivery Guarantees

| Guarantee | Meaning | Trade-off |
|-----------|---------|-----------|
| **At-most-once** | Messages may be lost, never duplicated | Fastest |
| **At-least-once** | Messages never lost, may be duplicated | Requires deduplication |
| **Exactly-once** | Messages delivered exactly once | Most complex, transactional support needed |

## Typical Pipeline

```php
Kafka -> Spark Structured Streaming -> Database/DWH
```

## Key Facts
- Structured Streaming does not allow terminal actions (count, collect) mid-pipeline
- Window functions apply over time-based windows
- Can combine streaming data with static (cached) data via joins
- Triggers: time-based, event-count, or continuous

## Gotchas
- Spark Streaming is NOT true streaming - it is micro-batching
- Development/debugging is harder than batch - use Jupyter for prototyping
- Structured Streaming output modes: `append`, `complete`, `update`
- State management adds complexity for aggregations over time windows

## See Also
- [[apache-kafka]] - message broker
- [[apache-spark-core]] - Spark architecture
- [[etl-elt-pipelines]] - batch vs stream processing
