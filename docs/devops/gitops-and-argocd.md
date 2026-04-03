---
title: GitOps and ArgoCD
category: concepts
tags: [devops, gitops, argocd, fluxcd, continuous-delivery, kubernetes]
---

# GitOps and ArgoCD

GitOps uses Git as the single source of truth for infrastructure and application state. An operator inside the cluster watches Git repos and automatically reconciles cluster state to match - providing self-healing, audit trails, and declarative deployments.

## GitOps Core Principles

1. **Declarative descriptions** - system state in files (K8s manifests, Terraform configs)
2. **Git as source of truth** - all changes versioned in Git
3. **Automated delivery** - CI/CD pipelines
4. **Automatic reconciliation** - operators detect and fix drift

### Pull Model

Operator (ArgoCD/Flux) inside cluster independently checks Git and updates cluster. No external CI system pushes to cluster.

Flow: Developer -> Git -> CI builds image -> Update manifest in Git -> ArgoCD detects change -> Deploys to cluster

### Self-Healing

If cluster deviates from desired state (e.g., pod deleted manually), ArgoCD automatically restores it.

## ArgoCD

### Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### CLI

```bash
argocd login <SERVER> --username admin
argocd repo add <url>                              # public repo
argocd repo add <url> --username <u> --password <p> # private
argocd repo add <url> --ssh-private-key-path ~/.ssh/id_rsa

argocd app sync <app-name>     # manual sync
argocd app get <app-name>      # status
argocd app list                # all apps
```

### Sync Modes

- **Automatic** - Git changes applied immediately
- **Manual** - user confirms via UI or CLI

### Features

- State synchronization with drift detection
- Multi-cluster management (dev, staging, prod)
- Web UI with diff views, pod logs, topology
- RBAC for access control
- ApplicationSet for auto-creating apps from templates
- Works with Jenkins, GitLab CI, GitHub Actions

## App of Apps Pattern

One parent Application manages multiple child applications:

- Parent references a Git repo containing child application manifests
- Single point of control for entire cluster state
- Adding new components = adding new manifest
- Disaster recovery: entire cluster recoverable from Git

## Sync Waves

Order resource deployment via annotations:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

Deployment order: Wave -1 -> Wave 0 -> Wave 1 -> Wave 2 (2s pause between). Deletion happens in reverse order.

**Typical ordering:**
1. Namespaces, CRDs (wave -1)
2. Databases, infrastructure (wave 0)
3. Backend services (wave 1)
4. Frontend services (wave 2)

## Sealed Secrets

Encrypted secrets safe for Git storage:

```bash
# kubeseal encrypts with cluster's public key
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml
# Only the cluster with matching private key can decrypt
```

SealedSecret controller in cluster decrypts at runtime.

## Crossplane (K8s-Native IaC)

Alternative to Terraform that runs inside the cluster:

- Extends K8s API with CRDs representing cloud infrastructure
- Uses K8s reconciliation loop for continuous drift detection
- Developer self-service via Claims
- Providers: provider-aws, provider-gcp, provider-kubernetes

**vs Terraform**: runs inside K8s, native RBAC, continuous reconciliation (not just plan/apply).

## Terraform in GitOps

1. Store Terraform configs in Git
2. On PR: auto-run `terraform plan`
3. After merge to main: auto-run `terraform apply`
4. Changes go through PR review

## Gotchas

- Secret management requires additional tools (Sealed Secrets, Vault, External Secrets Operator)
- Adding new environments requires Git repo edits
- ArgoCD itself needs to be managed (who deploys ArgoCD?)
- Sync waves only work within a single Application resource
- Image tag updates should modify Git manifests, not be pushed directly

## See Also

- [[helm-package-manager]] - Helm charts deployed via ArgoCD
- [[cicd-pipelines]] - CI builds images, GitOps deploys them
- [[terraform-iac]] - IaC in GitOps workflow
- [[deployment-strategies]] - blue-green, canary via GitOps
- [[sre-principles]] - Git as audit trail for changes
