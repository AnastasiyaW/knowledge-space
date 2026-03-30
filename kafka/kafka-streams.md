---
title: Kafka Streams
category: concepts
tags: [kafka, streams, kstream, ktable, stateful, windowing, exactly-once]
---

# Kafka Streams

Client library for building real-time stream processing applications on top of Apache Kafka. Runs as a regular JVM application - no separate cluster. Internally uses Consumer/Producer APIs. Provides a high-level DSL and a low-level Processor API. State stores backed by RocksDB with changelog topics for fault tolerance.

## KStream vs KTable vs GlobalKTable

### KStream - Event Stream

Unbounded, append-only stream of records. Every record is an independent event. INSERT semantics.

```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, Order> orders = builder.stream(
    "orders",
    Consumed.with(Serdes.String(), orderSerde)
);
```

Use when: event logs, clickstreams, transactions - every record matters independently.

### KTable - Changelog Stream

Compacted view of a topic. Each record is an UPDATE (upsert) keyed by record key. `null` value = tombstone (delete). Backed by a local state store. Only processes records from partitions assigned to the current instance.

```java
KTable<String, CustomerProfile> customers = builder.table(
    "customers",
    Materialized.<String, CustomerProfile, KeyValueStore<Bytes, byte[]>>as("customer-store")
        .withKeySerde(Serdes.String())
        .withValueSerde(customerSerde)
);
```

Use when: maintaining current state per key (user profiles, product catalog, account balances). Source topic should be compacted.

### GlobalKTable - Broadcast Table

Loads ALL partitions of a topic into every application instance. Not partitioned by [[consumer-groups]] - each instance has a full copy.

```java
GlobalKTable<String, Country> countries = builder.globalTable(
    "countries",
    Materialized.as("country-store")
);
```

Use when: small, slowly-changing reference/lookup data (country codes, currency rates, config). Enables non-key joins without repartitioning. **Never use for large datasets** - every instance holds the full dataset in memory/disk.

### Comparison Matrix

| Aspect | KStream | KTable | GlobalKTable |
|--------|---------|--------|--------------|
| Semantics | INSERT (all events) | UPSERT (latest per key) | UPSERT (latest per key) |
| Data loaded | Assigned partitions | Assigned partitions | ALL partitions |
| State store | No (unless stateful op) | Yes (always) | Yes (always, full copy) |
| Repartition needed for join | Depends on key | Yes (must be co-partitioned) | No |
| Memory footprint | Low | Proportional to unique keys | Full dataset per instance |
| Source topic | Any | Should be compacted | Must be compacted |

## Stateless Operations

Operations that transform records one-at-a-time without needing stored state.

```java
KStream<String, Order> orders = builder.stream("orders");

// filter - keep records matching predicate
KStream<String, Order> highValue = orders
    .filter((key, order) -> order.getAmount() > 1000.0);

// filterNot - inverse of filter
KStream<String, Order> lowValue = orders
    .filterNot((key, order) -> order.getAmount() > 1000.0);

// map - transform both key and value (triggers repartition flag)
KStream<String, String> mapped = orders
    .map((key, order) -> KeyValue.pair(order.getCustomerId(), order.toString()));

// mapValues - transform value only (no repartition)
KStream<String, OrderSummary> summaries = orders
    .mapValues(order -> new OrderSummary(order.getItem(), order.getAmount()));

// flatMap - one-to-many (triggers repartition flag)
KStream<String, LineItem> items = orders
    .flatMap((key, order) -> order.getItems().stream()
        .map(item -> KeyValue.pair(item.getSku(), item))
        .collect(Collectors.toList()));

// flatMapValues - one-to-many on values only (no repartition)
KStream<String, LineItem> itemsNoRekey = orders
    .flatMapValues(order -> order.getItems());

// selectKey - change the key (triggers repartition flag)
KStream<String, Order> byCustomer = orders
    .selectKey((key, order) -> order.getCustomerId());

// branch via split (replaces deprecated branch())
Map<String, KStream<String, Order>> branches = orders.split(Named.as("split-"))
    .branch((key, order) -> order.getRegion().equals("US"), Branched.as("us"))
    .branch((key, order) -> order.getRegion().equals("EU"), Branched.as("eu"))
    .defaultBranch(Branched.as("other"));

KStream<String, Order> usOrders = branches.get("split-us");
KStream<String, Order> euOrders = branches.get("split-eu");

// merge - combine streams
KStream<String, Order> combined = usOrders.merge(euOrders);

// peek - side-effect without modifying stream (logging, metrics)
orders.peek((key, order) -> log.info("Processing order: {}", key));
```

