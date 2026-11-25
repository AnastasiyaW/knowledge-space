---
title: "Container-Registries"
category: concepts
tags: [devops, docker, ecr, acr, docker-hub, nexus, registry]
level: 3
source_sha256: 76824a7308f22a0a187e619205bad3c67af62e0150153420a89b4be2b243029f
translation: machine
translated_at: '2026-10-24'
---
# Container-Registries {#container-registries}

Container-Registries speichern und verteilen Docker-Images. Jeder Cloud-Anbieter bietet eine verwaltete Registry an, dazu gibt es selbst gehostete Optionen wie Nexus.

## Docker Hub {#docker-hub}

Standardmäßige öffentliche Registry. Pull ist kostenlos, zum Push ist eine Registrierung erforderlich.

```bash
docker login
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
docker pull username/myapp:v1
```

Vor dem Vertrauen in Community-Images prüfen: Download-Anzahl, letzte Aktualisierung, Docker-Official- und Verified-Badges.

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

**CI/CD**: CodeBuild mit `buildspec.yml` baut Images und pusht sie nach ECR.

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

Für mehrere Registries: Service Principal + K8s-Image-Pull-Secrets.

## Google Artifact Registry (GAR) {#google-artifact-registry-gar}

Ersetzt GCR. `gcloud artifacts repositories create` ausführen, mit `us-docker.pkg.dev/project/repo/image:tag` taggen und pushen.

## Nexus (Self-Hosted) {#nexus-self-hosted}

Speichert JARs, Docker-Images und npm-Pakete. Docker Bearer Token Realm konfigurieren.

```groovy
// Jenkins integration
nexusArtifactUploader(
    nexusVersion: 'nexus3',
    nexusUrl: 'nexus.company.com:8081',
    repository: 'maven-releases',
    artifacts: [[artifactId: 'myapp', type: 'jar', file: 'target/myapp.jar']]
)
```

Docker-Push: `docker push nexus.company.com:8083/myapp:tag`

## Image Pull Secrets (Kubernetes) {#image-pull-secrets-kubernetes}

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

## Gotchas {#gotchas}

- ECR-Login-Tokens laufen nach 12 Stunden ab
- `az aks update --attach-acr` ist am einfachsten, funktioniert aber nur für eine einzelne Registry
- Image-Tags sind veränderlich – derselbe Tag kann auf unterschiedliche Images zeigen. Für Unveränderlichkeit per Digest pinnen
- Registry-Bereinigung: Lifecycle-Policies setzen, um alte und untaggte Images zu löschen
- Die `latest`-Tag-Konvention ist irreführend – immer spezifische Versions-Tags verwenden

## Siehe auch {#see-also}

- [[docker-fundamentals]] - Grundlagen zu Images
- [[dockerfile-and-image-building]] - Images bauen, die gepusht werden
- [[cicd-pipelines]] - automatisierter Push in Pipelines
- [[kubernetes-on-aks]] - ACR-Integration mit AKS
- [[kubernetes-on-eks]] - ECR-Integration mit EKS
