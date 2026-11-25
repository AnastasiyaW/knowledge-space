---
title: "Helm-Paketmanager"
category: concepts
tags: [devops, kubernetes, helm, charts, templates, releases]
level: 3
source_sha256: c3ec6e9f3c5a758ddc45f59ed405898788b1c53cd5ca1115dfecf1c876e7033b
translation: machine
translated_at: '2026-10-24'
---
# Helm-Paketmanager {#helm-package-manager}

Helm ist ein Paketmanager für Kubernetes, der Manifeste templatisiert, Releases verwaltet und wiederverwendbare Infrastrukturkonfigurationen ermöglicht. Ein Helm-Chart = Templates + Values = deploybares Paket.

## Architektur {#architecture}

- **Chart** - Paket mit vorkonfigurierten K8s-Ressourcen (vergleichbar mit einem npm-Paket)
- **Release** - bereitgestellte Instanz eines Charts mit spezifischen Values
- **Values** - Konfigurationsparameter, die das Verhalten des Charts anpassen
- **Repository** - Sammlung von Charts zur gemeinsamen Nutzung

Helm v3 hat Tiller entfernt (Sicherheitsbedenken bei v2) – direkte Interaktion mit der K8s-API.

## Chart-Struktur {#chart-structure}

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

### Chart.yaml {#chartyaml}

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

### values.yaml {#valuesyaml}

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

## Template-Syntax {#template-syntax}

Helm verwendet die Go-Template-Sprache mit Sprig-Funktionen.

### Eingebaute Objekte {#built-in-objects}

| Objekt | Beschreibung |
|--------|-------------|
| `.Values` | Values aus values.yaml und Überschreibungen |
| `.Release.Name` | Release-Name |
| `.Release.Namespace` | Ziel-Namespace |
| `.Chart.Name` | Chart-Name |
| `.Chart.Version` | Chart-Version |
| `.Template.Name` | Aktueller Template-Pfad |

### Grundlegendes Templating {#basic-templating}

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

### Kontrollstrukturen {#control-structures}

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

### Helper-Templates (_helpers.tpl) {#helper-templates-_helperstpl}

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

Verwendung: `{{ include "myapp.labels" . | nindent 4 }}`

### Wichtige Funktionen {#key-functions}

| Funktion | Beispiel | Beschreibung |
|----------|---------|-------------|
| `default` | `{{ .Values.x \| default "fallback" }}` | Standardwert |
| `quote` | `{{ .Values.x \| quote }}` | In Anführungszeichen setzen |
| `required` | `{{ required "msg" .Values.x }}` | Fehler, wenn leer |
| `toYaml` | `{{ toYaml .Values.x \| nindent 4 }}` | In YAML konvertieren |
| `nindent` | `{{ ... \| nindent 4 }}` | Zeilenumbruch + Einrückung |
| `b64enc` | `{{ .Values.x \| b64enc }}` | Base64-kodieren |
| `tpl` | `{{ tpl .Values.x . }}` | String als Template rendern |
| `lookup` | `{{ lookup "v1" "Secret" "ns" "name" }}` | Cluster abfragen |

## CLI-Befehle {#cli-commands}

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

## Hooks {#hooks}

Aktionen an Lebenszyklus-Punkten ausführen:

```yaml
annotations:
  "helm.sh/hook": pre-upgrade,post-upgrade
  "helm.sh/hook-weight": "-1"          # lower = earlier
  "helm.sh/hook-delete-policy": hook-succeeded
```

Best Practice: Hooks mit Jobs verwenden, insbesondere für Datenbankmigrationen.

## Priorität der Überschreibung von Values (höchste bis niedrigste) {#values-override-priority-highest-to-lowest}

1. `--set`-Flag
2. `-f custom-values.yaml`
3. values.yaml des Eltern-Charts (für Subcharts)
4. values.yaml des Charts selbst

## Abhängigkeiten {#dependencies}

```bash
helm dependency update    # download to charts/
helm dependency build     # rebuild from lock file
```

## Secrets (sops-Integration) {#secrets-sops-integration}

```bash
helm secrets encrypt values-secret.yaml
helm secrets install my-release ./ -f values-secret.yaml
```

## Alternativen {#alternatives}

- **Kustomize** - in kubectl integriert, Overlay-basiert (kein Templating)
- **CDK8s** - K8s-Ressourcen in Programmiersprachen definieren
- **Jsonnet/Tanka** - Ansatz mit einer Datentemplating-Sprache

## Fallstricke {#gotchas}

- `helm template` rendert lokal ohne Cluster-Zugriff – nützlich zum Debuggen
- Hooks mit `hook-delete-policy: hook-succeeded` räumen nach Erfolg automatisch auf
- Library-Charts können nicht direkt installiert werden – sie werden nur als Abhängigkeiten verwendet
- `helm upgrade --install` kombiniert Installation und Upgrade (idempotent)

## Siehe auch {#see-also}

- [[kubernetes-workloads]] - K8s-Objekte, die Helm templatisiert
- [[gitops-and-argocd]] - GitOps-Deployment von Helm-Charts
- [[cicd-pipelines]] - Helm in CI/CD
- [[deployment-strategies]] - Blue-Green, Canary über Helm
