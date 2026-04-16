---
title: Apache Kafka Architecture
category: reference
tags: [kafka, event-streaming, message-broker, partitions, consumer-groups]
---

# Apache Kafka Architecture

Kafka is a message broker built on the log (journal) model. Focus on preserving message ordering, long-term storage, and high throughput. Pull model - consumers control reading pace.

## Architecture Hierarchy

```php
Cluster -> Brokers -> Topics -> Partitions -> Messages (with offsets)
```

- **Topic** - logical grouping of partitions. One message type per topic (e.g., `page_visit`, `user_registration`, `order_placed`)
- **Partition** - physical log with strict ordering. Always belongs to one topic
- **Offset** - pointer indicating where consumer stopped reading. Stored in `__consumer_offsets` system topic
- **Consumer Group** - consumers sharing common offset. Within a group, each partition read by exactly one consumer
- **Broker** - Kafka server instance. Multiple form a cluster

## Message Flow

1. Producer sends to **topic** (not directly to partition). Kafka selects partition (round-robin, key-based, or producer-specified)
2. Kafka writes with offset to partition
3. **Individual consumers** can read every message, any number of times (pub-sub)
4. **Consumer groups** - one consumer per partition. 3 partitions + 2 consumers = consumer 1 reads partitions 1+2, consumer 2 reads partition 3. Extra consumers idle if consumers > partitions

## Replication and HA

- **Leader-Follower** per partition. Leader handles all reads/writes
- Followers replicate data. On leader failure, follower promoted
- **Replication factor** typically 3
- **ZooKeeper** manages coordination (being replaced by **KRaft** in newer versions)

## Delivery Guarantees (acks)

| Setting | Guarantee | Speed | Behavior |
|---------|-----------|-------|----------|
| `acks=0` | At most once | Fastest | No acknowledgment |
| `acks=1` | At least once | Medium | Leader confirms |
| `acks=all` | Strongest | Slowest | Leader + all replicas confirm |

**`min.insync.replicas`** with `acks=all`: allows writes when N-1 replicas unavailable.

## Consumer Guarantees

Consumer's responsibility (pull model):
- Commit offset **after** processing = at-least-once
- Commit offset **before** processing = at-most-once
- **Exactly-once** = Kafka transactions or idempotent consumers

## Data Persistence

- Messages always written to disk
- **Retention by time** (e.g., 7 days) or **by size** (e.g., 1GB per partition)
- **Log compaction** - keep latest value per key
- Unlike RabbitMQ, messages retained after consumption

## When to Use Kafka

- High-volume event streaming (100K+ msg/sec)
- Systems requiring message replay
- Log aggregation from multiple services
- Real-time analytics and metrics pipelines
- Event sourcing architectures
- Data pipeline between source systems and DWH

## When NOT to Use

- Simple task queues (use RabbitMQ)
- Request-response patterns
- Low-latency RPC
- Systems with few messages

## Gotchas

- **More consumers than partitions** = idle consumers wasting resources
- **Single partition for ordering** limits throughput - use key-based partitioning to balance ordering with parallelism
- **Consumer lag** - monitor offset lag to detect slow consumers before they fall too far behind
- **Partition count** - can increase but never decrease. Choose wisely at topic creation
- **Rebalancing storms** - adding/removing consumers triggers rebalance, briefly stopping all consumption in the group

## See Also

- [[rabbitmq-architecture]] - Queue-based alternative
- [[message-broker-patterns]] - Choosing between brokers
- [[microservices-communication]] - Event-driven architecture
- [[bigdata-ml-architecture]] - Kafka in data pipelines
