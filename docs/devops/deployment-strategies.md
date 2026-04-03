---
title: Deployment Strategies
category: operations
tags: [deployment, rolling-update, blue-green, canary, zero-downtime, rollback]
---
# Deployment Strategies

Rolling updates, blue-green, canary deployments, and zero-downtime release patterns.

## Key Facts

- **Rolling update** = gradually replace old pods with new; default K8s Deployment strategy
- **Blue-Green** = two identical environments; switch traffic from blue (current) to green (new) at once
- **Canary** = route small percentage of traffic to new version; expand if healthy, rollback if not
- **Recreate** = stop all old instances, then start new; causes downtime but simplest
- **A/B testing** = route specific users (by header, cookie, geo) to new version for feature testing
- Rolling update params: `maxSurge` (extra pods during update), `maxUnavailable` (pods removed during update)
- **Readiness probe** gates traffic to new pods; unready pods don't receive requests
- **Argo Rollouts** = K8s controller for advanced canary/blue-green with automated analysis
- **Progressive delivery** = canary + automated metrics analysis + auto-promote/rollback
- [[kubernetes-pods]] liveness/readiness probes are critical for safe deployments
- [[monitoring-observability]] signals drive canary promotion decisions
- [[helm-charts]] `helm rollback` provides release-level rollback

## Patterns

```yaml
# Kubernetes Rolling Update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # at most 5 pods during update
      maxUnavailable: 0      # zero downtime
  template:
    spec:
      containers:
      - name: app
        image: myapp:2.0.0
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

```yaml
# Argo Rollouts - Canary with analysis
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: web
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - analysis:
          templates:
          - templateName: success-rate
      - setWeight: 30
      - pause: {duration: 5m}
      - setWeight: 60
      - pause: {duration: 5m}
      - setWeight: 100
      canaryService: web-canary
      stableService: web-stable

---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
  - name: success-rate
    interval: 60s
    successCondition: result[0] >= 0.95
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{status=~"2.."}[5m])) /
          sum(rate(http_requests_total[5m]))
```

```bash
# Kubernetes manual rollout operations
kubectl set image deploy/web app=myapp:2.0.0
kubectl rollout status deploy/web            # watch progress
kubectl rollout pause deploy/web             # pause mid-rollout
kubectl rollout resume deploy/web            # resume
kubectl rollout undo deploy/web              # rollback to previous
kubectl rollout undo deploy/web --to-revision=3  # rollback to specific
kubectl rollout history deploy/web           # show revision history
```

```
# Strategy comparison
Strategy        | Downtime | Rollback | Resource cost | Risk
----------------|----------|----------|---------------|------
Recreate        | Yes      | Slow     | 1x            | High
Rolling Update  | No       | Fast     | 1-2x          | Medium
Blue-Green      | No       | Instant  | 2x            | Low
Canary          | No       | Fast     | 1.1x          | Lowest
```

## Gotchas

- Rolling update with `maxUnavailable: 0` and `maxSurge: 1` is safest but slowest (one pod at a time)
- Blue-green requires double the resources during deployment; clean up old environment after validation
- Canary with database schema changes is tricky - new code must work with both old and new schemas
- `kubectl rollout undo` only works for Deployments, not Helm releases; use `helm rollback` for Helm
- Readiness probe must accurately reflect app readiness; a pod that's "ready" but not serving = errors
- Session affinity (sticky sessions) can prevent canary traffic from spreading evenly
- Database migrations must be backward-compatible for zero-downtime deployments (expand-and-contract pattern)
- PodDisruptionBudget prevents K8s from evicting too many pods during node maintenance

## See Also

- [[kubernetes-pods]] - pod lifecycle and probes
- [[kubernetes-services]] - traffic routing to deployment versions
- [[monitoring-observability]] - metrics for canary analysis
- [[gitops]] - Argo Rollouts for GitOps-native progressive delivery
- K8s Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Argo Rollouts: https://argoproj.github.io/argo-rollouts/
