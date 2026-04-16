# Kafka Cluster Management

Cluster sizing, rolling upgrades, ZooKeeper-to-KRaft migration, disk failure handling, partition reassignment, and preferred leader election.

## Cluster Sizing

### Broker Count

Minimum 3 brokers for production (`replication.factor=3`, `min.insync.replicas=2` - tolerates 1 broker failure). Scale horizontally by adding brokers and reassigning partitions.

**Sizing formula:**

```toml
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

```toml
disk_per_broker = (write_throughput_MB_s * retention_seconds * replication_factor) / broker_count
                  + 20% overhead (compaction, index, snapshots)
```

XFS > ext4 for Kafka workloads. Mount with `noatime,nodiratime`. RAID-10 if using spinning disks; JBOD with multiple `log.dirs` preferred for SSDs (Kafka handles replica placement).

### Memory

Kafka relies on OS page cache, not JVM heap, for read performance.

```toml
total_RAM = JVM_heap + page_cache_for_active_segments
```

- JVM heap: 6 GB typical, 8 GB max (larger heaps = longer GC pauses)
- Page cache: enough to hold active segments for all partitions. A partition's active segment = `log.segment.bytes` (default 1 GB). If 1000 partitions: aim for ~32-64 GB page cache
- Total per broker: 64-128 GB RAM is common

### Network

```toml
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
echo "inter.broker.protocol.version=3.6" >> /opt/kafka/config/server.properties
echo "log.message.format.version=3.6" >> /opt/kafka/config/server.properties

# Step 2: Stop broker gracefully
sudo systemctl stop kafka
# Wait for "controlled shutdown complete" in logs

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

# Step 2: Save proposed assignment to file
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

## Quick Reference

```bash
# --- Cluster health ---
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --status
kafka-topics.sh --describe --under-replicated-partitions --bootstrap-server broker1:9092
kafka-topics.sh --describe --unavailable-partitions --bootstrap-server broker1:9092

# --- Broker API versions ---
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

# --- Config dump ---
kafka-configs.sh --describe --all --entity-type brokers --entity-name 1 \
  --bootstrap-server broker1:9092
```

## Gotchas

- **Rolling upgrade order matters.** Always upgrade brokers one at a time, waiting for ISR recovery between each. Never upgrade all at once.
- **`inter.broker.protocol.version` must be set to the OLD version** before binary upgrade. Removing it after all brokers are upgraded enables new features.
- **Reassignment throttle is not removed automatically on failure.** If `--verify` shows "in progress" but nothing moves, check `leader.replication.throttled.rate` and `follower.replication.throttled.rate` on brokers.
- **Partition reassignment saturates network** if not throttled. Always use `--throttle` flag. Start with 50 MB/s and increase.
- **Do not shrink partition count.** Kafka does not support reducing partitions. Only increase. Plan partition count carefully upfront. See [[topics-and-partitions]].

## See Also

- [[kafka-monitoring-and-tuning]] - JMX metrics, Prometheus setup, OS/JVM/broker tuning
- [[kafka-backup-and-dr]] - backup strategies, MirrorMaker 2, disaster recovery patterns
- [[broker-architecture]] - internals, controller election, log storage, segment lifecycle
- [[topics-and-partitions]] - partition count planning, key-based routing, compaction
- [[kafka-replication-fundamentals]] - ISR mechanics, acks semantics, unclean leader election
