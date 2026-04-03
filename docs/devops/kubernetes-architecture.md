---
title: Kubernetes Architecture
category: concepts
tags: [devops, kubernetes, k8s, control-plane, worker-nodes, cluster]
---

# Kubernetes Architecture

Kubernetes (K8s) is the industry-standard container orchestration platform. It manages containerized workloads across clusters of machines, providing automated deployment, scaling, and self-healing.

## Cluster Components

### Control Plane

| Component | Function |
|-----------|----------|
| **API Server** (kube-apiserver) | Central REST endpoint. All communication goes through it. Validates requests, stores state in etcd |
| **etcd** | Distributed key-value store. Source of truth for all cluster state |
| **Controller Manager** | Runs control loops watching for state changes and taking corrective actions |
| **Scheduler** | Assigns pods to nodes based on resource availability and placement policies |

### Controllers in Controller Manager

| Controller | Function |
|-----------|----------|
| Deployment Controller | Manages deployment lifecycle, scales ReplicaSets |
| ReplicaSet Controller | Maintains desired pod count |
| Node Controller | Monitors node health, marks NotReady, evacuates pods |
| Service Controller | Updates load balancers and endpoints |
| Job/CronJob Controller | Runs one-shot and scheduled tasks |

### Worker Node Components

| Component | Function |
|-----------|----------|
| **Kubelet** | Manages pod lifecycle on the node. Communicates with container runtime, reports status to API server |
| **Container Runtime** | Executes containers (containerd, CRI-O) |
| **Kube-proxy** | Handles service routing. Configures network rules (iptables/IPVS) |

### Kube-proxy Modes

| Mode | Mechanism | Performance |
|------|-----------|-------------|
| userspace | Proxy process per connection | Slowest |
| iptables | Linux netfilter rules | Standard (default) |
| IPVS | In-kernel L4 load balancer | Best for large clusters |

## Networking Model

- Every pod gets a unique IP address
- Pods communicate directly without NAT, even across nodes
- Nodes can communicate with pods on other nodes

### CNI Plugins

| Plugin | Key Feature |
|--------|-------------|
| Calico | L3 networking, network policies, security |
| Flannel | Simple overlay network (VXLAN-based) |
| Cilium | eBPF-based networking and security |
| Weave Net | Encrypted inter-node traffic |

## Kubernetes vs Docker Swarm

| Aspect | Docker Swarm | Kubernetes |
|--------|-------------|------------|
| Setup | Native Docker, `swarm init` | Separate installation or managed service |
| Cloud providers | No managed offerings | EKS, GKE, AKS everywhere |
| Auto-scaling | Manual | Built-in HPA, cluster autoscaler |
| Rolling updates | Limited | Native strategies, easy rollback |
| Runtime | Docker only | containerd, CRI-O |

## Cluster Deployment Methods

### Managed Kubernetes (Production)

- **AWS EKS** - `eksctl create cluster --name mycluster --region us-east-1`
- **Azure AKS** - `az aks create --resource-group myRG --name myCluster`
- **Google GKE** - `gcloud container clusters create my-cluster`

Cloud handles control plane, etcd, upgrades, and scaling.

### Self-Managed

- **kubeadm** - standard bootstrapping tool. `kubeadm init` on master, `kubeadm join` on workers
- **kubespray** - Ansible-based, more automated for multi-node setups

### Local Development

```bash
minikube start              # start local cluster
minikube status             # check status
minikube service <svc>      # access NodePort service
minikube dashboard          # K8s dashboard UI
```

## kubectl Essentials

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

## Gotchas

- `kubectl` reads config from `$HOME/.kube/config` - use `kubectl config` to manage multiple clusters
- Never delete the `default` namespace - contains default K8s ClusterIP service
- Always set resource requests/limits - without them, pods get BestEffort QoS and are first to be evicted
- Managed K8s clusters still require managing worker nodes, storage, and networking

## See Also

- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets, DaemonSets
- [[kubernetes-services-and-networking]] - Services, Ingress, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass
- [[kubernetes-resource-management]] - requests, limits, QoS, autoscaling
- [[helm-package-manager]] - Kubernetes package management
