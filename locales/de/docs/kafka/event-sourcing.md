---
title: "Event Sourcing"
category: patterns
tags: [kafka, event-sourcing, immutable-log, replay, audit, state-reconstruction]
level: 3
source_sha256: 351b3cdce2c65ab28fce9ebda1a0602a963b8f3904e8eddd9feb94a308d0dca2
translation: machine
translated_at: '2026-10-24'
---
# Event Sourcing {#event-sourcing}

Event Sourcing speichert jede Zustandsänderung als unveränderliches Ereignis in Kafka, anstatt den aktuellen Zustand in einer Datenbank zu überschreiben. Dadurch werden vollständige Historie-Replays, Audit-Trails und die Rekonstruktion des Zustands zu jedem beliebigen Zeitpunkt möglich.

## Wichtige Fakten {#key-facts}

- Das unveränderliche, nur anhängbare Log von Kafka passt natürlich zu Event Sourcing
- Alle Ereignisse werden als unveränderliche Fakten erfasst; der Zustand wird durch Replay der Ereignisse abgeleitet
- Der aktuelle Zustand wird durch Replay der Ereignisse ab einem beliebigen Offset rekonstruiert
- Die Log-Retention von Kafka stellt eine vollständige Ereignishistorie für Audits und Compliance sicher
- Mehrere [[consumer-groups]] können denselben Ereignisstrom unabhängig voneinander lesen, um unterschiedliche materialisierte Sichten aufzubauen
- Löst das Problem „Wie sind wir in diesen Zustand gekommen?“ – wenn nur der aktuelle Zustand in der DB liegt, lässt sich die Historie nicht nachvollziehen
- Das Schreiben aller Ereignisse in ein klassisches RDBMS stößt bei etwa 10.000 Schreibvorgängen pro Sekunde an seine Grenzen; Kafka verarbeitet Millionen
- Für materialisierte Sichten spezialisierte Read-Stores verwenden (ElasticSearch, Redis, Cassandra)
- Für eine unbegrenzte Speicherung von Ereignissen ist ein dedizierter Event Store (EventStoreDB, MongoDB) besser geeignet als Kafka, das standardmäßig löscht

## Muster {#patterns}

### Event-Sourcing-Architektur {#event-sourcing-architecture}

```bash
Events -> Kafka Topic (append-only log, source of truth)
    -> Materializer A -> Read Store A (current state for API)
    -> Materializer B -> Read Store B (analytics, full-text search)
    -> Materializer C -> Read Store C (notifications, ML fraud detection)
    -> Technical Support -> Full event history for debugging
```

### Event-Replay {#event-replay}

```sql
POST /api/replay-events
1. Command API reads all events from Event Store
2. Sends marker event "replay started"
3. Query API clears its read model
4. Query API re-applies all events to rebuild from scratch
```

Anwendungsfälle: Schema-Migration, Fehlerbehebung in Event-Handlern, Hinzufügen neuer Projektionen, Disaster Recovery. Während eines Replays werden eingehende Commands blockiert, bis der Vorgang abgeschlossen ist.

### Kafka als Actor-System {#kafka-as-actor-system}

Jeder Consumer, der eine Partition verarbeitet, verhält sich wie ein Actor:
- Empfängt Nachrichten sequenziell
- Verwaltet Zustand
- Kann Nachrichten in andere Topics schreiben
- Partitionen erzwingen die sequenzielle Verarbeitung auf natürliche Weise

## Fallstricke {#gotchas}

- **Kafka löscht Ereignisse standardmäßig irgendwann** – für eine dauerhafte Speicherung von Ereignissen einen dedizierten Event Store neben Kafka verwenden oder eine unbegrenzte Retention konfigurieren
- **Die Weiterentwicklung von Event-Schemata ist kritisch** – das Hinzufügen oder Entfernen von Feldern in Ereignissen bricht das Replay; [[schema-registry]] mit FULL-Kompatibilität verwenden
- **Replays können teuer sein** – Millionen von Ereignissen brauchen Zeit für das Replay; Snapshotting in Erwägung ziehen: den aktuellen Zustand periodisch speichern und nur ab dem letzten Snapshot neu abspielen
- **Reihenfolge nur innerhalb einer Partition** – zusammengehörige Ereignisse müssen denselben Partitionsschlüssel teilen; Reihenfolge über Partitionen hinweg erfordert zusätzliche Koordination

## Siehe auch {#see-also}

- [[cqrs-pattern]] – Command Query Responsibility Segregation, natürlicher Partner von Event Sourcing
- [[kafka-streams]] – Stream-Verarbeitung zum Aufbau materialisierter Sichten
- [[topics-and-partitions]] – Log Compaction für Tabellen mit „aktuellem Zustand pro Schlüssel“
- [[delivery-semantics]] – Exactly-once für die Verarbeitung von Ereignissen
