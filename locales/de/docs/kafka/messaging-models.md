---
title: "Messaging-Modelle"
category: concepts
tags: [kafka, messaging, queue, pub-sub, log, architecture]
level: 2
source_sha256: 16f2e8e14ebf0526aa0f82736b191bab3ed11b7a10548cac3c89eef56e633f1d
translation: machine
translated_at: '2026-10-24'
---
# Messaging-Modelle {#messaging-models}

In verteilten Systemen gibt es drei grundlegende Messaging-Modelle. Kafka verwendet das log-basierte Modell, das sowohl Queue- als auch Pub-Sub-Muster abdeckt.

## Kernfakten {#key-facts}

- **Queue-Modell (Competing Consumers)**: Nachrichten gehen in eine Queue, jede Nachricht wird von genau einem Consumer empfangen; konsumierte Nachrichten werden entfernt; verwendet für Task-Verteilung und Lastverteilung
- **Pub-Sub-Modell (Fan-Out)**: Nachrichten werden an ein Topic veröffentlicht, jeder Subscriber erhält eine Kopie; verwendet für Event-Benachrichtigungen, bei denen mehrere Systeme dieselben Daten benötigen
- **Log-basiertes Modell (Kafka)**: Nachrichten werden an ein unveränderliches, geordnetes Log angehängt; Consumer verwalten ihren eigenen Offset (Position); Nachrichten werden nach Zeit- oder Größenrichtlinie aufbewahrt, nicht nach Konsum
- Das log-basierte Modell ermöglicht: mehrere unabhängige [[consumer-groups]], die in ihrem eigenen Tempo lesen, Replay durch Zurücksetzen des Offsets, kein Nachrichtenverlust bei Ausfall eines Consumers
- Klassische Queues (RabbitMQ, ActiveMQ, SQS) konzentrieren sich auf Nachrichtenzustellung und Task-Verteilung; log-basiertes Streaming (Kafka, Pulsar, Redpanda) konzentriert sich auf Event-Speicherung und Stream-Verarbeitung
- Kafka ist KEIN Message Broker, sondern ein verteiltes Commit-Log (Write-Ahead-Log)
- Wesentlicher Unterschied zu klassischen Queues: Das Lesen eines Topics zehnmal erfordert zehn Consumer-Groups (10 x 8 Bytes Overhead pro Partition), nicht zehn Kopien der Daten

## Muster {#patterns}

| Eigenschaft | Klassische Queue | Log-basiertes Streaming |
|-------------|------------------|-------------------------|
| Lebenszyklus der Nachricht | Nach dem Konsum gelöscht | Nach Richtlinie aufbewahrt |
| Reihenfolge | Pro Queue (oder keine) | Pro Partition garantiert |
| Replay | Nicht möglich | Möglich (Offset zurücksetzen) |
| Consumer-Groups | Competing Consumers | Unabhängige Consumer-Groups |
| Durchsatz | Moderat | Sehr hoch (sequentielles I/O) |
| Anwendungsfall | Task-Verteilung | Event Sourcing, Analytics, CDC |

### Kommunikationsmuster {#communication-patterns}

| Muster | Notation | Beschreibung |
|--------|----------|--------------|
| Put/Take | 1 -> 1 | Eins-zu-eins, einzelner Consumer |
| Publish/Subscribe | 1 -> * | Eins-zu-viele, alle Subscriber empfangen |
| Request/Response | 1 <-> 1 | Synchron, bidirektional |

### Protokolle {#protocols}

AMQP, MQTT, STOMP, NATS, ZeroMQ, Kafkas eigenes binäres Protokoll.

## Fallstricke {#gotchas}

- **„Kafka ist nur ein weiterer Message Broker“** ist falsch. Kafkas log-basierte Architektur unterscheidet sich grundlegend von queue-basierten Brokern; Nachrichten werden unabhängig vom Konsum immer persistiert.
- **Queue-Modelle können nicht wiederholen (replay)**. Sobald eine Nachricht konsumiert und bestätigt wurde, ist sie weg. Das ist ein grundlegender architektonischer Unterschied und keine Konfigurationsoption.
- **Pub-Sub ohne Aufbewahrung** bedeutet, dass der Consumer zum Zeitpunkt der Veröffentlichung online sein muss. Kafka löst dieses Problem, indem Nachrichten für einen konfigurierbaren Zeitraum aufbewahrt werden.

## Siehe auch {#see-also}

- [[delivery-semantics]] - At-most-once-, At-least-once- und Exactly-once-Garantien
- [[consumer-groups]] - wie Kafka sowohl Queue- als auch Pub-Sub-Muster über Consumer-Groups umsetzt
- [[broker-architecture]] - wie Kafka Nachrichten speichert und bereitstellt
- [Apache Kafka Design: Motivation](https://kafka.apache.org/documentation/#design_motivation)
