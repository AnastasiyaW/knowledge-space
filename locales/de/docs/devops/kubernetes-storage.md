---
title: "Kubernetes Storage"
category: concepts
tags: [devops, kubernetes, storage, pv, pvc, storageclass, volumes, csi]
level: 3
source_sha256: 4a27467403c938acb638bf81a1c31fcea143b0046ba5c668201d713b6ff4f7ba
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes Storage {#kubernetes-storage}

Container sind standardmäßig flüchtig: Daten gehen bei einem Neustart, Update oder einer Migration des Pods verloren. Kubernetes stellt eine Storage-Abstraktionsschicht über Volumes, PersistentVolumes und StorageClasses bereit.

## Volume-Typen {#volume-types}

| Typ | Geltungsbereich | Anwendungsfall |
|------|-----------------|----------------|
| emptyDir | Lebensdauer des Pods | Temporärer Cache, gemeinsam genutzter Scratch-Speicher zwischen Containern |
| hostPath | Node-Dateisystem | Nur für Tests - Daten gehen verloren, wenn der Pod auf einen anderen Node wechselt |
| PersistentVolume | Clusterweit | Datenbanken, zustandsbehaftete Anwendungen |
| Cloud-spezifisch | Vom Provider verwaltet | EBS, EFS, Azure Disk, Azure Files |

## PersistentVolume (PV) und PersistentVolumeClaim (PVC) {#persistentvolume-pv-and-persistentvolumeclaim-pvc}

**PV** - clusterweite Ressource, die physischen Speicher repräsentiert. Wird vom Administrator angelegt oder dynamisch bereitgestellt.

**PVC** - Speicheranforderung eines Benutzers. Kubernetes bindet den PVC automatisch an einen passenden PV.

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

### Access Modes {#access-modes}

| Modus | Beschreibung | Unterstützung durch Storage |
|------|-------------|-----------------|
| ReadWriteOnce (RWO) | Lesen und Schreiben auf einem einzelnen Node | EBS, Azure Disk |
| ReadOnlyMany (ROX) | Nur Lesen auf mehreren Nodes | NFS, Azure Files |
| ReadWriteMany (RWX) | Lesen und Schreiben auf mehreren Nodes | EFS, Azure Files, NFS |
| ReadWriteOncePod (RWOP) | Nur ein einzelner Pod | CSI-Treiber |

### Reclaim Policies {#reclaim-policies}

| Policy | Verhalten |
|--------|----------|
| Retain | PV bleibt nach dem Löschen des PVC erhalten |
| Delete | PV wird zusammen mit dem PVC gelöscht (Standard bei dynamischer Bereitstellung) |
| Recycle | Daten werden gelöscht, PV ist wiederverwendbar (veraltet) |

## StorageClass {#storageclass}

Definiert eine Storage-"Klasse" für die dynamische Bereitstellung. Ein Eingreifen des Administrators ist nicht erforderlich.

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

### Volume Binding Modes {#volume-binding-modes}

- `Immediate` (Standard) - PV wird beim Anlegen des PVC erstellt und gebunden
- `WaitForFirstConsumer` - Bindung des PV wird verzögert, bis der Pod eingeplant ist (besser für topologiebewussten Storage)

## CSI (Container Storage Interface) {#csi-container-storage-interface}

Plugin-basierte Architektur, die In-Tree-Storage-Treiber ersetzt:

- **AWS EBS CSI**: `ebs.csi.aws.com` - RWO, einzelne AZ, Block-Storage
- **AWS EFS CSI**: `efs.csi.aws.com` - RWX, Multi-AZ, Datei-Storage
- **Azure Disk**: `kubernetes.io/azure-disk` - RWO, einzelner Node
- **Azure Files**: `azurefile`-Provisioner - RWX, mehrere Pods

### EBS vs. EFS auf AWS {#ebs-vs-efs-on-aws}

| Merkmal | EBS | EFS |
|---------|-----|-----|
| Typ | Block-Storage | Datei-Storage |
| Zugriff | RWO, einzelne AZ | RWX, Multi-AZ |
| Geschwindigkeit | Schneller | Höhere Latenz |
| Kosten | Günstiger | Teurer |
| Anwendungsfall | Datenbanken | Gemeinsame Konfigurationen, statische Inhalte |

## Cloud-spezifische Muster {#cloud-specific-patterns}

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

Einschränkung: nur RWO. Pod und PVC müssen in derselben Availability Zone liegen.

### Azure Files (AKS) {#azure-files-aks}

```yaml
spec:
  accessModes: [ReadWriteMany]
  storageClassName: azurefile
  resources:
    requests:
      storage: 5Gi
```

Mehrere Pods können gleichzeitig mounten.

### Mounting in Pods {#mounting-in-pods}

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

## StatefulSet-Volume-Muster {#statefulset-volume-pattern}

Jeder Pod erhält seinen eigenen PVC über volumeClaimTemplates:

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

PVCs bleiben über Neustarts und Neuplanungen von Pods hinweg erhalten.

## Stolperfallen {#gotchas}

- Azure Disk = nur RWO. Kann nicht gleichzeitig auf mehreren Nodes gemountet werden
- EBS-Volumes sind an eine AZ gebunden. Eine Migration des Pods über AZs hinweg verliert den Zugriff
- `WaitForFirstConsumer` wird für Cloud-Storage empfohlen, damit der PV in derselben Zone wie der Pod erstellt wird
- Die Standard-StorageClass funktioniert möglicherweise nur auf dem Node-Pool des Systems - für Benutzer-Node-Pools eine eigene StorageClass anlegen
- ConfigMaps, die als Volumes gemountet sind, werden automatisch aktualisiert, Umgebungsvariablen aus ConfigMaps dagegen NICHT

## Siehe auch {#see-also}

- [[kubernetes-workloads]] - StatefulSets, ConfigMaps, Secrets
- [[kubernetes-resource-management]] - Ressourcenquoten einschließlich PVC-Limits
- [[kubernetes-on-aks]] - Details zu Azure-Storage
- [[kubernetes-on-eks]] - Details zu AWS-Storage
