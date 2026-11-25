---
title: "Modèles de courtiers de messages"
category: concepts
tags: [messaging, pub-sub, queue, delivery-guarantees, message-broker]
level: 3
source_sha256: 446263f6471370ec370ef9d5362c29893118f99e0ecdf7995ce8c4db9ef6c40e
translation: machine
translated_at: '2026-10-24'
---
# Modèles de courtiers de messages {#message-broker-patterns}

Les courtiers de messages découplent les services (les dépendances se réduisent au seul format des messages) et permettent un traitement asynchrone (le producteur envoie et passe à autre chose, le consommateur traite à son propre rythme).

## Deux modèles fondamentaux {#two-fundamental-patterns}

### Publication-abonnement (Pub-Sub) {#publish-subscribe-pub-sub}
Le producteur publie sur un topic. **Tous les abonnés** reçoivent une copie. Les messages sont diffusés.

- Adapté pour : les notifications d'événements (« commande créée » consommée simultanément par l'expédition, l'analytique et les notifications)
- Problème : chaque consommateur reçoit chaque message, sans répartition de charge intégrée

### File d'attente (Point-à-point) {#message-queue-point-to-point}
Le producteur envoie vers une file. **Un seul consommateur** reçoit chaque message. Une fois consommé, il disparaît pour les autres.

- Adapté pour : la répartition de travail via des **consommateurs concurrents** (competing consumers) : 10 consommateurs sur une même file = un débit 10 fois supérieur
- Avantage clé : traitement unique garanti

### Choisir entre les deux {#choosing-between-them}

| Question | Pub-Sub | Queue |
|----------|---------|-------|
| Combien de consommateurs par message ? | Plusieurs | Un seul |
| Tous les consommateurs doivent-ils voir chaque message ? | Oui | Non |
| Besoin d'un traitement unique garanti ? | Non | Oui |
| Besoin de répartition de travail / d'équilibrage de charge ? | Non | Oui |

**Tendance :** les modèles pub-sub et à journal (Kafka) gagnent du terrain. De nombreux courtiers supportent les deux modèles.

## Push vs Pull {#push-vs-pull}

| Modèle | Courtier | Contrôle côté consommateur | Latence | Exemple |
|--------|----------|----------------------------|---------|---------|
| **Push** | Envoie immédiatement | Doit gérer le débit entrant | Faible | RabbitMQ par défaut |
| **Pull** | Attend une requête | Contrôle le rythme et la position | Variable | Kafka |

Le push peut surcharger les consommateurs lents (utiliser un prefetch count). Le pull ajoute un délai si l'interrogation est peu fréquente.

## Garanties de livraison {#delivery-guarantees}

| Niveau | Comportement | Compromis |
|--------|--------------|-----------|
| **At most once** | Envoi sans accusé (fire and forget) | Le plus rapide, des messages peuvent être perdus |
| **At least once** | Livré 1 fois ou plus, des doublons sont possibles | Le plus courant, le consommateur doit être idempotent |
| **Exactly once** | Livré exactement une fois | Le plus coûteux, souvent équivalent à at-least-once + consommateur idempotent |

## Architecture du courtier {#broker-architecture}

### Fédération {#federation}
Plusieurs courtiers indépendants connectés entre eux. Distribution géographique, couplage faible, domaines de panne isolés.

### Clustering {#clustering}
Courtiers fortement couplés partageant un état. Haute disponibilité, bascule automatique. Réseau plus complexe.

## Choisir un courtier {#choosing-a-broker}

| Critère | Kafka | RabbitMQ |
|---------|-------|----------|
| Volume de données | Élevé (100K+ msg/s) | Modéré |
| Rétention | Conservés après consommation | Supprimés après consommation |
| Ordonnancement | Par partition | Par file (FIFO) |
| Modèle de consommation | Pull | Push |
| Routage | Simple (topic/partition) | Flexible (exchanges) |
| Rejeu | Oui (à n'importe quel offset) | Non |
| Cas d'usage | Streaming d'événements, big data | Files de tâches, requête-réponse |

**Grille de décision :**
1. Volume élevé -> Kafka
2. Livraison fiable de petits volumes -> RabbitMQ
3. Besoin d'un routage flexible (exchanges, topics, headers) -> RabbitMQ
4. Besoin de rejouer un journal / event sourcing -> Kafka
5. Ordre global strict -> une seule partition Kafka

## Pièges courants {#gotchas}

- **Consommateurs concurrents avec pub-sub** : 3 consommateurs traitant chacun chaque message = 3 fois plus de doublons. Utiliser des groupes de consommateurs (Kafka) ou le modèle à file
- **At-least-once sans idempotence** : le consommateur traite le message, l'accusé est perdu à cause du réseau, le message est redélivré et traité à nouveau
- **Courtier utilisé comme base de données** : les courtiers servent à transmettre des messages, pas au stockage à long terme (sauf Kafka avec des politiques de rétention)
- **Ordre des messages** : garanti seulement au sein d'une même partition (Kafka) ou d'une même file (RabbitMQ), pas entre elles

## Voir aussi {#see-also}

- [[kafka-architecture]] - Étude approfondie de Kafka
- [[rabbitmq-architecture]] - Étude approfondie de RabbitMQ
- [[microservices-communication]] - Place des courtiers dans l'architecture de services
- [[data-serialization-formats]] - JSON, Avro, Protobuf pour les charges utiles des messages
- [[queueing-theory]] - Pourquoi les systèmes se dégradent sous charge
