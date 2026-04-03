---
title: Producer Patterns
category: patterns
tags: [kafka, producer, acks, batching, compression, partitioner, callback, retry]
---

# Producer Patterns

Advanced producer patterns beyond basic send/receive. Covers the full send pipeline, compression selection, custom partitioning, callback architectures, backpressure handling, header propagation, interceptors, and idempotent/transactional configurations with production-ready code in Java and Python (confluent-kafka).

For foundational producer concepts (record structure, acks overview, basic send modes), see [[producer-patterns]].

## Producer Send Pipeline

Every `send()` call traverses this pipeline before bytes hit the wire:

```
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

## Acks Modes - Deep Dive

### acks=0: Fire-and-Forget

Producer does not wait for any broker acknowledgment. The `send()` returns immediately after the message is placed in the network buffer.

**When to use:** Metrics collection, click tracking, debug logging - anywhere losing a small percentage of messages is acceptable and throughput is paramount.

**Risk profile:**
- Message lost if leader is down at the moment of send
- Message lost if network drops the packet
- No retries possible (producer never learns about failure)
- Ordering within partition is preserved (single in-flight)

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
// no .get(), no callback - truly fire-and-forget
```

```python
# Python - fire-and-forget, acks=0
from confluent_kafka import Producer

p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092",
    "acks": 0,
    "queue.buffering.max.messages": 1000000,  # large internal queue
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

```
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
    "batch.size": 65536,        # 64KB
    "linger.ms": 20,
    "compression.type": "lz4",
    "queue.buffering.max.kbytes": 65536,  # confluent-kafka buffer limit
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

```
Is CPU a constraint?
  YES -> lz4 or snappy
  NO  -> Is storage/bandwidth a constraint?
           YES -> zstd (best ratio)
           NO  -> Is interop with non-Kafka systems needed?
                    YES -> gzip
                    NO  -> lz4 (balanced default)
```

### zstd with Custom Compression Level

```java
// Java - zstd with tunable level (only via broker/producer config in librdkafka)
props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "zstd");
// Java client does not expose zstd level directly;
// librdkafka (Python, Go, C) supports compression.codec and compression.level
```

```python
# Python - zstd with compression level
p = Producer({
    "bootstrap.servers": "broker1:9092",
    "compression.type": "zstd",
    "compression.level": 3,  # 1 (fastest) to 19 (best ratio), default 3
})
```

### Broker-Side vs Producer-Side Compression

If the broker's `compression.type` for a topic differs from the producer's, the broker **recompresses** every batch - massive CPU waste.

```
# Match producer and broker compression to avoid recompression
# broker topic config:
kafka-configs.sh --alter --topic orders \
  --add-config compression.type=lz4

# producer config must also use lz4
```

If the broker topic has `compression.type=producer` (default), the broker stores whatever the producer sends without recompression.

## Retry and Error Handling Patterns

### Retry Configuration

```java
Properties props = new Properties();
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);     // unlimited retries
props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);    // 2 min overall deadline
props.put(ProducerConfig.RETRY_BACKOFF_MS_CONFIG, 100);          // 100ms between retries
props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);      // 30s per attempt
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);       // deduplicate retries
props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5); // up to 5 in-flight
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
        // Already exhausted retries within delivery.timeout.ms
        log.error("Retriable error exhausted for order {}: {}", orderId, exception.getMessage());
        deadLetterQueue.send(orderId, orderJson, exception);
    } else {
        // Fatal - bad data, auth failure, etc.
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
        # Retries exhausted within delivery.timeout.ms
        print(f"Retriable error exhausted: {err}")
        send_to_dlq(msg.key(), msg.value(), str(err))
    elif err.code() == KafkaError.MSG_SIZE_TOO_LARGE:
        print(f"Message too large: {len(msg.value())} bytes")
    else:
        print(f"Fatal error: {err}")

p.produce("orders", key="order-123", value=payload, callback=delivery_callback)
```

## Send Patterns: Fire-and-Forget vs Sync vs Async

### Fire-and-Forget

No delivery confirmation. Highest throughput, accepts message loss.

```java
// Java
producer.send(new ProducerRecord<>("logs", logLine));
// return value ignored
```

