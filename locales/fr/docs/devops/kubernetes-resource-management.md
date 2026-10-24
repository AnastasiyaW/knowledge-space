---
title: "Gestion des ressources Kubernetes"
category: concepts
tags: [devops, kubernetes, resources, limits, quotas, autoscaling, hpa, namespaces]
level: 3
source_sha256: e692cdccb21ec87b00b0770a5e49f7b756a03aeecefd5985bc8b1abfa648535c
translation: machine
translated_at: '2026-10-24'
---
# Gestion des ressources Kubernetes {#kubernetes-resource-management}

La gestion des ressources contrôle la manière dont le CPU et la mémoire sont alloués, consommés et bornés à l'échelle du cluster. Une configuration appropriée évite les voisins bruyants et garantit une répartition équitable des ressources.

## Requests et Limits {#requests-and-limits}

Définies par conteneur, et non par pod :

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "200m"
    memory: "256Mi"
```

- **Requests** - minimum garanti. Le scheduler utilise cette valeur pour décider du placement
- **Limits** - consommation maximale autorisée
- CPU en millicores : 1000m = 1 vCPU
- Mémoire en Mi/Gi

### Dépassement des limites {#exceeding-limits}

| Ressource | Comportement | Type |
|-----------|--------------|------|
| CPU | Throttling (pas de arrêt du conteneur) | Compressible - peut être redistribué |
| Mémoire | OOMKilled | Incompressible - récupérée uniquement en tuant le processus |

## Classes QoS {#qos-classes}

Attribuées automatiquement selon la configuration des requests et limits. Déterminent la priorité d'éviction (BestEffort en premier, Guaranteed en dernier) :

| Classe | Condition | Cas d'usage |
|--------|-----------|-------------|
| **Guaranteed** | Tous les conteneurs : limits == requests pour le CPU et la mémoire | Bases de données, services critiques |
| **Burstable** | Au moins un conteneur : requests < limits | Services web, applications à charge variable |
| **BestEffort** | Aucune request ni limit définie | Environnements de test uniquement |

## Namespaces {#namespaces}

Clusters virtuels au sein d'un cluster physique. Ils fournissent une frontière d'isolation et un contrôle des ressources par namespace.

```bash
kubectl create namespace dev
kubectl apply -f manifest.yaml -n dev
kubectl get pods -n dev
kubectl delete ns dev           # deletes namespace + ALL contents
```

**Namespaces par défaut** : `default`, `kube-system` (CoreDNS, kube-proxy, metrics-server), `kube-public`, `kube-node-lease`.

Le même manifeste peut être déployé dans plusieurs namespaces sans modifier les noms : il suffit d'utiliser `-n <namespace>`.

## LimitRange {#limitrange}

Politique par conteneur au sein d'un namespace. Elle attribue des valeurs par défaut et impose des minimums et maximums :

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

Les pods qui ne respectent pas le LimitRange sont rejetés à leur création.

## ResourceQuota {#resourcequota}

Budget global du namespace pour la consommation agrégée des ressources :

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

Les nouveaux pods échouent avec « exceeded quota » lorsque les totaux du namespace sont atteints.

**Distinction clé** : LimitRange = politique par conteneur. ResourceQuota = budget à l'échelle du namespace. Ils fonctionnent ensemble.

## Horizontal Pod Autoscaler (HPA) {#horizontal-pod-autoscaler-hpa}

Adapte le nombre de réplicas de pods en fonction de l'utilisation du CPU et de la mémoire. Nécessite Metrics Server.

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

- Montée en charge : immédiate dès que la cible est dépassée
- Descente en charge : temporisation de 5 minutes
- Nécessite que des resource requests soient définies sur les conteneurs

## Cluster Autoscaler {#cluster-autoscaler}

Adapte le nombre de nœuds workers en fonction de la demande des pods en attente :

```bash
az aks create --enable-cluster-autoscaler --min-count 1 --max-count 5
```

- Provisionne de nouveaux nœuds lorsque des pods ne peuvent pas être planifiés (1 à 3 minutes)
- Retire les nœuds sous-utilisés après une période de refroidissement
- Les requests/limits de ressources déterminent la décision : de grosses requests forcent l'ajout de nœuds plus rapidement

### HPA et Cluster Autoscaler combinés {#hpa-cluster-autoscaler-together}

HPA augmente le nombre de pods -> ressources de nœuds insuffisantes -> le cluster autoscaler ajoute des nœuds -> les pods sont planifiés. Processus inverse lors de la réduction.

## Sélecteurs de nœuds {#node-selectors}

Planifie les pods sur des pools de nœuds spécifiques :

```yaml
spec:
  nodeSelector:
    nodepoolos: linux           # Linux user pool
    # OR
    kubernetes.io/os: windows   # Windows pool
    # OR
    type: virtual-kubelet       # Virtual nodes (ACI/Fargate)
```

## Pièges à éviter {#gotchas}

- Sans requests, le scheduler ne dispose d'aucune information pour le placement : les pods sont placés au hasard
- Sans limits mémoire, un seul conteneur peut provoquer un OOMKill de tout le nœud
- Si `default` n'est pas spécifié pour le CPU dans le LimitRange, le système attribue 1 vCPU (1000m) par conteneur
- Un ResourceQuota atteint bloque la montée en charge : les nouveaux pods restent en Pending
- Metrics Server doit être en cours d'exécution pour que le HPA fonctionne (activé par défaut sur les offres Kubernetes managées)
- Ne supprimez jamais le namespace `default`

## Voir aussi {#see-also}

- [[kubernetes-architecture]] - composants du cluster
- [[kubernetes-workloads]] - pods, deployments
- [[kubernetes-on-aks]] - gestion des ressources spécifique à AKS
- [[kubernetes-on-eks]] - autoscaling spécifique à EKS
