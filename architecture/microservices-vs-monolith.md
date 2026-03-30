---
title: Microservices vs Monolith
category: concepts
tags: [architecture-style, microservices, monolith, migration, modular-monolith]
---
# Microservices vs Monolith

The choice between monolithic and microservices architecture is one of the most impactful architectural decisions, driven by team size, organizational structure, and actual scaling needs rather than technology hype.

## Key Facts

- Violating "rules" (like shared database in microservices) is justified IF done consciously with understanding of consequences
- Shared database between microservices is valid if: each service owns specific tables, updates don't affect other services, or impact follows a known process
- Every architectural decision creates future problems. A good architect minimizes future pain while solving current problems
- Conway's Law: system architecture mirrors team communication structure. Microservices work best when each service is owned by a separate team
- Monolith-first is often the right strategy: start monolithic, extract services when pain points emerge at scale
- Modular monolith = best of both: single deployment unit with clear module boundaries and defined interfaces
- See [[system-design-template]] for the full process that leads to this decision
- See [[architectural-decision-records]] for how to document this choice

## Patterns

### Architecture spectrum

```
Monolith          Modular Monolith       Microservices
  |                    |                      |
  Single codebase      Single deploy         Independent deploy
  Single DB            Schema per module     DB per service
  Single team OK       Multiple teams OK     Team per service
  Simple ops           Medium ops            Complex ops
  Fast dev (small)     Fast dev (medium)     Fast dev (large)
  Hard to scale parts  Can extract later     Independent scaling
```

### When to choose what

```
Monolith when:
  - Team < 10 developers
  - Single product, unclear domain boundaries
  - Early stage startup
  - Need fast iteration
  - Simple deployment requirements

Modular Monolith when:
  - 10-50 developers
  - Clear domain boundaries exist
  - Want independent module development
  - Not ready for distributed systems complexity
  - Migration path to microservices needed

Microservices when:
  - 50+ developers across multiple teams
  - Independent deployment required
  - Different scaling needs per domain
  - Different tech stacks needed per domain
  - Organization already aligned by service
```

### Migration strategy: Strangler Fig

```
Phase 1: Identify bounded contexts in monolith
  [Monolith: Orders + Users + Payments + Inventory]

Phase 2: Extract highest-value service
  [Monolith: Orders + Users + Inventory]
  [Payments Service] <-- extracted first (compliance needs)

Phase 3: Route via facade
  [API Gateway]
    /payments/* --> [Payments Service]
    /*          --> [Monolith]

Phase 4: Continue extraction as needed
  Each extraction is an independent decision
  Some modules may STAY in the monolith forever
```

### Mono-repo vs multi-repo

```
Mono-repo (Google, Meta style):
  + Atomic cross-service changes
  + Shared tooling and CI
  + Code reuse via shared libraries
  - Requires sophisticated build system
  - CI pipeline can be slow

Multi-repo:
  + Clear ownership boundaries
  + Independent CI/CD per service
  + Easier access control
  - Cross-repo changes are painful
  - Dependency management complexity

Platform repo (hybrid):
  - Core platform in one repo
  - Features as separate repos using platform
  - Works well for plugin architectures
```

## Gotchas

- **Symptom**: Customer wants microservices "because it's trendy" -> **Cause**: Cargo-cult architecture -> **Fix**: Present concrete tradeoffs. Microservices add network latency, distributed transactions, operational complexity. Ask: "Do you have 5+ teams that need independent deployment?"
- **Symptom**: "Distributed monolith" - microservices that must be deployed together -> **Cause**: Tight coupling between services (shared schemas, synchronous chains) -> **Fix**: Ensure each service can be deployed and tested independently. If services cannot function without each other, they should be one service
- **Symptom**: Shared database leads to schema conflicts between services -> **Cause**: No ownership boundaries for tables -> **Fix**: Assign each table to exactly one owning service. Other services access data only via API. Consider database views for read-only shared access
- **Symptom**: Extracting a service breaks existing functionality -> **Cause**: Extracting without understanding all callers and data dependencies -> **Fix**: Use Strangler Fig pattern: run both old and new code in parallel, route incrementally, verify parity before cutover

## See Also

- [[orchestration-vs-choreography]] - How services communicate
- [[message-queues]] - Async communication between services
- [[architectural-decision-records]] - Document the monolith vs microservices choice
- [[service-mesh]] - Infrastructure for microservices management
- Martin Fowler: [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)
- Martin Fowler: [Microservices Guide](https://martinfowler.com/microservices/)
- Sam Newman: "Building Microservices" (O'Reilly)