```python
# Python
p.produce("logs", value=log_line)
p.poll(0)  # non-blocking poll to serve internal callbacks
```

### Synchronous Send

Blocks until broker confirms. Lowest throughput, strongest guarantee per message.

```java
// Java - synchronous
try {
    RecordMetadata meta = producer.send(
        new ProducerRecord<>("orders", orderId, orderJson)
    ).get();  // blocks here
    log.info("Written at offset {}", meta.offset());
} catch (ExecutionException e) {
    if (e.getCause() instanceof RetriableException) {
        // handle
    }
}
```

```python
# Python - synchronous (confluent-kafka has no Future, use flush per message)
p.produce("orders", key=order_id, value=order_json, callback=delivery_callback)
p.flush()  # blocks until this message (and any buffered) is delivered
```

### Async with Callback (Recommended for Most Use Cases)

Non-blocking send with delivery notification via callback.

```java
// Java - async with callback
producer.send(
    new ProducerRecord<>("orders", orderId, orderJson),
    (metadata, exception) -> {
        if (exception != null) {
            handleError(orderId, exception);
        } else {
            confirmDelivery(metadata);
        }
    }
);
```

```python
# Python - async with callback
def on_delivery(err, msg):
    if err:
        handle_error(msg.key(), err)
    else:
        confirm_delivery(msg)

p.produce("orders", key=order_id, value=order_json, callback=on_delivery)

# Must call poll() periodically to trigger callbacks
# In a send loop:
for record in records:
    p.produce("orders", key=record.key, value=record.value, callback=on_delivery)
    p.poll(0)  # non-blocking, fires any pending callbacks

p.flush()  # final drain
```

### Async with Future (Java only)

```java
// Java - collect futures, check later
List<Future<RecordMetadata>> futures = new ArrayList<>();

for (Order order : batch) {
    Future<RecordMetadata> f = producer.send(
        new ProducerRecord<>("orders", order.id(), serialize(order))
    );
    futures.add(f);
}

// Check all results
for (Future<RecordMetadata> f : futures) {
    try {
        RecordMetadata meta = f.get(10, TimeUnit.SECONDS);
    } catch (ExecutionException | TimeoutException e) {
        // handle
    }
}
```

## Custom Partitioners

### Java Custom Partitioner

```java
public class RegionPartitioner implements Partitioner {

    private Map<String, Integer> regionToPartition;

    @Override
    public void configure(Map<String, ?> configs) {
        // Load region -> partition mapping from config or external source
        regionToPartition = Map.of(
            "us-east", 0,
            "us-west", 1,
            "eu-west", 2,
            "ap-south", 3
        );
    }

    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        int numPartitions = partitions.size();

        if (key == null) {
            // fallback: round-robin
            return ThreadLocalRandom.current().nextInt(numPartitions);
        }

        String region = extractRegion(key.toString());
        Integer fixed = regionToPartition.get(region);
        if (fixed != null && fixed < numPartitions) {
            return fixed;
        }

        // fallback: murmur2 hash (same as default)
        return Utils.toPositive(Utils.murmur2(keyBytes)) % numPartitions;
    }

    @Override
    public void close() {}

    private String extractRegion(String key) {
        // key format: "us-east:order-123"
        int idx = key.indexOf(':');
        return idx > 0 ? key.substring(0, idx) : "default";
    }
}

// Usage
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, RegionPartitioner.class.getName());
```

### Python Custom Partitioner (confluent-kafka)

confluent-kafka does not support a partitioner class. Instead, compute the partition and pass it explicitly:

```python
import hashlib

def region_partition(key: str, num_partitions: int) -> int:
    """Route by region prefix in key, fallback to hash."""
    region_map = {"us-east": 0, "us-west": 1, "eu-west": 2, "ap-south": 3}
    if ":" in key:
        region = key.split(":")[0]
        p = region_map.get(region)
        if p is not None and p < num_partitions:
            return p
    # fallback: consistent hash
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % num_partitions

# Usage
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient

admin = AdminClient({"bootstrap.servers": "broker1:9092"})
metadata = admin.list_topics("orders")
num_partitions = len(metadata.topics["orders"].partitions)

p = Producer({"bootstrap.servers": "broker1:9092", "acks": "all"})

key = "us-east:order-456"
partition = region_partition(key, num_partitions)
p.produce("orders", key=key, value=payload, partition=partition, callback=on_delivery)
p.flush()
```

