---
title: Kafka Cluster Operations
category: reference
tags: [kafka, operations, monitoring, tuning, upgrade, backup, disaster-recovery]
---

# Kafka Cluster Operations

Production Kafka: sizing, upgrades, monitoring, tuning, disk failures, partition reassignment, cross-DC replication, backup, and disaster recovery.

## Cluster Sizing

### Broker Count

Minimum 3 brokers for production (`replication.factor=3`, `min.insync.replicas=2` - tolerates 1 broker failure). Scale horizontally by adding brokers and reassigning partitions.

**Sizing formula:**

```
brokers_needed = max(
    total_disk_needed / disk_per_broker,
    total_throughput_needed / throughput_per_broker,
    total_partitions / max_partitions_per_broker
)
```

Rules of thumb:
- ~4000 partitions per broker (leaders + followers) before performance degrades
- ~200K partitions per cluster (KRaft; ZooKeeper limit was ~100K)
- Each partition replica uses 1 file descriptor per segment + 1 index fd
- Single broker can handle ~100 MB/s writes with NVMe, ~30 MB/s with spinning disks

### Disk

```properties
# Multiple log.dirs across disks = parallel I/O
log.dirs=/data/kafka-logs-1,/data/kafka-logs-2,/data/kafka-logs-3
```

**Capacity calculation:**

```
disk_per_broker = (write_throughput_MB_s * retention_seconds * replication_factor) / broker_count
                  + 20% overhead (compaction, index, snapshots)
```

XFS > ext4 for Kafka workloads. Mount with `noatime,nodiratime`. RAID-10 if using spinning disks; JBOD with multiple `log.dirs` preferred for SSDs (Kafka handles replica placement).

### Memory

Kafka relies on OS page cache, not JVM heap, for read performance.

```
total_RAM = JVM_heap + page_cache_for_active_segments
```

- JVM heap: 6 GB typical, 8 GB max (larger heaps = longer GC pauses)
- Page cache: enough to hold active segments for all partitions. A partition's active segment = `log.segment.bytes` (default 1 GB). If 1000 partitions: aim for ~32-64 GB page cache
- Total per broker: 64-128 GB RAM is common

### Network

```
network_per_broker = write_throughput * (replication_factor - 1) + read_throughput * consumer_count
```

10 GbE minimum for production. Bond multiple NICs if needed. Set `socket.send.buffer.bytes` and `socket.receive.buffer.bytes` to match BDP (bandwidth-delay product) for cross-DC replication.

### Controller Quorum (KRaft)

3 controllers for most deployments. 5 for large clusters (tolerates 2 failures). Controllers can be co-located with brokers (combined mode) or dedicated (separate mode).

```properties
# Dedicated controller (separate mode)
process.roles=controller
node.id=100
controller.quorum.voters=100@ctrl1:9093,101@ctrl2:9093,102@ctrl3:9093
listeners=CONTROLLER://ctrl1:9093
controller.listener.names=CONTROLLER
```

## Rolling Upgrade Procedure

### Pre-Upgrade

```bash
# 1. Check current versions
kafka-broker-api-versions.sh --bootstrap-server broker1:9092 | head -1

# 2. Verify cluster health
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --status  # KRaft
kafka-topics.sh --describe --under-replicated-partitions --bootstrap-server broker1:9092

# 3. Ensure no under-replicated partitions
# UnderReplicatedPartitions must be 0 before starting
```

### Upgrade Steps

```bash
# For each broker, one at a time:

# Step 1: Set inter.broker.protocol.version to CURRENT version
# in server.properties BEFORE upgrading binary
# This allows new binary to speak old protocol
echo "inter.broker.protocol.version=3.6" >> /opt/kafka/config/server.properties
echo "log.message.format.version=3.6" >> /opt/kafka/config/server.properties

# Step 2: Stop broker gracefully
sudo systemctl stop kafka
# Wait for controlled shutdown to complete (check logs for
# "controlled shutdown complete" or broker exits cleanly)

# Step 3: Replace binaries
mv /opt/kafka /opt/kafka-old
tar xzf kafka_2.13-3.7.0.tgz -C /opt/
mv /opt/kafka_2.13-3.7.0 /opt/kafka
cp /opt/kafka-old/config/server.properties /opt/kafka/config/

# Step 4: Start broker with new binary
sudo systemctl start kafka

# Step 5: Wait for ISR to recover before moving to next broker
watch -n 5 "kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server broker1:9092 | wc -l"
# Proceed only when output is 0
```

