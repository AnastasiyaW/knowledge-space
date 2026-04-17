---
title: Apache Kafka - Delivery Semantics and Consumer Patterns
category: concepts
tags: [kafka, messaging, event-driven, consumer-groups, streaming]
---

# Apache Kafka - Delivery Semantics and Consumer Patterns

Kafka delivery guarantees, consumer group mechanics, rebalancing strategies, and integration patterns. Focused on practical production usage rather than cluster administration.

## Key Facts

- Three delivery semantics: at-most-once, at-least-once (default/recommended), exactly-once
- At-least-once requires idempotent consumers - same message processed twice gives same result
- KRaft mode (Kafka 2.8+) eliminates ZooKeeper dependency
- Producer sends to topic partition: round-robin by default, or by key hash for ordering
- Consumer group distributes partitions among members; rebalancing on join/leave
- Cooperative Sticky is the preferred rebalancing strategy since Kafka 2.4

## Patterns

### Delivery Semantics

**At most once** - acknowledge offset before processing:
- Fast, may lose messages on crash
- Use when message loss is acceptable (metrics, non-critical events)

**At least once** - process then acknowledge:
- Default for most use cases
- Requires idempotent consumers
- Use database unique constraints or deduplication tables

**Exactly once** - requires Kafka transactions + idempotent producer:
- Kafka Streams API makes this easier
- Very complex for consumer-to-database scenarios
- Often simpler to implement at-least-once with idempotency keys

### Consumer Group Rebalancing

| Strategy | Behavior |
|----------|----------|
| RoundRobin | Evenly distribute all partitions |
| Sticky | Minimize partition movement on rebalance |
| Cooperative Sticky | Incremental rebalance; consumers keep partitions until new assignment confirmed |

Cooperative Sticky minimizes downtime during rolling restarts - consumers do not stop processing while rebalance is in progress.

### Transactional Outbox

Problem: atomically update DB and publish Kafka message.

1. Same DB transaction: update entity + insert event to `outbox` table
2. Background poller reads unsent outbox events, publishes to Kafka, marks sent
3. Consumer deduplicates using idempotency keys

This avoids the two-phase commit problem entirely.

### Key Concepts

- **Partition**: unit of parallelism and ordering. Messages within a partition are ordered.
- **Offset**: position within partition. Committed offset = "I have processed up to here."
- **Consumer group**: set of consumers sharing topic partitions. Each partition assigned to exactly one consumer in the group.
- **Key-based routing**: messages with same key always go to same partition, ensuring ordering per key.

## Gotchas

- Number of consumers in a group cannot exceed number of partitions - extra consumers sit idle
- Exactly-once is practically impossible across Kafka + external system without idempotency at the consumer
- Consumer lag (offset behind latest) is the primary health metric for consumer groups
- KRaft mode simplifies deployment but requires 1-3 controller nodes for metadata management
- Long processing times without committing offsets can trigger session timeout and rebalance

## See Also

- [[database-patterns]] - transactional outbox implementation in Go
- [[microservices]] - Kafka in microservice architecture
- [[observability-query-languages]] - monitoring consumer lag with PromQL
