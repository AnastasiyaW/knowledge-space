---
title: "Transactional Outbox und Inbox"
category: patterns
tags: [kafka, outbox, inbox, cdc, debezium, exactly-once, idempotent, distributed-transactions]
level: 3
source_sha256: 84ce0c95d5d38c6a7bc7d2330039f950eb34eba247ea16a71540705768e079bb
translation: machine
translated_at: '2026-10-24'
---
# Transactional Outbox und Inbox {#transactional-outbox-and-inbox}

Das Transactional-Outbox-Muster schreibt Events in eine Outbox-Tabelle innerhalb derselben Datenbanktransaktion wie die Geschäftsdaten. Das Inbox-Muster stellt consumer-seitige Idempotenz über Unique-Constraints bereit. Zusammen ergeben sie praktisches Exactly-once über Systemgrenzen hinweg.

## Key Facts {#key-facts}

- **Problem**: Wie kann eine Datenbank atomar aktualisiert und gleichzeitig ein Event an Kafka veröffentlicht werden?
- **Outbox**: Event in derselben DB-Transaktion wie die Geschäftsdaten in die Outbox-Tabelle schreiben; ein separater Processor veröffentlicht es an Kafka
- **Inbox**: Der empfangende Service nutzt eine Inbox-Tabelle mit Unique-Constraint, um eingehende Nachrichten zu deduplizieren
- **Vollständige Garantiekette**: Outbox (at-least-once) + Queue (at-least-once) + Inbox (Idempotenz) = praktisches Exactly-once
- "Exactly once"-Zustellung ist in verteilten Systemen unmöglich (Two Generals' Problem)
- Praktisches Exactly-once = at-least-once + Idempotenz an jeder Grenze
- [[kafka-connect]] mit Debezium kann eigene Outbox-/Inbox-Processors ersetzen

## Patterns {#patterns}

### Transactional Outbox {#transactional-outbox}

```sql
-- Outbox table schema
CREATE TABLE outbox (
    id UUID PRIMARY KEY,
    aggregate_id VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Within business transaction
BEGIN;
  INSERT INTO orders (id, customer_id, amount) VALUES (...);
  INSERT INTO outbox (id, aggregate_id, event_type, payload)
    VALUES (gen_random_uuid(), order_id, 'OrderCreated', '{"amount": 99.99}');
COMMIT;
```

**Outbox Processor** (separater Service):
1. Outbox-Tabelle nach unverarbeiteten Datensätzen abfragen (Polling)
2. An Kafka veröffentlichen
3. Nach erfolgreicher Veröffentlichung als verarbeitet markieren
4. Bei Fehlern erneut versuchen (at-least-once-Zustellung)

### Transactional Inbox {#transactional-inbox}

```sql
-- Inbox table schema
CREATE TABLE inbox (
    message_id UUID PRIMARY KEY,  -- unique constraint prevents duplicates
    processed_at TIMESTAMP DEFAULT NOW()
);

-- Consumer processing
BEGIN;
  INSERT INTO inbox (message_id) VALUES (:kafka_message_id);
  -- If unique constraint violation -> already processed, skip
  UPDATE balances SET amount = amount + :delta WHERE account_id = :id;
COMMIT;
```

### Gesamtarchitektur {#complete-architecture}

```php
App/1 -> DB1 [Data + Outbox]
    -> Outbox Processor -> Kafka
    -> Inbox Processor -> DB2 [Data + Inbox] -> App/2

Guarantee chain at each boundary:
  App -> DB: single transaction (atomic)
  DB -> Kafka: at-least-once (outbox processor retries)
  Kafka -> Consumer: at-least-once (consumer acks)
  Consumer -> DB: idempotent (inbox unique constraint)
```

### CDC als Alternative zur Outbox {#cdc-as-outbox-alternative}

Anstelle einer expliziten Outbox-Tabelle werden Änderungen aus dem WAL (Write-Ahead Log) der Datenbank erfasst:

| Ansatz | Eingriffstiefe | Datenbanklast |
|--------|----------------|---------------|
| Zeitstempel/Version in Zeilen | Hoch (Schemaänderungen) | Zusätzliche Abfragen |
| Trigger auf Tabellen | Gering (für die Anwendung transparent) | Zusätzliche Operationen |
| WAL-basiertes CDC (Debezium) | **Keine** | **Keine** |

```json
// Debezium CDC connector
{
  "name": "outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.dbname": "mydb",
    "table.include.list": "public.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter"
  }
}
```

WAL-basiertes CDC bedeutet: keinerlei Eingriff in Anwendung oder Schema, keine zusätzliche Datenbanklast, und es werden alle Änderungen erfasst, auch solche von anderen Tools oder Prozessen.

## Gotchas {#gotchas}

- **Absturz des Outbox Processors = at-least-once, nicht exactly-once**: Veröffentlicht der Processor ein Event und stürzt ab, bevor er es als verarbeitet markiert, wird es nach dem Neustart erneut veröffentlicht. Das Inbox-Muster auf Consumer-Seite ist daher unverzichtbar.
- **Die Outbox-Tabelle wächst**: Sie benötigt periodische Bereinigung (Löschen verarbeiteter Datensätze). Alternativ kann die Outbox per CDC über das WAL statt per Polling gelesen werden.
- **CDC braucht trotzdem eine Inbox auf Consumer-Seite**: Die WAL-Erfassung arbeitet mit at-least-once; der Consumer muss deduplizieren.
- **Debezium benötigt einen Replication Slot** (PostgreSQL): Den Slot-Lag überwachen. Wächst der Lag, wächst auch die WAL-Aufbewahrung, was den Festplattenspeicher erschöpfen kann.

## See Also {#see-also}

- [[kafka-transactions]] - Exactly-once innerhalb von Kafka (ohne externe Systeme)
- [[delivery-semantics]] - At-most-once, at-least-once, exactly-once
- [[kafka-connect]] - Debezium-Connector für CDC
- [[cqrs-pattern]] - CQRS nutzt das Outbox-Muster für zuverlässige Event-Veröffentlichung
- [Debezium-Dokumentation](https://debezium.io/documentation/)
