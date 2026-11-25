---
title: "Idempotenter Producer"
category: concepts
tags: [kafka, producer, idempotent, deduplication, ordering, exactly-once]
level: 3
source_sha256: c4f092912e5735c2bf2acb6e34a0521c5bc44a95d569e61e1380fdf602191ad1
translation: machine
translated_at: '2026-10-24'
---
# Idempotenter Producer {#idempotent-producer}

Der idempotente Producer weist jeder Nachricht eine PID (Producer ID) und Sequenznummern zu. Dadurch kann der Broker Wiederholungsversuche innerhalb einer Producer-Session mit vernachlässigbarem Overhead deduplizieren.

## Wichtige Fakten {#key-facts}

- Jeder Producer erhält beim Initialisieren vom Broker eine **PID** (Producer ID) zugewiesen
- Jede Nachricht erhält innerhalb ihrer Epoche pro Partition eine monoton steigende **Sequenznummer**
- Der Broker erkennt doppelte `(PID, sequence_number)`-Paare und lehnt sie ab
- Der Overhead ist minimal: nur wenige zusätzliche Bytes pro Nachricht (vernachlässigbarer Performance-Einfluss)
- **Seit Kafka 3.0.0 automatisch aktiviert**, wenn alle der folgenden Bedingungen erfüllt sind: `max.in.flight.requests.per.connection` <= 5, `retries` > 0, `acks=all`
- Wenn `enable.idempotence=true` explizit gesetzt wird, die Bedingungen aber nicht erfüllt sind, wirft der `KafkaProducer`-Konstruktor eine Exception
- Geltungsbereich: pro Partition und pro Producer-Session; der Broker speichert die letzten 5 Sequenznummern pro PID und Partition
- **Zusatznutzen**: Bei aktivierter Idempotenz garantiert Kafka die korrekte Reihenfolge, auch wenn Nachrichten durch Wiederholungsversuche außer der Reihe ankommen
- Ohne Idempotenz und mit `max.in.flight > 1` kann ein Retry von Batch N nach dem erfolgreichen Schreiben von Batch N+1 eintreffen, was zu einer Schreibreihenfolge führt, die nicht der Sendereihenfolge entspricht

## Muster {#patterns}

### Konfiguration {#configuration}

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

### Mechanismus der Reihenfolgegarantie {#ordering-guarantee-mechanism}

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

## Stolperfallen {#gotchas}

- **Schützt NICHT vor Wiederholungen auf Anwendungsebene**: Fängt der Anwendungscode einen Fehler ab und ruft `produce()` erneut auf, erhält die Nachricht eine neue Sequenznummer. Der Broker behandelt sie als neue Nachricht, nicht als Duplikat.
- **Session-Grenze**: Startet der Producer neu, erhält er eine neue PID. Noch ausstehende Wiederholungsversuche alter Sessions können nicht gegen die neue PID dedupliziert werden. Für Exactly-once über Sessions hinweg sind [[kafka-transactions]] mit `transactional.id` zu verwenden.
- **Die Sequenznummern-Erzeugung kann nicht überschrieben werden**: Es gibt keine API, um Sequenznummern manuell zu setzen.
- **`max.in.flight.requests.per.connection > 5` mit Idempotenz** führt zu einer ConfigException. Der Broker kann pro PID und Partition höchstens 5 in-flight Batches verfolgen.

## Siehe auch {#see-also}

- [[kafka-transactions]] - erweitert den idempotenten Producer um atomare Schreibvorgänge über mehrere Partitionen
- [[delivery-semantics]] - wie der idempotente Producer in die Exactly-once-Garantien eingeordnet ist
- [[kafka-producer-fundamentals]] - gesamte Producer-Pipeline, Batching, Komprimierung, Fehlerbehandlung
- [KIP-98: Exactly Once Delivery](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
