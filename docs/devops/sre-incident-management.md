---
title: SRE Incident Management
category: concepts
tags: [devops, sre, on-call, postmortems, incident-response, escalation]
---

# SRE Incident Management

Incident management covers on-call structure, escalation, mitigation, and blameless postmortems. The goal is to minimize MTTR while maintaining sustainable on-call practices.

## On-Call Structure

- Primary + secondary rotation
- Duration: 1-2 weeks typical
- Maximum: 2 incidents per 12-hour shift (sustainable pace)
- Follow-the-sun for global teams
- Tools: PagerDuty, Opsgenie, VictorOps

## On-Call Responsibilities

1. **Acknowledge** alert within SLA (e.g., 5 min for P1)
2. **Triage** - assess severity, determine escalation need
3. **Mitigate** - reduce user impact (not root cause yet)
4. **Communicate** - update status page, notify stakeholders
5. **Resolve** - full remediation
6. **Handoff** - document for next shift, file postmortem

## Essential On-Call Knowledge

1. **Reading traces** - how to debug distributed systems
2. **Fallback switching** - existing fallback mechanisms, manual procedures
3. **Deploy rollback** - rolling back bad deploys and configurations
4. **Rate limiting** - handling malicious DoS and accidental self-DoS
5. **Impact limitation** - containing broken parts' impact on whole system

**Key principle**: primary cause of all problems is someone misconfigured something. Deploy and configuration rollback must be documented and practiced.

## Escalation

| Severity | Response Time | Action |
|----------|---------------|--------|
| P1 (service down) | Page immediately | War room within 15 min |
| P2 (degraded) | Page, 30 min | Focused investigation |
| P3 (minor impact) | Ticket | Next business day |

When in doubt, escalate.

## Key Incident Roles

### IMOC (Incident Manager On-Call)

- Leads and coordinates SEV resolution
- Focused on TTR (time to recovery), target: SEV-0 in 15 min
- Single point of accountability
- Keeps team calm, manages communication to leadership
- Engineers focus on technical work, report status to IMOC

### TLOC (Technical Lead On-Call)

- Technical expert for diagnosis and mitigation
- Reports status to IMOC
- After SEV: works on root cause, leads chaos experiments

## Postmortems

### Principles

1. **Blame-free** - "what about the system made the error possible?"
2. **Written document** - permanent, shared record
3. **Action items with owners** - assigned, tracked, prioritized
4. **Shared broadly** - organization-wide learning

### Template

```markdown
## Incident: [Title]
**Date**: YYYY-MM-DD | **Severity**: P1 | **Duration**: 2h 15m

## Summary
2-3 sentences of what happened.

## Impact
- Users affected: X
- Revenue impact: $Y
- SLO burn: Z%

## Timeline
- HH:MM - Alert fired
- HH:MM - On-call acknowledged
- HH:MM - Root cause identified
- HH:MM - Mitigation applied
- HH:MM - Full resolution

## Root Cause Analysis (5 Whys)
1. Why did the service fail? -> OOM kill
2. Why was memory exhausted? -> Memory leak in handler
...

## What Went Well
- Detection was fast (< 2 min)
- Runbook was accurate

## What Went Wrong
- Monitoring gap: no alert on memory trend
- Rollback took 20 min (should be < 5)

## Action Items
| Action | Owner | Priority | Deadline | Status |
|--------|-------|----------|----------|--------|
| Add memory trend alert | @eng | P1 | 2026-04-10 | TODO |
| Automate rollback | @sre | P2 | 2026-04-17 | TODO |

## Lessons Learned
```

### Trigger Criteria

Write postmortem when: user-visible impact, error budget consumed, data loss, manual intervention required, monitoring gap discovered, on-call escalation.

## Diagnostics Methodology

1. **Observe** - what symptoms? When started? What changed?
2. **Hypothesize** - possible causes based on symptoms
3. **Test** - verify or eliminate with data
4. **Fix** - apply remediation
5. **Prevent** - add monitoring, tests, automation

### Common Debugging Dimensions

- **Time correlation**: deploy? Config change? Traffic pattern?
- **Scope**: one host? One AZ? One service? All users or some?
- **Dependency graph**: upstream/downstream services?
- **Resource exhaustion**: CPU, memory, disk, file descriptors, connections?

### Tools Hierarchy

Dashboards (Grafana) -> Logs (Loki/ELK) -> Traces (Jaeger/Tempo) -> Profiling (pprof) -> Core dumps. Start broad, narrow down.

## Knowledge Sharing

- Document diagnostic procedures
- Shadow on-call for training
- Wheel of Misfortune (simulated incidents)
- Game days (planned reliability exercises)

## Gotchas

- Postmortem without follow-through on action items is worthless
- Timeline reconstruction is critical - exactly when each event occurred
- Runbooks must be kept updated after each incident
- "One person knows how to switch" is a critical risk - document and cross-train
- Incident coordinator communicates status, does NOT debug

## See Also

- [[sre-principles]] - SRE culture and error budgets
- [[monitoring-and-observability]] - alerting and SLI/SLO
- [[chaos-engineering-and-testing]] - proactive reliability testing
- [[deployment-strategies]] - rollback strategies
