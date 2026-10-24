---
title: "Modèles de messagerie"
category: concepts
tags: [kafka, messaging, queue, pub-sub, log, architecture]
level: 2
source_sha256: 16f2e8e14ebf0526aa0f82736b191bab3ed11b7a10548cac3c89eef56e633f1d
translation: machine
translated_at: '2026-10-24'
---
# Modèles de messagerie {#messaging-models}

Trois modèles fondamentaux de messagerie existent dans les systèmes distribués ; Kafka utilise le modèle basé sur le journal (log), qui englobe à la fois les patterns de file d'attente et de publication-abonnement.

## Faits clés {#key-facts}

- **Modèle file d'attente (consommateurs concurrents)** : les messages sont envoyés dans une file, exactement un consommateur reçoit chaque message ; les messages consommés sont supprimés ; utilisé pour la répartition de tâches et l'équilibrage de charge
- **Modèle publication-abonnement (diffusion)** : les messages sont publiés sur un topic, chaque abonné reçoit une copie ; utilisé pour la notification d'événements lorsque plusieurs systèmes ont besoin des mêmes données
- **Modèle basé sur le journal (Kafka)** : les messages sont ajoutés à un journal immuable et ordonné ; chaque consommateur maintient son propre offset (position) ; les messages sont conservés selon une politique de durée ou de taille, et non en fonction de leur consommation
- Le modèle basé sur le journal permet : plusieurs [[consumer-groups]] indépendants lisant à leur propre rythme, la capacité de rejouer les messages en réinitialisant l'offset, et l'absence de perte de messages en cas de défaillance d'un consommateur
- Les files d'attente traditionnelles (RabbitMQ, ActiveMQ, SQS) se concentrent sur la livraison des messages et la répartition des tâches ; le streaming basé sur le journal (Kafka, Pulsar, Redpanda) se concentre sur le stockage d'événements et le traitement de flux
- Kafka n'est **pas** un courtier de messages : c'est un journal de validation distribué (write-ahead log)
- Différence clé avec les files d'attente traditionnelles : lire un topic 10 fois nécessite 10 groupes de consommateurs (10 x 8 octets de surcharge par partition), et non 10 copies des données

## Patrons {#patterns}

| Propriété | File d'attente traditionnelle | Streaming basé sur le journal |
|-----------|------------------------------|-------------------------------|
| Cycle de vie des messages | Supprimés après consommation | Conservés selon une politique |
| Ordonnancement | Par file (ou aucun) | Garanti par partition |
| Rejeu | Impossible | Possible (réinitialisation de l'offset) |
| Groupes de consommateurs | Consommateurs concurrents | Groupes de consommateurs indépendants |
| Débit | Modéré | Très élevé (E/S séquentielles) |
| Cas d'usage | Répartition de tâches | Event sourcing, analytique, CDC |

### Patrons de communication {#communication-patterns}

| Patron | Notation | Description |
|--------|----------|-------------|
| Put/Take | 1 -> 1 | Un-à-un, consommateur unique |
| Publish/Subscribe | 1 -> * | Un-à-plusieurs, tous les abonnés reçoivent |
| Request/Response | 1 <-> 1 | Synchrone, bidirectionnel |

### Protocoles {#protocols}

AMQP, MQTT, STOMP, NATS, ZeroMQ, le protocole binaire propriétaire de Kafka.

## Pièges à éviter {#gotchas}

- **« Kafka est simplement un courtier de messages de plus »** est faux : l'architecture basée sur le journal de Kafka est fondamentalement différente des courtiers traditionnels basés sur des files d'attente ; Kafka persiste toujours les messages, indépendamment de leur consommation
- **Le modèle file d'attente ne permet pas le rejeu** : une fois un message consommé et acquitté, il disparaît ; il s'agit d'une différence d'architecture fondamentale, et non d'une option de configuration
- **Le publication-abonnement sans rétention** impose que le consommateur soit en ligne au moment de la publication du message ; Kafka résout ce problème en conservant les messages pendant une durée configurable

## Voir aussi {#see-also}

- [[delivery-semantics]] - garanties at-most-once, at-least-once et exactly-once
- [[consumer-groups]] - comment Kafka implémente les patterns file d'attente et publication-abonnement via les groupes de consommateurs
- [[broker-architecture]] - comment Kafka stocke et sert les messages
- [Conception d'Apache Kafka : motivation](https://kafka.apache.org/documentation/#design_motivation)
