---
title: Enterprise Integration - ESB, Styles, Patterns
category: concepts
tags: [integration, esb, eip, api-gateway, service-mesh, ipaas]
---

# Enterprise Integration - ESB, Styles, Patterns

Modern systems rarely operate in isolation. Well-designed integration reduces latency, improves maintainability, enables scalability, and ensures security.

## Integration Styles

| Style | Mechanism | Coupling | Latency | Use Case |
|-------|-----------|---------|---------|----------|
| **File Transfer** | Shared files (CSV, XML, JSON) | Low | High | Batch data exchange |
| **Shared Database** | Multiple systems, same DB | Very high | Low | Avoid in modern architectures |
| **Remote Procedure (RPI)** | REST, gRPC, SOAP calls | Medium | Low | Service-to-service sync |
| **Messaging** | Message broker (Kafka, RabbitMQ) | Low | Medium | Async, decoupled systems |

## Enterprise Service Bus (ESB)

Middleware providing centralized integration: routing, protocol translation, message transformation, orchestration.

**Core capabilities:**
- **Routing** - content-based, rule-based, dynamic
- **Transformation** - XML to JSON, schema mapping
- **Protocol mediation** - SOAP to REST, JMS to HTTP
- **Orchestration** - multi-step business processes
- **Service virtualization** - abstract locations and versions
- **Monitoring** - centralized logging, metrics, auditing

**Products:** MuleSoft, IBM Integration Bus, Oracle Service Bus, WSO2, Microsoft BizTalk.

### ESB Anti-pattern
Putting business logic in ESB instead of services. ESB should only route, transform, and mediate - not contain domain logic. Creates monolithic bottleneck.

## Modern Alternatives to ESB

### API Gateway
Simpler than ESB, focused on API management. Rate limiting, auth, routing, transformation.
- Products: Kong, AWS API Gateway, Apigee, nginx

### Event-Driven Architecture
Services communicate via events. Event broker (Kafka) replaces ESB routing. Each service owns its logic.

### Service Mesh
Service-to-service communication at infrastructure level. Sidecar proxy pattern.
- Capabilities: mTLS, load balancing, circuit breaking, observability
- Products: Istio/Envoy, Linkerd
- No application code changes needed

### iPaaS (Integration Platform as a Service)
Cloud-based integration with pre-built connectors for SaaS.
- Products: MuleSoft Anypoint, Dell Boomi, Azure Integration Services

## Enterprise Integration Patterns (EIP)

### Routing Patterns
- **Content-Based Router** - route based on message content
- **Message Filter** - remove unwanted messages
- **Splitter** - break composite message into parts
- **Aggregator** - combine related messages
- **Scatter-Gather** - broadcast to multiple recipients, aggregate responses
- **Routing Slip** - dynamic list of processing steps

### Transformation Patterns
- **Envelope Wrapper** - wrap/unwrap messages for transport
- **Content Enricher** - add data from external source
- **Content Filter** - remove unnecessary data
- **Normalizer** - convert different formats to canonical form

### Error Handling
- **Dead Letter Channel** - unprocessable messages
- **Invalid Message Channel** - malformed messages
- **Retry with backoff** - exponential retry
- **Idempotent Receiver** - handle duplicate messages safely

## Canonical Data Model

Standard data format all systems translate to/from. Reduces N-to-N transformations to N-to-1.

```bash
System A -> [transform to canonical] -> Canonical Format
System B -> [transform to canonical] ->     |
System C -> [transform to canonical] ->     v
                                      [transform from canonical] -> Target
```

**Trade-off:** Maintenance overhead but simplifies adding new systems.

## Integration Planning Process

```php
Gather requirements -> Model in UML -> Choose style -> Define formats ->
  Implement -> Test -> Deploy (return to any step for refinement)
```

**Requirements checklist:** systems involved, data flows (direction, volume, frequency), transformation needs, error handling, SLA (latency, availability), security (auth, encryption, data sensitivity).

## Idempotency in Integration

Operations must be safely retried - messages may be delivered more than once. Use unique message IDs, check-before-write, upsert operations.

## Gotchas

- **Shared database** creates tight coupling and schema change coordination nightmares - avoid in modern architectures
- **File transfer** seems simple but managing polling, naming conventions, concurrent access, and error handling is complex
- **ESB becomes monolithic bottleneck** if it accumulates business logic
- **Service mesh adds latency** per hop (sidecar proxy) - measure before adopting
- **Canonical model overhead** - maintaining the canonical format becomes a governance challenge

## See Also

- [[microservices-communication]] - API Gateway, BFF, Saga patterns
- [[message-broker-patterns]] - Pub/sub, queue, delivery guarantees
- [[kafka-architecture]] - Event streaming for integration
- [[distributed-systems-fundamentals]] - CAP, consistency, replication
