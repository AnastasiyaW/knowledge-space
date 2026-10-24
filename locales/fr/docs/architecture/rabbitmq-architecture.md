---
title: "Architecture de RabbitMQ"
category: reference
tags: [rabbitmq, message-queue, exchange, routing, amqp]
level: 4
source_sha256: 0c7fb5d9c02d345f88fb3511ee8c4818c53c7c4298d0ff12b63526ddf6a49ee9
translation: machine
translated_at: '2026-10-24'
---
# Architecture de RabbitMQ {#rabbitmq-architecture}

RabbitMQ est un broker de messages reposant sur le modèle de files d'attente. Motif « broker intelligent, consommateur simple » : la logique de distribution se situe côté broker. Modèle par push par défaut.

## Flux de messages {#message-flow}

```php
Producer -> Exchange -> [Binding + Routing Key] -> Queue -> Consumer
```

**Les producteurs n'écrivent jamais directement dans les files.** Le exchange reçoit tous les messages et les route.

## Types d'exchange {#exchange-types}

| Type | Logique de routage | Vitesse | Cas d'usage |
|------|--------------------|---------|-------------|
| **Fanout** | Diffusion vers TOUTES les files liées | La plus rapide | File unique, diffusion |
| **Direct** | Correspondance exacte de la Routing Key | Rapide | Routage simple (le plus courant) |
| **Topic** | Routing Key avec jokers (`*`=un mot, `#`=n'importe quoi) | Plus lente | Logique métier complexe |
| **Headers** | Correspondance sur les en-têtes (`x-match=all` ou `any`) | La plus lente | Plusieurs critères de correspondance |

**Guide de sélection :**
1. Plus d'une file ? Non -> Fanout
2. Besoin de plus de 1000 msg/s ? Oui -> Direct ou Fanout uniquement
3. Le message doit aller dans exactement une file ? Oui -> Direct

**Exemples de Topic :** `asia.china.done` correspond à `#.done`, `asia.*.done`, `asia.china.*`

## Types de files {#queue-types}

| Type | Comportement | Cas d'usage |
|------|--------------|-------------|
| **Classic** | FIFO standard, un consommateur par message | Le plus courant |
| **Quorum** | Réplication distribuée pour la tolérance aux pannes | Fiabilité en production |
| **Stream** | Semblable à Kafka, conserve les données, plusieurs consommateurs | Volume élevé, rejeu |

## Structure des messages {#message-structure}

| Champ | Rôle |
|-------|------|
| `Payload` | Corps du message (vos données) |
| `Routing Key` | Détermine le routage via le binding |
| `delivery_mode` | 1 = mémoire uniquement, 2 = persistance sur disque |
| `mandatory` | Renvoie le message au producteur si aucun binding ne correspond |
| `expiration` | TTL du message |
| `confirm` | Demande une confirmation de livraison |

## Persistance {#persistence}

Les messages sont perdus en cas de crash, sauf si :
1. Le drapeau `durable` de la file est activé **ET**
2. Le producteur envoie avec `delivery_mode = 2`

Les deux conditions sont requises. Si l'une manque, le stockage reste en mémoire uniquement.

## Garanties de livraison {#delivery-guarantees}

### Côté consommateur (Ack/Nack) {#consumer-side-acknack}
- **Ack** : traitement réussi, le message est retiré de la file
- **Nack** : échec du traitement, le message retourne dans la file (également en cas de coupure de connexion)
- **AutoAck** : le broker acquitte automatiquement à l'envoi (au plus une fois, le plus rapide)

**Le prefetch count** contrôle le nombre de messages non acquittés par consommateur. `prefetch_count=1` = traitement strictement un par un.

### Côté producteur {#producer-side}
Même mécanisme Ack/Nack. Le paramètre `confirm` active le suivi complet de la livraison. `mandatory` renvoie les messages non routables.

### Risque de doublon {#duplicate-risk}
Le consommateur traite le message, mais l'ack n'atteint pas le broker (réseau). Le message est redélivré. Des consommateurs idempotents sont nécessaires pour une sémantique exactly-once.

## Dead Letter Exchange (DLE) {#dead-letter-exchange-dle}

Les messages en échec sont routés vers le DLE au lieu d'être perdus. Combinez-le avec une relance automatique après un délai et une journalisation des erreurs.

## Haute disponibilité {#high-availability}

- Plusieurs instances derrière un répartiteur de charge
- Quorum Queues pour la tolérance aux pannes
- Configuration en cluster pour la production

## Exemple de conception {#design-example}

```php
task_queue (Direct)           -> task processing
status_update_queue (Topic)   -> status tracking (*.completed, *.failed)
notification_queue (Fanout)   -> broadcast notifications
priority_queue (Direct)       -> urgent tasks
audit_queue (Direct)          -> compliance logging

Each queue has: Dead Letter Exchange, Quorum Queue, automatic retry
```

## Pièges à éviter {#gotchas}

- **Pas de persistance sur disque par défaut** : les messages sont perdus en cas de crash sans `durable` + `delivery_mode=2` explicites
- **Fanout ignore la routing key** : les paramètres de binding n'ont aucun effet, toutes les files liées reçoivent tout
- **Prefetch=0** signifie illimité : le broker envoie tous les messages immédiatement, ce qui peut saturer le consommateur
- **Les noms de files** sont uniques globalement au sein d'un vhost : des collisions sont possibles dans les environnements multi-équipes
- **Pas adapté aux flux de données massifs** : utilisez Kafka pour le streaming d'événements à fort volume

## Voir aussi {#see-also}

- [[kafka-architecture]] : alternative basée sur les logs pour le streaming à fort volume
- [[message-broker-patterns]] : choisir entre brokers, garanties de livraison
- [[microservices-communication]] : motifs de communication entre services
