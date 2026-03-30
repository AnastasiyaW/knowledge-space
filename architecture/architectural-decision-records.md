---
title: Architectural Decision Records (ADR)
category: patterns
tags: [documentation, architecture, decision-making, c4-model]
---
# Architectural Decision Records (ADR)

An ADR is a lightweight document capturing an architectural decision: the context, the decision itself, the alternatives considered, and the consequences. Part of a broader architecture documentation strategy.

## Key Facts

- ADRs are immutable once accepted - superseded ADRs link to their replacement, not edited
- Each ADR answers: What did we decide? Why? What alternatives did we reject? What are the consequences?
- ADRs complement diagrams (C4, UML) - diagrams show structure, ADRs explain WHY that structure
- Tool choices in [[system-design-template]] step 6 should be documented as ADRs
- C4 model provides 4 zoom levels: Context -> Container -> Component -> Code
- For drawing diagrams, clarity matters more than notation compliance - any readable format works during design phase
- Architecture documentation should include: diagrams, ADRs/RFCs, tables (comparison matrices), checklists, and optionally code (ArchUnit tests)

## Patterns

### ADR template (Michael Nygard format)

```markdown
# ADR-001: Use PostgreSQL for Order Service

## Status
Accepted (2024-03-15)

## Context
Order service needs ACID transactions for financial data.
Expected load: 5K TPS writes, 20K TPS reads.
Team has strong PostgreSQL expertise.

## Decision
Use PostgreSQL 16 with logical replication for read replicas.

## Alternatives Considered
1. MySQL 8 - comparable features but weaker JSON support
2. CockroachDB - better horizontal scaling but operational
   complexity exceeds team capacity
3. DynamoDB - no ACID across items, poor for relational data

## Consequences
+ ACID compliance for order lifecycle
+ Team expertise reduces time-to-market
+ Rich ecosystem (pg_stat, pgBouncer, Patroni)
- Vertical scaling limits (~500K TPS on single node)
- Will need sharding strategy if >100M orders
- Vendor-neutral but requires DBA expertise
```

### Comparison table pattern (for step 6 justification)

```
                  | PostgreSQL | Cassandra | DynamoDB
------------------+------------+-----------+----------
Consistency       | Strong     | Tunable   | Eventual*
Max write TPS     | 500K       | 1M+       | Unlimited
Operational cost  | Medium     | High      | Low (managed)
Team expertise    | HIGH       | Low       | Medium
Cost at 10TB      | $$         | $$$       | $$$$
Horizontal scale  | Limited    | Excellent | Excellent
```

Weight criteria by priority from [[quality-attributes]]:
consistency (critical) > team expertise (high) > cost (medium) > scale (low for current needs)

### C4 model zoom levels

```
Level 1: System Context
  [User] --> [Our System] --> [External System]
  Who uses the system? What external systems does it talk to?

Level 2: Container
  [Web App] --> [API Service] --> [Database]
  What deployable units exist? How do they communicate?

Level 3: Component
  [OrderController] --> [OrderService] --> [OrderRepository]
  What major components exist inside a container?

Level 4: Code (optional)
  Class diagrams, sequence diagrams for critical flows
```

## Gotchas

- **Symptom**: ADR says "chose X because it's the best" -> **Cause**: Missing comparison with alternatives -> **Fix**: Every ADR MUST include at least 2 alternatives with pros/cons. "I like it" is not a valid justification
- **Symptom**: Architecture diagrams become outdated within months -> **Cause**: Diagrams maintained separately from code -> **Fix**: Consider diagrams-as-code (PlantUML, Mermaid, Structurizr DSL) stored in repo alongside code
- **Symptom**: Spending too much time on formal notation (UML, ArchiMate) -> **Cause**: Notation compliance over communication -> **Fix**: Use whatever notation communicates clearly. Miro boards with boxes and arrows are fine for design phase; formalize later if needed

## See Also

- [[system-design-template]] - ADRs document decisions made in steps 4-6
- [[quality-attributes]] - Quality attributes drive the decisions ADRs capture
- [[microservices-vs-monolith]] - Classic ADR topic: architecture style selection
- Michael Nygard: [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Simon Brown: [The C4 Model](https://c4model.com/)
- Martin Fowler: [Architecture Decision Record](https://martinfowler.com/articles/architecture-decision-records.html)
