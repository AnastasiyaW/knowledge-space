---
title: Consumer Groups
category: concepts
tags: [kafka, consumer, group, rebalance, offset, commit, partition-assignment]
---

# Consumer Groups

Consumer groups are Kafka's mechanism for parallel, fault-tolerant message consumption. Each partition is assigned to exactly one consumer within a group - guaranteeing single delivery to the logical consumer while allowing horizontal scaling. Multiple groups read the same topic independently, each maintaining its own offsets.

Docs: [Consumer Group Protocol](https://kafka.apache.org/documentation/#consumerconfigs), [Consumer API](https://kafka.apache.org/documentation/#consumerapi)

## Consumer Group Protocol

### Group Coordinator

Every consumer group is managed by a single broker called the **group coordinator**. Determined by hashing `group.id` to a partition of `__consumer_offsets`, then finding which broker leads that partition.

```
coordinator_partition = hash(group.id) % __consumer_offsets.partition_count
coordinator_broker = leader_of(coordinator_partition)
```

Coordinator responsibilities:
- Tracks group membership via heartbeats
- Detects consumer failures (missed heartbeats beyond `session.timeout.ms`)
- Triggers rebalance when membership changes
- Stores committed offsets for the group

### Group Leader

The **first consumer** to join a group becomes the group leader. The leader performs partition assignment on behalf of the coordinator:

1. Consumer sends `JoinGroup` request to coordinator
2. Coordinator picks leader (first joiner), sends member list + subscriptions to leader
3. Leader runs the assignment strategy, returns assignments in `SyncGroup` request
4. Coordinator distributes assignments to all members via `SyncGroup` responses

The leader is a regular consumer - it also processes messages. If the leader dies, the coordinator picks a new leader during rebalance.

### Partition Assignment Strategies

Configured via `partition.assignment.strategy`. Each strategy implements `ConsumerPartitionAssignor`.

Docs: [Partition Assignment](https://kafka.apache.org/documentation/#consumerconfigs_partition.assignment.strategy)

#### RangeAssignor (default)

Assigns contiguous partition ranges per topic. For each topic independently:

```
partitions_per_consumer = ceil(num_partitions / num_consumers)
Consumer-0: [P0, P1, P2]
Consumer-1: [P3, P4]
```

Use case: co-partitioned topics where you need the same consumer to read partition N from both topic A and topic B (e.g., stream-table join). Requires topics to have the same partition count and key space.

Downside: uneven distribution when `num_partitions % num_consumers != 0`, compounded across multiple topics.

#### RoundRobinAssignor

Assigns partitions one at a time in round-robin across all consumers, across all topics:

```
Topic-A: P0, P1, P2    Topic-B: P0, P1, P2
Consumer-0: [A-P0, A-P2, B-P1]
Consumer-1: [A-P1, B-P0, B-P2]
```

Use case: maximum throughput when all partitions are equivalent and cross-topic co-location is unnecessary.

#### StickyAssignor

Two goals: (1) maximize balance, (2) minimize partition movement on rebalance. Preserves existing assignments where possible, only moving partitions to achieve balance.

Before rebalance:
```
C0: [P0, P1]  C1: [P2, P3]  C2: [P4, P5]
```
C1 dies - StickyAssignor:
```
C0: [P0, P1, P2]  C2: [P4, P5, P3]   # Only P2, P3 moved
```
RangeAssignor would reassign everything:
```
C0: [P0, P1, P2]  C2: [P3, P4, P5]   # P3, P4, P5 all moved
```

Use case: stateful consumers, caching layers, or any case where rebuilding partition-local state is expensive.

#### CooperativeStickyAssignor

Same balancing logic as StickyAssignor, but uses the **incremental cooperative rebalancing** protocol (see below). Consumers do NOT stop processing during rebalance - only the partitions being moved are revoked.

```java
// Enable cooperative rebalancing
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

**Production recommendation: always use CooperativeStickyAssignor** unless you need RangeAssignor for co-partitioned joins.

## Offset Management

### __consumer_offsets Topic

Internal compacted topic (default 50 partitions, RF=3). Stores:
- Committed offsets per (group, topic, partition) tuple
- Consumer group metadata (members, subscriptions, assignments)
- Transaction markers (for exactly-once)

```bash
# Inspect __consumer_offsets (debug only)
kafka-console-consumer.sh --topic __consumer_offsets \
  --bootstrap-server localhost:9092 \
  --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" \
  --from-beginning
```

Each record key = `(group.id, topic, partition)`, value = `(offset, metadata, timestamp)`. Compaction retains only the latest offset per key.

### Auto-Commit vs Manual Commit

**Auto-commit** (`enable.auto.commit=true`, default):

```python
conf = {
    "enable.auto.commit": True,           # default
    "auto.commit.interval.ms": 5000,      # commit every 5s
}
```

Offsets committed on next `poll()` if `auto.commit.interval.ms` has elapsed since last commit. Risk: crash between processing and next commit = reprocessing (at-least-once).

**Manual synchronous commit**:

```python
from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "enable.auto.commit": False,
})
consumer.subscribe(["events"])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            handle_error(msg.error())
            continue

        process(msg)
        consumer.commit(asynchronous=False)  # blocks until broker confirms
