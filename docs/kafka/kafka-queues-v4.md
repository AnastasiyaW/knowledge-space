---
title: Kafka Queues (v4.0)
category: concepts
tags: [kafka, queues, kafka-4, work-queue, virtual-partitions]
---

# Kafka Queues (v4.0)

Kafka 4.0 introduces work queue semantics where each message is processed by only one consumer in a group, with automatic scaling and no rebalancing, using virtual partitions internally.

## Key Facts

- Enabled via `queue.topic.enable=true` on the topic
- Each message processed by only ONE consumer in the group (competing consumers pattern)
- Automatic scaling without rebalancing (unlike traditional consumer groups)
- Partitioning hidden from the client - virtual partitions used internally for distribution
- Bridges the gap between Kafka's log model and traditional message queue behavior
- Part of Kafka 4.0 release alongside KRaft-only (ZooKeeper fully removed) and Tiered Storage

## Patterns

### Kafka 4.0 Feature Summary

| Feature | Status |
|---------|--------|
| KRaft (ZooKeeper removed) | Production default |
| Kafka Queues | New in 4.0 |
| Tiered Storage | GA in 4.0 |

### Tiered Storage

```properties
# Enable tiered storage
remote.log.enabled=true
# Recent data on local disk, older segments on remote tier (S3, HDFS)
# Extended retention without overwhelming local storage
```

## Gotchas

- **Kafka Queues is new in v4.0** - ecosystem support may be limited initially
- **Not a replacement for RabbitMQ** - Kafka Queues adds queue semantics but Kafka's architecture remains log-based
- **Virtual partitions are internal** - you don't configure or see them; distribution is automatic

## See Also

- [[messaging-models]] - queue vs pub-sub vs log-based models
- [[consumer-groups]] - traditional Kafka consumer group semantics
- [[broker-architecture]] - KRaft mode, Kafka 4.0 changes
- [KIP-932: Queues for Kafka](https://cwiki.apache.org/confluence/display/KAFKA/KIP-932)
