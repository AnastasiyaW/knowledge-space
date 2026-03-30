---
title: Incident Management & On-Call
category: operations
tags: [incident, on-call, postmortem, blameless, escalation, runbook, severity]
---
# Incident Management & On-Call

Incident response lifecycle, on-call practices, severity levels, and blameless postmortems.

## Key Facts

- **Incident** = unplanned event that degrades or disrupts service; requires coordinated response
- **Severity levels**: SEV1 (total outage, user-impacting), SEV2 (partial outage), SEV3 (degraded), SEV4 (minor)
- **IMOC** (Incident Manager On-Call) = coordinates response, makes decisions, communicates status
- **TLOC** (Tech Lead On-Call) = technical expert who diagnoses, mitigates, and resolves
- **On-call rotation** = engineers take turns being first responder; typically weekly rotation
- **Runbook** = documented step-by-step procedures for known incidents; reduces MTTR
- **Blameless postmortem** = after-incident review focusing on systems, not individuals; find root cause
- **MTTR** (Mean Time To Recovery) = key metric; target: minimize through automation and runbooks
- **MTTA** (Mean Time To Acknowledge) = time from alert to human response
- Incident lifecycle: **Detect** -> **Respond** -> **Mitigate** -> **Resolve** -> **Learn**
- [[monitoring-observability]] provides detection through alerts
- [[sre-sli-slo-sla]] error budget depletion triggers incident response
- Communication channels: dedicated Slack/Teams channel per incident, status page updates
- Escalation policy: if not acked in X minutes, escalate to next person

## Patterns

```
# Incident Response Checklist
1. ACKNOWLEDGE
   - Ack alert within 5 minutes
   - Create incident channel (#inc-YYYYMMDD-brief)
   - Declare severity level

2. ASSESS
   - Impact: How many users? Which services?
   - Scope: Single service or cascading?
   - Check recent changes (deployments, config changes)

3. MITIGATE
   - Rollback recent deployment if related
   - Scale up resources if capacity issue
   - Failover to backup system
   - Communicate status to stakeholders

4. RESOLVE
   - Fix root cause (not just symptoms)
   - Verify fix with monitoring
   - Confirm user experience restored

5. LEARN
   - Schedule postmortem within 48 hours
   - Document timeline, root cause, action items
   - Share findings broadly
```

```
# Postmortem Template
Title: [Service] [Impact] on [Date]
Severity: SEV-2
Duration: 45 minutes (14:23 - 15:08 UTC)

Summary: Brief description of what happened

Impact:
- X% of users affected
- Y requests failed
- Z revenue impact

Timeline:
- 14:20 - Deployment of v2.3.1 started
- 14:23 - Error rate alert fired
- 14:25 - On-call acknowledged
- 14:30 - Root cause identified (DB migration timeout)
- 14:35 - Rollback initiated
- 14:45 - Rollback complete, errors dropping
- 15:08 - Full recovery confirmed

Root Cause: Database migration locked table for > 30s, causing connection pool exhaustion

Contributing Factors:
- Migration not tested against production data volume
- No connection pool timeout configured
- Alert threshold too high (triggered after 3 minutes)

Action Items:
- [ ] Add migration testing with production-like data (Owner: Alice, Due: 2w)
- [ ] Configure connection pool timeouts (Owner: Bob, Due: 1w)
- [ ] Lower error rate alert threshold to 1% (Owner: Carol, Due: 3d)
- [ ] Add pre-deploy migration check to CI pipeline (Owner: Dave, Due: 2w)

Lessons Learned:
- What went well: Fast root cause identification, team coordination
- What went poorly: No automated rollback, slow alert
- Where we got lucky: Happened during business hours with full team available
```

```
# On-Call Best Practices
- Maximum on-call shift: 1 week; minimum team size for rotation: 4-6 people
- Compensation: extra pay, time off, or both for on-call duty
- Alert actionability: every alert must have a runbook link
- Noise budget: if >50% of alerts are false positives, fix alerts before fixing systems
- Handoff: end-of-shift handoff document with active issues and context
- Shadowing: new on-call engineers shadow experienced ones for 1-2 rotations
```

## Gotchas

- **Blame = silence**: if people fear blame, they hide information; blameless culture is essential
- Over-communicating during incident is better than under-communicating; silence breeds anxiety
- "Rollback first, investigate later" - mitigate impact before understanding root cause
- Multiple simultaneous incidents: assign separate incident commanders, don't mix channels
- Postmortem action items without owners and deadlines don't get done; track them in issue tracker
- Alert fatigue is a real safety hazard; too many alerts = all alerts get ignored
- On-call without runbooks = every incident is a fresh investigation; document as you go
- Knowledge transfer from incidents is the highest-ROI learning opportunity in engineering

## See Also

- [[monitoring-observability]] - alerting that triggers incident response
- [[sre-sli-slo-sla]] - error budgets and reliability targets
- [[deployment-strategies]] - rollback as incident mitigation
- [[microservices-architecture]] - cascading failures in distributed systems
- Google SRE - Managing Incidents: https://sre.google/sre-book/managing-incidents/
- PagerDuty incident response: https://response.pagerduty.com/
