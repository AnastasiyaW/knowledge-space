---
title: Replication and Fault Tolerance
category: concepts
tags: [kafka, replication, ISR, leader, follower, high-availability, min-insync-replicas, unclean-leader-election]
---

# Replication and Fault Tolerance

Every Kafka partition is replicated across multiple brokers. One replica is the **leader** (handles all produce and fetch requests), the rest are **followers** (passively pull data from the leader). Replication is the core mechanism for durability and availability -- a broker can die and no data is lost, no downtime is visible to clients, as long as a sufficient number of replicas remain in sync.

## Leader-Follower Replication Model

### How It Works

```
Producer --produce--> Broker 0 (Leader, Partition 0)
                         |
                    fetch request
                    (follower pull)
                         |
                   +-----+-----+
                   v           v
              Broker 1      Broker 2
             (Follower)    (Follower)
```

- Followers issue `Fetch` requests to the leader, identical to consumer fetches but on a separate replication channel
- Followers write fetched data to their own local log in the same order
- There is **no push** from leader to followers -- followers pull at their own pace
- Leadership is per-partition: a single broker is typically leader for some partitions and follower for others
- The controller (ZooKeeper or KRaft quorum) assigns leadership; see [[broker-architecture]]

### Replication Factor

Set at topic creation time. Cannot be increased beyond the number of brokers.

```bash
# Create topic with replication factor 3
kafka-topics.sh --create --topic orders \
  --partitions 12 --replication-factor 3 \
  --bootstrap-server localhost:9092

# Verify replica assignment
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Output:
# Topic: orders  Partition: 0  Leader: 1  Replicas: 1,2,3  Isr: 1,2,3
# Topic: orders  Partition: 1  Leader: 2  Replicas: 2,3,1  Isr: 2,3,1
```

**Recommendations by use case:**

| Use Case | Replication Factor | min.insync.replicas | Rationale |
|----------|-------------------|---------------------|-----------|
| Dev/test | 1 | 1 | No durability needed |
| Standard production | 3 | 2 | Tolerate 1 broker failure, no data loss |
| Critical financial data | 3 | 2 | Same, but with `acks=all` enforced |
| Large cluster (>10 brokers) | 3 | 2 | RF=3 is sufficient; RF=5 wastes disk |
| Multi-AZ (3 AZs) | 3 | 2 | One replica per AZ, survive full AZ loss |
| Two-datacenter stretch | 4 | 3 | 2 replicas per DC, survive full DC loss |

RF=2 is a common mistake. With `min.insync.replicas=2`, a single follower failure makes the partition read-only. With `min.insync.replicas=1`, a single broker loss risks data loss. **Always use RF >= 3 in production.**

## In-Sync Replicas (ISR)

The ISR set is the subset of replicas that are considered "caught up" with the leader. Only ISR members are eligible for leader election (unless `unclean.leader.election.enable=true`).

### ISR Membership Criteria

A replica stays in the ISR as long as:
1. It has fetched up to the leader's **Log End Offset (LEO)** within `replica.lag.time.max.ms` (default: 30000ms = 30s)
2. It maintains an active session with the controller (heartbeats)

```properties
# Key broker configs controlling ISR behavior
replica.lag.time.max.ms=30000        # Max time before follower is removed from ISR
# (Kafka < 0.9 also had replica.lag.max.messages -- REMOVED, do not use)
```

**ISR shrink/expand flow:**

```
t=0:  ISR = {0, 1, 2}     # All replicas caught up
t=5:  Broker 2 goes slow (GC pause, disk I/O, network)
t=35: Broker 2 hasn't fetched within 30s
      Leader removes Broker 2 from ISR
      ISR = {0, 1}         # Shrunk ISR
t=40: Broker 2 catches up, fetches to leader's LEO
      Leader adds Broker 2 back to ISR
      ISR = {0, 1, 2}     # Expanded ISR
```

**Monitoring ISR shrinks** is critical -- it signals broker health issues before failures occur.

```bash
# Check under-replicated partitions (ISR < replication factor)
kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server localhost:9092

# JMX metrics to monitor
# kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions  (should be 0)
# kafka.server:type=ReplicaManager,name=IsrShrinksPerSec
# kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
```

