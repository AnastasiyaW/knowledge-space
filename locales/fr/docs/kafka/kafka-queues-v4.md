---
title: "Kafka Queues (v4.0)"
category: concepts
tags: [kafka, queues, kafka-4, work-queue, virtual-partitions]
level: 2
source_sha256: 3f8a61706dbc8c5ca005f4ac245d5b0f3dfc01042d160c9a76d7c0de2f801eed
translation: machine
translated_at: '2026-10-24'
---
# Kafka Queues (v4.0) {#kafka-queues-v40}

Kafka 4.0 introduit une sémantique de file de travail dans laquelle chaque message n'est traité que par un seul consommateur du groupe, avec une mise à l'échelle automatique et sans rééquilibrage, en utilisant en interne des partitions virtuelles.

## Points clés {#key-facts}

- Activé via `queue.topic.enable=true` sur le topic
- Chaque message n'est traité que par UN seul consommateur du groupe (patron de consommateurs concurrents)
- Mise à l'échelle automatique sans rééquilibrage (contrairement aux groupes de consommateurs traditionnels)
- Partitionnement masqué pour le client : des partitions virtuelles sont utilisées en interne pour la distribution
- Comble l'écart entre le modèle de journal de Kafka et le comportement traditionnel des files de messages
- Fait partie de la version 4.0 de Kafka, aux côtés du mode KRaft seul (ZooKeeper entièrement supprimé) et de Tiered Storage

## Modèles {#patterns}

### Récapitulatif des fonctionnalités de Kafka 4.0 {#kafka-40-feature-summary}

| Fonctionnalité | Statut |
|----------------|--------|
| KRaft (ZooKeeper supprimé) | Valeur par défaut en production |
| Kafka Queues | Nouveauté de la 4.0 |
| Tiered Storage | Disponibilité générale (GA) en 4.0 |

### Tiered Storage {#tiered-storage}

```properties
# Enable tiered storage
remote.log.enabled=true
# Recent data on local disk, older segments on remote tier (S3, HDFS)
# Extended retention without overwhelming local storage
```

## Pièges {#gotchas}

- **Kafka Queues est nouveau dans la v4.0** : le support de l'écosystème peut être limité au départ
- **Ce n'est pas un remplacement de RabbitMQ** : Kafka Queues ajoute une sémantique de file, mais l'architecture de Kafka reste basée sur le journal
- **Les partitions virtuelles sont internes** : vous ne les configurez pas et ne les voyez pas ; la distribution est automatique

## Voir aussi {#see-also}

- [[messaging-models]] - modèles file d'attente, publication/abonnement et basé sur le journal
- [[consumer-groups]] - sémantique traditionnelle des groupes de consommateurs Kafka
- [[broker-architecture]] - mode KRaft, changements de Kafka 4.0
- [KIP-932 : Queues for Kafka](https://cwiki.apache.org/confluence/display/KAFKA/KIP-932)