### Post-Upgrade (After All Brokers)

```bash
# Remove protocol version pins to enable new features
# Edit server.properties on all brokers, remove:
#   inter.broker.protocol.version
#   log.message.format.version
# Then rolling restart again

# Verify new version
kafka-broker-api-versions.sh --bootstrap-server broker1:9092
```

### ZooKeeper to KRaft Migration

```bash
# 1. Generate migration metadata
kafka-metadata-migration.sh --zk-connect zk1:2181 --dry-run

# 2. Start KRaft controllers with migration flag
# In controller server.properties:
#   zookeeper.metadata.migration.enable=true
#   zookeeper.connect=zk1:2181,zk2:2181,zk3:2181

# 3. Rolling restart brokers with KRaft config
# 4. Verify all brokers registered with KRaft controllers
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --replication

# 5. Finalize migration (irreversible)
kafka-metadata-migration.sh --finalize
```

## Monitoring

### Critical JMX Metrics

#### Cluster Health

| MBean | Metric | Alert Threshold |
|---|---|---|
| `kafka.controller:type=KafkaController,name=ActiveControllerCount` | Must be exactly 1 across cluster | != 1 |
| `kafka.controller:type=KafkaController,name=OfflinePartitionsCount` | Partitions with no active leader | > 0 |
| `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions` | Partitions below replication factor | > 0 for > 5 min |
| `kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount` | Partitions below `min.insync.replicas` | > 0 |

#### Throughput

| MBean | Metric | Use |
|---|---|---|
| `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec` | Inbound bytes/sec | Capacity planning |
| `kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec` | Outbound bytes/sec | Network saturation |
| `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec` | Messages/sec | Throughput trending |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=Produce` | Produce requests/sec | Load profiling |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=FetchConsumer` | Consumer fetch requests/sec | Consumer load |

#### Latency

| MBean | Metric | Alert Threshold |
|---|---|---|
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce` | End-to-end produce latency (p99) | > 100ms |
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer` | Consumer fetch latency (p99) | > 500ms |
| `kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Produce` | Time waiting in request queue | > 50ms (broker overloaded) |
| `kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent` | Request handler thread idle ratio | < 0.3 (70%+ busy = overloaded) |

#### Replication

| MBean | Metric | Alert Threshold |
|---|---|---|
| `kafka.server:type=ReplicaManager,name=IsrShrinksPerSec` | ISR shrink rate | Sustained > 0 |
| `kafka.server:type=ReplicaManager,name=IsrExpandsPerSec` | ISR expand rate | Should follow shrinks |
| `kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica` | Max replication lag (messages) | > 10000 |
| `kafka.server:type=ReplicaManager,name=PartitionCount` | Partitions on broker | > 4000 |

#### Consumer Lag

```bash
# CLI method
kafka-consumer-groups.sh --bootstrap-server broker1:9092 \
  --describe --group my-consumer-group

# Output columns: TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
```

For real-time lag monitoring, use Burrow (LinkedIn) or export via JMX:

```
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,
  name=records-lag-max
```

### Prometheus + Grafana Setup

**1. JMX Exporter agent on each broker:**

