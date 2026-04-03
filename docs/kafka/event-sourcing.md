---
title: Event Sourcing
category: patterns
tags: [kafka, event-sourcing, immutable-log, replay, audit, state-reconstruction]
---

# Event Sourcing

Event sourcing stores every state change as an immutable event in Kafka rather than overwriting current state in a database, enabling full history replay, audit trails, and state reconstruction at any point in time.

## Key Facts

- Kafka's immutable append-only log is a natural fit for event sourcing
- All events recorded as immutable facts; state is derived by replaying events
- Current state reconstructed by replaying events from any offset
- Kafka's log retention ensures complete event history for audits and compliance
- Multiple [[consumer-groups]] can read the same event stream independently to build different materialized views
- Solves "how did we get to this state?" problem - with only current state in DB, you cannot trace history
- Writing all events to a traditional RDBMS bottlenecks at ~10K writes/sec; Kafka handles millions
- Use specialized read stores (ElasticSearch, Redis, Cassandra) for materialized views
- For indefinite event storage, a dedicated Event Store (EventStoreDB, MongoDB) is more appropriate than Kafka (which deletes by default)

## Patterns

### Event Sourcing Architecture

```
Events -> Kafka Topic (append-only log, source of truth)
    -> Materializer A -> Read Store A (current state for API)
    -> Materializer B -> Read Store B (analytics, full-text search)
    -> Materializer C -> Read Store C (notifications, ML fraud detection)
    -> Technical Support -> Full event history for debugging
```

### Event Replay

```
POST /api/replay-events
1. Command API reads all events from Event Store
2. Sends marker event "replay started"
3. Query API clears its read model
4. Query API re-applies all events to rebuild from scratch
```

Use cases: schema migration, bug fix in event handlers, adding new projections, disaster recovery. During replay: incoming commands blocked until complete.

### Kafka as Actor System

Each consumer processing a partition acts as an actor:
- Receives messages sequentially
- Maintains state
- Can produce messages to other topics
- Partitions naturally enforce sequential processing

## Gotchas

- **Kafka eventually deletes events by default** - for true indefinite event storage, use a dedicated Event Store alongside Kafka or configure infinite retention
- **Event schema evolution is critical** - adding/removing fields in events breaks replay; use [[schema-registry]] with FULL compatibility
- **Replay can be expensive** - millions of events take time to replay; consider snapshotting: periodically save current state, replay only from last snapshot
- **Ordering only within partition** - related events must share a partition key; cross-partition ordering requires additional coordination

## See Also

- [[cqrs-pattern]] - Command Query Responsibility Segregation, natural companion to Event Sourcing
- [[kafka-streams]] - stream processing for building materialized views
- [[topics-and-partitions]] - log compaction for "latest state per key" tables
- [[delivery-semantics]] - exactly-once for event processing
