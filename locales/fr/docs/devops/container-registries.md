---
title: "Registres de conteneurs"
category: concepts
tags: [devops, docker, ecr, acr, docker-hub, nexus, registry]
level: 3
source_sha256: 76824a7308f22a0a187e619205bad3c67af62e0150153420a89b4be2b243029f
translation: machine
translated_at: '2026-10-24'
---
# Registres de conteneurs {#container-registries}

Les registres de conteneurs stockent et distribuent les images Docker. Chaque fournisseur cloud propose un registre managé, ainsi que des options auto-hébergées comme Nexus.

## Docker Hub {#docker-hub}

Registre public par défaut. Gratuit pour le pull, inscription requise pour le push.

```bash
docker login
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
docker pull username/myapp:v1
```

Vérifiez avant de faire confiance aux images communautaires : nombre de téléchargements, date de dernière mise à jour, badges Docker Official/Verified.

## AWS ECR (Elastic Container Registry) {#aws-ecr-elastic-container-registry}

```bash
aws ecr create-repository --repository-name myapp

# Login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account>.dkr.ecr.us-east-1.amazonaws.com

# Push
docker tag myapp:v1 <account>.dkr.ecr.us-east-1.amazonaws.com/myapp:v1
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/myapp:v1
```

**CI/CD** : CodeBuild avec `buildspec.yml` construit et pousse les images vers ECR.

## Azure ACR (Azure Container Registry) {#azure-acr-azure-container-registry}

```bash
az acr create -g $RG -n $ACR_NAME --sku Basic
az acr login --name $ACR_NAME
docker tag myapp:latest $ACR_NAME.azurecr.io/myapp:v1
docker push $ACR_NAME.azurecr.io/myapp:v1

# Attach to AKS (simplest auth)
az aks update -n $CLUSTER -g $RG --attach-acr $ACR_NAME

# Or build directly in ACR
az acr build --registry $ACR_NAME --image myapp:v1 .
```

Pour le multi-registre : service principal + secrets de pull d'images K8s.

## Google Artifact Registry (GAR) {#google-artifact-registry-gar}

Remplace GCR. `gcloud artifacts repositories create`, taguer avec `us-docker.pkg.dev/project/repo/image:tag`, puis pousser.

## Nexus (auto-hébergé) {#nexus-self-hosted}

Stocke les JAR, les images Docker et les paquets npm. Configurer le Docker Bearer Token Realm.

```groovy
// Jenkins integration
nexusArtifactUploader(
    nexusVersion: 'nexus3',
    nexusUrl: 'nexus.company.com:8081',
    repository: 'maven-releases',
    artifacts: [[artifactId: 'myapp', type: 'jar', file: 'target/myapp.jar']]
)
```

Push Docker : `docker push nexus.company.com:8083/myapp:tag`

## Secrets de pull d'images (Kubernetes) {#image-pull-secrets-kubernetes}

```bash
kubectl create secret docker-registry acr-secret \
  --docker-server=$REGISTRY \
  --docker-username=$USER \
  --docker-password=$PASSWORD
```

```yaml
spec:
  imagePullSecrets:
  - name: acr-secret
```

## Pièges à éviter {#gotchas}

- Les tokens de connexion ECR expirent après 12 heures
- `az aks update --attach-acr` est le plus simple, mais ne fonctionne que pour un seul registre
- Les tags d'images sont mutables : le même tag peut pointer vers des images différentes. Épinglez par digest pour garantir l'immutabilité
- Nettoyage des registres : définissez des lifecycle policies pour supprimer les anciennes images et les images sans tag
- La convention du tag `latest` induit en erreur : utilisez toujours des tags de version spécifiques

## Voir aussi {#see-also}

- [[docker-fundamentals]] - bases des images
- [[dockerfile-and-image-building]] - construction des images à pousser
- [[cicd-pipelines]] - push automatisé dans les pipelines
- [[kubernetes-on-aks]] - intégration d'ACR avec AKS
- [[kubernetes-on-eks]] - intégration d'ECR avec EKS
