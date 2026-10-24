---
level: 3
source_sha256: eb2657598a6e75495728fed94f398f9da2d9a670c854b54bc8dd2ed01da45821
translation: machine
translated_at: '2026-10-24'
---
# Modèles avancés pour producteurs Kafka {#kafka-producer-advanced-patterns}

Partitionneurs personnalisés, en-têtes de records, intercepteurs, gestion de la contre-pression, fonctionnement interne du producteur idempotent, intégration avec Schema Registry et liste de contrôle pour la production.

Pour le pipeline d'envoi, les modes d'acquittement (acks), le regroupement (batching), la compression et la gestion d'erreurs de base, voir [[kafka-producer-fundamentals]].

## Partitionneurs personnalisés {#custom-partitioners}

### Partitionneur personnalisé en Java {#java-custom-partitioner}

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

### Partitionneur personnalisé en Python (confluent-kafka) {#python-custom-partitioner-confluent-kafka}

confluent-kafka ne prend pas en charge de classe de partitionnement. Calculez la partition et passez-la explicitement :

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

## En-têtes {#headers}

Les en-têtes de records sont des paires clé-valeur (`string -> bytes`) attachées à chaque message sans affecter la sérialisation ni le partitionnement. Ils servent à propager des métadonnées : identifiants de trace, système source, type de contenu, version de schéma.

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

Les en-têtes sont conservés tout au long du pipeline (producteur -> broker -> consommateur) et peuvent être lus sans désérialiser la valeur.

## Intercepteurs {#interceptors}

Les intercepteurs s'intègrent au pipeline du producteur pour les préoccupations transversales (métriques, traçage, audit) sans modifier la logique métier.

### ProducerInterceptor en Java {#java-producerinterceptor}

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

### Modèle d'intercepteur en Python {#python-interceptor-pattern}

confluent-kafka ne dispose pas d'API formelle d'intercepteurs. On obtient un résultat équivalent par un wrapper :

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

## Contre-pression : buffer.memory et max.block.ms {#backpressure-buffermemory-and-maxblockms}

Lorsque le producteur envoie plus vite que le broker ne peut accepter, le tampon interne se remplit.

### Mécanisme de tampon en Java {#java-buffer-mechanics}

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

### Configuration du tampon en Python {#python-buffer-configuration}

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

### Stratégies face à la contre-pression {#backpressure-strategies}

1. **Bloquer et attendre** (comportement par défaut) — `max.block.ms` en détermine la durée.
2. **Échec immédiat** — réglez `max.block.ms=0` (Java) ou vérifiez `len(p)` (Python) et rejetez le message si le tampon est plein.
3. **Limitation de débit en amont** — utilisez un sémaphore ou un token bucket avant d'appeler `send()`.
4. **Augmenter le tampon** — `buffer.memory` (Java) ou `queue.buffering.max.kbytes` (Python).

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

## Intégration avec Schema Registry {#schema-registry-integration}

### Avro avec Schema Registry {#avro-with-schema-registry}

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

Pour plus de détails sur la gestion des schémas : [[schema-registry]].

## Producteur idempotent {#idempotent-producer}

Le producteur idempotent attribue un PID (Producer ID) et des numéros de séquence à chaque message, ce qui permet au broker de dédupliquer les tentatives de réémission.

### Configuration {#configuration}

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

### Portée et limites {#scope-and-limits}

- **Portée :** par partition, par session de producteur. Le broker conserve les 5 derniers numéros de séquence par PID et par partition.
- **Frontière de session :** si le producteur redémarre, il obtient un nouveau PID. Les anciennes tentatives en vol ne peuvent pas être dédupliquées par rapport au nouveau PID.
- **Ne déduplique pas les réémissions au niveau applicatif.** Si votre code intercepte une erreur et rappelle `produce()`, le message reçoit un nouveau numéro de séquence.
- **Pour l'exactly-once inter-sessions,** utilisez [[kafka-transactions]] avec `transactional.id`.

### Garantie d'ordonnancement {#ordering-guarantee}

Avec l'idempotence activée et `max.in.flight.requests.per.connection <= 5`, le broker rejette les numéros de séquence arrivés hors ordre et le client les renvoie dans le bon ordre. Cela garantit l'ordre par partition, y compris lors des réémissions.

## Liste de contrôle pour la production {#production-checklist}

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

## Pièges courants {#gotchas}

- **Les exceptions des intercepteurs sont avalées.** Si `onSend()` lève une exception, elle est capturée et journalisée, mais le record est tout de même envoyé. Ne vous appuyez pas sur les intercepteurs pour la validation.
- **Le partitionneur personnalisé voit des octets sérialisés.** La méthode `partition()` reçoit `keyBytes` (déjà sérialisé). Si vous avez besoin de l'objet d'origine, utilisez le paramètre `key` (de type Object) et effectuez un cast.
- **`len(producer)` dans confluent-kafka ne compte que la file locale,** et non les requêtes en vol. Une véritable contre-pression nécessite de suivre les callbacks.
- **Les en-têtes ne sont pas compressés.** De gros en-têtes ajoutent une surcharge par message que la compression par lot ne réduit pas. Gardez les en-têtes petits.
- **Les producteurs transactionnels ne peuvent pas être utilisés avec `acks != all`.** Définir `transactional.id` force `acks=all` et `enable.idempotence=true`. Tenter de surcharger ces valeurs lève une `ConfigException`.

## Voir aussi {#see-also}

- [[kafka-producer-fundamentals]] - pipeline d'envoi, acks, batching, compression, gestion des erreurs
- [[topics-and-partitions]] - mécanique des partitions, routage par clé
- [[kafka-transactions]] - API du producteur transactionnel, sémantique exactly-once
- [[schema-registry]] - sérialisation Avro/JSON Schema/Protobuf et évolution des schémas
- [[partitioning-strategies]] - patrons de partitionnement en détail
- [[broker-architecture]] - traitement des ProduceRequests par les brokers, réplication
