---
title: "Apache Kafka - Sémantiques de livraison et patterns de consommateurs"
category: concepts
tags: [kafka, messaging, event-driven, consumer-groups, streaming]
level: 2
source_sha256: b7250aa01443d2fe2998a03fb8a0c9d2f301ea5da2650589cfaebfd0e5eaf8a5
translation: machine
translated_at: '2026-10-24'
---
# Apache Kafka - Sémantiques de livraison et patterns de consommateurs {#apache-kafka-delivery-semantics-and-consumer-patterns}

Garanties de livraison de Kafka, mécanique des groupes de consommateurs, stratégies de rééquilibrage et patterns d'intégration. Axé sur l'usage pratique en production plutôt que sur l'administration du cluster.

## Points clés {#key-facts}

- Trois sémantiques de livraison : at-most-once, at-least-once (par défaut et recommandée), exactly-once
- At-least-once impose des consommateurs idempotents : un même message traité deux fois produit le même résultat
- Le mode KRaft (Kafka 2.8+) supprime la dépendance à ZooKeeper
- Le producteur envoie vers une partition de topic : en round-robin par défaut, ou par hachage de clé pour garantir l'ordre
- Le groupe de consommateurs répartit les partitions entre ses membres ; rééquilibrage à chaque arrivée ou départ
- Cooperative Sticky est la stratégie de rééquilibrage privilégiée depuis Kafka 2.4

## Patterns {#patterns}

### Sémantiques de livraison {#delivery-semantics}

**At most once** - acquitter l'offset avant le traitement :
- Rapide, peut perdre des messages en cas de crash
- À utiliser lorsque la perte de messages est acceptable (métriques, événements non critiques)

**At least once** - traiter puis acquitter :
- Par défaut pour la plupart des cas d'usage
- Impose des consommateurs idempotents
- Utiliser des contraintes d'unicité en base de données ou des tables de déduplication

**Exactly once** - nécessite les transactions Kafka et un producteur idempotent :
- L'API Kafka Streams facilite sa mise en œuvre
- Très complexe pour les scénarios consommateur-vers-base de données
- Souvent plus simple d'implémenter at-least-once avec des clés d'idempotence

### Rééquilibrage des groupes de consommateurs {#consumer-group-rebalancing}

| Stratégie | Comportement |
|-----------|--------------|
| RoundRobin | Répartit uniformément l'ensemble des partitions |
| Sticky | Minimise les déplacements de partitions lors du rééquilibrage |
| Cooperative Sticky | Rééquilibrage incrémental ; les consommateurs conservent leurs partitions jusqu'à confirmation de la nouvelle affectation |

Cooperative Sticky réduit les interruptions lors des redémarrages progressifs : les consommateurs ne cessent pas de traiter pendant qu'un rééquilibrage est en cours.

### Transactional Outbox {#transactional-outbox}

Problème : mettre à jour la base de données et publier un message Kafka de manière atomique.

1. Dans la même transaction de base de données : mettre à jour l'entité et insérer l'événement dans la table `outbox`
2. Un poller en arrière-plan lit les événements outbox non envoyés, les publie sur Kafka et les marque comme envoyés
3. Le consommateur déduplique à l'aide de clés d'idempotence

Cette approche évite entièrement le problème du commit en deux phases.

### Concepts clés {#key-concepts}

- **Partition** : unité de parallélisme et d'ordonnancement. Les messages au sein d'une partition sont ordonnés.
- **Offset** : position dans la partition. L'offset commité signifie « j'ai traité jusqu'ici ».
- **Groupe de consommateurs** : ensemble de consommateurs partageant les partitions d'un topic. Chaque partition est affectée à exactement un consommateur du groupe.
- **Routage par clé** : les messages ayant la même clé vont toujours dans la même partition, garantissant l'ordre par clé.

## Pièges {#gotchas}

- Le nombre de consommateurs d'un groupe ne peut pas dépasser le nombre de partitions : les consommateurs en surplus restent inactifs
- L'exactly-once est pratiquement impossible entre Kafka et un système externe sans idempotence côté consommateur
- Le consumer lag (retard de l'offset par rapport au dernier) est la principale métrique de santé des groupes de consommateurs
- Le mode KRaft simplifie le déploiement mais nécessite 1 à 3 nœuds contrôleurs pour la gestion des métadonnées
- Des temps de traitement longs sans commit des offsets peuvent déclencher un expiration de session et un rééquilibrage

## Voir aussi {#see-also}

- [[database-patterns]] - implémentation de la transactional outbox en Go
- [[microservices]] - Kafka dans une architecture microservices
- [[observability-query-languages]] - surveillance du consumer lag avec PromQL
