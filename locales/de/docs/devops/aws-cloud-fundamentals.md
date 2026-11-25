---
title: "AWS Cloud-Grundlagen"
category: concepts
tags: [devops, aws, ec2, vpc, iam, s3, cloudwatch, networking]
level: 2
source_sha256: f73594b950b6d1a00c545c210d22a2535667a41afa4f5d6e5b312e372e99ad8d
translation: machine
translated_at: '2026-10-24'
---
# AWS Cloud-Grundlagen {#aws-cloud-fundamentals}

Zentrale AWS-Dienste für DevOps: IAM für die Zugriffskontrolle, VPC für das Networking, EC2 für Compute, S3 für Storage und CloudWatch für das Monitoring.

## IAM (Identity and Access Management) {#iam-identity-and-access-management}

### Kernkomponenten {#core-components}

- **Users** - einzelne Konten mit Zugangsdaten
- **Groups** - Sammlungen von Benutzern, die Berechtigungen teilen
- **Roles** - übernehmbare Identitäten für Dienste (keine dauerhaften Zugangsdaten)
- **Policies** - JSON-Dokumente, die Berechtigungen definieren

### Aufbau einer Policy {#policy-structure}

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

### Best Practices {#best-practices}

- Root-Konto: MFA aktivieren, nicht für den täglichen Betrieb verwenden
- Principle of Least Privilege
- Rollen für EC2/Lambda verwenden (keine eingebetteten Schlüssel)
- CloudTrail für das Audit aktivieren
- Zugriffsschlüssel regelmäßig rotieren

### CLI-Konfiguration {#cli-configuration}

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

### Komponenten {#components}

| Komponente | Zweck |
|-----------|---------|
| VPC | Isoliertes virtuelles Netzwerk (CIDR-Block) |
| Subnet | Segment in einer bestimmten AZ. Public = Route zum IGW |
| Internet Gateway | Konnektivität zwischen VPC und Internet |
| NAT Gateway | Ausgehender Verkehr aus dem Private Subnet (kein eingehender) |
| Route Table | Regeln für das Routing des Verkehrs |
| Security Group | Zustandsbehaltende Firewall auf Instanzebene (nur Allow) |
| NACL | Zustandslose Firewall auf Subnet-Ebene (Allow + Deny) |

### Security Groups vs. NACLs {#security-groups-vs-nacls}

| Merkmal | Security Group | NACL |
|---------|---------------|------|
| Ebene | Instanz | Subnet |
| Zustandsbehaftet | Ja | Nein |
| Regeln | Nur Allow | Allow + Deny |
| Auswertung | Alle Regeln | Nach Nummer geordnet |

## EC2 (Elastic Compute Cloud) {#ec2-elastic-compute-cloud}

### Instanztypen {#instance-types}

| Familie | Anwendungsfall |
|--------|----------|
| t2/t3 | Allgemeiner Zweck, Burstable |
| m5/m6i | Allgemeiner Zweck, dauerhafte Last |
| c5/c6i | Compute-optimiert |
| r5/r6i | Speicheroptimiert |
| g4/p4 | GPU-Instanzen |

### Verbindungsaufbau {#connecting}

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

### Docker auf EC2 (Amazon Linux 2) {#docker-on-ec2-amazon-linux-2}

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

### Speicherklassen {#storage-classes}

| Klasse | Anwendungsfall |
|-------|----------|
| Standard | Häufiger Zugriff |
| Intelligent-Tiering | Unbekannte Zugriffsmuster |
| Standard-IA | Seltener Zugriff |
| Glacier | Archiv (Abruf in Minuten bis Stunden) |
| Glacier Deep Archive | Langzeitspeicherung (Abruf in 12 Stunden) |

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

Zustände: OK -> ALARM -> INSUFFICIENT_DATA.

## ECR und App Runner {#ecr-and-app-runner}

**ECR**: Privates Docker-Registry. Push-Ablauf: `aws ecr get-login-password | docker login`, taggen, pushen.

**App Runner**: Verwaltete Container-Bereitstellung. Auto-Scaling, HTTPS, Load Balancing. Verweist auf ein ECR-Image. Nur für HTTP-Workloads.

## Route 53 + CloudFront {#route-53-cloudfront}

- **Route 53**: DNS-Dienst. Alias-Records für ALB/CloudFront/S3 (kostenlos, anders als CNAME)
- **CloudFront**: CDN. Edge-Caching für statische Inhalte. Eigene Domains über ein ACM-Zertifikat (muss in us-east-1 liegen)

## Gotchas {#gotchas}

- Gestoppte EC2-Instanzen behalten ihr EBS, können aber die öffentliche IP verlieren (für eine statische Adresse Elastic IP verwenden)
- Security Groups sind zustandsbehaftet, NACLs nicht - bei NACLs beide Richtungen konfigurieren
- S3-Bucket-Namen sind global eindeutig
- IAM-Rollen auf EC2 sind Zugriffsschlüsseln vorzuziehen - keine Rotation von Zugangsdaten nötig
- Pro Region existiert eine Default-VPC, für Produktion werden jedoch eigene VPCs empfohlen

## Siehe auch {#see-also}

- [[kubernetes-on-eks]] - EKS auf AWS
- [[terraform-iac]] - Provisionierung von AWS mit Terraform
- [[container-registries]] - Details zu ECR
- [[monitoring-and-observability]] - CloudWatch und Prometheus
