---
title: System Design Interviews and Practice
category: reference
tags: [system-design, interview, estimation, architecture, practice]
---

# System Design Interviews and Practice

Structured approach to system design problems, whether in interviews or real architecture work. The same methodology applies to both.

## 7-Step Process

1. **Clarify requirements** - ask questions, don't assume
2. **Define scope and boundaries** - what's in, what's out
3. **Identify key entities and relationships** - data model
4. **Design high-level architecture** - components and interactions
5. **Deep dive into critical components** - the hardest parts
6. **Address cross-cutting concerns** - security, monitoring, fault tolerance
7. **Discuss trade-offs and alternatives** - always explain WHY

## Common Mistakes

- Jumping to solution before understanding requirements
- Ignoring non-functional requirements
- Not considering failure scenarios
- Over-engineering for unlikely scale
- Presenting only one option without alternatives
- Missing NFR calculations (no numbers for load, storage, latency)
- Not explaining WHY a technology was chosen

## NFR Estimation Tables

For each system, build Year 1-5 projections:
- DAU, peak concurrent users
- Requests per second (RPS)
- Data volume and growth rate
- Storage needs
- Color code: green (manageable), yellow (attention), red (challenge)

## Performance Reference Numbers

| Operation | Latency |
|-----------|---------|
| Memory reference | ~100 ns |
| SSD read | ~100 us |
| Network roundtrip (same DC) | ~500 us |
| Distributed cache (Redis) | ~1 ms |
| Simple DB query | ~1-10 ms |
| Cross-region network | ~50-150 ms |

## Three-Option Rule

For every decision, present minimum 3 approaches:
- Even if two are obviously wrong, articulate WHY they're bad
- Train communicating to non-technical stakeholders
- Creates informed decision-making

## Practice: URL Shortener

**Requirements:** shorten URLs, redirect, track statistics. <100ms latency, 99.9% availability, 10K+ RPS.

**Architecture:**
- Redis for hot URL mappings, PostgreSQL for metadata
- ClickHouse for analytics/aggregations
- Horizontal scaling of stateless redirect service
- Base62 encoding for short IDs

## Practice: Notification Service

**Requirements:** multi-channel (SMS, email, push, messengers), provider integration, history, analytics, templates, A/B testing.

**Architecture:**
- Kafka for reliability and buffering
- Channel abstraction layer for provider independence
- Priority system for different notification types
- Template engine with variable substitution

## Documenting for Non-Technical Stakeholders

1. **Explain the obvious** - what engineers know isn't obvious to managers
2. **Show reasoning chain** - how you arrived at the conclusion
3. **Identify branching points** - where reasoning could differ
4. **Quantify trade-offs** - cost, time, risk for each option
5. **Use comparison tables** - side-by-side with criteria

## Hot/Cold Storage Pattern

- **Hot:** Recent data (3-6 months) on fast storage (SSD, in-memory)
- **Cold:** Old data on cheap storage (S3, HDD)
- 999/1000 requests hit hot data; cold access is slow but rare

### Dictionary/Normalization for Analytics
Replace repeated strings with integer IDs:
- Browser version string (50-100 bytes) -> 2-byte integer
- 25-50x storage reduction
- Apply dictionary at query boundaries (decode at input, encode at output)

## Gotchas

- **Requirements gathering is most underrated** - most candidates and projects fail here
- **"Simplest solution that meets requirements wins"** - don't over-engineer
- **Always quantify** - "high load" means nothing. "10K RPS with <100ms P99" means everything
- **Clients describe AS-IS mixed with TO-BE** - separate current state from desired state
- **Keep old API versions longer than expected** - some clients call APIs once per year

## See Also

- [[solution-architecture-process]] - Full requirements pipeline
- [[architecture-documentation]] - C4, ADR, 4+1 views
- [[database-selection]] - Choosing databases
- [[quality-attributes-reliability]] - SLA, availability math