## High Watermark (HW) vs Log End Offset (LEO)

Two offset markers govern what data is visible and what is replicated:

```
Partition Log (Leader):

Offset:  0   1   2   3   4   5   6   7   8
         [A] [B] [C] [D] [E] [F] [G] [H] [I]
                           ^               ^
                           HW              LEO
                           (committed)     (latest written)

Messages 0-4: committed (replicated to all ISR members)
Messages 5-8: uncommitted (only on leader, not yet fully replicated)
```

| Concept | Definition | Who maintains it |
|---------|-----------|-----------------|
| **LEO (Log End Offset)** | Offset of the next message to be written. Each replica has its own LEO. | Each replica independently |
| **HW (High Watermark)** | The highest offset replicated to **all** ISR members. Only messages below HW are visible to consumers. | Leader calculates, propagates to followers via fetch responses |

### How HW Advances

1. Producer writes message at offset 8 to the leader. Leader LEO = 9.
2. Follower 1 fetches up to offset 8. Follower 1 LEO = 9.
3. Follower 2 fetches up to offset 8. Follower 2 LEO = 9.
4. Leader sees all ISR members have LEO >= 9. Leader advances HW to 9.
5. Next fetch responses carry the new HW to followers. Followers advance their local HW.

**Consumer visibility**: consumers can only read up to `HW - 1`. This prevents consumers from reading data that might be lost if the leader crashes before followers replicate it.

### Leader Epoch (KIP-101)

The **leader epoch** is a monotonically increasing integer that increments each time a new leader is elected for a partition. It solves the **log divergence problem** that HW alone cannot handle:

```
Scenario without leader epoch:
1. Leader (Broker 0) writes offset 5, HW=4 (follower hasn't fetched yet)
2. Leader crashes
3. Follower (Broker 1) becomes leader, HW=4, LEO=5 (has offset 4, not 5)
4. New leader writes a DIFFERENT message at offset 5
5. Old leader comes back -- its offset 5 conflicts with new leader's offset 5

With leader epoch:
- Each leader election bumps epoch: epoch 0 -> epoch 1
- Recovering broker asks new leader: "What was the LEO at end of epoch 0?"
- New leader responds: "LEO was 5 at epoch 0"
- Recovering broker truncates its log to offset 5, then fetches from new leader
- No divergence
```

```properties
# Leader epoch checkpoint file on each broker (automatic, no config needed)
# $LOG_DIR/leader-epoch-checkpoint
# Format: leader_epoch start_offset
# 0  0
# 1  5
# 2  12
```

## Committed vs Uncommitted Messages

A message is **committed** when it has been replicated to all ISR replicas. Only committed messages are consumable.

```
                    acks=0     acks=1      acks=all
                    ------     ------      --------
Producer sends      fire&forget leader ACK  all ISR ACK
Leader writes       yes        yes         yes
Followers replicate maybe      maybe       yes (before ACK)
Message committed?  maybe      maybe       yes
Data loss risk      HIGH       MEDIUM      NONE*

* with min.insync.replicas >= 2
```

### acks + min.insync.replicas Interaction Matrix

This is the most critical configuration matrix for Kafka durability:

```properties
# Producer config
acks=all                  # -1 is equivalent
# Broker/topic config
min.insync.replicas=2     # Minimum ISR members to accept a write
```

| acks | min.insync.replicas | Replication Factor | Behavior |
|------|--------------------|--------------------|----------|
| `0` | any | any | Producer does not wait for ACK. Max throughput, no durability guarantee. Fire-and-forget. |
| `1` | any | any | Producer waits for leader ACK only. Data loss if leader dies before followers replicate. |
| `all` | `1` | 3 | Producer waits for all ISR. But ISR can shrink to leader only -- then `acks=all` = `acks=1`. **False sense of safety.** |
| `all` | `2` | 3 | Producer waits for all ISR. ISR must have >= 2 members or writes are rejected with `NotEnoughReplicasException`. **Recommended production setting.** |
| `all` | `3` | 3 | Producer waits for all 3 replicas. Any single broker failure blocks writes. **Too strict for most use cases.** |

**The golden rule**: `acks=all` + `min.insync.replicas=2` + `replication.factor=3`. This tolerates 1 broker failure without data loss and without blocking writes.

