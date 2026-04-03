---
title: Jenkins Automation
category: concepts
tags: [devops, jenkins, cicd, pipeline, jenkinsfile, shared-libraries]
---

# Jenkins Automation

Jenkins is an automation server for CI/CD pipelines. It orchestrates builds, tests, and deployments via Jenkinsfiles (pipeline-as-code) or freestyle jobs. Jenkins itself is NOT CI - it's a server that runs automation.

## Architecture

- **Controller (Master)** - orchestrates pipelines, serves web UI. Should not run builds in production
- **Agents (Slaves)** - execute build jobs. Static VMs or dynamic (Docker, K8s pods)
- **Executors** - threads on an agent, each runs one build job

## Installation

```bash
sudo apt install openjdk-17-jdk -y
# Add Jenkins repo, install, start
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Default port: 8080. Directory: `/var/lib/jenkins/`.

## Declarative Pipeline (Jenkinsfile)

```groovy
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'myregistry.azurecr.io'
        IMAGE_NAME = 'myapp'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/repo.git'
            }
        }
        stage('Build') {
            steps { sh 'mvn clean package -DskipTests' }
        }
        stage('Test') {
            steps { sh 'mvn test' }
            post {
                always { junit 'target/surefire-reports/*.xml' }
            }
        }
        stage('Docker Build & Push') {
            steps {
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                withCredentials([usernamePassword(
                    credentialsId: 'acr-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS')]) {
                    sh "docker login ${DOCKER_REGISTRY} -u $USER -p $PASS"
                    sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh "kubectl set image deployment/myapp myapp=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded!' }
        failure { echo 'Pipeline failed!' }
        always  { cleanWs() }
    }
}
```

## Key Directives

| Directive | Purpose |
|-----------|---------|
| `agent` | Where to run (any, none, docker, kubernetes, label) |
| `environment` | Define env vars |
| `stages/stage` | Named phases |
| `steps` | Commands within a stage |
| `post` | After pipeline/stage (always, success, failure, changed) |
| `when` | Conditional execution |
| `parameters` | User input |
| `options` | Timeout, retry, timestamps |

## Parallel Stages

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests')       { steps { sh 'mvn test' } }
        stage('Integration Tests') { steps { sh 'mvn verify' } }
        stage('Lint')             { steps { sh 'npm run lint' } }
    }
}
```

## Parameters

```groovy
parameters {
    string(name: 'BRANCH', defaultValue: 'main')
    booleanParam(name: 'DEPLOY', defaultValue: false)
    choice(name: 'ENV', choices: ['dev', 'qa', 'prod'])
}
```

## Shared Libraries

Reusable pipeline code in a separate Git repo:

```groovy
// vars/buildDockerImage.groovy
def call(String imageName, String tag = env.BUILD_NUMBER) {
    sh "docker build -t ${imageName}:${tag} ."
    sh "docker push ${imageName}:${tag}"
}
```

Usage:
```groovy
@Library('my-shared-library') _
pipeline {
    stages {
        stage('Build') {
            steps { buildDockerImage('myregistry/myapp') }
        }
    }
}
```

## Docker Agent

```groovy
pipeline {
    agent {
        docker {
            image 'maven:3.9-openjdk-17'
            args '-v /root/.m2:/root/.m2'
        }
    }
}
```

## Multibranch Pipeline

Auto-discovers branches, creates pipelines per branch. Each needs a `Jenkinsfile`. Auto-creates for new branches, auto-deletes when branch deleted.

## Credentials

Types: Username/Password, Secret text, SSH key, Secret file, Certificate.

```groovy
withCredentials([
    usernamePassword(credentialsId: 'docker-hub',
        usernameVariable: 'USER', passwordVariable: 'PASS'),
    string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')
]) {
    sh "docker login -u $USER -p $PASS"
}
```

Scopes: Global (all jobs), System (Jenkins system only), Folder (specific folder).

## Build Triggers

- **Poll SCM**: `H/5 * * * *` (H = hash offset to spread load)
- **Webhook**: GitHub/GitLab POST on push (preferred)
- **Build periodically**: cron schedule
- **Triggered by other projects**: chain jobs

## Gotchas

- Jenkins is Java - needs adequate heap (`-Xmx1024m` or more)
- Docker-in-Docker via socket mount has security implications
- Avoid running Jenkins as root
- `H` in cron expressions spreads load - don't use `*` for minutes
- Freestyle jobs are GUI-only - prefer Jenkinsfile for version control

## See Also

- [[cicd-pipelines]] - general CI/CD concepts
- [[docker-fundamentals]] - Docker integration
- [[container-registries]] - Nexus as Docker registry
- [[kubernetes-workloads]] - deploying to K8s from Jenkins
