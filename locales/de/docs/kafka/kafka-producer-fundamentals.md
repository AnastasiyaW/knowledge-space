---
level: 3
source_sha256: 349ce76c3629711360f98349cea40200371cadd08f876d6d0491e4a363a645d7
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Producer-Grundlagen {#kafka-producer-fundamentals}

Send-Pipeline des Producers, acks-Modi, Batching-Mechanik, Auswahl der Komprimierung, Retry-Konfiguration, Fehlerbehandlung und Sendemuster (Fire-and-Forget, synchron, asynchron).

## Send-Pipeline des Producers {#producer-send-pipeline}

Jeder `send()`-Aufruf durchläuft diese Pipeline, bevor Bytes auf die Leitung gelangen:

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

Zentrale Erkenntnis: Die Serialisierung erfolgt **vor** der Partitionierung. Der Partitionierer sieht die serialisierten Key-Bytes (relevant für eigene Partitionierer). Die Komprimierung erfolgt auf **Batch**-Ebene, nicht pro Nachricht.

## acks-Modi {#acks-modes}

### acks=0: Fire-and-Forget {#acks0-fire-and-forget}

Der Producer wartet auf keine Bestätigung des Brokers. `send()` kehrt sofort zurück, nachdem die Nachricht im Netzwerkpuffer abgelegt wurde.

**Einsatz:** Metrikerfassung, Klick-Tracking, Debug-Logging – überall dort, wo der Verlust eines kleinen Anteils von Nachrichten akzeptabel ist und der Durchsatz Priorität hat.

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

### acks=1: Nur Leader {#acks1-leader-only}

Der Leader schreibt in sein lokales Log und antwortet. Replicas holen die Daten asynchron nach.

**Einsatz:** Latenzkritische Pipelines, in denen gelegentlicher Nachrichtenverlust beim Ausfall des Leaders tolerierbar ist. Häufig in der Log-Aggregation.

**Risikofenster:** Zwischen dem Schreiben auf dem Leader und dem Abruf durch die Follower. Fällt der Leader in diesem Zeitfenster aus, verfügt der neue Leader (aus der ISR gewählt) nicht über die Nachricht.

### acks=all (-1): Bestätigung durch alle ISR {#acksall-1-full-isr-acknowledgment}

Der Leader wartet, bis alle In-Sync-Replicas (ISR) bestätigt haben, bevor er dem Producer antwortet.

**Kritische Kombination mit `min.insync.replicas`:**

| `replication.factor` | `min.insync.replicas` | Verhalten |
|-|-|-|
| 3 | 1 | `acks=all` fällt auf `acks=1` zurück, wenn 2 Replicas aus der ISR fallen |
| 3 | 2 | Toleriert den Ausfall eines Brokers; der Producer erhält `NotEnoughReplicasException`, wenn die ISR < 2 ist |
| 3 | 3 | Keine Ausfalltoleranz; fällt ein Broker aus, sind Schreibvorgänge blockiert |

**Produktionsstandard:** RF=3, `min.insync.replicas=2`, `acks=all`.

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

## Batching-Muster {#batching-patterns}

### Batch-Mechanik {#batch-mechanics}

Der `RecordAccumulator` verwaltet pro `TopicPartition` eine `Deque<ProducerBatch>`. Jeder Batch ist ein `MemoryRecords`-Puffer, der aus `buffer.memory` allokiert wird.

```text
buffer.memory (total pool)
  |
  +-- TopicPartition(orders, 0) -> [batch 16KB] [batch 16KB]
  +-- TopicPartition(orders, 1) -> [batch 16KB]
  +-- TopicPartition(events, 0) -> [batch 16KB] [batch 16KB] [batch 16KB]
```

Ein Batch wird gesendet, sobald **eine** der folgenden Bedingungen erfüllt ist:
1. Im Batch haben sich `batch.size` Bytes angesammelt
2. `linger.ms` ist verstrichen, seit der erste Datensatz dem Batch hinzugefügt wurde

### Durchsatzoptimiertes Batching {#throughput-optimized-batching}

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

### Latenzoptimiertes Batching (minimal) {#latency-optimized-minimal-batching}

```java
// Java - low latency
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);  // default 16KB
props.put(ProducerConfig.LINGER_MS_CONFIG, 0);        // send immediately
props.put(ProducerConfig.ACKS_CONFIG, "1");            // leader only
```

### Adaptives Batching-Muster {#adaptive-batching-pattern}

Füllgrad der Batches überwachen, um `linger.ms` dynamisch anzupassen:

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

## Komprimierungsmuster {#compression-patterns}

Die Komprimierung wird auf **Batch**-Ebene angewendet. Der Broker speichert Batches komprimiert; Consumer dekomprimieren beim Lesen.

### Vergleich der Codecs {#codec-comparison}

| Codec | Kompressionsrate | CPU (Komprimierung) | CPU (Dekomprimierung) | Geeignet für |
|-|-|-|-|-|
| `lz4` | Niedrig bis mittel | Sehr niedrig | Sehr niedrig | Allgemein einsetzbar, Standardwahl |
| `snappy` | Niedrig bis mittel | Niedrig | Sehr niedrig | Ähnlich wie lz4, historisch bevorzugt |
| `zstd` | Hoch | Mittel | Niedrig | Große Nachrichten, speicherbegrenzte Systeme, hohes Datenvolumen |
| `gzip` | Mittel bis hoch | Hoch | Mittel | Kompatibilität mit Nicht-Kafka-Consumern |

### Entscheidungsbaum zur Auswahl {#selection-decision-tree}

```text
Is CPU a constraint?
  YES -> lz4 or snappy
  NO  -> Is storage/bandwidth a constraint?
           YES -> zstd (best ratio)
           NO  -> Is interop with non-Kafka systems needed?
                    YES -> gzip
                    NO  -> lz4 (balanced default)
```

### Komprimierung auf Broker- vs. Producer-Seite {#broker-side-vs-producer-side-compression}

Weicht das `compression.type` eines Topics auf dem Broker vom Wert des Producers ab, komprimiert der Broker **jeden Batch neu** – eine enorme CPU-Verschwendung.

```bash
# Match producer and broker compression to avoid recompression
# broker topic config:
kafka-configs.sh --alter --topic orders \
  --add-config compression.type=lz4

# producer config must also use lz4
```

Hat das Broker-Topic `compression.type=producer` (Standard), speichert der Broker die vom Producer gesendeten Daten unverändert, ohne Neukomprimierung.

## Retry und Fehlerbehandlung {#retry-and-error-handling}

### Retry-Konfiguration {#retry-configuration}

```java
Properties props = new Properties();
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);     // unlimited retries
props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);    // 2 min overall deadline
props.put(ProducerConfig.RETRY_BACKOFF_MS_CONFIG, 100);          // 100ms between retries
props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);      // 30s per attempt
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);       // deduplicate retries
props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
```

**Bedingung:** `delivery.timeout.ms >= linger.ms + request.timeout.ms`. Wird dies verletzt, tritt eine `TimeoutException` auf, bevor der erste Retry abgeschlossen werden kann.

### Wiederholbare vs. fatale Fehler {#retriable-vs-fatal-errors}

| Fehlertyp | Beispiele | Verhalten des Producers |
|-|-|-|
| Wiederholbar | `LEADER_NOT_AVAILABLE`, `NOT_ENOUGH_REPLICAS`, `REQUEST_TIMED_OUT`, `NETWORK_EXCEPTION` | Automatisch wiederholt bis `delivery.timeout.ms` |
| Fatal | `MESSAGE_TOO_LARGE`, `INVALID_TOPIC_EXCEPTION`, `TOPIC_AUTHORIZATION_FAILED`, `SERIALIZATION_ERROR` | Wird sofort über den Callback zurückgegeben, kein Retry |

### Fehlerbehandlung mit Callbacks {#error-handling-with-callbacks}

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

## Sendemuster {#send-patterns}

### Fire-and-Forget {#fire-and-forget}

```java
// Java
producer.send(new ProducerRecord<>("logs", logLine));
```

```python
# Python
p.produce("logs", value=log_line)
p.poll(0)
```

### Synchroner Versand {#synchronous-send}

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

### Asynchron mit Callback (empfohlen) {#async-with-callback-recommended}

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

## Fallstricke {#gotchas}

- **`max.in.flight.requests.per.connection > 1` ohne Idempotenz** riskiert bei Retries eine Auslieferung in falscher Reihenfolge. Ist die Reihenfolge wichtig und lässt sich Idempotenz nicht aktivieren, setzen Sie `max.in.flight=1` (der Durchsatz sinkt dadurch aber deutlich).
- **Der Standardwert von `message.max.bytes` auf dem Broker beträgt 1 MB.** Größere Nachrichten werden mit `MSG_SIZE_TOO_LARGE` abgelehnt. Erhöhen Sie bei Bedarf sowohl die Broker-Konfiguration (`message.max.bytes`) als auch die Topic-Konfiguration (`max.message.bytes`).
- **`flush()` in Python wirft bei Auslieferungsfehlern keine Exception.** Es gibt die Anzahl der noch in der Warteschlange befindlichen Nachrichten zurück. Fehler prüfen Sie im Delivery-Callback, nicht am Rückgabewert von `flush()`.
- **`delivery.timeout.ms` muss >= `linger.ms + request.timeout.ms` sein.** Andernfalls läuft das Timeout ab, bevor der erste Wiederholungsversuch abgeschlossen ist.

## Siehe auch {#see-also}

- [[kafka-producer-advanced-patterns]] - eigene Partitionierer, Header, Interceptoren, Backpressure, idempotenter Producer, Schema Registry
- [[topics-and-partitions]] - Partitionsmechanik, schlüsselbasiertes Routing, Segmentaufbau
- [[kafka-transactions]] - transaktionale Producer-API, Exactly-once Read-Process-Write
- [[kafka-replication-fundamentals]] - ISR, Zusammenspiel von acks mit der Replikation
- [[broker-architecture]] - wie Broker ProduceRequests verarbeiten
