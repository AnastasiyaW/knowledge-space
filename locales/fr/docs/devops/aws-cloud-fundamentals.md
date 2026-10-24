---
title: "Fondamentaux du cloud AWS"
category: concepts
tags: [devops, aws, ec2, vpc, iam, s3, cloudwatch, networking]
level: 2
source_sha256: f73594b950b6d1a00c545c210d22a2535667a41afa4f5d6e5b312e372e99ad8d
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux du cloud AWS {#aws-cloud-fundamentals}

Services AWS essentiels pour le DevOps : IAM pour le contrôle d'accès, VPC pour le réseau, EC2 pour le calcul, S3 pour le stockage et CloudWatch pour la supervision.

## IAM (Identity and Access Management) {#iam-identity-and-access-management}

### Composants principaux {#core-components}

- **Utilisateurs** - comptes individuels avec identifiants
- **Groupes** - ensembles d'utilisateurs partageant des permissions
- **Rôles** - identités assumables par des services (sans identifiants permanents)
- **Politiques** - documents JSON définissant les permissions

### Structure d'une politique {#policy-structure}

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

### Bonnes pratiques {#best-practices}

- Compte root : activer le MFA, ne pas l'utiliser pour les opérations quotidiennes
- Principe du moindre privilège
- Utiliser des rôles pour EC2/Lambda (pas de clés intégrées)
- Activer CloudTrail pour l'audit
- Renouveler les clés d'accès régulièrement

### Configuration de la CLI {#cli-configuration}

```bash
aws configure
# Prompts for: Access Key ID, Secret Access Key, Region, Output
# Stored in ~/.aws/credentials and ~/.aws/config
```

## VPC (Virtual Private Cloud) {#vpc-virtual-private-cloud}

```java
VPC (10.0.0.0/16)
  +-- Public Subnet (10.0.1.0/24) -- Internet Gateway -- Internet
  |     +-- EC2 instances (public IP), NAT Gateway
  +-- Private Subnet (10.0.2.0/24) -- NAT Gateway -- Internet (outbound only)
        +-- Databases, backend services
```

### Composants {#components}

| Composant | Rôle |
|-----------|------|
| VPC | Réseau virtuel isolé (bloc CIDR) |
| Subnet | Segment dans une AZ spécifique. Public = route vers IGW |
| Internet Gateway | Connectivité du VPC vers Internet |
| NAT Gateway | Sortie depuis le sous-réseau privé (pas d'entrée) |
| Route Table | Règles de routage du trafic |
| Security Group | Pare-feu avec état au niveau de l'instance (autorisation uniquement) |
| NACL | Pare-feu sans état au niveau du sous-réseau (autorisation + refus) |

### Security Groups vs NACLs {#security-groups-vs-nacls}

| Critère | Security Group | NACL |
|---------|---------------|------|
| Niveau | Instance | Sous-réseau |
| Avec état | Oui | Non |
| Règles | Autorisation uniquement | Autorisation + refus |
| Évaluation | Toutes les règles | Ordonnées par numéro |

## EC2 (Elastic Compute Cloud) {#ec2-elastic-compute-cloud}

### Types d'instances {#instance-types}

| Famille | Cas d'usage |
|--------|----------|
| t2/t3 | Usage général, en rafale |
| m5/m6i | Usage général, charge soutenue |
| c5/c6i | Optimisées pour le calcul |
| r5/r6i | Optimisées pour la mémoire |
| g4/p4 | Instances GPU |

### Connexion {#connecting}

```bash
chmod 400 my-key.pem
ssh -i my-key.pem ec2-user@<public-ip>    # Amazon Linux
ssh -i my-key.pem ubuntu@<public-ip>      # Ubuntu
```

### User Data (Bootstrap) {#user-data-bootstrap}

```bash
#!/bin/bash
yum update -y
yum install docker -y
systemctl start docker && systemctl enable docker
docker run -d -p 80:80 nginx
```

### Docker sur EC2 (Amazon Linux 2) {#docker-on-ec2-amazon-linux-2}

```bash
sudo yum update -y && sudo yum install docker -y
sudo systemctl start docker && sudo systemctl enable docker
sudo usermod -aG docker ec2-user
# Logout and login for group change
```

## S3 (Simple Storage Service) {#s3-simple-storage-service}

```bash
aws s3 mb s3://my-bucket
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./dir s3://my-bucket/dir
aws s3 ls s3://my-bucket/
```

### Classes de stockage {#storage-classes}

| Classe | Cas d'usage |
|-------|----------|
| Standard | Accès fréquent |
| Intelligent-Tiering | Schémas d'accès inconnus |
| Standard-IA | Accès peu fréquent |
| Glacier | Archivage (récupération en minutes à heures) |
| Glacier Deep Archive | Long terme (récupération en 12 h) |

## CloudWatch {#cloudwatch}

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

États : OK -> ALARM -> INSUFFICIENT_DATA.

## ECR et App Runner {#ecr-and-app-runner}

**ECR** : registre Docker privé. Flux de push : `aws ecr get-login-password | docker login`, tagger, pousser.

**App Runner** : déploiement de conteneurs géré. Mise à l'échelle automatique, HTTPS, équilibrage de charge. Pointe vers une image ECR. Pour les charges de travail HTTP uniquement.

## Route 53 + CloudFront {#route-53-cloudfront}

- **Route 53** : service DNS. Enregistrements Alias pour ALB/CloudFront/S3 (gratuits, contrairement aux CNAME)
- **CloudFront** : CDN. Cache en périphérie pour le contenu statique. Domaines personnalisés via un certificat ACM (doit être dans us-east-1)

## Pièges courants {#gotchas}

- Les instances EC2 arrêtées conservent leur EBS mais peuvent perdre leur IP publique (utiliser une Elastic IP pour une adresse statique)
- Les security groups sont avec état mais pas les NACLs : configurer les deux sens pour les NACLs
- Les noms de bucket S3 sont uniques à l'échelle mondiale
- Les rôles IAM sur EC2 sont préférables aux clés d'accès : pas de rotation d'identifiants nécessaire
- Un VPC par défaut existe dans chaque région, mais des VPC personnalisés sont recommandés en production

## Voir aussi {#see-also}

- [[kubernetes-on-eks]] - EKS sur AWS
- [[terraform-iac]] - provisionnement d'AWS avec Terraform
- [[container-registries]] - détails sur ECR
- [[monitoring-and-observability]] - CloudWatch et Prometheus
