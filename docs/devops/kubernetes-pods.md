---
title: Kubernetes Pods & Workloads
category: orchestration
tags: [kubernetes, pods, deployment, replicaset, statefulset, daemonset, kubectl]
---
# Kubernetes Pods & Workloads

Core Kubernetes workload resources: Pods, Deployments, ReplicaSets, StatefulSets, DaemonSets.

## Key Facts

- **Pod** = smallest deployable unit; one or more containers sharing network namespace and storage
- All containers in a pod share `localhost`; each pod gets a unique cluster IP
- **Deployment** = declarative desired state for pods; manages ReplicaSets for rolling updates
- **ReplicaSet** = ensures N pod replicas running; usually managed by Deployment (don't create directly)
- **StatefulSet** = for stateful apps (databases); provides stable network IDs, persistent storage, ordered deploy/scale
- **DaemonSet** = runs one pod per node (monitoring agents, log collectors)
- **Job** = run-to-completion workload; **CronJob** = scheduled Jobs
- Pod lifecycle: Pending -> Running -> Succeeded/Failed; containers have Ready/NotReady status
- `kubectl` is the primary CLI; config stored in `~/.kube/config`
- **Labels** are key-value pairs for organizing; **selectors** filter resources by labels
- [[kubernetes-services]] expose pods to network traffic
- [[helm-charts]] template and package Kubernetes manifests
- Init containers run before main containers; useful for setup tasks
- Resource requests (guaranteed) vs limits (maximum) control CPU/memory allocation

## Patterns

```yaml
# Deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: app
        image: myapp:1.2.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: db_host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: db_password
```

```bash
# Core kubectl commands
kubectl apply -f deployment.yaml        # create/update resource
kubectl get pods                         # list pods
kubectl get pods -o wide                 # with node and IP info
kubectl get deploy,rs,pod               # multiple resource types
kubectl describe pod web-app-xyz        # detailed info + events
kubectl logs web-app-xyz -f             # follow container logs
kubectl logs web-app-xyz -c sidecar     # specific container in pod
kubectl exec -it web-app-xyz -- /bin/sh # shell into container

# Scaling
kubectl scale deploy web-app --replicas=5
kubectl autoscale deploy web-app --min=2 --max=10 --cpu-percent=80

# Rolling updates
kubectl set image deploy/web-app app=myapp:1.3.0
kubectl rollout status deploy/web-app
kubectl rollout undo deploy/web-app     # rollback to previous

# Debugging
kubectl get events --sort-by='.lastTimestamp'
kubectl top pods                        # resource usage (requires metrics-server)
kubectl get pods --field-selector=status.phase=Failed
```

## Gotchas

- Pod IPs are ephemeral - they change on restart; use [[kubernetes-services]] for stable endpoints
- `imagePullPolicy: Always` is default for `:latest` tag; pin versions and use `IfNotPresent` for speed
- Liveness probe failures = container restart; readiness probe failures = removed from Service endpoints (different consequences)
- Resource limits exceeded: CPU gets throttled, memory gets OOM-killed (pod evicted)
- `requests` are used for scheduling decisions; `limits` are enforced at runtime - set both
- StatefulSet pods are created sequentially (0, 1, 2...); deleted in reverse order
- `kubectl delete pod` with Deployment = pod immediately recreated; delete the Deployment instead
- ConfigMap/Secret updates don't auto-restart pods; use `kubectl rollout restart deploy/name`

## See Also

- [[kubernetes-services]] - exposing pods via Services, Ingress
- [[helm-charts]] - templating Kubernetes manifests
- [[deployment-strategies]] - rolling update, blue-green, canary
- [[monitoring-observability]] - pod metrics and alerting
- Kubernetes docs: https://kubernetes.io/docs/concepts/workloads/
- kubectl cheat sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
