---
title: "Automatisation avec Jenkins"
category: concepts
tags: [devops, jenkins, cicd, pipeline, jenkinsfile, shared-libraries]
level: 3
source_sha256: 32087e42b100b0d2a73a9671a1e2ad141d92a90bfce51438a2c78115460d09ba
translation: machine
translated_at: '2026-10-24'
---
# Automatisation avec Jenkins {#jenkins-automation}

Jenkins est un serveur d'automatisation pour les pipelines CI/CD. Il orchestre les builds, les tests et les déploiements via des Jenkinsfiles (pipeline-as-code) ou des jobs freestyle. Jenkins lui-même n'est PAS de la CI : c'est un serveur qui exécute de l'automatisation.

## Architecture {#architecture}

- **Contrôleur (Master)** - orchestre les pipelines, sert l'interface web. Ne doit pas exécuter de builds en production
- **Agents (Slaves)** - exécutent les jobs de build. VMs statiques ou dynamiques (Docker, pods K8s)
- **Executors** - threads sur un agent, chacun exécute un job de build

## Installation {#installation}

```bash
sudo apt install openjdk-17-jdk -y
# Add Jenkins repo, install, start
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Port par défaut : 8080. Répertoire : `/var/lib/jenkins/`.

## Pipeline déclaratif (Jenkinsfile) {#declarative-pipeline-jenkinsfile}

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

## Directives principales {#key-directives}

| Directive | Rôle |
|-----------|------|
| `agent` | Où exécuter (any, none, docker, kubernetes, label) |
| `environment` | Définir des variables d'environnement |
| `stages/stage` | Phases nommées |
| `steps` | Commandes au sein d'une étape |
| `post` | Après le pipeline/l'étape (always, success, failure, changed) |
| `when` | Exécution conditionnelle |
| `parameters` | Saisie utilisateur |
| `options` | Timeout, retry, timestamps |

## Étapes parallèles {#parallel-stages}

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests')       { steps { sh 'mvn test' } }
        stage('Integration Tests') { steps { sh 'mvn verify' } }
        stage('Lint')             { steps { sh 'npm run lint' } }
    }
}
```

## Paramètres {#parameters}

```groovy
parameters {
    string(name: 'BRANCH', defaultValue: 'main')
    booleanParam(name: 'DEPLOY', defaultValue: false)
    choice(name: 'ENV', choices: ['dev', 'qa', 'prod'])
}
```

## Bibliothèques partagées {#shared-libraries}

Code de pipeline réutilisable dans un dépôt Git séparé :

```groovy
// vars/buildDockerImage.groovy
def call(String imageName, String tag = env.BUILD_NUMBER) {
    sh "docker build -t ${imageName}:${tag} ."
    sh "docker push ${imageName}:${tag}"
}
```

Utilisation :
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

## Agent Docker {#docker-agent}

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

## Multibranch Pipeline {#multibranch-pipeline}

Détecte automatiquement les branches et crée un pipeline par branche. Chacune nécessite un `Jenkinsfile`. Création automatique pour les nouvelles branches, suppression automatique à la suppression de la branche.

## Identifiants (Credentials) {#credentials}

Types : Username/Password, Secret text, clé SSH, Secret file, Certificate.

```groovy
withCredentials([
    usernamePassword(credentialsId: 'docker-hub',
        usernameVariable: 'USER', passwordVariable: 'PASS'),
    string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')
]) {
    sh "docker login -u $USER -p $PASS"
}
```

Portées : Global (tous les jobs), System (système Jenkins uniquement), Folder (dossier spécifique).

## Déclencheurs de build {#build-triggers}

- **Poll SCM** : `H/5 * * * *` (H = décalage de hachage pour répartir la charge)
- **Webhook** : POST GitHub/GitLab lors d'un push (à privilégier)
- **Build périodique** : planification cron
- **Déclenché par d'autres projets** : chaînage de jobs

## Pièges à éviter {#gotchas}

- Jenkins est en Java : il nécessite un heap suffisant (`-Xmx1024m` ou plus)
- Docker-in-Docker via montage de socket a des implications de sécurité
- Éviter d'exécuter Jenkins en root
- `H` dans les expressions cron répartit la charge : ne pas utiliser `*` pour les minutes
- Les jobs freestyle ne se configurent que via l'interface graphique : préférer un Jenkinsfile pour le versionnement

## Voir aussi {#see-also}

- [[cicd-pipelines]] - concepts généraux de CI/CD
- [[docker-fundamentals]] - intégration Docker
- [[container-registries]] - Nexus comme registre Docker
- [[kubernetes-workloads]] - déploiement vers K8s depuis Jenkins
