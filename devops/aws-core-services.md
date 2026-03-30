---
title: AWS Core Services
category: cloud
tags: [aws, ec2, s3, iam, vpc, rds, eks, cloud-infrastructure]
---
# AWS Core Services

Essential AWS services for compute, storage, networking, identity, and managed Kubernetes.

## Key Facts

- **EC2** = virtual servers (instances); instance types define CPU/RAM/GPU (t3.micro, m6i.large, p4d.24xlarge)
- **S3** = object storage; buckets with globally unique names; 11 nines durability
- **IAM** = Identity & Access Management; users, groups, roles, policies; principle of least privilege
- **VPC** = Virtual Private Cloud; isolated network; subnets (public/private), route tables, security groups
- **RDS** = managed relational databases (PostgreSQL, MySQL, Aurora); automated backups, multi-AZ
- **EKS** = managed Kubernetes; AWS manages control plane; you manage worker nodes or use Fargate
- **ECR** = Elastic Container Registry; private Docker image storage
- **ELB** = Load Balancers: ALB (HTTP/HTTPS, layer 7), NLB (TCP/UDP, layer 4), CLB (legacy)
- **Route53** = DNS service; hosted zones, A/CNAME/ALIAS records, health checks
- **CloudWatch** = monitoring and logging; metrics, alarms, log groups
- Security Groups = stateful firewall at instance level; NACLs = stateless at subnet level
- [[terraform-iac]] is the primary tool for provisioning AWS resources as code
- [[kubernetes-pods]] run on EKS worker nodes

## Patterns

```bash
# EC2
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --key-name mykey \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0

aws ec2 describe-instances --filters "Name=tag:Name,Values=web-*"
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# S3
aws s3 mb s3://my-unique-bucket
aws s3 cp file.txt s3://my-bucket/path/
aws s3 sync ./local-dir s3://my-bucket/prefix/
aws s3 ls s3://my-bucket/prefix/
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# IAM
aws iam create-user --user-name deploy-bot
aws iam attach-user-policy --user-name deploy-bot \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# EKS
aws eks update-kubeconfig --name my-cluster --region us-east-1
kubectl get nodes   # after kubeconfig is set

# ECR
aws ecr get-login-password | docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.us-east-1.amazonaws.com
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

```hcl
# Terraform - VPC + EC2 (minimal)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Gotchas

- S3 bucket names are globally unique across ALL AWS accounts; use company prefix
- Security Groups are stateful (allow return traffic); NACLs are stateless (must allow both directions)
- EC2 instances in private subnets need NAT Gateway for outbound internet (costs money)
- IAM policies: explicit `Deny` always wins over `Allow`; default is implicit deny
- EKS costs: control plane (~$0.10/hr) + worker nodes (EC2 pricing); Fargate is per-pod pricing
- `aws configure` stores credentials in `~/.aws/credentials` plaintext; prefer IAM roles for EC2/EKS
- S3 eventual consistency for overwrite PUTs and DELETEs (strong consistency for new objects since 2020)
- Regions and AZs matter: resources in `us-east-1a` cannot directly access `eu-west-1a`

## See Also

- [[terraform-iac]] - infrastructure as code for AWS
- [[kubernetes-pods]] - workloads on EKS
- [[azure-aks]] - equivalent Azure services
- [[monitoring-observability]] - CloudWatch integration
- AWS docs: https://docs.aws.amazon.com/
- AWS CLI reference: https://awscli.amazonaws.com/v2/documentation/api/latest/index.html