```python
from confluent_kafka import Producer

# Production-grade producer config for durability
producer = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092,broker3:9092",
    "acks": "all",                            # Wait for all ISR replicas
    "enable.idempotence": True,               # Exactly-once per partition
    "max.in.flight.requests.per.connection": 5,  # Safe with idempotence
    "retries": 2147483647,                    # Infinite retries (bounded by delivery.timeout.ms)
    "delivery.timeout.ms": 120000,            # 2 min total timeout
    "linger.ms": 5,                           # Batch for 5ms
    "batch.size": 65536,                      # 64KB batch
})

# Topic-level config
# kafka-configs.sh --alter --topic orders \
#   --add-config min.insync.replicas=2 \
#   --bootstrap-server localhost:9092
```

### What Happens When ISR Shrinks Below min.insync.replicas

```
Scenario: RF=3, min.insync.replicas=2, acks=all

1. Normal: ISR={0,1,2}, writes succeed
2. Broker 2 dies: ISR={0,1}, writes succeed (2 >= min.insync)
3. Broker 1 dies: ISR={0}, writes FAIL with NotEnoughReplicasException
   - Partition is READABLE but NOT WRITABLE
   - Consumers continue reading committed data
   - Producers get errors until ISR recovers
4. Broker 1 returns: ISR={0,1}, writes resume
```

## Unclean Leader Election

When all ISR replicas are down, Kafka faces a choice: **availability vs data integrity**.

```properties
# Broker config (default: false since Kafka 0.11.0.0)
unclean.leader.election.enable=false
```

| Setting | Behavior | Tradeoff |
|---------|----------|----------|
| `false` (default) | Partition stays offline until an ISR member recovers | **No data loss**, but unavailability |
| `true` | An out-of-sync replica can become leader | **Data loss** (messages not replicated to this replica are gone), but availability |

**When to enable unclean leader election:**
- Metrics/logs/clickstream where availability > durability
- Topics that can be rebuilt from source systems
- **Never** for financial transactions, orders, audit logs

```properties
# Set per-topic for granular control
kafka-configs.sh --alter --topic clickstream \
  --add-config unclean.leader.election.enable=true \
  --bootstrap-server localhost:9092

# Keep default (false) for critical topics
kafka-configs.sh --alter --topic payments \
  --add-config unclean.leader.election.enable=false \
  --bootstrap-server localhost:9092
```

### Data Loss Mechanics with Unclean Election

```
Leader (Broker 0):    [0] [1] [2] [3] [4] [5] [6] [7]   LEO=8, HW=6
Follower (Broker 1):  [0] [1] [2] [3] [4] [5]            LEO=6  (in ISR)
Follower (Broker 2):  [0] [1] [2] [3]                     LEO=4  (out of ISR)

Broker 0 and Broker 1 crash simultaneously.

unclean.leader.election.enable=false:
  Partition offline. Wait for Broker 0 or 1 to recover.

unclean.leader.election.enable=true:
  Broker 2 becomes leader with LEO=4.
  Messages at offsets 4,5 (committed!) are LOST.
  Messages at offsets 6,7 (uncommitted) are LOST.
  New writes start at offset 4.
```

## Preferred Replica Election

Kafka assigns a **preferred leader** for each partition (the first broker in the replica list). Over time, after failures and recoveries, leadership may drift so that some brokers carry more leader load than others.

```bash
# Check current vs preferred leaders
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Replicas: 1,2,3  <-- first in list (1) is preferred leader
# Leader: 2        <-- actual leader is 2 (leadership drifted)

# Trigger preferred replica election
kafka-leader-election.sh --election-type PREFERRED \
  --topic orders --partition 0 \
  --bootstrap-server localhost:9092

# Auto-balance (broker config)
auto.leader.rebalance.enable=true           # default: true
leader.imbalance.check.interval.seconds=300 # default: 300 (5 min)
leader.imbalance.per.broker.percentage=10   # default: 10%
```

**How auto-rebalance works:**
1. Every `leader.imbalance.check.interval.seconds`, the controller checks each broker
2. If a broker's leader imbalance exceeds `leader.imbalance.per.broker.percentage`, the controller triggers preferred leader elections for the imbalanced partitions
3. This only works if the preferred leader is in the ISR

