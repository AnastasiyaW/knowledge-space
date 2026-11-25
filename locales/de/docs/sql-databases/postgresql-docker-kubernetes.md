---
title: "PostgreSQL auf Docker und Kubernetes"
category: reference
tags: [sql-databases, postgresql, docker, kubernetes, helm, statefulset, operator, gke, persistent-volume]
level: 3
source_sha256: 430250a4b706b2e6eb34ed0e3be252c91fa0aee7263300a953720c9302e23bc8
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL auf Docker und Kubernetes {#postgresql-on-docker-and-kubernetes}

Der Betrieb von PostgreSQL in Containern erfordert eine sorgfältige Handhabung von persistentem Speicher, Shared Memory und Mustern für zustandsbehaftete Workloads. Kubernetes bringt zusätzliche Orchestrierungskomplexität, ermöglicht aber automatisiertes HA.

## Docker {#docker}

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

**Produktionsaspekte:**
- Für das Datenverzeichnis immer benannte Volumes verwenden (keine Bind Mounts)
- `--shm-size=256m` für größeren Shared Memory (der Standard von 64MB ist zu klein)
- `shared_buffers` im Container auf den zugewiesenen Speicher abstimmen
- Health Checks: `pg_isready -U postgres`

## Zentrale Kubernetes-Ressourcen {#kubernetes-core-resources}

**StatefulSet:** Für zustandsbehaftete Anwendungen wie Datenbanken. Garantien: stabile Netzwerkidentifikatoren, stabiler persistenter Speicher, geordnetes Deployment und Skalieren mit Graceful Shutdown.

**PersistentVolumeClaim:** Anforderung von Speicher.

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

### Storage Class {#storage-class}
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

## HA auf Kubernetes {#ha-on-kubernetes}

### Bitnami Helm Chart {#bitnami-helm-chart}
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install pgsql-ha bitnami/postgresql-ha \
  --set service.type=LoadBalancer
# Architecture: Pgpool-II + postgresql-repmgr
```

### Zalando PostgreSQL Operator {#zalando-postgresql-operator}
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

### GKE-Patroni-Deployment {#gke-patroni-deployment}
```bash
gcloud container clusters create pg-cluster --zone us-central1-c --machine-type e2-medium --num-nodes 3

helm install patroni ./patroni \
  --set credentials.superuser="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c32)"

# Check roles
kubectl get pods -l spilo-role -L spilo-role
```

## Monitoring-Stack {#monitoring-stack}

- **Prometheus + pg_exporter:** Verbindungen, Abfragelatenz, Replikationsverzögerung, Tabellen-Bloat
- **Grafana:** PostgreSQL-Performance-Dashboards
- **pg_stat_statements:** Abfrageleistung verfolgen
- **pgBadger:** Log-Analyzer für Berichte über langsame Abfragen

## Wichtige Fakten {#key-facts}

- Ein PV allein ist kein Backup - immer extern sichern (S3/GCS)
- `volumeBindingMode: WaitForFirstConsumer` für regionale Cluster verwenden
- Das Löschen eines Pods löst in HA-Setups ein Failover aus
- Crunchy PGO: Operator in Produktionsqualität mit pgBackRest-Integration
- ConfigMap für postgresql.conf, Secret für Passwörter

## Fallstricke {#gotchas}

- Der Docker-Standard `--shm-size` (64MB) reicht nicht für shared_buffers > 128MB
- `reclaimPolicy: Delete` (Standard) löscht Daten, sobald das PV freigegeben wird - für Datenbanken `Retain` verwenden
- Ein Scale-down eines StatefulSets löscht die PVCs NICHT - verwaiste Volumes sammeln sich an
- `gcloud compute disks list` nach dem Löschen eines Clusters ausführen, um übriggebliebene Disks zu prüfen
- Kubernetes-DNS: `service-name.namespace.svc.cluster.local:5432`

## Siehe auch {#see-also}

- [[postgresql-ha-patroni]] - Patroni-Konfigurationsdetails
- [[postgresql-configuration-tuning]] - Parameter für containerisierte Deployments
- [[backup-and-recovery]] - Backup-Strategien für PostgreSQL auf Kubernetes
- [[connection-pooling]] - PgBouncer-Sidecar in Kubernetes
