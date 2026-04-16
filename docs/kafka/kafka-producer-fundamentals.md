# Kafka Producer Fundamentals

Producer send pipeline, acks modes, batching mechanics, compression selection, retry configuration, error handling, and send patterns (fire-and-forget, sync, async).

## Producer Send Pipeline

Every `send()` call traverses this pipeline before bytes hit the wire:

```text
send(record)
  |
  v
[Interceptors] -- onSend() modifies/inspects the record
  |
  v
[Key Serializer] -- key -> bytes
  |
  v
[Value Serializer] -- value -> bytes
  |
  v
[Partitioner] -- select target partition (explicit > key hash > sticky)
  |
  v
[RecordAccumulator] -- append to partition-specific batch (in buffer.memory)
  |                     batch sealed when: batch.size reached OR linger.ms expires
  v
[Compression] -- compress sealed batch (lz4/snappy/zstd/gzip/none)
  |
  v
[Sender Thread] -- drain batches, group by broker, send ProduceRequest
  |                 max.in.flight.requests.per.connection concurrent requests
  v
[Broker] -- write to leader log, replicate per acks setting
  |
  v
[Callback / Future] -- success or retriable/fatal error
```

Key insight: serialization happens **before** partitioning. The partitioner sees the serialized key bytes (relevant for custom partitioners). Compression happens at the **batch** level, not per-message.

## Acks Modes

### acks=0: Fire-and-Forget

Producer does not wait for any broker acknowledgment. The `send()` returns immediately after the message is placed in the network buffer.

**When to use:** Metrics collection, click tracking, debug logging - anywhere losing a small percentage of messages is acceptable and throughput is paramount.

```java
// Java - fire-and-forget, acks=0
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092");
props.put(ProducerConfig.ACKS_CONFIG, "0");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// send() returns a Future but with acks=0 it completes immediately
// the Future's metadata will have offset=-1 (unknown)
producer.send(new ProducerRecord<>("metrics", "cpu", "92.5"));
```

```python
# Python - fire-and-forget, acks=0
from confluent_kafka import Producer

p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092",
    "acks": 0,
    "queue.buffering.max.messages": 1000000,
})

for metric in metrics_stream:
    p.produce("metrics", key=metric.name, value=str(metric.value))
    p.poll(0)  # trigger callbacks / internal housekeeping without blocking

p.flush()  # drain on shutdown
```

### acks=1: Leader Only

Leader writes to its local log and responds. Replicas pull asynchronously.

**When to use:** Low-latency pipelines where occasional message loss on leader failure is tolerable. Common in log aggregation.

**Risk window:** Between leader write and follower fetch. If the leader dies in this window, the new leader (elected from ISR) will not have the message.

### acks=all (-1): Full ISR Acknowledgment

Leader waits for all in-sync replicas (ISR) to acknowledge before responding to the producer.

**Critical pairing with `min.insync.replicas`:**

| `replication.factor` | `min.insync.replicas` | Behavior |
|-|-|-|
| 3 | 1 | `acks=all` degrades to `acks=1` if 2 replicas fall out of ISR |
| 3 | 2 | Tolerates 1 broker failure; producer gets `NotEnoughReplicasException` if ISR < 2 |
| 3 | 3 | Zero tolerance for failure; any single broker down = writes blocked |

**Production standard:** RF=3, `min.insync.replicas=2`, `acks=all`.

```java
// Java - durable producer
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092,broker3:9092");
props.put(ProducerConfig.ACKS_CONFIG, "all");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
```

```python
# Python - durable producer
p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092,broker3:9092",
    "acks": "all",
    "enable.idempotence": True,
    "max.in.flight.requests.per.connection": 5,
    "retries": 2147483647,
    "delivery.timeout.ms": 120000,
})
```

## Batching Patterns

### Batch Mechanics

The `RecordAccumulator` maintains a `Deque<ProducerBatch>` per `TopicPartition`. Each batch is a `MemoryRecords` buffer allocated from `buffer.memory`.

