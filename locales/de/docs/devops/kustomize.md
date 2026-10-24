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

Vorlagenfreie Anpassung von Kubernetes-YAML-Konfigurationen. In kubectl integriert. Verwendet Overlays, um Basis-Manifeste zu patchen, ohne die Originale zu verändern.

## Wichtige Fakten {#key-facts}

- In kubectl integriert seit v1.14: `kubectl apply -k <dir>`
- Keine Templates - funktioniert mit einfachem YAML (im Gegensatz zu Helm)
- Basis-und-Overlay-Modell: Die Basis definiert Ressourcen, Overlays passen sie pro Umgebung an
- `kustomization.yaml` ist der Einstiegspunkt in jedem Verzeichnis
- Eigenständiges Binary ebenfalls verfügbar: `kustomize build <dir>`
- Unterstützt: Patches, Namenspräfixe, Namespace-Überschreibungen, Labels, ConfigMap-/Secret-Generierung
- `kubectl kustomize <dir>` zeigt die Ausgabe an, ohne sie anzuwenden

## Verzeichnisstruktur {#directory-structure}

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

## Basis-kustomization.yaml {#base-kustomizationyaml}

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

## Overlay-Beispiel {#overlay-example}

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

## Patch-Strategien {#patching-strategies}

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

### Inline-Patch {#inline-patch}

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

## ConfigMap- und Secret-Generierung {#configmap-and-secret-generation}

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

## Wichtige Operationen {#key-operations}

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

## Kustomize vs. Helm {#kustomize-vs-helm}

| Aspekt | Kustomize | Helm |
|--------|-----------|------|
| Templating | Keines (Patches) | Go-Templates |
| Lernkurve | Gering | Mittel |
| Komplexität | Einfache Overlays | Vollwertiger Paketmanager |
| Rollback | kubectl rollout | helm rollback |
| Ökosystem | In kubectl integriert | Riesiges Chart-Repository |
| Secrets | Einfache Generierung | Helm-Secrets-Plugin |
| Ideal für | Interne Apps, GitOps | Drittanbieter-Apps, komplexe Deployments |

## GitOps mit Kustomize {#gitops-with-kustomize}

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

## Stolperfallen {#gotchas}

- **Problem:** Das Namenssuffix (Hash) von ConfigMaps/Secrets führt dazu, dass das Deployment die Ressource nicht findet -> **Lösung:** Kustomize aktualisiert Referenzen in Deployments, die `configMapRef` oder `secretRef` verwenden, automatisch. Bei direkter Verwendung von `env.valueFrom` werden sie unter Umständen nicht automatisch aktualisiert - in diesem Fall `configMapGenerator` mit `behavior: merge` verwenden.
- **Problem:** `namePrefix` bricht namensraumübergreifende Referenzen -> **Lösung:** `namePrefix` mit Bedacht einsetzen. Für Ressourcen, die aus anderen Namespaces referenziert werden, bietet es sich an, die ursprünglichen Namen beizubehalten oder über `configurations` festzulegen, welche Felder Namen enthalten.
- **Problem:** Die Kustomize-Version in kubectl hinkt dem eigenständigen Binary hinterher -> **Lösung:** Für die neuesten Funktionen (Components, Replacements) das eigenständige `kustomize`-Binary installieren. Die in kubectl eingebaute Version liegt oft 1-2 Releases zurück.

## Siehe auch {#see-also}

- [[helm-package-manager]] - vorlagenbasierte Alternative
- [[gitops-and-argocd]] - GitOps-Workflows mit Kustomize
- [[kubernetes-workloads]] - Ressourcen, die Kustomize verwaltet
