---
title: "APIs asynchrones et événementielles"
category: reference
tags: [async, websocket, sse, webhooks, polling, concurrency, api]
level: 3
source_sha256: d558e9bd367f1be6bd172925626a6f9c51feefabf36c1126c0de8106012eab6e
translation: machine
translated_at: '2026-10-24'
---
# APIs asynchrones et événementielles {#async-and-event-based-apis}

Les API asynchrones permettent une communication non bloquante. Elles sont essentielles pour les fonctionnalités temps réel, les opérations de longue durée et les architectures scalables.

## Comparaison synchrone et asynchrone {#sync-vs-async-comparison}

| Attribut | Synchrone | Asynchrone |
|-----------|------------|--------------|
| Exécution | Attend la réponse | Continue sans attendre |
| Utilisation des ressources | Moins efficace (inactif pendant l'attente) | Plus efficace (parallèle) |
| Scalabilité | Plus faible (bloquant) | Plus élevée (traitement parallèle) |
| Complexité du code | Plus simple, séquentiel | Plus complexe, non linéaire |
| Cohérence des données | Moins de problèmes | Risques de problèmes d'ordonnancement |

## Mécanismes asynchrones basés sur HTTP {#http-based-async-mechanisms}

### Callback {#callback}
Le client fournit une URL que le serveur appelle lorsque la réponse est prête.
- **Latence faible**, complexité modérée
- Problème : « enfer des callbacks » avec des callbacks imbriqués, enjeux de sécurité

### Polling {#polling}
Le client envoie des requêtes à intervalles réguliers.
- Implémentation **simple**, latence élevée, forte charge serveur
- Cas d'usage : tableaux de bord de supervision, fils d'actualité

### Long Polling {#long-polling}
Le serveur maintient la requête ouverte jusqu'à la disponibilité de nouvelles données.
- **Latence faible à modérée**, charge serveur modérée
- Cas d'usage : applications de chat, scores sportifs en direct

| Caractéristique | Callback | Polling | Long Polling |
|---------|----------|---------|--------------|
| Complexité | Modérée | Simple | Modérée |
| Latence | Faible | Élevée | Faible à modérée |
| Charge serveur | Faible à modérée | Élevée | Modérée |

## Technologies asynchrones avancées {#advanced-async-technologies}

### Webhooks {#webhooks}
Le serveur envoie une requête HTTP POST vers un point de terminaison client prédéfini lorsqu'un événement se produit. Approche événementielle, qui élimine le polling.

**Cas d'usage :** notifications de paiement, déclencheurs CI/CD, mises à jour d'abonnement.

**Points d'attention :**
- Logique de nouvelle tentative pour les livraisons échouées
- Signature HMAC pour la sécurité
- Clés d'idempotence pour la gestion des doublons

### WebSockets {#websockets}
Communication bidirectionnelle full-duplex sur une connexion unique et de longue durée. Prend en charge les données textuelles et binaires.

```php
HTTP upgrade handshake -> persistent WebSocket connection
Client <---> Server (bidirectional)
```

**Cas d'usage :** chat en temps réel, enchères en ligne, édition collaborative, jeux.

**Inconvénients :** complexité de la gestion des connexions, connexions avec état plus difficiles à scaler, contraintes liées aux load balancers.

### Server-Sent Events (SSE) {#server-sent-events-sse}
Flux unidirectionnel du serveur vers le client, sur HTTP. Plus simple que les WebSockets.

**Cas d'usage :** cours boursiers en continu, notifications, flux en direct, suivi de progression.

**Avantages par rapport aux WebSockets :** compatible avec l'infrastructure HTTP standard, reconnexion automatique, implémentation plus simple.

## Concurrence et cohérence {#concurrency-and-consistency}

### Verrouillage optimiste (à privilégier pour les API web) {#optimistic-locking-preferred-for-web-apis}

**Basé sur les ETag (recommandé pour les charges élevées) :**
```bash
GET /resource -> ETag: "v5"
PUT /resource + If-Match: "v5"
  Success: 200 OK + new ETag
  Conflict: 412 Precondition Failed
```

**Basé sur l'horodatage (plus simple) :**
```bash
GET /resource -> Last-Modified: timestamp
PUT /resource + If-Unmodified-Since: timestamp
  Conflict: 412 Precondition Failed
```

### Verrouillage pessimiste (pour les conflits à coût élevé) {#pessimistic-locking-for-high-cost-conflicts}
```bash
POST /resource?lock=true -> lockToken
PUT /resource + X-Lock-Token: token -> update + release
Already locked -> 409 Conflict
```

Utilisez le verrouillage pessimiste pour les transactions financières, où les conflits sont très coûteux.

## Spécification AsyncAPI {#asyncapi-specification}

Comparable à OpenAPI, mais destinée aux API événementielles. Elle décrit les canaux (topics/queues), les messages, les schémas et les liaisons serveur pour Kafka, RabbitMQ, WebSocket et MQTT.

## Pièges à éviter {#gotchas}

- **WebSocket derrière des load balancers** : des sticky sessions ou un routage tenant compte des connexions sont nécessaires
- **Limite de connexions SSE** : les navigateurs limitent le nombre de connexions SSE simultanées par domaine (environ 6)
- **Sécurité des webhooks** : vérifiez toujours les signatures HMAC, ne faites jamais confiance à un payload non vérifié
- **Intervalle de polling** : trop fréquent, il gaspille des ressources ; trop espacé, il produit des données obsolètes
- **Horodatages du verrouillage optimiste** : pas assez précis sous forte charge, préférez les ETag

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - Fondements du protocole HTTP
- [[microservices-communication]] - Modèles de communication entre services
- [[message-broker-patterns]] - Kafka, RabbitMQ pour l'asynchrone côté backend
- [[api-documentation-specs]] - Spécification AsyncAPI
