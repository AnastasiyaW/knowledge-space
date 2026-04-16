---
title: Idempotent Producer
category: concepts
tags: [kafka, producer, idempotent, deduplication, ordering, exactly-once]
---

# Idempotent Producer

The idempotent producer assigns a PID (Producer ID) and sequence numbers to each message, allowing the broker to deduplicate retries within a producer session with negligible overhead.

## Key Facts

- Each producer gets a **PID** (Producer ID) assigned by the broker on initialization
- Each message gets a monotonic **sequence number** within its epoch per partition
- Broker detects and rejects duplicate `(PID, sequence_number)` pairs
- Overhead is minimal - just a few extra bytes per message (negligible performance impact)
- **Auto-enabled since Kafka 3.0.0** when all of: `max.in.flight.requests.per.connection` <= 5, `retries` > 0, `acks=all`
- If `enable.idempotence=true` is set explicitly but conditions are not met, `KafkaProducer` constructor throws an exception
- Scope: per-partition, per-producer-session; the broker tracks the last 5 sequence numbers per PID per partition
- **Bonus**: with idempotency enabled, Kafka guarantees correct ordering even when messages arrive out of order due to retries
- Without idempotency and `max.in.flight > 1`, a retry of batch N can arrive after batch N+1 succeeds, causing out-of-order writes

## Patterns

### Configuration

```java
// Java - explicit idempotent setup
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
// These are automatically enforced when idempotence is enabled:
//   acks = all
//   retries = Integer.MAX_VALUE
//   max.in.flight.requests.per.connection <= 5
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
```

```python
# Python - idempotent producer
from confluent_kafka import Producer

p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092",
    "enable.idempotence": True,
    # acks automatically set to "all"
    # max.in.flight.requests.per.connection automatically capped at 5
})
```

### Ordering Guarantee Mechanism

```bash
Without idempotency (max.in.flight=2):
  Batch 1 sent -> fails -> retry queued
  Batch 2 sent -> succeeds -> written at offset N
  Batch 1 retry -> succeeds -> written at offset N+1
  Result: messages OUT OF ORDER

With idempotency (max.in.flight<=5):
  Batch 1 sent -> fails -> retry queued
  Batch 2 sent -> broker rejects (out-of-sequence for this PID)
  Batch 1 retry -> succeeds
  Batch 2 retry -> succeeds
  Result: messages IN ORDER
```

## Gotchas

- **Does NOT protect against application-level retries** - if your code catches an error and calls `produce()` again, the message gets a new sequence number; the broker sees it as a new message, not a duplicate
- **Session boundary** - if the producer restarts, it gets a new PID; old in-flight retries cannot be deduplicated against the new PID; for cross-session exactly-once, use [[kafka-transactions]] with `transactional.id`
- **Cannot override sequence number generation** - there is no API to manually set sequence numbers
- **`max.in.flight.requests.per.connection > 5` with idempotence** throws ConfigException - the broker can only track up to 5 in-flight batches per PID per partition

## See Also

- [[kafka-transactions]] - extends idempotent producer with cross-partition atomic writes
- [[delivery-semantics]] - how idempotent producer fits into exactly-once guarantees
- [[kafka-producer-fundamentals]] - full producer pipeline, batching, compression, error handling
- [KIP-98: Exactly Once Delivery](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