**Repartition trigger**: `map`, `flatMap`, `selectKey` set an internal repartition-required flag. Kafka Streams automatically creates an internal repartition topic before the next stateful operation (join, aggregate, reduce). This is because state stores are partition-local - see [[topics-and-partitions]].

## Stateful Operations

Require state stores. Backed by RocksDB (default) or in-memory stores. State is persisted to changelog topics for fault tolerance.

### groupByKey vs groupBy

```java
// groupByKey - uses existing key, no repartition
KGroupedStream<String, Order> grouped = orders.groupByKey();

// groupBy - new key, triggers repartition
KGroupedStream<String, Order> byCategory = orders
    .groupBy((key, order) -> order.getCategory());
```

Always prefer `groupByKey` when the current key is already correct - avoids an expensive repartition.

### count

```java
KTable<String, Long> orderCounts = orders
    .groupByKey()
    .count(Materialized.as("order-counts-store"));
```

### reduce

Combines values using a reducer. Input and output types must be the same.

```java
KTable<String, Order> latestOrder = orders
    .groupByKey()
    .reduce(
        (aggValue, newValue) -> newValue,  // keep latest
        Materialized.as("latest-orders-store")
    );
```

### aggregate

Most flexible. Input and output types can differ. Requires initializer + aggregator.

```java
KTable<String, OrderStats> stats = orders
    .groupByKey()
    .aggregate(
        // Initializer
        () -> new OrderStats(0, 0.0),
        // Aggregator
        (key, order, agg) -> new OrderStats(
            agg.getCount() + 1,
            agg.getTotal() + order.getAmount()
        ),
        Materialized.<String, OrderStats, KeyValueStore<Bytes, byte[]>>as("order-stats")
            .withValueSerde(orderStatsSerde)
    );
```

### State Store Types

| Store | Class | Persistence | Use case |
|-------|-------|-------------|----------|
| Persistent KV | `Stores.persistentKeyValueStore(name)` | RocksDB on disk | Default. Survives restarts. |
| In-memory KV | `Stores.inMemoryKeyValueStore(name)` | RAM only | Fast but rebuilt from changelog on restart |
| LRU Map | `Stores.lruMap(name, maxSize)` | RAM, bounded | Caching, bounded memory |
| Persistent Window | `Stores.persistentWindowStore(...)` | RocksDB | Windowed aggregations |
| Persistent Session | `Stores.persistentSessionStore(...)` | RocksDB | Session windows |

Custom state store via `StoreBuilder`:

```java
StoreBuilder<KeyValueStore<String, Long>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("my-store"),
        Serdes.String(),
        Serdes.Long()
    ).withCachingEnabled()   // enable record cache
     .withLoggingEnabled(Map.of(  // changelog topic config
         "cleanup.policy", "compact",
         "retention.ms", "172800000"  // 2 days
     ));

builder.addStateStore(storeBuilder);
```

## Windowing

Constrain stateful operations to time-bounded ranges. All windows use event time by default (record timestamp).

### Tumbling Windows

Fixed-size, non-overlapping, gap-free. Each event belongs to exactly one window.

```java
KTable<Windowed<String>, Long> tumblingCounts = orders
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .count(Materialized.as("tumbling-counts"));

// With grace period - accept late-arriving records
KTable<Windowed<String>, Long> withGrace = orders
    .groupByKey()
    .windowedBy(
        TimeWindows.ofSizeAndGrace(
            Duration.ofMinutes(5),   // window size
            Duration.ofMinutes(1)    // grace period for late data
        )
    )
    .count();
```

### Hopping Windows

Fixed-size, overlapping. Each event can belong to multiple windows.

```java
// 10-minute windows, advancing every 2 minutes
// Each event appears in 5 windows (10/2)
KTable<Windowed<String>, Long> hoppingCounts = orders
    .groupByKey()
    .windowedBy(
        TimeWindows.ofSizeAndGrace(Duration.ofMinutes(10), Duration.ofMinutes(2))
            .advanceBy(Duration.ofMinutes(2))
    )
    .count();
```

### Sliding Windows

Fixed-size window anchored to each event's timestamp. A new window is created for each distinct pair of events that fall within the window size of each other.

