---
title: Kustomize
category: tools
tags: [kubernetes, configuration, overlay, yaml, kubectl]
---

# Kustomize

Template-free customization of Kubernetes YAML configurations. Built into kubectl. Uses overlays to patch base manifests without modifying originals.

## Key Facts

- Built into kubectl since v1.14: `kubectl apply -k <dir>`
- No templates - works with plain YAML (unlike Helm)
- Base + overlay model: base defines resources, overlays customize per environment
- `kustomization.yaml` is the entry point in each directory
- Standalone binary also available: `kustomize build <dir>`
- Supports: patches, name prefixes, namespace overrides, labels, configmap/secret generation
- `kubectl kustomize <dir>` previews output without applying

## Directory Structure

```text
app/
  base/
    kustomization.yaml
    deployment.yaml
    service.yaml
  overlays/
    dev/
      kustomization.yaml
      patch-replicas.yaml
    staging/
      kustomization.yaml
    production/
      kustomization.yaml
      patch-resources.yaml
```

## Base kustomization.yaml

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

commonLabels:
  app: myapp

images:
  - name: myapp
    newTag: latest
```

## Overlay Example

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namespace: production

namePrefix: prod-

commonLabels:
  environment: production

replicas:
  - name: myapp
    count: 5

images:
  - name: myapp
    newTag: v2.1.0

patches:
  - path: patch-resources.yaml
```

## Patching Strategies

### Strategic Merge Patch

```yaml
# patch-resources.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          limits:
            memory: "512Mi"
            cpu: "1000m"
          requests:
            memory: "256Mi"
            cpu: "500m"
```

### JSON Patch

```yaml
# In kustomization.yaml
patches:
  - target:
      kind: Deployment
      name: myapp
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 3
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: ENV
          value: production
```

### Inline Patch

```yaml
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: myapp
      spec:
        replicas: 3
```

## ConfigMap and Secret Generation

```yaml
# kustomization.yaml
configMapGenerator:
  - name: app-config
    literals:
      - DATABASE_HOST=db.production.svc
      - LOG_LEVEL=info
    files:
      - configs/app.properties

secretGenerator:
  - name: app-secrets
    literals:
      - DB_PASSWORD=s3cret
    type: Opaque

# Kustomize appends content hash to name: app-config-abc123
# Deployments referencing it auto-update on change
```

## Key Operations

```bash
# Preview generated manifests
kubectl kustomize overlays/production/

# Apply directly
kubectl apply -k overlays/production/

# Delete resources
kubectl delete -k overlays/production/

# Build with standalone kustomize (more features)
kustomize build overlays/production/ | kubectl apply -f -

# Diff before apply
kubectl diff -k overlays/production/
```

## Kustomize vs Helm

| Aspect | Kustomize | Helm |
|--------|-----------|------|
| Templating | None (patches) | Go templates |
| Learning curve | Low | Medium |
| Complexity | Simple overlays | Full package manager |
| Rollback | kubectl rollout | helm rollback |
| Ecosystem | Built into kubectl | Huge chart repository |
| Secrets | Basic generation | Helm secrets plugin |
| Best for | Internal apps, GitOps | Third-party apps, complex deploys |

## GitOps with Kustomize

```yaml
# ArgoCD Application pointing to kustomize overlay
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-production
spec:
  source:
    repoURL: https://github.com/org/k8s-config
    path: app/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
```

## Gotchas

- **Issue:** ConfigMap/Secret name suffix (hash) causes deployment not finding the resource -> **Fix:** Kustomize auto-updates references in Deployments that use `configMapRef` or `secretRef`. If using plain `env.valueFrom`, it may not auto-update - use `configMapGenerator` with `behavior: merge`.
- **Issue:** `namePrefix` breaks cross-namespace references -> **Fix:** Use `namePrefix` carefully. For resources referenced by other namespaces, consider keeping original names or using `configurations` to tell Kustomize which fields contain names.
- **Issue:** Kustomize version in kubectl lags behind standalone -> **Fix:** For latest features (components, replacements), install standalone `kustomize` binary. kubectl's built-in version is often 1-2 releases behind.

## See Also

- [[helm-package-manager]] - template-based alternative
- [[gitops-and-argocd]] - GitOps workflows with Kustomize
- [[kubernetes-workloads]] - resources Kustomize manages
