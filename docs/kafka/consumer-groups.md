---
title: Consumer Groups
category: concepts
tags: [kafka, consumer, group, rebalancing, heartbeat, partition-assignment, static-membership]
---

# Consumer Groups

A consumer group is a named entity that enables multiple consumers to cooperatively read from topic partitions, with each partition assigned to exactly one consumer in the group, providing both parallelism and fault tolerance.

## Key Facts

- Consumers join a group via `group.id` parameter - must be unique per logical consumer group
- Within a group, **one partition can only be read by one consumer** (but one consumer can read multiple partitions)
- If consumers > partitions, extra consumers sit idle (no work to do)
- Multiple consumer groups CAN read the same partition independently (each group tracks its own [[offsets-and-commits]])
- This is a killer feature: reading a topic 10 times requires 10 consumer groups (10 x 8 bytes per partition), not 10 copies of data
- One consumer can subscribe to multiple topics via `consumer.subscribe(List<String>)`
- No hard cap on consumer groups (theoretically ~2 billion); `__consumer_offsets` topic (default 50 partitions) starts slowing at thousands of groups
- First consumer to connect becomes **group leader** - performs partition redistribution on rebalance
- Consumer group timeout: if consumer is inactive too long, Kafka may delete its offsets (`offsets.retention.minutes`, default 7 days)
- Kafka is **pull-based**: consumers poll Kafka; Kafka does not push (different from RabbitMQ)

## Patterns

### Basic Consumer (Java)

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false");
props.put("auto.offset.reset", "earliest");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("topic1", "topic2"));

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        consumer.commitSync();
    }
} finally {
    consumer.close();  // ALWAYS close consumer
}
```

### Basic Consumer (Python)

```python
from confluent_kafka import Consumer

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
consumer = Consumer(conf)
consumer.subscribe(["topic1", "topic2"])

try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        process_message(msg)
        consumer.commit(msg)
finally:
    consumer.close()
```

### Partition Assignment Strategies

| Strategy | Use Case | Behavior |
|----------|----------|----------|
| **RangeAssignor** (default) | Co-partitioned topics | Assigns contiguous partitions per topic; can be unbalanced |
| **RoundRobinAssignor** | Fair distribution | Distributes all partitions evenly, alternating |
| **StickyAssignor** | Stateful consumers | Preserves existing assignments during rebalance |
| **CooperativeStickyAssignor** | Modern default (recommended) | Incremental rebalance, no stop-the-world |

```java
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

**Co-partitioned topics**: two topics with same partition count, same partitioning strategy, same keys. With RangeAssignor, data with same key from both topics goes to same consumer - enables joins without cross-process communication.

### Consumer Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `bootstrap.servers` | required | Broker addresses (comma-separated) |
| `group.id` | required | Consumer group identifier |
| `key.deserializer` | required | Deserialization class for keys |
| `value.deserializer` | required | Deserialization class for values |
| `enable.auto.commit` | `true` | Auto-commit offsets (disable in production) |
| `auto.commit.interval.ms` | `5000` | Auto-commit frequency |
| `auto.offset.reset` | `latest` | What to do with no stored offset |
| `max.partition.fetch.bytes` | `1048576` (1MB) | Max data per partition per poll |
| `max.poll.records` | `500` | Max messages per poll across all partitions |
| `fetch.min.bytes` | `1` | Min data before returning from poll |
| `fetch.max.wait.ms` | `500` | Max wait if min.bytes not met |
| `heartbeat.interval.ms` | `3000` | Heartbeat frequency |
| `session.timeout.ms` | `10000` | Session timeout before consumer considered dead |
| `max.poll.interval.ms` | `300000` | Max time between polls |

### Static Group Membership

```java
props.put("group.instance.id", "consumer-instance-1");
// No rebalance on temporary disconnect
// Risk: partition unread until restart
```

## Gotchas

- **Rebalancing storm** - consumers repeatedly stop and restart reading; causes: processing takes longer than `session.timeout.ms`, slow startup, frequent deploys; fix: increase timeouts, use CooperativeStickyAssignor
- **All consumers must use same assignment strategy** - mismatches cause global rebalancing
- **Paused consumers do NOT trigger rebalance** - `.pause()` keeps heartbeats alive
- **Consumer subscription is immutable per subscribe call** - calling `subscribe()` again replaces previous subscription
- **Extra consumers sit idle** - consumers > partitions means wasted resources; plan partition count ahead (rule of thumb: 4 partitions per consumer)

## See Also

- [[offsets-and-commits]] - offset tracking, auto-commit dangers, manual commit patterns
- [[rebalancing-deep-dive]] - heartbeat tuning, cooperative rebalancing, static membership
- [[topics-and-partitions]] - partition count sizing and key-based routing
- [[consumer-configuration]] - full consumer config reference
- [Apache Kafka Consumer Configuration](https://kafka.apache.org/documentation/#consumerconfigs)
