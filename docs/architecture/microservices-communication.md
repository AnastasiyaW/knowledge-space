---
title: Microservices Communication Patterns
category: patterns
tags: [microservices, api-gateway, bff, cqrs, saga, event-sourcing]
---

# Microservices Communication Patterns

How microservices talk to each other and to external clients. The choice between synchronous and asynchronous communication fundamentally shapes system behavior, coupling, and failure modes.

## Synchronous Communication (API-based)

Service A calls Service B's API directly. Simple but creates strong coupling - if B is slow or down, A suffers.

**Protocols:** REST, gRPC, GraphQL. Can also use WebSocket, webhooks, async HTTP.

## Asynchronous Communication (Message-based)

Services communicate through message brokers (RabbitMQ, Kafka). Service A sends message, Service B processes when ready. Enables loose coupling and independent operation.

### Async Styles

| Style | Behavior | Use Case |
|-------|----------|----------|
| **Request/Response** | Non-blocking, expect quick response | Inter-service queries |
| **Notifications** | Fire and forget, no response | Event broadcasting |
| **Request/Async Response** | Expect response at some future point | Long-running operations |

## API Gateway Pattern

Centralized entry point for all external clients. Hides internal system structure.

**Capabilities:**
1. **Request routing** - directs to appropriate microservice
2. **Data aggregation** - combines responses from multiple services
3. **Auth** - centralized authentication/authorization
4. **Rate limiting** - prevents overload
5. **Caching** - reduces backend load
6. **Monitoring/logging** - collects statistics and request logs
7. **Error handling** - standardized responses, hides internal details

**Drawbacks:** Single point of failure (need HA), performance bottleneck (all traffic flows through it), vendor lock-in risk.

## Backend for Frontend (BFF)

Separate gateway per client type (mobile, web, desktop). Each BFF is optimized for its specific client's needs, data requirements, and performance characteristics.

**Why BFF over single Gateway:** Mobile needs less data + different format than web. Single gateway serving all clients becomes bloated. BFF keeps each client's API lean and purpose-built.

## API Composition

One service (usually BFF or Gateway) aggregates data from multiple backend services via synchronous calls. Simple but vulnerable to cascade failures.

## CQRS (Command Query Responsibility Segregation)

Separate services for reading and writing data. Write services contain business logic. Read service maintains its own database optimized for fast queries, populated asynchronously via message broker.

```
[Client] --write--> [Command Service] --event--> [Message Broker] --event--> [Read Service/Query DB]
[Client] --read---> [Read Service] --query--> [Query DB (optimized)]
```

**When to choose:**
- API Composition: simple aggregation, synchronous, lower complexity
- CQRS: high-load systems, complex queries, read optimization needed, async data sync acceptable

## Saga Pattern

Coordinates distributed transactions across multiple services without 2PC (two-phase commit). Each service performs local transaction and publishes events/commands. On failure, compensating transactions undo previous steps.

### Orchestration (Centralized)
```
[Orchestrator] --command--> [Service A] --response--> [Orchestrator]
[Orchestrator] --command--> [Service B] --response--> [Orchestrator]
[Orchestrator] --compensate--> [Service A]  (on failure)
```
- Pro: centralized control, easier debugging, clear flow
- Con: single point of failure, orchestrator becomes complex

### Choreography (Decentralized)
```
[Service A] --event--> [Service B] --event--> [Service C]
                                     (failure) --compensating event-->
```
- Pro: no SPOF, simpler individual services, better scalability
- Con: harder to debug/monitor, implicit workflow

## Event Sourcing

Instead of storing current state, store sequence of events. Every change is an immutable event in an append-only log. Current state derived by replaying events.

**Benefits:** Complete audit trail, temporal queries, event replay for debugging.
**Costs:** Increased storage, complexity, eventual consistency, event schema evolution.

## Circuit Breaker

Prevents cascade failures when downstream service is failing.

```
[Closed] --failures exceed threshold--> [Open] --timeout--> [Half-Open]
  ^                                                              |
  |              success                                         |
  <--------------------------------------------------------------
```

1. **Closed** - normal operation, requests pass through
2. **Open** - service failing, requests immediately fail-fast
3. **Half-Open** - after timeout, allow limited requests to test recovery

## Idempotency

Critical for both sync and async patterns. Network failures can cause duplicate messages. Services must handle duplicates gracefully.

**Implementation:** unique request IDs + deduplication on receiver side. An idempotent operation produces the same result regardless of how many times it's called.

## Gotchas

- **Synchronous chains** (A calls B calls C) create cascading failure risk - one slow service blocks the chain
- **Saga rollback** is not true rollback - compensating transactions may have side effects
- **Event sourcing without snapshots** means replaying entire event history on every read
- **Circuit breaker requires tuning** - threshold too low causes false positives, too high doesn't protect
- **BFF per client type** can lead to code duplication - share a core library between BFFs

## See Also

- [[architectural-styles]] - Monolith to microservices spectrum
- [[message-broker-patterns]] - Pub/sub vs queue, push vs pull
- [[kafka-architecture]] - Event streaming platform
- [[rabbitmq-architecture]] - Message queue broker
- [[async-event-apis]] - WebSockets, SSE, webhooks, concurrency
