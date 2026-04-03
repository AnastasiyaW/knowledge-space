---
title: Architecture Documentation
category: concepts
tags: [architecture, documentation, c4-model, adr, uml, diagrams]
---

# Architecture Documentation

Architecture documentation should be pragmatic, not exhaustive. The Agile Manifesto says working software over comprehensive documentation - but documentation is still valuable. Focus on what helps teams make decisions and understand the system.

## Documentation Methods

- **Diagrams** - free-form (flexible, needs legend) or formal notations (UML, ArchiMate, C4, BPMN)
- **ADRs** - Architecture Decision Records, RFCs
- **Tables** - structured comparison of options
- **Code** - ArchUnit for automated architecture compliance testing
- **Checklists** - validation criteria

## Minimum Viable Architecture Document

If no organizational standard exists, document at minimum:

1. **Key architectural decisions and principles** - decisions shaping overall structure
2. **Important components and their interactions** - data and work flow through the system
3. **Technology choices with rationale** - why each tool was selected
4. **Data schemas and relationships** - data models, entity relationships

## 4+1 Architectural View Model (Kruchten)

| View | Shows | Diagrams |
|------|-------|----------|
| **Logical** | Functionality for end users | Class, sequence diagrams |
| **Process** | Concurrency, synchronization, performance | Activity, state diagrams |
| **Component** | Software structure for developers | Component, package diagrams |
| **Physical** | Infrastructure and hardware | Deployment diagrams |
| **Scenarios (+1)** | Use cases tying all views together | Use case diagrams |

Each scenario traces through the other four views, validating the architecture.

## C4 Model

Pragmatic alternative to full UML with four levels of abstraction:

### Level 1: System Context
Highest level. System as a box surrounded by users and external systems. Answers: what is the system, who uses it, what does it integrate with?

### Level 2: Container
Zooms into the system. Shows applications, databases, message brokers, file systems. Each container is a separately deployable unit.

### Level 3: Component
Zooms into a container. Shows internal components (controllers, services, repositories) and interactions.

### Level 4: Code
Class-level diagrams. Rarely drawn by architects - auto-generated or for critical modules only.

## Architecture Decision Records (ADR)

Lightweight documentation of individual decisions:

```markdown
# ADR-001: Use PostgreSQL for primary data storage

## Status: Accepted
## Date: 2024-01-15

## Context
We need a database for our order processing service.

## Decision
Use PostgreSQL 15.

## Rationale
- Team expertise in PostgreSQL
- ACID compliance required for financial data
- JSON support covers semi-structured data needs
- Cost-effective

## Alternatives Considered
- MongoDB: rejected due to ACID requirements
- MySQL: rejected due to limited JSON support

## Consequences
- Need DBA expertise for optimization
- Must plan for read replicas as load grows
```

## UML Diagrams for Architects

### Structural (most used)
- **Component Diagram** - system components and interfaces
- **Deployment Diagram** - physical infrastructure mapping

### Behavioral (most used)
- **Sequence Diagram** - interaction between components over time (critical for API design)
- **Activity Diagram** - workflow/process flow across systems

## Attribute-Driven Design (ADD)

Iterative design process from CMU SEI:

1. **Ensure requirements gathered** - use cases, constraints, quality attribute scenarios
2. **Select element to elaborate** - entire system or specific module
3. **Identify architecture driver** - use utility tree to prioritize (High/Medium business importance x technical difficulty)
4. **Choose design concept** - patterns, tactics, reference architectures, frameworks, COTS
5. **Instantiate elements and assign responsibilities**
6. **Define interfaces** - contracts between elements
7. **Verify and refine** - check decomposition satisfies drivers

**Termination:** when critical risks are mitigated, all drivers addressed, or allocated design time expires.

## Documentation Delivery Sequence

1. Architecture overview - system context and component diagrams
2. API specifications - OpenAPI for REST, WSDL for SOAP, AsyncAPI for event-driven
3. Data model documentation - ER diagrams, schema definitions
4. Integration specifications - external service connections
5. Deployment guide - infrastructure requirements, configuration
6. Runbook - operational procedures, monitoring, incident response

## Architectural Principles to Establish

1. **Separation of Concerns** - each component has bounded responsibility
2. **DRY** - single source of truth for data and logic
3. **KISS** - simplest solution meeting requirements
4. **YAGNI** - don't build what you don't need yet
5. **Fail Fast** - detect and report errors immediately
6. **Design for Failure** - assume components will fail
7. **Configuration over Code** - externalize environment-specific settings
8. **API First** - design interfaces before implementation

## Gotchas

- **Don't choose frameworks based on trends** - consider team knowledge, learning curve, product maturity, license types
- **Design in isolation** may produce solutions that poorly support critical quality attributes
- **Feature matrix helps** - map decisions to quality attributes when evaluating alternatives
- **Quality attributes conflict** - improving one may degrade another; document the trade-off
- **Full SAD documents** can be book-length - ask about existing documentation standards first

## See Also

- [[solution-architecture-process]] - Requirements gathering and trade-off resolution
- [[api-documentation-specs]] - OpenAPI, WSDL, AsyncAPI, OpenRPC specifications
- [[architectural-styles]] - Monolith to microservices spectrum
