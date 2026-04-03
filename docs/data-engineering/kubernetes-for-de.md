---
title: Kubernetes for Data Engineering
category: tools
tags: [data-engineering, kubernetes, k8s, orchestration, spark-on-k8s]
---

# Kubernetes for Data Engineering

Kubernetes orchestrates containerized workloads at scale. For DE, it provides the compute layer when separating storage (S3) and compute, running Spark, Airflow, JupyterHub.

## Architecture

**Control Plane:** API Server (central hub), etcd (distributed KV store), Scheduler, Controller Manager

**Worker Nodes:** kubelet, kube-proxy, container runtime (containerd, CRI-O)

## Core Abstractions

| Abstraction | Use Case |
|-------------|----------|
| **Pod** | Smallest deployable unit |
| **Deployment** | Production apps with rolling updates |
| **StatefulSet** | Stateful apps (databases) |
| **Service** | Network exposure (ClusterIP, NodePort, LoadBalancer) |
| **ConfigMap** | Application configuration |
| **Secret** | Sensitive data |
| **PersistentVolume + PVC** | Storage surviving pod restarts |

## kubectl Cheatsheet

```bash
kubectl get pods -n namespace
kubectl describe pod <name>
kubectl logs <pod-name>
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
```

## Spark on Kubernetes

Production-ready since Spark 3.1 (March 2021).

```bash
helm install my-release spark-operator/spark-operator \
  --namespace spark-operator --create-namespace \
  --set webhook.enable=true --version 1.1.11
```

**Always pin Spark Operator version.** Latest may have breaking changes.

## Cloud-Native Data Architecture

```
Storage Layer: S3 (or compatible)
Compute Layer: Kubernetes (Spark, Presto, Airflow)
```

Separation enables elastic compute independent of storage.

## Key Facts
- Container filesystem is ephemeral - use PV/PVC or S3 for persistent data
- etcd is sensitive to network latency
- **Always pause clusters after use** to save costs
- Spark History Server for job log inspection

## Gotchas
- Pin all Helm chart versions for reproducibility
- etcd performance degrades with cross-datacenter latency
- Pod resource limits must be set to prevent noisy-neighbor issues
- K8s cluster version matters - test compatibility with Spark/Airflow versions

## See Also
- [[docker-for-de]] - container basics
- [[apache-spark-core]] - Spark on K8s details
- [[cloud-data-platforms]] - cloud infrastructure
- [[yarn-resource-management]] - traditional alternative
