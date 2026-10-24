---
title: "Infrastructure as Code pour les bases de données"
category: reference
tags: [sql-databases, terraform, ansible, iac, cloud, gcp, postgresql, deployment, automation]
level: 3
source_sha256: fcbf5883db8f7889a298529d3df28e79a56cd1c6c3dca4b133539e7f1e55738a
translation: machine
translated_at: '2026-10-24'
---
# Infrastructure as Code pour les bases de données {#infrastructure-as-code-for-databases}

Terraform provisionne l'infrastructure (VM, bases de données managées, réseaux), tandis qu'Ansible configure les logiciels (installation de PostgreSQL, mise en place de la réplication, gestion de la configuration). Ensemble, ils permettent des déploiements de bases de données reproductibles.

## Terraform - Provisionnement d'infrastructure {#terraform-infrastructure-provisioning}

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

## Ansible - Gestion de la configuration {#ansible-configuration-management}

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

Rôles Ansible pré-construits : `galaxyproject.postgresql`, `geerlingguy.postgresql`.

## PostgreSQL managé dans le cloud {#cloud-managed-postgresql}

| Fournisseur | Service | Versions | Fonctionnalités |
|----------|---------|----------|----------|
| GCP | Cloud SQL | 10-15 | Sauvegarde automatique, HA, réplicas en lecture |
| AWS | RDS / Aurora | 10-15 | Multi-AZ, bascule automatique |
| Yandex Cloud | PostgreSQL managé | 10-15 | PITR, pooler de connexions |
| VK Cloud | Cloud Database | 10-14 | Single/Master-Replica/Cluster |

Configurations VK Cloud : Single (dev/test), Master-Replica (production), Cluster (haute fiabilité). SSD max : 5120GB.

## Installation de PostgreSQL (Linux) {#postgresql-installation-linux}

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

## Points clés {#key-facts}

- Terraform gère le cycle de vie de l'infrastructure, Ansible configure les applications
- `DEBIAN_FRONTEND=noninteractive` évite les invites lors des installations automatisées
- Les services managés prennent en charge les sauvegardes, la HA et l'application des correctifs : à privilégier pour des opérations plus simples
- `pg_lsclusters` liste les clusters PostgreSQL installés sur Debian/Ubuntu
- Ansible est sans agent (il se connecte via SSH)

## Pièges courants {#gotchas}

- Une commande `destroy` de Terraform supprime toutes les ressources gérées, données comprises : protégez-les avec des règles de cycle de vie (`lifecycle`)
- Les services PostgreSQL managés ne prennent pas forcément en charge toutes les extensions
- L'redimensionnement du disque d'une VM cloud peut nécessiter un redémarrage de l'instance
- Idempotence des playbooks Ansible : les handlers ne s'exécutent que si la tâche signale « changed »
- Utilisez toujours `DEBIAN_FRONTEND=noninteractive` sur les versions non LTS d'Ubuntu

## Voir aussi {#see-also}

- [[postgresql-configuration-tuning|réglage de la configuration de PostgreSQL]] - réglages après installation
- [[postgresql-ha-patroni|déploiement de Patroni via Ansible]] - déploiement de Patroni via Ansible
- [[postgresql-docker-kubernetes|déploiements basés sur des conteneurs]] - déploiements basés sur des conteneurs
- [[backup-and-recovery|automatisation de la configuration des sauvegardes]] - automatisation de la configuration des sauvegardes
