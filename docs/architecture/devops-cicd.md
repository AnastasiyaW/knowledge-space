---
title: DevOps and CI/CD
category: reference
tags: [devops, cicd, docker, kubernetes, iac, deployment, monitoring]
---

# DevOps and CI/CD

DevOps bridges development and operations through culture, automation, and process improvement. Not a tool - it's a methodology combining cultural, organizational, and technical practices.

## CI/CD Pipeline

```bash
Source (commit) -> Build (compile) -> Test (unit, integration, e2e) ->
  Security scan -> Artifact creation -> Deploy staging -> Acceptance tests ->
  Deploy production -> Smoke tests
```

| Practice | Description |
|----------|-------------|
| **CI** | Frequent merges (daily+), automated build and test, early bug detection |
| **Continuous Delivery** | Auto-prepared for release, manual deployment approval |
| **Continuous Deployment** | Auto-deploy on passing tests, no manual gate |

## Infrastructure as Code (IaC)

Manage infrastructure through version-controlled configuration files.

| Tool | Approach | Best For |
|------|----------|----------|
| **Terraform** | Declarative, cloud-agnostic | Multi-cloud provisioning |
| **CloudFormation** | Declarative, AWS-specific | AWS-only shops |
| **Pulumi** | General-purpose languages | Developers preferring code |
| **Ansible** | Configuration management | Server configuration, orchestration |

**Immutable infrastructure:** create new instances with updated config, replace old ones. Eliminates configuration drift. Works with containers and blue-green deployments.

## Containerization

**Docker:** Package app + dependencies into portable containers.
- Dockerfile defines build steps
- docker-compose for multi-container apps
- Best practices: small base images (Alpine, distroless), multi-stage builds, non-root user, health checks, resource limits

**Kubernetes (K8s):** Container orchestration.
- Key concepts: Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, Namespaces
- Auto-deployment, scaling, management of containerized apps

## Deployment Strategies

| Strategy | Mechanism | Rollback | Risk |
|----------|-----------|----------|------|
| **Blue-Green** | Two identical environments, switch traffic | Instant (switch back) | 2x infrastructure cost |
| **Canary** | Gradual rollout to small subset first | Remove canary | Low - small blast radius |
| **Rolling** | Replace instances gradually | Rolling back | Brief mixed versions |
| **Feature flags** | Deploy with features behind toggles | Toggle off | Code complexity |

## Zero-Downtime Database Migrations

**Expand-Contract Pattern:**
1. **Expand** - add new column/table alongside old. Both work
2. **Migrate data** - copy/transform from old to new
3. **Switch** - update app to use new structure
4. **Contract** - remove old after verification period

**Migration principles:**
- Forward-only (never modify existing scripts)
- Version controlled (Git)
- Idempotent (safe to run multiple times)
- Rollback plan for every migration

## Monitoring and Observability

### Three Pillars

| Pillar | What | Tools |
|--------|------|-------|
| **Metrics** | Numbers over time (latency, throughput, errors) | Prometheus + Grafana |
| **Logs** | Event records | ELK Stack, Loki |
| **Traces** | Request flow across services | Jaeger, Zipkin |

**All-in-one:** Datadog, New Relic.

### Key Metrics
- Latency: p50, p95, p99
- Throughput: requests/sec
- Error rate
- Saturation: resource utilization
- SLI/SLO/SLA

**Alerting:** Alert on symptoms (user impact), not causes. Reduce alert fatigue. Runbooks for each alert. PagerDuty, OpsGenie for incident management.

## 12-Factor App Methodology

1. **Codebase** - one repo per app
2. **Dependencies** - explicitly declare
3. **Config** - in environment variables
4. **Backing services** - treat as attached resources
5. **Build, release, run** - strict separation
6. **Processes** - stateless, share-nothing
7. **Port binding** - self-contained
8. **Concurrency** - scale via processes
9. **Disposability** - fast startup, graceful shutdown
10. **Dev/prod parity** - keep environments similar
11. **Logs** - treat as event streams
12. **Admin** - one-off processes

## Design for Operations

- Health endpoints, graceful shutdown
- Structured logging, correlation IDs across services
- Configuration externalization
- Backward-compatible DB migrations
- API versioning, feature flags
- Business metrics alongside technical ones

## Gotchas

- **CI without tests** is just "continuous building" - automated tests are the point
- **Blue-green with databases** - both versions must work with same DB schema during transition
- **Feature flag cleanup** - dead flags accumulate. Schedule removal after rollout
- **Monitoring without alerting** - dashboards nobody watches are useless
- **DevSecOps** - integrate security at every stage, not as afterthought

## See Also

- [[quality-attributes-reliability]] - Availability, fault tolerance, auto-scaling
- [[security-architecture]] - DevSecOps integration
- [[microservices-communication]] - Service architecture patterns
- [[database-selection]] - ORM, migrations, zero-downtime patterns
