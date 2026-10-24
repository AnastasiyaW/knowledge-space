---
title: "Kubernetes pour l'ingénierie des données"
category: tools
tags: [data-engineering, kubernetes, k8s, orchestration, spark-on-k8s]
level: 3
source_sha256: cc9521f6190d062523afc4b172c9e5a61f27519721c64fddcde71f1ceed2beaa
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes pour l'ingénierie des données {#kubernetes-for-data-engineering}

Kubernetes orchestre des charges de travail conteneurisées à grande échelle. Pour l'ingénierie des données (DE), il fournit la couche de calcul lorsque le stockage (S3) et le calcul sont séparés, en exécutant Spark, Airflow, JupyterHub.

## Architecture {#architecture}

**Plan de contrôle :** API Server (point central), etcd (magasin clé-valeur distribué), Scheduler, Controller Manager

**Nœuds de travail :** kubelet, kube-proxy, runtime de conteneurs (containerd, CRI-O)

## Abstractions principales {#core-abstractions}

| Abstraction | Cas d'usage |
|-------------|----------|
| **Pod** | Plus petite unité déployable |
| **Deployment** | Applications en production avec mises à jour progressives |
| **StatefulSet** | Applications avec état (bases de données) |
| **Service** | Exposition réseau (ClusterIP, NodePort, LoadBalancer) |
| **ConfigMap** | Configuration applicative |
| **Secret** | Données sensibles |
| **PersistentVolume + PVC** | Stockage survivant aux redémarrages de pods |

## Aide-mémoire kubectl {#kubectl-cheatsheet}

```bash
kubectl get pods -n namespace
kubectl describe pod <name>
kubectl logs <pod-name>
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
```

## Spark sur Kubernetes {#spark-on-kubernetes}

Prêt pour la production depuis Spark 3.1 (mars 2021).

```bash
helm install my-release spark-operator/spark-operator \
  --namespace spark-operator --create-namespace \
  --set webhook.enable=true --version 1.1.11
```

**Épinglez toujours la version du Spark Operator.** La dernière version peut introduire des changements incompatibles.

## Architecture de données cloud-native {#cloud-native-data-architecture}

```text
Storage Layer: S3 (or compatible)
Compute Layer: Kubernetes (Spark, Presto, Airflow)
```

La séparation permet un calcul élastique indépendant du stockage.

## Points clés {#key-facts}
- Le système de fichiers du conteneur est éphémère : utilisez PV/PVC ou S3 pour les données persistantes
- etcd est sensible à la latence réseau
- **Mettez toujours les clusters en pause après utilisation** pour réduire les coûts
- Spark History Server pour l'inspection des journaux de jobs

## Pièges à éviter {#gotchas}
- Épinglez toutes les versions des charts Helm pour garantir la reproductibilité
- Les performances d'etcd se dégradent avec la latence inter-datacenters
- Les limites de ressources des pods doivent être définies pour éviter les problèmes de voisinage bruyant (noisy neighbor)
- La version du cluster K8s compte : testez la compatibilité avec les versions de Spark/Airflow

## Voir aussi {#see-also}
- [[docker-for-de]] - notions de base sur Docker
- [[apache-spark-core]] - détails sur Spark sur K8s
- [[cloud-data-platforms]] - infrastructure cloud
- [[yarn-resource-management]] - alternative traditionnelle
