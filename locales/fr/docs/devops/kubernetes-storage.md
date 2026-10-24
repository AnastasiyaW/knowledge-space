---
title: "Stockage Kubernetes"
category: concepts
tags: [devops, kubernetes, storage, pv, pvc, storageclass, volumes, csi]
level: 3
source_sha256: 4a27467403c938acb638bf81a1c31fcea143b0046ba5c668201d713b6ff4f7ba
translation: machine
translated_at: '2026-10-24'
---
# Stockage Kubernetes {#kubernetes-storage}

Par défaut, les conteneurs sont éphémères : les données sont perdues lors du redémarrage, de la mise à jour ou de la migration d'un pod. Kubernetes fournit une couche d'abstraction du stockage à travers les Volumes, les PersistentVolumes et les StorageClasses.

## Types de volumes {#volume-types}

| Type | Portée | Cas d'usage |
|------|--------|-------------|
| emptyDir | Durée de vie du pod | Cache temporaire, espace de travail partagé entre conteneurs |
| hostPath | Système de fichiers du nœud | Tests uniquement : données perdues si le pod migre vers un autre nœud |
| PersistentVolume | Ensemble du cluster | Bases de données, applications avec état |
| Spécifique au cloud | Géré par le fournisseur | EBS, EFS, Azure Disk, Azure Files |

## PersistentVolume (PV) et PersistentVolumeClaim (PVC) {#persistentvolume-pv-and-persistentvolumeclaim-pvc}

**PV** : ressource à l'échelle du cluster représentant un stockage physique. Créé par un administrateur ou provisionné dynamiquement.

**PVC** : demande de stockage émise par un utilisateur. Kubernetes lie automatiquement le PVC à un PV approprié.

```yaml
# PV - provisioned by admin
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-data
spec:
  capacity:
    storage: 5Gi
  accessModes: [ReadWriteOnce]
  hostPath:
    path: /data/pv
---
# PVC - requested by developer
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-data
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 5Gi
```

### Modes d'accès {#access-modes}

| Mode | Description | Support de stockage |
|------|-------------|---------------------|
| ReadWriteOnce (RWO) | Lecture-écriture sur un seul nœud | EBS, Azure Disk |
| ReadOnlyMany (ROX) | Lecture seule sur plusieurs nœuds | NFS, Azure Files |
| ReadWriteMany (RWX) | Lecture-écriture sur plusieurs nœuds | EFS, Azure Files, NFS |
| ReadWriteOncePod (RWOP) | Un seul pod uniquement | Pilotes CSI |

### Politiques de récupération {#reclaim-policies}

| Politique | Comportement |
|-----------|--------------|
| Retain | PV conservé après suppression du PVC |
| Delete | PV supprimé avec le PVC (par défaut pour le provisionnement dynamique) |
| Recycle | Données effacées, PV réutilisable (obsolète) |

## StorageClass {#storageclass}

Définit une « classe » de stockage pour le provisionnement dynamique. Aucune intervention de l'administrateur n'est nécessaire.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium-retain
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Premium_LRS
  kind: Managed
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
```

### Modes de liaison des volumes {#volume-binding-modes}

- `Immediate` (par défaut) : le PV est créé et lié dès la création du PVC
- `WaitForFirstConsumer` : la liaison du PV est différée jusqu'à la planification du pod (préférable pour un stockage tenant compte de la topologie)

## CSI (Container Storage Interface) {#csi-container-storage-interface}

Architecture basée sur des plugins, remplaçant les pilotes de stockage intégrés (in-tree) :

- **AWS EBS CSI** : `ebs.csi.aws.com` : RWO, une seule AZ, stockage bloc
- **AWS EFS CSI** : `efs.csi.aws.com` : RWX, multi-AZ, stockage fichier
- **Azure Disk** : `kubernetes.io/azure-disk` : RWO, un seul nœud
- **Azure Files** : provisionneur `azurefile` : RWX, plusieurs pods

### EBS vs EFS sur AWS {#ebs-vs-efs-on-aws}

| Caractéristique | EBS | EFS |
|-----------------|-----|-----|
| Type | Stockage bloc | Stockage fichier |
| Accès | RWO, une seule AZ | RWX, multi-AZ |
| Performance | Plus rapide | Latence plus élevée |
| Coût | Moins cher | Plus cher |
| Cas d'usage | Bases de données | Configurations partagées, contenu statique |

## Modèles spécifiques au cloud {#cloud-specific-patterns}

### Azure Disk (AKS) {#azure-disk-aks}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: managed-premium-retain
  resources:
    requests:
      storage: 5Gi
```

Limitation : RWO uniquement. Le pod et le PVC doivent se trouver dans la même zone de disponibilité.

### Azure Files (AKS) {#azure-files-aks}

```yaml
spec:
  accessModes: [ReadWriteMany]
  storageClassName: azurefile
  resources:
    requests:
      storage: 5Gi
```

Plusieurs pods peuvent le monter simultanément.

### Montage dans les pods {#mounting-in-pods}

```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: data-vol
      mountPath: /var/lib/mysql
  volumes:
  - name: data-vol
    persistentVolumeClaim:
      claimName: mysql-pvc
```

## Modèle de volume pour StatefulSet {#statefulset-volume-pattern}

Chaque pod obtient son propre PVC via volumeClaimTemplates :

```yaml
apiVersion: apps/v1
kind: StatefulSet
spec:
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ReadWriteOnce]
      resources:
        requests:
          storage: 5Gi
```

Les PVC persistent lors des redémarrages et des replanifications des pods.

## Pièges à éviter {#gotchas}

- Azure Disk = RWO uniquement. Impossible de le monter sur plusieurs nœuds simultanément
- Les volumes EBS sont liés à une AZ. Une migration de pod entre AZ entraîne une perte d'accès
- `WaitForFirstConsumer` est recommandé pour le stockage cloud afin de garantir que le PV est créé dans la même zone que le pod
- La StorageClass par défaut ne fonctionne parfois que sur le pool de nœuds système : créez une StorageClass personnalisée pour les pools de nœuds utilisateurs
- Les ConfigMaps montées en volumes se mettent à jour automatiquement, mais pas les variables d'environnement issues de ConfigMaps

## Voir aussi {#see-also}

- [[kubernetes-workloads]] : StatefulSets, ConfigMaps, Secrets
- [[kubernetes-resource-management]] : quotas de ressources, y compris les limites de PVC
- [[kubernetes-on-aks]] : détails sur le stockage Azure
- [[kubernetes-on-eks]] : détails sur le stockage AWS
