---
title: Kafka Transactions
category: concepts
tags: [kafka, transactions, exactly-once, idempotent, transactional-id, eos]
---

# Kafka Transactions

Atomic read-process-write across multiple partitions and topics. Combines idempotent producer (dedup retries) with transaction coordinator (atomic multi-partition commits). EOS guarantee applies only to Kafka-to-Kafka pipelines - external systems require at-least-once + application-level dedup.

## Idempotent Producer

Foundation layer. Prevents duplicate writes caused by **client library retries** (network timeouts, leader failover). Does NOT protect against application-level retries (calling `send()` again in your code).

**Mechanism:** Broker assigns each producer a **Producer ID (PID)** + tracks **sequence number** per topic-partition. Duplicate sequence = silently discarded. Sequence gap = `OutOfOrderSequenceException`.

```properties
enable.idempotence=true
acks=all                                    # required
max.in.flight.requests.per.connection=5     # max allowed; lower = more ordering guarantees
retries=2147483647                          # effectively infinite; default since 2.1
```

Since Kafka 3.0, idempotence is enabled by default when `acks=all` and `max.in.flight.requests.per.connection <= 5`.

**PID lifetime:** assigned on `initTransactions()` or first `send()`. Lost on producer restart unless `transactional.id` is set (which persists the mapping). Without `transactional.id`, a restarted producer gets a new PID - old in-flight messages become potential duplicates.

## Transactional Producer

Extends idempotent producer with atomic multi-partition writes. Setting `transactional.id` automatically enables idempotence.

### Lifecycle API

```
initTransactions()              -- register transactional.id, fence zombies, once per producer
beginTransaction()              -- start new transaction
send(record)                    -- buffer writes (can span multiple topics/partitions)
sendOffsetsToTransaction(...)   -- atomically commit consumer offsets with produced messages
commitTransaction()             -- two-phase commit via transaction coordinator
abortTransaction()              -- discard all buffered writes
```

### Java - Full Read-Process-Write Pattern

```java
Properties producerProps = new Properties();
producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092");
producerProps.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "order-processor-partition-0");
producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
// enable.idempotence, acks=all set automatically

KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);

Properties consumerProps = new Properties();
consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092");
consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processors");
consumerProps.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
consumerProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
consumer.subscribe(Collections.singleton("input-orders"));

producer.initTransactions(); // call ONCE before any transactions

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    if (records.isEmpty()) continue;

    producer.beginTransaction();
    try {
        for (ConsumerRecord<String, String> record : records) {
            String enriched = process(record.value());
            producer.send(new ProducerRecord<>("enriched-orders", record.key(), enriched));
        }

        // commit offsets atomically with produced messages
        Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
        for (TopicPartition partition : records.partitions()) {
            List<ConsumerRecord<String, String>> partRecords = records.records(partition);
            long lastOffset = partRecords.get(partRecords.size() - 1).offset();
            offsets.put(partition, new OffsetAndMetadata(lastOffset + 1));
        }
        producer.sendOffsetsToTransaction(offsets, consumer.groupMetadata());

        producer.commitTransaction();
    } catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
        // fatal - cannot recover, must close
        producer.close();
        throw e;
    } catch (KafkaException e) {
        producer.abortTransaction();
        // consumer will re-read uncommitted offsets on next poll
    }
}
```

### Python - confluent-kafka Transactional Producer

```python
from confluent_kafka import Producer, Consumer, KafkaException

producer_conf = {
    'bootstrap.servers': 'broker1:9092,broker2:9092',
    'transactional.id': 'etl-processor-0',
    # enable.idempotence=true set automatically
}
producer = Producer(producer_conf)
producer.init_transactions()

consumer_conf = {
    'bootstrap.servers': 'broker1:9092,broker2:9092',
    'group.id': 'etl-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
    'isolation.level': 'read_committed',
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['raw-events'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        producer.begin_transaction()
        try:
            result = transform(msg.value().decode('utf-8'))
            producer.produce(
                topic='processed-events',
                key=msg.key(),
                value=result.encode('utf-8'),
            )
            # commit consumer offset within the same transaction
            producer.send_offsets_to_transaction(
                consumer.position(consumer.assignment()),
                consumer.consumer_group_metadata(),
            )
            producer.commit_transaction()
        except KafkaException:
            producer.abort_transaction()
finally:
    consumer.close()
    producer.flush()
```

### Python - kafka-python (no native transaction support)

