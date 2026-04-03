---
title: Delivery Semantics
category: concepts
tags: [kafka, delivery, exactly-once, at-least-once, at-most-once, idempotent]
---

# Delivery Semantics

Kafka supports three delivery semantics - at-most-once, at-least-once, and exactly-once - each with specific configuration requirements and trade-offs at both producer and consumer sides.

## Key Facts

- **At-most-once**: messages may be lost but never duplicated; `acks=0` or auto-commit before processing; use for metrics, logs, analytics where loss is acceptable
- **At-least-once**: messages may be duplicated but never lost; `acks=all` + `retries>0` + manual commit after processing; most common production setup
- **Exactly-once**: each message processed exactly once despite failures; requires idempotent producer + transactions OR application-level deduplication
- "Exactly once" is technically impossible (Two Generals' Problem); practical exactly-once = at-least-once + idempotence at every boundary
- Duplicates can occur on both **producer side** (lost ACK causes retry) and **consumer side** (crash after processing but before offset commit)
- Kafka's exactly-once works ONLY for the pattern: Read from Kafka -> Process -> Write to Kafka (via [[kafka-transactions]])
- Cross-system exactly-once (Kafka -> external DB) requires application-level deduplication
- Stricter semantics = more overhead = lower throughput

## Patterns

### At-Most-Once Configuration

```properties
# Producer
acks=0

# Consumer
enable.auto.commit=true
auto.commit.interval.ms=5000
```

### At-Least-Once Configuration

```properties
# Producer
acks=all
retries=2147483647
enable.idempotence=true

# Consumer
enable.auto.commit=false
# Commit manually after successful processing
```

```java
// Java - at-least-once consumer
try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);  // Process first
        }
        consumer.commitSync();  // Then commit
    }
} finally {
    consumer.close();
}
```

```python
# Python - at-least-once consumer
from confluent_kafka import Consumer

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "enable.auto.commit": False,
}
consumer = Consumer(conf)
consumer.subscribe(["my-topic"])

try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None or msg.error():
            continue
        process_message(msg)
        consumer.commit(msg)  # Commit after processing
finally:
    consumer.close()
```

### Exactly-Once (Kafka-to-Kafka)

```java
// Producer config
props.put("transactional.id", "my-transactional-id");
props.put("enable.idempotence", "true");

producer.initTransactions();
producer.beginTransaction();
try {
    producer.send(new ProducerRecord<>("output", key, value));
    producer.sendOffsetsToTransaction(offsets, consumerGroupMetadata);
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}

// Consumer config
props.put("isolation.level", "read_committed");
props.put("enable.auto.commit", "false");
```

### Where Duplicates Occur

```
Producer Side:
  Producer sends -> Broker receives + stores -> ACK lost on network
  -> Producer retries -> DUPLICATE in broker

Consumer Side:
  Consumer receives batch -> Processes messages -> Crashes before commit
  -> Restart -> Re-reads same batch -> DUPLICATE processing
```

## Gotchas

- **Auto-commit is the #1 source of bugs for Kafka beginners** - consumer receives messages, auto-commit fires, consumer crashes during processing; on restart Kafka considers messages processed and delivers the next batch; lost messages are gone forever
- **Idempotent producer only prevents library-level retry duplicates** - if your application code catches an error and calls `produce()` again, the message gets a new sequence number and the broker sees it as a new message
- **`isolation.level` defaults to `read_uncommitted`** - transactions have no effect unless consumer explicitly sets `isolation.level=read_committed`
- **Exactly-once does NOT cover external systems** - database writes, HTTP calls, or cross-cluster operations are outside the scope of Kafka's transactional guarantees

## See Also

- [[kafka-transactions]] - transactional producer API for exactly-once within Kafka
- [[idempotent-producer]] - PID + sequence number deduplication mechanism
- [[consumer-groups]] - offset management and commit strategies
- [[transactional-outbox]] - pattern for exactly-once with external databases
- [KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
