---
title: "Consumer-Konfiguration"
category: reference
tags: [kafka, consumer, configuration, fetch, polling, timeout]
level: 3
source_sha256: 213de6862339098c62ff67ea2397b13e0beb4cea646fc2deab449b9a696a7c89
translation: machine
translated_at: '2026-10-24'
---
# Consumer-Konfiguration {#consumer-configuration}

Vollständige Referenz der Konfigurationsparameter für Kafka-Consumer mit Standardwerten, Tuning-Empfehlungen und Auswirkungen auf das Verhalten.

## Wichtige Fakten {#key-facts}

- Der Consumer arbeitet pull-basiert: Er ruft `poll()` auf, um Daten von den Brokern abzurufen; Kafka pusht keine Daten
- `fetch.max.wait.ms` steuert die maximale Wartezeit während `poll()`; alles, was in diesem Zeitfenster eintrifft, wird zurückgegeben
- `fetch.min.bytes` legt die minimale Datenmenge fest, bevor zurückgegeben wird; Kafka wartet, bis diese Menge verfügbar ist ODER `fetch.max.wait.ms` abläuft
- Kafka liefert niemals partielle Nachrichten, immer vollständige Records
- `max.poll.records` (Standard 500) begrenzt die Anzahl der Nachrichten pro Poll über alle Partitionen hinweg
- Drei Python-Kafka-Clients: confluent-kafka-python (librdkafka-Wrapper, Produktion), kafka-python (reines Python), kafka-go für Go

## Muster {#patterns}

### Durchsatzoptimierter Consumer {#throughput-optimized-consumer}

```properties
fetch.min.bytes=1048576        # 1MB - wait for larger batches
fetch.max.wait.ms=500          # wait up to 500ms
max.poll.records=1000          # larger batches per poll
max.partition.fetch.bytes=2097152  # 2MB per partition
```

### Latenzoptimierter Consumer {#latency-optimized-consumer}

```properties
fetch.min.bytes=1              # return as soon as any data available
fetch.max.wait.ms=100          # short wait
max.poll.records=100           # smaller batches, faster processing
```

### Consumer für lange Verarbeitung {#long-processing-consumer}

```properties
max.poll.interval.ms=600000    # 10 min between polls
max.poll.records=50            # smaller batches
session.timeout.ms=45000       # longer session
heartbeat.interval.ms=15000    # 1/3 of session timeout
```

### Consumer-Group-Operationen über die Admin-API {#consumer-group-operations-via-admin-api}

```java
Admin admin = Admin.create(Map.of("bootstrap.servers", "localhost:9092"));

admin.listConsumerGroups();
admin.describeConsumerGroups(List.of("group-id"));
admin.listConsumerGroupOffsets("group-id");
admin.alterConsumerGroupOffsets("group-id", offsetMap);
admin.deleteConsumerGroupOffsets("group-id", partitions);
```

## Fallstricke {#gotchas}

- **`enable.auto.commit=true` ist der Standard**: Das ist die häufigste Ursache für Datenverlust bei Einsteigern; für jeden Produktionsbetrieb deaktivieren
- **`auto.commit.interval.ms` muss kleiner sein als `session.timeout.ms`**: Andernfalls wird der Consumer als tot erklärt, bevor der Commit ausgeführt wird
- **Überschreitung von `max.poll.interval.ms` = Consumer wird aus der Gruppe entfernt**: auch wenn die Heartbeats in Ordnung sind; tritt bei lang laufender Verarbeitung auf
- **Es gibt drei Go-Clients mit unterschiedlichen APIs**: kafka-go (reines Go, Kontexte), confluent-kafka-go (librdkafka-Wrapper, Java-ähnlich) und weitere; die Wahl richtet sich nach den Präferenzen des Teams

## Siehe auch {#see-also}

- [[consumer-groups]] - Gruppenmechanik, Zuweisungsstrategien
- [[offsets-and-commits]] - Strategien zur Offset-Verwaltung
- [[rebalancing-deep-dive]] - Heartbeat-Tuning, kooperatives Rebalancing
- [Apache Kafka Consumer-Konfigurationen](https://kafka.apache.org/documentation/#consumerconfigs)
