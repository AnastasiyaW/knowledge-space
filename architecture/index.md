---
title: Software Architecture - Knowledge Base
type: MOC
---
# Software Architecture

Reference knowledge base for software architecture concepts, patterns, and decision-making frameworks. Organized for querying during development work.

## Architecture Process

The structured approach to solving architectural problems, from business requirements to technology choices.

- [[system-design-template]] - 7-step algorithm for solving any architectural task
- [[quality-attributes]] - Non-functional requirements: availability, latency, throughput, scalability
- [[architectural-decision-records]] - Documenting decisions with ADR format, C4 model, comparison tables

## Distributed Systems Fundamentals

Core theory and patterns for building reliable distributed systems.

- [[cap-theorem]] - Consistency vs availability tradeoffs, PACELC extension, tunable consistency
- [[distributed-system-patterns]] - CQRS, Event Sourcing, Circuit Breaker, Retry, Bulkhead, Idempotency
- [[quality-attributes]] - USL (Universal Scalability Law), availability math, SLA calculations

## Architecture Styles

Choosing and implementing the right architecture style for your context.

- [[microservices-vs-monolith]] - Architecture spectrum, migration strategies, Conway's Law
- [[orchestration-vs-choreography]] - Centralized vs event-driven service coordination, Saga pattern
- [[bff-pattern]] - Backend-for-Frontend: client-specific API aggregation
- [[service-mesh]] - Infrastructure layer for microservices (Istio, Envoy, Linkerd)

## Data & Storage

Database selection, caching, and data format decisions.

- [[database-selection]] - Relational, Document, Wide-Column, Key-Value, Graph, Time-Series comparison
- [[caching-strategies]] - Read/write strategies, session externalization, eviction policies
- [[data-serialization-formats]] - JSON, XML/XSD, Protobuf, schema evolution

## Integration & Communication

API design, messaging, and service communication.

- [[api-design-process]] - REST/gRPC/GraphQL selection, versioning, idempotency, OpenAPI
- [[message-queues]] - RabbitMQ vs Kafka, delivery guarantees, exchange types, consumer groups
- [[load-balancing]] - L4/L7 balancing, algorithms, health checks, sticky sessions

## Quality & Operations

Testing strategies and operational concerns.

- [[testing-pyramid]] - Unit/integration/E2E distribution, test-design techniques, migration testing

---

## Quick Decision Trees

### "Which database?"
```
Need ACID transactions?
  Yes -> PostgreSQL (or MySQL)
Need flexible schema?
  Yes -> MongoDB
Need high write throughput (>500K TPS)?
  Yes -> Cassandra / ScyllaDB
Need sub-ms latency for simple keys?
  Yes -> Redis
Need full-text search?
  Yes -> Elasticsearch
Need relationship traversal?
  Yes -> Neo4j
```

### "Microservices or monolith?"
```
Team size < 10?
  -> Monolith (or modular monolith)
Clear domain boundaries + independent deployment needed?
  -> Microservices
Unclear boundaries + fast iteration needed?
  -> Start monolith, extract later (Strangler Fig)
```

### "REST, gRPC, or GraphQL?"
```
Public/browser API?
  -> REST (with OpenAPI)
Internal service-to-service, performance critical?
  -> gRPC
Complex queries, client needs flexibility?
  -> GraphQL
Bidirectional real-time?
  -> WebSocket (or gRPC streaming)
```
