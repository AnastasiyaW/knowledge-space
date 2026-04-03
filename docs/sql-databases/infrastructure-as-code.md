---
title: Infrastructure as Code for Databases
category: reference
tags: [sql-databases, terraform, ansible, iac, cloud, gcp, postgresql, deployment, automation]
---

# Infrastructure as Code for Databases

Terraform provisions infrastructure (VMs, managed databases, networks), while Ansible configures software (PostgreSQL installation, replication setup, configuration management). Together they enable reproducible database deployments.

## Terraform - Infrastructure Provisioning

```hcl
# GCP PostgreSQL VM
resource "google_compute_instance" "postgres" {
  name         = "postgres-server"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 50
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}

# Yandex Cloud Managed PostgreSQL
resource "yandex_mdb_postgresql_cluster" "pg" {
  name        = "pg-cluster"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.net.id

  config {
    version = 15
    resources {
      resource_preset_id = "s2.micro"
      disk_type_id       = "network-ssd"
      disk_size          = 20
    }
  }
}
```

```bash
terraform init      # initialize providers
terraform plan      # preview changes
terraform apply     # create infrastructure
terraform destroy   # tear down
```

## Ansible - Configuration Management

```yaml
# inventory.yml
all:
  hosts:
    pg-primary:
      ansible_host: 10.0.0.1
    pg-replica:
      ansible_host: 10.0.0.2

# playbook.yml
- hosts: all
  become: yes
  tasks:
    - name: Install PostgreSQL
      apt:
        name: postgresql-15
        state: present
        update_cache: yes

    - name: Configure PostgreSQL
      template:
        src: postgresql.conf.j2
        dest: /etc/postgresql/15/main/postgresql.conf
      notify: restart postgresql

    - name: Configure pg_hba.conf
      template:
        src: pg_hba.conf.j2
        dest: /etc/postgresql/15/main/pg_hba.conf
      notify: reload postgresql

  handlers:
    - name: restart postgresql
      service: { name: postgresql, state: restarted }
    - name: reload postgresql
      service: { name: postgresql, state: reloaded }
```

Pre-built Ansible roles: `galaxyproject.postgresql`, `geerlingguy.postgresql`.

## Cloud Managed PostgreSQL

| Provider | Service | Versions | Features |
|----------|---------|----------|----------|
| GCP | Cloud SQL | 10-15 | Auto-backup, HA, read replicas |
| AWS | RDS / Aurora | 10-15 | Multi-AZ, auto-failover |
| Yandex Cloud | Managed PostgreSQL | 10-15 | PITR, connection pooler |
| VK Cloud | Cloud Database | 10-14 | Single/Master-Replica/Cluster |

VK Cloud configurations: Single (dev/test), Master-Replica (production), Cluster (high reliability). Max SSD: 5120GB.

## PostgreSQL Installation (Linux)

```bash
# Ubuntu/Debian (PGDG repo)
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
  > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt -y install postgresql-15

# AlmaLinux/CentOS/RHEL
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo yum install -y postgresql15-server postgresql15
sudo /usr/pgsql-15/bin/postgresql-15-setup initdb
sudo systemctl enable --now postgresql-15
```

## Key Facts

- Terraform manages infrastructure lifecycle, Ansible configures applications
- `DEBIAN_FRONTEND=noninteractive` avoids prompts during automated installs
- Managed services handle backups, HA, and patching - use for simpler ops
- `pg_lsclusters` lists installed PostgreSQL clusters on Debian/Ubuntu
- Ansible is agentless (connects via SSH)

## Gotchas

- Terraform `destroy` deletes all managed resources including data - protect with lifecycle rules
- Managed PostgreSQL services may not support all extensions
- Cloud VM disk resize may require instance restart
- Ansible playbook idempotency: handlers only run if task reports "changed"
- Always use `DEBIAN_FRONTEND=noninteractive` on non-LTS Ubuntu releases

## See Also

- [[postgresql-configuration-tuning]] - post-installation tuning
- [[postgresql-ha-patroni]] - Patroni deployment via Ansible
- [[postgresql-docker-kubernetes]] - container-based deployments
- [[backup-and-recovery]] - backup configuration automation