## Observer Replicas (KIP-392)

Observer replicas are **non-voting** replicas that replicate data but are **never added to the ISR** and **never eligible for leader election**. They serve read-only consumer fetches.

```
Producer --> Leader (Broker 0, DC-East)
                |
         +------+------+
         v             v
    Follower       Observer
    (Broker 1,     (Broker 3,
     DC-East)      DC-West)
     [ISR]         [NOT in ISR,
                    never votes]
```

Use cases:
- **Cross-DC reads**: consumers in DC-West read from the local observer, reducing cross-DC latency
- **Offload read traffic**: observer handles consumer fetches without affecting ISR/write latency
- **Analytics workloads**: heavy consumers don't impact production replicas

```properties
# Consumer config to fetch from closest replica (including observers)
client.rack=dc-west
# Broker config
broker.rack=dc-east

# Replica placement (topic config)
# KIP-392 uses replica.selector.class for rack-aware fetching
replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector
```

**Limitation**: observer replicas may lag behind the leader. Consumers reading from observers get **eventually consistent** data. For strict consistency, consumers must read from the leader.

## Rack-Aware Replication

`broker.rack` tells Kafka which failure domain (rack, AZ, datacenter) each broker belongs to. The partition assignment algorithm ensures replicas are spread across racks.

```properties
# Broker configs
# Broker 0 (AZ-a)
broker.rack=us-east-1a

# Broker 1 (AZ-b)
broker.rack=us-east-1b

# Broker 2 (AZ-c)
broker.rack=us-east-1c
```

With rack awareness enabled, a topic with RF=3 on a 6-broker cluster across 3 AZs:

```
Partition 0: Broker 0 (AZ-a), Broker 3 (AZ-b), Broker 5 (AZ-c)
Partition 1: Broker 1 (AZ-b), Broker 4 (AZ-c), Broker 2 (AZ-a)

Each partition has one replica per AZ -- survives full AZ failure.
```

Without `broker.rack`, Kafka may place all replicas in the same AZ, making a single AZ failure fatal for that partition.

```bash
# Verify rack-aware placement
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Cross-reference broker IDs with their broker.rack setting
# to confirm replicas span different racks
```

## Multi-Datacenter Patterns

### Pattern 1: Stretch Cluster

Single Kafka cluster spanning 2-3 datacenters over a low-latency network.

```
DC-East                         DC-West
+----------+                    +----------+
| Broker 0 |<--- replication -->| Broker 3 |
| Broker 1 |      (sync)       | Broker 4 |
| Broker 2 |                    | Broker 5 |
+----------+                    +----------+
      ^                               ^
      |                               |
  Producers                       Consumers
  (local writes)              (local reads via
                               rack-aware fetch)
```

**Requirements:**
- Round-trip latency < 50ms between DCs (ideally < 10ms)
- `broker.rack` set to DC name
- RF=4, min.insync.replicas=3 for 2-DC; RF=3, min.insync.replicas=2 for 3-DC

**Pros:** single cluster, transactional semantics, simple consumer model
**Cons:** write latency includes cross-DC replication, requires low-latency link, ZooKeeper/KRaft quorum spans DCs

### Pattern 2: MirrorMaker 2 (MM2) -- Active-Passive

Separate Kafka clusters per DC. MM2 asynchronously replicates topics between clusters.

```
DC-East (Primary)                   DC-West (DR)
+-----------------+                 +-----------------+
| Kafka Cluster A |  --- MM2 --->   | Kafka Cluster B |
| orders          |  (async)        | east.orders     |
| payments        |                 | east.payments   |
+-----------------+                 +-----------------+
       ^                                   ^
   Producers                          Consumers
   Consumers                       (failover only)
```

```properties
# MM2 config (connect-mirror-maker.properties)
clusters=east,west
east.bootstrap.servers=east-broker1:9092,east-broker2:9092
west.bootstrap.servers=west-broker1:9092,west-broker2:9092

# Replication flow
east->west.enabled=true
west->east.enabled=false    # Active-passive: one direction only

# Topic selection
east->west.topics=orders,payments,user-events
east->west.topics.exclude=.*internal.*,__.*

# Consumer offset sync
emit.checkpoints.enabled=true
emit.checkpoints.interval.seconds=10
sync.group.offsets.enabled=true
sync.group.offsets.interval.seconds=10

# Replication policy
replication.factor=3
```