```java
KTable<Windowed<String>, Long> slidingCounts = orders
    .groupByKey()
    .windowedBy(
        SlidingWindows.ofTimeDifferenceAndGrace(
            Duration.ofMinutes(5),   // window size
            Duration.ofMinutes(1)    // grace
        )
    )
    .count();
```

### Session Windows

Dynamic windows based on activity gaps. Per-key: inactivity gap closes the window. New activity after the gap starts a new session.

```java
KTable<Windowed<String>, Long> sessionCounts = orders
    .groupByKey()
    .windowedBy(
        SessionWindows.ofInactivityGapAndGrace(
            Duration.ofMinutes(5),   // inactivity gap
            Duration.ofMinutes(2)    // grace period
        )
    )
    .count();
```

### Grace Period

Controls how long a window accepts late-arriving records after the window closes. Records arriving after `window_end + grace_period` are dropped.

- `ofSizeWithNoGrace` / `ofInactivityGapWithNoGrace` - drops late records immediately after window closes
- Default grace period was 24 hours in older versions; now must be explicitly set
- Grace period adds to memory usage: window state is retained longer

### Suppression

By default, windowed aggregations emit intermediate results (one update per input record). Suppression holds results until the window closes, then emits a single final result.

```java
KTable<Windowed<String>, Long> finalCounts = orders
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(
        Duration.ofMinutes(5), Duration.ofMinutes(1)))
    .count()
    .suppress(
        Suppressed.untilWindowCloses(Suppressed.BufferConfig.unbounded())
    );

// With bounded buffer - spill to disk if buffer exceeds limit
KTable<Windowed<String>, Long> boundedSuppress = orders
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(
        Duration.ofMinutes(5), Duration.ofMinutes(1)))
    .count()
    .suppress(
        Suppressed.untilWindowCloses(
            Suppressed.BufferConfig
                .maxBytes(1_000_000L)      // 1MB buffer limit
                .shutDownWhenFull()         // or .emitEarlyWhenFull()
        )
    );
```

### Window Type Visual

```
Tumbling:  |--W1--|--W2--|--W3--|      Fixed, non-overlapping
Hopping:   |----W1----|                Fixed, overlapping
              |----W2----|
                 |----W3----|
Sliding:       [===event===]           Around each event timestamp
Session:   |==activity==|  gap  |==activity==|  Dynamic per key
```

## Joins

All joins require records to share the same key. If keys differ, repartition first via `selectKey`.

### KStream-KStream Join (Windowed)

Both sides are event streams. Requires a `JoinWindows` because you cannot join two infinite streams without a time boundary.

```java
KStream<String, Order> orders = builder.stream("orders");
KStream<String, Payment> payments = builder.stream("payments");

// Inner join: emit when both sides have a matching record within window
KStream<String, EnrichedOrder> joined = orders.join(
    payments,
    (order, payment) -> new EnrichedOrder(order, payment),
    JoinWindows.ofTimeDifferenceAndGrace(
        Duration.ofMinutes(5),   // match window
        Duration.ofMinutes(1)    // grace period
    ),
    StreamJoined.with(Serdes.String(), orderSerde, paymentSerde)
);

// Left join: emit order even if no payment matches
KStream<String, EnrichedOrder> leftJoined = orders.leftJoin(
    payments,
    (order, payment) -> new EnrichedOrder(order, payment),  // payment may be null
    JoinWindows.ofTimeDifferenceAndGrace(
        Duration.ofMinutes(5), Duration.ofMinutes(1)),
    StreamJoined.with(Serdes.String(), orderSerde, paymentSerde)
);

// Outer join: emit from either side, other may be null
KStream<String, EnrichedOrder> outerJoined = orders.outerJoin(
    payments,
    (order, payment) -> new EnrichedOrder(order, payment),
    JoinWindows.ofTimeDifferenceAndGrace(
        Duration.ofMinutes(5), Duration.ofMinutes(1)),
    StreamJoined.with(Serdes.String(), orderSerde, paymentSerde)
);
```

Both input topics must be **co-partitioned**: same number of partitions, same partitioning strategy.

### KStream-KTable Join (Non-Windowed)

Stream event enriched with current table state. No window needed - table is always "current." The stream drives output: each stream record triggers a lookup in the table.

