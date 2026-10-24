---
title: "Gestionnaire de paquets Helm"
category: concepts
tags: [devops, kubernetes, helm, charts, templates, releases]
level: 3
source_sha256: c3ec6e9f3c5a758ddc45f59ed405898788b1c53cd5ca1115dfecf1c876e7033b
translation: machine
translated_at: '2026-10-24'
---
# Gestionnaire de paquets Helm {#helm-package-manager}

Helm est un gestionnaire de paquets pour Kubernetes qui templatise les manifestes, gère les releases et permet de réutiliser des configurations d'infrastructure. Un chart Helm = templates + values = paquet déployable.

## Architecture {#architecture}

- **Chart** - paquet de ressources K8s préconfigurées (comme un paquet npm)
- **Release** - instance déployée d'un chart avec des values spécifiques
- **Values** - paramètres de configuration qui personnalisent le comportement du chart
- **Repository** - collection de charts destinée au partage

Helm v3 a supprimé Tiller (problème de sécurité de la v2) - interaction directe avec l'API K8s.

## Structure d'un chart {#chart-structure}

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

## Syntaxe des templates {#template-syntax}

Helm utilise le langage de templates Go avec les fonctions Sprig.

### Objets intégrés {#built-in-objects}

| Objet | Description |
|--------|-------------|
| `.Values` | Valeurs issues de values.yaml et des surcharges |
| `.Release.Name` | Nom de la release |
| `.Release.Namespace` | Namespace cible |
| `.Chart.Name` | Nom du chart |
| `.Chart.Version` | Version du chart |
| `.Template.Name` | Chemin du template courant |

### Templating de base {#basic-templating}

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

### Structures de contrôle {#control-structures}

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

### Templates d'aide (_helpers.tpl) {#helper-templates-_helperstpl}

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

Utilisation : `{{ include "myapp.labels" . | nindent 4 }}`

### Fonctions clés {#key-functions}

| Fonction | Exemple | Description |
|----------|---------|-------------|
| `default` | `{{ .Values.x \| default "fallback" }}` | Valeur par défaut |
| `quote` | `{{ .Values.x \| quote }}` | Entourer de guillemets |
| `required` | `{{ required "msg" .Values.x }}` | Échoue si vide |
| `toYaml` | `{{ toYaml .Values.x \| nindent 4 }}` | Conversion en YAML |
| `nindent` | `{{ ... \| nindent 4 }}` | Saut de ligne + indentation |
| `b64enc` | `{{ .Values.x \| b64enc }}` | Encodage Base64 |
| `tpl` | `{{ tpl .Values.x . }}` | Rend une chaîne comme template |
| `lookup` | `{{ lookup "v1" "Secret" "ns" "name" }}` | Interroge le cluster |

## Commandes CLI {#cli-commands}

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

Exécuter des actions à des points du cycle de vie :

```yaml
annotations:
  "helm.sh/hook": pre-upgrade,post-upgrade
  "helm.sh/hook-weight": "-1"          # lower = earlier
  "helm.sh/hook-delete-policy": hook-succeeded
```

Bonne pratique : utiliser les hooks avec des Jobs, en particulier pour les migrations de base de données.

## Priorité de surcharge des values (de la plus haute à la plus basse) {#values-override-priority-highest-to-lowest}

1. Option `--set`
2. `-f custom-values.yaml`
3. values.yaml du chart parent (pour les subcharts)
4. values.yaml du chart lui-même

## Dépendances {#dependencies}

```bash
helm dependency update    # download to charts/
helm dependency build     # rebuild from lock file
```

## Secrets (intégration sops) {#secrets-sops-integration}

```bash
helm secrets encrypt values-secret.yaml
helm secrets install my-release ./ -f values-secret.yaml
```

## Alternatives {#alternatives}

- **Kustomize** - intégré à kubectl, basé sur des overlays (sans templating)
- **CDK8s** - définir des ressources K8s dans des langages de programmation
- **Jsonnet/Tanka** - approche par langage de templating de données

## Pièges courants {#gotchas}

- `helm template` effectue le rendu en local sans accès au cluster - utile pour le débogage
- Les hooks avec `hook-delete-policy: hook-succeeded` se nettoient automatiquement après succès
- Les library charts ne peuvent pas être installés directement - ils servent uniquement de dépendances
- `helm upgrade --install` combine install et upgrade (idempotent)

## Voir aussi {#see-also}

- [[kubernetes-workloads]] - objets K8s que Helm templatise
- [[gitops-and-argocd]] - déploiement GitOps de charts Helm
- [[cicd-pipelines]] - Helm dans la CI/CD
- [[deployment-strategies]] - blue-green, canary avec Helm
