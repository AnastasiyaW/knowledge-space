---
title: "Pipelines CI/CD"
category: concepts
tags: [devops, cicd, jenkins, github-actions, azure-devops, continuous-integration, continuous-delivery]
level: 3
source_sha256: b00882f5959de8a85a282d53a6eca9040c7d952ed932d8a5d12d8107f75b83e5
translation: machine
translated_at: '2026-10-24'
---
# Pipelines CI/CD {#cicd-pipelines}

Le CI/CD automatise la compilation, les tests et le déploiement des logiciels. CI (Continuous Integration) intègre le code fréquemment grâce à des builds et des tests automatisés. CD (Continuous Delivery) rend chaque build déployable. Le Continuous Deployment déploie automatiquement les builds qui réussissent.

## Étapes du pipeline {#pipeline-stages}

```go
Code Push -> Build -> Test -> Package -> Deploy to Dev -> Deploy to QA -> Deploy to Prod
```

## Panorama des outils {#tools-landscape}

| Outil | Atout principal |
|-------|-----------------|
| Jenkins | Flexibilité, écosystème de plugins, auto-hébergé |
| GitLab CI | Intégré, aucun outil externe |
| GitHub Actions | Intégration native à GitHub |
| Azure DevOps | Intégration à l'écosystème Azure |
| CircleCI | Configuration simple |

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

### Pipeline YAML multi-étapes {#multi-stage-yaml-pipeline}

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

### Variables clés {#key-variables}

| Variable | Description |
|----------|-------------|
| `$(Build.BuildId)` | Numéro de build séquentiel |
| `$(Build.SourceVersion)` | SHA du commit Git |
| `$(Build.SourceBranchName)` | Nom de la branche |
| `$(Pipeline.Workspace)` | Racine de l'espace de travail du pipeline |

### Connexions de service {#service-connections}

Trois sont requises : GitHub (source), registre de conteneurs (push/pull) et Kubernetes (déploiement).

### Environnements et approbations {#environments-and-approvals}

Créez les environnements dans DevOps : Pipelines -> Environments. Ajoutez des vérifications d'approbation pour les déploiements en production.

## Terraform dans le CI/CD {#terraform-in-cicd}

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

## Stratégies de tagging des images Docker {#docker-image-tagging-strategies}

- `$(Build.BuildId)` - séquentiel, simple
- `$(Build.SourceVersion)` - SHA du commit Git, permet la traçabilité
- Versionnage sémantique - `v1.2.3`
- Basé sur la branche - `main-abc1234`

## Organisation des pipelines {#pipeline-organization}

- Renommez les pipelines pour plus de clarté : `01-docker-build-push-to-acr`
- Regroupez-les dans des dossiers : `app1-pipelines/`
- Désactivez les pipelines inutilisés
- Faites toujours un `git pull` après la création d'un pipeline (le YAML est commité automatiquement dans le dépôt)

## Points d'attention {#gotchas}

- `depends_on` dans les étapes Azure DevOps garantit l'ordre d'exécution
- Les vérifications d'approbation d'environnement bloquent le pipeline tant qu'il n'est pas approuvé
- Les pipelines Classic (GUI) et YAML coexistent, mais le YAML est préféré pour le contrôle de version
- Séparez les pipelines de build et de release, ou combinez-les dans un YAML multi-étapes
- `condition: succeeded()` est la valeur par défaut : ne l'écrivez explicitement que pour la clarté

## Voir aussi {#see-also}

- [[jenkins-automation]] - Patterns spécifiques à Jenkins
- [[gitops-and-argocd]] - Déploiement basé sur GitOps
- [[terraform-iac]] - Terraform dans les pipelines
- [[container-registries]] - Cibles de push/pull des images
- [[deployment-strategies]] - Blue-green, canary
