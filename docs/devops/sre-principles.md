---
title: SRE Principles and Culture
category: concepts
tags: [devops, sre, reliability, error-budget, toil, culture, blameless]
---

# SRE Principles and Culture

Site Reliability Engineering (SRE) is a set of engineering techniques for building and maintaining reliable systems. Originated at Google (2003, Ben Treynor). "SRE is what happens when a software engineer is tasked with what used to be called operations."

## SRE vs DevOps

- **DevOps** defines WHAT should be done (cultural movement, broad practices)
- **SRE** defines HOW to implement reliability (prescriptive, engineering-focused)
- SRE implements DevOps principles. SRE includes coding: 50% operations, 50% engineering projects

## Key Principles

1. **Operations is a software problem** - solve with engineering
2. **Manage by SLOs** - not "maximum reliability"
3. **Error budgets** - quantified acceptable unreliability
4. **Toil reduction** - automate repetitive manual work
5. **Shared ownership** - SREs co-own production with developers
6. **Blame-free postmortems** - focus on systemic fixes

## Culture Pillars

### Engineering Culture
- Free exchange of ideas. No organizational consequences for problems (if SLO maintained)
- "Everyone in the same boat" - shared responsibility
- Blameless: blame is neurophysiological - build culture that overcomes it

### Measure Everything (Observability)
- Know your system: where to look, what's happening, quickly
- Simple-sounding but complex and expensive to implement

### Blameless Postmortems
- Finding blame is counterproductive
- Open culture for discussing problems when they arise

### Incident Management
- Failures always happen. Runbooks, escalation ladders, classification
- Well-classified incidents with known procedures lead to self-healing systems
- Simplest example: health checks with auto-restart

## Key Metrics

| Metric | Description |
|--------|-------------|
| Deploy Frequency | How often new code ships. Decreasing = pipeline problem |
| MTTC | Mean Time To Commit - commit to production |
| Change Failure Rate | Proportion of changes causing failure |
| MTTA | Mean Time To Acknowledge (~5 min industry standard) |
| MTTR | Mean Time To Resolve (~1 hour industry standard) |

## Error Budget

`100% - SLO = error budget`

- SLO 99.9% = 0.1% budget = 43.2 min/month
- Budget exhausted -> freeze feature releases, focus on reliability
- Budget remaining -> deploy faster, take more risks
- Error budget burn rate tracks consumption speed
- Error budget policy defines actions at thresholds

## Toil

Repetitive manual work that can be automated. Characteristics: manual, automatable, tactical, no enduring value, scales linearly with growth.

`Toil / All tasks` = toil ratio. Target: below 50%.

### Automation Maturity Levels

1. **No automation** - fully manual
2. **System-specific scripts** - individual admins
3. **Generic shared automation** - shared tools
4. **Built-in automation** - system self-manages
5. **Autonomous systems** - self-healing, self-scaling

## SRE Team Models

| Model | Description |
|-------|-------------|
| **Infrastructure SRE** | Shared platform team. Unified approach. Risk: disconnected from product |
| **Product SRE** | Embedded with product team. Deep knowledge. Risk: siloed practices |
| **Consulting SRE** | Temporary engagement. Helps teams improve. Moves on when SLO met |

### When SRE Is NOT Needed

- Service already works well
- Service is unimportant
- Service is legacy being decommissioned

## Anti-patterns

- "SRE solves all problems" - SRE is techniques; people solve problems
- "SRE is a silver bullet" - works only with certain systems at certain lifecycle stages
- "SRE is part of DevOps team" - goals differ, subordination is problematic
- Launching SRE without commitment from ALL departments

## Gotchas

- Excessive reliability is wasteful - SRE ensures "reliable enough" for business
- SRE requires commitment from all departments, not just engineering
- Know-Do-Learn cycles: constant change is the new reality

## See Also

- [[monitoring-and-observability]] - SLI/SLO/SLA measurement
- [[sre-incident-management]] - on-call, postmortems, escalation
- [[deployment-strategies]] - release management and error budgets
- [[chaos-engineering-and-testing]] - reliability testing
- [[sre-automation-and-toil]] - automation tools and practices
