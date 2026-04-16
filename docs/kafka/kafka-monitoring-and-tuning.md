# Kafka Monitoring and Tuning

Critical JMX metrics, Prometheus + Grafana setup, alert rules, and OS/JVM/broker-level performance tuning for production Kafka clusters.

## Critical JMX Metrics

### Cluster Health

| MBean | Metric | Alert Threshold |
|---|---|---|
| `kafka.controller:type=KafkaController,name=ActiveControllerCount` | Must be exactly 1 across cluster | != 1 |
| `kafka.controller:type=KafkaController,name=OfflinePartitionsCount` | Partitions with no active leader | > 0 |
| `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions` | Partitions below replication factor | > 0 for > 5 min |
| `kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount` | Partitions below `min.insync.replicas` | > 0 |

### Throughput

| MBean | Metric | Use |
|---|---|---|
| `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec` | Inbound bytes/sec | Capacity planning |
| `kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec` | Outbound bytes/sec | Network saturation |
| `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec` | Messages/sec | Throughput trending |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=Produce` | Produce requests/sec | Load profiling |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=FetchConsumer` | Consumer fetch requests/sec | Consumer load |

### Latency

| MBean | Metric | Alert Threshold |
|---|---|---|
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce` | End-to-end produce latency (p99) | > 100ms |
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer` | Consumer fetch latency (p99) | > 500ms |
| `kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Produce` | Time waiting in request queue | > 50ms (broker overloaded) |
| `kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent` | Request handler thread idle ratio | < 0.3 (70%+ busy = overloaded) |

### Replication

| MBean | Metric | Alert Threshold |
|---|---|---|
| `kafka.server:type=ReplicaManager,name=IsrShrinksPerSec` | ISR shrink rate | Sustained > 0 |
| `kafka.server:type=ReplicaManager,name=IsrExpandsPerSec` | ISR expand rate | Should follow shrinks |
| `kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica` | Max replication lag (messages) | > 10000 |
| `kafka.server:type=ReplicaManager,name=PartitionCount` | Partitions on broker | > 4000 |

### Consumer Lag

```bash
# CLI method
kafka-consumer-groups.sh --bootstrap-server broker1:9092 \
  --describe --group my-consumer-group

# Output columns: TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
```

For real-time lag monitoring, use Burrow (LinkedIn) or export via JMX:

```properties
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,
  name=records-lag-max
```

## Prometheus + Grafana Setup

### 1. JMX Exporter Agent

```bash
# Download
curl -LO https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/1.0.1/jmx_prometheus_javaagent-1.0.1.jar
```

```yaml
# kafka-jmx-config.yml
lowercaseOutputName: true
lowercaseOutputLabelNames: true
whitelistObjectNames:
  - "kafka.controller:*"
  - "kafka.server:type=BrokerTopicMetrics,*"
  - "kafka.server:type=ReplicaManager,*"
  - "kafka.server:type=ReplicaFetcherManager,*"
  - "kafka.server:type=KafkaRequestHandlerPool,*"
  - "kafka.network:type=RequestMetrics,*"
  - "kafka.network:type=RequestChannel,*"
  - "kafka.network:type=SocketServer,*"
  - "kafka.log:type=LogFlushStats,*"
  - "kafka.log:type=Log,name=Size,*"
  - "java.lang:type=GarbageCollector,*"
  - "java.lang:type=Memory"
rules:
  - pattern: "kafka.server<type=(.+), name=(.+), topic=(.+)><>(.+):"
    name: kafka_server_$1_$2
    labels:
      topic: $3
    type: GAUGE
  - pattern: "kafka.server<type=(.+), name=(.+)><>(.+):"
    name: kafka_server_$1_$2
    type: GAUGE
```

### 2. Broker Startup with Agent

```bash
# In systemd unit Environment or kafka-server-start.sh
export KAFKA_OPTS="-javaagent:/opt/kafka/libs/jmx_prometheus_javaagent-1.0.1.jar=7071:/opt/kafka/config/kafka-jmx-config.yml"
```

### 3. Prometheus Scrape Config

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kafka-brokers'
    static_configs:
      - targets:
        - broker1:7071
        - broker2:7071
        - broker3:7071
    relabel_configs:
      - source_labels: [__address__]
        regex: '(.+):7071'
        target_label: broker
        replacement: '$1'

  - job_name: 'kafka-consumer-lag'
    static_configs:
      - targets: ['burrow:8000']  # or kafka-lag-exporter
```

### 4. Alert Rules

```yaml
# kafka-alerts.yml
groups:
  - name: kafka
    rules:
      - alert: KafkaUnderReplicatedPartitions
        expr: kafka_server_replicamanager_underreplicatedpartitions > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.broker }} has {{ $value }} under-replicated partitions"

      - alert: KafkaNoActiveController
        expr: sum(kafka_controller_kafkacontroller_activecontrollercount) != 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "No active Kafka controller in the cluster"

      - alert: KafkaRequestHandlerSaturated
        expr: kafka_server_kafkarequesthandlerpool_requesthandleravgidlepercent < 0.3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.broker }} request handlers >70% busy"

      - alert: KafkaHighConsumerLag
        expr: kafka_consumer_consumer_fetch_manager_metrics_records_lag_max > 100000
        for: 10m
        labels:
          severity: warning