**Topic naming**: MM2 renames replicated topics with a source prefix: `orders` on cluster `east` becomes `east.orders` on cluster `west`. This prevents replication loops in active-active.

**Offset translation**: MM2 stores offset mappings in `__consumer_offsets` sync checkpoints. On failover, consumers can resume from the translated offset:

```java
// After failover to DR cluster, translate consumer group offsets
RemoteClusterUtils.translateOffsets(
    properties,                    // DR cluster connection
    "east",                        // source cluster alias
    consumerGroupId,               // group to translate
    Duration.ofSeconds(10)
);
```

### Pattern 3: MirrorMaker 2 -- Active-Active

Both clusters accept writes. MM2 replicates bidirectionally.

```
DC-East                              DC-West
+-----------------+                  +-----------------+
| Kafka Cluster A | <--- MM2 --->    | Kafka Cluster B |
| orders          |   (bidir)        | orders          |
| west.orders     |                  | east.orders     |
+-----------------+                  +-----------------+
       ^                                    ^
   Producers                            Producers
   Consumers                            Consumers
   (local topics +                  (local topics +
    replicated topics)               replicated topics)
```

**Topic namespace prevents loops:**
- DC-East produces to `orders`; MM2 replicates as `east.orders` to DC-West
- DC-West produces to `orders`; MM2 replicates as `west.orders` to DC-East
- MM2 never replicates topics with the remote prefix (`east.*` is not replicated back to east)

**Challenges:**
- No global ordering across DCs for the same logical topic
- Consumers must read both `orders` and `east.orders` (or `west.orders`) to get the full picture
- Conflict resolution for key-based compacted topics is application-level
- Exactly-once semantics do not span clusters

**When to use each pattern:**

| Criterion | Stretch Cluster | MM2 Active-Passive | MM2 Active-Active |
|-----------|----------------|-------------------|-------------------|
| DC latency | < 50ms required | Any | Any |
| Write latency | Higher (cross-DC) | Local | Local |
| Failover | Automatic (ISR) | Manual (consumer redirect) | Manual (topic routing) |
| Exactly-once | Yes (single cluster) | No (async gap) | No |
| Complexity | Low | Medium | High |
| Data loss on DC failure | None (if ISR spans DCs) | Possible (async lag) | Possible (async lag) |

### MM2 Lag Monitoring

```bash
# Check replication lag (consumer group __mm2-offsets-*)
kafka-consumer-groups.sh --describe \
  --group mm2-MirrorSourceConnector-0 \
  --bootstrap-server west-broker1:9092

# JMX metrics on MM2 Connect workers
# kafka.connect.mirror:type=MirrorSourceConnector,target=west,topic=orders,partition=0
#   replication-latency-ms       # end-to-end latency
#   record-count                 # records replicated
#   byte-rate                    # throughput
```

## Configuration Reference

### Broker-Level Replication Configs

```properties
# --- ISR ---
replica.lag.time.max.ms=30000           # Follower removed from ISR after this lag
min.insync.replicas=2                    # Cluster-wide default (override per topic)

# --- Replication threads ---
num.replica.fetchers=1                   # Threads per broker for fetching from leaders
replica.fetch.max.bytes=1048576          # 1MB max fetch per partition per request
replica.fetch.wait.max.ms=500            # Max wait before fetch returns (if not enough data)
replica.socket.timeout.ms=30000          # Socket timeout for replication fetches
replica.socket.receive.buffer.bytes=65536

# --- Leader election ---
unclean.leader.election.enable=false     # NEVER set true for critical topics
auto.leader.rebalance.enable=true        # Periodic preferred leader election
leader.imbalance.check.interval.seconds=300
leader.imbalance.per.broker.percentage=10

# --- Log recovery ---
log.recovery.threads.per.data.dir=1      # Threads for log recovery on startup
unclean.shutdown.recovery.enable=true    # Recover from unclean shutdown
```

### Topic-Level Overrides