```java
KStream<String, Order> orders = builder.stream("orders");
KTable<String, Customer> customers = builder.table("customers");

// Inner join: only emits if customer exists
KStream<String, EnrichedOrder> enriched = orders.join(
    customers,
    (order, customer) -> new EnrichedOrder(order, customer)
);

// Left join: emits even if customer is null
KStream<String, EnrichedOrder> leftEnriched = orders.leftJoin(
    customers,
    (order, customer) -> new EnrichedOrder(order, customer)
);
```

Requires co-partitioning. To avoid this constraint, use `GlobalKTable`:

```java
GlobalKTable<String, Country> countries = builder.globalTable("countries");

// No co-partitioning required. KeyValueMapper extracts the foreign key.
KStream<String, EnrichedOrder> withCountry = orders.join(
    countries,
    (orderKey, order) -> order.getCountryCode(),  // extract join key from stream record
    (order, country) -> order.withCountry(country)
);
```

### KTable-KTable Join

Both sides are tables. Result is a KTable. Updates from either side trigger a new join result.

```java
KTable<String, Customer> customers = builder.table("customers");
KTable<String, Address> addresses = builder.table("addresses");

// Inner join
KTable<String, CustomerWithAddress> joined = customers.join(
    addresses,
    (customer, address) -> new CustomerWithAddress(customer, address)
);

// Left join, outer join also available
```

Requires co-partitioning. No windowing needed.

### KTable-KTable Foreign Key Join

Join KTables on a non-primary key. Available since Kafka Streams 2.4.

```java
KTable<String, Order> orders = builder.table("orders");         // key: orderId
KTable<String, Customer> customers = builder.table("customers"); // key: customerId

// Join orders to customers via order.customerId (foreign key)
KTable<String, EnrichedOrder> enriched = orders.join(
    customers,
    order -> order.getCustomerId(),   // foreign key extractor
    (order, customer) -> new EnrichedOrder(order, customer)
);
```

### Join Requirements Summary

| Join Type | Windowed | Co-partitioned | Result Type |
|-----------|----------|----------------|-------------|
| KStream-KStream | Yes (required) | Yes | KStream |
| KStream-KTable | No | Yes | KStream |
| KStream-GlobalKTable | No | No | KStream |
| KTable-KTable | No | Yes | KTable |
| KTable-KTable (FK) | No | No | KTable |

## Exactly-Once Semantics

Kafka Streams wraps read-process-write in [[kafka-transactions]]. Guarantees that for each input record, the output record and the offset commit happen atomically.

### Configuration

```java
Properties props = new Properties();
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
    StreamsConfig.EXACTLY_ONCE_V2);  // Kafka 2.6+
```

`exactly_once_v2` (replaces deprecated `exactly_once`):
- Uses a single transaction producer per StreamThread (not per task)
- Significantly fewer transactional producers = less overhead on brokers
- Requires broker version >= 2.5

### What It Guarantees

1. Each input record is processed exactly once
2. Output records + offset commits are atomic
3. State store updates are consistent with output + offsets
4. Zombie protection: fenced producers from old instances cannot write

### What It Does NOT Guarantee

- Exactly-once delivery to external systems (databases, APIs). Use at-least-once + idempotent writes for those.
- Deduplication of records already in the input topic. That is the producer's responsibility.

### Performance Impact

- Adds transaction overhead: begin, commit, abort on each `commit.interval.ms`
- ~5-20% throughput reduction depending on workload
- Increase `commit.interval.ms` (default 100ms with EOS) to reduce transaction frequency at the cost of higher latency

## Interactive Queries

Query local state stores directly from your application without reading from Kafka. Turn a Kafka Streams app into a queryable microservice.

### ReadOnlyKeyValueStore

```java
// Build and start the topology
KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();

// Query a named state store
ReadOnlyKeyValueStore<String, OrderStats> store =
    streams.store(
        StoreQueryParameters.fromNameAndType(
            "order-stats",
            QueryableStoreTypes.keyValueStore()
        )
    );

// Point lookup
OrderStats stats = store.get("customer-123");

// Range scan
KeyValueIterator<String, OrderStats> range =
    store.range("customer-100", "customer-200");
while (range.hasNext()) {
    KeyValue<String, OrderStats> kv = range.next();
    // process kv.key, kv.value
}
range.close();  // MUST close iterators

// Iterate all entries
KeyValueIterator<String, OrderStats> all = store.all();
// ...
all.close();
```

### ReadOnlyWindowStore