```

### 5. Grafana Dashboards

Import IDs `721` (broker overview), `7589` (topic detail), or use Confluent's open-source dashboards. Key panels: BytesIn/Out per broker, request latency heatmap, partition count distribution, consumer lag by group.

## Performance Tuning

### OS-Level

```bash
# --- Page cache ---
# Kafka reads/writes through page cache. More free RAM = more cache hits.
echo 1 > /proc/sys/vm/swappiness          # near-zero swap preference
echo "vm.swappiness=1" >> /etc/sysctl.conf

# Dirty page flush tuning (aggressive flush to avoid I/O bursts)
echo "vm.dirty_ratio=60" >> /etc/sysctl.conf
echo "vm.dirty_background_ratio=5" >> /etc/sysctl.conf

# --- File descriptors ---
# Each partition segment = 2 fds (log + index). 10K partitions = 20K fds minimum.
echo "kafka soft nofile 128000" >> /etc/security/limits.conf
echo "kafka hard nofile 128000" >> /etc/security/limits.conf
# Or in systemd unit: LimitNOFILE=128000

# --- TCP settings (critical for high-throughput and cross-DC) ---
echo "net.core.wmem_max=2097152" >> /etc/sysctl.conf         # 2 MB send buffer max
echo "net.core.rmem_max=2097152" >> /etc/sysctl.conf         # 2 MB receive buffer max
echo "net.ipv4.tcp_wmem=4096 65536 2097152" >> /etc/sysctl.conf
echo "net.ipv4.tcp_rmem=4096 65536 2097152" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog=50000" >> /etc/sysctl.conf  # packet queue before kernel
echo "net.ipv4.tcp_max_syn_backlog=8192" >> /etc/sysctl.conf

# --- Filesystem ---
# XFS is preferred. Mount options:
# /dev/sdb /data/kafka xfs noatime,nodiratime,nobarrier 0 2
# nobarrier: safe with battery-backed RAID or NVMe with PLP

sysctl -p  # apply all
```

### JVM Tuning (G1GC)

```bash
# kafka-server-start.sh or systemd Environment
export KAFKA_HEAP_OPTS="-Xms6g -Xmx6g"
export KAFKA_JVM_PERFORMANCE_OPTS="\
  -server \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=20 \
  -XX:InitiatingHeapOccupancyPercent=35 \
  -XX:+ExplicitGCInvokesConcurrent \
  -XX:MaxInlineLevel=15 \
  -XX:+ParallelRefProcEnabled \
  -XX:+UnlockExperimentalVMOptions \
  -XX:G1NewSizePercent=10 \
  -XX:G1MaxNewSizePercent=25 \
  -Djava.awt.headless=true"
```

Key GC principles:
- **6 GB heap** is the sweet spot for most workloads. Higher = longer GC pauses.
- **G1GC** with `MaxGCPauseMillis=20` keeps tail latency low.
- `InitiatingHeapOccupancyPercent=35` starts concurrent GC early, preventing full GC.
- Monitor `java.lang:type=GarbageCollector,name=G1 Young Generation` and `G1 Old Generation` in JMX. Alert if old gen collections > 0/min.

### Broker-Level Tuning

```properties
# --- Threading ---
num.network.threads=8              # network I/O threads (default 3, increase for 10GbE+)
num.io.threads=16                  # disk I/O threads (default 8, increase for JBOD)
num.replica.fetchers=4             # parallel replica fetch threads (default 1)
num.recovery.threads.per.data.dir=2  # log recovery threads at startup

# --- Socket buffers ---
socket.send.buffer.bytes=1048576   # 1 MB (default 100 KB)
socket.receive.buffer.bytes=1048576

# --- Replication ---
replica.fetch.max.bytes=10485760   # 10 MB (match message.max.bytes)
replica.fetch.wait.max.ms=500      # max wait before fetch response

# --- Log flush (usually leave to OS page cache) ---
# log.flush.interval.messages=10000  # uncomment only for durability-critical
# log.flush.interval.ms=1000

# --- Compression ---
compression.type=producer          # let producer decide (lz4 recommended)
```

## Gotchas

- **Page cache thrashing.** If consumers read very old data (catch-up reads), they evict recent data from page cache, degrading real-time consumers. Use tiered storage or separate read-only followers for historical reads.
- **Heap > 8 GB causes long GC pauses.** Kafka stores minimal state in heap. Extra RAM is better spent on page cache.
- **`UnderReplicatedPartitions > 0` does not always mean broker failure.** Can be caused by slow disks, network saturation, or GC pauses. Check `IsrShrinksPerSec` correlation with GC logs.
- **JMX exporter `whitelistObjectNames` matters.** Scraping all MBeans generates thousands of metrics and can cause OOM on the exporter. Whitelist only what you alert on.

## See Also

- [[kafka-cluster-management]] - sizing, upgrades, disk failure, partition reassignment
- [[kafka-backup-and-dr]] - MirrorMaker 2, backup strategies, disaster recovery
- [[kafka-replication-fundamentals]] - ISR mechanics, replication lag semantics
- [[consumer-groups]] - rebalance protocols, offset management, consumer lag semantics
- [[kafka-monitoring]] - additional monitoring patterns and tooling
