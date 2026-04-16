---
title: Transactional Outbox and Inbox
category: patterns
tags: [kafka, outbox, inbox, cdc, debezium, exactly-once, idempotent, distributed-transactions]
---

# Transactional Outbox and Inbox

The Transactional Outbox pattern writes events to an outbox table within the same database transaction as business data, while the Inbox pattern provides consumer-side idempotency via unique constraints, together achieving practical exactly-once across system boundaries.

## Key Facts

- **Problem**: how to atomically update a database AND publish an event to Kafka
- **Outbox**: write event to outbox table in same DB transaction as business data; separate processor publishes to Kafka
- **Inbox**: receiving service uses inbox table with unique constraint to deduplicate incoming messages
- **Complete guarantee chain**: outbox (at-least-once) + queue (at-least-once) + inbox (idempotency) = practical exactly-once
- "Exactly once" delivery is impossible in distributed systems (Two Generals' Problem)
- Practical exactly-once = at-least-once + idempotence at every boundary
- [[kafka-connect]] with Debezium can replace custom outbox/inbox processors

## Patterns

### Transactional Outbox

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

**Outbox Processor** (separate service):
1. Poll outbox table for unprocessed records
2. Publish to Kafka
3. Mark as processed after successful publish
4. Retry on failure (at-least-once delivery)

### Transactional Inbox

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

### Complete Architecture

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

### CDC as Outbox Alternative

Instead of explicit outbox table, capture changes from database's WAL:

| Approach | Intrusion Level | DB Load |
|----------|----------------|---------|
| Timestamps/version on rows | Major (schema changes) | Additional queries |
| Triggers on tables | Minor (opaque to app) | Additional operations |
| WAL-based CDC (Debezium) | **None** | **None** |

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

WAL-based CDC: zero intrusion into application or schema, no additional database load, captures all changes including from other tools/processes.

## Gotchas

- **Outbox processor crash = at-least-once, not exactly-once** - if processor publishes but crashes before marking as processed, it will re-publish on restart; inbox pattern on consumer side is essential
- **Outbox table grows** - needs periodic cleanup (delete processed records); can also use CDC to read outbox via WAL instead of polling
- **CDC still needs inbox on consumer side** - WAL capture is at-least-once; consumer must deduplicate
- **Debezium requires replication slot** (PostgreSQL) - monitor slot lag; growing lag means WAL retention grows and can exhaust disk

## See Also

- [[kafka-transactions]] - exactly-once within Kafka (no external systems)
- [[delivery-semantics]] - at-most-once, at-least-once, exactly-once
- [[kafka-connect]] - Debezium connector for CDC
- [[cqrs-pattern]] - CQRS uses outbox pattern for reliable event publishing
- [Debezium Documentation](https://debezium.io/documentation/)
