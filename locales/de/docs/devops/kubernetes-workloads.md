---
title: "Kubernetes-Workloads"
category: concepts
tags: [devops, kubernetes, deployment, statefulset, daemonset, pods, replicaset]
level: 3
source_sha256: f9140ad40dfb9b85f9dc6ad70602a022f966df22d6360745839a39f756b08d6d
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes-Workloads {#kubernetes-workloads}

Kubernetes-Workload-Ressourcen verwalten Gruppen von Pods. Jeder Typ dient unterschiedlichen Anwendungsmustern, von zustandslosen Webdiensten bis zu zustandsbehafteten Datenbanken.

## Pod {#pod}

Kleinste deploybare Einheit. Ein oder mehrere Container, die sich Network-Namespace und Speicher teilen. Einziges K8s-Objekt, das Container direkt startet.

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

Pods sind flüchtig. Niemals direkt verwalten, stattdessen Deployments, StatefulSets oder andere Controller verwenden.

## Labels und Selektoren {#labels-and-selectors}

**Labels** sind Schlüssel-Wert-Paare, die an Ressourcen angehängt werden: `app: nginx`, `env: prod`. Sie steuern Service-Routing, Scheduling und die Gruppierung von Ressourcen.

```bash
kubectl get pods -l app=nginx
kubectl label pod <name> env=prod
```

## ReplicaSet {#replicaset}

Stellt eine vorgegebene Anzahl identischer Pod-Replikate sicher. Erstellt automatisch Ersatz, wenn Pods ausfallen.

```bash
kubectl scale rs/nginx --replicas=5
```

Selten direkt verwendet, da Deployments ReplicaSets automatisch verwalten.

## Deployment {#deployment}

Der Standard-Workload für zustandslose Anwendungen. Verwaltet ReplicaSets und übernimmt Rolling Updates und Rollbacks.

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

### Update-Strategien {#update-strategies}

| Strategie | Verhalten |
|----------|----------|
| **RollingUpdate** (Standard) | Ersetzt Pods schrittweise. `maxUnavailable` + `maxSurge` steuern das Tempo |
| **Recreate** | Beendet zuerst alle alten Pods, erstellt dann neue (verursacht Ausfallzeit) |

### Deployment-Operationen {#deployment-operations}

```bash
kubectl apply -f deployment.yaml
kubectl scale deployment/my-app --replicas=5
kubectl set image deployment/my-app my-app=my-app:2.0
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app                    # previous revision
kubectl rollout undo deployment/my-app --to-revision=1    # specific revision
```

## StatefulSet {#statefulset}

Für zustandsbehaftete Anwendungen, die stabile Identitäten und persistenten Speicher benötigen.

**Bietet:**
- **Stabile Netzwerkkennungen**: Jeder Pod erhält einen eindeutigen Namen (app-0, app-1, ...)
- **Geordnete Bereitstellung**: Pods werden sequenziell erstellt und gelöscht
- **Persistenter Speicher**: Jeder Pod ist über volumeClaimTemplates an ein eigenes PersistentVolume gebunden

**Erfordert einen Headless-Service** (clusterIP: None) für stabiles DNS pro Pod:
```html
<pod-name>.<headless-service>.<namespace>.svc.cluster.local
# Example: mongo-0.mongo-headless.default.svc.cluster.local
```

### Wann Deployment vs. StatefulSet {#when-deployment-vs-statefulset}

| Kriterium | Deployment | StatefulSet |
|-----------|------------|-------------|
| Pod-Identität | Austauschbar | Eindeutig, stabil |
| Persistenter Zustand | Nein | Ja, pro Pod |
| Bereitstellungsreihenfolge | Egal | Sequenziell |
| Anwendungsfälle | APIs, Webserver, zustandslose Apps | Datenbanken, Kafka, ZooKeeper |

## DaemonSet {#daemonset}

Garantiert genau einen Pod auf jedem Node (oder auf ausgewählten Nodes). Wird für systemnahe Dienste verwendet: Log-Collectors, Monitoring-Agents, CNI-Plugins.

## ConfigMap und Secret {#configmap-and-secret}

**ConfigMap**: nicht sensible Konfiguration als Schlüssel-Wert-Paare:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  MYSQL_DATABASE: mydb
  LOG_LEVEL: info
```

**Secret**: sensible Daten (base64-kodiert, standardmäßig nicht verschlüsselt):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=
```

Verwendung in Pods:
```yaml
envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: db-secret
```

## Health Probes {#health-probes}

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

## Image Pull Policy {#image-pull-policy}

| Policy | Verhalten |
|--------|----------|
| `Always` | Registry bei jedem Start prüfen (Standard für `:latest`) |
| `IfNotPresent` | Lokales Image verwenden, falls vorhanden (Standard für spezifische Tags) |
| `Never` | Nur lokale Images verwenden |

## Reihenfolge der Multi-Service-Bereitstellung {#multi-service-deployment-order}

1. Namespace
2. Secrets und ConfigMaps
3. PersistentVolumeClaims
4. Datenbank-Deployment + Service
5. Datenbank-Migrationen (als Job)
6. API-Deployment + Service
7. Frontend-Deployment + Service
8. Ingress für externen Zugriff

## Stolperfallen {#gotchas}

- Immer Ressource-Requests und -Limits für Container setzen
- Spezifische Image-Tags verwenden, niemals `:latest` in Produktion
- Mehrere Ressourcen in YAML: Ressourcen in einer Datei mit `---` trennen
- Dateinamenskonvention: `00-namespace.yaml`, `01-configmap.yaml`, `02-deployment.yaml` sorgt für die Erstellungsreihenfolge

## Siehe auch {#see-also}

- [[kubernetes-architecture]] - Cluster-Komponenten und Netzwerk
- [[kubernetes-services-and-networking]] - Services, Ingress, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass
- [[kubernetes-resource-management]] - Requests, Limits, Autoskalierung
- [[helm-package-manager]] - templatebasierte Deployments
