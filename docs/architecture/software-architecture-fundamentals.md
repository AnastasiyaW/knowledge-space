---
title: Software Architecture Fundamentals
category: concepts
tags: [architecture, solution-architecture, enterprise-architecture, roles]
---

# Software Architecture Fundamentals

Software architecture is the sustainable foundation defining a system's overall structure, components, relationships, and interactions with its environment. It determines how parts work together to fulfill required functions while reducing complexity for both current use and future maintenance.

## Defining Architecture

Core definitions from practitioners:
- "Set of significant design decisions shaping the system, where significance is measured by the cost of change"
- "Framework on which the entire product is built - a plan showing where pieces go and how they connect"
- "Discipline allowing systems to survive in time and space, adapting to new requirements and environmental changes"

**Good architecture** provides: stability, performance, reliability, maintainability, ease of future modification. **Bad architecture** leads to: maintenance difficulties, scaling problems, performance issues, security vulnerabilities.

## Three Architecture Levels

| Level | Scope | Focus |
|-------|-------|-------|
| **Enterprise Architecture** | Organization-wide | Business strategy, global processes, more business than tech |
| **Solution Architecture** | Specific business problem | Individual systems/services, intersection of business and tech |
| **System/Technical Architecture** | Specific system | Modules, atomic processes, closest to code |

## Architect Roles

| Role | Focus |
|------|-------|
| Enterprise Architect | Organization strategy, business architecture |
| Solution Architect | Solution design, integration across systems |
| Technical Architect | Software design and development |
| Cloud Architect | Cloud strategy, migration |
| Data Architect | Data models, storage strategy |
| Security Architect | Security posture, threat modeling |
| Infrastructure Architect | Network, hardware, deployment |

In smaller organizations one person may fill multiple roles.

## Solution Architect Responsibilities

1. Identify and analyze business, functional, and user requirements
2. Define non-functional requirements and constraints
3. Extract architecturally significant requirements, find compromises with stakeholders
4. Design solution concept and document it
5. Approve solution with stakeholders
6. Communicate solution to technical teams
7. Participate in development, solving architectural questions
8. Ensure operability and maintenance after launch
9. Introduce architectural principles guiding development teams

Over 60% of success depends on soft skills, not technical knowledge. Architecture is an active social process.

## Architectural Style Evolution

1. **Monolith** - single deployment, tightly coupled
2. **Modular Monolith** - clear module boundaries within single deployment
3. **SOA** - services via enterprise bus
4. **Microservices** - independent services with own databases
5. **Microservices + Micro-Frontends** - independent UI pieces per service

## Key Architectural Principles

1. **Separation of Concerns** - each component has clear, bounded responsibility
2. **DRY** - single source of truth for data and logic
3. **KISS** - simplest solution that meets requirements
4. **YAGNI** - don't build what you don't need yet
5. **Fail Fast** - detect and report errors immediately
6. **Design for Failure** - assume components will fail; plan recovery
7. **Configuration over Code** - externalize environment-specific settings
8. **API First** - design interfaces before implementation

## Architectural Trade-offs

**Core principle: Architecture is the art and science of finding and resolving trade-offs.** There are no perfect solutions, only trade-offs resolved in one direction or another.

| Trade-off | Example Resolution |
|-----------|-------------------|
| Performance vs. Cost | Start affordable, upgrade later |
| Security vs. Usability | Match auth level to actual risk |
| Scalability vs. Complexity | Start monolith, design for future decomposition |
| Availability vs. Cost | Accept 99.9% instead of 99.999% |
| Features vs. Time-to-market | MVP with core features, iterate |

Always document: what trade-off was identified, what decision was made, why, and what was sacrificed.

## Gotchas

- Architecture design in isolation produces solutions that poorly support critical quality attributes - involve the team
- Choosing frameworks based on trends rather than team knowledge, learning curve, and product maturity
- Some quality attributes conflict - improving one may degrade another
- Skipping requirements phase is the #1 cause of project failure

## See Also

- [[requirements-analysis]] - requirements gathering and ASR extraction
- [[architecture-documentation]] - documenting decisions with ADR, C4, 4+1
- [[design-patterns-gof]] - GoF patterns and SOLID principles
- [[microservices-patterns]] - when to decompose into services
- [[tech-lead-role]] - career path from senior to architect
