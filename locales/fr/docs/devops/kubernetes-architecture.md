---
title: "Architecture de Kubernetes"
category: concepts
tags: [devops, kubernetes, k8s, control-plane, worker-nodes, cluster]
level: 4
source_sha256: 15f36047512050ecc93c69775db4a29a8caeac24ef06349be422fe898cca7432
translation: machine
translated_at: '2026-10-24'
---
# Architecture de Kubernetes {#kubernetes-architecture}

Kubernetes (K8s) est la plateforme d'orchestration de conteneurs de référence dans l'industrie. Il gère les charges de travail conteneurisées sur des clusters de machines, en assurant le déploiement automatisé, la mise à l'échelle et l'auto-réparation.

## Composants du cluster {#cluster-components}

### Control Plane {#control-plane}

| Composant | Fonction |
|-----------|----------|
| **API Server** (kube-apiserver) | Point d'entrée REST central. Toute communication passe par lui. Valide les requêtes et stocke l'état dans etcd |
| **etcd** | Magasin clé-valeur distribué. Source de vérité pour l'ensemble de l'état du cluster |
| **Controller Manager** | Exécute les boucles de contrôle qui surveillent les changements d'état et engagent des actions correctives |
| **Scheduler** | Affecte les pods aux nœuds en fonction des ressources disponibles et des politiques de placement |

### Contrôleurs du Controller Manager {#controllers-in-controller-manager}

| Contrôleur | Fonction |
|-----------|----------|
| Deployment Controller | Gère le cycle de vie des déploiements et met à l'échelle les ReplicaSets |
| ReplicaSet Controller | Maintient le nombre de pods souhaité |
| Node Controller | Surveille la santé des nœuds, marque les nœuds NotReady et évacue les pods |
| Service Controller | Met à jour les load balancers et les endpoints |
| Job/CronJob Controller | Exécute les tâches ponctuelles et planifiées |

### Composants des nœuds worker {#worker-node-components}

| Composant | Fonction |
|-----------|----------|
| **Kubelet** | Gère le cycle de vie des pods sur le nœud. Communique avec le container runtime et remonte le statut à l'API Server |
| **Container Runtime** | Exécute les conteneurs (containerd, CRI-O) |
| **Kube-proxy** | Gère le routage des services. Configure les règles réseau (iptables/IPVS) |

### Modes de kube-proxy {#kube-proxy-modes}

| Mode | Mécanisme | Performance |
|------|-----------|-------------|
| userspace | Processus proxy par connexion | La plus lente |
| iptables | Règles Linux netfilter | Standard (par défaut) |
| IPVS | Load balancer L4 dans le noyau | Idéal pour les grands clusters |

## Modèle réseau {#networking-model}

- Chaque pod reçoit une adresse IP unique
- Les pods communiquent directement, sans NAT, y compris entre nœuds
- Les nœuds peuvent communiquer avec les pods hébergés sur d'autres nœuds

### Plugins CNI {#cni-plugins}

| Plugin | Fonctionnalité clé |
|--------|-------------------|
| Calico | Réseau L3, network policies, sécurité |
| Flannel | Réseau overlay simple (basé sur VXLAN) |
| Cilium | Réseau et sécurité basés sur eBPF |
| Weave Net | Trafic inter-nœuds chiffré |

## Kubernetes vs Docker Swarm {#kubernetes-vs-docker-swarm}

| Aspect | Docker Swarm | Kubernetes |
|--------|-------------|------------|
| Installation | Intégré à Docker, `swarm init` | Installation séparée ou service managé |
| Fournisseurs cloud | Aucune offre managée | EKS, GKE, AKS disponibles partout |
| Mise à l'échelle automatique | Manuelle | HPA et cluster autoscaler intégrés |
| Mises à jour progressives | Limitées | Stratégies natives, rollback facile |
| Runtime | Docker uniquement | containerd, CRI-O |

## Méthodes de déploiement d'un cluster {#cluster-deployment-methods}

### Kubernetes managé (production) {#managed-kubernetes-production}

- **AWS EKS** - `eksctl create cluster --name mycluster --region us-east-1`
- **Azure AKS** - `az aks create --resource-group myRG --name myCluster`
- **Google GKE** - `gcloud container clusters create my-cluster`

Le cloud prend en charge le control plane, etcd, les mises à jour et la mise à l'échelle.

### Auto-géré {#self-managed}

- **kubeadm** - outil d'amorçage standard. `kubeadm init` sur le master, `kubeadm join` sur les workers
- **kubespray** - basé sur Ansible, plus automatisé pour les configurations multi-nœuds

### Développement local {#local-development}

```bash
minikube start              # start local cluster
minikube status             # check status
minikube service <svc>      # access NodePort service
minikube dashboard          # K8s dashboard UI
```

## Essentiels de kubectl {#kubectl-essentials}

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes -o wide
kubectl config get-contexts
kubectl config use-context <name>

# Resource operations
kubectl apply -f manifest.yaml
kubectl apply -f directory/              # all files in dir
kubectl apply -R -f directory/           # recursive
kubectl delete -f manifest.yaml
kubectl get all
kubectl get pods,svc,deploy
kubectl describe pod <name>
kubectl logs <pod> [-f]
kubectl exec -it <pod> -- /bin/bash
kubectl port-forward svc/my-svc 8080:80
```

## Points d'attention {#gotchas}

- `kubectl` lit sa configuration dans `$HOME/.kube/config` - utilisez `kubectl config` pour gérer plusieurs clusters
- Ne supprimez jamais le namespace `default` - il contient le service ClusterIP par défaut de K8s
- Définissez toujours les requests et limits de ressources - sans elles, les pods reçoivent une QoS BestEffort et sont les premiers évincés
- Les clusters K8s managés nécessitent tout de même de gérer les nœuds worker, le stockage et le réseau

## Voir aussi {#see-also}

- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets, DaemonSets
- [[kubernetes-services-and-networking]] - Services, Ingress, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass
- [[kubernetes-resource-management]] - requests, limits, QoS, autoscaling
- [[helm-package-manager]] - Gestion de paquets Kubernetes
