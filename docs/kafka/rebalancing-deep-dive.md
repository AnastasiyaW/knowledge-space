---
title: Rebalancing Deep Dive
category: concepts
tags: [kafka, rebalancing, heartbeat, session-timeout, cooperative, static-membership]
---

# Rebalancing Deep Dive

Rebalancing is the process of redistributing partition assignments among consumers in a group, triggered by membership changes; it is both Kafka's fault tolerance mechanism and its primary source of consumer-side latency spikes.

## Key Facts

- Each consumer sends heartbeat to **group coordinator** (a designated broker) every `heartbeat.interval.ms` (default 3000ms)
- If no heartbeat within `session.timeout.ms` (default 10000ms for Java, 45000ms for librdkafka), consumer declared dead
- Heartbeat runs in a **separate thread** from message processing
- `max.poll.interval.ms` (default 300000ms = 5 min) - max time between `poll()` calls; exceeding triggers rebalance
- Rebalance triggers: consumer joins/leaves, subscription changes, partition count changes
- Does NOT trigger when consumer is paused (`.pause()`) - paused consumer still sends heartbeats

## Patterns

### Heartbeat Tuning

```properties
# Recommended settings to avoid unnecessary rebalances
heartbeat.interval.ms=3000          # 1/3 of session.timeout.ms
session.timeout.ms=10000            # 10s for consumer failure detection
max.poll.interval.ms=300000         # 5 min for long processing
max.poll.records=100                # reduce batch size if processing is slow
```

Rule: `heartbeat.interval.ms = session.timeout.ms / 3` - gives consumer 3 chances to heartbeat before being declared dead.

### Cooperative Rebalancing (Recommended)

```java
// Java - incremental cooperative rebalancing
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

Cooperative rebalancing only revokes and reassigns affected partitions. Other partitions continue being consumed without interruption.

### Static Group Membership

```java
// Java - static membership
props.put("group.instance.id", "consumer-host-1");
// Consumer keeps its assignment across restarts
// No rebalance triggered on temporary disconnect
```

Risk: if consumer crashes, its partition remains unread until it restarts (or `session.timeout.ms` expires for non-static members).

### Rebalance Listener

```java
// Java - track rebalance events
consumer.subscribe(List.of("orders"), new ConsumerRebalanceListener() {
    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
        // Commit offsets for revoked partitions
        consumer.commitSync(currentOffsets(partitions));
        // Clean up any in-memory state
    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
        // Initialize state for newly assigned partitions
        for (TopicPartition tp : partitions) {
            seekToStoredOffset(tp);
        }
    }
});
```

### Rebalance Triggers and Non-Triggers

| Event | Triggers Rebalance? |
|-------|-------------------|
| Consumer joins group | Yes |
| Consumer leaves/crashes | Yes |
| Consumer changes subscription | Yes |
| Partition count increases | Yes |
| Consumer paused (`.pause()`) | No |
| Consumer slow processing (within `max.poll.interval.ms`) | No |
| Consumer exceeds `max.poll.interval.ms` | Yes |

## Gotchas

- **Rebalancing storm** - consumers repeatedly stop and restart reading; causes: processing longer than `session.timeout.ms`, slow application startup, frequent deploys, network instability; fix: increase timeouts, reduce batch size, use CooperativeStickyAssignor
- **All reading stops during eager rebalance** - with default eager protocol, ALL consumers in the group stop reading during rebalance; slow-starting applications make this worse
- **Long processing + short timeout = infinite rebalance loop** - consumer processes batch, exceeds `max.poll.interval.ms`, gets kicked, rejoins, gets same batch, exceeds again
- **Mixing assignment strategies causes global rebalancing** - all consumers in a group must use the same partition assignment strategy

## See Also

- [[consumer-groups]] - group mechanics and assignment strategies
- [[consumer-configuration]] - all consumer config parameters with defaults
- [[kafka-monitoring-and-tuning]] - monitoring rebalance frequency
- [KIP-429: Kafka Consumer Incremental Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%3A+Kafka+Consumer+Incremental+Rebalance+Protocol)
