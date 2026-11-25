---
title: "Apache-Kafka-Architektur"
category: reference
tags: [kafka, event-streaming, message-broker, partitions, consumer-groups]
level: 4
source_sha256: b06a0a25e176be191e9784684f25a17014ebe87a05bad9de34f8fc5afbf9e843
translation: machine
translated_at: '2026-10-24'
---
# Apache-Kafka-Architektur {#apache-kafka-architecture}

Kafka ist ein Message Broker auf Basis des Log-(Journal-)Modells. Im Fokus stehen die Erhaltung der Nachrichtenreihenfolge, die langfristige Speicherung und hoher Durchsatz. Pull-Modell: Consumer steuern das Lesetempo.

## Architekturhierarchie {#architecture-hierarchy}

```php
Cluster -> Brokers -> Topics -> Partitions -> Messages (with offsets)
```

- **Topic** - logische Gruppierung von Partitionen. Ein Nachrichtentyp pro Topic (z. B. `page_visit`, `user_registration`, `order_placed`)
- **Partition** - physisches Log mit strikter Reihenfolge. Gehört immer zu genau einem Topic
- **Offset** - Zeiger darauf, wo ein Consumer zuletzt gelesen hat. Wird im Systemtopic `__consumer_offsets` gespeichert
- **Consumer Group** - Consumer, die einen gemeinsamen Offset teilen. Innerhalb einer Gruppe liest jede Partition genau ein Consumer
- **Broker** - Kafka-Serverinstanz. Mehrere bilden einen Cluster

## Nachrichtenfluss {#message-flow}

1. Producer sendet an das **Topic** (nicht direkt an eine Partition). Kafka wählt die Partition (Round-Robin, schlüsselbasiert oder vom Producer vorgegeben)
2. Kafka schreibt die Nachricht mit Offset in die Partition
3. **Einzelne Consumer** können jede Nachricht beliebig oft lesen (Pub-Sub)
4. **Consumer Groups** - ein Consumer pro Partition. 3 Partitionen + 2 Consumer = Consumer 1 liest Partitionen 1+2, Consumer 2 liest Partition 3. Überzählige Consumer bleiben untätig, wenn es mehr Consumer als Partitionen gibt

## Replikation und HA {#replication-and-ha}

- **Leader-Follower** pro Partition. Der Leader verarbeitet alle Lese- und Schreibzugriffe
- Follower replizieren die Daten. Bei Ausfall des Leaders wird ein Follower zum Leader befördert
- **Replikationsfaktor** typischerweise 3
- **ZooKeeper** übernimmt die Koordination (wird in neueren Versionen durch **KRaft** ersetzt)

## Zustellungsgarantien (acks) {#delivery-guarantees-acks}

| Einstellung | Garantie | Geschwindigkeit | Verhalten |
|-------------|----------|-----------------|-----------|
| `acks=0` | Höchstens einmal | Am schnellsten | Keine Bestätigung |
| `acks=1` | Mindestens einmal | Mittel | Leader bestätigt |
| `acks=all` | Stärkste Garantie | Am langsamsten | Leader und alle Replikate bestätigen |

**`min.insync.replicas`** mit `acks=all`: erlaubt Schreibvorgänge, wenn N-1 Replikate nicht verfügbar sind.

## Consumer-Garantien {#consumer-guarantees}

Verantwortung des Consumers (Pull-Modell):
- Offset **nach** der Verarbeitung committen = mindestens einmal
- Offset **vor** der Verarbeitung committen = höchstens einmal
- **Exactly-once** = Kafka-Transaktionen oder idempotente Consumer

## Datenpersistenz {#data-persistence}

- Nachrichten werden immer auf die Festplatte geschrieben
- **Aufbewahrung nach Zeit** (z. B. 7 Tage) oder **nach Größe** (z. B. 1 GB pro Partition)
- **Log Compaction** - behält den neuesten Wert pro Schlüssel
- Anders als bei RabbitMQ bleiben Nachrichten nach dem Konsumieren erhalten

## Wann Kafka einsetzen {#when-to-use-kafka}

- Event-Streaming mit hohem Volumen (100K+ Nachrichten/Sek.)
- Systeme, die Nachrichten-Replay benötigen
- Log-Aggregation aus mehreren Services
- Echtzeit-Analysen und Metrik-Pipelines
- Event-Sourcing-Architekturen
- Datenpipeline zwischen Quellsystemen und DWH

## Wann nicht {#when-not-to-use}

- Einfache Task-Queues (besser RabbitMQ)
- Request-Response-Muster
- Latenzkritische RPC-Aufrufe
- Systeme mit wenigen Nachrichten

## Stolperfallen {#gotchas}

- **Mehr Consumer als Partitionen** = untätige Consumer, die Ressourcen verschwenden
- **Einzelne Partition für Reihenfolge** begrenzt den Durchsatz - schlüsselbasierte Partitionierung verbindet Reihenfolge mit Parallelität
- **Consumer-Lag** - Offset-Lag überwachen, um langsame Consumer zu erkennen, bevor sie zu weit zurückfallen
- **Partitionsanzahl** - kann erhöht, aber nie verringert werden. Bei der Topic-Erstellung sorgfältig wählen
- **Rebalancing-Stürme** - Hinzufügen oder Entfernen von Consumern löst ein Rebalancing aus, das die Verarbeitung in der Gruppe kurzzeitig vollständig anhält

## Siehe auch {#see-also}

- [[rabbitmq-architecture]] - Queue-basierte Alternative
- [[message-broker-patterns]] - Auswahl zwischen Brokern
- [[microservices-communication]] - Event-getriebene Architektur
- [[bigdata-ml-architecture]] - Kafka in Datenpipelines