`kafka-python` does **not** support transactions. Use `confluent-kafka` (librdkafka wrapper) for transactional workloads. For simple idempotent-only use:

```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='broker1:9092',
    enable_idempotence=True,   # PID + sequence dedup
    acks='all',
    max_in_flight_requests_per_connection=5,
    retries=5,
)
# No beginTransaction/commitTransaction available
```

## Exactly-Once Semantics (EOS)

EOS = idempotent producer + transactions + `read_committed` consumers. Only valid for **Kafka-to-Kafka** pipelines.

### Consumer isolation.level

```properties
# DEFAULT - sees all messages including uncommitted
isolation.level=read_uncommitted

# Transactional - only sees committed messages
isolation.level=read_committed
```

With `read_committed`, the consumer's **Last Stable Offset (LSO)** is the offset of the earliest open transaction. All messages below LSO with committed transaction markers are delivered; aborted messages are filtered out. Messages above LSO are held back.

**Critical side effect:** while a transaction is open on partition P, ALL messages on P are blocked for `read_committed` consumers - including messages from non-transactional producers. Long-running transactions cause consumer lag spikes.

### EOS in Kafka Streams

[[kafka-streams]] has built-in EOS support:

```java
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE_V2);
// V2 (KIP-447, Kafka 2.5+): one producer per StreamThread instead of per task
// V1 (deprecated): one producer per task, higher resource usage
```

Streams handles `initTransactions`, `beginTransaction`, `sendOffsetsToTransaction`, `commitTransaction` internally. The `transactional.id` is derived from `application.id` + task assignment.

## Transaction Coordinator

Each broker can act as a transaction coordinator (TC). The TC for a given `transactional.id` is determined by hashing `transactional.id` to a partition of `__transaction_state`.

### __transaction_state Topic

Internal compacted topic (default 50 partitions). Stores transaction metadata:

```
Key:   transactional.id
Value: {PID, epoch, state, partitions, timeout, last_update_time}
```

Transaction states: `Empty` -> `Ongoing` -> `PrepareCommit` / `PrepareAbort` -> `CompleteCommit` / `CompleteAbort` -> `Empty`

The TC is the leader of the `__transaction_state` partition assigned to the `transactional.id`. If the TC broker fails, the new partition leader takes over and recovers state from the log.

### Two-Phase Commit Flow

```
1. Producer -> TC:   AddPartitionsToTxn(topic-partition list)
2. TC -> __transaction_state:  log partition additions
3. Producer -> Partition Leaders: ProduceRequest (messages with PID, epoch)
4. Producer -> TC:   EndTxn(COMMIT)
5. TC -> __transaction_state:  log PrepareCommit
6. TC -> Partition Leaders:    WriteTxnMarkers(COMMIT) to each partition
7. Partition Leaders -> TC:    acknowledgments
8. TC -> __transaction_state:  log CompleteCommit
```

Abort follows the same flow with `ABORT` markers instead of `COMMIT`.

## Transaction Timeout

```properties
# Producer-side: max time between beginTransaction() and commit/abort
transaction.timeout.ms=60000          # default 60s

# Broker-side: upper bound on what producers can request
max.transaction.timeout.ms=900000     # default 15min
```

If `transaction.timeout.ms > max.transaction.timeout.ms`, the producer gets `InvalidTransactionTimeout` on `initTransactions()`.

When a transaction exceeds its timeout, the TC forcibly aborts it and bumps the epoch. The producer receives `ProducerFencedException` on next operation.

**Operational concern:** stuck transactions (crashed producer without abort) block `read_committed` consumers on affected partitions until timeout expires. Monitor via `kafka-transactions.sh --list` or Admin API.

## Zombie Fencing

Prevents duplicate writes from "zombie" producer instances - e.g., an instance that paused during GC, got replaced by a rebalance, then resumed.

### Epoch Bumping

```
Instance A: initTransactions("txn-id-0")  -> PID=100, epoch=0
Instance A: beginTransaction(), send(...)
            -- GC pause, consumer group rebalance --
Instance B: initTransactions("txn-id-0")  -> PID=100, epoch=1
            TC aborts Instance A's open transaction
Instance A: wakes up, send(...)
            -> broker rejects: epoch 0 < current epoch 1
            -> ProducerFencedException (fatal, must close producer)
```

### Transactional ID Assignment Strategy

The `transactional.id` must be **deterministic** based on input partitions so that a replacement instance reuses the same ID and fences the zombie:

