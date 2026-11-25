---
title: "CI/CD-Pipelines"
category: concepts
tags: [devops, cicd, jenkins, github-actions, azure-devops, continuous-integration, continuous-delivery]
level: 3
source_sha256: b00882f5959de8a85a282d53a6eca9040c7d952ed932d8a5d12d8107f75b83e5
translation: machine
translated_at: '2026-10-24'
---
# CI/CD-Pipelines {#cicd-pipelines}

CI/CD automatisiert das Bauen, Testen und Ausliefern von Software. CI (Continuous Integration) integriert Code häufig mit automatisierten Builds und Tests. CD (Continuous Delivery) macht jeden Build deploybar. Continuous Deployment deployt erfolgreiche Builds automatisch.

## Pipeline-Stufen {#pipeline-stages}

```go
Code Push -> Build -> Test -> Package -> Deploy to Dev -> Deploy to QA -> Deploy to Prod
```

## Tool-Landschaft {#tools-landscape}

| Tool | Hauptvorteil |
|------|---------------|
| Jenkins | Flexibilität, Plugin-Ökosystem, selbst gehostet |
| GitLab CI | Integriert, keine externen Tools nötig |
| GitHub Actions | Native GitHub-Integration |
| Azure DevOps | Integration in das Azure-Ökosystem |
| CircleCI | Einfache Konfiguration |

## GitHub Actions {#github-actions}

```yaml
name: CI/CD Pipeline
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm test
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: docker build -t my-app .
      - run: docker push my-app
```

## Azure DevOps Pipelines {#azure-devops-pipelines}

### Multi-Stage-YAML-Pipeline {#multi-stage-yaml-pipeline}

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

variables:
  tag: '$(Build.BuildId)'

stages:
- stage: Build
  jobs:
  - job: Build
    steps:
    - task: Docker@2
      inputs:
        containerRegistry: 'acr-connection'
        repository: 'myapp'
        command: 'buildAndPush'
        Dockerfile: '**/Dockerfile'
        tags: |
          $(tag)
          $(Build.SourceVersion)
    - task: CopyFiles@2
      inputs:
        SourceFolder: 'kube-manifests'
        Contents: '**'
        TargetFolder: '$(Build.ArtifactStagingDirectory)'
    - task: PublishBuildArtifacts@1

- stage: DeployDev
  dependsOn: Build
  jobs:
  - deployment: DeployDev
    environment: 'dev'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            inputs:
              action: 'createSecret'
              namespace: 'dev'
              secretType: 'dockerRegistry'
              secretName: 'acr-secret'
          - task: KubernetesManifest@0
            inputs:
              action: 'deploy'
              namespace: 'dev'
              manifests: '$(Pipeline.Workspace)/**/*.yaml'
              imagePullSecrets: 'acr-secret'

- stage: DeployQA
  dependsOn: DeployDev
  condition: succeeded()
  jobs:
  - deployment: DeployQA
    environment: 'qa'     # can have approval gates
```

### Wichtige Variablen {#key-variables}

| Variable | Beschreibung |
|----------|-------------|
| `$(Build.BuildId)` | Fortlaufende Build-Nummer |
| `$(Build.SourceVersion)` | Git-Commit-SHA |
| `$(Build.SourceBranchName)` | Branch-Name |
| `$(Pipeline.Workspace)` | Wurzelverzeichnis des Pipeline-Workspace |

### Service Connections {#service-connections}

Drei sind erforderlich: GitHub (Quelle), Container Registry (Push/Pull) und Kubernetes (Deployment).

### Umgebungen und Freigaben {#environments-and-approvals}

Umgebungen in DevOps anlegen: Pipelines -> Environments. Für Produktions-Deployments Freigabeprüfungen (Approval Checks) hinzufügen.

## Terraform in CI/CD {#terraform-in-cicd}

```yaml
stages:
- stage: Validate
  steps:
  - terraform init
  - terraform validate
  - terraform fmt --check

- stage: Plan
  steps:
  - terraform plan -var-file="dev.tfvars" -out=dev.plan

- stage: Apply
  steps:    # approval gate before this stage
  - terraform apply dev.plan
```

## Docker-Image-Tagging-Strategien {#docker-image-tagging-strategies}

- `$(Build.BuildId)` - fortlaufend, einfach
- `$(Build.SourceVersion)` - Git-Commit-SHA, ermöglicht Nachvollziehbarkeit
- Semantische Versionierung - `v1.2.3`
- Branch-basiert - `main-abc1234`

## Pipeline-Organisation {#pipeline-organization}

- Pipelines für mehr Übersicht umbenennen: `01-docker-build-push-to-acr`
- In Ordnern gruppieren: `app1-pipelines/`
- Nicht genutzte Pipelines deaktivieren
- Nach der Erstellung einer Pipeline immer `git pull` ausführen (YAML wird automatisch ins Repository committet)

## Fallstricke {#gotchas}

- `depends_on` in Azure-DevOps-Stages stellt die Ausführungsreihenfolge sicher
- Freigabeprüfungen für Umgebungen blockieren die Pipeline, bis sie genehmigt sind
- Klassische (GUI-)Pipelines und YAML-Pipelines bestehen nebeneinander, YAML ist für die Versionskontrolle jedoch vorzuziehen
- Build- und Release-Pipelines getrennt halten oder in einer Multi-Stage-YAML-Pipeline kombinieren
- `condition: succeeded()` ist der Standard – explizite Angabe nur zur Verdeutlichung

## Siehe auch {#see-also}

- [[jenkins-automation]] - Jenkins-spezifische Muster
- [[gitops-and-argocd]] - GitOps-basiertes Deployment
- [[terraform-iac]] - Terraform in Pipelines
- [[container-registries]] - Ziele für Image-Push/Pull
- [[deployment-strategies]] - Blue-Green, Canary
