---
title: Kafka Transactions
category: concepts
tags: [kafka, transactions, exactly-once, transactional-id, zombie-fencing, isolation-level]
---

# Kafka Transactions

Kafka transactions enable atomic writes to multiple topics/partitions - either all messages in a transaction are committed or none are visible to `read_committed` consumers, solving the read-process-write exactly-once problem within Kafka.

## Key Facts

- A transaction allows writing messages to one or more topics atomically
- Since consumer offsets are stored in `__consumer_offsets` topic, committing offsets is also a topic write; within a transaction you can atomically: send output messages AND commit input offsets
- `transactional.id` config is required and must be unique per logical producer instance
- Setting `transactional.id` auto-enables idempotent producer (`enable.idempotence=true`, `acks=all`)
- Transaction metadata stored in internal topic `__transaction_state`
- Default `isolation.level` is `read_uncommitted` - transactions have no effect unless consumer sets `read_committed`
- Transaction overhead is **constant per transaction** regardless of message count; larger transactions amortize overhead better
- Large transactions block the partition for `read_committed` consumers for the entire transaction duration
- `transaction.timeout.ms` - forced abort timeout, default 60 seconds
- Offsets in transactional topics appear non-sequential (e.g., 0, 2, 4) due to control records (commit/abort markers)

## Patterns

### Transaction API (Java)

```java
// Producer config
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092");
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "my-transactional-id");
// enable.idempotence and acks=all are auto-set

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();  // Call ONCE after creation

// Read-process-write loop
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    producer.beginTransaction();
    try {
        for (ConsumerRecord<String, String> record : records) {
            String result = process(record);
            producer.send(new ProducerRecord<>("output", record.key(), result));
        }
        // Commit input offsets within the transaction
        producer.sendOffsetsToTransaction(
            offsetsToCommit,
            consumer.groupMetadata()
        );
        producer.commitTransaction();
    } catch (Exception e) {
        producer.abortTransaction();
    }
}
```

### Consumer Config for Transactions

```properties
isolation.level=read_committed   # Only see committed messages
enable.auto.commit=false         # Manage offsets via transaction
```

### Zombie Fencing Mechanism

```
Scenario without transactions:
  Instance 1 gets messages 1,2 -> processes message 1 -> sends A
  Instance 1 enters long GC pause
  Kafka rebalances -> Instance 2 gets partition
  Instance 2 processes message 2 -> sends B
  Instance 1 wakes up -> processes message 2 again -> sends B
  Result: A, B, B (DUPLICATE)

With transactions (same transactional.id = X):
  When Instance 2 calls initTransactions(t.id = X), epoch increments
  Instance 1 wakes up -> broker rejects (stale epoch)
  Result: A, B (CORRECT)
```

### Transaction Internals (4 Phases)

```
1. Producer -> Transaction Coordinator (TC):
   - Register transactional.id
   - TC aborts any active transaction with that ID
   - TC "fences" old producer (epoch increment)
   - Notify TC of each new partition involved
   - Commit/abort sent to TC

2. TC -> Transaction Log (__transaction_state):
   - All actions from step 1 recorded durably

3. Producer -> Topic/Partition:
   - Actual data writes (messages appear but invisible to read_committed)

4. TC -> Topic/Partition (after commit/abort):
   - Write commit/abort markers to all involved partitions
   - Update transaction state to completed
```

### AdminClient Transaction API

```java
AdminClient admin = AdminClient.create(props);
admin.listTransactions();     // Returns: transactionalId, producerId, state
admin.describeTransactions(Collection<String> transactionalIds);
admin.abortTransaction(new AbortTransactionSpec(tp, producerId, epoch, coordEpoch));
```

## Gotchas

- **`isolation.level` defaults to `read_uncommitted`** - most critical mistake; transactions are invisible to consumers unless they explicitly opt in with `read_committed`
- **`read_committed` consumers are blocked by open transactions** - messages from ALL producers (including non-transactional) in the same partition are delayed until the transaction completes
- **Exactly-once ONLY works for Kafka-to-Kafka** - if an external system is involved (database, HTTP), you must use at-least-once + deduplication (see [[transactional-outbox]])
- **Transactional producers cannot use `acks != all`** - setting `transactional.id` forces `acks=all`; attempting to override throws `ConfigException`
- **`transactional.id` must be stable across restarts** - this is how zombie fencing works; a new ID means a new producer identity (no fencing)
- **Offset commits in transactions use producer, not consumer** - must use `producer.sendOffsetsToTransaction()`, not `consumer.commitSync()`

## See Also

- [[idempotent-producer]] - PID + sequence number deduplication (prerequisite for transactions)
- [[delivery-semantics]] - how transactions fit into exactly-once guarantees
- [[transactional-outbox]] - pattern for exactly-once with external databases
- [[producer-patterns]] - producer pipeline, error handling
- [KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
