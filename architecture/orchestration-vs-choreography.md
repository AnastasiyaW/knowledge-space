---
title: Orchestration vs Choreography
category: concepts
tags: [service-communication, saga, workflow, event-driven]
---
# Orchestration vs Choreography

Two fundamental approaches to coordinating work across multiple services: centralized control (orchestration) vs distributed event-driven coordination (choreography).

## Key Facts

- Orchestration: a central coordinator (orchestrator) tells each service what to do and when. Services are "dumb workers"
- Choreography: each service reacts to events independently. No central coordinator. Services are autonomous
- [[bff-pattern]] naturally uses orchestration: BFF calls backend services, aggregates responses, returns to client
- Orchestration is simpler for BFF but choreography works better for complex backend workflows
- The Saga pattern implements distributed transactions using either orchestration or choreography
- Nothing prevents mixing both: BFF orchestrates frontend-facing calls, backend services use choreography for internal workflows
- See [[message-queues]] for the infrastructure that enables choreography
- See [[microservices-vs-monolith]] for when you even need these patterns

## Patterns

### Orchestration

```
Client --> [Orchestrator]
              |
              +--> Service A (validate order)
              |       |
              |    response
              |       |
              +--> Service B (charge payment)
              |       |
              |    response
              |       |
              +--> Service C (ship order)
              |
           Return aggregated result

Characteristics:
  + Clear workflow visible in one place
  + Easy to debug (follow the orchestrator)
  + Simple error handling (orchestrator decides)
  - Single point of failure
  - Orchestrator becomes a bottleneck
  - Tight coupling (orchestrator knows all services)
```

### Choreography

```
Service A publishes --> [Event Bus] --> Service B subscribes
                                    --> Service C subscribes
                                    --> Service D subscribes

Event: "OrderCreated"
  -> PaymentService: charge customer
       Event: "PaymentProcessed"
         -> InventoryService: reserve items
              Event: "ItemsReserved"
                -> ShippingService: create shipment

Characteristics:
  + Services are loosely coupled
  + Easy to add new subscribers
  + No single point of failure
  + Better scalability
  - Hard to track full workflow
  - Debugging requires distributed tracing
  - Complex error handling (compensating events)
```

### Saga pattern (distributed transactions)

```
Orchestration-based Saga:
  [Saga Orchestrator]
    1. CreateOrder      --> OrderService
    2. ReserveStock     --> InventoryService
    3. ProcessPayment   --> PaymentService
    4. ConfirmOrder     --> OrderService

  On failure at step 3:
    Compensate 2: ReleaseStock  --> InventoryService
    Compensate 1: CancelOrder   --> OrderService

Choreography-based Saga:
  OrderService:
    on OrderCreated -> publish "OrderCreated"
  InventoryService:
    on OrderCreated -> reserve stock, publish "StockReserved"
  PaymentService:
    on StockReserved -> charge, publish "PaymentProcessed"
  OrderService:
    on PaymentProcessed -> confirm order

  On PaymentFailed:
    InventoryService: on PaymentFailed -> release stock
    OrderService: on StockReleased -> cancel order
```

### When to use which

| Criterion | Orchestration | Choreography |
|-----------|--------------|--------------|
| Workflow complexity | Simple, linear | Complex, branching |
| Number of services | Few (2-5) | Many (5+) |
| Error handling | Centralized | Distributed compensation |
| Visibility | Clear (one place) | Requires tracing |
| Coupling | Higher | Lower |
| Scalability | Limited by orchestrator | Better |
| BFF use case | Natural fit | Unusual |
| Backend workflows | OK for simple | Better for complex |

## Gotchas

- **Symptom**: Choreography workflow is impossible to debug -> **Cause**: No distributed tracing, events not correlated -> **Fix**: Use correlation IDs in every event. Implement distributed tracing (Jaeger, Zipkin). Log event chains with timestamps
- **Symptom**: Saga compensation fails, leaving system in inconsistent state -> **Cause**: Compensating action itself can fail -> **Fix**: Make compensating actions idempotent and retriable. Use dead letter queues for failed compensations. Design for eventual consistency
- **Symptom**: Adding new step to choreography breaks existing flow -> **Cause**: Implicit ordering assumptions between services -> **Fix**: Each service should react only to events it cares about, not assume event ordering. Use explicit state machines per entity
- **Symptom**: Orchestrator becomes a monolith -> **Cause**: Business logic creeping into orchestrator -> **Fix**: Orchestrator should only manage workflow sequence, not business rules. Each service owns its domain logic

## See Also

- [[message-queues]] - Infrastructure for event-based choreography
- [[bff-pattern]] - Orchestration pattern for frontend-facing APIs
- [[microservices-vs-monolith]] - Architecture context for these patterns
- [[distributed-system-patterns]] - Related patterns (CQRS, Event Sourcing)
- Microsoft: [Choreography pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography)
- Microsoft: [Saga distributed transactions](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga)
- Chris Richardson: [Saga Pattern](https://microservices.io/patterns/data/saga.html)
