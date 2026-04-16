# Kafka Fault Tolerance

Unclean leader election, preferred replica election, observer replicas, rack-aware replication, multi-datacenter patterns, failure scenarios with recovery procedures, and replication health metrics.

For the replication model, ISR, HW/LEO, and acks interaction, see [[kafka-replication-fundamentals]].

## Unclean Leader Election

When all ISR replicas are down, Kafka faces a choice: **availability vs data integrity**.

```properties
# Broker config (default: false since Kafka 0.11.0.0)
unclean.leader.election.enable=false
```

| Setting | Behavior | Tradeoff |
|---------|----------|----------|
| `false` (default) | Partition stays offline until an ISR member recovers | **No data loss**, but unavailability |
| `true` | An out-of-sync replica can become leader | **Data loss** (unreplicated messages are gone), but availability |

**When to enable unclean leader election:**
- Metrics/logs/clickstream where availability > durability
- Topics that can be rebuilt from source systems
- **Never** for financial transactions, orders, audit logs

```bash
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

```text
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

Kafka assigns a **preferred leader** for each partition (the first broker in the replica list). After failures and recoveries, leadership may drift so that some brokers carry more leader load than others.

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
2. If a broker's leader imbalance exceeds `leader.imbalance.per.broker.percentage`, the controller triggers preferred leader elections
3. This only works if the preferred leader is in the ISR

## Observer Replicas (KIP-392)

Observer replicas are **non-voting** replicas that replicate data but are **never added to the ISR** and **never eligible for leader election**. They serve read-only consumer fetches.

```text
Producer --> Leader (Broker 0, DC-East)
                |
         +------+------+
         v             v
    Follower       Observer
    (Broker 1,     (Broker 3,
     DC-East)      DC-West)
     [ISR]         [NOT in ISR, never votes]
```

Use cases:
- **Cross-DC reads**: consumers in DC-West read from the local observer
- **Offload read traffic**: observer handles consumer fetches without affecting ISR/write latency
- **Analytics workloads**: heavy consumers don't impact production replicas

```properties
# Consumer config to fetch from closest replica (including observers)
client.rack=dc-west
# Broker config
broker.rack=dc-east

# Replica placement (topic config)
replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector
```

**Limitation**: observer replicas may lag behind the leader. Consumers reading from observers get **eventually consistent** data.

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

```text
Partition 0: Broker 0 (AZ-a), Broker 3 (AZ-b), Broker 5 (AZ-c)
Partition 1: Broker 1 (AZ-b), Broker 4 (AZ-c), Broker 2 (AZ-a)

Each partition has one replica per AZ -- survives full AZ failure.
```

Without `broker.rack`, Kafka may place all replicas in the same AZ, making a single AZ failure fatal.

```bash
# Verify rack-aware placement
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Cross-reference broker IDs with their broker.rack setting
```

## Multi-Datacenter Patterns

### Pattern 1: Stretch Cluster

Single Kafka cluster spanning 2-3 datacenters over a low-latency network.

```text
DC-East                         DC-West
+----------+                    +----------+
| Broker 0 |<--- replication -->| Broker 3 |
| Broker 1 |      (sync)       | Broker 4 |
| Broker 2 |                    | Broker 5 |
+----------+                    +----------+
```

**Requirements:**
- Round-trip latency < 50ms between DCs (ideally < 10ms)
- `broker.rack` set to DC name
- RF=4, min.insync.replicas=3 for 2-DC; RF=3, min.insync.replicas=2 for 3-DC

### Pattern 2: MM2 Active-Passive

Separate Kafka clusters per DC. MM2 asynchronously replicates topics.

### Pattern 3: MM2 Active-Active

Both clusters accept writes. MM2 replicates bidirectionally. Topic namespace prevents loops.

### Pattern Comparison

| Criterion | Stretch Cluster | MM2 Active-Passive | MM2 Active-Active |
|-----------|----------------|-------------------|-------------------|
| DC latency | < 50ms required | Any | Any |
| Write latency | Higher (cross-DC) | Local | Local |
| Failover | Automatic (ISR) | Manual | Manual |
| Exactly-once | Yes | No (async gap) | No |
| Complexity | Low | Medium | High |
| Data loss on DC failure | None (if ISR spans DCs) | Possible | Possible |

For detailed MM2 configuration and failover procedures, see [[kafka-backup-and-dr]].

## Failure Scenarios and Recovery

### Scenario 1: Single Broker Failure (RF=3, min.insync.replicas=2)

```yaml
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 crashes
After:  Controller elects Broker 1 as leader (next in ISR)
        ISR={1,2}, writes continue normally
        When Broker 0 recovers, it joins as follower, catches up, rejoins ISR
```

No data loss. No downtime. Automatic recovery.

### Scenario 2: Two Broker Failures (RF=3, min.insync.replicas=2)

```yaml
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 and Broker 1 crash
After:  Controller elects Broker 2 as leader
        ISR={2} -- below min.insync.replicas=2
        Reads work. Writes FAIL with NotEnoughReplicasException.
        Writes resume when any other broker recovers and joins ISR.
```

No data loss. Writes blocked until recovery.

### Scenario 3: Leader Crash with Unreplicated Data

```yaml
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
# Rolling restart procedure (zero downtime):
# 1. Stop broker (leadership migrates to ISR members)
# 2. Upgrade/config change
# 3. Start broker (rejoins cluster, catches up, rejoins ISR)
# 4. Wait for under-replicated partitions to reach 0
# 5. Repeat for next broker

kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server localhost:9092
# Wait until output is empty before proceeding to next broker
```

```properties
# Controlled shutdown config
controlled.shutdown.enable=true          # default: true
controlled.shutdown.max.retries=3
controlled.shutdown.retry.backoff.ms=5000
```

## Key Metrics for Replication Health

```text
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

## Gotchas

- **Unclean leader election can lose committed data.** Messages that were fully replicated to the ISR can be lost if the only surviving replica was out-of-sync. This is not just "uncommitted" data loss.
- **Auto leader rebalance only works if preferred leader is in ISR.** If it fell behind, the rebalance waits until it catches up. No forced election.
- **Observer replicas add replication load but no durability.** They pull from the leader just like regular followers, consuming network bandwidth. Size your network accordingly.
- **Rack-aware placement requires broker.rack on ALL brokers.** If some brokers lack it, Kafka ignores rack awareness entirely for those topics.

## See Also

- [[kafka-replication-fundamentals]] - ISR, HW/LEO, acks + min.insync.replicas matrix
- [[kafka-backup-and-dr]] - MirrorMaker 2 configuration, disaster recovery procedures
- [[broker-architecture]] - controller election, KRaft, broker internals
- [[topics-and-partitions]] - partition assignment, log segments
- [[kafka-cluster-management]] - rolling upgrades, partition reassignment
