---
title: System Design Template
category: patterns
tags: [system-design, architecture-process, estimation]
---
# System Design Template

A structured 7-step algorithm for solving any architectural task, ensuring no critical aspect is missed regardless of domain or scale.

## Key Facts

- The template is domain-agnostic - specific domains only lengthen individual steps, not change the structure
- After each step you can return to any previous step, refine it, and re-execute forward
- Steps 1-2 are covered by "Business Research" - understanding WHAT we are building and WHY
- Steps 3-5 form the core design work with [[quality-attributes]], [[distributed-system-patterns]], and component selection
- Step 6 justifies specific tool choices (e.g., "ClickHouse fits our read-heavy analytics profile" not "I like ClickHouse")
- Step 7 is optional: infrastructure cost estimation, operational concerns, and anything not covered earlier

## Patterns

```
Step 1: Business Context & Constraints
  |  - Stakeholder needs, business goals, revenue model
  |  - Non-functional constraints (budget, team size, deadlines)
  v
Step 2: Functional Requirements (User Stories, BPMN)
  |  - User stories: "As [role], I want [action], so that [benefit]"
  |  - Business process diagrams
  v
Step 3: Non-Functional Requirements / Quality Attributes
  |  - Availability targets (e.g., 99.9% != 100%)
  |  - Latency, throughput, consistency requirements
  |  - See [[quality-attributes]]
  v
Step 4: High-Level Architecture (C4 Context + Container)
  |  - Component identification and boundaries
  |  - Communication patterns (sync/async)
  |  - See [[orchestration-vs-choreography]]
  v
Step 5: Data Flow & Storage Design
  |  - Data models, storage selection
  |  - See [[database-selection]], [[caching-strategies]]
  v
Step 6: Technology Justification
  |  - Why THIS database/queue/framework
  |  - Comparison table with criteria weighted by NFRs
  v
Step 7: Operational Concerns (optional)
     - Cost estimation (AWS/Hetzner/DO price comparison)
     - Monitoring, deployment, migration plan
     - See [[testing-pyramid]]
```

### Back-of-envelope estimation

| Resource | Latency |
|----------|---------|
| L1 cache ref | 0.5 ns |
| L2 cache ref | 7 ns |
| Main memory ref | 100 ns |
| SSD random read | 150 us |
| HDD seek | 10 ms |
| Round trip within datacenter | 500 us |
| Cross-continent round trip | 150 ms |

Use these to sanity-check design decisions. If your design requires cross-datacenter round trips for every request, latency will dominate.

## Gotchas

- **Symptom**: Infrastructure cost estimate comes to $100K+/month -> **Cause**: Over-engineering, too many independent services for actual load -> **Fix**: Re-evaluate if you actually need microservices at your scale, consider [[microservices-vs-monolith]]
- **Symptom**: 100% availability requirement from business -> **Cause**: Business does not understand distributed systems limits -> **Fix**: Negotiate to 99.99% (52 min downtime/year); explain that even load balancers can fail. Client-side retries are cheaper than heroic server-side measures
- **Symptom**: Spending weeks on step 4 without completing steps 1-2 -> **Cause**: Jumping to solution without understanding the problem -> **Fix**: Enforce sequential completion; architecture is driven by requirements, not technology preferences

## See Also

- [[quality-attributes]] - Step 3 deep dive
- [[architectural-decision-records]] - Documenting step 6 decisions
- [[distributed-system-patterns]] - Patterns applied in steps 4-5
- Martin Fowler: [Software Architecture Guide](https://martinfowler.com/architecture/)
- Book: "Software Architecture in Practice" (Bass, Clements, Kazman)
