---
title: "Muster für Message Broker"
category: concepts
tags: [messaging, pub-sub, queue, delivery-guarantees, message-broker]
level: 3
source_sha256: 446263f6471370ec370ef9d5362c29893118f99e0ecdf7995ce8c4db9ef6c40e
translation: machine
translated_at: '2026-10-24'
---
# Message Broker Patterns {#message-broker-patterns}

Message Broker entkoppeln Services (Abhängigkeiten werden auf das Nachrichtenformat reduziert) und ermöglichen asynchrone Verarbeitung (der Producer sendet und arbeitet weiter, der Consumer verarbeitet in seinem eigenen Tempo).

## Zwei grundlegende Muster {#two-fundamental-patterns}

### Publish-Subscribe (Pub-Sub) {#publish-subscribe-pub-sub}
Der Producer veröffentlicht in ein Topic. **Alle Subscriber** erhalten eine Kopie. Nachrichten werden broadcastet.

- Geeignet für: Event-Benachrichtigungen ("Bestellung erstellt" wird gleichzeitig von Versand, Analytics und Benachrichtigungen konsumiert)
- Problem: Jeder Consumer erhält jede Nachricht - keine eingebaute Verteilung der Arbeit

### Message Queue (Point-to-Point) {#message-queue-point-to-point}
Der Producer sendet an eine Queue. **Nur ein Consumer** empfängt jede Nachricht. Nach dem Konsumieren ist sie für andere verschwunden.

- Geeignet für: Arbeitsverteilung über **konkurrierende Consumer** - 10 Consumer auf einer Queue = 10-facher Durchsatz
- Wichtigster Vorteil: garantierte Einmalverarbeitung

### Auswahl zwischen beiden {#choosing-between-them}

| Frage | Pub-Sub | Queue |
|-------|---------|-------|
| Wie viele Consumer pro Nachricht? | Mehrere | Einer |
| Sollen alle Consumer jede Nachricht sehen? | Ja | Nein |
| Garantierte Einmalverarbeitung nötig? | Nein | Ja |
| Arbeitsverteilung / Lastverteilung nötig? | Nein | Ja |

**Trend:** Pub-Sub und Log-Modelle (Kafka) werden zunehmend üblich. Viele Broker unterstützen beide Muster.

## Push vs. Pull {#push-vs-pull}

| Modell | Broker | Steuerung durch Consumer | Latenz | Beispiel |
|--------|--------|--------------------------|--------|----------|
| **Push** | Sendet sofort | Muss die eingehende Rate verarbeiten | Niedrig | RabbitMQ-Standard |
| **Pull** | Wartet auf Anfrage | Steuert Tempo und Position | Variabel | Kafka |

Push kann langsame Consumer überlasten (Prefetch-Count verwenden). Pull fügt Verzögerung hinzu, wenn selten gepollt wird.

## Zustellungsgarantien {#delivery-guarantees}

| Stufe | Verhalten | Abwägung |
|-------|-----------|----------|
| **At most once** | Fire and forget | Am schnellsten, Nachrichten können verloren gehen |
| **At least once** | Mindestens einmal zugestellt, Duplikate möglich | Am häufigsten, Consumer muss idempotent sein |
| **Exactly once** | Genau einmal zugestellt | Am teuersten, oft = At-least-once + idempotenter Consumer |

## Broker-Architektur {#broker-architecture}

### Federation {#federation}
Mehrere unabhängige Broker sind miteinander verbunden. Geografische Verteilung, lose Kopplung, isolierte Ausfalldomänen.

### Clustering {#clustering}
Eng gekoppelte Broker, die Zustand teilen. Hohe Verfügbarkeit, automatisches Failover. Komplexere Netzwerkkonfiguration.

## Die Wahl eines Brokers {#choosing-a-broker}

| Kriterium | Kafka | RabbitMQ |
|-----------|-------|----------|
| Datenvolumen | Hoch (100K+ Nachrichten/Sek.) | Moderat |
| Aufbewahrung | Nach dem Konsumieren gespeichert | Nach dem Konsumieren gelöscht |
| Reihenfolge | Pro Partition | Pro Queue (FIFO) |
| Consumer-Modell | Pull | Push |
| Routing | Einfach (Topic/Partition) | Flexibel (Exchanges) |
| Replay | Ja (beliebiger Offset) | Nein |
| Anwendungsfall | Event-Streaming, Big Data | Task-Queues, Request-Response |

**Entscheidungsrahmen:**
1. Hohes Volumen -> Kafka
2. Zuverlässige Zustellung kleiner Volumina -> RabbitMQ
3. Flexibles Routing nötig (Exchanges, Topics, Header) -> RabbitMQ
4. Log-Replay / Event Sourcing nötig -> Kafka
5. Strikte globale Reihenfolge -> einzelne Kafka-Partition

## Fallstricke {#gotchas}

- **Konkurrierende Consumer mit Pub-Sub** - 3 Consumer, die jeweils jede Nachricht verarbeiten, ergeben 3-fache Duplikate. Consumer-Gruppen (Kafka) oder das Queue-Modell verwenden
- **At-least-once ohne Idempotenz** - Consumer verarbeitet Nachricht, das Ack geht durch einen Netzwerkfehler verloren, Nachricht wird erneut zugestellt und erneut verarbeitet
- **Broker als Datenbank** - Broker dienen dem Nachrichtenaustausch, nicht der langfristigen Speicherung (außer Kafka mit Aufbewahrungsrichtlinien)
- **Nachrichtenreihenfolge** - nur innerhalb einer einzelnen Partition (Kafka) bzw. einer einzelnen Queue (RabbitMQ) garantiert, nicht darüber hinaus

## Siehe auch {#see-also}

- [[kafka-architecture]] - Tiefere Einblicke in Kafka
- [[rabbitmq-architecture]] - Tiefere Einblicke in RabbitMQ
- [[microservices-communication]] - Wo Broker in der Service-Architektur einzuordnen sind
- [[data-serialization-formats]] - JSON, Avro, Protobuf für Nachrichten-Payloads
- [[queueing-theory]] - Warum Systeme unter Last degradieren
