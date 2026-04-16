---
title: Helm Package Manager
category: concepts
tags: [devops, kubernetes, helm, charts, templates, releases]
---

# Helm Package Manager

Helm is a package manager for Kubernetes that templates manifests, manages releases, and enables reusable infrastructure configurations. A Helm chart = templates + values = deployable package.

## Architecture

- **Chart** - package of pre-configured K8s resources (like npm package)
- **Release** - deployed instance of a chart with specific values
- **Values** - configuration parameters customizing chart behavior
- **Repository** - collection of charts for sharing

Helm v3 removed Tiller (v2 security concern) - direct K8s API interaction.

## Chart Structure

```hcl
my-chart/
  Chart.yaml          # metadata (name, version, appVersion)
  values.yaml         # default configuration values
  charts/             # dependencies (subcharts)
  templates/          # K8s manifest templates
    deployment.yaml
    service.yaml
    ingress.yaml
    _helpers.tpl       # reusable template snippets
    NOTES.txt          # post-install instructions
  .helmignore          # files to exclude
```

### Chart.yaml

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application      # or "library"
version: 0.1.0         # chart version
appVersion: "1.0.0"    # application version
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### values.yaml

```yaml
replicaCount: 3
image:
  repository: my-app
  tag: "1.0.0"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: false
  host: myapp.example.com
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

## Template Syntax

Helm uses Go template language with Sprig functions.

### Built-in Objects

| Object | Description |
|--------|-------------|
| `.Values` | Values from values.yaml and overrides |
| `.Release.Name` | Release name |
| `.Release.Namespace` | Target namespace |
| `.Chart.Name` | Chart name |
| `.Chart.Version` | Chart version |
| `.Template.Name` | Current template path |

### Basic Templating

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    app: {{ .Values.app.name | default .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: {{ .Values.service.port }}
```

### Control Structures

```yaml
# Conditionals
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
{{- end }}

# Loops
{{- range .Values.env }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}

# Scope change
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

### Helper Templates (_helpers.tpl)

```yaml
{{- define "myapp.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}

{{- define "myapp.labels" -}}
app: {{ include "myapp.fullname" . }}
chart: {{ .Chart.Name }}-{{ .Chart.Version }}
release: {{ .Release.Name }}
{{- end -}}
```

Usage: `{{ include "myapp.labels" . | nindent 4 }}`

### Key Functions

| Function | Example | Description |
|----------|---------|-------------|
| `default` | `{{ .Values.x \| default "fallback" }}` | Default value |
| `quote` | `{{ .Values.x \| quote }}` | Wrap in quotes |
| `required` | `{{ required "msg" .Values.x }}` | Fail if empty |
| `toYaml` | `{{ toYaml .Values.x \| nindent 4 }}` | Convert to YAML |
| `nindent` | `{{ ... \| nindent 4 }}` | Newline + indent |
| `b64enc` | `{{ .Values.x \| b64enc }}` | Base64 encode |
| `tpl` | `{{ tpl .Values.x . }}` | Render string as template |
| `lookup` | `{{ lookup "v1" "Secret" "ns" "name" }}` | Query cluster |

## CLI Commands

```bash
# Chart development
helm create my-chart              # scaffold new chart
helm template my-chart ./         # render templates locally (dry run)
helm lint ./                      # validate chart

# Install and manage
helm install my-release ./my-chart
helm install my-release ./my-chart -f custom-values.yaml
helm install my-release ./my-chart --set replicaCount=5
helm upgrade my-release ./my-chart
helm rollback my-release 1        # rollback to revision 1
helm uninstall my-release

# Release info
helm list
helm history my-release
helm status my-release

# Repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx
helm pull bitnami/nginx           # download chart locally

# Package and publish
helm package ./my-chart           # create .tgz
helm repo index . --url https://<user>.github.io/<repo>
```

## Hooks

Run actions at lifecycle points:

```yaml
annotations:
  "helm.sh/hook": pre-upgrade,post-upgrade
  "helm.sh/hook-weight": "-1"          # lower = earlier
  "helm.sh/hook-delete-policy": hook-succeeded
```

Best practice: use hooks with Jobs, especially for database migrations.

## Values Override Priority (highest to lowest)

1. `--set` flag
2. `-f custom-values.yaml`
3. Parent chart's values.yaml (for subcharts)
4. Chart's own values.yaml

## Dependencies

```bash
helm dependency update    # download to charts/
helm dependency build     # rebuild from lock file
```

## Secrets (sops integration)

```bash
helm secrets encrypt values-secret.yaml
helm secrets install my-release ./ -f values-secret.yaml
```

## Alternatives

- **Kustomize** - built into kubectl, overlay-based (no templating)
- **CDK8s** - define K8s resources in programming languages
- **Jsonnet/Tanka** - data-templating language approach

## Gotchas

- `helm template` renders locally without cluster access - useful for debugging
- Hooks with `hook-delete-policy: hook-succeeded` auto-clean after success
- Library charts cannot be installed directly - only used as dependencies
- `helm upgrade --install` combines install and upgrade (idempotent)

## See Also

- [[kubernetes-workloads]] - K8s objects that Helm templates
- [[gitops-and-argocd]] - GitOps deployment of Helm charts
- [[cicd-pipelines]] - Helm in CI/CD
- [[deployment-strategies]] - blue-green, canary via Helm
