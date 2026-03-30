---
title: Terraform & Infrastructure as Code
category: iac
tags: [terraform, iac, hcl, providers, state, modules, plan, apply]
---
# Terraform & Infrastructure as Code

HashiCorp Terraform: declarative infrastructure provisioning across cloud providers using HCL.

## Key Facts

- **IaC** = managing infrastructure through code files instead of manual processes
- Terraform uses **HCL** (HashiCorp Configuration Language) - declarative, not imperative
- Core workflow: `terraform init` -> `terraform plan` -> `terraform apply` -> `terraform destroy`
- **State file** (`terraform.tfstate`) tracks real-world resource mapping; MUST be stored remotely for teams
- **Providers** = plugins for each platform (AWS, Azure, GCP, K8s, Docker, etc.)
- **Resources** = infrastructure objects (EC2 instance, S3 bucket, DNS record)
- **Data sources** = read-only queries to existing infrastructure
- **Modules** = reusable groups of resources; local or from Terraform Registry
- **Variables** = inputs (`variable` block); **Outputs** = exported values (`output` block)
- Plan shows diff before applying; `+` = create, `-` = destroy, `~` = modify
- [[aws-core-services]] and [[azure-aks]] are common Terraform targets
- [[ci-cd-pipelines]] automate Terraform plan/apply in CI
- State locking prevents concurrent modifications (S3 + DynamoDB for AWS backend)

## Patterns

```hcl
# providers.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}

# variables.tf
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# main.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_instance" "web" {
  count         = 3
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public[count.index].id
  tags = {
    Name = "${var.environment}-web-${count.index}"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"]
  }
}

# outputs.tf
output "instance_ips" {
  value = aws_instance.web[*].public_ip
}
```

```bash
# Workflow
terraform init                         # download providers, init backend
terraform plan                         # preview changes
terraform plan -out=tfplan             # save plan to file
terraform apply tfplan                 # apply saved plan
terraform apply -auto-approve          # skip confirmation (CI only)
terraform destroy                      # remove all resources

# State management
terraform state list                   # list resources in state
terraform state show aws_instance.web  # show resource details
terraform state mv                     # rename resource in state
terraform import aws_instance.web i-123  # import existing resource

# Workspace management (environment isolation)
terraform workspace new staging
terraform workspace select prod
terraform workspace list

# Module usage
terraform init -upgrade                # update module versions
terraform get                          # download modules
```

## Gotchas

- **Never edit state file manually**; use `terraform state` commands or `terraform import`
- State file contains secrets in plaintext; encrypt at rest (S3 encryption, Terraform Cloud)
- `terraform destroy` is irreversible; always run `plan -destroy` first to review
- Changing a resource attribute that forces replacement (e.g., AMI) will destroy + recreate - check plan carefully
- `count` vs `for_each`: count uses index (removing middle item shifts all); `for_each` uses keys (stable references)
- Provider version constraints: `~> 5.0` allows 5.x but not 6.0; pin in production
- `terraform apply` without saved plan re-plans (state may have changed between plan and apply)
- Circular dependencies cause errors; use `depends_on` for implicit dependencies Terraform cannot detect

## See Also

- [[aws-core-services]] - AWS resources managed by Terraform
- [[azure-aks]] - Azure Kubernetes via Terraform
- [[ansible-configuration]] - configuration management (complements Terraform)
- [[ci-cd-pipelines]] - automated Terraform pipelines
- Terraform docs: https://developer.hashicorp.com/terraform/docs
- Terraform Registry: https://registry.terraform.io/