```text
buffer.memory (total pool)
  |
  +-- TopicPartition(orders, 0) -> [batch 16KB] [batch 16KB]
  +-- TopicPartition(orders, 1) -> [batch 16KB]
  +-- TopicPartition(events, 0) -> [batch 16KB] [batch 16KB] [batch 16KB]
```

A batch is sent when **either** condition is met:
1. `batch.size` bytes accumulated in the batch
2. `linger.ms` elapsed since the first record was added to the batch

### Throughput-Optimized Batching

```java
// Java - high throughput
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 65536);     // 64KB batches
props.put(ProducerConfig.LINGER_MS_CONFIG, 20);          // wait up to 20ms
props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4"); // compress batch
props.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 67108864); // 64MB buffer
```

```python
# Python - high throughput
p = Producer({
    "bootstrap.servers": "broker1:9092",
    "batch.size": 65536,
    "linger.ms": 20,
    "compression.type": "lz4",
    "queue.buffering.max.kbytes": 65536,
})
```

### Latency-Optimized (Minimal Batching)

```java
// Java - low latency
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);  // default 16KB
props.put(ProducerConfig.LINGER_MS_CONFIG, 0);        // send immediately
props.put(ProducerConfig.ACKS_CONFIG, "1");            // leader only
```

### Adaptive Batching Pattern

Monitor batch fill ratio to tune `linger.ms` dynamically:

```java
// Java - monitor batch efficiency via metrics
Metric batchSizeAvg = producer.metrics().get(
    new MetricName("batch-size-avg", "producer-metrics", "", Collections.emptyMap())
);
Metric recordsPerBatch = producer.metrics().get(
    new MetricName("records-per-request-avg", "producer-metrics", "", Collections.emptyMap())
);
// If batch-size-avg << batch.size, increase linger.ms
// If records-per-request-avg == 1, batching is not happening
```

## Compression Patterns

Compression is applied at the **batch** level. The broker stores batches compressed; consumers decompress on read.

### Codec Comparison

| Codec | Compression Ratio | CPU (compress) | CPU (decompress) | Best For |
|-|-|-|-|-|
| `lz4` | Low-medium | Very low | Very low | General purpose, default choice |
| `snappy` | Low-medium | Low | Very low | Similar to lz4, legacy preference |
| `zstd` | High | Medium | Low | Large messages, storage-constrained, high-volume |
| `gzip` | Medium-high | High | Medium | Compatibility with non-Kafka consumers |

### Selection Decision Tree

```text
Is CPU a constraint?
  YES -> lz4 or snappy
  NO  -> Is storage/bandwidth a constraint?
           YES -> zstd (best ratio)
           NO  -> Is interop with non-Kafka systems needed?
                    YES -> gzip
                    NO  -> lz4 (balanced default)
```

### Broker-Side vs Producer-Side Compression

If the broker's `compression.type` for a topic differs from the producer's, the broker **recompresses** every batch - massive CPU waste.

```bash
# Match producer and broker compression to avoid recompression
# broker topic config:
kafka-configs.sh --alter --topic orders \
  --add-config compression.type=lz4

# producer config must also use lz4
```

If the broker topic has `compression.type=producer` (default), the broker stores whatever the producer sends without recompression.

## Retry and Error Handling

### Retry Configuration

```java
Properties props = new Properties();
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);     // unlimited retries
props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);    // 2 min overall deadline
props.put(ProducerConfig.RETRY_BACKOFF_MS_CONFIG, 100);          // 100ms between retries
props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);      // 30s per attempt
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);       // deduplicate retries
props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
```

**Constraint:** `delivery.timeout.ms >= linger.ms + request.timeout.ms`. Violating this produces `TimeoutException` before the first retry can complete.

### Retriable vs Fatal Errors

| Error Type | Examples | Producer Behavior |
|-|-|-|
| Retriable | `LEADER_NOT_AVAILABLE`, `NOT_ENOUGH_REPLICAS`, `REQUEST_TIMED_OUT`, `NETWORK_EXCEPTION` | Auto-retried until `delivery.timeout.ms` |
| Fatal | `MESSAGE_TOO_LARGE`, `INVALID_TOPIC_EXCEPTION`, `TOPIC_AUTHORIZATION_FAILED`, `SERIALIZATION_ERROR` | Returned immediately via callback, no retry |

