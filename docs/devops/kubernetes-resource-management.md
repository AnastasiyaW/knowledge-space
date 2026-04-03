---
title: Kubernetes Resource Management
category: concepts
tags: [devops, kubernetes, resources, limits, quotas, autoscaling, hpa, namespaces]
---

# Kubernetes Resource Management

Resource management controls how CPU and memory are allocated, consumed, and bounded across the cluster. Proper configuration prevents noisy neighbors and ensures fair resource distribution.

## Requests and Limits

Defined per container, not per pod:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "200m"
    memory: "256Mi"
```

- **Requests** - guaranteed minimum. Scheduler uses this for placement decisions
- **Limits** - maximum allowed consumption
- CPU in millicores: 1000m = 1 vCPU
- Memory in Mi/Gi

### Exceeding Limits

| Resource | Behavior | Type |
|----------|----------|------|
| CPU | Throttled (not killed) | Compressible - can be redistributed |
| Memory | OOMKilled | Incompressible - reclaimed only by killing |

## QoS Classes

Assigned automatically based on requests/limits configuration. Determines eviction priority (BestEffort first, Guaranteed last):

| Class | Condition | Use Case |
|-------|-----------|----------|
| **Guaranteed** | All containers: limits == requests for both CPU and memory | Databases, critical services |
| **Burstable** | At least one container: requests < limits | Web services, variable-load apps |
| **BestEffort** | No requests or limits set | Test environments only |

## Namespaces

Virtual clusters within a physical cluster. Provide isolation boundary and per-namespace resource control.

```bash
kubectl create namespace dev
kubectl apply -f manifest.yaml -n dev
kubectl get pods -n dev
kubectl delete ns dev           # deletes namespace + ALL contents
```

**Default namespaces**: `default`, `kube-system` (CoreDNS, kube-proxy, metrics-server), `kube-public`, `kube-node-lease`.

Same manifest deploys to multiple namespaces without changing names - just use `-n <namespace>`.

## LimitRange

Per-container policy within a namespace. Assigns defaults and enforces min/max:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-mem-limit-range
  namespace: dev
spec:
  limits:
  - type: Container
    default:            # default limits
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:     # default requests
      cpu: "300m"
      memory: "256Mi"
    min:
      cpu: "100m"
      memory: "64Mi"
    max:
      cpu: "2"
      memory: "2Gi"
```

Pods violating LimitRange are rejected at creation.

## ResourceQuota

Namespace-wide budget for aggregate resource consumption:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ns-resource-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "4Gi"
    limits.cpu: "8"
    limits.memory: "8Gi"
    pods: "20"
    configmaps: "10"
    persistentvolumeclaims: "10"
    secrets: "10"
    services: "10"
```

New pods fail with "exceeded quota" when namespace totals are reached.

**Key distinction**: LimitRange = per-container policy. ResourceQuota = namespace-wide budget. They work together.

## Horizontal Pod Autoscaler (HPA)

Scales pod replicas based on CPU/memory utilization. Requires Metrics Server.

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-demo
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```

```bash
kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10
kubectl get hpa
```

- Scale-up: immediate when target exceeded
- Scale-down: 5-minute cooldown
- Requires resource requests set on containers

## Cluster Autoscaler

Scales worker nodes based on pending pod demands:

```bash
az aks create --enable-cluster-autoscaler --min-count 1 --max-count 5
```

- Provisions new nodes when pods can't be scheduled (1-3 minutes)
- Removes underutilized nodes after cool-down period
- Resource requests/limits drive the decision - large requests force new nodes faster

### HPA + Cluster Autoscaler Together

HPA increases pods -> insufficient node resources -> cluster autoscaler adds nodes -> pods scheduled. Reverse on scale-down.

## Node Selectors

Schedule pods to specific node pools:

```yaml
spec:
  nodeSelector:
    nodepoolos: linux           # Linux user pool
    # OR
    kubernetes.io/os: windows   # Windows pool
    # OR
    type: virtual-kubelet       # Virtual nodes (ACI/Fargate)
```

## Gotchas

- Without requests, scheduler has no information for placement - pods land randomly
- Without limits on memory, a single container can OOMKill the entire node
- If CPU `default` not specified in LimitRange, system assigns 1 vCPU (1000m) per container
- ResourceQuota blocks scaling if quota reached - new pods stay Pending
- Metrics Server must be running for HPA to work (default in managed K8s)
- Never delete `default` namespace

## See Also

- [[kubernetes-architecture]] - cluster components
- [[kubernetes-workloads]] - pods, deployments
- [[kubernetes-on-aks]] - AKS-specific resource management
- [[kubernetes-on-eks]] - EKS-specific autoscaling
