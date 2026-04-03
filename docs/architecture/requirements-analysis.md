---
title: Requirements Analysis for Solution Architecture
category: concepts
tags: [architecture, requirements, nfr, asr, stakeholders, trade-offs]
---

# Requirements Analysis for Solution Architecture

Requirements analysis is the foundation of solution architecture - the process of understanding business needs, identifying stakeholders, eliciting functional and non-functional requirements, and extracting architecturally significant requirements that drive design decisions.

## Starting Point: Business Architecture

Everything begins with understanding the organization's business architecture:

1. **Business Strategy** - key goals, priorities, strategic documents
2. **Business Model** - how the company creates, delivers, and earns value
3. **Organizational Structure** - hierarchy, roles, responsibilities
4. **Business Processes** - operational workflows, bottlenecks
5. **Information Architecture** - data organization, management, integration
6. **Systems and Technologies** - current tech stack, infrastructure

Solution architecture is an expression of business architecture through technology. Learn it progressively as the project develops.

## Stakeholder Identification

Stakeholders are people/groups who influence or are influenced by the project.

**Common stakeholders:**
- **Business sponsors** - define business requirements and expected outcomes
- **End users** - will directly use the solution
- **Developers and testers** - build and validate; understand technical constraints
- **Support and operations** - long-term maintenance; views on scalability, reliability
- **Security department** - must approve before production release
- **Call center/support staff** - need documentation to support users

**How to identify:** brainstorming, stakeholder mapping, influence/interest analysis. Involve early to build trust.

## Three Key Questions

1. **WHY is this solution being created?** - Business requirements, goals, expected value. Avoid unnecessary duplication (check existing IT landscape). Understand business value (financial impact, efficiency gains).

2. **WHO will use it?** - Identify all user groups (not just "customers" but also support staff, admins, security, partner developers).

3. **HOW will they use it?** - Usage scenarios as the foundation of design.

**Principle: Do NOT invent answers.** Actively interact with stakeholders. You are a researcher at this stage.

## Non-Functional Requirements (NFRs)

Without NFRs, you build a system that crashes, loses data, or responds once per hour. NFRs define HOW the system works, not WHAT it does.

| Category | What to Define |
|----------|---------------|
| **Performance** | Response time targets (e.g., < 3 seconds at P95) |
| **Availability** | Uptime requirements (e.g., 99.9% SLA) |
| **Scalability** | Growth handling (e.g., support 10x user increase) |
| **Security** | Data protection, authentication, compliance |
| **Reliability** | Fault tolerance, data durability |
| **Maintainability** | Ease of updates, monitoring, debugging |

### Load Estimation

Always quantify NFRs with numbers:
- Expected concurrent users
- Requests per second (RPS)
- Data volume and growth rate
- Peak vs. average load
- Response time at P95/P99

## Architecturally Significant Requirements (ASR)

ASRs are requirements that directly influence architectural decisions.

### Functional Requirements as ASRs

Not all functional requirements are architecturally significant. Signs of ASR:
- Introduces **new integration** into the system
- Requires **new user interaction pattern**
- Appears **complex** with no trivially simple implementation

Missing a functional ASR usually doesn't require full rebuild - typically solved by adding a new service.

### Non-Functional Requirements as ASRs

**ALL NFRs are architecturally significant** because they influence:
- Infrastructure choice (performance/availability -> cloud with auto-scaling)
- Architectural patterns (modularity -> microservices)
- Technology selection (real-time big data -> streaming technologies)
- Solution cost (security -> additional investment; performance -> more hardware)

## Trade-off Resolution

### Resolution Approaches

1. **Prioritize with stakeholders** - determine which characteristic matters more
2. **Find middle ground** - solution that partially satisfies both sides

### Common Trade-offs

| Trade-off | Example Resolution |
|-----------|-------------------|
| Performance vs. Cost | Start with affordable infrastructure; upgrade later |
| Security vs. Usability | Match auth complexity to actual risk level |
| Scalability vs. Complexity | Start monolith, design for future microservices |
| Availability vs. Cost | Accept 99.9% instead of 99.999% |
| Features vs. Time-to-market | MVP with core features, iterate |

Always document: what trade-off was identified, what decision was made, why, and what was sacrificed.

## Process Summary

```
Business Architecture Study
    -> Stakeholder Identification
        -> Requirements Elicitation (WHY, WHO, HOW)
            -> NFR Definition (quantified with numbers)
                -> ASR Extraction
                    -> Trade-off Identification
                        -> Trade-off Resolution
                            -> Ready for Solution Design
```

Each stage feeds the next. Skipping or rushing the requirements phase is the #1 cause of project failure.

## Gotchas

- Clients describe current state (AS-IS) mixed with desired state (TO-BE) - architect must separate them
- "Why does the business invest in this product?" must be answered before diving into features
- Missing non-functional requirements is worse than missing functional ones - NFRs shape architecture
- Presenting only one option to stakeholders; always offer 2-3 alternatives

## See Also

- [[software-architecture-fundamentals]] - architecture types and principles
- [[architecture-documentation]] - documenting decisions with ADR
- [[system-design-interviews]] - applying requirements gathering under pressure
- [[reliability-fault-tolerance]] - availability, MTTF, MTTR, RTO, RPO metrics
