---
title: Kafka Troubleshooting
category: gotchas
tags: [kafka, troubleshooting, errors, leader-not-available, rebalancing, data-loss, duplicates]
---

# Kafka Troubleshooting

Common Kafka problems mapped to symptoms, root causes, and fixes for both producer-side and consumer-side issues.

## Key Facts

- Most Kafka issues fall into: leader election delays, rebalancing storms, offset management bugs, serialization errors, or disk exhaustion
- "Leader Not Available" is the most common Kafka error and usually self-resolves in seconds
- Auto-commit is the #1 source of data loss for beginners
- Disk exhaustion is the #1 operational outage cause
- Serialization errors cascade when schema changes without consumer coordination

## Patterns

### Producer Problems

**Leader Not Available**
- Symptom: `LEADER_NOT_AVAILABLE` error on produce
- Causes: leader died (election in progress), cluster under load, new topic being created
- Fix: usually self-resolves in seconds; if persists > 2 minutes, escalate to ops
- Protection: increase `retries` with `retry.backoff.ms`; implement [[transactional-outbox]] pattern

**ACK Lost (Duplicates)**
- Symptom: same message appears twice in topic
- Cause: broker stores message, ACK packet lost on network, producer retries
- Fix: enable [[idempotent-producer]] (`enable.idempotence=true`); for cross-session: use [[kafka-transactions]]

**Batch Lost on Producer Crash**
- Symptom: messages silently disappear
- Cause: in-flight batches exist only in producer memory; crash before send = permanent loss
- Fix: for critical data, implement write-ahead logging (write to local DB before sending to Kafka)

**Message Too Large**
- Symptom: `MSG_SIZE_TOO_LARGE` error
- Cause: broker `message.max.bytes` default is 1MB
- Fix: increase both broker (`message.max.bytes`) and topic (`max.message.bytes`) configs

### Consumer Problems

**Rebalancing Storm**
- Symptom: consumers repeatedly stop and restart reading; consumer lag grows
- Causes: processing > `session.timeout.ms`, slow app startup, frequent deploys, network instability
- Fix: increase `session.timeout.ms` + `max.poll.interval.ms`; reduce `max.poll.records`; use CooperativeStickyAssignor

**Auto-Commit Data Loss**
- Symptom: messages lost without error
- Cause: auto-commit fires before processing completes; consumer crashes mid-processing
- Fix: `enable.auto.commit=false`; commit manually after successful processing

**Offset Expiration**
- Symptom: consumer re-reads everything (or skips to latest) after downtime
- Cause: inactive > `offsets.retention.minutes` (default 7 days); Kafka deletes stored offsets
- Fix: set `auto.offset.reset` appropriately; consider storing offsets externally

**Serialization Errors**
- Symptom: consumer crashes on deserialize; `SerializationException`
- Cause: schema changed (field added/removed) without consumer coordination
- Fix: implement Dead Letter Queue for unparseable messages; use [[schema-registry]] with compatibility modes

**Database Restore Gap**
- Symptom: data inconsistency after database restore from backup
- Cause: consumer offset in Kafka points to current position; data from the gap already committed past
- Fix: reset consumer group offset via CLI; use new consumer group name; or store offsets in application DB

### Cluster Problems

**Disk Exhaustion**
- Symptom: broker cannot write, crashes
- Cause: retention configured but segments stay open longer than expected; advancing system time creates future timestamps preventing deletion
- Fix: monitor disk usage (alert at 80%); tune `log.segment.bytes` and `log.roll.hours` for faster segment closure
- **Most common way to crash Kafka**: advance system time during testing; messages with future timestamps prevent any segment from being deleted

**ISR Shrink**
- Symptom: `UnderReplicatedPartitions > 0`; `IsrShrinksPerSec` spikes
- Cause: slow disk, network issues, GC pauses, broker overloaded
- Fix: check disk I/O, network, JVM GC logs; consider manual degradation: switch `acks` from `all` to `1` temporarily

## Gotchas

- **"We upgraded Kafka, it'll be faster now"** - admin config changes are the most common trigger for Leader Not Available errors in production
- **`flush()` in Python does not throw on delivery failure** - it returns the number of messages still in queue; check errors in delivery callback, not `flush()` return value
- **TCP clock drift breaks connections** - if clocks drift significantly between producer and broker, TCP handshake timestamp validation fails
- **Always implement a Dead Letter Queue** - can be a Kafka topic, database table, or file; log the raw message bytes, not the deserialized form
- **Client auto-reconnects on broker failure** - `bootstrap.servers` with multiple brokers enables automatic failover; metadata refresh discovers alive brokers

## See Also

- [[kafka-monitoring]] - metrics, alerting thresholds
- [[delivery-semantics]] - at-most-once, at-least-once, exactly-once patterns
- [[consumer-groups]] - rebalancing mechanics
- [[broker-architecture]] - retention, segments, ISR management
