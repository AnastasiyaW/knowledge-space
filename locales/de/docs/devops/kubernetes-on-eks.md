---
title: "Kubernetes auf AWS (EKS)"
category: patterns
tags: [devops, kubernetes, aws, eks, ecr, eksctl, fargate]
level: 3
source_sha256: 244c60ad75508bd823fa1b7cac5fa2c0873d037139cef4bc4cd29ef18dd32002
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes auf AWS (EKS) {#kubernetes-on-aws-eks}

Elastic Kubernetes Service ist das verwaltete Kubernetes von AWS. Behandelt werden die Cluster-Erstellung mit eksctl, die ECR-Integration, Storage mit EBS/EFS und der ALB Ingress Controller.

## Cluster-Erstellung {#cluster-creation}

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

eksctl erstellt VPC, Subnetze, IAM-Rollen und Node Groups automatisch.

### Einrichtung des Access Entry {#access-entry-setup}

Wenn die Meldung „Your current IAM principal doesn't have access to Kubernetes objects" erscheint:
1. EKS -> Cluster -> Access -> Create access entry
2. IAM principal ARN: `arn:aws:iam::<account-id>:root`
3. Policy: AmazonEKSClusterAdminPolicy, scope: Cluster

## AWS ECS (Alternative) {#aws-ecs-alternative}

Für einfachere Container-Orchestrierung ohne Kubernetes:

- **Task Definition** - Blaupause: Image, CPU/Speicher, Port-Mappings, Umgebungsvariablen
- **Service** - betreibt N Tasks und hält die gewünschte Anzahl aufrecht
- **Fargate** - serverless, keine EC2-Verwaltung
- **EC2 launch type** - selbstverwaltete Instanzen

```yaml
# ECS + Fargate: serverless containers
# ECS + EFS: shared storage across tasks via NFS
# ECS + ALB: load balancing across tasks
# ECS + RDS: managed database backend
```

## Storage auf EKS {#storage-on-eks}

### EBS CSI Driver {#ebs-csi-driver}

Blockspeicher, RWO, einzelne AZ:
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

Erfordert eine IAM-Rolle für das Service Account mit AmazonEBSCSIDriverPolicy.

### EFS CSI Driver {#efs-csi-driver}

Dateispeicher, RWX, Multi-AZ:
```bash
helm install aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver
```

Security Group: NFS (Port 2049) von der Security Group der EKS-Worker erlauben.

### EBS vs. EFS {#ebs-vs-efs}

| Merkmal | EBS | EFS |
|---------|-----|-----|
| Typ | Block | Datei |
| Zugriff | RWO, einzelne AZ | RWX, Multi-AZ |
| Geschwindigkeit | Schneller | Höhere Latenz |
| Kosten | Günstiger | Teurer |

## ALB Ingress Controller {#alb-ingress-controller}

Verwaltet ALB/NLB für Kubernetes-Ingress-Ressourcen:

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

Der Target-Typ `ip` leitet direkt an Pod-IPs weiter. Erfordert das VPC-CNI-Plugin.

## NodePort auf EKS {#nodeport-on-eks}

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

Erfordert eine Security Group, die eingehenden TCP-Verkehr auf den NodePort (30000-32767) für die Worker-Knoten erlaubt.

## ECR-Integration {#ecr-integration}

```bash
# Create repository
aws ecr create-repository --repository-name myapp

# Login, build, push
aws ecr get-login-password | docker login --username AWS \
  --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag myapp:v1 <account>.dkr.ecr.<region>.amazonaws.com/myapp:v1
docker push <account>.dkr.ecr.<region>.amazonaws.com/myapp:v1
```

## Stolperfallen {#gotchas}

- eksctl erstellt Ressourcen in CloudFormation - Cluster daher mit `eksctl delete cluster` löschen
- NodePort erfordert eine manuelle Anpassung der Security Group an den Worker-Knoten
- EBS-Volumes sind an eine AZ gebunden - Pods können EBS nur in derselben AZ nutzen
- Der Standard-LoadBalancer erstellt einen Classic LB - für NLB die Annotation verwenden: `service.beta.kubernetes.io/aws-load-balancer-type: nlb`

## Siehe auch {#see-also}

- [[kubernetes-architecture]] - generelle K8s-Konzepte
- [[aws-cloud-fundamentals]] - EC2, VPC, IAM, S3
- [[container-registries]] - ECR-Details
- [[terraform-iac]] - Bereitstellung von EKS mit Terraform
