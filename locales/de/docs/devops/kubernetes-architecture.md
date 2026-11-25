---
title: "Kubernetes-Architektur"
category: concepts
tags: [devops, kubernetes, k8s, control-plane, worker-nodes, cluster]
level: 4
source_sha256: 15f36047512050ecc93c69775db4a29a8caeac24ef06349be422fe898cca7432
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes-Architektur {#kubernetes-architecture}

Kubernetes (K8s) ist die branchenweit etablierte Plattform zur Orchestrierung von Containern. Sie verwaltet containerisierte Workloads über Cluster aus mehreren Maschinen hinweg und bietet automatisiertes Deployment, Skalierung und Self-Healing.

## Cluster-Komponenten {#cluster-components}

### Control Plane {#control-plane}

| Komponente | Funktion |
|-----------|----------|
| **API Server** (kube-apiserver) | Zentraler REST-Endpunkt. Sämtliche Kommunikation läuft über ihn. Validiert Anfragen und speichert den Zustand in etcd |
| **etcd** | Verteilter Key-Value-Store. Single Source of Truth für den gesamten Cluster-Zustand |
| **Controller Manager** | Führt Kontrollschleifen aus, die auf Zustandsänderungen achten und Korrekturmaßnahmen einleiten |
| **Scheduler** | Weist Pods auf Basis verfügbarer Ressourcen und Platzierungsrichtlinien Nodes zu |

### Controller im Controller Manager {#controllers-in-controller-manager}

| Controller | Funktion |
|-----------|----------|
| Deployment Controller | Verwaltet den Lebenszyklus von Deployments und skaliert ReplicaSets |
| ReplicaSet Controller | Hält die gewünschte Anzahl an Pods aufrecht |
| Node Controller | Überwacht den Zustand der Nodes, markiert sie als NotReady und verlagert Pods |
| Service Controller | Aktualisiert Load Balancer und Endpoints |
| Job/CronJob Controller | Führt einmalige und zeitgesteuerte Aufgaben aus |

### Worker-Node-Komponenten {#worker-node-components}

| Komponente | Funktion |
|-----------|----------|
| **Kubelet** | Verwaltet den Lebenszyklus der Pods auf dem Node. Kommuniziert mit der Container Runtime und meldet den Status an den API Server |
| **Container Runtime** | Führt Container aus (containerd, CRI-O) |
| **Kube-proxy** | Übernimmt das Service-Routing. Konfiguriert Netzwerkregeln (iptables/IPVS) |

### Kube-proxy-Modi {#kube-proxy-modes}

| Modus | Mechanismus | Performance |
|------|-----------|-------------|
| userspace | Proxy-Prozess pro Verbindung | Am langsamsten |
| iptables | Linux-netfilter-Regeln | Standard (Default) |
| IPVS | Im Kernel laufender L4-Load-Balancer | Am besten für große Cluster |

## Netzwerkmodell {#networking-model}

- Jeder Pod erhält eine eindeutige IP-Adresse
- Pods kommunizieren direkt ohne NAT, auch über Nodes hinweg
- Nodes können mit Pods auf anderen Nodes kommunizieren

### CNI-Plugins {#cni-plugins}

| Plugin | Wichtigstes Merkmal |
|--------|-------------|
| Calico | L3-Networking, Network Policies, Sicherheit |
| Flannel | Einfaches Overlay-Netzwerk (VXLAN-basiert) |
| Cilium | Auf eBPF basierendes Networking und Sicherheit |
| Weave Net | Verschlüsselter Datenverkehr zwischen Nodes |

## Kubernetes vs. Docker Swarm {#kubernetes-vs-docker-swarm}

| Aspekt | Docker Swarm | Kubernetes |
|--------|-------------|------------|
| Einrichtung | Nativ in Docker, `swarm init` | Separate Installation oder Managed Service |
| Cloud-Anbieter | Keine verwalteten Angebote | EKS, GKE, AKS verfügbar |
| Auto-Scaling | Manuell | Integriert: HPA, Cluster Autoscaler |
| Rolling Updates | Eingeschränkt | Native Strategien, einfaches Rollback |
| Runtime | Nur Docker | containerd, CRI-O |

## Methoden zur Cluster-Bereitstellung {#cluster-deployment-methods}

### Managed Kubernetes (Produktion) {#managed-kubernetes-production}

- **AWS EKS** - `eksctl create cluster --name mycluster --region us-east-1`
- **Azure AKS** - `az aks create --resource-group myRG --name myCluster`
- **Google GKE** - `gcloud container clusters create my-cluster`

Die Cloud übernimmt Control Plane, etcd, Upgrades und Skalierung.

### Self-Managed {#self-managed}

- **kubeadm** - Standard-Werkzeug zur Initialisierung. `kubeadm init` auf dem Master, `kubeadm join` auf den Workern
- **kubespray** - Auf Ansible basierend, stärker automatisiert für Multi-Node-Setups

### Lokale Entwicklung {#local-development}

```bash
minikube start              # start local cluster
minikube status             # check status
minikube service <svc>      # access NodePort service
minikube dashboard          # K8s dashboard UI
```

## kubectl-Grundlagen {#kubectl-essentials}

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

## Stolperfallen {#gotchas}

- `kubectl` liest die Konfiguration aus `$HOME/.kube/config` - mit `kubectl config` lassen sich mehrere Cluster verwalten
- Den `default`-Namespace niemals löschen - er enthält den Standard-ClusterIP-Service von K8s
- Immer Resource Requests und Limits setzen - ohne sie erhalten Pods die QoS-Klasse BestEffort und werden als Erste verdrängt
- Auch bei Managed-K8s-Clustern müssen Worker-Nodes, Storage und Networking selbst verwaltet werden

## Siehe auch {#see-also}

- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets, DaemonSets
- [[kubernetes-services-and-networking]] - Services, Ingress, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass
- [[kubernetes-resource-management]] - requests, limits, QoS, Autoscaling
- [[helm-package-manager]] - Paketverwaltung für Kubernetes
