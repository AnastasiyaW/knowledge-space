---
title: Architectural Styles - Monolith to Microservices
category: concepts
tags: [architecture, monolith, microservices, soa, modular-monolith]
---

# Architectural Styles - Monolith to Microservices

The choice of architectural style is the first and most important design step. It determines flexibility, scalability, and key system characteristics. Architecture is a spectrum, not a binary choice.

## Style Evolution

```
Monolith -> Modular Monolith -> SOA -> Microservices -> Microservices + Micro-Frontends
```

1. **Monolith** - single deployment, tightly coupled. All components in one codebase
2. **Modular Monolith** - clear module boundaries within single deployment, well-defined interfaces
3. **SOA** - services via enterprise bus (ESB), shared database possible
4. **Microservices** - independent services with own databases, independent deployment
5. **Microservices + Micro-Frontends** - both backend and frontend split into autonomous parts

## When to Choose What

### Start with Monolith When
- Small team (< 5-7 developers)
- Simple domain
- Speed of initial development matters
- Don't know the domain well yet
- Low change frequency
- Team lacks DevOps/infrastructure maturity

### Migrate to Microservices When
- Team grows and needs independent deployments
- Different scaling requirements per domain
- Need technology diversity
- Clear domain boundaries identified
- Operational complexity overhead is worth the benefits

### Decision Tree

```
Team size < 10?
  -> Monolith (or modular monolith)
Clear domain boundaries + independent deployment needed?
  -> Microservices
Unclear boundaries + fast iteration needed?
  -> Start monolith, extract later (Strangler Fig)
```

## Monolith to Microservices Migration

### Strangler Fig Pattern
Gradually replace monolith functionality:
1. New features built as microservices
2. Existing features extracted one by one
3. Route traffic through a facade that decides monolith vs. microservice
4. Monolith shrinks over time until fully replaced

### Distributed Monolith (Anti-pattern)
Services that are deployed separately but so tightly coupled they must be deployed together. Worst of both worlds - distributed complexity without independence benefits.

## Microservices Core Principles

### Low Coupling
Service A (creates orders) knows nothing about payment. Service B (processes payment) knows nothing about order creation. Each service has minimal dependencies, enabling independent deployment.

### High Cohesion
Code for one functional area belongs together. Each microservice is responsible for one and only one functional area.

### Benefits of Both
- Independent scaling per service
- Independent deployment (no full rebuild)
- Each service stays simple
- Different technology stacks per service
- Accelerated delivery of production code

## Microservices Database Patterns

### Database per Service
Each microservice owns its database. No shared databases. Services communicate through APIs, not joins. Enables technology diversity and independent scaling.

### Shared Database (Anti-pattern)
Multiple services accessing same database creates tight coupling. Acceptable only in transitional monolith-to-microservices migration.

### Data Ownership Rules
- Small datasets from another service: local cache (fastest but needs invalidation)
- Large shared datasets: distributed cache (Redis) accessible by both
- If cached foreign data >> own data: reconsider service boundaries

## Service Discovery

Services need to find each other in dynamic environments (containers, auto-scaling).

- **Client-side discovery** - client queries registry, connects directly
- **Server-side discovery** - client sends to load balancer which queries registry

Tools: Consul, Eureka, etcd, Kubernetes DNS.

## Gotchas

- **Don't start with microservices** - start with well-structured monolith, decompose when pain points emerge
- **Conway's Law** - system design mirrors organizational communication structure
- **Microservices without DevOps maturity** = operational nightmare
- **Modular monolith** is often the sweet spot - clear boundaries without distributed system complexity
- **Architects sometimes appear to underperform** while fighting organizational battles (e.g., waiting months for infrastructure)

## See Also

- [[microservices-communication]] - Sync vs async, API gateway, BFF, CQRS
- [[distributed-systems-fundamentals]] - CAP theorem, consensus, replication
- [[enterprise-integration]] - ESB, integration styles, modern alternatives
- [[microfrontends]] - Frontend decomposition strategies
