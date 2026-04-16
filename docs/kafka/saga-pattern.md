---
title: Saga Pattern
category: patterns
tags: [kafka, saga, choreography, orchestration, distributed-transactions, microservices, compensation]
---

# Saga Pattern

The Saga pattern manages distributed transactions across microservices via Kafka using either choreography (event-driven, decentralized) or orchestration (coordinator-driven, centralized), with compensation logic for rollback on failure.

## Key Facts

- Distributed transactions via two-phase commit (2PC) are slow, complex, and fragile in microservice architectures
- Saga replaces 2PC with a sequence of local transactions, each publishing events to Kafka
- Two variants: **choreography** (decentralized) and **orchestration** (centralized coordinator)
- Each step has a corresponding **compensation** action for rollback
- Debugging distributed transactions requires replaying Kafka log backwards to reconstruct object state
- Eventual consistency is inherent - strong consistency requires distributed transactions

## Patterns

### Choreography-Based Saga

```php
Order Service -> "OrderCreated" event -> Kafka
  Payment Service consumes -> processes payment -> "PaymentCompleted" event -> Kafka
    Inventory Service consumes -> reserves stock -> "StockReserved" event -> Kafka
      Shipping Service consumes -> schedules delivery -> "OrderFulfilled" event -> Kafka

On failure (e.g., payment fails):
  Payment Service -> "PaymentFailed" event -> Kafka
    Order Service consumes -> compensates (cancel order)
```

- Pro: simple implementation, fully decoupled services
- Con: hard to debug and monitor overall transaction flow; no central visibility

### Orchestration-Based Saga

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

- Pro: clear transaction flow, easy debugging, single point of control
- Con: coordinator is a single point of complexity; needs to be resilient itself

### Implementation with Kafka

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

### Design Considerations

- **Partition by entity key** (e.g., order ID) - ensures all events for one saga land in same partition, preserving order
- **Idempotent compensation** - compensation actions must be idempotent (may be called multiple times)
- **Timeout handling** - define maximum saga duration; auto-compensate on timeout
- **State machine** - track saga state (STARTED, PAYMENT_DONE, STOCK_RESERVED, COMPLETED, COMPENSATING, FAILED)

## Gotchas

- **Choreography is hard to debug at scale** - no single place to see saga status; consider adding correlation IDs and central logging
- **Compensation is not always possible** - some actions are irreversible (email sent, physical shipment dispatched); design compensating actions before implementing the saga
- **Eventual consistency confuses users** - display "processing" states instead of waiting for completion
- **Orchestrator must be resilient** - if it crashes mid-saga, it must recover and continue; store saga state in a database or Kafka topic

## See Also

- [[event-sourcing]] - storing state transitions as events for replay
- [[cqrs-pattern]] - separating command and query paths
- [[transactional-outbox]] - reliable event publishing from services
- [[delivery-semantics]] - at-least-once + idempotence for saga steps
