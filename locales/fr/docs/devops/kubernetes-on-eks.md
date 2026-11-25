---
title: "Kubernetes sur AWS (EKS)"
category: patterns
tags: [devops, kubernetes, aws, eks, ecr, eksctl, fargate]
level: 3
source_sha256: 244c60ad75508bd823fa1b7cac5fa2c0873d037139cef4bc4cd29ef18dd32002
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes sur AWS (EKS) {#kubernetes-on-aws-eks}

Elastic Kubernetes Service est le service Kubernetes géré d'AWS. Couvre la création de cluster avec eksctl, l'intégration ECR, le stockage avec EBS/EFS et l'ALB Ingress Controller.

## Création du cluster {#cluster-creation}

```bash
# Using eksctl (recommended)
eksctl create cluster \
  --name my-cluster \
  --region us-east-1 \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 2 \
  --full-ecr-access \
  --alb-ingress-access

# Configure kubectl
aws eks update-kubeconfig --name my-cluster --region us-east-1
```

eksctl crée automatiquement le VPC, les subnets, les rôles IAM et les node groups.

### Configuration de l'access entry {#access-entry-setup}

Si le message « Your current IAM principal doesn't have access to Kubernetes objects » apparaît :
1. EKS -> Cluster -> Access -> Create access entry
2. IAM principal ARN : `arn:aws:iam::<account-id>:root`
3. Policy : AmazonEKSClusterAdminPolicy, scope : Cluster

## AWS ECS (alternative) {#aws-ecs-alternative}

Pour une orchestration de conteneurs plus simple, sans Kubernetes :

- **Task Definition** - modèle : image, CPU/mémoire, mappings de ports, variables d'environnement
- **Service** - exécute N tâches et maintient le nombre souhaité
- **Fargate** - serverless, pas de gestion d'instances EC2
- **Type de lancement EC2** - instances gérées par vos soins

```yaml
# ECS + Fargate: serverless containers
# ECS + EFS: shared storage across tasks via NFS
# ECS + ALB: load balancing across tasks
# ECS + RDS: managed database backend
```

## Stockage sur EKS {#storage-on-eks}

### EBS CSI Driver {#ebs-csi-driver}

Stockage bloc, RWO, mono-AZ :
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
volumeBindingMode: WaitForFirstConsumer
```

Nécessite un rôle IAM pour le service account avec la policy AmazonEBSCSIDriverPolicy.

### EFS CSI Driver {#efs-csi-driver}

Stockage de fichiers, RWX, multi-AZ :
```bash
helm install aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver
```

Security group : autoriser NFS (port 2049) depuis le security group des workers EKS.

### EBS vs EFS {#ebs-vs-efs}

| Caractéristique | EBS | EFS |
|---------|-----|-----|
| Type | Bloc | Fichier |
| Accès | RWO, mono-AZ | RWX, multi-AZ |
| Vitesse | Plus rapide | Latence plus élevée |
| Coût | Moins cher | Plus cher |

## ALB Ingress Controller {#alb-ingress-controller}

Gère les ALB/NLB pour les ressources Ingress de Kubernetes :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:...
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

Le target type `ip` route directement vers les IP des pods. Nécessite le plugin VPC CNI.

## NodePort sur EKS {#nodeport-on-eks}

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

Nécessite un security group autorisant le trafic TCP entrant sur le NodePort (30000-32767) pour les nœuds workers.

## Intégration ECR {#ecr-integration}

```bash
# Create repository
aws ecr create-repository --repository-name myapp

# Login, build, push
aws ecr get-login-password | docker login --username AWS \
  --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag myapp:v1 <account>.dkr.ecr.<region>.amazonaws.com/myapp:v1
docker push <account>.dkr.ecr.<region>.amazonaws.com/myapp:v1
```

## Pièges à éviter {#gotchas}

- eksctl crée les ressources dans CloudFormation - supprimez le cluster avec `eksctl delete cluster`
- NodePort nécessite une mise à jour manuelle du security group sur les nœuds workers
- Les volumes EBS sont liés à une AZ - les pods ne peuvent utiliser EBS que dans la même AZ
- Le LoadBalancer par défaut crée un Classic LB - utilisez l'annotation pour un NLB : `service.beta.kubernetes.io/aws-load-balancer-type: nlb`

## Voir aussi {#see-also}

- [[kubernetes-architecture]] - concepts Kubernetes génériques
- [[aws-cloud-fundamentals]] - EC2, VPC, IAM, S3
- [[container-registries]] - détails sur ECR
- [[terraform-iac]] - provisionnement d'EKS avec Terraform
