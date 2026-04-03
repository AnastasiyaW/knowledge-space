---
title: PostgreSQL on Docker and Kubernetes
category: reference
tags: [sql-databases, postgresql, docker, kubernetes, helm, statefulset, operator, gke, persistent-volume]
---

# PostgreSQL on Docker and Kubernetes

Running PostgreSQL in containers requires careful handling of persistent storage, shared memory, and stateful workload patterns. Kubernetes adds orchestration complexity but enables automated HA.

## Docker

```bash
# Run PostgreSQL in Docker
docker run -d --name pg \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  --shm-size=256m \
  postgres:15

# Connect
psql -h localhost -U postgres
```

**Production considerations:**
- Always use named volumes (not bind mounts) for data directory
- `--shm-size=256m` for larger shared memory (default 64MB too small)
- Set `shared_buffers` inside container to match allocated memory
- Health checks: `pg_isready -U postgres`

## Kubernetes Core Resources

**StatefulSet:** For stateful applications like databases. Guarantees: stable network identifiers, stable persistent storage, ordered graceful deployment/scaling.

**PersistentVolumeClaim:** Request for storage.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: pg-secret
              key: password
        volumeMounts:
        - name: pgdata
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: pgdata
    spec:
      accessModes: [ReadWriteOnce]
      resources:
        requests:
          storage: 50Gi
      storageClassName: fast-ssd
```

### Storage Class
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
reclaimPolicy: Retain  # CRITICAL: don't delete data when PV released
volumeBindingMode: WaitForFirstConsumer
```

## HA on Kubernetes

### Bitnami Helm Chart
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install pgsql-ha bitnami/postgresql-ha \
  --set service.type=LoadBalancer
# Architecture: Pgpool-II + postgresql-repmgr
```

### Zalando PostgreSQL Operator
```yaml
apiVersion: acid.zalan.do/v1
kind: postgresql
metadata:
  name: acid-cluster
spec:
  teamId: "myteam"
  numberOfInstances: 3
  postgresql:
    version: "15"
  volume:
    size: 50Gi
  resources:
    requests:
      cpu: "1"
      memory: 2Gi
```

### GKE Patroni Deployment
```bash
gcloud container clusters create pg-cluster --zone us-central1-c --machine-type e2-medium --num-nodes 3

helm install patroni ./patroni \
  --set credentials.superuser="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c32)"

# Check roles
kubectl get pods -l spilo-role -L spilo-role
```

## Monitoring Stack

- **Prometheus + pg_exporter:** Connections, query latency, replication lag, table bloat
- **Grafana:** PostgreSQL performance dashboards
- **pg_stat_statements:** Track query performance
- **pgBadger:** Log analyzer for slow query reports

## Key Facts

- PV alone is not backup - always backup to external storage (S3/GCS)
- Use `volumeBindingMode: WaitForFirstConsumer` for regional clusters
- Pod deletion triggers failover in HA setups
- Crunchy PGO: production-grade operator with pgBackRest integration
- ConfigMap for postgresql.conf, Secret for passwords

## Gotchas

- Default Docker `--shm-size` (64MB) is insufficient for shared_buffers > 128MB
- `reclaimPolicy: Delete` (default) destroys data when PV released - use `Retain` for databases
- StatefulSet scaling down does NOT delete PVCs - orphaned volumes accumulate
- `gcloud compute disks list` after cluster deletion to check for leftover disks
- Kubernetes DNS: `service-name.namespace.svc.cluster.local:5432`

## See Also

- [[postgresql-ha-patroni]] - Patroni configuration details
- [[postgresql-configuration-tuning]] - parameters for containerized deployments
- [[backup-and-recovery]] - backup strategies for K8s PostgreSQL
- [[connection-pooling]] - PgBouncer sidecar in K8s
