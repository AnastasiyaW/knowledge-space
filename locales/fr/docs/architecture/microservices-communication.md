---
title: "Modèles de communication des microservices"
category: patterns
tags: [microservices, api-gateway, bff, cqrs, saga, event-sourcing]
level: 3
source_sha256: 982fe5e58c1aa1049184e877502bb14037faa7cdfe6ff60f0bc6e6f38588d4cf
translation: machine
translated_at: '2026-10-24'
---
# Modèles de communication des microservices {#microservices-communication-patterns}

Comment les microservices communiquent entre eux et avec les clients externes. Le choix entre communication synchrone et asynchrone façonne fondamentalement le comportement du système, le couplage et les modes de défaillance.

## Communication synchrone (basée sur les API) {#synchronous-communication-api-based}

Le service A appelle directement l'API du service B. C'est simple, mais cela crée un couplage fort : si B est lent ou indisponible, A en pâtit.

**Protocoles :** REST, gRPC, GraphQL. Il est aussi possible d'utiliser WebSocket, les webhooks ou HTTP asynchrone.

## Communication asynchrone (basée sur les messages) {#asynchronous-communication-message-based}

Les services communiquent via des brokers de messages (RabbitMQ, Kafka). Le service A envoie un message, et le service B le traite quand il est prêt. Cela permet un couplage faible et un fonctionnement indépendant.

### Styles asynchrones {#async-styles}

| Style | Comportement | Cas d'usage |
|-------|--------------|-------------|
| **Requête/Réponse** | Non bloquant, réponse attendue rapidement | Requêtes inter-services |
| **Notifications** | Envoi sans attente, aucune réponse | Diffusion d'événements |
| **Requête/Réponse asynchrone** | Réponse attendue à un moment ultérieur | Opérations de longue durée |

## Pattern API Gateway {#api-gateway-pattern}

Point d'entrée centralisé pour tous les clients externes. Il masque la structure interne du système.

**Fonctionnalités :**
1. **Routage des requêtes** : dirige vers le microservice approprié
2. **Agrégation de données** : combine les réponses de plusieurs services
3. **Authentification** : authentification/autorisation centralisées
4. **Limitation de débit** : prévient la surcharge
5. **Mise en cache** : réduit la charge sur les backends
6. **Supervision/journalisation** : collecte des statistiques et des journaux de requêtes
7. **Gestion des erreurs** : réponses standardisées, masquage des détails internes

**Inconvénients :** point de défaillance unique (nécessite de la haute disponibilité), goulot d'étranglement de performance (tout le trafic transite par lui), risque de dépendance vis-à-vis d'un fournisseur.

## Backend for Frontend (BFF) {#backend-for-frontend-bff}

Une passerelle distincte par type de client (mobile, web, desktop). Chaque BFF est optimisé pour les besoins, les exigences de données et les caractéristiques de performance de son client spécifique.

**Pourquoi un BFF plutôt qu'une Gateway unique :** le mobile a besoin de moins de données et d'un format différent de celui du web. Une passerelle unique servant tous les clients devient surchargée. Le BFF garde l'API de chaque client légère et conçue pour son usage.

## Composition d'API {#api-composition}

Un service (généralement le BFF ou la Gateway) agrège les données de plusieurs services backend via des appels synchrones. C'est simple, mais vulnérable aux défaillances en cascade.

## CQRS (Command Query Responsibility Segregation) {#cqrs-command-query-responsibility-segregation}

Services distincts pour la lecture et l'écriture des données. Les services d'écriture contiennent la logique métier. Le service de lecture maintient sa propre base de données, optimisée pour des requêtes rapides, alimentée de manière asynchrone via un broker de messages.

```php
[Client] --write--> [Command Service] --event--> [Message Broker] --event--> [Read Service/Query DB]
[Client] --read---> [Read Service] --query--> [Query DB (optimized)]
```

**Quand le choisir :**
- Composition d'API : agrégation simple, synchrone, complexité moindre
- CQRS : systèmes à forte charge, requêtes complexes, besoin d'optimisation de la lecture, synchronisation asynchrone des données acceptable

## Pattern Saga {#saga-pattern}

Coordonne les transactions distribuées entre plusieurs services sans 2PC (two-phase commit, validation en deux phases). Chaque service effectue une transaction locale et publie des événements ou des commandes. En cas d'échec, des transactions compensatoires annulent les étapes précédentes.

### Orchestration (centralisée) {#orchestration-centralized}
```php
[Orchestrator] --command--> [Service A] --response--> [Orchestrator]
[Orchestrator] --command--> [Service B] --response--> [Orchestrator]
[Orchestrator] --compensate--> [Service A]  (on failure)
```
- Avantage : contrôle centralisé, débogage plus facile, flux clair
- Inconvénient : point de défaillance unique, l'orchestrateur devient complexe

### Chorégraphie (décentralisée) {#choreography-decentralized}
```php
[Service A] --event--> [Service B] --event--> [Service C]
                                     (failure) --compensating event-->
```
- Avantage : pas de SPOF, services individuels plus simples, meilleure scalabilité
- Inconvénient : débogage et supervision plus difficiles, workflow implicite

## Event Sourcing {#event-sourcing}

Au lieu de stocker l'état courant, on stocke la séquence des événements. Chaque modification est un événement immuable dans un journal en ajout seul (append-only). L'état courant est obtenu en rejouant les événements.

**Avantages :** piste d'audit complète, requêtes temporelles, rejeu des événements pour le débogage.
**Coûts :** augmentation du stockage, complexité, cohérence à terme, évolution du schéma des événements.

## Circuit Breaker {#circuit-breaker}

Empêche les défaillances en cascade lorsqu'un service aval tombe en panne.

```php
[Closed] --failures exceed threshold--> [Open] --timeout--> [Half-Open]
  ^                                                              |
  |              success                                         |
  <--------------------------------------------------------------
```

1. **Fermé** : fonctionnement normal, les requêtes passent
2. **Ouvert** : service en panne, les requêtes échouent immédiatement (fail-fast)
3. **Semi-ouvert** : après le délai d'attente, un nombre limité de requêtes est autorisé pour tester la reprise

## Idempotence {#idempotency}

Essentielle pour les modèles synchrones comme asynchrones. Les défaillances réseau peuvent provoquer des messages dupliqués. Les services doivent gérer les doublons correctement.

**Mise en œuvre :** identifiants de requête uniques + déduplication côté récepteur. Une opération idempotente produit le même résultat quel que soit le nombre de fois où elle est appelée.

## Pièges à éviter {#gotchas}

- **Chaînes synchrones** (A appelle B qui appelle C) créent un risque de défaillance en cascade : un seul service lent bloque toute la chaîne
- **Le rollback d'une saga** n'est pas un véritable rollback : les transactions compensatoires peuvent avoir des effets de bord
- **Event sourcing sans snapshots** implique de rejouer l'historique complet des événements à chaque lecture
- **Le circuit breaker nécessite un réglage** : un seuil trop bas provoque de faux positifs, un seuil trop haut n'offre pas de protection
- **Un BFF par type de client** peut entraîner de la duplication de code : partager une bibliothèque commune entre les BFF

## Voir aussi {#see-also}

- [[architectural-styles]] - Du monolithe aux microservices
- [[message-broker-patterns]] - Pub/sub vs file d'attente, push vs pull
- [[kafka-architecture]] - Plateforme de streaming d'événements
- [[rabbitmq-architecture]] - Broker de files de messages
- [[async-event-apis]] - WebSockets, SSE, webhooks, concurrence
