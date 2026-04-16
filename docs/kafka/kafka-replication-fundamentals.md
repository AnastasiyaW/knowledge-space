# Kafka Replication Fundamentals

Leader-follower replication model, replication factor recommendations, ISR mechanics, High Watermark (HW) vs Log End Offset (LEO), leader epoch, committed vs uncommitted messages, and acks + min.insync.replicas interaction.

## Leader-Follower Replication Model

### How It Works

```text
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
```

**ISR shrink/expand flow:**

```text
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

```yaml
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
5. Next fetch responses carry the new HW to followers.

**Consumer visibility**: consumers can only read up to `HW - 1`. This prevents consumers from reading data that might be lost if the leader crashes before followers replicate it.

### Leader Epoch (KIP-101)

The **leader epoch** is a monotonically increasing integer that increments each time a new leader is elected for a partition. It solves the **log divergence problem**:

```text
Scenario without leader epoch:
1. Leader (Broker 0) writes offset 5, HW=4 (follower hasn't fetched yet)
2. Leader crashes
3. Follower (Broker 1) becomes leader, HW=4, LEO=5
4. New leader writes a DIFFERENT message at offset 5
5. Old leader comes back -- its offset 5 conflicts

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

### acks + min.insync.replicas Interaction Matrix

This is the most critical configuration matrix for Kafka durability:

```properties
# Producer config
acks=all                  # -1 is equivalent
# Broker/topic config
min.insync.replicas=2     # Minimum ISR members to accept a write
```

| acks | min.insync.replicas | RF | Behavior |
|------|--------------------|----|----------|
| `0` | any | any | Producer does not wait for ACK. Max throughput, no durability guarantee. |
| `1` | any | any | Producer waits for leader ACK only. Data loss if leader dies before replication. |
| `all` | `1` | 3 | ISR can shrink to leader only -- then `acks=all` = `acks=1`. **False sense of safety.** |
| `all` | `2` | 3 | ISR must have >= 2 members or writes rejected. **Recommended production setting.** |
| `all` | `3` | 3 | Any single broker failure blocks writes. **Too strict for most use cases.** |

**The golden rule**: `acks=all` + `min.insync.replicas=2` + `replication.factor=3`.

### What Happens When ISR Shrinks Below min.insync.replicas

```yaml
Scenario: RF=3, min.insync.replicas=2, acks=all

1. Normal: ISR={0,1,2}, writes succeed
2. Broker 2 dies: ISR={0,1}, writes succeed (2 >= min.insync)
3. Broker 1 dies: ISR={0}, writes FAIL with NotEnoughReplicasException
   - Partition is READABLE but NOT WRITABLE
   - Consumers continue reading committed data
4. Broker 1 returns: ISR={0,1}, writes resume
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
replica.fetch.wait.max.ms=500            # Max wait before fetch returns
replica.socket.timeout.ms=30000          # Socket timeout for replication fetches
replica.socket.receive.buffer.bytes=65536

# --- Leader election ---
unclean.leader.election.enable=false     # NEVER set true for critical topics
auto.leader.rebalance.enable=true        # Periodic preferred leader election
leader.imbalance.check.interval.seconds=300
leader.imbalance.per.broker.percentage=10

# --- Log recovery ---
log.recovery.threads.per.data.dir=1
unclean.shutdown.recovery.enable=true
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
```

## Gotchas

- **RF=2 is a trap.** With `min.insync.replicas=2`, any single follower failure makes the partition read-only. With `min.insync.replicas=1`, you're one broker crash from data loss. Always RF >= 3.
- **`acks=all` with `min.insync.replicas=1` is false safety.** If ISR shrinks to the leader alone, `acks=all` degrades to `acks=1` -- no replication confirmation.
- **ISR shrinks are often caused by GC pauses, not broker failures.** Check GC logs and `replica.lag.time.max.ms` before assuming a hardware issue.
- **HW propagation is delayed.** The leader updates HW, but followers learn about it on the next fetch response. Brief windows exist where followers have data above their local HW.

## See Also

- [[kafka-fault-tolerance]] - failure scenarios, unclean leader election, rack-aware replication, multi-DC patterns
- [[broker-architecture]] - controller election, KRaft, broker internals
- [[topics-and-partitions]] - partition assignment, log segments, compaction
- [[kafka-cluster-management]] - rolling upgrades, reassignment, monitoring
- [[kafka-producer-fundamentals]] - acks modes from the producer perspective
