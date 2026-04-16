---
title: CI/CD Pipelines
category: concepts
tags: [devops, cicd, jenkins, github-actions, azure-devops, continuous-integration, continuous-delivery]
---

# CI/CD Pipelines

CI/CD automates building, testing, and deploying software. CI (Continuous Integration) integrates code frequently with automated builds/tests. CD (Continuous Delivery) makes every build deployable. Continuous Deployment auto-deploys passing builds.

## Pipeline Stages

```go
Code Push -> Build -> Test -> Package -> Deploy to Dev -> Deploy to QA -> Deploy to Prod
```

## Tools Landscape

| Tool | Key Advantage |
|------|---------------|
| Jenkins | Flexibility, plugin ecosystem, self-hosted |
| GitLab CI | Built-in, no external tools |
| GitHub Actions | Native GitHub integration |
| Azure DevOps | Azure ecosystem integration |
| CircleCI | Simple configuration |

## GitHub Actions

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

## Azure DevOps Pipelines

### Multi-Stage YAML Pipeline

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

### Key Variables

| Variable | Description |
|----------|-------------|
| `$(Build.BuildId)` | Sequential build number |
| `$(Build.SourceVersion)` | Git commit SHA |
| `$(Build.SourceBranchName)` | Branch name |
| `$(Pipeline.Workspace)` | Pipeline workspace root |

### Service Connections

Three required: GitHub (source), Container Registry (push/pull), Kubernetes (deploy).

### Environments and Approvals

Create environments in DevOps: Pipelines -> Environments. Add approval checks for production deployments.

## Terraform in CI/CD

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

## Docker Image Tagging Strategies

- `$(Build.BuildId)` - sequential, simple
- `$(Build.SourceVersion)` - git commit SHA, enables traceability
- Semantic versioning - `v1.2.3`
- Branch-based - `main-abc1234`

## Pipeline Organization

- Rename pipelines for clarity: `01-docker-build-push-to-acr`
- Group in folders: `app1-pipelines/`
- Disable unused pipelines
- Always `git pull` after pipeline creation (YAML auto-committed to repo)

## Gotchas

- `depends_on` in Azure DevOps stages ensures execution order
- Environment approval checks block pipeline until approved
- Classic (GUI) and YAML pipelines coexist but YAML is preferred for version control
- Separate build and release pipelines or combine into multi-stage YAML
- `condition: succeeded()` is default - explicit only for clarity

## See Also

- [[jenkins-automation]] - Jenkins-specific patterns
- [[gitops-and-argocd]] - GitOps-based deployment
- [[terraform-iac]] - Terraform in pipelines
- [[container-registries]] - image push/pull targets
- [[deployment-strategies]] - blue-green, canary
