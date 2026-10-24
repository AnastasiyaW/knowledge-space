---
title: "Kafka Streams State Stores"
category: concepts
tags: [kafka, streams, state-store, rocksdb, changelog, repartition, fault-tolerance]
level: 3
source_sha256: aa8fc5abbcc6c45a27fe1d62563e1f0c003dd3dbad037030257d4d7cec9c8462
translation: machine
translated_at: '2026-10-24'
---
# Kafka Streams State Stores {#kafka-streams-state-stores}

State Stores stellen pro Kafka-Streams-Task lokalen Key-Value-Speicher bereit. Die Daten werden auf der Festplatte in RocksDB gehalten und über Changelog-Topics in Kafka gesichert. So wird fehlertolerante, zustandsbehaftete Verarbeitung mit automatischer Wiederherstellung ermöglicht.

## Kernfakten {#key-facts}

- Jeder Task (= jede Partition) hat seinen eigenen isolierten State Store; State Stores verschiedener Tasks werden NICHT geteilt
- State Stores werden durch ein **Changelog-Topic** gesichert (intern, automatisch angelegt, benannt `{app-id}-{store-name}-changelog`)
- Jede Aktualisierung des Stores wird zur Sicherung in das Changelog-Topic geschrieben
- Beim Neustart wird der Zustand aus dem Changelog-Topic wiederhergestellt (oder aus dem lokalen RocksDB-Cache, falls das Dateisystem erhalten blieb)
- Persistente Stores verwenden intern RocksDB und überstehen Prozessneustarts, sofern das Dateisystem erhalten bleibt
- Changelog-Topics werden kompaktiert, um die Wiederherstellung zu beschleunigen
- Standby-Replikate können Changelogs konsumieren, um ein schnelles Failover zu ermöglichen (`num.standby.replicas`)

## Muster {#patterns}

### Typen von State Stores {#state-store-types}

```java
// Persistent (RocksDB) - survives restarts, backed by changelog
Stores.persistentKeyValueStore("my-store")

// In-memory - lost on restart, rebuilt from changelog
Stores.inMemoryKeyValueStore("my-store")

// LRU cache - evicts oldest entries
Stores.lruMap("my-store", maxCacheSize)
```

### Erstellen und Registrieren von State Stores {#creating-and-registering-state-stores}

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

### Zugriff auf den Zustand in Processors {#accessing-state-in-processors}

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

### Changelog-Konfiguration {#changelog-configuration}

```java
// Disable changelog (state lost on restart)
storeBuilder.withLoggingDisabled();

// Configure changelog topic params
storeBuilder.withLoggingEnabled(Map.of(
    "cleanup.policy", "compact",
    "retention.ms", "604800000"  // 7 days
));
```

### Repartitionierung für korrekten Zustand {#repartitioning-for-correct-state}

```java
// Problem: records with same logical key in different partitions
// Solution: repartition before stateful operations

// Option 1: selectKey (auto-repartitions downstream)
stream.selectKey((key, value) -> value.getCustomerId());

// Option 2: explicit repartition
stream.repartition(Repartitioned.with(Serdes.String(), valueSerde));
```

Die Repartitionierung erzeugt ein **internes Zwischen-Topic** und teilt die Topologie in Subtopologien auf.

## Stolperfallen {#gotchas}

- **Der Zustand ist pro Task LOKAL** - landen Datensätze mit demselben Key in verschiedenen Partitionen (kein Key oder falsches Partitionieren), liefern zustandsbehaftete Operationen falsche Ergebnisse, weil verschiedene Tasks getrennte Zustände führen
- **Repartitionierung = internes Topic = zusätzliche Latenz** - jede Repartitionierung fügt einen Schreib-Lese-Schritt über Kafka hinzu; Key-Wechsel in der Topologie sollten minimiert werden
- **Speicherdruck durch RocksDB** - die Standardkonfiguration von RocksDB kann erheblichen Off-Heap-Speicher beanspruchen; in ressourcenbeschränkten Umgebungen `rocksdb.config.setter` anpassen
- **Die Wiederherstellung aus dem Changelog beim ersten Start ist langsam** - bei großen State Stores kann das initiale Bootstrapping aus dem Changelog Minuten bis Stunden dauern; für schnelleres Failover Standby-Replikate (`num.standby.replicas`) verwenden
- **Namen von State Stores müssen innerhalb der gesamten Topologie eindeutig sein**

## Siehe auch {#see-also}

- [[kafka-streams]] - zentrale KStream/KTable-Operationen, Grundlagen der Topologie
- [[kafka-streams-windowing]] - Windowed State Stores für zeitbasierte Aggregationen
- [[topics-and-partitions]] - wie die Partitionszuweisung die Lokalität von State Stores beeinflusst
- [Kafka Streams State Store-Dokumentation](https://kafka.apache.org/documentation/streams/developer-guide/processor-api.html#state-stores)
