---
title: "Partitionierungsstrategien"
category: concepts
tags: [kafka, partition, key, hash, ordering, scaling, murmur2]
level: 4
source_sha256: de27dd314fbfa46890b3fa5a6d6c3b2bc98666f313b55f6b23d2a0d5ea1eae03
translation: machine
translated_at: '2026-10-24'
---
# Partitionierungsstrategien {#partitioning-strategies}

Die Partitionierung in Kafka bestimmt, wie Nachrichten auf Partitionen verteilt werden: über Key-Hashing (murmur2), per Round-Robin für Nachrichten ohne Key oder über benutzerdefinierte Partitioner. Eine strikte Reihenfolge ist nur innerhalb einer einzelnen Partition garantiert.

## Wichtige Fakten {#key-facts}

- Kafka verwendet **Modulo über den murmur2-Key-Hash**, um die Partitionsnummer zu bestimmen (NICHT Consistent Hashing)
- Gleicher Key = gleiche Partition = erhaltene Reihenfolge innerhalb dieser Partition
- Ohne Key werden Nachrichten zufällig über `UniformStickyPartitioner` auf die Partitionen verteilt (batching-freundlich)
- **Reihenfolge ist NUR innerhalb einer einzelnen Partition garantiert** – zwischen Partitionen ist die Reihenfolge NICHT garantiert
- Die Anzahl der Partitionen kann erhöht, aber offiziell NICHT verringert werden
- Ändert sich die Anzahl der Partitionen, ändern sich die Modulo-Ergebnisse, und die Zuordnung von Key zu Partition bricht
- Praxisregel: **4 Partitionen pro Consumer**; bei unbekannter Consumer-Anzahl standardmäßig 8 Partitionen
- Für bis zu 100.000 Nachrichten/s funktionieren 8 Partitionen gut
- Das nachträgliche Hinzufügen von Partitionen zur Laufzeit verursacht Umsortierungen und kann Kafka zum Absturz bringen; besser ist es, Kafka Streams zu verwenden, um die Daten neu zu streamen
- Zu viele Topics/Partitionen auf einem einzelnen Broker (>1000) beeinträchtigen die Leistung
- Kafka verteilt Partitionen selbstständig auf die Broker, KANN aber ALLE Partitionen eines Topics auf einen einzigen Knoten legen

## Muster {#patterns}

### Dimensionierung der Partitionsanzahl {#partition-count-sizing}

| Skalierung | Empfohlene Partitionen |
|-------|----------------------|
| Klein (unbekannte Consumer) | 8 |
| Regel pro Consumer | 4 x erwartete Consumer-Anzahl |
| Hoher Durchsatz (>100K Nachr./s) | 12-24+ |
| Einzelner Consumer | 1 (Reihenfolge garantiert) |

### Benutzerdefinierter Partitioner (Java) {#custom-partitioner-java}

```java
public class RegionPartitioner implements Partitioner {
    private Map<String, Integer> regionToPartition;

    @Override
    public void configure(Map<String, ?> configs) {
        regionToPartition = Map.of("us-east", 0, "us-west", 1, "eu-west", 2);
    }

    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        int numPartitions = cluster.partitionsForTopic(topic).size();
        if (key == null) return ThreadLocalRandom.current().nextInt(numPartitions);

        String region = extractRegion(key.toString());
        Integer fixed = regionToPartition.get(region);
        if (fixed != null && fixed < numPartitions) return fixed;

        return Utils.toPositive(Utils.murmur2(keyBytes)) % numPartitions;
    }

    @Override public void close() {}
}

props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, RegionPartitioner.class.getName());
```

### Benutzerdefinierte Partitionsauswahl (Python) {#custom-partition-selection-python}

```python
# confluent-kafka does not support partitioner class; compute and pass explicitly
import hashlib

def region_partition(key: str, num_partitions: int) -> int:
    region_map = {"us-east": 0, "us-west": 1, "eu-west": 2}
    if ":" in key:
        region = key.split(":")[0]
        p = region_map.get(region)
        if p is not None and p < num_partitions:
            return p
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % num_partitions

p.produce("orders", key=key, value=payload, partition=region_partition(key, num_partitions))
```

### Best Practices für Partitionierungs-Keys {#partition-key-best-practices}

```sql
# Use entity ID as key for ordering guarantees
key = customer_id      # All orders for same customer in same partition
key = camera_id        # All frames from same camera in order
key = user_id          # All impressions for same user co-located

# Avoid high-cardinality keys that create hot partitions
# Bad: key = timestamp (each message unique, no grouping benefit)
# Bad: key = "constant" (all messages to one partition)
```

## Fallstricke {#gotchas}

- **„Die Buchempfehlung (Partitionen = Consumer) ist in der Praxis falsch“** – Man gewinnt etwa 4–5 % Leistung, verliert aber Skalierbarkeit; das Hinzufügen eines Consumers erfordert das Hinzufügen einer Partition (aufwendige Operation)
- **Das Hinzufügen von Partitionen bricht die schlüsselbasierte Reihenfolge** – Nachrichten mit demselben Key können durch die Modulo-Änderung in einer anderen Partition landen; deshalb ist das Ändern der Partitionsanzahl im Produktivbetrieb problematisch
- **Kafka legt Topics automatisch mit `num.partitions=1` an**, wenn in ein nicht existierendes Topic geschrieben wird – schlecht für die Skalierbarkeit; in Produktivumgebungen immer `auto.create.topics.enable=false` setzen
- **Alle Partitionen eines Topics können auf einem einzigen Knoten landen** – im Test unsichtbar, unter Last im Produktivbetrieb problematisch; Admin-Teams sollten die Partitionszuweisungen überwachen
- **Ein benutzerdefinierter Partitioner sieht serialisierte Bytes** – die Methode `partition()` erhält `keyBytes` (bereits serialisiert); um auf das ursprüngliche Objekt zuzugreifen, muss der Parameter `key` gecastet werden

## Siehe auch {#see-also}

- [[topics-and-partitions]] – Topic-Operationen, Segmentstruktur, Retention
- [[consumer-groups]] – Zusammenhang zwischen Partitionsanzahl und Consumer-Parallelität
- [[kafka-producer-advanced-patterns]] – Partitioner in der Sende-Pipeline
- [Apache Kafka: Partitioner-Entwurf](https://kafka.apache.org/documentation/#design_loadbalancing)
