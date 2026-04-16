---
title: Broker Architecture
category: concepts
tags: [kafka, broker, cluster, zookeeper, kraft, replication]
---

# Broker Architecture

A Kafka broker is a single server process that receives messages from producers, assigns offsets, persists data to disk, and serves fetch requests from consumers. A **cluster** is a group of brokers coordinating through a metadata layer (ZooKeeper or KRaft). This entry covers broker internals, controller election, partition leadership, replication mechanics, log storage, retention policies, and the KRaft migration path.

## Broker Role in a Cluster

Each broker in a cluster:
- Is identified by a unique integer `broker.id`
- Owns a subset of partitions (as leader or follower)
- Accepts TCP connections on `listeners` (PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL)
- Stores partition data under `log.dirs` as append-only segment files
- Reports metadata to the controller and receives partition assignments

A minimal production cluster requires **3 brokers** (to tolerate 1 failure with `replication.factor=3` and `min.insync.replicas=2`).

```php
Producer --> Broker 0 (leader P0)  --> Broker 1 (follower P0, leader P1)
                                   --> Broker 2 (follower P0, follower P1)
```

Brokers are **stateless with respect to consumers** -- they do not track consumer offsets internally (offsets are stored in the `__consumer_offsets` topic). See [[consumer-groups]].

## Controller Election

### ZooKeeper Mode (legacy, deprecated since Kafka 3.3)

One broker in the cluster is elected as the **controller**. It is responsible for:
- Detecting broker failures (via ZooKeeper session expiry)
- Reassigning partition leadership when a leader broker goes down
- Propagating metadata changes (new topics, partition reassignments) to all brokers

Election mechanism:
1. Each broker attempts to create an **ephemeral ZNode** `/controller` in ZooKeeper on startup
2. The first broker to succeed becomes the controller
3. Other brokers set a **watch** on the `/controller` ZNode
4. When the controller dies, ZooKeeper deletes the ephemeral node, triggering a watch event
5. Remaining brokers race to create the node again -- winner becomes the new controller

```bash
# ZooKeeper znodes used by Kafka
/brokers/ids/[broker_id]      # ephemeral - broker registration
/controller                    # ephemeral - current controller
/brokers/topics/[topic]        # persistent - topic metadata
/admin/reassign_partitions     # persistent - reassignment state
```

**Limitations**: ZooKeeper becomes a bottleneck at scale (>200k partitions). Metadata propagation is asynchronous, causing split-brain windows during controller failover.

### KRaft Mode (Kafka Raft -- production-ready since Kafka 3.6)

KRaft replaces ZooKeeper with an internal Raft-based consensus protocol. Controller nodes form a **quorum** that manages cluster metadata as a replicated log (`__cluster_metadata` topic).

Key differences from ZooKeeper mode:

| Aspect | ZooKeeper | KRaft |
|--------|-----------|-------|
| External dependency | ZooKeeper ensemble (3-5 nodes) | None |
| Metadata storage | ZooKeeper znodes | `__cluster_metadata` internal topic |
| Controller election | Ephemeral znode race | Raft leader election |
| Max partitions per cluster | ~200k practical limit | Millions (tested at 2M+) |
| Shutdown/startup | Slow (full metadata reload from ZK) | Fast (log replay) |
| Config | `zookeeper.connect` | `controller.quorum.voters` |

KRaft node roles:
- **Controller-only** (`process.roles=controller`): participates in metadata quorum, does not serve client data
- **Broker-only** (`process.roles=broker`): serves produce/fetch, receives metadata from controllers
- **Combined** (`process.roles=broker,controller`): both roles on one JVM (suitable for small clusters, not recommended for production >10 nodes)

```properties
# KRaft controller configuration
process.roles=controller
node.id=1
controller.quorum.voters=1@controller1:9093,2@controller2:9093,3@controller3:9093
controller.listener.names=CONTROLLER
listeners=CONTROLLER://controller1:9093
log.dirs=/var/kafka/controller-logs
```

```properties
# KRaft broker configuration
process.roles=broker
node.id=101
controller.quorum.voters=1@controller1:9093,2@controller2:9093,3@controller3:9093
listeners=PLAINTEXT://broker1:9092
log.dirs=/var/kafka/data
```

Ref: [KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)

## Partition Leadership and ISR

### Leader and Followers

