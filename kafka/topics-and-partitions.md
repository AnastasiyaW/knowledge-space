---
title: Topics and Partitions
category: concepts
tags: [kafka, topics, partitions, keys, ordering, segments]
---

# Topics and Partitions

A **topic** is Kafka's logical channel for organizing records. Physically, each topic is split into one or more **partitions** -- ordered, append-only, immutable log segments stored on broker disks. Partitions are the fundamental unit of parallelism, storage, and replication in Kafka. Every design decision in a Kafka deployment -- throughput, ordering guarantees, consumer scaling, data retention -- traces back to how topics and partitions are configured.

## Core Concepts

### Topic as Logical Channel

A topic is a named feed of records. Producers write to topics; consumers read from topics. Topics are identified by name and exist across the cluster -- they are not bound to a single broker.

- Topics can have any number of producers and consumers simultaneously
- Multiple [[consumer-groups]] can read the same topic independently, each tracking its own offsets
- Topics are created explicitly (`kafka-topics.sh --create`) or automatically when a producer first writes to them (if `auto.create.topics.enable=true` on the broker)
- Topic names support `[a-zA-Z0-9._-]`, max 249 characters. Avoid `.` and `_` in the same cluster -- Kafka uses both as internal separators in metric names

### Partition as Unit of Parallelism

Each partition is an independent, ordered log. Parallelism in Kafka scales with partition count:

```
Topic: user-events (4 partitions)

Partition 0:  [msg0] [msg1] [msg2] [msg3] ...
Partition 1:  [msg0] [msg1] [msg2] ...
Partition 2:  [msg0] [msg1] [msg2] [msg3] [msg4] ...
Partition 3:  [msg0] [msg1] ...
```

- Each partition has its own offset sequence starting at 0
- A [[consumer-groups|consumer group]] can have at most one consumer per partition -- so partition count is the upper bound on consumer parallelism
- Each partition has one **leader** replica (handles all reads/writes) and zero or more **follower** replicas (passive replication)
- Partitions are distributed across brokers in the cluster -- see [[broker-architecture]]

### Message Ordering Guarantees

**Kafka guarantees ordering only within a single partition.** There is no global ordering across partitions.

```
Partition 0:  A -> B -> C        (order guaranteed: A before B before C)
Partition 1:  D -> E -> F        (order guaranteed: D before E before F)

Cross-partition: no guarantee on relative order of A vs D
```

If you need strict ordering for a set of related records (e.g., all events for a single user), you must route them to the same partition using a consistent key.

With `max.in.flight.requests.per.connection > 1` (default: 5), out-of-order delivery is possible even within a partition if retries occur. To guarantee per-partition ordering with retries:
- Use an idempotent producer (`enable.idempotence=true`, default since Kafka 3.0) -- this handles reordering internally
- Or set `max.in.flight.requests.per.connection=1` (reduces throughput)

See [[producer-patterns]] for idempotent and transactional producer configuration.

### Key-Based Partitioning

The producer determines the target partition for each record:

**1. Keyed messages (DefaultPartitioner)**:

```python
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

# All records with key="user-42" go to the same partition
# Partition = murmur2(key_bytes) % num_partitions
producer.produce("user-events", key="user-42", value="login")
producer.produce("user-events", key="user-42", value="purchase")  # Same partition
producer.flush()
```

The default partitioner applies `murmur2` hash to the serialized key bytes, then takes modulo by partition count. This is deterministic: same key always maps to the same partition (as long as partition count does not change).

**2. Null keys = round-robin / sticky**:

```python
# No key -> round-robin distribution (pre-2.4) or sticky partitioner (2.4+)
producer.produce("metrics", value="cpu=80%")
producer.produce("metrics", value="mem=60%")  # May go to a different partition
```

Since Kafka 2.4, the **sticky partitioner** is the default for null-key records: the producer "sticks" to one partition until the current batch is full or `linger.ms` expires, then switches. This improves batching efficiency over pure round-robin.

**3. Custom partitioner**:

```python
from confluent_kafka import Producer

def region_partitioner(key, partitions, _):
    """Route by region prefix in key: 'us-east:user-42' -> hash only region."""
    if key is None:
        return None  # Fall back to default
    region = key.split(b":")[0]
    return hash(region) % len(partitions)

# confluent-kafka doesn't directly support custom partitioner callbacks
# in Python -- use the Java client or implement key prefixing with
# default partitioner. For Python, a common workaround:
# encode routing info into the key itself.
```

In Java:

```java
public class RegionPartitioner implements Partitioner {
    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        int numPartitions = partitions.size();
        if (keyBytes == null) return ThreadLocalRandom.current().nextInt(numPartitions);
        String region = new String(keyBytes).split(":")[0];
        return Utils.toPositive(Utils.murmur2(region.getBytes())) % numPartitions;
    }
}
```

### Partition Storage: Segments

Each partition is stored as a directory on the broker's log directory. Inside, data is split into **segments**:

```
/kafka-logs/user-events-0/
    00000000000000000000.log        # Segment file (records)
    00000000000000000000.index      # Offset -> file position index
    00000000000000000000.timeindex  # Timestamp -> offset index
    00000000000000523417.log        # Next segment (starts at offset 523417)
    00000000000000523417.index
    00000000000000523417.timeindex
    leader-epoch-checkpoint
    partition.metadata
```

- The **active segment** is the one currently being written to
- Segment rotation occurs when `segment.bytes` (default: 1 GB) is reached or `segment.ms` (default: 7 days) elapses
- Only **closed (inactive) segments** are eligible for deletion or compaction
- Smaller segments = more frequent cleanup but more file handles; larger segments = delayed cleanup

### Partition Reassignment

Partitions can be moved between brokers for load balancing or during broker decommission.

**Generate reassignment plan**:
```bash
# Create a JSON file listing topics to reassign
cat > topics.json << 'EOF'
{"topics": [{"topic": "user-events"}], "version": 1}
EOF

# Generate a reassignment plan (move to brokers 1, 2, 3)
kafka-reassign-partitions.sh --generate \
  --topics-to-move-json-file topics.json \
  --broker-list "1,2,3" \
  --bootstrap-server localhost:9092
```

**Execute reassignment**:
```bash
# Save the generated plan to reassignment.json, then execute
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file reassignment.json \
  --bootstrap-server localhost:9092

# Monitor progress
kafka-reassign-partitions.sh --verify \
  --reassignment-json-file reassignment.json \
  --bootstrap-server localhost:9092
```

**Throttle reassignment** to limit replication bandwidth:
```bash
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file reassignment.json \
  --throttle 50000000 \
  --bootstrap-server localhost:9092
# 50 MB/s throttle -- prevents reassignment from saturating network
```

### Preferred Leader Election

Each partition has a **preferred leader** -- the first broker in the replica list. Over time, leaders can shift (broker restarts, failures). To rebalance leadership:

```bash
# Trigger preferred leader election for all partitions
kafka-leader-election.sh --election-type PREFERRED --all-topic-partitions \
  --bootstrap-server localhost:9092

# For a specific topic
kafka-leader-election.sh --election-type PREFERRED \
  --topic user-events \
  --bootstrap-server localhost:9092

# Unclean leader election (risk of data loss -- only for non-critical topics)
kafka-leader-election.sh --election-type UNCLEAN \
  --topic user-events --partition 0 \
  --bootstrap-server localhost:9092
```

`auto.leader.rebalance.enable=true` (default) triggers automatic preferred leader election when leader imbalance exceeds `leader.imbalance.percentage.per.broker` (default: 10%).

## Topic Configuration

### cleanup.policy

Controls how old data is removed from a topic.

| Policy | Behavior | Use Case |
|--------|----------|----------|
| `delete` (default) | Remove segments older than `retention.ms` or larger than `retention.bytes` | Event streams, logs, metrics |
| `compact` | Keep only the latest value per key; tombstone (null value) removes key | State snapshots, changelogs, caches |
| `compact,delete` | Compact first, then delete segments older than retention | Compacted topics with a retention ceiling |