finally:
    consumer.close()
```

**Manual async commit with sync on shutdown**:

```python
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        process(msg)
        consumer.commit(asynchronous=True)   # fire-and-forget
finally:
    consumer.commit(asynchronous=False)      # sync commit before exit
    consumer.close()
```

**Commit specific offsets** (per-partition granularity):

```python
from confluent_kafka import TopicPartition

# Commit offset 42 for partition 0 of "events"
consumer.commit(offsets=[
    TopicPartition("events", partition=0, offset=42)
], asynchronous=False)
```

**Java - commitSync / commitAsync**:

```java
// commitAsync with callback
consumer.commitAsync((offsets, exception) -> {
    if (exception != null) {
        log.error("Commit failed for offsets {}", offsets, exception);
    }
});

// commitSync in finally
try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            process(record);
        }
        consumer.commitAsync();
    }
} finally {
    consumer.commitSync();
    consumer.close();
}
```

### auto.offset.reset

Controls behavior when **no committed offset exists** for a partition (new group, or offsets expired past `offsets.retention.minutes` - default 7 days):

| Value | Behavior |
|-------|----------|
| `latest` (default) | Read only new messages from this point forward |
| `earliest` | Read from the beginning of the partition |
| `none` | Throw `NoOffsetForPartitionException` |

This does NOT rewind an existing consumer group. To replay, reset offsets explicitly:

```bash
kafka-consumer-groups.sh --reset-offsets --to-earliest \
  --group my-group --topic my-topic --execute \
  --bootstrap-server localhost:9092
```

## Rebalancing

Docs: [Incremental Cooperative Rebalancing](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%3A+Kafka+Consumer+Incremental+Rebalance+Protocol)

### Rebalance Triggers

- Consumer joins the group (new instance, restart)
- Consumer leaves the group (shutdown, crash, heartbeat timeout)
- Consumer exceeds `max.poll.interval.ms` (stuck processing)
- Subscription changes (consumer.subscribe with different topics)
- Topic partition count changes (partitions added)
- Consumer group coordinator failover

### Eager (Stop-the-World) Rebalancing

Default protocol with RangeAssignor and RoundRobinAssignor:

1. Coordinator sends `REBALANCE_IN_PROGRESS` error on next heartbeat/poll
2. **All consumers revoke ALL partitions** - processing stops group-wide
3. All consumers send `JoinGroup` request
4. Leader computes full assignment from scratch
5. Coordinator distributes new assignments via `SyncGroup`
6. Consumers resume on their newly assigned partitions

Impact: complete processing pause for the entire group. Duration depends on `max.poll.interval.ms` (waiting for slow consumers to rejoin).

### Incremental Cooperative Rebalancing

Used by CooperativeStickyAssignor. Two-phase protocol:

**Phase 1 - Detect changes:**
1. Coordinator triggers rebalance
2. Consumers send `JoinGroup` with their current assignments
3. Leader computes new assignment, identifies partitions that need to move
4. Consumers that must give up partitions revoke **only those partitions**
5. Other consumers continue processing uninterrupted

**Phase 2 - Reassign:**
1. A second rebalance is triggered automatically
2. Revoked partitions are now unowned
3. Leader assigns them to their new owners
4. New owners start consuming

```
Before: C0=[P0,P1,P2]  C1=[P3,P4,P5]
C2 joins group.