```bash
# Download
curl -LO https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/1.0.1/jmx_prometheus_javaagent-1.0.1.jar

# Kafka JMX config (kafka-jmx-config.yml)
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

**2. Broker startup with agent:**

```bash
# In systemd unit Environment or kafka-server-start.sh
export KAFKA_OPTS="-javaagent:/opt/kafka/libs/jmx_prometheus_javaagent-1.0.1.jar=7071:/opt/kafka/config/kafka-jmx-config.yml"
```

**3. Prometheus scrape config:**

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

**4. Key Prometheus alert rules:**

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

**5. Grafana dashboards:** Import IDs `721` (broker overview), `7589` (topic detail), or use Confluent's open-source dashboards. Key panels: BytesIn/Out per broker, request latency heatmap, partition count distribution, consumer lag by group.

## Performance Tuning

### OS-Level

```bash
# --- Page cache ---
# Kafka reads/writes through page cache. More free RAM = more cache hits.
# Don't let the kernel swap Kafka pages.
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

## Disk Failure Handling

### JBOD Configuration

```properties
# Multiple independent disks (JBOD)
log.dirs=/data1/kafka-logs,/data2/kafka-logs,/data3/kafka-logs
```

Since Kafka 1.1, JBOD disk failure is handled gracefully:

```properties
# Broker stays online when a disk fails (default since 2.0)
log.dir.failure.handler=kafka.server.LogDirFailureHandler
# Broker marks failed log dir as offline, stops partitions on that disk
# Other disks continue serving
```

### Disk Failure Response

```bash
# 1. Identify failed disk
kafka-log-dirs.sh --describe --bootstrap-server broker1:9092 | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for broker in data['brokers']:
    for ld in broker['logDirs']:
        if ld['error']:
            print(f\"Broker {broker['broker']}: {ld['logDir']} - {ld['error']}\")
"

# 2. Partitions on failed disk lose their replicas on this broker.
# ISR shrinks. If this was the leader, leadership moves to another ISR member.
# No data loss if replication.factor >= 2.

# 3. Replace disk, recreate mount, restart broker
# Broker re-joins cluster, controller assigns replicas, data replicates from leaders
sudo systemctl stop kafka
# ... replace disk, mkfs.xfs, mount ...
sudo systemctl start kafka

# 4. Verify recovery
watch -n 10 "kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server broker1:9092 | wc -l"
```

### Monitoring Disk Health

```bash
# Include in cron or monitoring agent
smartctl -a /dev/sdb | grep -E "Reallocated_Sector|Current_Pending|Offline_Uncorrectable"
iostat -x 5 | grep -E "sdb|sdc|sdd"  # watch await, %util
```

Alert on: `await > 50ms`, `%util > 90%` sustained, SMART errors.

## Partition Reassignment

### When to Reassign

- New broker added to cluster (new broker has 0 partitions)
- Broker decommissioned (move all partitions off)
- Uneven partition distribution (hot brokers)
- Disk rebalancing within a broker (move between `log.dirs`)

### Manual Reassignment

```bash
# Step 1: Generate reassignment plan
# Create topics-to-move.json:
cat > topics-to-move.json << 'EOF'
{
  "version": 1,
  "topics": [
    {"topic": "orders"},
    {"topic": "events"}
  ]
}
EOF

# Generate proposal (target brokers: 1,2,3,4 - including new broker 4)
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --topics-to-move-json-file topics-to-move.json \
  --broker-list "1,2,3,4" \
  --generate

# Output: current assignment + proposed assignment JSON

# Step 2: Save proposed assignment to file
# (copy the "Proposed partition reassignment configuration" output)
cat > reassignment.json << 'EOF'
{
  "version": 1,
  "partitions": [
    {"topic": "orders", "partition": 0, "replicas": [4,2,3], "log_dirs": ["any","any","any"]},
    {"topic": "orders", "partition": 1, "replicas": [1,4,2], "log_dirs": ["any","any","any"]},
    {"topic": "orders", "partition": 2, "replicas": [2,3,4], "log_dirs": ["any","any","any"]}
  ]
}
EOF

# Step 3: Execute (throttled to avoid saturating network)
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassignment.json \
  --execute \
  --throttle 50000000  # 50 MB/s replication throttle

# Step 4: Monitor progress
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassignment.json \
  --verify

# Step 5: After completion, remove throttle
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassignment.json \
  --verify  # automatically removes throttle on completion
```

### Preferred Leader Election

