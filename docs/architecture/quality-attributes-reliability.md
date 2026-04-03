---
title: Quality Attributes - Reliability and Fault Tolerance
category: concepts
tags: [reliability, availability, fault-tolerance, sla, chaos-engineering, recovery]
---

# Quality Attributes - Reliability and Fault Tolerance

Reliability = system operates correctly under specified conditions over time, including recovery from failures. Three pillars: availability, fault tolerance, recoverability.

## Availability

Percentage of time system is accessible. Uptime / total observation time.

| SLA | Downtime/Year | Classification |
|-----|--------------|----------------|
| 99.999% | ~5 min | Five nines (ideal) |
| 99.99% | ~52 min | Four nines |
| 99.9% | ~8.76 hours | Standard |
| 99% | ~3.65 days | Basic |
| 95% | ~18.25 days | Poor |

### Availability Tools

| Tool | Purpose |
|------|---------|
| **Auto-scaling** | Dynamically add/remove instances based on metrics |
| **Load balancer** | Distribute traffic across instances |
| **CDN** | Geographic distribution for static content |
| **Caching** | Reduce backend load |
| **Rate limiting** | Prevent overload |
| **Service discovery** | Auto-detect services (Consul, etcd, ZooKeeper) |
| **Health checks** | Active probes or passive heartbeats |
| **Connection pooling** | Reuse pre-established connections |
| **Hot standby** | Backup runs in sync, immediate failover |
| **Cold standby** | Backup off, needs startup time |

## Fault Tolerance

System continues operating during partial failures.

### Key Metrics

| Metric | Measures | Ideal | Normal | Poor |
|--------|----------|-------|--------|------|
| **MTTF** | Time between failures | 2 years | 6 months | 1 week |
| **MTTR** | Time to restore | 5 min | 30 min | 3 days |

### Fault Tolerance Patterns

**Failover:**
- **Active-Passive** - one active, standby waits
- **Active-Active** - all handle traffic simultaneously

**Bulkhead:** Isolate resources so one failure doesn't cascade. Thread-level or process-level isolation.

**Timeouts + Retries:** Exponential backoff with jitter to prevent thundering herd.

**Graceful Degradation:** Disable non-critical features. If recommendations service down, purchases still work.

**Chaos Engineering:** Intentionally inject failures. Netflix Chaos Monkey randomly kills production services to verify self-healing.

### Organizational Practices
- **Recovery plans** - pre-prepared scenarios, regularly tested
- **Post-mortem analysis** - timeline, root cause, actions taken, communication effectiveness

## Recoverability

Ability to return to operational state after failure.

### Key Metrics

| Metric | Measures | Ideal | Normal | Poor |
|--------|----------|-------|--------|------|
| **RTO** | Max acceptable downtime | 5 min | 1 hour | 3 days |
| **RPO** | Max acceptable data loss | 1 min | 15 min | 1 day |

### Recovery Tools

- **Automated recovery** - scripts + orchestration (Kubernetes auto-restarts)
- **Rollback** - quickly revert to previous stable version
- **Database rollback** - transaction rollback mechanisms
- **Configuration management** - Ansible for config versioning

**Key principle:** preparation is everything. Pre-create scripts and scenarios for fast recovery.

## Problem-to-Tool Mapping

| Problem | Solution |
|---------|----------|
| Server crashes, manual restart needed | Health checks + auto-restart |
| Traffic spikes cause degradation | Auto-scaling |
| Microservice down, can't find standby | Service discovery |
| All requests hit single server | Load balancer |
| High latency for remote users | CDN + geographic distribution |
| Database overloaded by queries | Caching |
| Single client floods API | Rate limiting |
| Single server failure = total outage | Hot/cold standby |

## Architect's Role

The architect's value is deep understanding of problem domain and business needs, not knowing every technical detail. Core question: "what and why" - implementation details delegated to dev teams.

Technical decisions are interconnected with organizational culture, business strategy, regulatory requirements. All reliability metrics vary by use case, system criticality, and business requirements.

## Gotchas

- **Five nines costs exponentially more** than three nines - each additional nine roughly 10x the cost
- **MTTR matters more than MTTF** in practice - failures are inevitable, fast recovery is the goal
- **Hot standby without testing** - standby that was never tested may not work when needed. Test failover regularly
- **Chaos engineering without monitoring** - injecting failures without observing results is just breaking things
- **SLA != SLO != SLI** - SLI measures, SLO targets, SLA is the contract with consequences

## See Also

- [[distributed-systems-fundamentals]] - CAP theorem, consensus, replication
- [[microservices-communication]] - Circuit breaker, bulkhead patterns
- [[devops-cicd]] - Deployment strategies, monitoring, observability
- [[security-architecture]] - Security as part of reliability
