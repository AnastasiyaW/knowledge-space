---
title: Kubernetes Workloads
category: concepts
tags: [devops, kubernetes, deployment, statefulset, daemonset, pods, replicaset]
---

# Kubernetes Workloads

Kubernetes workload resources manage sets of pods. Each type serves different application patterns - from stateless web services to stateful databases.

## Pod

Smallest deployable unit. One or more containers sharing network namespace and storage. Only K8s object that directly starts containers.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
  - name: my-app
    image: my-app:1.0
    ports:
    - containerPort: 3000
```

Pods are ephemeral - never manage directly. Use Deployments, StatefulSets, or other controllers.

## Labels and Selectors

**Labels** are key-value pairs attached to resources: `app: nginx`, `env: prod`. They drive service routing, scheduling, and resource grouping.

```bash
kubectl get pods -l app=nginx
kubectl label pod <name> env=prod
```

## ReplicaSet

Ensures a specified number of identical pod replicas. Auto-creates replacements when pods fail.

```bash
kubectl scale rs/nginx --replicas=5
```

Rarely used directly - Deployments manage ReplicaSets automatically.

## Deployment

The standard workload for stateless applications. Manages ReplicaSets, handles rolling updates and rollbacks.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:1.0
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
```

### Update Strategies

| Strategy | Behavior |
|----------|----------|
| **RollingUpdate** (default) | Gradually replaces pods. `maxUnavailable` + `maxSurge` control pace |
| **Recreate** | Kills all old pods first, then creates new (causes downtime) |

### Deployment Operations

```bash
kubectl apply -f deployment.yaml
kubectl scale deployment/my-app --replicas=5
kubectl set image deployment/my-app my-app=my-app:2.0
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app                    # previous revision
kubectl rollout undo deployment/my-app --to-revision=1    # specific revision
```

## StatefulSet

For stateful applications requiring stable identities and persistent storage.

**Provides:**
- **Stable network identifiers** - each pod gets unique name (app-0, app-1, ...)
- **Ordered deployment** - pods created/deleted sequentially
- **Persistent storage** - each pod bound to its own PersistentVolume via volumeClaimTemplates

**Requires headless service** (clusterIP: None) for stable DNS per pod:
```html
<pod-name>.<headless-service>.<namespace>.svc.cluster.local
# Example: mongo-0.mongo-headless.default.svc.cluster.local
```

### When Deployment vs StatefulSet

| Criterion | Deployment | StatefulSet |
|-----------|------------|-------------|
| Pod identity | Interchangeable | Unique, stable |
| Persistent state | No | Yes, per pod |
| Deployment order | Doesn't matter | Sequential |
| Use cases | APIs, web servers, stateless apps | Databases, Kafka, ZooKeeper |

## DaemonSet

Guarantees exactly one pod on every node (or selected nodes). Used for system-level services: log collectors, monitoring agents, CNI plugins.

## ConfigMap and Secret

**ConfigMap** - non-sensitive configuration as key-value pairs:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  MYSQL_DATABASE: mydb
  LOG_LEVEL: info
```

**Secret** - sensitive data (base64 encoded, not encrypted by default):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=
```

Usage in pods:
```yaml
envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: db-secret
```

## Health Probes

```yaml
readinessProbe:        # can accept traffic?
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 30

livenessProbe:         # still alive?
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 60
```

## Image Pull Policy

| Policy | Behavior |
|--------|----------|
| `Always` | Check registry every time (default for `:latest`) |
| `IfNotPresent` | Use local if exists (default for specific tags) |
| `Never` | Only use local images |

## Multi-Service Deployment Order

1. Namespace
2. Secrets and ConfigMaps
3. PersistentVolumeClaims
4. Database Deployment + Service
5. Database migrations (as Job)
6. API Deployment + Service
7. Frontend Deployment + Service
8. Ingress for external access

## Gotchas

- Always set resource requests and limits on containers
- Use specific image tags, never `:latest` in production
- Multi-resource YAML: separate resources with `---` in a single file
- File naming convention: `00-namespace.yaml`, `01-configmap.yaml`, `02-deployment.yaml` ensures creation order

## See Also

- [[kubernetes-architecture]] - cluster components and networking
- [[kubernetes-services-and-networking]] - Services, Ingress, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass
- [[kubernetes-resource-management]] - requests, limits, autoscaling
- [[helm-package-manager]] - templated deployments