Phase 1: C0 revokes P2, C1 revokes P5. C0 and C1 continue on remaining partitions.
Phase 2: C2 receives P2 and P5.
After:  C0=[P0,P1]  C1=[P3,P4]  C2=[P2,P5]
```

Benefit: only moved partitions experience downtime. Other partitions process continuously.

### Static Group Membership

Docs: [KIP-345 Static Membership](https://cwiki.apache.org/confluence/display/KAFKA/KIP-345%3A+Introduce+static+membership+protocol+to+reduce+consumer+rebalances)

Assign a persistent identity to each consumer via `group.instance.id`. When a consumer with a static ID disconnects and reconnects within `session.timeout.ms`, it gets its old partitions back with **no rebalance**.

```python
conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "group.instance.id": "consumer-host-1",  # stable identity
    "session.timeout.ms": 300000,            # 5min - allow for rolling restarts
}
```

Use cases:
- Rolling deployments (restart consumers one at a time without rebalance storm)
- Kubernetes pods with stable network identities (StatefulSet)
- Consumers with expensive local state initialization

Without static membership: consumer restart = leave + join = 2 rebalances. With static membership: consumer restart within session timeout = 0 rebalances.

## Consumer Configuration Reference

Docs: [Consumer Configs](https://kafka.apache.org/documentation/#consumerconfigs)

### Polling and Processing

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max.poll.records` | 500 | Max records returned per `poll()` call. Lower = more frequent commits, higher = better throughput |
| `max.poll.interval.ms` | 300000 (5min) | Max time between `poll()` calls before consumer is considered stuck. Exceeding triggers rebalance and partition revocation |
| `fetch.min.bytes` | 1 | Min data the broker should return. Higher = fewer requests, more latency |
| `fetch.max.wait.ms` | 500 | Max time broker waits to accumulate `fetch.min.bytes` |
| `max.partition.fetch.bytes` | 1048576 (1MB) | Max data per partition per fetch |

### Liveness and Heartbeats

| Parameter | Default | Description |
|-----------|---------|-------------|
| `session.timeout.ms` | 45000 | Time before coordinator considers consumer dead. Must be within broker's `group.min.session.timeout.ms` and `group.max.session.timeout.ms` |
| `heartbeat.interval.ms` | 3000 | Heartbeat frequency. Rule of thumb: set to 1/3 of `session.timeout.ms` |

### Offset Management

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enable.auto.commit` | true | Auto-commit offsets periodically |
| `auto.commit.interval.ms` | 5000 | Auto-commit interval |
| `auto.offset.reset` | latest | Where to start when no committed offset exists |
| `isolation.level` | read_uncommitted | Set to `read_committed` to skip aborted transactional records |

### Group Management

| Parameter | Default | Description |
|-----------|---------|-------------|
| `group.id` | -- | Consumer group identifier (required) |
| `group.instance.id` | -- | Static membership ID. Set to prevent rebalance on restart |
| `partition.assignment.strategy` | RangeAssignor | Partition distribution algorithm |

### Tuning Guidelines

```
# High-throughput batch processing
max.poll.records=1000
max.poll.interval.ms=600000       # 10min for heavy processing
fetch.min.bytes=65536             # wait for 64KB before returning
session.timeout.ms=30000

# Low-latency event processing
max.poll.records=50
max.poll.interval.ms=30000
fetch.min.bytes=1                 # return immediately
fetch.max.wait.ms=100
session.timeout.ms=10000
heartbeat.interval.ms=3000
```

## Consumer Lag Monitoring

### kafka-consumer-groups.sh --describe

```bash
kafka-consumer-groups.sh --describe --group my-group \
  --bootstrap-server localhost:9092
```

Output:

```
GROUP       TOPIC       PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG    CONSUMER-ID                                HOST            CLIENT-ID
my-group    events      0          1000            1050            50     consumer-1-abc-xyz                          /10.0.0.1       consumer-1
my-group    events      1          2000            2000            0      consumer-2-def-uvw                          /10.0.0.2       consumer-2
my-group    events      2          1500            1600            100    consumer-1-abc-xyz                          /10.0.0.1       consumer-1
```

| Column | Meaning |
|--------|---------|
| CURRENT-OFFSET | Last committed offset for this partition |
| LOG-END-OFFSET | Latest offset in the partition (highwater mark) |
| LAG | `LOG-END-OFFSET - CURRENT-OFFSET` - messages behind |
| CONSUMER-ID | Which consumer instance owns this partition |

### Monitoring Commands

```bash
# List all consumer groups
kafka-consumer-groups.sh --list --bootstrap-server localhost:9092