```java
// Pattern: derive transactional.id from input partition assignment
String txnId = String.format("processor-%s-%d",
    inputTopic,
    assignedPartition);
// "processor-orders-3" - replacement for partition 3 fences the old instance
```

**Wrong:** random/UUID-based `transactional.id` - replacement gets different ID, no fencing occurs.

With [[kafka-streams]] `EXACTLY_ONCE_V2` (Kafka 2.5+), transactional IDs are managed per StreamThread and derived from `application.id` + thread index.

## Performance Impact

### Latency

| Operation | Overhead |
|-----------|----------|
| `initTransactions()` | ~50-100ms (once per producer lifetime) |
| `beginTransaction()` | negligible (local state only) |
| `send()` within txn | first send per new partition adds ~5-10ms (AddPartitionsToTxn RPC) |
| `commitTransaction()` | ~20-50ms (two-phase commit: TC log + partition markers) |

**Commit latency is fixed per transaction, not per message.** Batching more messages per transaction amortizes the ~20-50ms commit cost.

### Throughput Tradeoffs

```
Messages/txn    Commit overhead/msg    Consumer lag risk
─────────────────────────────────────────────────────────
1               20-50ms/msg            minimal
100             0.2-0.5ms/msg          low
1000            0.02-0.05ms/msg        moderate
10000+          negligible             HIGH - long open txn blocks LSO
```

**Recommendation:** batch 100-1000 messages per transaction, or commit on a time interval (e.g., every 100ms). [[kafka-streams]] with `EXACTLY_ONCE_V2` commits per `commit.interval.ms` (default 100ms).

### Resource Overhead

- Each `transactional.id` holds state in `__transaction_state` - thousands of concurrent transactional producers add TC load
- `EXACTLY_ONCE_V2` (one producer per StreamThread) vs `EXACTLY_ONCE` (one per task) - V2 reduces producer count by ~10-100x
- `read_committed` consumers maintain LSO tracking per partition - marginal CPU overhead vs `read_uncommitted`

### When NOT to Use Transactions

- Simple fire-and-forget producing (no read-process-write) - idempotent producer alone suffices
- External systems in the pipeline - transactions don't extend beyond Kafka; use outbox pattern
- Ultra-low-latency requirements (<5ms end-to-end) - commit overhead may be unacceptable
- High-throughput logging/metrics - `acks=1` with `at-least-once` and downstream dedup is cheaper

## Configuration Reference

| Config | Scope | Default | Notes |
|--------|-------|---------|-------|
| `enable.idempotence` | Producer | `true` (3.0+) | PID + sequence dedup |
| `transactional.id` | Producer | none | Enables transactions; auto-enables idempotence |
| `transaction.timeout.ms` | Producer | 60000 | Max open transaction duration |
| `max.in.flight.requests.per.connection` | Producer | 5 | Must be <= 5 for idempotency |
| `acks` | Producer | `all` | Must be `all` for idempotency |
| `isolation.level` | Consumer | `read_uncommitted` | `read_committed` for transactional consumers |
| `max.transaction.timeout.ms` | Broker | 900000 | Upper bound on producer timeout |
| `transaction.state.log.replication.factor` | Broker | 3 | Replication for `__transaction_state` |
| `transaction.state.log.num.partitions` | Broker | 50 | Partitions for `__transaction_state` |
| `transaction.state.log.min.isr` | Broker | 2 | Min ISR for `__transaction_state` |

## Operational Commands

```bash
# List active/stuck transactions
kafka-transactions.sh --bootstrap-server localhost:9092 --list

# Describe a specific transaction
kafka-transactions.sh --bootstrap-server localhost:9092 \
    --describe --transactional-id my-txn-id

# Abort a stuck transaction (requires finding PID and epoch)
kafka-transactions.sh --bootstrap-server localhost:9092 \
    --abort --transactional-id my-txn-id \
    --producer-id 12345 --producer-epoch 5 --coordinator-epoch 10

# Read __transaction_state (internal topic, requires admin)
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic __transaction_state --from-beginning \
    --formatter "kafka.coordinator.transaction.TransactionLog\$TransactionLogMessageFormatter"
```

## See Also

- [[producer-patterns]] - idempotent producer config, batching strategies, delivery guarantees
- [[consumer-groups]] - rebalancing, offset management, isolation.level impact
- [[kafka-streams]] - built-in EOS with EXACTLY_ONCE_V2, commit.interval.ms tuning
- [[broker-architecture]] - transaction coordinator election, __transaction_state replication