```bash
# After reassignment, new preferred leaders may not be active leaders.
# Trigger preferred leader election:
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type PREFERRED \
  --all-topic-partitions

# Or for specific topic:
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type PREFERRED \
  --topic orders
```

### Automated Rebalancing with Cruise Control

For large clusters, LinkedIn's Cruise Control automates rebalancing:

```bash
# Key endpoints:
# GET  /kafkacruisecontrol/state          - cluster state
# POST /kafkacruisecontrol/rebalance      - trigger rebalance
# POST /kafkacruisecontrol/add_broker     - integrate new broker
# POST /kafkacruisecontrol/remove_broker  - decommission broker

# Example: add broker 4 and rebalance
curl -X POST "http://cruise-control:9090/kafkacruisecontrol/add_broker?brokerid=4&dryrun=false"
```

## MirrorMaker 2 - Multi-DC Replication

MM2 is built on Kafka Connect. Supports active-active, active-passive, and fan-out topologies.

### Configuration

```properties
# mm2.properties
clusters = dc-east, dc-west
dc-east.bootstrap.servers = east-broker1:9092,east-broker2:9092,east-broker3:9092
dc-west.bootstrap.servers = west-broker1:9092,west-broker2:9092,west-broker3:9092

# Replicate east -> west
dc-east->dc-west.enabled = true
dc-east->dc-west.topics = orders, events, users
# Or regex: dc-east->dc-west.topics = .*

# Replicate west -> east (active-active)
dc-west->dc-east.enabled = true
dc-west->dc-east.topics = orders, events, users

# Prevent infinite replication loops
# MM2 prefixes remote topics: "dc-east.orders" on dc-west cluster
# Exclude remote topics from replication back:
dc-west->dc-east.topics.exclude = dc-east\..*
dc-east->dc-west.topics.exclude = dc-west\..*

# Offset sync (consumers can failover with correct offsets)
emit.checkpoints.enabled = true
emit.checkpoints.interval.seconds = 60
sync.group.offsets.enabled = true
sync.group.offsets.interval.seconds = 60

# Replication tuning
replication.factor = 3
tasks.max = 4
offset-syncs.topic.replication.factor = 3
heartbeats.topic.replication.factor = 3
checkpoints.topic.replication.factor = 3
```

### Launch

```bash
# Standalone mode
bin/connect-mirror-maker.sh config/mm2.properties

# Distributed mode (via Kafka Connect cluster)
# Submit MM2 connectors through Connect REST API:
curl -X POST http://connect:8083/connectors -H "Content-Type: application/json" -d '{
  "name": "mm2-dc-east-to-dc-west",
  "config": {
    "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "source.cluster.alias": "dc-east",
    "target.cluster.alias": "dc-west",
    "source.cluster.bootstrap.servers": "east-broker1:9092",
    "target.cluster.bootstrap.servers": "west-broker1:9092",
    "topics": "orders,events,users",
    "replication.factor": "3",
    "tasks.max": "4"
  }
}'
```

### Consumer Failover with Offset Translation

```bash
# On dc-west, after dc-east failure:
# MM2 checkpoints store translated offsets in dc-west's
# "dc-east.checkpoints.internal" topic

# Consumer can read translated offsets:
kafka-console-consumer.sh --topic dc-east.checkpoints.internal \
  --from-beginning --bootstrap-server west-broker1:9092 \
  --property print.key=true | head

# Automated offset translation for consumer group failover:
kafka-consumer-groups.sh --bootstrap-server west-broker1:9092 \
  --group my-app --reset-offsets --to-latest \
  --topic dc-east.orders --execute
```

### MM2 Monitoring

Key metrics (via JMX on Connect workers):
- `kafka.connect.mirror:type=MirrorSourceConnector,target=*,topic=*,partition=*` - `record-count`, `byte-rate`, `replication-latency-ms`
- Alert on `replication-latency-ms-avg > 5000` (5s replication lag)

## Backup Strategies

Kafka is not a database, but data loss scenarios exist. Backup approaches:

### 1. Topic-Level Backup with kafka-consumer

