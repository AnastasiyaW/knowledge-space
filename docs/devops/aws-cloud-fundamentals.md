---
title: AWS Cloud Fundamentals
category: concepts
tags: [devops, aws, ec2, vpc, iam, s3, cloudwatch, networking]
---

# AWS Cloud Fundamentals

Core AWS services for DevOps: IAM for access control, VPC for networking, EC2 for compute, S3 for storage, and CloudWatch for monitoring.

## IAM (Identity and Access Management)

### Core Components

- **Users** - individual accounts with credentials
- **Groups** - collections of users sharing permissions
- **Roles** - assumable identities for services (no permanent credentials)
- **Policies** - JSON documents defining permissions

### Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
  }]
}
```

### Best Practices

- Root account: enable MFA, don't use for daily operations
- Principle of least privilege
- Use roles for EC2/Lambda (no embedded keys)
- Enable CloudTrail for audit
- Rotate access keys regularly

### CLI Configuration

```bash
aws configure
# Prompts for: Access Key ID, Secret Access Key, Region, Output
# Stored in ~/.aws/credentials and ~/.aws/config
```

## VPC (Virtual Private Cloud)

```
VPC (10.0.0.0/16)
  +-- Public Subnet (10.0.1.0/24) -- Internet Gateway -- Internet
  |     +-- EC2 instances (public IP), NAT Gateway
  +-- Private Subnet (10.0.2.0/24) -- NAT Gateway -- Internet (outbound only)
        +-- Databases, backend services
```

### Components

| Component | Purpose |
|-----------|---------|
| VPC | Isolated virtual network (CIDR block) |
| Subnet | Segment in specific AZ. Public = route to IGW |
| Internet Gateway | VPC-to-internet connectivity |
| NAT Gateway | Private subnet outbound (no inbound) |
| Route Table | Traffic routing rules |
| Security Group | Stateful instance-level firewall (allow only) |
| NACL | Stateless subnet-level firewall (allow + deny) |

### Security Groups vs NACLs

| Feature | Security Group | NACL |
|---------|---------------|------|
| Level | Instance | Subnet |
| Stateful | Yes | No |
| Rules | Allow only | Allow + Deny |
| Evaluation | All rules | Ordered by number |

## EC2 (Elastic Compute Cloud)

### Instance Types

| Family | Use Case |
|--------|----------|
| t2/t3 | General purpose, burstable |
| m5/m6i | General purpose, sustained |
| c5/c6i | Compute optimized |
| r5/r6i | Memory optimized |
| g4/p4 | GPU instances |

### Connecting

```bash
chmod 400 my-key.pem
ssh -i my-key.pem ec2-user@<public-ip>    # Amazon Linux
ssh -i my-key.pem ubuntu@<public-ip>      # Ubuntu
```

### User Data (Bootstrap)

```bash
#!/bin/bash
yum update -y
yum install docker -y
systemctl start docker && systemctl enable docker
docker run -d -p 80:80 nginx
```

### Docker on EC2 (Amazon Linux 2)

```bash
sudo yum update -y && sudo yum install docker -y
sudo systemctl start docker && sudo systemctl enable docker
sudo usermod -aG docker ec2-user
# Logout and login for group change
```

## S3 (Simple Storage Service)

```bash
aws s3 mb s3://my-bucket
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./dir s3://my-bucket/dir
aws s3 ls s3://my-bucket/
```

### Storage Classes

| Class | Use Case |
|-------|----------|
| Standard | Frequent access |
| Intelligent-Tiering | Unknown patterns |
| Standard-IA | Infrequent access |
| Glacier | Archive (minutes-hours retrieval) |
| Glacier Deep Archive | Long-term (12h retrieval) |

## CloudWatch

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "HighCPU" \
  --metric-name "CPUUtilization" \
  --namespace "AWS/EC2" \
  --statistic "Average" \
  --period 300 --threshold 80 \
  --comparison-operator "GreaterThanThreshold" \
  --alarm-actions arn:aws:sns:us-east-1:123456:alert-topic
```

States: OK -> ALARM -> INSUFFICIENT_DATA.

## ECR and App Runner

**ECR**: Private Docker registry. Push flow: `aws ecr get-login-password | docker login`, tag, push.

**App Runner**: Managed container deployment. Auto-scaling, HTTPS, load balancing. Points to ECR image. For HTTP workloads only.

## Route 53 + CloudFront

- **Route 53**: DNS service. Alias records for ALB/CloudFront/S3 (free, unlike CNAME)
- **CloudFront**: CDN. Edge caching for static content. Custom domains via ACM cert (must be us-east-1)

## Gotchas

- Stopped EC2 instances keep EBS but may lose public IP (use Elastic IP for static)
- Security groups are stateful but NACLs are not - configure both directions for NACLs
- S3 bucket names are globally unique
- IAM roles on EC2 are preferred over access keys - no credential rotation needed
- Default VPC exists per region but custom VPCs recommended for production

## See Also

- [[kubernetes-on-eks]] - EKS on AWS
- [[terraform-iac]] - provisioning AWS with Terraform
- [[container-registries]] - ECR details
- [[monitoring-and-observability]] - CloudWatch and Prometheus
