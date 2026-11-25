---
title: "Kafka Streams"
category: concepts
tags: [kafka, streams, kstream, ktable, topology, serde, stateless, processor-api]
level: 3
source_sha256: 118832b6955e481686cf1e633f16ae72d81a588de4a650d60e67a090991904c5
translation: machine
translated_at: '2026-10-24'
---
# Kafka Streams {#kafka-streams}

Kafka Streams ist eine Client-Bibliothek (kein Framework und kein eigenständiger Cluster) zum Erstellen von Stream-Processing-Anwendungen als DAGs (Directed Acyclic Graphs). Sie bietet höherwertige Abstraktionen über den Producer- und Consumer-APIs und unterstützt zustandslose und zustandsbehaftete Transformationen.

## Wichtige Fakten {#key-facts}

- Füge die Abhängigkeit `kafka-streams` in deine Anwendung ein. Sie läuft als gewöhnlicher JVM-Prozess, ohne separaten Cluster.
- Intern basiert sie auf den Producer- und Consumer-APIs. Es gibt keine Magie.
- Verarbeitet Events aus Input-Topics, transformiert sie und schreibt die Ergebnisse in Output-Topics.
- **Topology**: ein DAG aus Stream-Processors (Knoten), die durch Streams (Kanten) verbunden sind. Anzeige über `topology.describe()`
- **Serde**: Paar aus Serializer und Deserializer; `Serdes.String()`, `Serdes.Integer()` und `Serdes.Long()` für primitive Typen
- **KStream**: unbegrenzter Stream von Records; jeder Record ist ein unabhängiges Event
- **KTable**: Changelog-Stream; jeder Record ist ein Update für einen Key; nur der jeweils neueste Wert pro Key ist relevant
- **GlobalKTable**: liest ALLE Partitionen eines Topics; geeignet für kleine Referenzdaten (für Joins ist keine Repartitionierung nötig)
- Kafka Streams verwaltet Offsets automatisch (`commit.interval.ms`, Standardwert 30s)

## Muster {#patterns}

### Zustandslose KStream-Operationen {#kstream-stateless-operations}

| Operation | Zweck | Löst Repartitionierung aus? |
|-----------|-------|----------------------------|
| `filter(predicate)` | Passende Records behalten | Nein |
| `mapValues(mapper)` | Nur den Wert transformieren | Nein |
| `map(mapper)` | Key und Wert transformieren | Ja |
| `flatMap(mapper)` | Einer zu null oder mehreren, kann den Key ändern | Ja |
| `flatMapValues(mapper)` | Einer zu null oder mehreren, nur Wert | Nein |
| `selectKey(mapper)` | Key ändern | Ja |
| `split()` / `branch` | Über eine Bedingung in Sub-Streams aufteilen | Nein |
| `merge(otherStream)` | Zwei Streams zusammenführen | Nein |
| `peek(action)` | Side-Effect (Logging) | Nein |
| `foreach(action)` | Terminaler Side-Effect | Nicht zutreffend |
| `to(topic)` | In ein Output-Topic schreiben | Nicht zutreffend |

### Beispiel für Stream-Verarbeitung {#stream-processing-example}

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

### Verwendung von KTable {#ktable-usage}

```java
// KTable: topic interpreted as changelog (upserts)
KTable<String, String> users = builder.table("users",
    Consumed.with(Serdes.String(), Serdes.String()));

// KTable caching: deduplicates rapid updates to same key
// Controlled by cache.max.bytes.buffering (default 10MB) and commit.interval.ms (default 30s)
```

### Joins {#joins}

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

### Aggregation {#aggregation}

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

### Processor API (Low-Level) {#processor-api-low-level}

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

### Interaktive Abfragen (Queryable State) {#interactive-queries-queryable-state}

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

## Stolperfallen {#gotchas}

- **Eine Key-Änderung löst Repartitionierung aus**: `map()`, `selectKey()` und `flatMap()` erzeugen interne Repartitionierungs-Topics. Verwende `mapValues()`, wenn nur der Wert geändert wird.
- **State ist LOKAL pro Task**: Jeder Task (= jede Partition) hat einen eigenen, isolierten State-Store. Die Daten für zustandsbehaftete Operationen müssen co-partitioniert sein.
- **`branch()` ist veraltet**: Verwende stattdessen `split()`. Branch-Namen setzen sich aus Split-Name und Branch-Name zusammen.
- **Repartitionierung erzeugt Zwischen-Topics**: Interne Topics werden automatisch benannt, und die Topology wird in Subtopologien aufgeteilt.
- **GlobalKTable liest ALLE Partitionen**: Nur für kleine Referenzdaten verwenden. Große Tabellen verbrauchen übermäßig viel Speicher.
- **Wenn Nachrichten nur ohne Transformation verschoben werden, verwende Kafka Streams nicht**: Ein Consumer plus Producer genügt.

## Siehe auch {#see-also}

- [[kafka-streams-state-stores]] - RocksDB, Changelog-Topics, Fehlertoleranz
- [[kafka-streams-windowing]] - Tumbling-, Hopping-, Session- und Sliding-Windows
- [[ksqldb]] - SQL-Schnittstelle für Kafka Streams
- [[kafka-streams-time-semantics]] - Event-Time vs. Processing-Time, Timestamp-Extractors
- [Apache Kafka Streams Dokumentation](https://kafka.apache.org/documentation/streams/)
