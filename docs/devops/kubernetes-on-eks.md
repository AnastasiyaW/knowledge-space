---
title: Kubernetes on AWS (EKS)
category: patterns
tags: [devops, kubernetes, aws, eks, ecr, eksctl, fargate]
---

# Kubernetes on AWS (EKS)

Elastic Kubernetes Service is AWS's managed Kubernetes. Covers cluster creation with eksctl, ECR integration, storage with EBS/EFS, and ALB Ingress Controller.

## Cluster Creation

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

eksctl creates VPC, subnets, IAM roles, and node groups automatically.

### Access Entry Setup

If "Your current IAM principal doesn't have access to Kubernetes objects":
1. EKS -> Cluster -> Access -> Create access entry
2. IAM principal ARN: `arn:aws:iam::<account-id>:root`
3. Policy: AmazonEKSClusterAdminPolicy, scope: Cluster

## AWS ECS (Alternative)

For simpler container orchestration without Kubernetes:

- **Task Definition** - blueprint: image, CPU/memory, port mappings, env vars
- **Service** - runs N tasks, maintains desired count
- **Fargate** - serverless, no EC2 management
- **EC2 launch type** - self-managed instances

```yaml
# ECS + Fargate: serverless containers
# ECS + EFS: shared storage across tasks via NFS
# ECS + ALB: load balancing across tasks
# ECS + RDS: managed database backend
```

## Storage on EKS

### EBS CSI Driver

Block storage, RWO, single AZ:
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

Requires IAM role for service account with AmazonEBSCSIDriverPolicy.

### EFS CSI Driver

File storage, RWX, multi-AZ:
```bash
helm install aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver
```

Security group: allow NFS (port 2049) from EKS worker SG.

### EBS vs EFS

| Feature | EBS | EFS |
|---------|-----|-----|
| Type | Block | File |
| Access | RWO, single AZ | RWX, multi-AZ |
| Speed | Faster | Higher latency |
| Cost | Cheaper | More expensive |

## ALB Ingress Controller

Manages ALB/NLB for Kubernetes Ingress resources:

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

Target type `ip` routes directly to pod IPs. Requires VPC CNI plugin.

## NodePort on EKS

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

Requires security group allowing inbound TCP on NodePort (30000-32767) for worker nodes.

## ECR Integration

```bash
# Create repository
aws ecr create-repository --repository-name myapp

# Login, build, push
aws ecr get-login-password | docker login --username AWS \
  --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag myapp:v1 <account>.dkr.ecr.<region>.amazonaws.com/myapp:v1
docker push <account>.dkr.ecr.<region>.amazonaws.com/myapp:v1
```

## Gotchas

- eksctl creates resources in CloudFormation - delete cluster via `eksctl delete cluster`
- NodePort requires manual security group update on worker nodes
- EBS volumes are AZ-bound - pods can only use EBS in the same AZ
- Default LoadBalancer creates Classic LB - use annotation for NLB: `service.beta.kubernetes.io/aws-load-balancer-type: nlb`

## See Also

- [[kubernetes-architecture]] - generic K8s concepts
- [[aws-cloud-fundamentals]] - EC2, VPC, IAM, S3
- [[container-registries]] - ECR details
- [[terraform-iac]] - provisioning EKS with Terraform
