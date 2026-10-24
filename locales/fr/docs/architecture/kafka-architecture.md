---
title: "Architecture d'Apache Kafka"
category: reference
tags: [kafka, event-streaming, message-broker, partitions, consumer-groups]
level: 4
source_sha256: b06a0a25e176be191e9784684f25a17014ebe87a05bad9de34f8fc5afbf9e843
translation: machine
translated_at: '2026-10-24'
---
# Architecture d'Apache Kafka {#apache-kafka-architecture}

Kafka est un broker de messages construit sur le modèle de journal (log). L'accent est mis sur la préservation de l'ordre des messages, le stockage à long terme et un haut débit. Modèle pull : les consumers contrôlent le rythme de lecture.

## Hiérarchie de l'architecture {#architecture-hierarchy}

```php
Cluster -> Brokers -> Topics -> Partitions -> Messages (with offsets)
```

- **Topic** - regroupement logique de partitions. Un type de message par topic (par ex. `page_visit`, `user_registration`, `order_placed`)
- **Partition** - log physique à ordre strict. Appartient toujours à un seul topic
- **Offset** - pointeur indiquant où le consumer s'est arrêté de lire. Stocké dans le topic système `__consumer_offsets`
- **Consumer Group** - consumers partageant un même offset. Au sein d'un groupe, chaque partition est lue par exactement un consumer
- **Broker** - instance serveur de Kafka. Plusieurs brokers forment un cluster

## Flux des messages {#message-flow}

1. Le producer envoie vers un **topic** (et non directement vers une partition). Kafka sélectionne la partition (round-robin, basée sur la clé, ou spécifiée par le producer)
2. Kafka écrit le message avec son offset dans la partition
3. Les **consumers individuels** peuvent lire chaque message, un nombre quelconque de fois (pub-sub)
4. **Consumer groups** - un consumer par partition. 3 partitions + 2 consumers = le consumer 1 lit les partitions 1 et 2, le consumer 2 lit la partition 3. Les consumers supplémentaires restent inactifs si le nombre de consumers dépasse le nombre de partitions

## Réplication et haute disponibilité {#replication-and-ha}

- **Leader-Follower** par partition. Le leader gère toutes les lectures et écritures
- Les followers répliquent les données. En cas de panne du leader, un follower est promu
- **Facteur de réplication** généralement égal à 3
- **ZooKeeper** gère la coordination (remplacé progressivement par **KRaft** dans les versions récentes)

## Garanties de livraison (acks) {#delivery-guarantees-acks}

| Paramètre | Garantie | Vitesse | Comportement |
|-----------|----------|---------|--------------|
| `acks=0` | Au plus une fois | La plus rapide | Aucun accusé de réception |
| `acks=1` | Au moins une fois | Moyenne | Le leader confirme |
| `acks=all` | La plus forte | La plus lente | Le leader et tous les réplicas confirment |

**`min.insync.replicas`** avec `acks=all` : autorise les écritures tant que N-1 réplicas sont indisponibles.

## Garanties côté consumer {#consumer-guarantees}

Responsabilité du consumer (modèle pull) :
- Commit de l'offset **après** le traitement = au moins une fois
- Commit de l'offset **avant** le traitement = au plus une fois
- **Exactly-once** = transactions Kafka ou consumers idempotents

## Persistance des données {#data-persistence}

- Les messages sont toujours écrits sur disque
- **Rétention par durée** (par ex. 7 jours) ou **par taille** (par ex. 1 Go par partition)
- **Log compaction** - conserve la dernière valeur pour chaque clé
- Contrairement à RabbitMQ, les messages sont conservés après consommation

## Quand utiliser Kafka {#when-to-use-kafka}

- Streaming d'événements à fort volume (plus de 100 000 msg/s)
- Systèmes nécessitant le rejeu de messages
- Agrégation de logs provenant de plusieurs services
- Pipelines d'analyse temps réel et de métriques
- Architectures event sourcing
- Pipeline de données entre les systèmes sources et le DWH

## Quand ne pas l'utiliser {#when-not-to-use}

- Files de tâches simples (utiliser RabbitMQ)
- Patterns requête-réponse
- RPC à faible latence
- Systèmes à faible volume de messages

## Pièges courants {#gotchas}

- **Plus de consumers que de partitions** = consumers inactifs gaspillant des ressources
- **Une seule partition pour garantir l'ordre** limite le débit : utiliser un partitionnement par clé pour concilier ordre et parallélisme
- **Consumer lag** - surveiller le retard d'offset pour détecter les consumers lents avant qu'ils ne accumulent un retard trop important
- **Nombre de partitions** - peut être augmenté mais jamais diminué. À choisir avec soin à la création du topic
- **Tempêtes de rebalancing** - l'ajout ou le retrait de consumers déclenche un rebalancing, qui interrompt brièvement toute la consommation du groupe

## Voir aussi {#see-also}

- [[rabbitmq-architecture]] - Alternative basée sur les files
- [[message-broker-patterns]] - Choisir entre les brokers
- [[microservices-communication]] - Architecture orientée événements
- [[bigdata-ml-architecture]] - Kafka dans les pipelines de données
