---
title: "Liefersemantik"
category: concepts
tags: [kafka, delivery, exactly-once, at-least-once, at-most-once, idempotent]
level: 3
source_sha256: 91408255db31fda830960730031e5b6913f422c64066a7a765a0a3c99d9e1aec
translation: machine
translated_at: '2026-10-24'
---
# Liefersemantik {#delivery-semantics}

Kafka unterstützt drei Liefersemantiken: at-most-once, at-least-once und exactly-once. Jede hat spezifische Konfigurationsanforderungen und Abwägungen auf Producer- und Consumer-Seite.

## Wichtige Fakten {#key-facts}

- **At-most-once**: Nachrichten können verloren gehen, werden aber nie dupliziert; `acks=0` oder Auto-Commit vor der Verarbeitung; geeignet für Metriken, Logs und Analytics, bei denen Verluste akzeptabel sind
- **At-least-once**: Nachrichten können dupliziert werden, gehen aber nie verloren; `acks=all` + `retries>0` + manuelles Commit nach der Verarbeitung; das häufigste Setup in Produktionsumgebungen
- **Exactly-once**: Jede Nachricht wird trotz Fehlern genau einmal verarbeitet; erfordert einen idempotenten Producer + Transaktionen ODER Deduplizierung auf Anwendungsebene
- "Exactly once" ist technisch unmöglich (Problem der zwei Generäle); praktisches Exactly-once = At-least-once + Idempotenz an jeder Grenze
- Duplikate können sowohl auf **Producer-Seite** (verlorenes ACK führt zu einem Retry) als auch auf **Consumer-Seite** (Absturz nach der Verarbeitung, aber vor dem Offset-Commit) entstehen
- Exactly-once in Kafka funktioniert NUR für das Muster: Aus Kafka lesen -> verarbeiten -> in Kafka schreiben (über [[kafka-transactions]])
- Systemübergreifendes Exactly-once (Kafka -> externe DB) erfordert Deduplizierung auf Anwendungsebene
- Striktere Semantik = mehr Overhead = geringerer Durchsatz

## Muster {#patterns}

### Konfiguration für At-Most-Once {#at-most-once-configuration}

```properties
# Producer
acks=0

# Consumer
enable.auto.commit=true
auto.commit.interval.ms=5000
```

### Konfiguration für At-Least-Once {#at-least-once-configuration}

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

### Exactly-Once (Kafka-zu-Kafka) {#exactly-once-kafka-to-kafka}

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

### Wo Duplikate entstehen {#where-duplicates-occur}

```php
Producer Side:
  Producer sends -> Broker receives + stores -> ACK lost on network
  -> Producer retries -> DUPLICATE in broker

Consumer Side:
  Consumer receives batch -> Processes messages -> Crashes before commit
  -> Restart -> Re-reads same batch -> DUPLICATE processing
```

## Fallstricke {#gotchas}

- **Auto-Commit ist die häufigste Fehlerquelle für Kafka-Einsteiger**: Der Consumer empfängt Nachrichten, der Auto-Commit wird ausgelöst, und der Consumer stürzt während der Verarbeitung ab. Beim Neustart betrachtet Kafka die Nachrichten als verarbeitet und liefert den nächsten Batch. Verlorene Nachrichten sind endgültig weg.
- **Der idempotente Producer verhindert nur Duplikate durch Retries auf Bibliotheksebene**: Fängt der Anwendungscode einen Fehler ab und ruft `produce()` erneut auf, erhält die Nachricht eine neue Sequenznummer, und der Broker behandelt sie als neue Nachricht.
- **`isolation.level` ist standardmäßig `read_uncommitted`**: Transaktionen haben keine Wirkung, solange der Consumer nicht explizit `isolation.level=read_committed` setzt.
- **Exactly-once gilt NICHT für externe Systeme**: Datenbankschreibzugriffe, HTTP-Aufrufe oder clusterübergreifende Operationen liegen außerhalb der Garantien für Transaktionen in Kafka.

## Siehe auch {#see-also}

- [[kafka-transactions]] - transaktionale Producer-API für Exactly-once innerhalb von Kafka
- [[idempotent-producer]] - PID- und Sequenznummer-basierter Deduplizierungsmechanismus
- [[consumer-groups]] - Offset-Verwaltung und Commit-Strategien
- [[transactional-outbox]] - Muster für Exactly-once mit externen Datenbanken
- [KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
