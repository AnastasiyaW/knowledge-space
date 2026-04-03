---
title: Deployment Strategies
category: concepts
tags: [devops, deployment, blue-green, canary, rolling-update, feature-flags, release-management]
---

# Deployment Strategies

Deployment strategies control how new application versions replace old ones. The choice affects downtime, rollback speed, resource cost, and risk exposure.

## Rolling Update (Kubernetes Default)

Gradually replaces old pods with new. Zero-downtime if health checks configured.

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%         # max extra pods during update
    maxUnavailable: 25%   # max pods unavailable during update
```

```bash
kubectl set image deployment/app app=app:2.0
kubectl rollout status deployment/app
kubectl rollout undo deployment/app         # rollback
```

## Blue-Green Deployment

Two identical environments. Deploy to inactive, switch traffic after validation.

- **Blue** = current stable
- **Green** = new version
- Rollback = redirect traffic back
- In K8s: two Deployments, Service selector switches between them

**Pros**: instant rollback, full testing before switch
**Cons**: double infrastructure cost

## Canary Deployment

Route small percentage of traffic to new version. Monitor, then gradually increase.

With Kubernetes + Istio:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
spec:
  http:
  - route:
    - destination:
        host: app
        subset: v1
      weight: 90
    - destination:
        host: app
        subset: v2
      weight: 10
```

Without service mesh: use multiple Deployments with different replica counts under same Service.

**Pros**: low risk, gradual validation
**Cons**: requires traffic splitting capability

## Feature Flags

Deploy code with features toggled off. Enable gradually by user segment.

- Decouple deployment from release
- Kill switch for problematic features
- Progressive rollout per user segment
- No extra infrastructure needed

## Release Checklist

- **Capacity planning**: expected load, can infrastructure handle it
- **Integration**: load balancers configured, monitoring ready
- **Failure handling**: per-component impact assessment
- **Rollback plan**: defined and tested
- **Communication**: stakeholder notification, status pages

## Release and Error Budget

From SRE perspective:
- Error budget remaining -> can deploy faster, take more risks
- Error budget exhausted -> freeze releases, focus on reliability
- Smaller changes = lower risk (smaller blast radius)
- Automated rollback mechanisms mandatory

## Cloud-Native 15-Factor Methodology

Extension of 12-Factor App for cloud-native services:

1. One Codebase per service
2. API First - contract before implementation
3. Explicit Dependencies (pom.xml, package.json)
4. Strict Design/Build/Release/Run separation
5. Externalized Configuration (env vars, config server)
6. Logs as event streams (stdout)
7. Fast startup, graceful shutdown (Disposability)
8. Backing Services as attached resources
9. Environment Parity (dev ~ staging ~ prod)
10. Admin Processes as one-off tasks
11. Port Binding for service export
12. Stateless Processes (share-nothing)
13. Scale via process model (Concurrency)
14. Telemetry (health, performance, business metrics)
15. Authentication/Authorization as first-class concern

## Gotchas

- Rolling updates can cause mixed-version traffic during transition - ensure backward compatibility
- Blue-green requires database migration strategy if schema changes
- Canary requires good observability to detect issues at low traffic percentages
- Feature flags accumulate technical debt if not cleaned up after rollout
- Config rollback is as important as code rollback

## See Also

- [[sre-principles]] - error budgets driving deployment velocity
- [[kubernetes-workloads]] - K8s deployment strategies
- [[service-mesh-istio]] - traffic splitting for canary
- [[helm-package-manager]] - versioned releases and rollbacks
- [[gitops-and-argocd]] - automated deployments
