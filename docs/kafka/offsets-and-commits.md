---
title: Offsets and Commits
category: concepts
tags: [kafka, offset, commit, auto-commit, consumer-lag, __consumer_offsets]
---

# Offsets and Commits

An offset is a sequential message number within a partition, assigned on write; consumers track their position via offsets stored either in Kafka's internal `__consumer_offsets` topic or in an external database.

## Key Facts

- Offset is just 8 bytes per partition per consumer - a pointer indicating where to read next
- The pair `(partition_number, offset)` uniquely addresses any message in a topic
- `__consumer_offsets` is an internal topic storing: consumer group + topic + partition + **next offset to read** (last read + 1)
- `__consumer_offsets` uses `acks=all` by default with 50 partitions
- Two levels of tracking: **broker-side** (always on, tracks what was sent) and **consumer commit** (confirms processing)
- Auto-commit (`enable.auto.commit=true`, default) commits every `auto.commit.interval.ms` (default 5000ms) regardless of processing success
- Manual commit: `commitSync()` (blocking) or `commitAsync()` (non-blocking with callback)
- Best practice: `commitAsync()` during processing, `commitSync()` in finally block
- External offset storage: store offsets in application DB alongside business data for exactly-once with external systems (Spark uses checkpoint files, does NOT commit to `__consumer_offsets`)

## Patterns

### Auto-Commit (Dangerous Default)

```properties
# Default configuration - auto-commit enabled
enable.auto.commit=true
auto.commit.interval.ms=5000
```

**Problem flow**: consumer receives -> auto-commit fires -> consumer crashes mid-processing -> messages lost forever.

### Manual Commit (Recommended)

```java
// Java - manual commit patterns
consumer.subscribe(List.of("orders"));
props.put("enable.auto.commit", "false");

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        // Synchronous commit - blocks, safest
        consumer.commitSync();
    }
} catch (Exception e) {
    log.error("Processing failed", e);
} finally {
    consumer.commitSync();  // Final sync commit
    consumer.close();
}
```

```python
# Python - manual commit
conf = {"enable.auto.commit": False}
consumer = Consumer(conf)

msg = consumer.poll(0.1)
if msg and not msg.error():
    process(msg)
    consumer.commit(msg)
```

### Seeking to Specific Offset

```java
// Read from specific offset
consumer.seek(new TopicPartition("topic", 0), 42L);

// Assign specific partitions (no consumer group coordination)
consumer.assign(List.of(new TopicPartition("topic", 0)));
```

### Offset Reset Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `auto.offset.reset=latest` | Read only new messages | Real-time stream processing |
| `auto.offset.reset=earliest` | Read from oldest available | Debugging, data migration, full history |
| `auto.offset.reset=none` | Throw exception | Fail explicitly when offset is missing |

### Resetting Offsets via CLI

```bash
# Reset to earliest
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-earliest --execute

# Reset to specific offset
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic:0 \
  --reset-offsets --to-offset 100 --execute

# Reset to timestamp
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-datetime 2024-01-01T00:00:00.000 --execute
```

### Consumer Lag Monitoring

```bash
# Check consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe
```

Consumer lag = latest offset in partition - consumer's committed offset. Growing lag means consumers cannot keep up. Solutions: add partitions + consumers, optimize processing, increase `fetch.min.bytes` and `fetch.max.wait.ms`.

## Gotchas

- **Auto-commit is the #1 beginner mistake** - it commits before processing completes; disable it for any production workload where data loss matters
- **`auto.commit.interval.ms` must be less than `session.timeout.ms`** - otherwise Kafka considers consumer dead and triggers rebalancing before commit
- **Offset expiration** - if consumer inactive longer than `offsets.retention.minutes` (broker setting, default 7 days), Kafka deletes stored offsets; on reconnect, `auto.offset.reset` kicks in
- **Database restore gap** - after restoring DB from backup, consumer offset in Kafka points to current position; data from the gap exists in Kafka but consumer already committed past it; solutions: reset offset via CLI, use new consumer group, or store offsets in application DB
- **`__consumer_offsets` corruption** - can occur with frequent broker restarts during active reading; try manually reassigning problematic topic partitions before recreating the consumer group

## See Also

- [[consumer-groups]] - group mechanics and partition assignment
- [[delivery-semantics]] - how offset management maps to delivery guarantees
- [[kafka-transactions]] - atomic offset commit with message production
- [Apache Kafka Consumer Offset Management](https://kafka.apache.org/documentation/#consumerconfigs)
