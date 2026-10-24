---
title: "PostgreSQL sur Docker et Kubernetes"
category: reference
tags: [sql-databases, postgresql, docker, kubernetes, helm, statefulset, operator, gke, persistent-volume]
level: 3
source_sha256: 430250a4b706b2e6eb34ed0e3be252c91fa0aee7263300a953720c9302e23bc8
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL sur Docker et Kubernetes {#postgresql-on-docker-and-kubernetes}

Faire tourner PostgreSQL dans des conteneurs exige une gestion rigoureuse du stockage persistant, de la mémoire partagée et des schémas de charges de travail avec état. Kubernetes ajoute une complexité d'orchestration, mais permet une haute disponibilité automatisée.

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

**Considérations de production :**
- Utiliser toujours des volumes nommés (et non des bind mounts) pour le répertoire de données
- `--shm-size=256m` pour une mémoire partagée plus importante (la valeur par défaut de 64 Mo est trop faible)
- Définir `shared_buffers` à l'intérieur du conteneur pour correspondre à la mémoire allouée
- Vérifications de santé : `pg_isready -U postgres`

## Ressources Kubernetes de base {#kubernetes-core-resources}

**StatefulSet :** Pour les applications avec état comme les bases de données. Garanties : identifiants réseau stables, stockage persistant stable, déploiement/mise à l'échelle ordonnés et gracieux.

**PersistentVolumeClaim :** Demande de stockage.

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

## Haute disponibilité sur Kubernetes {#ha-on-kubernetes}

### Chart Helm Bitnami {#bitnami-helm-chart}
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install pgsql-ha bitnami/postgresql-ha \
  --set service.type=LoadBalancer
# Architecture: Pgpool-II + postgresql-repmgr
```

### Opérateur PostgreSQL de Zalando {#zalando-postgresql-operator}
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

### Déploiement Patroni sur GKE {#gke-patroni-deployment}
```bash
gcloud container clusters create pg-cluster --zone us-central1-c --machine-type e2-medium --num-nodes 3

helm install patroni ./patroni \
  --set credentials.superuser="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c32)"

# Check roles
kubectl get pods -l spilo-role -L spilo-role
```

## Pile de supervision {#monitoring-stack}

- **Prometheus + pg_exporter :** Connexions, latence des requêtes, retard de réplication, bloat des tables
- **Grafana :** Tableaux de bord de performance PostgreSQL
- **pg_stat_statements :** Suivi des performances des requêtes
- **pgBadger :** Analyseur de journaux pour les rapports de requêtes lentes

## Points clés {#key-facts}

- Un PV seul n'est pas une sauvegarde : sauvegarder toujours vers un stockage externe (S3/GCS)
- Utiliser `volumeBindingMode: WaitForFirstConsumer` pour les clusters régionaux
- La suppression d'un pod déclenche un basculement dans les configurations HA
- Crunchy PGO : opérateur de qualité production avec intégration pgBackRest
- ConfigMap pour postgresql.conf, Secret pour les mots de passe

## Pièges à éviter {#gotchas}

- La valeur par défaut de `--shm-size` dans Docker (64 Mo) est insuffisante pour shared_buffers > 128 Mo
- `reclaimPolicy: Delete` (par défaut) détruit les données lorsque le PV est libéré : utiliser `Retain` pour les bases de données
- La réduction d'un StatefulSet ne supprime PAS les PVC : les volumes orphelins s'accumulent
- `gcloud compute disks list` après la suppression d'un cluster permet de vérifier la présence de disques résiduels
- DNS Kubernetes : `service-name.namespace.svc.cluster.local:5432`

## Voir aussi {#see-also}

- [[postgresql-ha-patroni]] - Détails de configuration de Patroni
- [[postgresql-configuration-tuning]] - paramètres pour les déploiements conteneurisés
- [[backup-and-recovery]] - stratégies de sauvegarde pour PostgreSQL sur K8s
- [[connection-pooling]] - sidecar PgBouncer dans K8s
