---
title: Kubernetes Storage
category: concepts
tags: [devops, kubernetes, storage, pv, pvc, storageclass, volumes, csi]
---

# Kubernetes Storage

Containers are ephemeral by default - data lost on pod restart, update, or migration. Kubernetes provides a storage abstraction layer through Volumes, PersistentVolumes, and StorageClasses.

## Volume Types

| Type | Scope | Use Case |
|------|-------|----------|
| emptyDir | Pod lifetime | Temp cache, shared scratch space between containers |
| hostPath | Node filesystem | Testing only - data lost if pod moves to another node |
| PersistentVolume | Cluster-wide | Databases, stateful apps |
| Cloud-specific | Provider-managed | EBS, EFS, Azure Disk, Azure Files |

## PersistentVolume (PV) and PersistentVolumeClaim (PVC)

**PV** - cluster-wide resource representing physical storage. Created by admin or dynamically provisioned.

**PVC** - user request for storage. Kubernetes binds PVC to suitable PV automatically.

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

### Access Modes

| Mode | Description | Storage Support |
|------|-------------|-----------------|
| ReadWriteOnce (RWO) | Single node read-write | EBS, Azure Disk |
| ReadOnlyMany (ROX) | Multiple nodes read-only | NFS, Azure Files |
| ReadWriteMany (RWX) | Multiple nodes read-write | EFS, Azure Files, NFS |
| ReadWriteOncePod (RWOP) | Single pod only | CSI drivers |

### Reclaim Policies

| Policy | Behavior |
|--------|----------|
| Retain | PV preserved after PVC deletion |
| Delete | PV deleted with PVC (default for dynamic provisioning) |
| Recycle | Data wiped, PV reusable (deprecated) |

## StorageClass

Defines storage "class" for dynamic provisioning. No admin intervention needed.

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

### Volume Binding Modes

- `Immediate` (default) - PV created and bound when PVC created
- `WaitForFirstConsumer` - PV binding delayed until pod scheduled (better for topology-aware storage)

## CSI (Container Storage Interface)

Plugin-based architecture replacing in-tree storage drivers:

- **AWS EBS CSI**: `ebs.csi.aws.com` - RWO, single AZ, block storage
- **AWS EFS CSI**: `efs.csi.aws.com` - RWX, multi-AZ, file storage
- **Azure Disk**: `kubernetes.io/azure-disk` - RWO, single node
- **Azure Files**: `azurefile` provisioner - RWX, multiple pods

### EBS vs EFS on AWS

| Feature | EBS | EFS |
|---------|-----|-----|
| Type | Block storage | File storage |
| Access | RWO, single AZ | RWX, multi-AZ |
| Speed | Faster | Higher latency |
| Cost | Cheaper | More expensive |
| Use case | Databases | Shared configs, static content |

## Cloud-Specific Patterns

### Azure Disk (AKS)

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

Limitation: RWO only. Pod and PVC must be in same availability zone.

### Azure Files (AKS)

```yaml
spec:
  accessModes: [ReadWriteMany]
  storageClassName: azurefile
  resources:
    requests:
      storage: 5Gi
```

Multiple pods can mount simultaneously.

### Mounting in Pods

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

## StatefulSet Volume Pattern

Each pod gets its own PVC via volumeClaimTemplates:

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

PVCs persist across pod restarts and rescheduling.

## Gotchas

- Azure Disk = RWO only. Cannot mount on multiple nodes simultaneously
- EBS volumes are AZ-bound. Pod migration across AZs loses access
- `WaitForFirstConsumer` is recommended for cloud storage to ensure PV is created in the same zone as the pod
- Default StorageClass may only work on system node pool - create custom StorageClass for user node pools
- ConfigMaps mounted as volumes update automatically, but env vars from ConfigMaps do NOT

## See Also

- [[kubernetes-workloads]] - StatefulSets, ConfigMaps, Secrets
- [[kubernetes-resource-management]] - resource quotas including PVC limits
- [[kubernetes-on-aks]] - Azure storage details
- [[kubernetes-on-eks]] - AWS storage details
