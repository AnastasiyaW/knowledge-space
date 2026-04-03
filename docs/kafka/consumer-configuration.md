---
title: Consumer Configuration
category: reference
tags: [kafka, consumer, configuration, fetch, polling, timeout]
---

# Consumer Configuration

Complete reference for Kafka consumer configuration parameters with defaults, tuning guidelines, and impact on behavior.

## Key Facts

- Consumer is pull-based: calls `poll()` to fetch data from brokers; Kafka does not push
- `fetch.max.wait.ms` controls max wait during poll; whatever arrives in this window is returned
- `fetch.min.bytes` sets minimum data size before returning; Kafka waits until this much data is available OR `fetch.max.wait.ms` expires
- Kafka never returns partial messages - always complete records
- `max.poll.records` (default 500) limits messages per poll across all partitions
- Three Python Kafka clients: confluent-kafka-python (librdkafka wrapper, production), kafka-python (pure Python), kafka-go for Go

## Patterns

### Throughput-Optimized Consumer

```properties
fetch.min.bytes=1048576        # 1MB - wait for larger batches
fetch.max.wait.ms=500          # wait up to 500ms
max.poll.records=1000          # larger batches per poll
max.partition.fetch.bytes=2097152  # 2MB per partition
```

### Latency-Optimized Consumer

```properties
fetch.min.bytes=1              # return as soon as any data available
fetch.max.wait.ms=100          # short wait
max.poll.records=100           # smaller batches, faster processing
```

### Long-Processing Consumer

```properties
max.poll.interval.ms=600000    # 10 min between polls
max.poll.records=50            # smaller batches
session.timeout.ms=45000       # longer session
heartbeat.interval.ms=15000    # 1/3 of session timeout
```

### Consumer Group Operations via Admin API

```java
Admin admin = Admin.create(Map.of("bootstrap.servers", "localhost:9092"));

admin.listConsumerGroups();
admin.describeConsumerGroups(List.of("group-id"));
admin.listConsumerGroupOffsets("group-id");
admin.alterConsumerGroupOffsets("group-id", offsetMap);
admin.deleteConsumerGroupOffsets("group-id", partitions);
```

## Gotchas

- **`enable.auto.commit=true` is the default** - this is the #1 source of data loss bugs for beginners; disable for any production workload
- **`auto.commit.interval.ms` must be less than `session.timeout.ms`** - otherwise consumer is declared dead before commit fires
- **`max.poll.interval.ms` exceeded = consumer kicked from group** - even if heartbeats are fine; happens with long-running processing
- **Three Go clients exist with different APIs** - kafka-go (pure Go, contexts), confluent-kafka-go (librdkafka wrapper, Java-like), and others; choose based on team preference

## See Also

- [[consumer-groups]] - group mechanics, assignment strategies
- [[offsets-and-commits]] - offset management strategies
- [[rebalancing-deep-dive]] - heartbeat tuning, cooperative rebalancing
- [Apache Kafka Consumer Configs](https://kafka.apache.org/documentation/#consumerconfigs)
