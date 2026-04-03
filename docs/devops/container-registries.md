---
title: Container Registries
category: concepts
tags: [devops, docker, ecr, acr, docker-hub, nexus, registry]
---

# Container Registries

Container registries store and distribute Docker images. Each cloud provider offers a managed registry, plus self-hosted options like Nexus.

## Docker Hub

Default public registry. Free to pull, registration required to push.

```bash
docker login
docker tag myapp:v1 username/myapp:v1
docker push username/myapp:v1
docker pull username/myapp:v1
```

Check before trusting community images: download count, last updated, Docker Official/Verified badges.

## AWS ECR (Elastic Container Registry)

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

**CI/CD**: CodeBuild with `buildspec.yml` builds and pushes to ECR.

## Azure ACR (Azure Container Registry)

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

For multi-registry: service principal + K8s image pull secrets.

## Google Artifact Registry (GAR)

Replaces GCR. `gcloud artifacts repositories create`, tag with `us-docker.pkg.dev/project/repo/image:tag`, push.

## Nexus (Self-Hosted)

Stores JARs, Docker images, npm packages. Configure Docker Bearer Token Realm.

```groovy
// Jenkins integration
nexusArtifactUploader(
    nexusVersion: 'nexus3',
    nexusUrl: 'nexus.company.com:8081',
    repository: 'maven-releases',
    artifacts: [[artifactId: 'myapp', type: 'jar', file: 'target/myapp.jar']]
)
```

Docker push: `docker push nexus.company.com:8083/myapp:tag`

## Image Pull Secrets (Kubernetes)

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

## Gotchas

- ECR login tokens expire after 12 hours
- ACR `az aks update --attach-acr` is simplest but works only for single registry
- Image tags are mutable - same tag can point to different images. Pin by digest for immutability
- Registry cleanup: set lifecycle policies to delete old/untagged images
- `latest` tag convention misleads - always use specific version tags

## See Also

- [[docker-fundamentals]] - image basics
- [[dockerfile-and-image-building]] - building images to push
- [[cicd-pipelines]] - automated push in pipelines
- [[kubernetes-on-aks]] - ACR integration with AKS
- [[kubernetes-on-eks]] - ECR integration with EKS