```java
ReadOnlyWindowStore<String, Long> windowStore =
    streams.store(
        StoreQueryParameters.fromNameAndType(
            "tumbling-counts",
            QueryableStoreTypes.windowStore()
        )
    );

// Fetch all windows for a key in a time range
Instant from = Instant.now().minus(Duration.ofHours(1));
Instant to = Instant.now();
WindowStoreIterator<Long> iter = windowStore.fetch("customer-123", from, to);
while (iter.hasNext()) {
    KeyValue<Long, Long> kv = iter.next();
    // kv.key = window start timestamp, kv.value = count
}
iter.close();
```

### ReadOnlySessionStore

```java
ReadOnlySessionStore<String, Long> sessionStore =
    streams.store(
        StoreQueryParameters.fromNameAndType(
            "session-counts",
            QueryableStoreTypes.sessionStore()
        )
    );

KeyValueIterator<Windowed<String>, Long> sessions =
    sessionStore.fetch("customer-123");
while (sessions.hasNext()) {
    KeyValue<Windowed<String>, Long> kv = sessions.next();
    Window window = kv.key.window();
    // window.start(), window.end(), kv.value
}
sessions.close();
```

### Distributed Queries

State stores are partition-local. In a multi-instance deployment, a key's state lives on the instance that owns that key's partition. Use `KafkaStreams.metadataForKey()` to discover which instance holds a given key, then route the query via HTTP/gRPC.

```java
// Find which instance has the data for a key
KeyQueryMetadata metadata = streams.queryMetadataForKey(
    "order-stats",
    "customer-123",
    Serdes.String().serializer()
);

if (metadata.equals(KeyQueryMetadata.NOT_AVAILABLE)) {
    // Store not yet ready (rebalancing)
    throw new RetryableException();
}

HostInfo activeHost = metadata.activeHost();
if (isLocalHost(activeHost)) {
    // Query local store directly
    return store.get("customer-123");
} else {
    // Forward request to the remote instance
    return httpClient.get(
        "http://" + activeHost.host() + ":" + activeHost.port()
        + "/api/stats/customer-123"
    );
}
```

Configure each instance to advertise its host/port:

```java
props.put(StreamsConfig.APPLICATION_SERVER_CONFIG, "myhost:7070");
```

## Topology: Processor API vs DSL

### DSL (High-Level)

Declarative, functional API. `StreamsBuilder` creates the topology implicitly.

```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, String> stream = builder.stream("input");
stream.filter((k, v) -> v != null)
      .mapValues(v -> v.toUpperCase())
      .to("output");

Topology topology = builder.build();
```

### Processor API (Low-Level)

Full control over processing logic. Explicit topology construction with `Topology` object.

```java
Topology topology = new Topology();

topology.addSource("source", "input-topic")
        .addProcessor("process", () -> new Processor<String, String, String, String>() {
            private ProcessorContext<String, String> context;
            private KeyValueStore<String, Long> store;

            @Override
            public void init(ProcessorContext<String, String> context) {
                this.context = context;
                this.store = context.getStateStore("my-store");
                // Schedule periodic punctuation
                context.schedule(
                    Duration.ofSeconds(30),
                    PunctuationType.WALL_CLOCK_TIME,
                    this::punctuate
                );
            }

            @Override
            public void process(Record<String, String> record) {
                Long count = store.get(record.key());
                count = (count == null) ? 1L : count + 1;
                store.put(record.key(), count);

                if (count % 100 == 0) {
                    context.forward(record.withValue("milestone: " + count));
                }
            }

            private void punctuate(long timestamp) {
                // Periodic logic: emit aggregates, clean expired state, etc.
                try (KeyValueIterator<String, Long> iter = store.all()) {
                    while (iter.hasNext()) {
                        KeyValue<String, Long> kv = iter.next();
                        context.forward(new Record<>(kv.key, "periodic: " + kv.value, timestamp));
                    }
                }
            }
        }, "source")
        .addStateStore(
            Stores.keyValueStoreBuilder(
                Stores.persistentKeyValueStore("my-store"),
                Serdes.String(), Serdes.Long()
            ),
            "process"  // attach store to this processor
        )
        .addSink("sink", "output-topic", "process");
```

### Mixing DSL and Processor API

Use `process()` or `transformValues()` in the DSL to inject custom Processor API logic:

```java
StreamsBuilder builder = new StreamsBuilder();
builder.addStateStore(storeBuilder);

builder.stream("input")
    .filter((k, v) -> v != null)
    .process(() -> new MyCustomProcessor(), "my-store")  // processor with state store
    .to("output");
```

