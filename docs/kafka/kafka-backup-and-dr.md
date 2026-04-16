# Kafka Backup and Disaster Recovery

MirrorMaker 2 multi-DC replication, backup strategies (topic-level, filesystem, metadata), and disaster recovery patterns (active-passive, active-active, stretch cluster, tiered storage).

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

Kafka is not a database, but data loss scenarios exist.

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

```text
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

# RTO: 5-15 min (mostly DNS propagation + consumer group stabilization)
# RPO: seconds to minutes (depends on MM2 replication lag)
```

### Pattern 2: Active-Active with MM2

```text
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

- **MM2 topic naming.** Remote topics get prefixed (`dc-east.orders`). Consumers must subscribe to prefixed topic names on the standby cluster. This is not transparent.
- **Consumer lag after failover.** Even with MM2 checkpoint sync, consumer offsets may be slightly behind. Design consumers to be idempotent.
- **LVM snapshots on leader partitions are not guaranteed consistent.** The broker may be mid-write. Prefer snapshotting follower brokers or using `controlled.shutdown` first.
- **Metadata backup misses in-flight state.** Consumer group offsets exported via CLI are point-in-time; active consumers may have uncommitted offsets beyond what's exported.

## See Also

- [[kafka-cluster-management]] - sizing, upgrades, partition reassignment
- [[kafka-monitoring-and-tuning]] - JMX metrics, alerting, performance tuning
- [[kafka-replication-fundamentals]] - ISR, HW/LEO, replication model
- [[kafka-fault-tolerance]] - failure scenarios, multi-DC patterns, rack-aware replication
- [[mirrormaker]] - dedicated MirrorMaker deep-dive