## Headers

Record headers are key-value pairs (`string -> bytes`) attached to each message without affecting serialization or partitioning. Used for metadata propagation: trace IDs, source system, content type, schema version.

```java
// Java - headers
ProducerRecord<String, String> record = new ProducerRecord<>("events", eventId, eventJson);
record.headers()
    .add("trace-id", traceId.getBytes(StandardCharsets.UTF_8))
    .add("source", "order-service".getBytes(StandardCharsets.UTF_8))
    .add("content-type", "application/json".getBytes(StandardCharsets.UTF_8))
    .add("schema-version", "3".getBytes(StandardCharsets.UTF_8));

producer.send(record);
```

```python
# Python - headers
p.produce(
    "events",
    key=event_id,
    value=event_json,
    headers={
        "trace-id": trace_id.encode(),
        "source": b"order-service",
        "content-type": b"application/json",
        "schema-version": b"3",
    },
    callback=on_delivery,
)
```

Headers are preserved through the entire pipeline (producer -> broker -> consumer) and are readable without deserializing the value.

## Interceptors

Interceptors hook into the producer pipeline for cross-cutting concerns (metrics, tracing, auditing) without modifying business logic.

### Java ProducerInterceptor

```java
public class TracingInterceptor implements ProducerInterceptor<String, String> {

    @Override
    public ProducerRecord<String, String> onSend(ProducerRecord<String, String> record) {
        // Called before serialization -- can modify the record
        record.headers().add("send-timestamp",
            Long.toString(System.currentTimeMillis()).getBytes(StandardCharsets.UTF_8));
        record.headers().add("producer-host",
            getHostname().getBytes(StandardCharsets.UTF_8));
        return record;
    }

    @Override
    public void onAcknowledgement(RecordMetadata metadata, Exception exception) {
        // Called when broker responds (success or failure)
        if (exception != null) {
            Metrics.counter("kafka.producer.errors", "topic", metadata.topic()).increment();
        } else {
            long latency = System.currentTimeMillis() - metadata.timestamp();
            Metrics.timer("kafka.producer.latency", "topic", metadata.topic())
                   .record(latency, TimeUnit.MILLISECONDS);
        }
    }

    @Override
    public void close() {}

    @Override
    public void configure(Map<String, ?> configs) {}
}

// Register
props.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,
    TracingInterceptor.class.getName());
// Multiple interceptors: comma-separated, executed in order
```

### Python Interceptor Pattern

confluent-kafka does not have a formal interceptor API. Achieve the same via wrapper:

```python
class InstrumentedProducer:
    """Wrapper that adds interceptor-like behavior around confluent-kafka Producer."""

    def __init__(self, conf: dict):
        self._producer = Producer(conf)
        self._send_count = 0
        self._error_count = 0

    def produce(self, topic, key=None, value=None, headers=None, callback=None, **kwargs):
        headers = dict(headers or {})
        headers["send-timestamp"] = str(time.time_ns()).encode()
        headers["producer-host"] = socket.gethostname().encode()

        self._send_count += 1
        original_cb = callback

        def wrapped_callback(err, msg):
            if err:
                self._error_count += 1
                logger.error(f"Delivery failed: {err}")
            else:
                latency_ms = (time.time_ns() - int(msg.headers()["send-timestamp"])) / 1e6
                metrics.observe("producer_latency_ms", latency_ms)
            if original_cb:
                original_cb(err, msg)

        self._producer.produce(
            topic, key=key, value=value, headers=headers,
            callback=wrapped_callback, **kwargs
        )

    def poll(self, timeout=0):
        return self._producer.poll(timeout)

    def flush(self, timeout=None):
        return self._producer.flush(timeout)
```

## Backpressure: buffer.memory and max.block.ms

When the producer sends faster than the broker can accept, the internal buffer fills up.

### Java Buffer Mechanics

