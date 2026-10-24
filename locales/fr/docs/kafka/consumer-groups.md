---
title: "Groupes de consommateurs"
category: concepts
tags: [kafka, consumer, group, rebalancing, heartbeat, partition-assignment, static-membership]
level: 4
source_sha256: a8b274145e723ce1bf8ce34e4c90f32fce90e9979643464bea0ca8f01b0c80e8
translation: machine
translated_at: '2026-10-24'
---
# Groupes de consommateurs {#consumer-groups}

Un groupe de consommateurs est une entité nommée qui permet à plusieurs consommateurs de lire de manière coopérative les partitions d'un topic, chaque partition étant assignée à exactement un consommateur du groupe, ce qui apporte à la fois le parallélisme et la tolérance aux pannes.

## Faits clés {#key-facts}

- Les consommateurs rejoignent un groupe via le paramètre `group.id`, qui doit être unique pour chaque groupe de consommateurs logique
- Au sein d'un groupe, **une partition ne peut être lue que par un seul consommateur** (mais un consommateur peut lire plusieurs partitions)
- Si le nombre de consommateurs dépasse le nombre de partitions, les consommateurs excédentaires restent inactifs (aucun travail à effectuer)
- Plusieurs groupes de consommateurs PEUVENT lire la même partition de manière indépendante (chaque groupe suit ses propres [[offsets-and-commits]])
- C'est une fonctionnalité majeure : lire un topic 10 fois nécessite 10 groupes de consommateurs (10 x 8 octets par partition), et non 10 copies des données
- Un consommateur peut s'abonner à plusieurs topics via `consumer.subscribe(List<String>)`
- Il n'existe pas de plafond strict sur le nombre de groupes de consommateurs (théoriquement environ 2 milliards) ; le topic `__consumer_offsets` (50 partitions par défaut) commence à ralentir à partir de quelques milliers de groupes
- Le premier consommateur à se connecter devient le **leader du groupe** : il effectue la redistribution des partitions lors d'un rééquilibrage
- Délai d'expiration du groupe de consommateurs : si un consommateur reste inactif trop longtemps, Kafka peut supprimer ses offsets (`offsets.retention.minutes`, 7 jours par défaut)
- Kafka fonctionne en **mode pull** : les consommateurs interrogent Kafka ; Kafka ne pousse pas les messages (contrairement à RabbitMQ)

## Modèles d'utilisation {#patterns}

### Consommateur de base (Java) {#basic-consumer-java}

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false");
props.put("auto.offset.reset", "earliest");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("topic1", "topic2"));

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        consumer.commitSync();
    }
} finally {
    consumer.close();  // ALWAYS close consumer
}
```

### Consommateur de base (Python) {#basic-consumer-python}

```python
from confluent_kafka import Consumer

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
consumer = Consumer(conf)
consumer.subscribe(["topic1", "topic2"])

try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        process_message(msg)
        consumer.commit(msg)
finally:
    consumer.close()
```

### Stratégies d'assignation des partitions {#partition-assignment-strategies}

| Stratégie | Cas d'usage | Comportement |
|----------|----------|----------|
| **RangeAssignor** (par défaut) | Topics co-partitionnés | Assigne des partitions contiguës par topic ; peut être déséquilibré |
| **RoundRobinAssignor** | Répartition équitable | Répartit toutes les partitions de manière uniforme, en alternance |
| **StickyAssignor** | Consommateurs avec état | Préserve les assignations existantes lors d'un rééquilibrage |
| **CooperativeStickyAssignor** | Valeur par défaut moderne (recommandée) | Rééquilibrage incrémental, sans arrêt global (stop-the-world) |

```java
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

**Topics co-partitionnés** : deux topics ayant le même nombre de partitions, la même stratégie de partitionnement et les mêmes clés. Avec RangeAssignor, les données ayant la même clé provenant des deux topics sont envoyées au même consommateur, ce qui permet de réaliser des jointures sans communication inter-processus.

### Référence de configuration du consommateur {#consumer-configuration-reference}

| Paramètre | Valeur par défaut | Description |
|-----------|---------|-------------|
| `bootstrap.servers` | obligatoire | Adresses des brokers (séparées par des virgules) |
| `group.id` | obligatoire | Identifiant du groupe de consommateurs |
| `key.deserializer` | obligatoire | Classe de désérialisation des clés |
| `value.deserializer` | obligatoire | Classe de désérialisation des valeurs |
| `enable.auto.commit` | `true` | Validation automatique des offsets (à désactiver en production) |
| `auto.commit.interval.ms` | `5000` | Fréquence de la validation automatique |
| `auto.offset.reset` | `latest` | Comportement en l'absence d'offset enregistré |
| `max.partition.fetch.bytes` | `1048576` (1 Mo) | Volume maximal de données par partition et par poll |
| `max.poll.records` | `500` | Nombre maximal de messages par poll, toutes partitions confondues |
| `fetch.min.bytes` | `1` | Volume minimal de données avant le retour de poll |
| `fetch.max.wait.ms` | `500` | Temps d'attente maximal si `min.bytes` n'est pas atteint |
| `heartbeat.interval.ms` | `3000` | Fréquence des heartbeats |
| `session.timeout.ms` | `10000` | Délai de session avant que le consommateur ne soit considéré comme mort |
| `max.poll.interval.ms` | `300000` | Délai maximal entre deux polls |

### Appartenance statique au groupe {#static-group-membership}

```java
props.put("group.instance.id", "consumer-instance-1");
// No rebalance on temporary disconnect
// Risk: partition unread until restart
```

## Pièges {#gotchas}

- **Tempête de rééquilibrage** : les consommateurs arrêtent et redémarrent la lecture de façon répétée. Causes : traitement plus long que `session.timeout.ms`, démarrage lent, déploiements fréquents. Solution : augmenter les délais d'expiration, utiliser CooperativeStickyAssignor
- **Tous les consommateurs doivent utiliser la même stratégie d'assignation** : des stratégies différentes entraînent un rééquilibrage global
- **Les consommateurs suspendus ne déclenchent PAS de rééquilibrage** : `.pause()` maintient les heartbeats actifs
- **L'abonnement d'un consommateur est propre à chaque appel de subscribe** : un nouvel appel à `subscribe()` remplace l'abonnement précédent
- **Les consommateurs excédentaires restent inactifs** : avoir plus de consommateurs que de partitions représente des ressources gaspillées ; anticipez le nombre de partitions (règle empirique : 4 partitions par consommateur)

## Voir aussi {#see-also}

- [[offsets-and-commits]] - suivi des offsets, dangers de la validation automatique, modèles de validation manuelle
- [[rebalancing-deep-dive]] - réglage des heartbeats, rééquilibrage coopératif, appartenance statique
- [[topics-and-partitions]] - dimensionnement du nombre de partitions et routage par clé
- [[consumer-configuration]] - référence complète de la configuration du consommateur
- [Configuration des consommateurs Apache Kafka](https://kafka.apache.org/documentation/#consumerconfigs)