```bash
# Dump topic to file (for smaller topics / config topics)
kafka-console-consumer.sh --bootstrap-server broker1:9092 \
  --topic __consumer_offsets --from-beginning \
  --timeout-ms 30000 \
  --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" \
  > consumer_offsets_backup_$(date +%Y%m%d).txt
```

### 2. Filesystem-Level Backup

```bash
# Stop broker, snapshot log.dirs
sudo systemctl stop kafka

# Rsync partition data (preserves segment files, indexes, snapshots)
rsync -avz --progress /data/kafka-logs/ backup-server:/backup/kafka/broker1/

sudo systemctl start kafka
```

For online backup: snapshot the underlying filesystem (LVM, ZFS, or EBS snapshots on cloud).

```bash
# LVM snapshot (online, consistent if broker is not leader for partitions)
lvcreate -L 50G -s -n kafka-snap /dev/vg0/kafka-data
mount /dev/vg0/kafka-snap /mnt/kafka-snap
rsync -avz /mnt/kafka-snap/ backup-server:/backup/kafka/broker1/
umount /mnt/kafka-snap
lvremove -f /dev/vg0/kafka-snap
```

### 3. Cross-Cluster Replication (Preferred)

MirrorMaker 2 to a standby cluster is the recommended "backup" for production data. It handles offset translation, topic configs, and ACLs.

### 4. Metadata Backup

```bash
# Export topic configs
kafka-topics.sh --describe --bootstrap-server broker1:9092 | \
  tee topics_describe_$(date +%Y%m%d).txt

# Export all topic configurations
for topic in $(kafka-topics.sh --list --bootstrap-server broker1:9092); do
  echo "=== $topic ==="
  kafka-configs.sh --describe --all --topic "$topic" --bootstrap-server broker1:9092
done > topic_configs_$(date +%Y%m%d).txt

# Export consumer group offsets
kafka-consumer-groups.sh --bootstrap-server broker1:9092 --all-groups --describe \
  > consumer_groups_$(date +%Y%m%d).txt

# Export ACLs
kafka-acls.sh --bootstrap-server broker1:9092 --list \
  > acls_$(date +%Y%m%d).txt

# KRaft metadata snapshot (already in log.dirs/__cluster_metadata-0/)
# Automatically maintained by controller quorum
```

## Disaster Recovery Patterns

### Pattern 1: Active-Passive with MM2

```
DC-East (Primary)  ----MM2---->  DC-West (Standby)
   producers                       idle consumers
   consumers                       ready to activate
```

**Failover procedure:**

```bash
# 1. Detect primary failure (automated or manual)
# 2. Stop MM2 replication
# 3. Translate consumer offsets on standby
kafka-consumer-groups.sh --bootstrap-server west-broker1:9092 \
  --group my-app --reset-offsets --to-latest \
  --topic dc-east.orders --execute

# 4. Redirect producers to standby cluster (DNS failover or config push)
# 5. Start consumers on standby cluster pointing to dc-east.* prefixed topics
#    OR rename topics (topic aliases via consumer config)

# RTO: 5-15 min (mostly DNS propagation + consumer group stabilization)
# RPO: seconds to minutes (depends on MM2 replication lag)
```

### Pattern 2: Active-Active with MM2

```
DC-East  <----MM2---->  DC-West
   producers write locally         producers write locally
   consumers read local + remote   consumers read local + remote
```

Consumers subscribe to both local and remote-prefixed topics:

```java
consumer.subscribe(Arrays.asList("orders", "dc-west.orders"));
// Application must handle deduplication if needed
```

**Conflict resolution:** application-level. Use record keys with DC-prefix or event timestamps for last-writer-wins.

### Pattern 3: Stretch Cluster (Single Cluster, Multiple DCs)

```properties
# Broker rack awareness
broker.rack=dc-east-rack1

# Topic with rack-aware replica placement
kafka-topics.sh --create --topic orders \
  --partitions 6 --replication-factor 3 \
  --config min.insync.replicas=2 \
  --bootstrap-server broker1:9092

# Replica placement across racks/DCs is automatic with CreateTopicPolicy
# or manual via replica assignment
```

