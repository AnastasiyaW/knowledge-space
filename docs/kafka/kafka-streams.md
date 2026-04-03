---
title: Kafka Streams
category: concepts
tags: [kafka, streams, kstream, ktable, topology, serde, stateless, processor-api]
---

# Kafka Streams

Kafka Streams is a client library (not a framework or separate cluster) for building stream processing applications as DAGs (Directed Acyclic Graphs), providing higher-level abstractions over Producer/Consumer APIs with support for stateless and stateful transformations.

## Key Facts

- Include `kafka-streams` dependency in your application - runs as regular JVM process, no separate cluster
- Internally built on Producer/Consumer APIs - no magic
- Processes events from input topics, transforms them, writes results to output topics
- **Topology**: a DAG of stream processors (nodes) connected by streams (edges); view via `topology.describe()`
- **Serde**: Serializer/Deserializer pair; `Serdes.String()`, `Serdes.Integer()`, `Serdes.Long()` for primitives
- **KStream**: unbounded stream of records; each record is an independent event
- **KTable**: changelog stream; each record is an update to a key; only latest value per key matters
- **GlobalKTable**: reads ALL partitions of a topic; useful for small reference data (no repartitioning needed for joins)
- Kafka Streams manages offsets automatically (`commit.interval.ms`, default 30s)

## Patterns

### KStream Stateless Operations

| Operation | Purpose | Triggers Repartition? |
|-----------|---------|----------------------|
| `filter(predicate)` | Keep matching records | No |
| `mapValues(mapper)` | Transform value only | No |
| `map(mapper)` | Transform key and value | Yes |
| `flatMap(mapper)` | One -> zero or more, can change key | Yes |
| `flatMapValues(mapper)` | One -> zero or more, value only | No |
| `selectKey(mapper)` | Change the key | Yes |
| `split()` / `branch` | Route to sub-streams by condition | No |
| `merge(otherStream)` | Combine two streams | No |
| `peek(action)` | Side-effect (logging) | No |
| `foreach(action)` | Terminal side-effect | N/A |
| `to(topic)` | Write to output topic | N/A |

### Stream Processing Example

```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, Purchase> stream = builder.stream("purchases",
    Consumed.with(Serdes.String(), purchaseSerde));

// 1. Mask credit card (value-only transform - no repartition)
KStream<String, Purchase> masked = stream.mapValues(Purchase::maskCard);

// 2. Calculate rewards (value transform + write to topic)
masked.mapValues(Reward::fromPurchase).to("rewards");

// 3. Filter expensive purchases
stream.filter((key, value) -> value.getAmount() > 1000.0)
    .to("expensive-purchases");

// 4. Branch by department
Map<String, KStream<String, Purchase>> branches = stream
    .split(Named.as("dept-"))
    .branch((k, v) -> v.getDept().equals("coffee"), Branched.as("coffee"))
    .branch((k, v) -> v.getDept().equals("electronics"), Branched.as("electronics"))
    .noDefaultBranch();
```

### KTable Usage

```java
// KTable: topic interpreted as changelog (upserts)
KTable<String, String> users = builder.table("users",
    Consumed.with(Serdes.String(), Serdes.String()));

// KTable caching: deduplicates rapid updates to same key
// Controlled by cache.max.bytes.buffering (default 10MB) and commit.interval.ms (default 30s)
```

### Joins

```java
// Stream-Stream join (windowed, requires time constraint)
KStream<String, String> joined = stream1.join(
    stream2,
    (left, right) -> left + " + " + right,
    JoinWindows.ofTimeDifferenceAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1))
);

// Stream-Table join (no window needed, table lookup)
KStream<String, EnrichedOrder> enriched = orders.join(
    customers,  // KTable
    (order, customer) -> new EnrichedOrder(order, customer)
);

// Stream-GlobalKTable join (no repartition needed)
KStream<String, EnrichedOrder> enriched = orders.join(
    globalCustomers,  // GlobalKTable
    (key, value) -> value.getCustomerId(),  // key mapper
    (order, customer) -> new EnrichedOrder(order, customer)
);
```

### Aggregation

```java
// GroupBy + Count
stream.groupByKey()
    .count(Materialized.as("count-store"));

// GroupBy + Aggregate
stream.groupBy((key, value) -> value.getCustomerId())
    .aggregate(
        () -> 0L,  // initializer
        (key, value, aggregate) -> aggregate + value.getAmount(),  // aggregator
        Materialized.with(Serdes.String(), Serdes.Long())
    );
```

### Processor API (Low-Level)

```java
Topology topology = new Topology();
topology.addSource("source", "input-topic");
topology.addProcessor("processor", () -> new MyProcessor(), "source");
topology.addSink("sink", "output-topic", "processor");

// Mix with DSL via process()
stream.process(() -> new MyProcessor(), "my-state-store");

// Punctuate: schedule periodic callbacks
context.schedule(Duration.ofSeconds(30), PunctuationType.WALL_CLOCK_TIME,
    timestamp -> { /* flush state, emit aggregates */ });
```

### Interactive Queries (Queryable State)

```java
// Query state stores directly via REST without external database
// 1. Set APPLICATION_SERVER_CONFIG
props.put(StreamsConfig.APPLICATION_SERVER_CONFIG, "host:7070");

// 2. Route query to correct instance
KeyQueryMetadata meta = streams.queryMetadataForKey("store", key, serializer);
if (meta.activeHost().equals(thisHost)) {
    ReadOnlyKeyValueStore<String, Long> store =
        streams.store(StoreQueryParameters.fromNameAndType("store", QueryableStoreTypes.keyValueStore()));
    return store.get(key);
} else {
    // Forward to remote instance (implement HTTP/gRPC yourself)
}
```

## Gotchas

- **Key change triggers repartition** - `map()`, `selectKey()`, `flatMap()` all create internal repartition topics; use `mapValues()` when only changing values
- **State is LOCAL per task** - each task (= each partition) has its own isolated state store; data for stateful operations must be co-partitioned
- **`branch()` is deprecated** - use `split()` instead; branch names are composed as split name + branch name
- **Repartitioning creates intermediate topics** - auto-named internal topics; topology splits into subtopologies
- **GlobalKTable reads ALL partitions** - only use for small reference data; large tables will consume excessive memory
- **If only moving messages without transformation, don't use Kafka Streams** - just use consumer + producer

## See Also

- [[kafka-streams-state-stores]] - RocksDB, changelog topics, fault tolerance
- [[kafka-streams-windowing]] - tumbling, hopping, session, sliding windows
- [[ksqldb]] - SQL interface to Kafka Streams
- [[kafka-streams-time-semantics]] - event time vs processing time, timestamp extractors
- [Apache Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
