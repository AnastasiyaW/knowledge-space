---
title: Terraform Infrastructure as Code
category: concepts
tags: [devops, terraform, iac, hcl, state, modules, providers]
---

# Terraform Infrastructure as Code

Terraform is a declarative IaC tool using HCL (HashiCorp Configuration Language). It manages infrastructure across AWS, Azure, GCP, Kubernetes, and hundreds of other providers through a plan-before-apply workflow.

## Core Workflow

```bash
terraform init          # download providers, initialize backend
terraform validate      # syntax check
terraform fmt           # auto-format files
terraform plan          # preview changes (CRUD without R)
terraform apply         # execute changes
terraform destroy       # teardown all resources
```

## HCL Syntax

### Resources

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  tags = merge(local.common_tags, { Name = "web-server" })
}
```

### Variables

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

### Variable Input Priority (highest to lowest)

1. `-var "name=value"` (CLI)
2. `-var-file="dev.tfvars"` (explicit file)
3. `terraform.tfvars` or `*.auto.tfvars` (auto-loaded)
4. `TF_VAR_name` (environment variable)
5. `default` value
6. Interactive prompt

### Outputs

```hcl
output "public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of web server"
}
```

### Data Sources

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

### Locals

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = "myproject"
    ManagedBy   = "terraform"
  }
}
```

### Conditionals and Loops

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

## File Structure

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

## State Management

### Remote State (production)

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

### State Commands

```bash
terraform state list
terraform state show aws_instance.web
terraform state rm aws_instance.web       # remove from state only
terraform state mv old_name new_name
terraform import aws_instance.web i-12345 # import existing
terraform refresh                         # sync state with reality
```

**Never commit `.tfstate` to Git** - contains sensitive data.

## Modules

### Creating

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

### Using

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

### Module Sources

```hcl
source = "./modules/vpc"                            # local
source = "git::https://github.com/org/module.git"   # Git
source = "hashicorp/consul/aws"                     # Registry
```

## Workspaces

```bash
terraform workspace new dev
terraform workspace select prod
terraform workspace list
```

```hcl
instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"
```

## Terraform in CI/CD Pipelines

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

## Best Practices

1. **Remote state** with locking for team work
2. **Separate state per environment** (dev/qa/prod)
3. **Pin provider versions**: `version = "~> 5.0"`
4. **Use modules** for reusable patterns
5. **Never hardcode secrets** - use variables or vault
6. **Plan before apply** - always review
7. **Tag everything** for cost tracking
8. **.gitignore**: `terraform.tfstate`, `*.tfstate.*`, `.terraform/`, sensitive `*.tfvars`

## Gotchas

- State is the source of truth for Terraform - losing state means Terraform doesn't know about your infrastructure
- `terraform destroy` with no target deletes EVERYTHING managed by that state
- `terraform import` only imports to state - you still need to write the HCL
- Terraform is verbose - Terragrunt helps with DRY
- Changing provider version can cause breaking changes - always pin versions

## See Also

- [[aws-cloud-fundamentals]] - AWS resources managed by Terraform
- [[kubernetes-on-aks]] - AKS provisioning with Terraform
- [[cicd-pipelines]] - Terraform in pipelines
- [[gitops-and-argocd]] - GitOps-native Terraform workflow
- [[ansible-configuration-management]] - complementary tool for configuration
