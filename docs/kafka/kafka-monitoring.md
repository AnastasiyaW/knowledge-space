---
title: Kafka Monitoring
category: reference
tags: [kafka, monitoring, jmx, prometheus, grafana, metrics, alerting, consumer-lag]
---

# Kafka Monitoring

Kafka exposes metrics via JMX; production monitoring requires tracking broker health, replication state, consumer lag, and request latency with alerting on critical thresholds.

## Key Facts

- Kafka metrics exposed via JMX (Java Management Extensions)
- Recommended stack: Prometheus + Grafana with pre-built Kafka dashboards
- Consumer lag is the most critical application health metric
- Disk monitoring is #1 priority - disk exhaustion is the most common Kafka outage cause
- Confluent Control Center provides web UI for monitoring (port 9021) but is a commercial product

## Patterns

### Critical Broker Metrics

```markdown
# Cluster-level (MUST alert on these)
kafka.controller:type=KafkaController,name=ActiveControllerCount   # MUST be exactly 1
kafka.controller:type=KafkaController,name=OfflinePartitionsCount   # MUST be 0
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions     # should be 0
kafka.controller:type=KafkaController,name=UncleanLeaderElectionsPerSec  # MUST be 0

# Broker throughput
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec

# Replication health
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec     # spikes = trouble
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount  # ISR < minIsr

# Request latency
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce   # p99 latency
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Fetch

# Disk
kafka.log:type=LogFlushRateAndTimeMs   # disk flush latency

# Thread utilization
kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent
kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent
```

### Alert Thresholds

| Metric | Alert Threshold | Severity |
|--------|----------------|----------|
| `ActiveControllerCount` | != 1 (sum across cluster) | Critical |
| `OfflinePartitionsCount` | > 0 | Critical |
| `UnderReplicatedPartitions` | > 0 for > 5 min | Warning |
| `UncleanLeaderElectionsPerSec` | > 0 | Critical (potential data loss) |
| `UnderMinIsrPartitionCount` | > 0 | Warning (unavailable to acks=all) |
| `IsrShrinksPerSec` | sustained spikes | Warning |
| Consumer lag | growing over time | Warning |
| Disk usage | > 80% | Warning |
| Request latency p99 | > 1s | Warning |

### Consumer Lag Monitoring

```bash
# CLI monitoring
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe

# Output columns:
# GROUP  TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG  CONSUMER-ID
```

Consumer lag = `LOG-END-OFFSET - CURRENT-OFFSET`. Growing lag means consumers cannot keep up.

### Broker Thread Tuning

```properties
# Network threads: handle incoming connections
num.network.threads=3     # Monitor idle%; if < 30%, increase
# 10,000 connections sufficient for most deployments

# I/O threads: handle disk operations
num.io.threads=8          # Monitor idle%; more = better disk utilization

# Total request capacity = network threads + I/O threads
```

### Consumer Metrics to Track

```markdown
# Java producer/consumer metrics
record-send-rate           # messages sent per second
record-error-rate          # send failures per second
batch-size-avg             # average batch size
buffer-available-bytes     # producer buffer remaining
request-latency-avg        # average request latency
produce-throttle-time-avg  # broker-side throttling time
```

## Gotchas

- **`OfflinePartitionsCount > 0` requires immediate investigation** - partitions without active leader are not writable/readable
- **`UnderReplicatedPartitions > 0` for extended period** - check disk I/O, network, GC pauses on lagging brokers
- **Segment vs retention interaction causes unexpected disk usage** - actual data lifetime may exceed configured retention because retention applies only to closed segments
- **Unclean Leader Election** - Kafka selects out-of-sync replica as leader; causes log truncation = data loss; triggered by quorum outages, network partitions, slow disks, GC pauses
- **Consumer lag growing = processing problem, not Kafka problem** - add partitions + consumers, optimize processing logic, or increase batch sizes

## See Also

- [[broker-architecture]] - broker internals, JMX metrics reference
- [[kafka-replication-fundamentals]] - ISR mechanics, what UnderReplicated means
- [[kafka-cluster-management]] - operational procedures, capacity planning
- [[kafka-monitoring-and-tuning]] - JMX metrics reference, Prometheus setup, performance tuning
- [[kafka-troubleshooting]] - symptom-to-fix mapping
- [Apache Kafka Monitoring](https://kafka.apache.org/documentation/#monitoring)
