---
title: Kafka Streams Time Semantics
category: concepts
tags: [kafka, streams, event-time, processing-time, watermark, dataflow-model, late-data]
---

# Kafka Streams Time Semantics

Stream processing time semantics based on the Google Dataflow model define how events are grouped by time, with watermarks estimating progress and triggering/accumulation modes controlling when and how results are emitted.

## Key Facts

- **Event time**: when the event actually occurred in the real world
- **Processing time**: when the event is observed/processed by the system
- These can differ significantly due to network delays, buffering, and distributed system behavior
- **Watermark**: system's estimate of how far it has progressed in event time; "at processing time X, I believe I have seen all events up to event time Y"
- Watermarks are heuristic - they may be wrong; some data may arrive "late"
- In Kafka Streams, watermarks are tracked per partition based on observed timestamps
- **Stream time** in Kafka Streams: maximum timestamp seen so far across all processed records
- Timestamp assignment controlled by `message.timestamp.type` on the topic: `CreateTime` (default, producer-set) or `LogAppendTime` (broker-set)

## Patterns

### Triggering Strategies (Dataflow Model)

| Trigger | When Results Emitted |
|---------|---------------------|
| At watermark | When watermark passes end of window |
| Periodically | Every N seconds of processing time |
| Per element | On each new element (early results) |
| Composite | Combine multiple strategies |

### Accumulation Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| Discarding | Each trigger emits only new data since last trigger | Independent per-trigger results |
| Accumulating | Each trigger emits cumulative result | Running totals, overwrite downstream |
| Accumulating & Retracting | Emits retraction of previous + new cumulative | Multi-stage pipelines with downstream grouping |

**Retractions** are necessary when downstream operations group by different keys than the windowed operation. Without retractions, downstream aggregations double-count.

### ksqlDB Time Override

```sql
-- Use any field as timestamp
CREATE STREAM events (
    event_id VARCHAR,
    event_time BIGINT,
    data VARCHAR
) WITH (
    KAFKA_TOPIC = 'events',
    VALUE_FORMAT = 'JSON',
    TIMESTAMP = 'event_time'
);

-- With custom timestamp format
WITH (TIMESTAMP = 'event_time', TIMESTAMP_FORMAT = 'yyyy-MM-dd HH:mm:ss')
```

### Bounded vs Unbounded Data

The Dataflow model treats batch as a special case of streaming:
- **Bounded** (batch): finite dataset, known size, can reprocess
- **Unbounded** (stream): infinite, continuously arriving, must process incrementally
- Same operations (windowing, triggering, accumulation) apply to both

## Gotchas

- **Event time and processing time can diverge significantly** - a message produced at 14:00 might be processed at 14:30 due to consumer lag; using processing time for aggregation produces incorrect results
- **Advancing system time during testing causes data retention issues** - messages with future timestamps mix with current ones; no segment can be deleted until the newest message expires; this fills disk and is the most common way to crash Kafka
- **`LogAppendTime` loses producer-side event time** - broker overwrites timestamp, making event-time processing impossible

## See Also

- [[kafka-streams-windowing]] - window types and grace periods
- [[kafka-streams]] - topology, operations, aggregations
- [Google Dataflow Model Paper](https://research.google/pubs/pub43864/)
- [Kafka Streams Time Documentation](https://kafka.apache.org/documentation/streams/concepts.html#streams_time)
