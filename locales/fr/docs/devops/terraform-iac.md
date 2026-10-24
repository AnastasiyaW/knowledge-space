---
title: "Infrastructure as Code avec Terraform"
category: concepts
tags: [devops, terraform, iac, hcl, state, modules, providers]
level: 3
source_sha256: 9f3211556769b7f7c54e6d83eb827e0d63e9d36ce1c4dc7eb8fad6dec18beca8
translation: machine
translated_at: '2026-10-24'
---
# Infrastructure as Code avec Terraform {#terraform-infrastructure-as-code}

Terraform est un outil IaC déclaratif qui utilise HCL (HashiCorp Configuration Language). Il gère l'infrastructure sur AWS, Azure, GCP, Kubernetes et des centaines d'autres providers grâce à un workflow en deux temps : plan, puis apply.

## Flux de travail principal {#core-workflow}

```bash
terraform init          # download providers, initialize backend
terraform validate      # syntax check
terraform fmt           # auto-format files
terraform plan          # preview changes (CRUD without R)
terraform apply         # execute changes
terraform destroy       # teardown all resources
```

## Syntaxe HCL {#hcl-syntax}

### Ressources {#resources}

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  tags = merge(local.common_tags, { Name = "web-server" })
}
```

### Variables {#variables}

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

### Priorité des entrées de variables (de la plus haute à la plus basse) {#variable-input-priority-highest-to-lowest}

1. `-var "name=value"` (CLI)
2. `-var-file="dev.tfvars"` (fichier explicite)
3. `terraform.tfvars` ou `*.auto.tfvars` (chargés automatiquement)
4. `TF_VAR_name` (variable d'environnement)
5. Valeur `default`
6. Invite interactive

### Sorties {#outputs}

```hcl
output "public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of web server"
}
```

### Sources de données {#data-sources}

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

### Conditions et boucles {#conditionals-and-loops}

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

## Structure des fichiers {#file-structure}

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

## Gestion de l'état {#state-management}

### État distant (production) {#remote-state-production}

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

### Commandes d'état {#state-commands}

```bash
terraform state list
terraform state show aws_instance.web
terraform state rm aws_instance.web       # remove from state only
terraform state mv old_name new_name
terraform import aws_instance.web i-12345 # import existing
terraform refresh                         # sync state with reality
```

**Ne jamais commiter de `.tfstate` dans Git** - il contient des données sensibles.

## Modules {#modules}

### Création {#creating}

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

### Utilisation {#using}

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

### Sources des modules {#module-sources}

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

## Terraform dans les pipelines CI/CD {#terraform-in-cicd-pipelines}

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

## Bonnes pratiques {#best-practices}

1. **État distant** avec verrouillage pour le travail en équipe
2. **Un état séparé par environnement** (dev/qa/prod)
3. **Épingler les versions des providers** : `version = "~> 5.0"`
4. **Utiliser des modules** pour les patterns réutilisables
5. **Ne jamais coder de secrets en dur** - utiliser des variables ou un coffre-fort (vault)
6. **Plan avant apply** - toujours relire le plan
7. **Taguer toutes les ressources** pour le suivi des coûts
8. **.gitignore** : `terraform.tfstate`, `*.tfstate.*`, `.terraform/`, ainsi que les `*.tfvars` sensibles

## Pièges courants {#gotchas}

- L'état est la source de vérité pour Terraform - perdre l'état signifie que Terraform ignore votre infrastructure
- `terraform destroy` sans cible supprime TOUT ce qui est géré par cet état
- `terraform import` n'importe que dans l'état - vous devez toujours écrire le HCL correspondant
- Terraform est verbeux - Terragrunt aide à appliquer le principe DRY
- Changer la version d'un provider peut introduire des ruptures de compatibilité - épinglez toujours les versions

## Voir aussi {#see-also}

- [[aws-cloud-fundamentals]] - ressources AWS gérées par Terraform
- [[kubernetes-on-aks]] - provisionnement d'AKS avec Terraform
- [[cicd-pipelines]] - Terraform dans les pipelines
- [[gitops-and-argocd]] - workflow Terraform natif GitOps
- [[ansible-configuration-management]] - outil complémentaire pour la configuration