```
buffer.memory (default 32MB)
  |
  [Free Pool] <---> [Allocated Batches per TopicPartition]
  |
  When free pool exhausted:
    send() blocks for up to max.block.ms (default 60s)
    then throws TimeoutException
```

```java
// Java - backpressure configuration
props.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 67108864L);  // 64MB
props.put(ProducerConfig.MAX_BLOCK_MS_CONFIG, 30000);        // block 30s max, then fail fast

// Monitor buffer usage
Metric bufferAvailable = producer.metrics().get(
    new MetricName("buffer-available-bytes", "producer-metrics", "", Collections.emptyMap())
);
Metric bufferTotal = producer.metrics().get(
    new MetricName("buffer-total-bytes", "producer-metrics", "", Collections.emptyMap())
);
// Alert when bufferAvailable / bufferTotal < 0.2 (80% full)
```

### Python Buffer Configuration

```python
# confluent-kafka uses different parameter names for buffer control
p = Producer({
    "bootstrap.servers": "broker1:9092",
    "queue.buffering.max.messages": 100000,      # max messages in internal queue
    "queue.buffering.max.kbytes": 1048576,        # 1GB max buffer (kbytes)
    "queue.buffering.max.ms": 5,                  # linger.ms equivalent
    "message.send.max.retries": 2147483647,
})

# Check queue length for backpressure
queue_len = len(p)  # returns current internal queue length
if queue_len > 50000:
    # slow down production, apply backpressure upstream
    time.sleep(0.1)
```

### Backpressure Strategies

1. **Block and wait** (default) -- `max.block.ms` controls how long. Simple but can stall the caller thread.
2. **Fail fast** -- set `max.block.ms=0` (Java) or check `len(p)` (Python) and reject/drop if full.
3. **Rate limiting upstream** -- use a semaphore or token bucket before calling `send()`.
4. **Increase buffer** -- `buffer.memory` up to available heap (Java) or `queue.buffering.max.kbytes` (Python).

```java
// Java - semaphore-based rate limiter
Semaphore semaphore = new Semaphore(10000); // max 10K in-flight messages

void sendWithBackpressure(String topic, String key, String value) throws InterruptedException {
    semaphore.acquire();
    producer.send(new ProducerRecord<>(topic, key, value), (meta, ex) -> {
        semaphore.release();
        if (ex != null) handleError(key, ex);
    });
}
```

## Key Serialization Patterns

### Schema Registry Integration

```java
// Java - Avro key + value with Schema Registry
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
    KafkaAvroSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
    KafkaAvroSerializer.class.getName());
props.put("schema.registry.url", "http://schema-registry:8081");

// The Schema Registry client auto-registers schemas on first send
GenericRecord key = new GenericData.Record(keySchema);
key.put("orderId", "ORD-12345");

GenericRecord value = new GenericData.Record(valueSchema);
value.put("amount", 99.99);
value.put("currency", "USD");

producer.send(new ProducerRecord<>("orders", key, value));
```

```python
# Python - Avro with Schema Registry
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

sr_client = SchemaRegistryClient({"url": "http://schema-registry:8081"})

key_schema_str = '{"type":"record","name":"OrderKey","fields":[{"name":"orderId","type":"string"}]}'
value_schema_str = '''{"type":"record","name":"Order","fields":[
    {"name":"amount","type":"double"},
    {"name":"currency","type":"string"}
]}'''

key_serializer = AvroSerializer(sr_client, key_schema_str)
value_serializer = AvroSerializer(sr_client, value_schema_str)

producer = SerializingProducer({
    "bootstrap.servers": "broker1:9092",
    "key.serializer": key_serializer,
    "value.serializer": value_serializer,
    "acks": "all",
})

producer.produce(
    "orders",
    key={"orderId": "ORD-12345"},
    value={"amount": 99.99, "currency": "USD"},
    on_delivery=on_delivery,
)
producer.flush()
```

### JSON Serialization with Schema Validation

```java
// Java - JSON Schema serializer
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
    KafkaJsonSchemaSerializer.class.getName());
props.put("schema.registry.url", "http://schema-registry:8081");
props.put("auto.register.schemas", true);
props.put("json.fail.invalid.schema", true);  // reject messages that violate schema
```

For details on schema management: [[schema-registry]].

