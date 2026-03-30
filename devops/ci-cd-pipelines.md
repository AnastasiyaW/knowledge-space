---
title: CI/CD Pipelines
category: automation
tags: [ci-cd, jenkins, gitlab-ci, github-actions, pipelines, automation, testing]
---
# CI/CD Pipelines

Continuous Integration and Continuous Delivery/Deployment: automated build, test, and deploy workflows.

## Key Facts

- **CI** (Continuous Integration) = auto-build and test on every commit; catch bugs early
- **CD** = Continuous Delivery (manual deploy gate) or Continuous Deployment (auto-deploy to production)
- Pipeline stages typically: lint -> build -> test -> security scan -> deploy staging -> deploy prod
- **Jenkins** = self-hosted, Groovy-based `Jenkinsfile`; highly extensible plugin ecosystem
- **GitLab CI** = `.gitlab-ci.yml`; built into GitLab; runners execute jobs; shared or self-hosted
- **GitHub Actions** = `.github/workflows/*.yml`; event-driven; marketplace of reusable actions
- Artifacts = build outputs passed between stages (compiled binaries, Docker images, test reports)
- **Pipeline as Code** = pipeline definition versioned alongside application code
- [[docker-images-containers]] are commonly built and pushed in CI
- [[terraform-iac]] plan/apply integrated into CD pipelines
- [[helm-charts]] deployed as final CD step
- Branch-based workflows: `main` = prod, `develop` = staging, feature branches = CI only

## Patterns

```yaml
# GitHub Actions workflow
name: CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
    - run: npm test
    - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/build-push-action@v5
      with:
        push: true
        tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v4
    - run: |
        helm upgrade --install myapp ./chart \
          --set image.tag=${{ github.sha }} \
          --namespace production
```

```yaml
# GitLab CI (.gitlab-ci.yml)
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pytest --cov=app tests/

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

deploy_prod:
  stage: deploy
  environment: production
  when: manual
  only:
    - main
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
```

```groovy
// Jenkinsfile (declarative pipeline)
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
    post {
        failure {
            slackSend channel: '#alerts', message: "Build failed: ${env.JOB_NAME}"
        }
    }
}
```

## Gotchas

- Secrets in CI: use encrypted variables / vault integration; NEVER hardcode in pipeline files
- Docker-in-Docker (DinD) has security implications; prefer kaniko or buildah for rootless builds
- GitHub Actions: `actions/checkout@v4` only checks out current commit by default; add `fetch-depth: 0` for full history
- GitLab CI: jobs in same stage run in parallel by default; use `needs:` for DAG-based pipelines
- Cache vs artifacts: cache = speed up future runs (dependencies); artifacts = pass data between stages
- Self-hosted runners/agents need maintenance; use ephemeral runners when possible
- Pipeline secrets exposed in logs if `echo`'d; mask sensitive values in all CI platforms
- `when: manual` in GitLab creates a gate; `environment: production` in GitHub requires approval rules

## See Also

- [[docker-images-containers]] - building images in CI
- [[helm-charts]] - deploying charts in CD
- [[terraform-iac]] - infrastructure deployment pipelines
- [[gitops]] - pull-based CD alternative
- GitHub Actions docs: https://docs.github.com/en/actions
- GitLab CI docs: https://docs.gitlab.com/ee/ci/
