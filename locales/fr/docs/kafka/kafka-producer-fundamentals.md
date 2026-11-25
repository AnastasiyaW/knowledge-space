---
level: 3
source_sha256: 349ce76c3629711360f98349cea40200371cadd08f876d6d0491e4a363a645d7
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux du producteur Kafka {#kafka-producer-fundamentals}

Pipeline d'envoi du producteur, modes d'acquittement (`acks`), mécanique de batching, choix de la compression, configuration des tentatives, gestion des erreurs et modes d'envoi (fire-and-forget, synchrone, asynchrone).

## Pipeline d'envoi du producteur {#producer-send-pipeline}

Chaque appel à `send()` traverse ce pipeline avant que les octets ne partent sur le réseau :

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

Point clé : la sérialisation intervient **avant** le partitionnement. Le partitionneur voit les octets de la clé sérialisée (ce qui est pertinent pour les partitionneurs personnalisés). La compression s'effectue au niveau du **batch**, et non message par message.

## Modes d'acquittement (acks) {#acks-modes}

### acks=0 : Fire-and-Forget {#acks0-fire-and-forget}

Le producteur n'attend aucun acquittement du broker. `send()` retourne immédiatement après que le message a été placé dans le tampon réseau.

**Quand l'utiliser :** collecte de métriques, suivi de clics, journalisation de débogage, c'est-à-dire partout où la perte d'un faible pourcentage de messages est acceptable et où le débit est prioritaire.

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

### acks=1 : Leader uniquement {#acks1-leader-only}

Le leader écrit dans son journal local et répond. Les réplicas récupèrent les données de manière asynchrone.

**Quand l'utiliser :** pipelines à faible latence où une perte occasionnelle de messages en cas de panne du leader est tolérable. Courant dans l'agrégation de logs.

**Fenêtre de risque :** entre l'écriture sur le leader et la récupération par les followers. Si le leader tombe pendant cette fenêtre, le nouveau leader (élu parmi l'ISR) ne possédera pas le message.

### acks=all (-1) : Acquittement de tout l'ISR {#acksall-1-full-isr-acknowledgment}

Le leader attend que tous les réplicas synchronisés (ISR) aient acquitté avant de répondre au producteur.

**Association critique avec `min.insync.replicas` :**

| `replication.factor` | `min.insync.replicas` | Comportement |
|-|-|-|
| 3 | 1 | `acks=all` se dégrade en `acks=1` si 2 réplicas sortent de l'ISR |
| 3 | 2 | Tolère la panne d'1 broker ; le producteur reçoit `NotEnoughReplicasException` si l'ISR < 2 |
| 3 | 3 | Aucune tolérance aux pannes ; un seul broker en panne = écritures bloquées |

**Standard en production :** RF=3, `min.insync.replicas=2`, `acks=all`.

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

## Patterns de batching {#batching-patterns}

### Mécanique du batch {#batch-mechanics}

Le `RecordAccumulator` maintient un `Deque<ProducerBatch>` par `TopicPartition`. Chaque batch est un tampon `MemoryRecords` alloué depuis `buffer.memory`.

```text
buffer.memory (total pool)
  |
  +-- TopicPartition(orders, 0) -> [batch 16KB] [batch 16KB]
  +-- TopicPartition(orders, 1) -> [batch 16KB]
  +-- TopicPartition(events, 0) -> [batch 16KB] [batch 16KB] [batch 16KB]
```

Un batch est envoyé lorsque **l'une ou l'autre** de ces conditions est remplie :
1. `batch.size` octets se sont accumulés dans le batch
2. `linger.ms` s'est écoulé depuis l'ajout du premier enregistrement au batch

### Batching optimisé pour le débit {#throughput-optimized-batching}

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

### Faible latence (batching minimal) {#latency-optimized-minimal-batching}

```java
// Java - low latency
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);  // default 16KB
props.put(ProducerConfig.LINGER_MS_CONFIG, 0);        // send immediately
props.put(ProducerConfig.ACKS_CONFIG, "1");            // leader only
```

### Pattern de batching adaptatif {#adaptive-batching-pattern}

Surveiller le taux de remplissage des batchs pour ajuster `linger.ms` dynamiquement :

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

## Patterns de compression {#compression-patterns}

La compression s'applique au niveau du **batch**. Le broker stocke les batchs compressés ; les consommateurs les décompressent à la lecture.

### Comparaison des codecs {#codec-comparison}

