---
title: "Jenkins-Automatisierung"
category: concepts
tags: [devops, jenkins, cicd, pipeline, jenkinsfile, shared-libraries]
level: 3
source_sha256: 32087e42b100b0d2a73a9671a1e2ad141d92a90bfce51438a2c78115460d09ba
translation: machine
translated_at: '2026-10-24'
---
# Jenkins-Automatisierung {#jenkins-automation}

Jenkins ist ein Automatisierungsserver für CI/CD-Pipelines. Er orchestriert Builds, Tests und Deployments über Jenkinsfiles (Pipeline-as-Code) oder Freestyle-Jobs. Jenkins selbst ist NICHT CI – es ist ein Server, der Automatisierung ausführt.

## Architektur {#architecture}

- **Controller (Master)** – orchestriert Pipelines, stellt die Web-UI bereit. Sollte in Produktion keine Builds ausführen
- **Agents (Slaves)** – führen Build-Jobs aus. Statische VMs oder dynamisch (Docker, K8s-Pods)
- **Executors** – Threads auf einem Agent; jeder führt genau einen Build-Job aus

## Installation {#installation}

```bash
sudo apt install openjdk-17-jdk -y
# Add Jenkins repo, install, start
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Standardport: 8080. Verzeichnis: `/var/lib/jenkins/`.

## Deklarative Pipeline (Jenkinsfile) {#declarative-pipeline-jenkinsfile}

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

## Wichtige Direktiven {#key-directives}

| Direktive | Zweck |
|-----------|-------|
| `agent` | Wo ausgeführt werden soll (any, none, docker, kubernetes, label) |
| `environment` | Umgebungsvariablen definieren |
| `stages/stage` | Benannte Phasen |
| `steps` | Befehle innerhalb einer Stage |
| `post` | Nach Pipeline/Stage (always, success, failure, changed) |
| `when` | Bedingte Ausführung |
| `parameters` | Benutzereingaben |
| `options` | Timeout, Retry, Zeitstempel |

## Parallele Stages {#parallel-stages}

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests')       { steps { sh 'mvn test' } }
        stage('Integration Tests') { steps { sh 'mvn verify' } }
        stage('Lint')             { steps { sh 'npm run lint' } }
    }
}
```

## Parameter {#parameters}

```groovy
parameters {
    string(name: 'BRANCH', defaultValue: 'main')
    booleanParam(name: 'DEPLOY', defaultValue: false)
    choice(name: 'ENV', choices: ['dev', 'qa', 'prod'])
}
```

## Shared Libraries {#shared-libraries}

Wiederverwendbarer Pipeline-Code in einem separaten Git-Repository:

```groovy
// vars/buildDockerImage.groovy
def call(String imageName, String tag = env.BUILD_NUMBER) {
    sh "docker build -t ${imageName}:${tag} ."
    sh "docker push ${imageName}:${tag}"
}
```

Verwendung:
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

## Docker-Agent {#docker-agent}

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

## Multibranch-Pipeline {#multibranch-pipeline}

Erkennt Branches automatisch und erstellt pro Branch eine Pipeline. Jede benötigt ein `Jenkinsfile`. Wird für neue Branches automatisch angelegt und beim Löschen des Branches automatisch entfernt.

## Credentials {#credentials}

Typen: Benutzername/Passwort, Secret-Text, SSH-Schlüssel, Secret-Datei, Zertifikat.

```groovy
withCredentials([
    usernamePassword(credentialsId: 'docker-hub',
        usernameVariable: 'USER', passwordVariable: 'PASS'),
    string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')
]) {
    sh "docker login -u $USER -p $PASS"
}
```

Geltungsbereiche: Global (alle Jobs), System (nur Jenkins-System), Ordner (bestimmter Ordner).

## Build-Trigger {#build-triggers}

- **Poll SCM**: `H/5 * * * *` (H = Hash-Offset, um die Last zu verteilen)
- **Webhook**: GitHub/GitLab-POST bei Push (bevorzugt)
- **Build periodisch**: Cron-Zeitplan
- **Durch andere Projekte ausgelöst**: Jobs verketten

## Stolperfallen {#gotchas}

- Jenkins ist in Java geschrieben – benötigt ausreichend Heap (`-Xmx1024m` oder mehr)
- Docker-in-Docker über Socket-Mount hat Sicherheitsimplikationen
- Jenkins nicht als root betreiben
- `H` in Cron-Ausdrücken verteilt die Last – `*` bei den Minuten nicht verwenden
- Freestyle-Jobs sind nur über die GUI konfigurierbar – für Versionskontrolle ein Jenkinsfile bevorzugen

## Siehe auch {#see-also}

- [[cicd-pipelines]] – allgemeine CI/CD-Konzepte
- [[docker-fundamentals]] – Docker-Integration
- [[container-registries]] – Nexus als Docker-Registry
- [[kubernetes-workloads]] – Deployment aus Jenkins auf K8s
