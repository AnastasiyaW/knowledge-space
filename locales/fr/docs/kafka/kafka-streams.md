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

Kafka Streams est une bibliothèque cliente (et non un framework ni un cluster distinct) permettant de construire des applications de traitement de flux sous forme de DAG (graphes orientés acycliques). Elle fournit des abstractions de plus haut niveau au-dessus des API Producer/Consumer, avec la prise en charge des transformations sans état et avec état.

## Points clés {#key-facts}

- Ajouter la dépendance `kafka-streams` à votre application : elle s'exécute comme un processus JVM ordinaire, sans cluster séparé
- Construite en interne sur les API Producer/Consumer, sans magie
- Traite les événements des topics d'entrée, les transforme et écrit les résultats dans les topics de sortie
- **Topology** : un DAG de processeurs de flux (nœuds) reliés par des flux (arêtes) ; à visualiser via `topology.describe()`
- **Serde** : paire Serializer/Deserializer ; `Serdes.String()`, `Serdes.Integer()`, `Serdes.Long()` pour les types primitifs
- **KStream** : flux non borné d'enregistrements ; chaque enregistrement est un événement indépendant
- **KTable** : flux de changelog ; chaque enregistrement est une mise à jour d'une clé ; seule la dernière valeur par clé compte
- **GlobalKTable** : lit TOUTES les partitions d'un topic ; utile pour de petites données de référence (aucun repartitionnement nécessaire pour les jointures)
- Kafka Streams gère automatiquement les offsets (`commit.interval.ms`, 30 s par défaut)

## Modèles {#patterns}

### Opérations sans état sur KStream {#kstream-stateless-operations}

| Opération | Rôle | Déclenche un repartitionnement ? |
|-----------|------|----------------------------------|
| `filter(predicate)` | Conserver les enregistrements correspondants | Non |
| `mapValues(mapper)` | Transformer uniquement la valeur | Non |
| `map(mapper)` | Transformer la clé et la valeur | Oui |
| `flatMap(mapper)` | Un vers zéro ou plusieurs, peut modifier la clé | Oui |
| `flatMapValues(mapper)` | Un vers zéro ou plusieurs, valeur uniquement | Non |
| `selectKey(mapper)` | Modifier la clé | Oui |
| `split()` / `branch` | Router vers des sous-flux selon une condition | Non |
| `merge(otherStream)` | Combiner deux flux | Non |
| `peek(action)` | Effet de bord (journalisation) | Non |
| `foreach(action)` | Effet de bord terminal | N/A |
| `to(topic)` | Écrire dans le topic de sortie | N/A |

### Exemple de traitement de flux {#stream-processing-example}

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

### Utilisation de KTable {#ktable-usage}

```java
// KTable: topic interpreted as changelog (upserts)
KTable<String, String> users = builder.table("users",
    Consumed.with(Serdes.String(), Serdes.String()));

// KTable caching: deduplicates rapid updates to same key
// Controlled by cache.max.bytes.buffering (default 10MB) and commit.interval.ms (default 30s)
```

### Jointures {#joins}

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

### Agrégation {#aggregation}

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

### Processor API (bas niveau) {#processor-api-low-level}

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

### Requêtes interactives (état interrogeable) {#interactive-queries-queryable-state}

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

## Pièges à éviter {#gotchas}

- **Un changement de clé déclenche un repartitionnement** : `map()`, `selectKey()` et `flatMap()` créent tous des topics de repartitionnement internes ; utilisez `mapValues()` lorsque seule la valeur change
- **L'état est LOCAL à chaque tâche** : chaque tâche (soit chaque partition) possède son propre magasin d'état isolé ; les données des opérations avec état doivent être co-partitionnées
- **`branch()` est déprécié** : utilisez `split()` à la place ; les noms de branches sont composés du nom du split suivi du nom de la branche
- **Le repartitionnement crée des topics intermédiaires** : topics internes nommés automatiquement ; la topologie se découpe en sous-topologies
- **GlobalKTable lit TOUTES les partitions** : à réserver aux petites données de référence ; les grandes tables consommeront une mémoire excessive
- **Si vous ne faites que déplacer des messages sans transformation, n'utilisez pas Kafka Streams** : un simple consumer + producer suffit

## Voir aussi {#see-also}

- [[kafka-streams-state-stores]] - RocksDB, topics de changelog, tolérance aux pannes
- [[kafka-streams-windowing]] - fenêtres tumbling, hopping, session et sliding
- [[ksqldb]] - interface SQL pour Kafka Streams
- [[kafka-streams-time-semantics]] - temps d'événement vs temps de traitement, extracteurs de timestamp
- [Documentation Apache Kafka Streams](https://kafka.apache.org/documentation/streams/)