# Describe with state info
kafka-consumer-groups.sh --describe --group my-group --state \
  --bootstrap-server localhost:9092

# Output includes group state: Stable, PreparingRebalance, CompletingRebalance, Dead, Empty

# Describe all groups
kafka-consumer-groups.sh --describe --all-groups \
  --bootstrap-server localhost:9092

# Members detail (shows assignments)
kafka-consumer-groups.sh --describe --group my-group --members --verbose \
  --bootstrap-server localhost:9092
```

### Programmatic Lag Monitoring (Python)

```python
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, TopicPartition

admin = AdminClient({"bootstrap.servers": "localhost:9092"})

# Get committed offsets for group
group_id = "my-group"
future = admin.list_consumer_group_offsets([{"group.id": group_id}])
offsets = future[group_id].result()

# Get end offsets
consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "lag-monitor",
})

for tp, offset_meta in offsets.items():
    # Get high watermark
    low, high = consumer.get_watermark_offsets(tp)
    lag = high - offset_meta.offset
    print(f"{tp.topic}:{tp.partition} committed={offset_meta.offset} "
          f"end={high} lag={lag}")

consumer.close()
```

### Key Lag Thresholds

| Lag | Interpretation |
|-----|---------------|
| 0 | Consumer is caught up |
| < 1000 | Normal for most workloads |
| Growing steadily | Consumer throughput < producer throughput - scale consumers |
| Sudden spike | Consumer restart, rebalance, or downstream slowdown |
| CURRENT-OFFSET = `-` | Consumer assigned but has not committed yet |

## Exactly-Once Consumption

Kafka's exactly-once semantics (EOS) cover the full read-process-write cycle. For consumers that only read and process (no write back to Kafka), use **idempotent processing** instead.

### Transactional Read-Process-Write (Kafka-to-Kafka)

When the consumer reads from Kafka, processes, and writes results back to Kafka:

```java
// Producer with transactions
Properties producerProps = new Properties();
producerProps.put("transactional.id", "my-txn-id");
producerProps.put("enable.idempotence", true);
KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);
producer.initTransactions();

// Consumer
Properties consumerProps = new Properties();
consumerProps.put("group.id", "my-group");
consumerProps.put("enable.auto.commit", false);
consumerProps.put("isolation.level", "read_committed");
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
consumer.subscribe(List.of("input-topic"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    if (records.isEmpty()) continue;

    producer.beginTransaction();
    try {
        for (ConsumerRecord<String, String> record : records) {
            String result = process(record);
            producer.send(new ProducerRecord<>("output-topic", record.key(), result));
        }
        // Commit offsets within the transaction
        producer.sendOffsetsToTransaction(
            currentOffsets(records),
            consumer.groupMetadata()
        );
        producer.commitTransaction();
    } catch (Exception e) {
        producer.abortTransaction();
    }
}
```

Key: `sendOffsetsToTransaction` atomically commits consumer offsets with the produced records. If the transaction aborts, offsets are not committed.

### Idempotent Processing (Kafka-to-External)

When writing to an external system (database, API), Kafka transactions don't help. Use idempotent processing:

**Pattern 1: Deduplication table**

```python
import psycopg2
from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "enable.auto.commit": False,
})
consumer.subscribe(["orders"])

conn = psycopg2.connect("dbname=mydb")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue

        order = deserialize(msg.value())
        cur = conn.cursor()

        # Atomic: insert + offset update in same DB transaction
        try:
            cur.execute("BEGIN")

            # Check if already processed (idempotency key = topic:partition:offset)
            idempotency_key = f"{msg.topic()}:{msg.partition()}:{msg.offset()}"
            cur.execute(
                "INSERT INTO processed_offsets (idempotency_key) VALUES (%s) "
                "ON CONFLICT DO NOTHING RETURNING idempotency_key",
                (idempotency_key,)
            )
            if cur.fetchone() is None:
                # Already processed - skip
                cur.execute("ROLLBACK")
                consumer.commit(asynchronous=False)
                continue

            # Process
            cur.execute(
                "INSERT INTO orders (id, amount) VALUES (%s, %s)",
                (order["id"], order["amount"])
            )
            cur.execute("COMMIT")
            consumer.commit(asynchronous=False)

        except Exception:
            cur.execute("ROLLBACK")
            raise

