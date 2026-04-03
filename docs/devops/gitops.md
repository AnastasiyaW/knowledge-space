---
title: GitOps
category: automation
tags: [gitops, argocd, fluxcd, kubernetes, declarative, git, reconciliation]
---
# GitOps

Git as single source of truth for declarative infrastructure and application deployment.

## Key Facts

- **GitOps** = operational model where Git repo is the desired state; controllers reconcile cluster to match
- **Pull-based** deployment: controller in cluster watches Git repo and syncs changes (vs push-based CI/CD)
- **ArgoCD** = most popular GitOps controller for Kubernetes; web UI, multi-cluster support, SSO
- **Flux CD** = CNCF GitOps toolkit; lighter weight, composable controllers, better for platform teams
- Core principles: declarative config, versioned in Git, automatically applied, continuously reconciled
- **Drift detection** = controller detects when cluster state differs from Git and auto-corrects
- **App of Apps** pattern: one ArgoCD Application manages other Applications (bootstrap entire cluster)
- ArgoCD supports Helm charts, Kustomize, plain YAML, and Jsonnet as manifest sources
- **Sync waves** = order resource creation (e.g., namespace -> secrets -> deployment)
- [[kubernetes-pods]] are the ultimate target of GitOps reconciliation
- [[helm-charts]] are commonly deployed via ArgoCD or Flux
- [[ci-cd-pipelines]] build images and update Git repo; GitOps controller handles the deploy

## Patterns

```yaml
# ArgoCD Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/manifests.git
    targetRevision: main
    path: apps/myapp/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true          # delete resources removed from Git
      selfHeal: true       # revert manual changes in cluster
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

---
# App of Apps (bootstrap)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cluster-bootstrap
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/org/cluster-config.git
    path: apps
  destination:
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      selfHeal: true
```

```bash
# ArgoCD installation
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# ArgoCD CLI
argocd login argocd.example.com
argocd app list
argocd app get myapp
argocd app sync myapp                  # manual sync
argocd app diff myapp                  # show diff between Git and cluster
argocd app history myapp               # deployment history
argocd app rollback myapp 3            # rollback to revision 3

# GitOps workflow (CI updates Git, ArgoCD deploys)
# In CI pipeline after image build:
git clone https://github.com/org/manifests.git
cd manifests/apps/myapp
kustomize edit set image myapp=registry/myapp:${NEW_TAG}
git add . && git commit -m "deploy myapp:${NEW_TAG}" && git push
# ArgoCD automatically detects change and syncs
```

```
# Recommended Git repository structure
manifests/
  apps/
    myapp/
      base/
        deployment.yaml
        service.yaml
        kustomization.yaml
      overlays/
        staging/
          kustomization.yaml
          patch-replicas.yaml
        production/
          kustomization.yaml
          patch-replicas.yaml
          patch-resources.yaml
  infrastructure/
    cert-manager/
    ingress-nginx/
    monitoring/
```

## Gotchas

- GitOps requires ALL state in Git; manual `kubectl apply` changes will be reverted by self-heal
- Secrets in Git are problematic; use Sealed Secrets, SOPS, or External Secrets Operator
- ArgoCD `prune: true` deletes resources removed from Git - can accidentally delete critical resources
- Image tag updates in Git can create noisy commit history; consider image updater automation
- Multi-cluster GitOps needs careful RBAC; ArgoCD supports cluster-level access control
- Sync loops can occur if cluster webhooks modify resources on apply (e.g., mutating admission controllers)
- ArgoCD web UI exposes cluster state; secure it with SSO and RBAC
- Git repository is a single point of failure; ensure repo availability and backup

## See Also

- [[kubernetes-pods]] - resources managed by GitOps
- [[helm-charts]] - chart deployment via ArgoCD/Flux
- [[ci-cd-pipelines]] - image building before GitOps sync
- [[deployment-strategies]] - progressive delivery with Argo Rollouts
- ArgoCD docs: https://argo-cd.readthedocs.io/
- Flux docs: https://fluxcd.io/docs/