Every partition has exactly **one leader** and zero or more **followers**. The leader:
- Handles all produce and fetch requests for that partition
- Assigns monotonically increasing offsets to incoming records
- Maintains the **High Watermark (HW)** -- the offset up to which all ISR members have replicated

Followers:
- Issue fetch requests to the leader (same protocol as consumers)
- Replicate records in order
- Do **not** serve client reads (in standard mode; see KIP-392 for follower fetching)

### In-Sync Replicas (ISR)

The ISR is the dynamic set of replicas that are "caught up" with the leader. A replica falls out of the ISR if it has not fetched from the leader within `replica.lag.time.max.ms` (default: 30s).

```sql
Partition P0:
  Leader: Broker 0  (offset 1000, HW=998)
  ISR: [0, 1, 2]
  Broker 1: offset 998 (in sync)
  Broker 2: offset 998 (in sync)
  Broker 3: offset 950 (OUT of sync -- lagging, removed from ISR)
```

**Committed record**: a record is committed (visible to consumers) only when **all ISR members** have acknowledged it. The High Watermark advances accordingly.

### Replication Factor

Set per-topic at creation time:

```bash
kafka-topics.sh --create \
  --topic orders \
  --partitions 12 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092
```

Rules of thumb:
- `replication.factor=3` is standard for production
- **Must be <= number of brokers** in the cluster
- Higher RF increases durability but costs disk and network

### min.insync.replicas

Controls the minimum number of replicas that must acknowledge a write before the producer receives success (when `acks=all`):

```properties
# Topic-level or broker-level config
min.insync.replicas=2
```

With `replication.factor=3` and `min.insync.replicas=2`:
- Writes succeed if at least 2 replicas (including leader) are in-sync
- If ISR shrinks to 1, produces with `acks=all` get `NotEnoughReplicasException`
- This guarantees **no data loss** as long as at least 1 of the 2 acknowledged replicas survives

**Gotcha**: `min.insync.replicas` has no effect unless the producer sets `acks=all` (or `acks=-1`). With `acks=1`, only the leader acknowledges.

See [[kafka-fault-tolerance]] for leader election, unclean leader election, and failure scenarios.

## Log Segments and Storage

### On-Disk Layout

Each partition is stored as a directory on the broker's filesystem:

```text
/var/kafka/data/
  orders-0/                          # topic "orders", partition 0
    00000000000000000000.log         # segment file (records)
    00000000000000000000.index        # offset index
    00000000000000000000.timeindex    # timestamp index
    00000000000000123456.log         # next segment (starts at offset 123456)
    00000000000000123456.index
    00000000000000123456.timeindex
    leader-epoch-checkpoint
    partition.metadata
```

- **.log**: the actual message data (batch-compressed with the configured `compression.type`)
- **.index**: sparse offset-to-position index (maps logical offsets to byte positions in `.log`)
- **.timeindex**: sparse timestamp-to-offset index (enables time-based lookups)

### Segment Rolling

A new segment is created when any of these conditions is met:

| Config | Default | Triggers new segment when... |
|--------|---------|------------------------------|
| `log.segment.bytes` | 1 GB (`1073741824`) | Current segment reaches this size |
| `log.roll.ms` / `log.roll.hours` | 7 days (`168` hours) | Time since segment creation exceeds this |
| `log.index.size.max.bytes` | 10 MB | Index file reaches this size |

Only the **active segment** (the latest one) is being written to. Older segments are immutable and eligible for retention/compaction.

```properties
# Smaller segments = more frequent rolling, finer retention granularity
log.segment.bytes=536870912    # 512 MB
log.roll.hours=24              # roll daily
```

### Zero-Copy Transfer

Kafka uses `sendfile()` (zero-copy) to transfer data from disk to network socket, bypassing userspace buffers. This is why Kafka achieves high throughput with minimal CPU overhead. Zero-copy works only when SSL is **not** enabled on the broker listener.

## Retention Policies

Kafka supports three retention strategies, configured per-topic or at broker level.

### Time-Based Retention (default)

Delete segments older than the retention period:

```properties
log.retention.hours=168         # 7 days (default)
log.retention.minutes=10080     # equivalent, finer granularity
log.retention.ms=604800000      # equivalent, finest granularity
# Precedence: ms > minutes > hours
```

The broker's log cleaner thread checks periodically (`log.retention.check.interval.ms`, default 5 min) whether any **closed segments** have a max timestamp older than the retention period. If so, the segment is deleted.