| Codec | Taux de compression | CPU (compression) | CPU (décompression) | Usage recommandé |
|-|-|-|-|-|
| `lz4` | Faible à moyen | Très faible | Très faible | Usage général, choix par défaut |
| `snappy` | Faible à moyen | Faible | Très faible | Proche de lz4, préférence historique |
| `zstd` | Élevé | Moyen | Faible | Gros messages, contraintes de stockage, volume élevé |
| `gzip` | Moyen à élevé | Élevé | Moyen | Compatibilité avec des consommateurs non Kafka |

### Arbre de décision pour le choix {#selection-decision-tree}

```text
Is CPU a constraint?
  YES -> lz4 or snappy
  NO  -> Is storage/bandwidth a constraint?
           YES -> zstd (best ratio)
           NO  -> Is interop with non-Kafka systems needed?
                    YES -> gzip
                    NO  -> lz4 (balanced default)
```

### Compression côté broker vs côté producteur {#broker-side-vs-producer-side-compression}

Si le `compression.type` du broker pour un topic diffère de celui du producteur, le broker **recompresse** chaque batch, ce qui gaspille énormément de CPU.

```bash
# Match producer and broker compression to avoid recompression
# broker topic config:
kafka-configs.sh --alter --topic orders \
  --add-config compression.type=lz4

# producer config must also use lz4
```

Si le topic du broker a `compression.type=producer` (valeur par défaut), le broker stocke ce que le producteur envoie, sans recompression.

## Gestion des tentatives et des erreurs {#retry-and-error-handling}

### Configuration des tentatives {#retry-configuration}

```java
Properties props = new Properties();
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);     // unlimited retries
props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);    // 2 min overall deadline
props.put(ProducerConfig.RETRY_BACKOFF_MS_CONFIG, 100);          // 100ms between retries
props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);      // 30s per attempt
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);       // deduplicate retries
props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
```

**Contrainte :** `delivery.timeout.ms >= linger.ms + request.timeout.ms`. Ne pas respecter cette contrainte produit une `TimeoutException` avant que la première tentative de réémission ne puisse se terminer.

### Erreurs réessayables vs erreurs fatales {#retriable-vs-fatal-errors}

| Type d'erreur | Exemples | Comportement du producteur |
|-|-|-|
| Réessayable | `LEADER_NOT_AVAILABLE`, `NOT_ENOUGH_REPLICAS`, `REQUEST_TIMED_OUT`, `NETWORK_EXCEPTION` | Réémises automatiquement jusqu'à `delivery.timeout.ms` |
| Fatale | `MESSAGE_TOO_LARGE`, `INVALID_TOPIC_EXCEPTION`, `TOPIC_AUTHORIZATION_FAILED`, `SERIALIZATION_ERROR` | Renvoyées immédiatement via le callback, sans réémission |

### Gestion des erreurs avec des callbacks {#error-handling-with-callbacks}

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

## Modes d'envoi {#send-patterns}

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

### Envoi synchrone {#synchronous-send}

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

### Asynchrone avec callback (recommandé) {#async-with-callback-recommended}

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

## Pièges courants {#gotchas}

- **`max.in.flight.requests.per.connection > 1` sans idempotence** risque une livraison désordonnée lors des réémissions. Si l'ordre compte et que l'idempotence ne peut pas être activée, fixez `max.in.flight=1` (mais le débit chute nettement).
- **La valeur par défaut de `message.max.bytes` côté broker est 1 Mo.** Les messages plus volumineux sont rejetés avec `MSG_SIZE_TOO_LARGE`. Augmentez à la fois la configuration du broker (`message.max.bytes`) et celle du topic (`max.message.bytes`) si nécessaire.
- **`flush()` en Python ne lève pas d'exception en cas d'échec de livraison.** Elle retourne le nombre de messages encore présents dans la file. Vérifiez les erreurs dans le callback de livraison, et non dans la valeur retournée par `flush()`.
- **`delivery.timeout.ms` doit être >= `linger.ms + request.timeout.ms`.** Sinon, le délai expire avant la fin de la première tentative de réémission.

## Voir aussi {#see-also}

- [[kafka-producer-advanced-patterns]] - partitionneurs personnalisés, en-têtes, intercepteurs, contre-pression, producteur idempotent, Schema Registry
- [[topics-and-partitions]] - mécanique des partitions, routage par clé, structure des segments
- [[kafka-transactions]] - API du producteur transactionnel, lecture-traitement-écriture exactly-once
- [[kafka-replication-fundamentals]] - ISR, interaction entre `acks` et la réplication
- [[broker-architecture]] - traitement des ProduceRequests par les brokers