### Error Handling with Callbacks

```java
// Java - robust callback with error classification
producer.send(new ProducerRecord<>("orders", orderId, orderJson), (metadata, exception) -> {
    if (exception == null) {
        log.info("Delivered to {}[{}]@{}", metadata.topic(), metadata.partition(), metadata.offset());
        return;
    }
    if (exception instanceof RetriableException) {
        log.error("Retriable error exhausted for order {}: {}", orderId, exception.getMessage());
        deadLetterQueue.send(orderId, orderJson, exception);
    } else {
        log.error("Fatal producer error for order {}: {}", orderId, exception.getMessage());
        alerting.critical("Producer fatal error", exception);
    }
});
```

```python
# Python - error classification in callback
from confluent_kafka import KafkaException, KafkaError

def delivery_callback(err, msg):
    if err is None:
        print(f"OK: {msg.topic()}[{msg.partition()}]@{msg.offset()}")
        return
    if err.retriable():
        print(f"Retriable error exhausted: {err}")
        send_to_dlq(msg.key(), msg.value(), str(err))
    elif err.code() == KafkaError.MSG_SIZE_TOO_LARGE:
        print(f"Message too large: {len(msg.value())} bytes")
    else:
        print(f"Fatal error: {err}")

p.produce("orders", key="order-123", value=payload, callback=delivery_callback)
```

## Send Patterns

### Fire-and-Forget

```java
// Java
producer.send(new ProducerRecord<>("logs", logLine));
```

```python
# Python
p.produce("logs", value=log_line)
p.poll(0)
```

### Synchronous Send

```java
// Java - synchronous
try {
    RecordMetadata meta = producer.send(
        new ProducerRecord<>("orders", orderId, orderJson)
    ).get();  // blocks here
    log.info("Written at offset {}", meta.offset());
} catch (ExecutionException e) {
    if (e.getCause() instanceof RetriableException) { /* handle */ }
}
```

```python
# Python - synchronous (confluent-kafka has no Future, use flush per message)
p.produce("orders", key=order_id, value=order_json, callback=delivery_callback)
p.flush()  # blocks until delivered
```

### Async with Callback (Recommended)

```java
// Java - async with callback
producer.send(
    new ProducerRecord<>("orders", orderId, orderJson),
    (metadata, exception) -> {
        if (exception != null) { handleError(orderId, exception); }
        else { confirmDelivery(metadata); }
    }
);
```

```python
# Python - async with callback
def on_delivery(err, msg):
    if err: handle_error(msg.key(), err)
    else: confirm_delivery(msg)

for record in records:
    p.produce("orders", key=record.key, value=record.value, callback=on_delivery)
    p.poll(0)

p.flush()
```

## Gotchas

- **`max.in.flight.requests.per.connection > 1` without idempotency** risks out-of-order delivery on retries. If ordering matters and you cannot enable idempotency, set `max.in.flight=1` (but throughput drops significantly).
- **Broker-side `message.max.bytes` default is 1MB.** Messages larger than this are rejected with `MSG_SIZE_TOO_LARGE`. Increase both broker (`message.max.bytes`) and topic (`max.message.bytes`) configs if needed.
- **`flush()` in Python does not throw on delivery failure.** It returns the number of messages still in the queue. Check errors in the delivery callback, not the `flush()` return value.
- **`delivery.timeout.ms` must be >= `linger.ms + request.timeout.ms`.** Otherwise the timeout fires before the first retry attempt completes.

## See Also

- [[kafka-producer-advanced-patterns]] - custom partitioners, headers, interceptors, backpressure, idempotent producer, Schema Registry
- [[topics-and-partitions]] - partition mechanics, key-based routing, segment structure
- [[kafka-transactions]] - transactional producer API, exactly-once read-process-write
- [[kafka-replication-fundamentals]] - ISR, acks interaction with replication
- [[broker-architecture]] - how brokers handle ProduceRequests
