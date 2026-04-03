---
title: Kafka Streams State Stores
category: concepts
tags: [kafka, streams, state-store, rocksdb, changelog, repartition, fault-tolerance]
---

# Kafka Streams State Stores

State stores provide local key-value storage per Kafka Streams task, backed by RocksDB on disk and changelog topics in Kafka, enabling fault-tolerant stateful processing with automatic recovery.

## Key Facts

- Each task (= each partition) has its own isolated state store; state stores from different tasks are NOT shared
- State stores are backed by a **changelog topic** (internal, auto-created, named `{app-id}-{store-name}-changelog`)
- Every update to the store is written to the changelog topic for durability
- On restart, state is rebuilt from the changelog topic (or from local RocksDB cache if filesystem preserved)
- Persistent stores use RocksDB under the hood, surviving process restarts if filesystem is preserved
- Changelog topics are compacted for faster recovery
- Standby replicas can consume changelogs for fast failover (`num.standby.replicas`)

## Patterns

### State Store Types

```java
// Persistent (RocksDB) - survives restarts, backed by changelog
Stores.persistentKeyValueStore("my-store")

// In-memory - lost on restart, rebuilt from changelog
Stores.inMemoryKeyValueStore("my-store")

// LRU cache - evicts oldest entries
Stores.lruMap("my-store", maxCacheSize)
```

### Creating and Registering State Stores

```java
StreamsBuilder builder = new StreamsBuilder();

StoreBuilder<KeyValueStore<String, Integer>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("reward-store"),
        Serdes.String(),
        Serdes.Integer()
    );
builder.addStateStore(storeBuilder);
```

### Accessing State in Processors

```java
stream.process(() -> new Processor<String, Purchase, String, Reward>() {
    private KeyValueStore<String, Integer> store;

    @Override
    public void init(ProcessorContext<String, Reward> context) {
        store = context.getStateStore("reward-store");
    }

    @Override
    public void process(Record<String, Purchase> record) {
        String customerId = record.value().getCustomerId();
        Integer prev = store.get(customerId);
        int newTotal = (prev != null ? prev : 0) + record.value().getRewardPoints();
        store.put(customerId, newTotal);
        context.forward(record.withValue(new Reward(record.value(), newTotal)));
    }
}, "reward-store");
```

### Changelog Configuration

```java
// Disable changelog (state lost on restart)
storeBuilder.withLoggingDisabled();

// Configure changelog topic params
storeBuilder.withLoggingEnabled(Map.of(
    "cleanup.policy", "compact",
    "retention.ms", "604800000"  // 7 days
));
```

### Repartitioning for Correct State

```java
// Problem: records with same logical key in different partitions
// Solution: repartition before stateful operations

// Option 1: selectKey (auto-repartitions downstream)
stream.selectKey((key, value) -> value.getCustomerId());

// Option 2: explicit repartition
stream.repartition(Repartitioned.with(Serdes.String(), valueSerde));
```

Repartitioning creates an **intermediate internal topic** and splits topology into subtopologies.

## Gotchas

- **State is LOCAL per task** - if records for the same key land in different partitions (no key or wrong partitioning), stateful operations produce incorrect results because different tasks maintain separate state
- **Repartition = internal topic = additional latency** - each repartition adds a read-write hop through Kafka; minimize key changes in topology
- **RocksDB memory pressure** - default RocksDB config may use significant off-heap memory; tune `rocksdb.config.setter` for constrained environments
- **Changelog rebuild on first start is slow** - for large state stores, initial bootstrap from changelog can take minutes/hours; use standby replicas (`num.standby.replicas`) for faster failover
- **State store names must be unique** across the entire topology

## See Also

- [[kafka-streams]] - core KStream/KTable operations, topology basics
- [[kafka-streams-windowing]] - windowed state stores for time-based aggregations
- [[topics-and-partitions]] - how partition assignment affects state store locality
- [Kafka Streams State Store Documentation](https://kafka.apache.org/documentation/streams/developer-guide/processor-api.html#state-stores)
