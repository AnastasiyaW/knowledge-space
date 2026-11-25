---
title: "Apache Kafka - Liefersemantik und Consumer-Muster"
category: concepts
tags: [kafka, messaging, event-driven, consumer-groups, streaming]
level: 2
source_sha256: b7250aa01443d2fe2998a03fb8a0c9d2f301ea5da2650589cfaebfd0e5eaf8a5
translation: machine
translated_at: '2026-10-24'
---
# Apache Kafka - Liefersemantik und Consumer-Muster {#apache-kafka-delivery-semantics-and-consumer-patterns}

Liefergarantien von Kafka, Mechanik von Consumer Groups, Rebalancing-Strategien und Integrationsmuster. Der Schwerpunkt liegt auf dem praktischen Einsatz im Produktivbetrieb und nicht auf der Cluster-Administration.

## Wichtige Fakten {#key-facts}

- Drei Liefersemantiken: at-most-once, at-least-once (Standard/empfohlen), exactly-once
- At-least-once erfordert idempotente Consumer, d. h. dieselbe Nachricht, zweimal verarbeitet, liefert dasselbe Ergebnis
- KRaft-Modus (Kafka 2.8+) macht die Abhängigkeit von ZooKeeper überflüssig
- Producer senden an eine Topic-Partition: standardmäßig Round-Robin, oder über den Key-Hash, um Reihenfolge sicherzustellen
- Eine Consumer Group verteilt Partitionen auf ihre Mitglieder; Rebalancing erfolgt bei Beitritt und Austritt
- Cooperative Sticky ist seit Kafka 2.4 die bevorzugte Rebalancing-Strategie

## Muster {#patterns}

### Liefersemantik {#delivery-semantics}

**At most once** - Offset vor der Verarbeitung bestätigen:
- Schnell, Nachrichten können bei einem Absturz verloren gehen
- Einsetzbar, wenn Nachrichtenverlust akzeptabel ist (Metriken, unkritische Events)

**At least once** - erst verarbeiten, dann bestätigen:
- Standard für die meisten Anwendungsfälle
- Erfordert idempotente Consumer
- Datenbank-Unique-Constraints oder Deduplizierungstabellen verwenden

**Exactly once** - erfordert Kafka-Transaktionen und einen idempotenten Producer:
- Die Kafka Streams API erleichtert dies
- Sehr komplex bei Szenarien von Consumer zu Datenbank
- Oft einfacher umzusetzen: at-least-once mit Idempotenz-Schlüsseln

### Rebalancing von Consumer Groups {#consumer-group-rebalancing}

| Strategie | Verhalten |
|-----------|-----------|
| RoundRobin | Verteilt alle Partitionen gleichmäßig |
| Sticky | Minimiert Partitionswechsel beim Rebalancing |
| Cooperative Sticky | Inkrementelles Rebalancing; Consumer behalten ihre Partitionen, bis die neue Zuweisung bestätigt ist |

Cooperative Sticky minimiert Ausfallzeiten bei rollierenden Neustarts, da Consumer während eines laufenden Rebalancings nicht die Verarbeitung anhalten.

### Transactional Outbox {#transactional-outbox}

Problem: Datenbank aktualisieren und Kafka-Nachricht veröffentlichen, atomar.

1. Gleiche Datenbanktransaktion: Entität aktualisieren und Event in die Tabelle `outbox` einfügen
2. Ein Hintergrund-Poller liest noch nicht gesendete Outbox-Events, veröffentlicht sie in Kafka und markiert sie als gesendet
3. Consumer dedupliziert anhand von Idempotenz-Schlüsseln

Dies umgeht das Two-Phase-Commit-Problem vollständig.

### Kernkonzepte {#key-concepts}

- **Partition**: Einheit für Parallelität und Reihenfolge. Nachrichten innerhalb einer Partition sind geordnet.
- **Offset**: Position innerhalb einer Partition. Der committete Offset bedeutet: „Bis hierhin habe ich verarbeitet.“
- **Consumer Group**: Menge von Consumern, die sich Topic-Partitionen teilen. Jede Partition ist genau einem Consumer innerhalb der Gruppe zugewiesen.
- **Key-basiertes Routing**: Nachrichten mit demselben Key landen immer in derselben Partition, wodurch die Reihenfolge pro Key sichergestellt wird.

## Stolperfallen {#gotchas}

- Die Anzahl der Consumer in einer Gruppe darf die Anzahl der Partitionen nicht übersteigen, überzählige Consumer bleiben untätig
- Exactly-once ist über Kafka plus ein externes System praktisch nicht umsetzbar, ohne Idempotenz auf Consumer-Seite
- Consumer Lag (Offset-Rückstand gegenüber dem neuesten Offset) ist die wichtigste Health-Metrik für Consumer Groups
- Der KRaft-Modus vereinfacht das Deployment, erfordert aber 1–3 Controller-Knoten für die Metadatenverwaltung
- Lange Verarbeitungszeiten ohne Offset-Commit können einen Session-Timeout und ein Rebalancing auslösen

## Siehe auch {#see-also}

- [[database-patterns]] - Implementierung der Transactional Outbox in Go
- [[microservices]] - Kafka in Microservice-Architekturen
- [[observability-query-languages]] - Überwachung des Consumer Lags mit PromQL