finally:
    consumer.close()
    conn.close()
```

**Pattern 2: Store offset in external system**

Instead of committing offsets to Kafka, store them alongside business data:

```python
# In the same DB transaction as your business logic:
cur.execute(
    "INSERT INTO kafka_offsets (group_id, topic, partition, committed_offset) "
    "VALUES (%s, %s, %s, %s) "
    "ON CONFLICT (group_id, topic, partition) DO UPDATE SET committed_offset = %s",
    (group_id, topic, partition, offset, offset)
)
```

On consumer restart, seek to the stored offset instead of relying on `__consumer_offsets`:

```python
from confluent_kafka import TopicPartition

def on_assign(consumer, partitions):
    for tp in partitions:
        stored = get_offset_from_db(group_id, tp.topic, tp.partition)
        if stored is not None:
            tp.offset = stored + 1
    consumer.assign(partitions)

consumer.subscribe(["orders"], on_assign=on_assign)
```

### Exactly-Once Decision Matrix

| Sink | Strategy | Offset Storage |
|------|----------|---------------|
| Kafka topic | Kafka Transactions (`sendOffsetsToTransaction`) | `__consumer_offsets` (transactional) |
| Database | Idempotent writes (dedup table or upsert) | External DB (same transaction as data) |
| External API | Idempotent API calls (natural keys / request IDs) | `__consumer_offsets` + retry |
| [[kafka-streams]] | Built-in EOS (`processing.guarantee=exactly_once_v2`) | Automatic |

## Gotchas

- **More consumers than partitions = idle consumers.** A partition is never split across consumers. If topic has 3 partitions and group has 5 consumers, 2 sit idle. Scale partitions first.
- **`max.poll.interval.ms` is the silent killer.** If processing takes longer than this (default 5min), Kafka considers the consumer stuck and triggers rebalance. The consumer doesn't crash - it just loses its partitions. Increase the timeout or reduce batch size via `max.poll.records`.
- **Auto-commit + crash = reprocessing.** If `enable.auto.commit=true` and consumer crashes between commits, messages processed since last commit are reprocessed on rebalance. For critical workloads, disable auto-commit.
- **`auto.offset.reset` is one-shot.** Only applies when no committed offset exists. To replay an existing group, use `kafka-consumer-groups.sh --reset-offsets` (requires consumer group to be stopped).
- **Eager rebalancing stops ALL consumers.** With RangeAssignor/RoundRobinAssignor, even adding one consumer pauses the entire group. Switch to CooperativeStickyAssignor.
- **Static membership requires longer session timeout.** If `group.instance.id` is set but `session.timeout.ms` is too short, restarts still trigger rebalance. Set session timeout to cover your longest restart window.
- **Offset expiration.** Broker config `offsets.retention.minutes` (default 10080 = 7 days). If a consumer group is inactive longer than this, committed offsets are deleted. Next startup falls back to `auto.offset.reset`.
- **`isolation.level=read_committed` hides messages.** When using transactional producers, consumers with `read_uncommitted` (default) see ALL records including aborted transactions. Set `read_committed` to only see committed records - but this adds latency until transactions complete.
- **Cooperative rebalancing takes two rounds.** CooperativeStickyAssignor performs two rebalance phases - the first revokes, the second assigns. Brief period where some partitions are unowned. Total rebalance time is slightly longer, but impact is far lower.

## See Also

- [[topics-and-partitions]] - topic design, partition count, key-based routing
- [[consumer-groups]] - deep dive into offset commit patterns and retention
- [[kafka-streams]] - stateful stream processing with automatic consumer group management
- [[broker-architecture]] - brokers, replication, ISR, KRaft coordination
- [[kafka-transactions]] - exactly-once delivery with transactional producers/consumers