```bash
# Set replication configs per topic
kafka-configs.sh --alter --topic payments \
  --add-config min.insync.replicas=2,unclean.leader.election.enable=false \
  --bootstrap-server localhost:9092

# Increase replication factor of existing topic (reassignment)
cat > reassignment.json << 'EOF'
{
  "version": 1,
  "partitions": [
    {"topic": "orders", "partition": 0, "replicas": [1, 2, 3]},
    {"topic": "orders", "partition": 1, "replicas": [2, 3, 1]},
    {"topic": "orders", "partition": 2, "replicas": [3, 1, 2]}
  ]
}
EOF

kafka-reassign-partitions.sh --reassignment-json-file reassignment.json \
  --execute --bootstrap-server localhost:9092

# Monitor reassignment progress
kafka-reassign-partitions.sh --reassignment-json-file reassignment.json \
  --verify --bootstrap-server localhost:9092
```

## Failure Scenarios and Recovery

### Scenario 1: Single Broker Failure (RF=3, min.insync.replicas=2)

```
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 crashes
After:  Controller elects Broker 1 as leader (next in ISR)
        ISR={1,2}, writes continue normally
        When Broker 0 recovers, it joins as follower, catches up, rejoins ISR
```

No data loss. No downtime. Automatic recovery.

### Scenario 2: Two Broker Failures (RF=3, min.insync.replicas=2)

```
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 and Broker 1 crash
After:  Controller elects Broker 2 as leader
        ISR={2} -- below min.insync.replicas=2
        Reads work. Writes FAIL with NotEnoughReplicasException.
        Writes resume when any other broker recovers and joins ISR.
```

No data loss. Writes blocked until recovery.

### Scenario 3: Leader Crash with Unreplicated Data

```
Before: Leader LEO=100, HW=95, Follower LEO=95
Event:  Leader crashes (offsets 95-99 not replicated)
After:  Follower becomes leader with LEO=95
        Offsets 95-99 LOST (were uncommitted)
        Producers with acks=all never received ACK for 95-99
        Producers with acks=1 DID receive ACK -- DATA LOSS for those messages
```

This is why `acks=all` is essential for durability.

### Scenario 4: Full Cluster Restart

```bash
# Controlled shutdown -- preferred for rolling restarts
kafka-server-stop.sh
# Broker transfers leadership away before stopping (controlled.shutdown.enable=true)
# Reduces unavailability window

# Rolling restart procedure (zero downtime):
# 1. Stop broker (leadership migrates to ISR members)
# 2. Upgrade/config change
# 3. Start broker (rejoins cluster, catches up, rejoins ISR)
# 4. Wait for under-replicated partitions to reach 0
# 5. Repeat for next broker

# Monitor between restarts:
kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server localhost:9092
# Wait until output is empty before proceeding to next broker
```

```properties
# Controlled shutdown config
controlled.shutdown.enable=true          # default: true
controlled.shutdown.max.retries=3        # default: 3
controlled.shutdown.retry.backoff.ms=5000
```

## Key Metrics for Replication Health

```
# JMX beans to monitor

# Broker level
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions     # TARGET: 0
kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount      # TARGET: 0
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec               # Alert on sustained > 0
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
kafka.server:type=ReplicaManager,name=FailedIsrUpdatesPerSec         # TARGET: 0
kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec

# Partition level
kafka.cluster:type=Partition,name=UnderReplicated,topic=*,partition=*
kafka.log:type=Log,name=LogEndOffset,topic=*,partition=*
kafka.log:type=Log,name=Size,topic=*,partition=*

# Controller
kafka.controller:type=KafkaController,name=OfflinePartitionsCount    # TARGET: 0
kafka.controller:type=KafkaController,name=ActiveControllerCount     # TARGET: 1
kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs
```

**Alert thresholds:**
- `UnderReplicatedPartitions > 0` for > 5 minutes - broker health issue
- `OfflinePartitionsCount > 0` - immediate alert, partitions unavailable
- `IsrShrinksPerSec` sustained - check disk I/O, network, GC on affected brokers
- `UnderMinIsrPartitionCount > 0` - writes failing for affected partitions

## Wiki Links

- [[broker-architecture]] - controller election, KRaft, broker internals
- [[topics-and-partitions]] - partition assignment, log segments, compaction
- [[kafka-cluster-operations]] - rolling upgrades, reassignment, monitoring
