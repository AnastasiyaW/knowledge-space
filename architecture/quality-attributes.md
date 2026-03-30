---
title: Quality Attributes (Non-Functional Requirements)
category: concepts
tags: [nfr, availability, scalability, performance, reliability]
---
# Quality Attributes (Non-Functional Requirements)

Quality attributes are measurable properties of a system that describe HOW it performs its functions, not WHAT functions it performs. They drive architectural decisions more than functional requirements do.

## Key Facts

- Quality attributes must be quantified: "fast" is not a requirement, "p99 latency < 200ms" is
- They often conflict: high availability may reduce consistency ([[cap-theorem]]); strong security increases latency
- Derived from business context in [[system-design-template]] step 3
- The "-ilities": availability, scalability, reliability, maintainability, testability, deployability, security, observability, performance
- Architecture is primarily shaped by quality attribute priorities, not features
- Each attribute should have a stimulus-response scenario: "When 10K concurrent users hit the system, response time stays under 500ms"

## Patterns

### Key quality attributes with metrics

| Attribute | Metric | Example Target |
|-----------|--------|----------------|
| Availability | Uptime % | 99.95% = 4.38h downtime/year |
| Latency | p50, p95, p99 | p99 < 200ms |
| Throughput | RPS, TPS | 50K RPS sustained |
| Durability | Data loss probability | 99.999999999% (11 nines, S3) |
| Scalability | Max load before degradation | Linear to 100 nodes |
| Consistency | Model type | Strong for payments, eventual for feeds |
| Security | Compliance standard | PCI DSS, SOC2, GDPR |

### Availability math

```
Availability = MTBF / (MTBF + MTTR)

Nines  | Downtime/year | Downtime/month
99%    | 3.65 days     | 7.31 hours
99.9%  | 8.77 hours    | 43.8 minutes
99.95% | 4.38 hours    | 21.9 minutes
99.99% | 52.6 minutes  | 4.38 minutes
99.999%| 5.26 minutes  | 26.3 seconds

Serial: A_total = A1 * A2 * A3
  3 components at 99.9% = 99.7%

Parallel: A_total = 1 - (1-A1)*(1-A2)
  2 instances at 99.9% = 99.9999%
```

### Availability depends on definition

The critical question is: "What constitutes an available response?"

```
Scenario: Service aggregates data from 3 sources
  Source A: required fields (core data)
  Source B: optional enrichment
  Source C: analytics metadata

Options:
  1. Available = returns 200 with ALL fields -> low availability
  2. Available = returns 200 with required fields only -> high availability
  3. Available = returns any 200, even empty -> meaningless metric

Decision: Define per business context. Different endpoints may
have different availability definitions.
```

### Universal Scalability Law (USL)

```
C(N) = N / (1 + sigma*(N-1) + kappa*N*(N-1))

sigma = contention coefficient (serialization)
kappa = crosstalk coefficient (coherence/coordination)

When kappa > 0: throughput DECREASES after optimal N
  -> Adding more nodes makes system SLOWER
  -> Must reduce coordination between nodes
```

## Gotchas

- **Symptom**: System meets SLA on average but customers complain -> **Cause**: Measuring p50 instead of p99; tail latency affects real users -> **Fix**: Always track p95/p99, optimize for worst case, not average
- **Symptom**: Adding more instances does not improve throughput -> **Cause**: USL contention (sigma) or crosstalk (kappa) dominating -> **Fix**: Identify serialization points (shared locks, single DB writer) and coordination overhead (distributed cache invalidation)
- **Symptom**: 99.9% availability component behind 99.9% load balancer -> **Cause**: Serial availability multiplication: 0.999 * 0.999 = 0.998 -> **Fix**: Account for all components in chain; redundancy at each layer

## See Also

- [[cap-theorem]] - Consistency vs availability tradeoff
- [[system-design-template]] - Quality attributes are step 3
- [[distributed-system-patterns]] - Patterns that address specific quality attributes
- Book: "Software Architecture in Practice" (Bass, Clements, Kazman) - Quality Attribute Scenarios
- Book: "High Performance MySQL" (Baron Schwartz) - USL applied to databases
- Microsoft: [Quality Attributes](https://learn.microsoft.com/en-us/azure/architecture/guide/pillars)