**Compaction internals**:
- The log cleaner thread scans "dirty" (uncompacted) segments
- For each key, only the record with the highest offset survives
- A **tombstone** (key with null value) marks a key for deletion; removed after `delete.retention.ms` (default: 24h)
- `min.compaction.lag.ms` -- minimum time before a record is eligible for compaction (prevents compacting records that consumers haven't processed yet)
- `max.compaction.lag.ms` -- maximum time before compaction is guaranteed to run
- `min.cleanable.dirty.ratio` (default: 0.5) -- compaction starts when 50%+ of the log is dirty

```bash
# Create a compacted topic
kafka-topics.sh --create --topic user-profiles \
  --partitions 6 --replication-factor 3 \
  --config cleanup.policy=compact \
  --config min.compaction.lag.ms=3600000 \
  --config delete.retention.ms=86400000 \
  --bootstrap-server localhost:9092
```

### Retention Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retention.ms` | 604800000 (7 days) | Time-based retention; `-1` = infinite |
| `retention.bytes` | -1 (unlimited) | Size-based retention per partition |
| `segment.bytes` | 1073741824 (1 GB) | Max size of a single segment file |
| `segment.ms` | 604800000 (7 days) | Max time before active segment is rolled |
| `min.compaction.lag.ms` | 0 | Minimum delay before record is compactable |
| `max.compaction.lag.ms` | 9223372036854775807 | Maximum delay before compaction runs |
| `delete.retention.ms` | 86400000 (24h) | How long tombstones survive after compaction |
| `message.timestamp.type` | `CreateTime` | `CreateTime` (producer sets) or `LogAppendTime` (broker sets) |

Retention is evaluated per-segment, not per-record. A segment is deleted when **all** records in it exceed the retention threshold.

## Practical Patterns

### kafka-topics.sh Commands

**Create a topic**:
```bash
kafka-topics.sh --create --topic orders \
  --partitions 12 --replication-factor 3 \
  --config retention.ms=259200000 \
  --config cleanup.policy=delete \
  --bootstrap-server kafka1:9092
```

**Describe a topic** (partitions, replicas, ISR, configs):
```bash
kafka-topics.sh --describe --topic orders \
  --bootstrap-server kafka1:9092

# Output:
# Topic: orders  PartitionCount: 12  ReplicationFactor: 3  Configs: retention.ms=259200000
#   Topic: orders  Partition: 0  Leader: 1  Replicas: 1,2,3  Isr: 1,2,3
#   Topic: orders  Partition: 1  Leader: 2  Replicas: 2,3,1  Isr: 2,3,1
#   ...
```

**List all topics**:
```bash
kafka-topics.sh --list --bootstrap-server kafka1:9092

# Exclude internal topics
kafka-topics.sh --list --exclude-internal --bootstrap-server kafka1:9092
```

**Alter partition count** (increase only):
```bash
kafka-topics.sh --alter --topic orders --partitions 24 \
  --bootstrap-server kafka1:9092
# WARNING: breaks key-based partition assignment for existing keys
```

**Alter topic configs**:
```bash
# Using kafka-configs.sh (preferred for config changes)
kafka-configs.sh --alter --entity-type topics --entity-name orders \
  --add-config retention.ms=86400000,segment.bytes=536870912 \
  --bootstrap-server kafka1:9092

# Remove a config override (revert to broker default)
kafka-configs.sh --alter --entity-type topics --entity-name orders \
  --delete-config retention.ms \
  --bootstrap-server kafka1:9092

# Describe current configs
kafka-configs.sh --describe --entity-type topics --entity-name orders \
  --bootstrap-server kafka1:9092
```

**Delete a topic**:
```bash
kafka-topics.sh --delete --topic orders \
  --bootstrap-server kafka1:9092
# Requires delete.topic.enable=true on broker (default: true since Kafka 1.0)
# Deletion is asynchronous -- data is removed in the background
```

### Programmatic Topic Management (Python)

```python
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource

admin = AdminClient({"bootstrap.servers": "localhost:9092"})

# Create topic
topic = NewTopic(
    "user-events",
    num_partitions=12,
    replication_factor=3,
    config={
        "cleanup.policy": "compact,delete",
        "retention.ms": "604800000",
        "min.compaction.lag.ms": "3600000",
        "segment.bytes": "536870912",
    },
)
futures = admin.create_topics([topic])
for topic_name, future in futures.items():
    try:
        future.result()  # Block until complete
        print(f"Created topic: {topic_name}")
    except Exception as e:
        print(f"Failed to create {topic_name}: {e}")

# Describe topic config
resource = ConfigResource("TOPIC", "user-events")
futures = admin.describe_configs([resource])
for res, future in futures.items():
    configs = future.result()
    for key, config in configs.items():
        print(f"  {key} = {config.value}")

# List topics
metadata = admin.list_topics(timeout=10)
for topic_name in metadata.topics:
    print(f"Topic: {topic_name}, Partitions: {len(metadata.topics[topic_name].partitions)}")
```

### Partition Count Selection Heuristic

```
Target throughput:    100 MB/s
Per-partition write:  ~10 MB/s (single partition, single producer)
Consumer instances:   8 (in one consumer group)

Minimum partitions = max(100/10, 8) = 10
Recommended:         12 (round up, leave room for growth)
```

Start with fewer partitions and increase later. You cannot decrease partition count without recreating the topic.

## Gotchas

- **Increasing partitions breaks key affinity.** `murmur2(key) % 12` != `murmur2(key) % 24`. After increasing partitions, records with the same key may land in different partitions. If ordering matters, either plan partition count from the start or use a custom partitioner that handles growth.
- **Partition count cannot be decreased.** The only way to reduce is to create a new topic with fewer partitions and migrate data using MirrorMaker, Kafka Connect, or a consumer-producer bridge.
- **Compaction requires non-null keys.** If `cleanup.policy=compact`, every record must have a key. Null-key records will cause compaction to skip those records entirely.
- **Active segment is never deleted or compacted.** Retention and compaction only apply to closed segments. If `segment.bytes=1GB` and you produce 500 MB/day, the active segment won't roll for ~2 days, delaying cleanup.
- **Topic deletion is asynchronous and may leave state.** After `--delete`, partitions are marked for deletion but data removal happens in the background. The topic name becomes unavailable immediately, but disk space is reclaimed later.
- **`retention.bytes` is per-partition, not per-topic.** A topic with 12 partitions and `retention.bytes=1GB` can retain up to 12 GB total.
- **Unclean leader election risks data loss.** If `unclean.leader.election.enable=true` (default: false since Kafka 0.11), an out-of-sync replica can become leader, losing unreplicated messages.
- **Cross-partition joins require co-partitioning.** If you need to join two topics by key, both must have the same partition count and use the same partitioner. See [[consumer-groups]] for `RangeAssignor` requirements.

## Quick Reference

### Key Topic-Level Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cleanup.policy` | `delete` | `delete`, `compact`, or `compact,delete` |
| `retention.ms` | 604800000 (7d) | Time-based retention |
| `retention.bytes` | -1 | Per-partition size-based retention |
| `segment.bytes` | 1073741824 (1GB) | Segment file size |
| `segment.ms` | 604800000 (7d) | Max age of active segment |
| `min.compaction.lag.ms` | 0 | Min delay before compaction eligibility |
| `max.compaction.lag.ms` | MAX_LONG | Max delay before forced compaction |
| `delete.retention.ms` | 86400000 (24h) | Tombstone TTL after compaction |
| `min.cleanable.dirty.ratio` | 0.5 | Dirty log ratio to trigger compaction |
| `max.message.bytes` | 1048588 (~1MB) | Max record size for this topic |
| `min.insync.replicas` | 1 | ISR count required for `acks=all` |
| `unclean.leader.election.enable` | false | Allow out-of-sync replica as leader |
| `message.timestamp.type` | `CreateTime` | `CreateTime` or `LogAppendTime` |

### Essential CLI Commands

```bash
# Create
kafka-topics.sh --create --topic T --partitions N --replication-factor R \
  --bootstrap-server HOST:9092

# Describe
kafka-topics.sh --describe --topic T --bootstrap-server HOST:9092

# List
kafka-topics.sh --list --bootstrap-server HOST:9092

# Alter partitions (increase only)
kafka-topics.sh --alter --topic T --partitions N --bootstrap-server HOST:9092

# Alter configs
kafka-configs.sh --alter --entity-type topics --entity-name T \
  --add-config KEY=VALUE --bootstrap-server HOST:9092

# Delete
kafka-topics.sh --delete --topic T --bootstrap-server HOST:9092

# Preferred leader election
kafka-leader-election.sh --election-type PREFERRED --all-topic-partitions \
  --bootstrap-server HOST:9092

# Reassign partitions
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file plan.json --bootstrap-server HOST:9092
```

## Official Documentation

- [Topics and Logs](https://kafka.apache.org/documentation/#intro_topics) - core topic/partition model
- [Topic-Level Configs](https://kafka.apache.org/documentation/#topicconfigs) - full configuration reference
- [Log Compaction](https://kafka.apache.org/documentation/#compaction) - compaction semantics and guarantees
- [Operations: Adding/Removing Topics](https://kafka.apache.org/documentation/#basic_ops_add_topic) - CLI management
- [Partition Reassignment](https://kafka.apache.org/documentation/#basic_ops_partitionassignment) - rebalancing partitions across brokers

## See Also

- [[broker-architecture]] - how partitions map to brokers, ISR, controller election
- [[consumer-groups]] - partition assignment strategies, rebalancing, offset management
- [[producer-patterns]] - key serialization, idempotent producer, batching, acks
- [[topics-and-partitions]] - choosing partition count, replication factor, custom partitioners
- [[kafka-cluster-operations]] - day-to-day topic and cluster management
