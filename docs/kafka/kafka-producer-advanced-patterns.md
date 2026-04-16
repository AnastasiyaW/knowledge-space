# Kafka Producer Advanced Patterns

Custom partitioners, record headers, interceptors, backpressure handling, idempotent producer internals, Schema Registry integration, and production checklist.

For the send pipeline, acks modes, batching, compression, and basic error handling, see [[kafka-producer-fundamentals]].

## Custom Partitioners

### Java Custom Partitioner

```java
public class RegionPartitioner implements Partitioner {

    private Map<String, Integer> regionToPartition;

    @Override
    public void configure(Map<String, ?> configs) {
        regionToPartition = Map.of(
            "us-east", 0, "us-west", 1, "eu-west", 2, "ap-south", 3
        );
    }

    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        int numPartitions = partitions.size();

        if (key == null) {
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
        int idx = key.indexOf(':');
        return idx > 0 ? key.substring(0, idx) : "default";
    }
}

// Usage
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, RegionPartitioner.class.getName());
```

### Python Custom Partitioner (confluent-kafka)

confluent-kafka does not support a partitioner class. Compute the partition and pass it explicitly:

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
        record.headers().add("send-timestamp",
            Long.toString(System.currentTimeMillis()).getBytes(StandardCharsets.UTF_8));
        record.headers().add("producer-host",
            getHostname().getBytes(StandardCharsets.UTF_8));
        return record;
    }

    @Override
    public void onAcknowledgement(RecordMetadata metadata, Exception exception) {
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
```

### Python Interceptor Pattern

confluent-kafka does not have a formal interceptor API. Achieve the same via wrapper:

```python
class InstrumentedProducer:
    """Wrapper that adds interceptor-like behavior."""

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

```text
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
props.put(ProducerConfig.MAX_BLOCK_MS_CONFIG, 30000);        // block 30s max

// Monitor buffer usage
Metric bufferAvailable = producer.metrics().get(
    new MetricName("buffer-available-bytes", "producer-metrics", "", Collections.emptyMap())
);
// Alert when bufferAvailable / bufferTotal < 0.2 (80% full)
```

### Python Buffer Configuration

```python
p = Producer({
    "bootstrap.servers": "broker1:9092",
    "queue.buffering.max.messages": 100000,
    "queue.buffering.max.kbytes": 1048576,        # 1GB max buffer
    "queue.buffering.max.ms": 5,                  # linger.ms equivalent
    "message.send.max.retries": 2147483647,
})

# Check queue length for backpressure
queue_len = len(p)
if queue_len > 50000:
    time.sleep(0.1)  # slow down production
```

### Backpressure Strategies

1. **Block and wait** (default) -- `max.block.ms` controls how long.
2. **Fail fast** -- set `max.block.ms=0` (Java) or check `len(p)` (Python) and reject if full.
3. **Rate limiting upstream** -- use a semaphore or token bucket before calling `send()`.
4. **Increase buffer** -- `buffer.memory` (Java) or `queue.buffering.max.kbytes` (Python).

```java
// Java - semaphore-based rate limiter
Semaphore semaphore = new Semaphore(10000);

void sendWithBackpressure(String topic, String key, String value) throws InterruptedException {
    semaphore.acquire();
    producer.send(new ProducerRecord<>(topic, key, value), (meta, ex) -> {
        semaphore.release();
        if (ex != null) handleError(key, ex);
    });
}
```

## Schema Registry Integration

### Avro with Schema Registry

```java
// Java - Avro key + value
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class.getName());
props.put("schema.registry.url", "http://schema-registry:8081");

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

For details on schema management: [[schema-registry]].

## Idempotent Producer

Idempotent producer assigns a PID (Producer ID) and sequence numbers to each message, allowing the broker to deduplicate retries.

### Configuration

```java
// Java - idempotent setup
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092,broker3:9092");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
// Automatically enforced: acks=all, retries=MAX, max.in.flight<=5
```

```python
# Python - idempotent producer
p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092,broker3:9092",
    "enable.idempotence": True,
})
```

### Scope and Limits

- **Scope:** per-partition, per-producer-session. The broker tracks the last 5 sequence numbers per PID per partition.
- **Session boundary:** if the producer restarts, it gets a new PID. Old in-flight retries cannot be deduplicated against the new PID.
- **Does NOT deduplicate application-level retries.** If your code catches an error and calls `produce()` again, the message gets a new sequence number.
- **For cross-session exactly-once,** use [[kafka-transactions]] with `transactional.id`.

### Ordering Guarantee

With idempotency enabled and `max.in.flight.requests.per.connection <= 5`, the broker rejects out-of-order sequence numbers and the client re-sends in the correct order. This guarantees per-partition ordering even during retries.

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
batch.size: 65536         # 64KB
linger.ms: 10             # trade 10ms latency for better batching

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

- **Interceptor exceptions are swallowed.** If `onSend()` throws, the exception is caught and logged but the record is still sent. Don't rely on interceptors for validation.
- **Custom partitioner sees serialized bytes.** The `partition()` method receives `keyBytes` (already serialized). If you need the original object, use the `key` parameter (Object type) and cast.
- **`len(producer)` in confluent-kafka counts only the local queue,** not in-flight requests. True backpressure requires tracking callbacks.
- **Headers are not compressed.** Large headers add per-message overhead that is not reduced by batch compression. Keep headers small.
- **Transactional producers cannot be used with `acks != all`.** Setting `transactional.id` forces `acks=all`, `enable.idempotence=true`. Attempting to override throws `ConfigException`.

## See Also

- [[kafka-producer-fundamentals]] - send pipeline, acks, batching, compression, error handling
- [[topics-and-partitions]] - partition mechanics, key-based routing
- [[kafka-transactions]] - transactional producer API, exactly-once semantics
- [[schema-registry]] - Avro/JSON Schema/Protobuf serialization with schema evolution
- [[partitioning-strategies]] - partitioner patterns in depth
- [[broker-architecture]] - how brokers handle ProduceRequests, replication
