---
title: Solution Architecture Process
category: concepts
tags: [architecture, requirements, stakeholders, trade-offs, process]
---

# Solution Architecture Process

Solution architecture bridges business needs and technology implementation. The architect's process spans from requirements gathering through deployment, focusing on finding and resolving trade-offs. Over 60% of success depends on soft skills - solutions are created for people by people.

## Architecture Levels and Roles

| Level | Scope | Focus |
|-------|-------|-------|
| **Enterprise Architecture** | Entire organization | Business strategy, global processes |
| **Solution Architecture** | Specific business problem | Business-tech intersection, system integration |
| **System/Technical Architecture** | Specific system | Modules, code, atomic processes |

| Role | Scope | Primary Activity |
|------|-------|-----------------|
| Senior Engineer | Own tasks/module | Development |
| Tech Lead | Team-wide | Development + some design |
| Solution Architect | Multiple teams | Design + business alignment |

In smaller organizations, one person fills multiple roles. Authority is earned through demonstrated expertise, not title.

## Requirements Pipeline

```php
Business Architecture Study
  -> Stakeholder Identification
    -> Requirements Elicitation (WHY, WHO, HOW)
      -> NFR Definition (quantified with numbers)
        -> ASR Extraction
          -> Trade-off Identification
            -> Trade-off Resolution
              -> Ready for Solution Design
```

### Three Key Questions

1. **WHY** is this solution being created? - Business requirements, goals, expected value
2. **WHO** will use it? - All user groups (customers, support staff, admins, partners, security)
3. **HOW** will they use it? - Usage scenarios as the foundation of design

**Principle:** Do NOT invent answers. Actively interact with stakeholders. You are a researcher at this stage.

### Stakeholder Identification

Common stakeholders: business sponsors, end users, developers/testers, support/operations, security department, call center staff. Involve early to build trust. Use brainstorming, stakeholder mapping, influence/interest analysis.

## Non-Functional Requirements (NFRs)

Without NFRs, you build a system that crashes, loses data, or responds once per hour. Always quantify with numbers.

| Category | What to Define | Example |
|----------|---------------|---------|
| **Performance** | Response time targets | Chatbot responds < 3 seconds |
| **Availability** | Uptime requirements | 99.9% SLA |
| **Scalability** | Growth handling | Support 10x user increase |
| **Security** | Data protection, compliance | Personal data law compliance |
| **Reliability** | Fault tolerance, durability | Data survives failures |
| **Maintainability** | Ease of updates, debugging | Monitoring, structured logging |

### Load Estimation Checklist

- Expected concurrent users
- Requests per second (RPS)
- Data volume and growth rate
- Peak vs. average load ratio
- Response time at P95/P99

## Architecturally Significant Requirements (ASRs)

Signs of a functional ASR:
- Introduces **new integration** into the system
- Requires **new user interaction pattern**
- Appears **complex** with no trivially simple implementation

**ALL NFRs are architecturally significant** - they influence infrastructure choice, architectural patterns, technology selection, and solution cost.

## Architectural Trade-offs

**Core principle: Architecture is the art and science of finding and resolving trade-offs.** No perfect solutions exist - only trade-offs resolved in one direction or another.

| Trade-off | Example Resolution |
|-----------|-------------------|
| Performance vs. Cost | Start affordable, upgrade later |
| Security vs. Usability | Skip full auth for chatbot; require only name + email |
| Scalability vs. Complexity | Start monolith, design for future microservices |
| Availability vs. Cost | Accept 99.9% instead of 99.999% |
| Features vs. Time-to-market | MVP with core features, iterate later |

### Resolution Approaches

1. **Prioritize with stakeholders** - determine which characteristic matters more
2. **Find middle ground** - partially satisfy both sides

Always document: what trade-off was identified, what decision was made, why, and what was sacrificed.

## Data Volume Reference Points

| Range | Classification | Implications |
|-------|---------------|-------------|
| < 100 GB | Small | Single machine, minimal complexity |
| < 2 TB | Moderate | Single large machine, managed services |
| < 10-50 TB | Significant | Multiple machines, careful planning |
| < 1 PB | Large | Dynamic scaling, significant effort |
| > 100 PB | Extreme | Disk replacement becomes routine |

## Gotchas

- **Skipping requirements phase** is the #1 cause of project failure - each stage feeds the next
- **Clients describe AS-IS mixed with TO-BE** - architect must separate these and ask "Why does the business invest?"
- **Missing a functional ASR** usually doesn't require full rebuild - typically solved by adding a new service
- **Ticket titles without descriptions** - modern teams expect engineers to investigate requirements autonomously
- **Three-option rule** - always present minimum 3 approaches for every decision, even if two are obviously wrong

## See Also

- [[architecture-documentation]] - C4 model, ADRs, 4+1 views
- [[architectural-styles]] - Monolith to microservices spectrum
- [[quality-attributes-reliability]] - Availability, fault tolerance, recoverability metrics
- [[database-selection]] - Choosing databases by data type and requirements
