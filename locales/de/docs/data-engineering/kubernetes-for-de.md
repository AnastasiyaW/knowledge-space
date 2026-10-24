---
title: "Kubernetes für Data Engineering"
category: tools
tags: [data-engineering, kubernetes, k8s, orchestration, spark-on-k8s]
level: 3
source_sha256: cc9521f6190d062523afc4b172c9e5a61f27519721c64fddcde71f1ceed2beaa
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes für Data Engineering {#kubernetes-for-data-engineering}

Kubernetes orchestriert containerisierte Workloads in großem Maßstab. Für Data Engineering stellt es die Compute-Schicht bereit, wenn Storage (S3) und Compute getrennt werden, und betreibt Spark, Airflow und JupyterHub.

## Architektur {#architecture}

**Control Plane:** API Server (zentraler Knotenpunkt), etcd (verteilter KV-Store), Scheduler, Controller Manager

**Worker Nodes:** kubelet, kube-proxy, Container Runtime (containerd, CRI-O)

## Zentrale Abstraktionen {#core-abstractions}

| Abstraktion | Anwendungsfall |
|-------------|----------------|
| **Pod** | Kleinste deploybare Einheit |
| **Deployment** | Produktionsanwendungen mit Rolling Updates |
| **StatefulSet** | Zustandsbehaftete Anwendungen (Datenbanken) |
| **Service** | Netzwerkfreigabe (ClusterIP, NodePort, LoadBalancer) |
| **ConfigMap** | Anwendungskonfiguration |
| **Secret** | Sensible Daten |
| **PersistentVolume + PVC** | Speicher, der Pod-Neustarts übersteht |

## kubectl-Spickzettel {#kubectl-cheatsheet}

```bash
kubectl get pods -n namespace
kubectl describe pod <name>
kubectl logs <pod-name>
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
```

## Spark on Kubernetes {#spark-on-kubernetes}

Produktionsreif seit Spark 3.1 (März 2021).

```bash
helm install my-release spark-operator/spark-operator \
  --namespace spark-operator --create-namespace \
  --set webhook.enable=true --version 1.1.11
```

**Die Version des Spark Operators immer fixieren.** Die neueste Version kann Breaking Changes enthalten.

## Cloud-native Data-Architektur {#cloud-native-data-architecture}

```text
Storage Layer: S3 (or compatible)
Compute Layer: Kubernetes (Spark, Presto, Airflow)
```

Diese Trennung ermöglicht elastische Compute-Ressourcen unabhängig vom Storage.

## Wichtige Fakten {#key-facts}
- Das Container-Dateisystem ist flüchtig – für persistente Daten PV/PVC oder S3 verwenden
- etcd reagiert empfindlich auf Netzwerklatenz
- **Cluster nach der Nutzung immer pausieren**, um Kosten zu sparen
- Spark History Server zur Inspektion von Job-Logs nutzen

## Fallstricke {#gotchas}
- Alle Helm-Chart-Versionen fixieren, um Reproduzierbarkeit sicherzustellen
- Die Performance von etcd leidet unter datacenterübergreifender Latenz
- Pod-Ressourcenlimits müssen gesetzt werden, um Noisy-Neighbor-Probleme zu verhindern
- Die Kubernetes-Clusterversion ist relevant – Kompatibilität mit Spark-/Airflow-Versionen testen

## Siehe auch {#see-also}
- [[docker-for-de]] - Container-Grundlagen
- [[apache-spark-core]] - Details zu Spark on K8s
- [[cloud-data-platforms]] - Cloud-Infrastruktur
- [[yarn-resource-management]] - traditionelle Alternative
