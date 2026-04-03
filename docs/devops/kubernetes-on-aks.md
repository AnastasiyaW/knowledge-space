---
title: Kubernetes on Azure (AKS)
category: patterns
tags: [devops, kubernetes, azure, aks, acr, azure-ad, rbac, monitoring]
---

# Kubernetes on Azure (AKS)

Azure Kubernetes Service is a managed K8s offering where Azure manages the control plane. Covers cluster creation, node pools, ACR integration, RBAC with Azure AD, and monitoring.

## Cluster Creation

```bash
az aks create \
  --resource-group $RG --name $CLUSTER \
  --kubernetes-version $VERSION \
  --node-count 1 --node-vm-size Standard_DS2_v2 \
  --enable-cluster-autoscaler --min-count 1 --max-count 3 \
  --nodepool-name systempool --zones 1 2 3 \
  --enable-managed-identity \
  --network-plugin azure --network-policy azure \
  --vnet-subnet-id $SUBNET_ID \
  --enable-aad --aad-admin-group-object-ids $ADMIN_GROUP_ID \
  --enable-addons monitoring,virtual-node \
  --workspace-resource-id $WORKSPACE_ID \
  --ssh-key-value ~/.ssh/id_rsa.pub

az aks get-credentials --resource-group $RG --name $CLUSTER
```

### Key Design Decisions

| Decision | Options |
|----------|---------|
| Authentication | System-assigned managed identity (recommended) vs service principal |
| Networking | Azure CNI (production, required for virtual nodes) vs kubenet |
| Network policy | Azure or Calico |
| Load balancer | Standard (production) vs Basic |
| Cluster access | Public (with authorized IPs) vs Private (jump box required) |

### kubenet vs Azure CNI

| Aspect | kubenet | Azure CNI |
|--------|---------|-----------|
| Pod IPs | NAT behind node IP | Direct VNet IP per pod |
| Performance | NAT overhead | Better (no NAT) |
| IP consumption | Low | High (needs large subnet) |
| Network policies | Limited | Full support |
| Required for | Small clusters | Virtual nodes, Windows pools |

## Node Pools

```bash
# Linux user pool
az aks nodepool add \
  --resource-group $RG --cluster-name $CLUSTER \
  --name linux101 --mode User --os-type Linux \
  --node-count 1 --enable-cluster-autoscaler --min-count 1 --max-count 3 \
  --node-vm-size Standard_DS2_v2 --zones 1 2 3 \
  --labels nodepool-type=user nodepoolos=linux

# Windows pool (name limited to 6 chars, requires Azure CNI)
az aks nodepool add \
  --name win101 --mode User --os-type Windows --node-count 1
```

## Azure Container Registry (ACR)

```bash
az acr create -g $RG -n $ACR_NAME --sku Basic
az acr login --name $ACR_NAME
docker tag myapp:latest $ACR_NAME.azurecr.io/myapp:v1
docker push $ACR_NAME.azurecr.io/myapp:v1

# Attach to AKS (auto-auth, simplest)
az aks update -n $CLUSTER -g $RG --attach-acr $ACR_NAME
```

For multi-registry setups, use service principal + K8s image pull secrets:
```yaml
spec:
  imagePullSecrets:
  - name: acr-secret
  containers:
  - image: myacr.azurecr.io/myapp:v1
```

## Azure AD Integration

### RBAC Flow

1. Create Azure AD groups (AKS-Admins, AKS-Dev)
2. Create AD users, assign to groups
3. Create K8s Role/RoleBinding mapping AD groups to namespace permissions
4. Users authenticate via `kubectl` -> Azure device login -> tokens in kubeconfig

### Admin Bypass

```bash
az aks get-credentials --resource-group $RG --name $CLUSTER --admin
```

## Azure Monitor (Container Insights)

Enable: `--enable-addons monitoring --workspace-resource-id $WORKSPACE_ID`

KQL log queries:
```kql
ContainerLog
| where LogEntry contains "error"
| project TimeGenerated, LogEntry, ContainerID
| order by TimeGenerated desc
| take 50
```

## Virtual Nodes (ACI)

Serverless burst scaling. Pods up in <60s vs minutes for regular nodes.

```yaml
nodeSelector:
  type: virtual-kubelet
```

**Limitations**: no Azure Disks, no init containers, no DaemonSets, requires Azure CNI. Best for stateless burst workloads.

## Cluster Management

```bash
az aks show -g $RG -n $CLUSTER -o table
az aks get-upgrades -g $RG -n $CLUSTER -o table
az aks upgrade -g $RG -n $CLUSTER --kubernetes-version 1.28.0
az aks stop -g $RG -n $CLUSTER        # cost saving
az aks start -g $RG -n $CLUSTER
az aks delete -g $RG -n $CLUSTER --yes --no-wait
```

## Gotchas

- Always delete unused clusters/resources to avoid billing
- Windows node pool names limited to 6 characters
- Default StorageClass may not work on user node pools - create custom StorageClass
- Azure Disk RWO only - pod and PVC must be in same availability zone
- Virtual nodes require Azure CNI networking

## See Also

- [[kubernetes-architecture]] - generic K8s concepts
- [[kubernetes-resource-management]] - namespaces, quotas, autoscaling
- [[terraform-iac]] - provisioning AKS with Terraform
- [[cicd-pipelines]] - Azure DevOps pipelines for AKS
- [[container-registries]] - ACR details