**Important**: retention applies to whole segments, not individual records. A record may live longer than `log.retention.hours` if it is in the active segment that has not rolled yet.

### Size-Based Retention

Delete oldest segments when partition log exceeds a total size:

```properties
log.retention.bytes=10737418240  # 10 GB per partition
# -1 = no size limit (default)
```

Can be combined with time-based retention -- whichever triggers first wins.

### Log Compaction

Retains only the **latest value for each key** within a partition. Used for changelog/snapshot topics (e.g., `__consumer_offsets`, KTable state stores).

```properties
log.cleanup.policy=compact       # or "delete,compact" for both
log.cleaner.min.compaction.lag.ms=0
log.cleaner.min.cleanable.ratio=0.5
```

Compaction process:
1. The **log cleaner** thread builds an in-memory offset map (key hash -> latest offset)
2. Reads the "dirty" (uncompacted) portion of the log
3. Copies records, skipping any key whose latest offset is in a newer segment
4. Records with `null` value (tombstones) are retained for `delete.retention.ms` (default 24h) then removed

```text
Before compaction:        After compaction:
offset  key  value        offset  key  value
0       A    v1           2       A    v3
1       B    v1           3       B    v2
2       A    v3           (tombstone B removed after delete.retention.ms)
3       B    v2
4       B    null (tombstone)
```

**Gotcha**: compacted topics must have non-null keys. Records with null keys are rejected if `log.cleanup.policy=compact`.

See [[topics-and-partitions]] for topic-level config overrides.

## Key Broker Configurations

### Critical Production Settings

```properties
# --- Identity & Networking ---
broker.id=1                              # unique per broker
listeners=PLAINTEXT://0.0.0.0:9092       # bind address
advertised.listeners=PLAINTEXT://broker1.example.com:9092  # client-facing address

# --- Storage ---
log.dirs=/data/kafka1,/data/kafka2       # comma-separated for JBOD
num.partitions=6                         # default partitions for auto-created topics
default.replication.factor=3             # default RF for auto-created topics

# --- Replication ---
min.insync.replicas=2                    # require 2 ISR acks with acks=all
replica.lag.time.max.ms=30000            # ISR eviction threshold
replica.fetch.max.bytes=1048576          # max bytes per replica fetch

# --- Retention ---
log.retention.hours=168                  # 7 days
log.retention.bytes=-1                   # unlimited size
log.segment.bytes=1073741824             # 1 GB segments
log.retention.check.interval.ms=300000   # check every 5 min

# --- Performance ---
num.io.threads=8                         # threads for disk I/O
num.network.threads=3                    # threads for network requests
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
num.replica.fetchers=1                   # increase for high-partition counts

# --- Topic Management ---
auto.create.topics.enable=false          # ALWAYS disable in production
delete.topic.enable=true                 # allow topic deletion
```

### Config Hierarchy

Kafka configs can be set at multiple levels. More specific overrides less specific:

1. **Per-topic dynamic config** (highest priority): `kafka-configs.sh --alter --topic X`
2. **Per-broker dynamic config**: `kafka-configs.sh --alter --entity-type brokers --entity-name 0`
3. **Cluster-wide dynamic config**: `kafka-configs.sh --alter --entity-type brokers --entity-default`
4. **Static broker config** (`server.properties`): requires broker restart

```bash
# Set topic-level retention to 3 days (overrides broker default)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --entity-type topics --entity-name orders \
  --add-config retention.ms=259200000

# Set broker-level default partitions dynamically (no restart)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --entity-type brokers --entity-default \
  --add-config num.partitions=12
```

## KRaft Migration from ZooKeeper

Migration path for existing ZooKeeper-based clusters (supported since Kafka 3.6, ZooKeeper fully removed in Kafka 4.0):

### Step-by-Step Migration

```hcl
Phase 1: Deploy KRaft controllers alongside existing ZK cluster
Phase 2: Migrate metadata (brokers dual-write to ZK and KRaft)
Phase 3: Switch brokers to KRaft mode
Phase 4: Decommission ZooKeeper
```

**1. Provision KRaft controller nodes**

```properties
# New controller nodes (do NOT run on existing broker machines if possible)
process.roles=controller
node.id=3000    # use IDs that don't conflict with existing broker.id values
controller.quorum.voters=3000@ctrl1:9093,3001@ctrl2:9093,3002@ctrl3:9093
controller.listener.names=CONTROLLER
listeners=CONTROLLER://ctrl1:9093
```