### Sub-Topologies

Kafka Streams partitions the topology into **sub-topologies** at topic boundaries (source/sink/repartition topics). Each sub-topology is independently parallelized and assigned to tasks.

```
Sub-topology 0: source(input) -> filter -> selectKey -> sink(repartition-topic)
Sub-topology 1: source(repartition-topic) -> aggregate -> sink(output)
```

Inspect topology structure:

```java
Topology topology = builder.build();
System.out.println(topology.describe());
```

Output shows sub-topologies, sources, processors, sinks, and state stores. Useful for debugging partition assignment and identifying unnecessary repartitions.

## Key Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `application.id` | Unique app identifier. Used as consumer group.id, prefix for internal topics, state store directory name. | Required |
| `bootstrap.servers` | Kafka broker addresses | Required |
| `num.stream.threads` | Processing threads per instance. Each thread runs independent tasks. Scale up to partition count. | 1 |
| `state.dir` | Base directory for local state stores (RocksDB). Each app gets a subdirectory. | `/tmp/kafka-streams` |
| `commit.interval.ms` | How often to commit offsets and flush state stores. Lower = less duplicate processing on failure. Higher = better throughput. | 30000 (at_least_once), 100 (exactly_once) |
| `cache.max.bytes.buffering` | Total memory for record caching across all threads. Deduplicates updates before writing to state stores and downstream. 0 = disable caching (every update propagates immediately). | 10485760 (10MB) |
| `processing.guarantee` | `at_least_once` or `exactly_once_v2` | `at_least_once` |
| `default.key.serde` | Default Serde for keys | ByteArraySerde |
| `default.value.serde` | Default Serde for values | ByteArraySerde |
| `application.server` | `host:port` for interactive queries. Advertised via consumer group metadata. | none |
| `num.standby.replicas` | Number of standby replicas per state store. Pre-loads changelog for faster failover. | 0 |
| `topology.optimization` | Set to `all` to enable topology optimizations (merge repartition topics, reuse source topics as changelogs). | `none` |
| `max.task.idle.ms` | Max time to wait for data on all input partitions before processing. Helps with event-time synchronization. | 0 |
| `rocksdb.config.setter` | Custom RocksDB config (block cache size, compaction style, bloom filters). | none |

### RocksDB Tuning

```java
props.put(StreamsConfig.ROCKSDB_CONFIG_SETTER_CLASS_CONFIG,
    CustomRocksDBConfig.class.getName());

public class CustomRocksDBConfig implements RocksDBConfigSetter {
    @Override
    public void setConfig(String storeName, Options options,
                          Map<String, Object> configs) {
        BlockBasedTableConfig tableConfig = (BlockBasedTableConfig) options.tableFormatConfig();
        tableConfig.setBlockCacheSize(64 * 1024 * 1024L);  // 64MB block cache
        tableConfig.setBlockSize(4096);
        options.setTableFormatConfig(tableConfig);
        options.setMaxWriteBufferNumber(3);
        options.setWriteBufferSize(16 * 1024 * 1024);      // 16MB write buffer
        options.setCompactionStyle(CompactionStyle.UNIVERSAL);
    }

    @Override
    public void close(String storeName, Options options) {}
}
```

## Common Patterns

### Event Enrichment Pipeline

```java
StreamsBuilder builder = new StreamsBuilder();

KStream<String, Order> orders = builder.stream("orders");
KTable<String, Customer> customers = builder.table("customers");
GlobalKTable<String, Product> products = builder.globalTable("products");

orders
    // Enrich with customer data (co-partitioned join)
    .join(customers,
        (order, customer) -> order.withCustomer(customer))
    // Enrich with product data (global table, no co-partition needed)
    .join(products,
        (key, order) -> order.getProductId(),
        (order, product) -> order.withProduct(product))
    // Filter and route
    .split(Named.as("route-"))
    .branch((k, o) -> o.getTotal() > 500, Branched.withConsumer(
        s -> s.to("high-value-orders")))
    .branch((k, o) -> o.isSubscription(), Branched.withConsumer(
        s -> s.to("subscription-orders")))
    .defaultBranch(Branched.withConsumer(
        s -> s.to("standard-orders")));
```

### Deduplication via State Store

