---
title: "Consumer Groups"
category: concepts
tags: [kafka, consumer, group, rebalancing, heartbeat, partition-assignment, static-membership]
level: 4
source_sha256: a8b274145e723ce1bf8ce34e4c90f32fce90e9979643464bea0ca8f01b0c80e8
translation: machine
translated_at: '2026-10-24'
---
# Consumer Groups {#consumer-groups}

Eine Consumer-Gruppe ist eine benannte Einheit, die es mehreren Consumern ermöglicht, gemeinsam aus Topic-Partitionen zu lesen. Dabei ist jede Partition genau einem Consumer innerhalb der Gruppe zugewiesen. So entstehen sowohl Parallelität als auch Fehlertoleranz.

## Key Facts {#key-facts}

- Consumer treten einer Gruppe über den Parameter `group.id` bei - er muss pro logischer Consumer-Gruppe eindeutig sein
- Innerhalb einer Gruppe kann **eine Partition nur von einem Consumer gelesen werden** (ein Consumer kann aber mehrere Partitionen lesen)
- Wenn es mehr Consumer als Partitionen gibt, sind die überzähligen Consumer untätig (es gibt keine Arbeit für sie)
- Mehrere Consumer-Gruppen KÖNNEN dieselbe Partition unabhängig voneinander lesen (jede Gruppe verfolgt ihre eigenen [[offsets-and-commits]])
- Das ist ein echter Vorteil: Ein Topic zehnmal zu lesen erfordert 10 Consumer-Gruppen (10 x 8 Bytes pro Partition), nicht 10 Kopien der Daten
- Ein Consumer kann über `consumer.subscribe(List<String>)` mehrere Topics abonnieren
- Es gibt keine harte Obergrenze für Consumer-Gruppen (theoretisch ~2 Milliarden); das Topic `__consumer_offsets` (standardmäßig 50 Partitionen) wird bei Tausenden von Gruppen langsamer
- Der erste Consumer, der sich verbindet, wird zum **Gruppen-Leader** und führt beim Rebalancing die Neuverteilung der Partitionen durch
- Timeout der Consumer-Gruppe: Wenn ein Consumer zu lange inaktiv ist, kann Kafka seine Offsets löschen (`offsets.retention.minutes`, Standard 7 Tage)
- Kafka arbeitet **pull-basiert**: Consumer fragen Kafka ab (poll); Kafka pusht nicht (anders als RabbitMQ)

## Patterns {#patterns}

### Basic Consumer (Java) {#basic-consumer-java}

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false");
props.put("auto.offset.reset", "earliest");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("topic1", "topic2"));

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        consumer.commitSync();
    }
} finally {
    consumer.close();  // ALWAYS close consumer
}
```

### Basic Consumer (Python) {#basic-consumer-python}

```python
from confluent_kafka import Consumer

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
consumer = Consumer(conf)
consumer.subscribe(["topic1", "topic2"])

try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        process_message(msg)
        consumer.commit(msg)
finally:
    consumer.close()
```

### Partition Assignment Strategies {#partition-assignment-strategies}

| Strategie | Anwendungsfall | Verhalten |
|----------|----------|----------|
| **RangeAssignor** (Standard) | Co-partitionierte Topics | Weist pro Topic zusammenhängende Partitionen zu; kann unausgewogen sein |
| **RoundRobinAssignor** | Faire Verteilung | Verteilt alle Partitionen gleichmäßig im Wechsel |
| **StickyAssignor** | Zustandsbehaftete Consumer | Behält bestehende Zuweisungen beim Rebalancing bei |
| **CooperativeStickyAssignor** | Aktueller Standard (empfohlen) | Inkrementelles Rebalancing, kein Stop-the-World |

```java
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

**Co-partitionierte Topics**: zwei Topics mit gleicher Partitionsanzahl, gleicher Partitionierungsstrategie und gleichen Schlüsseln. Mit dem RangeAssignor landen Daten mit demselben Schlüssel aus beiden Topics beim selben Consumer - so werden Joins ohne prozessübergreifende Kommunikation möglich.

### Consumer Configuration Reference {#consumer-configuration-reference}

| Parameter | Standard | Beschreibung |
|-----------|---------|-------------|
| `bootstrap.servers` | erforderlich | Broker-Adressen (durch Kommas getrennt) |
| `group.id` | erforderlich | Bezeichner der Consumer-Gruppe |
| `key.deserializer` | erforderlich | Deserialisierungsklasse für Schlüssel |
| `value.deserializer` | erforderlich | Deserialisierungsklasse für Werte |
| `enable.auto.commit` | `true` | Automatisches Committen der Offsets (in Produktion deaktivieren) |
| `auto.commit.interval.ms` | `5000` | Häufigkeit des automatischen Commits |
| `auto.offset.reset` | `latest` | Verhalten, wenn kein gespeicherter Offset vorhanden ist |
| `max.partition.fetch.bytes` | `1048576` (1 MB) | Maximale Datenmenge pro Partition und Poll |
| `max.poll.records` | `500` | Maximale Anzahl Nachrichten pro Poll über alle Partitionen |
| `fetch.min.bytes` | `1` | Minimale Datenmenge, bevor poll zurückkehrt |
| `fetch.max.wait.ms` | `500` | Maximale Wartezeit, falls min.bytes nicht erreicht wird |
| `heartbeat.interval.ms` | `3000` | Häufigkeit der Heartbeats |
| `session.timeout.ms` | `10000` | Session-Timeout, bevor der Consumer als tot gilt |
| `max.poll.interval.ms` | `300000` | Maximale Zeit zwischen zwei Polls |

### Static Group Membership {#static-group-membership}

```java
props.put("group.instance.id", "consumer-instance-1");
// No rebalance on temporary disconnect
// Risk: partition unread until restart
```

## Gotchas {#gotchas}

- **Rebalancing-Sturm** - Consumer stoppen und starten das Lesen wiederholt; Ursachen: Verarbeitung dauert länger als `session.timeout.ms`, langsamer Start, häufige Deployments; Abhilfe: Timeouts erhöhen, CooperativeStickyAssignor verwenden
- **Alle Consumer müssen dieselbe Zuweisungsstrategie verwenden** - Abweichungen lösen ein globales Rebalancing aus
- **Pausierte Consumer lösen KEIN Rebalancing aus** - `.pause()` hält die Heartbeats aktiv
- **Das Subscription eines Consumers ist pro subscribe-Aufruf festgelegt** - ein erneuter Aufruf von `subscribe()` ersetzt das vorherige Abonnement
- **Überzählige Consumer sind untätig** - mehr Consumer als Partitionen bedeutet verschwendete Ressourcen; die Partitionsanzahl frühzeitig planen (Faustregel: 4 Partitionen pro Consumer)

## See Also {#see-also}

- [[offsets-and-commits]] - Offset-Verfolgung, Gefahren des automatischen Commits, Muster für manuelles Committen
- [[rebalancing-deep-dive]] - Heartbeat-Tuning, kooperatives Rebalancing, statische Mitgliedschaft
- [[topics-and-partitions]] - Dimensionierung der Partitionsanzahl und schlüsselbasiertes Routing
- [[consumer-configuration]] - vollständige Referenz der Consumer-Konfiguration
- [Apache Kafka Consumer Configuration](https://kafka.apache.org/documentation/#consumerconfigs)