**2. Format controller storage**

```bash
# Generate a cluster ID from the existing ZK cluster
CLUSTER_ID=$(kafka-metadata.sh --snapshot /var/kafka/data/__cluster_metadata-0/00000000000000000000.log --cluster-id)
# Or from ZooKeeper directly:
CLUSTER_ID=$(zookeeper-shell.sh localhost:2181 get /cluster/id | grep version | jq -r .id)

# Format each controller's log directory
kafka-storage.sh format \
  --config /etc/kafka/kraft-controller.properties \
  --cluster-id $CLUSTER_ID
```

**3. Start controllers and begin migration**

```bash
# Start controller quorum
kafka-server-start.sh /etc/kafka/kraft-controller.properties

# Initiate migration on the ZK-based cluster -- enable dual-write
kafka-metadata.sh --bootstrap-controller ctrl1:9093 \
  --command-config admin.properties \
  migrate --start
```

**4. Roll brokers to KRaft mode**

For each broker (rolling restart):

```properties
# Remove ZK config, add KRaft config
# REMOVE: zookeeper.connect=zk1:2181,zk2:2181,zk3:2181
# ADD:
controller.quorum.voters=3000@ctrl1:9093,3001@ctrl2:9093,3002@ctrl3:9093
controller.listener.names=CONTROLLER
```

```bash
# Restart each broker one at a time
kafka-server-stop.sh
kafka-server-start.sh /etc/kafka/server.properties
```

**5. Finalize migration**

```bash
# After all brokers are on KRaft, finalize (stops dual-write to ZK)
kafka-metadata.sh --bootstrap-controller ctrl1:9093 \
  --command-config admin.properties \
  migrate --finalize
```

**6. Decommission ZooKeeper**

After finalization, ZooKeeper is no longer needed. Stop ZK nodes and remove them from infrastructure.

### Migration Gotchas

- **Do not skip Kafka versions**: migrate to 3.6+ first if on an older version, then migrate from ZK to KRaft
- **Controller node count**: always odd (3 or 5), same as ZooKeeper ensemble sizing
- **`node.id` conflicts**: controller node IDs must not overlap with existing broker IDs
- **ACLs**: if using ZK-based ACLs (`kafka.security.auth.SimpleAclAuthorizer`), switch to `kafka.security.authorizer.AclAuthorizer` (KRaft-compatible) before migration
- **Rollback**: possible only before `--finalize`. After finalization, rollback to ZK is not supported
- **Monitoring**: watch `kafka.controller:type=KafkaController,name=ActiveControllerCount` -- must be exactly 1 at all times

Ref: [Apache Kafka ZooKeeper to KRaft Migration Guide](https://kafka.apache.org/documentation/#kraft_zk_migration)

## Monitoring Broker Health

Key JMX metrics to monitor:

```markdown
# Cluster-level
kafka.controller:type=KafkaController,name=ActiveControllerCount  # must be 1
kafka.controller:type=KafkaController,name=OfflinePartitionsCount  # must be 0

# Broker-level
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions    # should be 0
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec             # spikes = trouble
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce  # p99 latency
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Fetch
kafka.log:type=LogFlushRateAndTimeMs                                # disk flush latency
```

**Alert thresholds**:
- `OfflinePartitionsCount > 0` -- immediate investigation
- `UnderReplicatedPartitions > 0` for >5 min -- broker likely overloaded or failing
- `IsrShrinksPerSec` sustained -- check disk I/O, network, GC pauses

## Cross-References

- [[topics-and-partitions]] -- partition assignment strategies, key-based routing, partition count sizing
- [[consumer-groups]] -- consumer offset management, rebalancing, group coordinator
- [[kafka-replication-fundamentals]] -- ISR, HW/LEO, acks + min.insync.replicas
- [[kafka-fault-tolerance]] -- unclean leader election, rack-aware replication, preferred leader election

## External References

- [Apache Kafka Broker Configuration](https://kafka.apache.org/documentation/#brokerconfigs)
- [KIP-500: Replace ZooKeeper with KRaft](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)
- [KRaft Migration Guide](https://kafka.apache.org/documentation/#kraft_zk_migration)
- [Kafka Design: Log Storage](https://kafka.apache.org/documentation/#design_filesystem)
- [Kafka Design: Replication](https://kafka.apache.org/documentation/#replication)