Pros: single cluster, no offset translation, strong consistency.
Cons: cross-DC latency on every write (acks=all), requires low-latency interconnect (<10ms RTT).

### Pattern 4: Tiered Storage for Cost-Effective Retention

```properties
# Kafka 3.6+ tiered storage (early access)
remote.log.storage.system.enable=true
remote.log.storage.manager.class.name=org.apache.kafka.server.log.remote.storage.RemoteLogManagerConfig

# Move old segments to S3/GCS/Azure Blob
remote.log.storage.manager.impl.prefix=rsm.config.
rsm.config.s3.bucket.name=kafka-tiered-storage
rsm.config.s3.region=us-east-1

# Topic-level config
kafka-configs.sh --alter --topic orders \
  --add-config "remote.storage.enable=true,local.retention.ms=86400000,retention.ms=2592000000" \
  --bootstrap-server broker1:9092
# Local: 1 day, Total: 30 days (29 days on remote storage)
```

## Gotchas

- **Rolling upgrade order matters.** Always upgrade brokers one at a time, waiting for ISR recovery between each. Never upgrade all at once.
- **`inter.broker.protocol.version` must be set to the OLD version** before binary upgrade. Removing it after all brokers are upgraded enables new features.
- **Reassignment throttle is not removed automatically on failure.** If `--verify` shows "in progress" but nothing moves, check `leader.replication.throttled.rate` and `follower.replication.throttled.rate` on brokers.
- **MM2 topic naming.** Remote topics get prefixed (`dc-east.orders`). Consumers must subscribe to prefixed topic names on the standby cluster. This is not transparent.
- **Consumer lag after failover.** Even with MM2 checkpoint sync, consumer offsets may be slightly behind. Design consumers to be idempotent.
- **Page cache thrashing.** If consumers read very old data (catch-up reads), they evict recent data from page cache, degrading real-time consumers. Use tiered storage or separate read-only followers for historical reads.
- **Heap > 8 GB causes long GC pauses.** Kafka stores minimal state in heap. Extra RAM is better spent on page cache.
- **`UnderReplicatedPartitions > 0` does not always mean broker failure.** Can be caused by slow disks, network saturation, or GC pauses. Check `IsrShrinksPerSec` correlation with GC logs.
- **Partition reassignment saturates network** if not throttled. Always use `--throttle` flag. Start with 50 MB/s and increase.
- **Do not shrink partition count.** Kafka does not support reducing partitions. Only increase. Plan partition count carefully upfront. See [[topics-and-partitions]].

## Quick Reference

```bash
# --- Cluster health ---
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --status
kafka-topics.sh --describe --under-replicated-partitions --bootstrap-server broker1:9092
kafka-topics.sh --describe --unavailable-partitions --bootstrap-server broker1:9092

# --- Broker API versions (check version compatibility) ---
kafka-broker-api-versions.sh --bootstrap-server broker1:9092

# --- Partition reassignment ---
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --topics-to-move-json-file topics.json --broker-list "1,2,3,4" --generate
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassign.json --execute --throttle 50000000
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassign.json --verify

# --- Leader election ---
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type PREFERRED --all-topic-partitions

# --- Log dirs (disk usage per partition) ---
kafka-log-dirs.sh --describe --bootstrap-server broker1:9092 --topic-list orders

# --- Consumer lag ---
kafka-consumer-groups.sh --bootstrap-server broker1:9092 --describe --group my-group
kafka-consumer-groups.sh --bootstrap-server broker1:9092 --all-groups --describe

# --- Config dump ---
kafka-configs.sh --describe --all --entity-type brokers --entity-name 1 \
  --bootstrap-server broker1:9092
```

## See Also

- [[broker-architecture]] - internals, controller election, log storage, segment lifecycle
- [[topics-and-partitions]] - partition count planning, key-based routing, compaction
- [[consumer-groups]] - rebalance protocols, offset management, consumer lag semantics
- [[replication-and-fault-tolerance]] - ISR mechanics, acks semantics, unclean leader election