```java
builder.stream("events")
    .transform(() -> new Transformer<String, Event, KeyValue<String, Event>>() {
        private KeyValueStore<String, Long> seen;

        @Override
        public void init(ProcessorContext context) {
            seen = context.getStateStore("dedup-store");
            // Purge expired entries every minute
            context.schedule(Duration.ofMinutes(1),
                PunctuationType.WALL_CLOCK_TIME, ts -> {
                    long cutoff = ts - Duration.ofHours(1).toMillis();
                    try (KeyValueIterator<String, Long> it = seen.all()) {
                        while (it.hasNext()) {
                            KeyValue<String, Long> kv = it.next();
                            if (kv.value < cutoff) seen.delete(kv.key);
                        }
                    }
                });
        }

        @Override
        public KeyValue<String, Event> transform(String key, Event event) {
            String dedupKey = event.getIdempotencyKey();
            if (seen.get(dedupKey) != null) return null;  // duplicate
            seen.put(dedupKey, System.currentTimeMillis());
            return KeyValue.pair(key, event);
        }

        @Override
        public void close() {}
    }, "dedup-store")
    .filter((k, v) -> v != null)
    .to("deduplicated-events");
```

### Full Application Bootstrap

```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "order-processing-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092");
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE_V2);
props.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 3);
props.put(StreamsConfig.STATE_DIR_CONFIG, "/var/lib/kafka-streams");
props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 100);
props.put(StreamsConfig.APPLICATION_SERVER_CONFIG, "localhost:7070");
props.put(StreamsConfig.NUM_STANDBY_REPLICAS_CONFIG, 1);

StreamsBuilder builder = new StreamsBuilder();
// ... build topology ...

KafkaStreams streams = new KafkaStreams(builder.build(), props);

// Graceful shutdown
Runtime.getRuntime().addShutdownHook(new Thread(streams::close));

// State listener for health checks
streams.setStateListener((newState, oldState) -> {
    if (newState == KafkaStreams.State.RUNNING) {
        log.info("Streams application is running");
    }
    if (newState == KafkaStreams.State.ERROR) {
        log.error("Streams application error, shutting down");
        streams.close();
    }
});

// Uncaught exception handler
streams.setUncaughtExceptionHandler(ex -> {
    log.error("Uncaught exception in stream thread", ex);
    return StreamsUncaughtExceptionHandler.StreamThreadExceptionResponse.REPLACE_THREAD;
});

streams.start();
```

## Gotchas

- **State stores are partition-local.** Aggregating by a key that differs from the input key requires repartitioning first (`selectKey` / `groupBy`). Without it, records for the same logical key may land in different state stores, producing wrong results.
- **KTable caches updates.** It does NOT emit every update downstream. Controlled by `cache.max.bytes.buffering` and `commit.interval.ms`. Set `cache.max.bytes.buffering=0` for immediate propagation (at the cost of higher load).
- **GlobalKTable loads all data into every instance.** Only use for small lookup datasets. For a 10GB table with 5 instances, each instance stores 10GB (not 2GB).
- **Repartition creates internal topics.** Every `selectKey()`, `map()`, `flatMap()` that changes the key triggers an internal repartition topic. Plan for extra topic count, disk usage, and network I/O.
- **Stream-Stream joins REQUIRE windows.** No window = compile error. Window too small = missed matches. Window too large = excessive state and memory.
- **Close iterators.** `KeyValueIterator`, `WindowStoreIterator` from state stores MUST be closed. Unclosed iterators leak RocksDB resources and eventually crash the application.
- **`exactly_once_v2` requires brokers >= 2.5.** Using it with older brokers silently falls back to `at_least_once` or throws at startup depending on the version.
- **`commit.interval.ms` default changes with EOS.** 30s for `at_least_once`, 100ms for `exactly_once_v2`. Don't blindly override without understanding the tradeoff.
- **`topology.optimization=all`** can merge repartition topics and reuse source topics as changelogs. Always test after enabling - it changes internal topic layout, making rolling upgrades from the non-optimized topology incompatible.
- **Standby replicas (`num.standby.replicas`)** pre-load changelog data on other instances. Speeds up failover but doubles (or more) state store disk usage across the cluster.

## See Also

- [[consumer-groups]] - Kafka Streams uses consumer groups internally for partition assignment and rebalancing
- [[topics-and-partitions]] - partitioning determines state store locality and parallelism
- [[ksqldb]] - SQL interface built on Kafka Streams; same semantics, declarative syntax
- [[kafka-transactions]] - underpins `exactly_once_v2` processing guarantee
