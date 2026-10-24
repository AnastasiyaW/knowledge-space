---
title: "Charges de travail Kubernetes"
category: concepts
tags: [devops, kubernetes, deployment, statefulset, daemonset, pods, replicaset]
level: 3
source_sha256: f9140ad40dfb9b85f9dc6ad70602a022f966df22d6360745839a39f756b08d6d
translation: machine
translated_at: '2026-10-24'
---
# Charges de travail Kubernetes {#kubernetes-workloads}

Les ressources de charge de travail Kubernetes gèrent des ensembles de pods. Chaque type répond à des modèles d'application différents, des services web sans état aux bases de données avec état.

## Pod {#pod}

Plus petite unité déployable. Un ou plusieurs conteneurs partageant un espace de noms réseau et un stockage. Seul objet K8s qui démarre directement des conteneurs.

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

Les pods sont éphémères : ne les gérez jamais directement. Utilisez des Deployments, des StatefulSets ou d'autres contrôleurs.

## Labels et sélecteurs {#labels-and-selectors}

Les **labels** sont des paires clé-valeur attachées aux ressources : `app: nginx`, `env: prod`. Ils pilotent le routage des services, l'ordonnancement et le regroupement des ressources.

```bash
kubectl get pods -l app=nginx
kubectl label pod <name> env=prod
```

## ReplicaSet {#replicaset}

Garantit un nombre défini de répliques identiques de pods. Crée automatiquement des remplaçants lorsque des pods échouent.

```bash
kubectl scale rs/nginx --replicas=5
```

Rarement utilisé directement : les Deployments gèrent automatiquement les ReplicaSets.

## Deployment {#deployment}

La charge de travail standard pour les applications sans état. Gère les ReplicaSets et assure les mises à jour progressives ainsi que les retours en arrière.

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

### Stratégies de mise à jour {#update-strategies}

| Stratégie | Comportement |
|-----------|--------------|
| **RollingUpdate** (par défaut) | Remplace progressivement les pods. `maxUnavailable` et `maxSurge` contrôlent le rythme |
| **Recreate** | Arrête d'abord tous les anciens pods, puis en crée de nouveaux (provoque une interruption de service) |

### Opérations sur les Deployments {#deployment-operations}

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

Pour les applications avec état nécessitant des identités stables et un stockage persistant.

**Fournit :**
- **Identifiants réseau stables** : chaque pod reçoit un nom unique (app-0, app-1, ...)
- **Déploiement ordonné** : pods créés et supprimés séquentiellement
- **Stockage persistant** : chaque pod est lié à son propre PersistentVolume via volumeClaimTemplates

**Nécessite un service headless** (clusterIP: None) pour un DNS stable par pod :
```html
<pod-name>.<headless-service>.<namespace>.svc.cluster.local
# Example: mongo-0.mongo-headless.default.svc.cluster.local
```

### Deployment ou StatefulSet {#when-deployment-vs-statefulset}

| Critère | Deployment | StatefulSet |
|---------|------------|-------------|
| Identité du pod | Interchangeable | Unique, stable |
| État persistant | Non | Oui, par pod |
| Ordre de déploiement | Sans importance | Séquentiel |
| Cas d'usage | APIs, serveurs web, applications sans état | Bases de données, Kafka, ZooKeeper |

## DaemonSet {#daemonset}

Garantit exactement un pod sur chaque nœud (ou sur les nœuds sélectionnés). Utilisé pour les services système : collecteurs de logs, agents de supervision, plugins CNI.

## ConfigMap et Secret {#configmap-and-secret}

**ConfigMap** : configuration non sensible sous forme de paires clé-valeur :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  MYSQL_DATABASE: mydb
  LOG_LEVEL: info
```

**Secret** : données sensibles (encodées en base64, non chiffrées par défaut) :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=
```

Utilisation dans les pods :
```yaml
envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: db-secret
```

## Sondes de santé {#health-probes}

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

## Politique de téléchargement des images {#image-pull-policy}

| Politique | Comportement |
|-----------|--------------|
| `Always` | Vérifie le registre à chaque fois (par défaut pour `:latest`) |
| `IfNotPresent` | Utilise l'image locale si elle existe (par défaut pour les tags spécifiques) |
| `Never` | Utilise uniquement les images locales |

## Ordre de déploiement multi-services {#multi-service-deployment-order}

1. Namespace
2. Secrets et ConfigMaps
3. PersistentVolumeClaims
4. Deployment et Service de la base de données
5. Migrations de la base de données (sous forme de Job)
6. Deployment et Service de l'API
7. Deployment et Service du frontend
8. Ingress pour l'accès externe

## Pièges courants {#gotchas}

- Définissez toujours les requests et les limits de ressources sur les conteneurs
- Utilisez des tags d'image spécifiques, n'utilisez jamais `:latest` en production
- YAML multi-ressources : séparez les ressources avec `---` dans un même fichier
- La convention de nommage `00-namespace.yaml`, `01-configmap.yaml`, `02-deployment.yaml` garantit l'ordre de création

## Voir aussi {#see-also}

- [[kubernetes-architecture]] - composants du cluster et réseau
- [[kubernetes-services-and-networking]] - Services, Ingress, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass
- [[kubernetes-resource-management]] - requests, limits, autoscaling
- [[helm-package-manager]] - déploiements templatisés
