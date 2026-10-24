---
title: "Kustomize"
category: tools
tags: [kubernetes, configuration, overlay, yaml, kubectl]
level: 3
source_sha256: 2162030cdd0433fc38c2400bd76295ceae9f7bf1204a81658f688b4bbc7630f7
translation: machine
translated_at: '2026-10-24'
---
# Kustomize {#kustomize}

Personnalisation sans templates des configurations YAML de Kubernetes. Intégré à kubectl. Utilise des overlays pour appliquer des patchs aux manifestes de base sans modifier les originaux.

## Points clés {#key-facts}

- Intégré à kubectl depuis la v1.14 : `kubectl apply -k <dir>`
- Pas de templates : fonctionne avec du YAML brut (contrairement à Helm)
- Modèle base + overlay : la base définit les ressources, les overlays les personnalisent par environnement
- `kustomization.yaml` est le point d'entrée de chaque répertoire
- Binaire autonome également disponible : `kustomize build <dir>`
- Prend en charge : patchs, préfixes de noms, surcharges de namespace, labels, génération de configmap/secret
- `kubectl kustomize <dir>` prévisualise la sortie sans l'appliquer

## Structure des répertoires {#directory-structure}

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

## kustomization.yaml de base {#base-kustomizationyaml}

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

## Exemple d'overlay {#overlay-example}

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

## Stratégies de patch {#patching-strategies}

### Strategic Merge Patch {#strategic-merge-patch}

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

### JSON Patch {#json-patch}

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

### Patch en ligne {#inline-patch}

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

## Génération de ConfigMap et de Secret {#configmap-and-secret-generation}

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

## Opérations clés {#key-operations}

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

## Kustomize vs Helm {#kustomize-vs-helm}

| Aspect | Kustomize | Helm |
|--------|-----------|------|
| Templating | Aucun (patchs) | Templates Go |
| Courbe d'apprentissage | Faible | Moyenne |
| Complexité | Overlays simples | Gestionnaire de paquets complet |
| Rollback | kubectl rollout | helm rollback |
| Écosystème | Intégré à kubectl | Vaste dépôt de charts |
| Secrets | Génération basique | Plugin helm secrets |
| Idéal pour | Applications internes, GitOps | Applications tierces, déploiements complexes |

## GitOps avec Kustomize {#gitops-with-kustomize}

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

## Pièges courants {#gotchas}

- **Problème :** le suffixe (hash) du nom de ConfigMap/Secret empêche le déploiement de trouver la ressource -> **Solution :** Kustomize met à jour automatiquement les références dans les Deployments qui utilisent `configMapRef` ou `secretRef`. Si vous utilisez `env.valueFrom` directement, la mise à jour automatique peut ne pas s'appliquer : utilisez `configMapGenerator` avec `behavior: merge`.
- **Problème :** `namePrefix` casse les références inter-namespaces -> **Solution :** utilisez `namePrefix` avec précaution. Pour les ressources référencées depuis d'autres namespaces, conservez les noms d'origine ou utilisez `configurations` pour indiquer à Kustomize quels champs contiennent des noms.
- **Problème :** la version de Kustomize intégrée à kubectl est en retard sur le binaire autonome -> **Solution :** pour bénéficier des dernières fonctionnalités (components, replacements), installez le binaire `kustomize` autonome. La version intégrée à kubectl accuse souvent 1 à 2 versions de retard.

## Voir aussi {#see-also}

- [[helm-package-manager]] - alternative basée sur les templates
- [[gitops-and-argocd]] - workflows GitOps avec Kustomize
- [[kubernetes-workloads]] - ressources gérées par Kustomize
