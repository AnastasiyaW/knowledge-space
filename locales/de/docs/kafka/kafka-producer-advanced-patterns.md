---
level: 3
source_sha256: eb2657598a6e75495728fed94f398f9da2d9a670c854b54bc8dd2ed01da45821
translation: machine
translated_at: '2026-10-24'
---
# Kafka Producer: Fortgeschrittene Muster {#kafka-producer-advanced-patterns}

Custom Partitioner, Record-Header, Interceptors, Backpressure-Behandlung, interne Funktionsweise des idempotenten Producers, Schema-Registry-Integration und Produktions-Checkliste.

Zur Sendepipeline, den acks-Modi, Batching, Komprimierung und der grundlegenden Fehlerbehandlung siehe [[kafka-producer-fundamentals]].

## Custom Partitioner {#custom-partitioners}

### Java Custom Partitioner {#java-custom-partitioner}

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

### Python Custom Partitioner (confluent-kafka) {#python-custom-partitioner-confluent-kafka}

confluent-kafka unterstützt keine Partitioner-Klasse. Die Partition wird selbst berechnet und explizit übergeben:

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

## Header {#headers}

Record-Header sind Schlüssel-Wert-Paare (`string -> bytes`), die jeder Nachricht angehängt werden, ohne Serialisierung oder Partitionierung zu beeinflussen. Sie dienen der Weitergabe von Metadaten: Trace-IDs, Quellsystem, Content-Type, Schema-Version.

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

Header bleiben über die gesamte Pipeline erhalten (Producer -> Broker -> Consumer) und sind lesbar, ohne den Wert zu deserialisieren.

## Interceptors {#interceptors}

Interceptors greifen in die Producer-Pipeline ein, um querschnittliche Belange (Metriken, Tracing, Auditing) zu behandeln, ohne die Geschäftslogik zu verändern.

### Java ProducerInterceptor {#java-producerinterceptor}

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

### Python Interceptor-Muster {#python-interceptor-pattern}

confluent-kafka besitzt keine formale Interceptor-API. Dasselbe Verhalten wird über einen Wrapper erreicht:

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

## Backpressure: buffer.memory und max.block.ms {#backpressure-buffermemory-and-maxblockms}

Sendet der Producer schneller, als der Broker Nachrichten annehmen kann, füllt sich der interne Puffer.

### Java-Mechanik des Puffers {#java-buffer-mechanics}

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

### Python-Konfiguration des Puffers {#python-buffer-configuration}

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

### Backpressure-Strategien {#backpressure-strategies}

1. **Blockieren und warten** (Standard) -- `max.block.ms` legt die Dauer fest.
2. **Sofort fehlschlagen** -- `max.block.ms=0` setzen (Java) oder `len(p)` prüfen (Python) und die Nachricht bei vollem Puffer ablehnen.
3. **Upstream-Ratenbegrenzung** -- vor dem Aufruf von `send()` einen Semaphor oder Token Bucket verwenden.
4. **Puffer vergrößern** -- `buffer.memory` (Java) oder `queue.buffering.max.kbytes` (Python).

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

## Schema-Registry-Integration {#schema-registry-integration}

### Avro mit Schema Registry {#avro-with-schema-registry}

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

Details zur Schema-Verwaltung: [[schema-registry]].

## Idempotenter Producer {#idempotent-producer}

Der idempotente Producer weist jeder Nachricht eine PID (Producer-ID) und Sequenznummern zu, sodass der Broker Wiederholungsversuche deduplizieren kann.

### Konfiguration {#configuration}

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

### Geltungsbereich und Grenzen {#scope-and-limits}

- **Geltungsbereich:** pro Partition und pro Producer-Sitzung. Der Broker speichert für jede PID und Partition die letzten 5 Sequenznummern.
- **Sitzungsgrenze:** Startet der Producer neu, erhält er eine neue PID. Alte, noch laufende Wiederholungsversuche können nicht gegen die neue PID dedupliziert werden.
- **Anwendungsseitige Wiederholungen werden NICHT dedupliziert.** Fängt der Code einen Fehler ab und ruft `produce()` erneut auf, erhält die Nachricht eine neue Sequenznummer.
- **Für sitzungsübergreifende Exactly-once-Semantik** [[kafka-transactions]] mit `transactional.id` verwenden.

### Garantie der Reihenfolge {#ordering-guarantee}

Ist Idempotenz aktiviert und gilt `max.in.flight.requests.per.connection <= 5`, lehnt der Broker Sequenznummern außer der Reihe ab, und der Client sendet in der korrekten Reihenfolge erneut. Dadurch bleibt die Reihenfolge pro Partition auch bei Wiederholungsversuchen erhalten.

## Produktions-Checkliste {#production-checklist}

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

## Stolperfallen {#gotchas}

- **Ausnahmen in Interceptors werden verschluckt.** Wirft `onSend()` eine Ausnahme, wird sie abgefangen und protokolliert, der Datensatz wird aber trotzdem gesendet. Interceptors nicht zur Validierung verwenden.
- **Der Custom Partitioner sieht serialisierte Bytes.** Die Methode `partition()` erhält `keyBytes` (bereits serialisiert). Wird das ursprüngliche Objekt benötigt, muss der Parameter `key` (Typ Object) verwendet und gecastet werden.
- **`len(producer)` in confluent-kafka zählt nur die lokale Warteschlange,** nicht die laufenden Anfragen. Echte Backpressure erfordert die Verfolgung von Callbacks.
- **Header werden nicht komprimiert.** Große Header verursachen pro Nachricht zusätzlichen Overhead, den auch die Batch-Komprimierung nicht reduziert. Header klein halten.
- **Transaktionale Producer können nicht mit `acks != all` verwendet werden.** Das Setzen von `transactional.id` erzwingt `acks=all` und `enable.idempotence=true`. Ein Überschreiben dieser Werte führt zu einer `ConfigException`.

## Siehe auch {#see-also}

- [[kafka-producer-fundamentals]] - Sendepipeline, acks, Batching, Komprimierung, Fehlerbehandlung
- [[topics-and-partitions]] - Partitionsmechanik, schlüsselbasiertes Routing
- [[kafka-transactions]] - API des transaktionalen Producers, Exactly-once-Semantik
- [[schema-registry]] - Avro/JSON Schema/Protobuf-Serialisierung mit Schema-Evolution
- [[partitioning-strategies]] - Partitioner-Muster im Detail
- [[broker-architecture]] - Verarbeitung von ProduceRequests durch Broker, Replikation
