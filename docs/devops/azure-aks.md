---
title: Azure Kubernetes Service (AKS)
category: cloud
tags: [azure, aks, kubernetes, acr, azure-devops, terraform]
---
# Azure Kubernetes Service (AKS)

Managed Kubernetes on Azure: cluster provisioning, ACR integration, Azure DevOps pipelines.

## Key Facts

- **AKS** = Azure-managed Kubernetes; free control plane, pay only for worker nodes
- **ACR** (Azure Container Registry) = private Docker registry; integrates with AKS via managed identity
- **Node pools** = groups of VMs with same config; system pool (required) + user pools (workloads)
- **Azure CNI** networking: pods get VPC IPs directly; vs kubenet (overlay network, fewer IPs needed)
- **Managed Identity** = passwordless auth for Azure resources; preferred over service principals
- **Azure DevOps** = CI/CD platform; YAML pipelines, Boards, Repos, Artifacts
- AKS supports **cluster autoscaler** (add/remove nodes) and **KEDA** (event-driven pod autoscaling)
- **Azure Monitor** / **Container Insights** = built-in monitoring for AKS clusters
- **Virtual nodes** = serverless containers via Azure Container Instances (ACI) for burst workloads
- [[terraform-iac]] provisions AKS clusters and Azure resources
- [[kubernetes-pods]] and [[kubernetes-services]] work identically on AKS
- [[helm-charts]] deployed to AKS clusters via Azure DevOps or ArgoCD

## Patterns

```bash
# AKS cluster creation (CLI)
az aks create \
  --resource-group myRG \
  --name myAKS \
  --node-count 3 \
  --node-vm-size Standard_DS2_v2 \
  --enable-managed-identity \
  --attach-acr myACR \
  --network-plugin azure \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group myRG --name myAKS
kubectl get nodes

# ACR
az acr create --resource-group myRG --name myACR --sku Basic
az acr login --name myACR
docker push myACR.azurecr.io/myapp:v1

# Attach ACR to AKS (allow image pulls)
az aks update --resource-group myRG --name myAKS --attach-acr myACR

# Scale node pool
az aks scale --resource-group myRG --name myAKS --node-count 5
az aks nodepool add --resource-group myRG --cluster-name myAKS \
  --name gpupool --node-count 1 --node-vm-size Standard_NC6s_v3
```

```hcl
# Terraform - AKS cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "myAKS"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "myaks"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS2_v2"
    auto_scaling_enabled = true
    min_count  = 2
    max_count  = 5
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    load_balancer_sku = "standard"
  }
}

resource "azurerm_container_registry" "acr" {
  name                = "myACR"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
}
```

```yaml
# Azure DevOps Pipeline (azure-pipelines.yml)
trigger:
  branches:
    include: [main]

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Docker@2
  inputs:
    containerRegistry: 'myACR'
    repository: 'myapp'
    command: 'buildAndPush'
    tags: '$(Build.BuildId)'

- task: HelmDeploy@0
  inputs:
    connectionType: 'Azure Resource Manager'
    azureSubscription: 'my-subscription'
    azureResourceGroup: 'myRG'
    kubernetesCluster: 'myAKS'
    command: 'upgrade'
    chartType: 'FilePath'
    chartPath: './charts/myapp'
    releaseName: 'myapp'
    overrideValues: 'image.tag=$(Build.BuildId)'
```

## Gotchas

- AKS control plane is free but node VMs, load balancers, and disks cost money
- `az aks get-credentials` overwrites existing kubeconfig context; use `--overwrite-existing` or merge manually
- Azure CNI requires large subnet (each pod gets an IP); plan CIDR ranges carefully
- ACR attached via managed identity is the easiest path; service principal approach is being deprecated
- Node pool VM size cannot be changed after creation; must create new pool and migrate
- AKS upgrades can cause brief downtime; use `PodDisruptionBudget` and `maxUnavailable` settings
- Azure DevOps service connections need proper RBAC on the AKS cluster for deployment tasks

## See Also

- [[kubernetes-pods]] - workload specs are cloud-agnostic
- [[kubernetes-services]] - LoadBalancer type provisions Azure LB
- [[terraform-iac]] - AKS infrastructure provisioning
- [[helm-charts]] - deploying to AKS via Helm
- AKS docs: https://learn.microsoft.com/en-us/azure/aks/
- AKS best practices: https://learn.microsoft.com/en-us/azure/aks/best-practices
