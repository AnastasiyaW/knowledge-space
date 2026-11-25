---
title: "Terraform Infrastructure as Code"
category: concepts
tags: [devops, terraform, iac, hcl, state, modules, providers]
level: 3
source_sha256: 9f3211556769b7f7c54e6d83eb827e0d63e9d36ce1c4dc7eb8fad6dec18beca8
translation: machine
translated_at: '2026-10-24'
---
# Terraform Infrastructure as Code {#terraform-infrastructure-as-code}

Terraform ist ein deklaratives IaC-Werkzeug, das HCL (HashiCorp Configuration Language) verwendet. Es verwaltet Infrastruktur über AWS, Azure, GCP, Kubernetes und hunderte weitere Provider hinweg und folgt dabei einem Workflow, bei dem vor dem Apply immer geplant wird.

## Kern-Workflow {#core-workflow}

```bash
terraform init          # download providers, initialize backend
terraform validate      # syntax check
terraform fmt           # auto-format files
terraform plan          # preview changes (CRUD without R)
terraform apply         # execute changes
terraform destroy       # teardown all resources
```

## HCL-Syntax {#hcl-syntax}

### Ressourcen {#resources}

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  tags = merge(local.common_tags, { Name = "web-server" })
}
```

### Variablen {#variables}

```hcl
variable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "EC2 instance type"
}

variable "tags"    { type = map(string) }
variable "cidrs"   { type = list(string) }
variable "config"  { type = object({ name = string, port = number }) }
```

### Priorität der Variableneingabe (von hoch nach niedrig) {#variable-input-priority-highest-to-lowest}

1. `-var "name=value"` (CLI)
2. `-var-file="dev.tfvars"` (explizite Datei)
3. `terraform.tfvars` oder `*.auto.tfvars` (automatisch geladen)
4. `TF_VAR_name` (Umgebungsvariable)
5. `default`-Wert
6. Interaktive Abfrage

### Outputs {#outputs}

```hcl
output "public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of web server"
}
```

### Data Sources {#data-sources}

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*"]
  }
}
```

### Locals {#locals}

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = "myproject"
    ManagedBy   = "terraform"
  }
}
```

### Bedingungen und Schleifen {#conditionals-and-loops}

```hcl
# Conditional
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"

# Count
resource "aws_instance" "server" {
  count         = 3
  tags = { Name = "server-${count.index}" }
}

# For Each
resource "aws_instance" "server" {
  for_each = toset(["web", "api", "worker"])
  tags = { Name = "server-${each.key}" }
}
```

## Dateistruktur {#file-structure}

```bash
project/
  main.tf              # resource definitions
  variables.tf         # input variable declarations
  outputs.tf           # output values
  providers.tf         # provider + terraform block
  terraform.tfvars     # default values (auto-loaded)
  dev.tfvars           # environment-specific
  modules/
    vpc/
      main.tf
      variables.tf
      outputs.tf
```

## State-Verwaltung {#state-management}

### Remote-State (Produktion) {#remote-state-production}

```hcl
# AWS S3 backend
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"   # state locking
    encrypt        = true
  }
}

# Azure Storage backend
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

### State-Befehle {#state-commands}

```bash
terraform state list
terraform state show aws_instance.web
terraform state rm aws_instance.web       # remove from state only
terraform state mv old_name new_name
terraform import aws_instance.web i-12345 # import existing
terraform refresh                         # sync state with reality
```

**Niemals `.tfstate` in Git committen** - enthält sensible Daten.

## Module {#modules}

### Erstellen {#creating}

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
}
resource "aws_subnet" "public" {
  count  = length(var.public_subnets)
  vpc_id = aws_vpc.main.id
  cidr_block = var.public_subnets[count.index]
}

# modules/vpc/outputs.tf
output "vpc_id"     { value = aws_vpc.main.id }
output "subnet_ids" { value = aws_subnet.public[*].id }
```

### Verwenden {#using}

```hcl
module "vpc" {
  source         = "./modules/vpc"
  vpc_cidr       = "10.0.0.0/16"
  public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
}

resource "aws_instance" "web" {
  subnet_id = module.vpc.subnet_ids[0]
}
```

### Modulquellen {#module-sources}

```hcl
source = "./modules/vpc"                            # local
source = "git::https://github.com/org/module.git"   # Git
source = "hashicorp/consul/aws"                     # Registry
```

## Workspaces {#workspaces}

```bash
terraform workspace new dev
terraform workspace select prod
terraform workspace list
```

```hcl
instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"
```

## Terraform in CI/CD-Pipelines {#terraform-in-cicd-pipelines}

```yaml
# Azure DevOps example
- task: TerraformTaskV4@4
  displayName: Terraform Init
  inputs:
    provider: 'azurerm'
    command: 'init'
    backendServiceArm: 'azure-service-connection'

- task: TerraformTaskV4@4
  displayName: Terraform Plan
  inputs:
    command: 'plan'
    commandOptions: '-var-file="dev.tfvars" -out=dev.plan'

- task: TerraformTaskV4@4
  displayName: Terraform Apply
  inputs:
    command: 'apply'
    commandOptions: 'dev.plan'
```

## Best Practices {#best-practices}

1. **Remote-State** mit Locking für Teamarbeit
2. **Eigener State pro Umgebung** (dev/qa/prod)
3. **Provider-Versionen fixieren**: `version = "~> 5.0"`
4. **Module verwenden** für wiederverwendbare Muster
5. **Geheimnisse niemals hardcodieren** - Variablen oder Vault verwenden
6. **Vor dem Apply planen** - Ergebnis immer prüfen
7. **Alles taggen** für die Kostenverfolgung
8. **.gitignore**: `terraform.tfstate`, `*.tfstate.*`, `.terraform/`, sensible `*.tfvars`

## Fallstricke {#gotchas}

- Der State ist die Quelle der Wahrheit für Terraform - geht der State verloren, weiß Terraform nichts mehr über die Infrastruktur
- `terraform destroy` ohne Target löscht ALLES, was von diesem State verwaltet wird
- `terraform import` importiert nur in den State - der HCL-Code muss trotzdem geschrieben werden
- Terraform ist ausführlich - Terragrunt hilft mit DRY
- Eine Änderung der Provider-Version kann Breaking Changes verursachen - Versionen immer fixieren

## Siehe auch {#see-also}

- [[aws-cloud-fundamentals]] - AWS-Ressourcen, die mit Terraform verwaltet werden
- [[kubernetes-on-aks]] - AKS-Bereitstellung mit Terraform
- [[cicd-pipelines]] - Terraform in Pipelines
- [[gitops-and-argocd]] - GitOps-nativer Terraform-Workflow
- [[ansible-configuration-management]] - ergänzendes Werkzeug für die Konfiguration
