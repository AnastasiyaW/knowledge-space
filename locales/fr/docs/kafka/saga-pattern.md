---
title: "Patron Saga"
category: patterns
tags: [kafka, saga, choreography, orchestration, distributed-transactions, microservices, compensation]
level: 3
source_sha256: d019e396ab0090394153312fbd743d415e2157855d7d30cb2b7751a55da10dec
translation: machine
translated_at: '2026-10-24'
---
# Patron Saga {#saga-pattern}

Le patron Saga gère les transactions distribuées entre microservices via Kafka, en utilisant soit la chorégraphie (pilotée par les événements, décentralisée), soit l'orchestration (pilotée par un coordinateur, centralisée), avec une logique de compensation pour le retour en arrière en cas d'échec.

## Points clés {#key-facts}

- Les transactions distribuées via le two-phase commit (2PC) sont lentes, complexes et fragiles dans les architectures microservices
- Saga remplace le 2PC par une séquence de transactions locales, chacune publiant des événements dans Kafka
- Deux variantes : **chorégraphie** (décentralisée) et **orchestration** (coordinateur centralisé)
- Chaque étape possède une action de **compensation** correspondante pour le retour en arrière
- Le débogage des transactions distribuées nécessite de rejouer le log Kafka à rebours pour reconstruire l'état des objets
- La cohérence éventuelle est inhérente : une cohérence forte nécessite des transactions distribuées

## Patrons {#patterns}

### Saga basée sur la chorégraphie {#choreography-based-saga}

```php
Order Service -> "OrderCreated" event -> Kafka
  Payment Service consumes -> processes payment -> "PaymentCompleted" event -> Kafka
    Inventory Service consumes -> reserves stock -> "StockReserved" event -> Kafka
      Shipping Service consumes -> schedules delivery -> "OrderFulfilled" event -> Kafka

On failure (e.g., payment fails):
  Payment Service -> "PaymentFailed" event -> Kafka
    Order Service consumes -> compensates (cancel order)
```

- Avantage : implémentation simple, services totalement découplés
- Inconvénient : difficile à déboguer et à superviser pour l'ensemble du flux transactionnel ; pas de visibilité centrale

### Saga basée sur l'orchestration {#orchestration-based-saga}

```php
Saga Coordinator receives "CreateOrder" command
  -> sends "ProcessPayment" to Payment Service
  <- receives "PaymentCompleted"
  -> sends "ReserveStock" to Inventory Service
  <- receives "StockReserved"
  -> sends "ScheduleDelivery" to Shipping Service
  <- receives "DeliveryScheduled"
  -> marks saga as complete

On failure:
  <- receives "StockUnavailable"
  -> sends "RefundPayment" to Payment Service (compensation)
  -> sends "CancelOrder" to Order Service (compensation)
  -> marks saga as failed
```

- Avantage : flux transactionnel clair, débogage facilité, point de contrôle unique
- Inconvénient : le coordinateur est un point de complexité unique ; il doit lui-même être résilient

### Implémentation avec Kafka {#implementation-with-kafka}

```java
// Choreography: each service produces events on completion
@KafkaListener(topics = "order-events")
public void handleOrderEvent(OrderEvent event) {
    if (event.getType().equals("OrderCreated")) {
        try {
            processPayment(event.getOrderId());
            kafkaTemplate.send("payment-events", new PaymentCompleted(event.getOrderId()));
        } catch (Exception e) {
            kafkaTemplate.send("payment-events", new PaymentFailed(event.getOrderId(), e.getMessage()));
        }
    }
}
```

### Considérations de conception {#design-considerations}

- **Partitionnement par clé d'entité** (par exemple, l'identifiant de commande) : garantit que tous les événements d'une même saga atterrissent dans la même partition, préservant ainsi l'ordre
- **Compensation idempotente** : les actions de compensation doivent être idempotentes (elles peuvent être appelées plusieurs fois)
- **Gestion des délais d'expiration** : définir une durée maximale pour la saga ; compenser automatiquement en cas de dépassement
- **Machine à états** : suivre l'état de la saga (STARTED, PAYMENT_DONE, STOCK_RESERVED, COMPLETED, COMPENSATING, FAILED)

## Pièges {#gotchas}

- **La chorégraphie est difficile à déboguer à grande échelle** : aucun point unique pour consulter l'état de la saga ; envisager d'ajouter des identifiants de corrélation et une journalisation centralisée
- **La compensation n'est pas toujours possible** : certaines actions sont irréversibles (courriel envoyé, expédition physique effectuée) ; concevoir les actions de compensation avant d'implémenter la saga
- **La cohérence éventuelle déroute les utilisateurs** : afficher des états « en cours de traitement » plutôt qu'attendre la fin du processus
- **L'orchestrateur doit être résilient** : s'il tombe en panne au milieu d'une saga, il doit pouvoir reprendre et poursuivre ; stocker l'état de la saga dans une base de données ou un topic Kafka

## Voir aussi {#see-also}

- [[event-sourcing]] - stocker les transitions d'état sous forme d'événements pour les rejouer
- [[cqrs-pattern]] - séparer les chemins de commande et de requête
- [[transactional-outbox]] - publication fiable d'événements depuis les services
- [[delivery-semantics]] - at-least-once + idempotence pour les étapes de la saga
