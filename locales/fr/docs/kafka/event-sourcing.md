---
title: "Event Sourcing"
category: patterns
tags: [kafka, event-sourcing, immutable-log, replay, audit, state-reconstruction]
level: 3
source_sha256: 351b3cdce2c65ab28fce9ebda1a0602a963b8f3904e8eddd9feb94a308d0dca2
translation: machine
translated_at: '2026-10-24'
---
# Event Sourcing {#event-sourcing}

L'event sourcing consiste à stocker chaque changement d'état sous forme d'événement immuable dans Kafka, plutôt que d'écraser l'état courant dans une base de données. Cela permet de rejouer l'historique complet, de disposer de pistes d'audit et de reconstruire l'état à n'importe quel moment.

## Points clés {#key-facts}

- Le journal immuable en ajout seul (append-only) de Kafka est un choix naturel pour l'event sourcing
- Tous les événements sont enregistrés comme des faits immuables ; l'état est dérivé en rejouant les événements
- L'état courant est reconstruit en rejouant les événements à partir de n'importe quel offset
- La rétention du log Kafka garantit un historique complet des événements pour les audits et la conformité
- Plusieurs [[consumer-groups]] peuvent lire le même flux d'événements de manière indépendante afin de construire différentes vues matérialisées
- Répond à la question « comment en sommes-nous arrivés à cet état ? » : avec seulement l'état courant en base, il est impossible de retracer l'historique
- Écrire tous les événements dans un SGBDR traditionnel se heurte à un goulot d'étranglement vers ~10K écritures/s ; Kafka en gère plusieurs millions
- Utiliser des magasins de lecture spécialisés (ElasticSearch, Redis, Cassandra) pour les vues matérialisées
- Pour un stockage d'événements indéfini, un Event Store dédié (EventStoreDB, MongoDB) est plus approprié que Kafka, qui supprime les données par défaut

## Patterns {#patterns}

### Architecture de l'event sourcing {#event-sourcing-architecture}

```bash
Events -> Kafka Topic (append-only log, source of truth)
    -> Materializer A -> Read Store A (current state for API)
    -> Materializer B -> Read Store B (analytics, full-text search)
    -> Materializer C -> Read Store C (notifications, ML fraud detection)
    -> Technical Support -> Full event history for debugging
```

### Rejeu des événements {#event-replay}

```sql
POST /api/replay-events
1. Command API reads all events from Event Store
2. Sends marker event "replay started"
3. Query API clears its read model
4. Query API re-applies all events to rebuild from scratch
```

Cas d'usage : migration de schéma, correction de bug dans les gestionnaires d'événements, ajout de nouvelles projections, reprise après sinistre. Pendant le rejeu, les commandes entrantes sont bloquées jusqu'à la fin du traitement.

### Kafka comme système d'acteurs {#kafka-as-actor-system}

Chaque consommateur traitant une partition agit comme un acteur :
- Il reçoit les messages séquentiellement
- Il maintient un état
- Il peut produire des messages vers d'autres topics
- Les partitions garantissent naturellement un traitement séquentiel

## Pièges à éviter {#gotchas}

- **Kafka supprime les événements par défaut** - pour un stockage réellement illimité, utiliser un Event Store dédié en complément de Kafka ou configurer une rétention infinie
- **L'évolution du schéma des événements est critique** - ajouter ou supprimer des champs dans les événements casse le rejeu ; utiliser un [[schema-registry]] avec une compatibilité FULL
- **Le rejeu peut être coûteux** - rejouer des millions d'événements prend du temps ; envisager des snapshots : sauvegarder périodiquement l'état courant et ne rejouer que depuis le dernier snapshot
- **L'ordre n'est garanti qu'au sein d'une partition** - les événements liés doivent partager une même clé de partitionnement ; l'ordre entre partitions nécessite une coordination supplémentaire

## Voir aussi {#see-also}

- [[cqrs-pattern]] - Command Query Responsibility Segregation, compagnon naturel de l'event sourcing
- [[kafka-streams]] - traitement de flux pour construire des vues matérialisées
- [[topics-and-partitions]] - compaction de log pour les tables « dernier état par clé »
- [[delivery-semantics]] - exactly-once pour le traitement des événements
