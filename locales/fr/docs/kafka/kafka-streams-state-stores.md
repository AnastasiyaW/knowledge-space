---
title: "Stores d'état de Kafka Streams"
category: concepts
tags: [kafka, streams, state-store, rocksdb, changelog, repartition, fault-tolerance]
level: 3
source_sha256: aa8fc5abbcc6c45a27fe1d62563e1f0c003dd3dbad037030257d4d7cec9c8462
translation: machine
translated_at: '2026-10-24'
---
# Stores d'état de Kafka Streams {#kafka-streams-state-stores}

Les state stores fournissent un stockage local clé-valeur par tâche Kafka Streams, adossé à RocksDB sur disque et à des topics de changelog dans Kafka. Ils permettent un traitement avec état tolérant aux pannes, avec reprise automatique.

## Points clés {#key-facts}

- Chaque tâche (= chaque partition) possède son propre state store isolé ; les state stores de tâches différentes ne sont PAS partagés
- Les state stores sont adossés à un **topic de changelog** (interne, créé automatiquement, nommé `{app-id}-{store-name}-changelog`)
- Chaque mise à jour du store est écrite dans le topic de changelog pour garantir la durabilité
- Au redémarrage, l'état est reconstruit à partir du topic de changelog (ou à partir du cache RocksDB local si le système de fichiers a été conservé)
- Les stores persistants utilisent RocksDB en interne et survivent aux redémarrages du processus si le système de fichiers est conservé
- Les topics de changelog sont compactés pour accélérer la reprise
- Les réplicas standby peuvent consommer les changelogs pour un basculement rapide (`num.standby.replicas`)

## Motifs {#patterns}

### Types de state stores {#state-store-types}

```java
// Persistent (RocksDB) - survives restarts, backed by changelog
Stores.persistentKeyValueStore("my-store")

// In-memory - lost on restart, rebuilt from changelog
Stores.inMemoryKeyValueStore("my-store")

// LRU cache - evicts oldest entries
Stores.lruMap("my-store", maxCacheSize)
```

### Création et enregistrement des state stores {#creating-and-registering-state-stores}

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

### Accès à l'état dans les processors {#accessing-state-in-processors}

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

### Configuration du changelog {#changelog-configuration}

```java
// Disable changelog (state lost on restart)
storeBuilder.withLoggingDisabled();

// Configure changelog topic params
storeBuilder.withLoggingEnabled(Map.of(
    "cleanup.policy", "compact",
    "retention.ms", "604800000"  // 7 days
));
```

### Repartitionnement pour un état correct {#repartitioning-for-correct-state}

```java
// Problem: records with same logical key in different partitions
// Solution: repartition before stateful operations

// Option 1: selectKey (auto-repartitions downstream)
stream.selectKey((key, value) -> value.getCustomerId());

// Option 2: explicit repartition
stream.repartition(Repartitioned.with(Serdes.String(), valueSerde));
```

Le repartitionnement crée un **topic interne intermédiaire** et découpe la topologie en sous-topologies.

## Pièges {#gotchas}

- **L'état est LOCAL à chaque tâche** : si des enregistrements de la même clé arrivent dans des partitions différentes (absence de clé ou mauvais partitionnement), les opérations avec état produisent des résultats incorrects, car des tâches différentes maintiennent des états séparés
- **Repartitionnement = topic interne = latence supplémentaire** : chaque repartitionnement ajoute un saut de lecture-écriture via Kafka ; limitez les changements de clé dans la topologie
- **Pression mémoire de RocksDB** : la configuration RocksDB par défaut peut consommer beaucoup de mémoire hors tas ; ajustez `rocksdb.config.setter` dans les environnements contraints
- **La reconstruction depuis le changelog au premier démarrage est lente** : pour les gros state stores, l'amorçage initial depuis le changelog peut prendre des minutes, voire des heures ; utilisez des réplicas standby (`num.standby.replicas`) pour un basculement plus rapide
- **Les noms des state stores doivent être uniques** dans toute la topologie

## Voir aussi {#see-also}

- [[kafka-streams]] - opérations de base KStream/KTable, notions de topologie
- [[kafka-streams-windowing]] - state stores fenêtrés pour les agrégations temporelles
- [[topics-and-partitions]] - impact de l'affectation des partitions sur la localité des state stores
- [Documentation Kafka Streams sur les state stores](https://kafka.apache.org/documentation/streams/developer-guide/processor-api.html#state-stores)