## Idempotent Producer - Configuration Details

Idempotent producer assigns a PID (Producer ID) and sequence numbers to each message, allowing the broker to deduplicate retries.

### Full Idempotent Configuration

```java
// Java - explicit idempotent setup
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092,broker3:9092");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
// These are automatically enforced when idempotence is enabled:
// acks = all
// retries = Integer.MAX_VALUE
// max.in.flight.requests.per.connection <= 5
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
```

```python
# Python - idempotent producer
p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092,broker3:9092",
    "enable.idempotence": True,
    # acks automatically set to "all"
    # max.in.flight.requests.per.connection automatically capped at 5
})
```

### Idempotency Scope and Limits

- **Scope:** per-partition, per-producer-session. The broker tracks the last 5 sequence numbers per PID per partition.
- **Session boundary:** if the producer restarts, it gets a new PID. Old in-flight retries cannot be deduplicated against the new PID.
- **Does NOT deduplicate application-level retries.** If your code catches an error and calls `produce()` again, the message gets a new sequence number - the broker sees it as a new message.
- **For cross-session exactly-once,** use [[kafka-transactions]] with `transactional.id`.

### Ordering Guarantee

With idempotency enabled and `max.in.flight.requests.per.connection <= 5`, the broker rejects out-of-order sequence numbers and the client re-sends in the correct order. This guarantees per-partition ordering even during retries.

Without idempotency, if `max.in.flight > 1`, a retry of batch N can arrive after batch N+1 succeeds, causing out-of-order writes.

## Production Checklist

```yaml
# Durable, high-throughput producer config
bootstrap.servers: broker1:9092,broker2:9092,broker3:9092
acks: all
enable.idempotence: true
max.in.flight.requests.per.connection: 5
retries: 2147483647
delivery.timeout.ms: 120000
request.timeout.ms: 30000
retry.backoff.ms: 100

# Batching
batch.size: 65536         # 64KB - tune based on avg message size
linger.ms: 10             # 10ms - trade 10ms latency for better batching

# Compression
compression.type: lz4     # or zstd for storage-sensitive

# Backpressure
buffer.memory: 67108864   # 64MB (Java)
max.block.ms: 60000       # fail after 60s if buffer full

# Monitoring: track these metrics
# - record-send-rate
# - record-error-rate
# - batch-size-avg
# - buffer-available-bytes
# - request-latency-avg
# - produce-throttle-time-avg (broker-side throttling)
```

## Gotchas

- **Interceptor exceptions are swallowed.** If `onSend()` throws, the exception is caught and logged but the record is still sent. Don't rely on interceptors for validation - use explicit checks before `send()`.
- **Custom partitioner sees serialized bytes.** The `partition()` method receives `keyBytes` (already serialized). If you need the original object, use the `key` parameter (Object type) and cast.
- **`len(producer)` in confluent-kafka counts only the local queue,** not in-flight requests. True backpressure requires tracking callbacks.
- **Headers are not compressed.** Large headers add per-message overhead that is not reduced by batch compression. Keep headers small.
- **`max.in.flight.requests.per.connection > 1` without idempotency** risks out-of-order delivery on retries. If ordering matters and you cannot enable idempotency, set `max.in.flight=1` (but throughput drops significantly).
- **Broker-side `message.max.bytes` default is 1MB.** Messages larger than this are rejected with `MSG_SIZE_TOO_LARGE`. Increase both broker (`message.max.bytes`) and topic (`max.message.bytes`) configs if needed.
- **`flush()` in Python does not throw on delivery failure.** It returns the number of messages still in the queue. Check errors in the delivery callback, not the `flush()` return value.
- **Transactional producers cannot be used with `acks != all`.** Setting `transactional.id` forces `acks=all`, `enable.idempotence=true`. Attempting to override these throws `ConfigException`.

## See Also

- [[topics-and-partitions]] -- partition mechanics, key-based routing, segment structure
- [[kafka-transactions]] -- transactional producer API, exactly-once read-process-write
- [[schema-registry]] -- Avro/JSON Schema/Protobuf serialization with schema evolution
- [[broker-architecture]] -- how brokers handle ProduceRequests, replication, ISR management
