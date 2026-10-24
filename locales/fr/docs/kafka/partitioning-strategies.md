---
title: "Stratégies de partitionnement"
category: concepts
tags: [kafka, partition, key, hash, ordering, scaling, murmur2]
level: 4
source_sha256: de27dd314fbfa46890b3fa5a6d6c3b2bc98666f313b55f6b23d2a0d5ea1eae03
translation: machine
translated_at: '2026-10-24'
---
# Stratégies de partitionnement {#partitioning-strategies}

Le partitionnement dans Kafka détermine la répartition des messages entre les partitions, à l'aide du hachage de la clé (murmur2), d'un round-robin pour les messages sans clé, ou de partitionneurs personnalisés. L'ordre strict n'est garanti qu'au sein d'une même partition.

## Points clés {#key-facts}

- Kafka utilise un **modulo sur le hachage murmur2 de la clé** pour déterminer le numéro de partition (et NON un hachage cohérent)
- Même clé = même partition = ordre préservé au sein de cette partition
- Sans clé, les messages sont répartis aléatoirement entre les partitions via UniformStickyPartitioner (favorable au batching)
- **L'ordre n'est garanti QU'au sein d'une même partition** : entre partitions, l'ordre n'est PAS garanti
- Le nombre de partitions peut augmenter mais NE PEUT PAS diminuer (officiellement)
- Lorsque le nombre de partitions change, les résultats du modulo changent, ce qui rompt la correspondance clé-partition
- Règle pratique : **4 partitions par consommateur** ; si le nombre de consommateurs est inconnu, prendre 8 partitions par défaut
- Pour jusqu'à 100 000 messages/s, 8 partitions suffisent
- Ajouter des partitions à chaud provoque des réordonnancements et peut faire planter Kafka ; meilleure approche : utiliser Kafka Streams pour rejouer les données
- Trop de topics/partitions sur un seul broker (>1000) dégrade les performances
- Kafka répartit les partitions entre les brokers de manière autonome, mais PEUT placer TOUTES les partitions d'un topic sur un seul nœud

## Patterns {#patterns}

### Dimensionnement du nombre de partitions {#partition-count-sizing}

| Échelle | Nombre de partitions recommandé |
|---------|----------------------|
| Petite (consommateurs inconnus) | 8 |
| Règle par consommateur | 4 x nombre de consommateurs attendu |
| Haut débit (>100K msg/s) | 12-24+ |
| Consommateur unique | 1 (ordre garanti) |

### Partitionneur personnalisé (Java) {#custom-partitioner-java}

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

### Sélection de partition personnalisée (Python) {#custom-partition-selection-python}

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

### Bonnes pratiques pour la clé de partitionnement {#partition-key-best-practices}

```sql
# Use entity ID as key for ordering guarantees
key = customer_id      # All orders for same customer in same partition
key = camera_id        # All frames from same camera in order
key = user_id          # All impressions for same user co-located

# Avoid high-cardinality keys that create hot partitions
# Bad: key = timestamp (each message unique, no grouping benefit)
# Bad: key = "constant" (all messages to one partition)
```

## Pièges {#gotchas}

- **« La recommandation du livre (partitions = consommateurs) est erronée en pratique »** : on gagne environ 4 à 5 % de performance mais on perd en scalabilité ; ajouter un consommateur exige d'ajouter une partition (opération lourde)
- **Ajouter des partitions casse l'ordre basé sur la clé** : des messages de même clé peuvent atterrir dans une autre partition à cause du changement de modulo ; c'est pourquoi modifier le nombre de partitions en production pose problème
- **Kafka crée automatiquement les topics avec `num.partitions=1`** lorsqu'on écrit dans un topic inexistant : catastrophique pour la scalabilité ; toujours définir `auto.create.topics.enable=false` en production
- **Toutes les partitions d'un topic peuvent se retrouver sur un seul nœud** : invisible pendant les tests, cela explose en production sous charge ; les équipes d'administration doivent suivre l'affectation des partitions
- **Le partitionneur personnalisé reçoit des octets sérialisés** : la méthode `partition()` reçoit `keyBytes` (déjà sérialisé) ; pour accéder à l'objet d'origine, convertir (cast) le paramètre `key`

## Voir aussi {#see-also}

- [[topics-and-partitions]] - opérations sur les topics, structure des segments, rétention
- [[consumer-groups]] - lien entre le nombre de partitions et le parallélisme des consommateurs
- [[kafka-producer-advanced-patterns]] - partitionneur dans le pipeline d'envoi
- [Conception du partitionneur Apache Kafka](https://kafka.apache.org/documentation/#design_loadbalancing)
