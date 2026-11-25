---
title: "RabbitMQ-Architektur"
category: reference
tags: [rabbitmq, message-queue, exchange, routing, amqp]
level: 4
source_sha256: 0c7fb5d9c02d345f88fb3511ee8c4818c53c7c4298d0ff12b63526ddf6a49ee9
translation: machine
translated_at: '2026-10-24'
---
# RabbitMQ-Architektur {#rabbitmq-architecture}

RabbitMQ ist ein Message Broker, der auf dem Queue-Modell basiert. Muster „Smarter Broker – einfacher Consumer“: Die Zustellungslogik liegt auf Broker-Seite. Standardmäßig wird das Push-Modell verwendet.

## Nachrichtenfluss {#message-flow}

```php
Producer -> Exchange -> [Binding + Routing Key] -> Queue -> Consumer
```

**Producer schreiben niemals direkt in Queues.** Der Exchange empfängt alle Nachrichten und leitet sie weiter.

## Exchange-Typen {#exchange-types}

| Typ | Routing-Logik | Geschwindigkeit | Anwendungsfall |
|------|--------------|-------|----------|
| **Fanout** | Broadcast an ALLE gebundenen Queues | Am schnellsten | Einzelne Queue, Broadcast |
| **Direct** | Exakte Übereinstimmung des Routing Keys | Schnell | Einfaches Routing (am häufigsten) |
| **Topic** | Wildcard-Routing-Key (`*` = ein Wort, `#` = beliebig) | Langsamer | Komplexe Geschäftslogik |
| **Headers** | Header-Abgleich (`x-match=all` oder `any`) | Am langsamsten | Mehrere Abgleichskriterien |

**Auswahlhilfe:**
1. Mehr als eine Queue? Nein -> Fanout
2. Mehr als 1000 Nachr./Sek. nötig? Ja -> nur Direct oder Fanout
3. Muss die Nachricht in genau eine Queue gehen? Ja -> Direct

**Topic-Beispiele:** `asia.china.done` passt auf `#.done`, `asia.*.done` und `asia.china.*`

## Queue-Typen {#queue-types}

| Typ | Verhalten | Anwendungsfall |
|------|----------|----------|
| **Classic** | Standard-FIFO, ein Consumer pro Nachricht | Am häufigsten |
| **Quorum** | Verteilte Replikation für Fehlertoleranz | Produktive Zuverlässigkeit |
| **Stream** | Kafka-ähnlich, behält Daten, mehrere Consumer | Hohes Volumen, Replay |

## Nachrichtenstruktur {#message-structure}

| Feld | Zweck |
|-------|---------|
| `Payload` | Nachrichtenkörper (Ihre Daten) |
| `Routing Key` | Bestimmt das Routing über das Binding |
| `delivery_mode` | 1 = nur im Speicher, 2 = auf Festplatte persistieren |
| `mandatory` | An Producer zurückgeben, wenn kein Binding passt |
| `expiration` | TTL der Nachricht |
| `confirm` | Zustellbestätigung anfordern |

## Persistenz {#persistence}

Nachrichten gehen bei einem Absturz verloren, es sei denn:
1. Das Flag `durable` der Queue ist aktiviert **UND**
2. der Producer sendet mit `delivery_mode = 2`

Beides ist erforderlich. Fehlt eines davon, erfolgt nur eine Speicherung im Arbeitsspeicher.

## Zustellungsgarantien {#delivery-guarantees}

### Consumer-Seite (Ack/Nack) {#consumer-side-acknack}
- **Ack** – erfolgreiche Verarbeitung, Nachricht wird aus der Queue entfernt
- **Nack** – Verarbeitungsfehler, Nachricht kehrt in die Queue zurück (auch bei Verbindungsabbruch)
- **AutoAck** – Broker bestätigt beim Senden automatisch (at-most-once, am schnellsten)

**Prefetch Count** steuert die Anzahl unbestätigter Nachrichten pro Consumer. `prefetch_count=1` bedeutet strikt eine Nachricht nach der anderen.

### Producer-Seite {#producer-side}
Derselbe Ack/Nack-Mechanismus. Der Parameter `confirm` aktiviert die vollständige Zustellverfolgung. `mandatory` gibt nicht zustellbare Nachrichten zurück.

### Risiko von Duplikaten {#duplicate-risk}
Der Consumer verarbeitet die Nachricht, das Ack erreicht den Broker jedoch nicht (Netzwerk). Die Nachricht wird erneut zugestellt. Für Exactly-once-Semantik sind idempotente Consumer erforderlich.

## Dead Letter Exchange (DLE) {#dead-letter-exchange-dle}

Fehlgeschlagene Nachrichten werden an den DLE weitergeleitet, statt verloren zu gehen. Kombinieren Sie dies mit automatischem Retry nach einem Timeout und Fehlerprotokollierung.

## Hochverfügbarkeit {#high-availability}

- Mehrere Instanzen hinter einem Load Balancer
- Quorum Queues für Fehlertoleranz
- Cluster-Konfiguration für den produktiven Betrieb

## Designbeispiel {#design-example}

```php
task_queue (Direct)           -> task processing
status_update_queue (Topic)   -> status tracking (*.completed, *.failed)
notification_queue (Fanout)   -> broadcast notifications
priority_queue (Direct)       -> urgent tasks
audit_queue (Direct)          -> compliance logging

Each queue has: Dead Letter Exchange, Quorum Queue, automatic retry
```

## Fallstricke {#gotchas}

- **Standardmäßig keine Festplattenpersistenz** – Nachrichten gehen bei einem Absturz verloren ohne explizites `durable` + `delivery_mode=2`
- **Fanout ignoriert den Routing Key** – Binding-Einstellungen haben keine Wirkung, alle gebundenen Queues erhalten alles
- **Prefetch=0** bedeutet unbegrenzt – der Broker sendet sofort alle Nachrichten und kann den Consumer überlasten
- **Queue-Namen** sind innerhalb eines vhost global eindeutig – in Umgebungen mit mehreren Teams sind Kollisionen möglich
- **Nicht für massive Datenströme geeignet** – für Event-Streaming mit hohem Volumen Kafka verwenden

## Siehe auch {#see-also}

- [[kafka-architecture]] – Log-basierte Alternative für Streaming mit hohem Volumen
- [[message-broker-patterns]] – Auswahl zwischen Brokern, Zustellungsgarantien
- [[microservices-communication]] – Muster der Service-Kommunikation
