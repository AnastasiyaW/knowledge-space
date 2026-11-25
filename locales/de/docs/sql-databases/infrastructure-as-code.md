---
title: "Infrastruktur als Code für Datenbanken"
category: reference
tags: [sql-databases, terraform, ansible, iac, cloud, gcp, postgresql, deployment, automation]
level: 3
source_sha256: fcbf5883db8f7889a298529d3df28e79a56cd1c6c3dca4b133539e7f1e55738a
translation: machine
translated_at: '2026-10-24'
---
# Infrastruktur als Code für Datenbanken {#infrastructure-as-code-for-databases}

Terraform stellt Infrastruktur bereit (VMs, verwaltete Datenbanken, Netzwerke), während Ansible Software konfiguriert (PostgreSQL-Installation, Replikationseinrichtung, Konfigurationsmanagement). Zusammen ermöglichen sie reproduzierbare Datenbankbereitstellungen.

## Terraform - Bereitstellung der Infrastruktur {#terraform-infrastructure-provisioning}

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

## Ansible - Konfigurationsmanagement {#ansible-configuration-management}

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

Vorgefertigte Ansible-Rollen: `galaxyproject.postgresql`, `geerlingguy.postgresql`.

## Verwaltetes PostgreSQL in der Cloud {#cloud-managed-postgresql}

| Anbieter | Dienst | Versionen | Funktionen |
|----------|---------|----------|----------|
| GCP | Cloud SQL | 10-15 | Automatische Backups, HA, Read-Replicas |
| AWS | RDS / Aurora | 10-15 | Multi-AZ, automatisches Failover |
| Yandex Cloud | Managed PostgreSQL | 10-15 | PITR, Connection Pooler |
| VK Cloud | Cloud Database | 10-14 | Single/Master-Replica/Cluster |

VK-Cloud-Konfigurationen: Single (Entwicklung/Test), Master-Replica (Produktion), Cluster (hohe Ausfallsicherheit). Maximale SSD: 5120GB.

## PostgreSQL-Installation (Linux) {#postgresql-installation-linux}

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

## Wichtige Fakten {#key-facts}

- Terraform verwaltet den Lebenszyklus der Infrastruktur, Ansible konfiguriert die Anwendungen
- `DEBIAN_FRONTEND=noninteractive` verhindert Abfragen während automatisierter Installationen
- Verwaltete Dienste übernehmen Backups, HA und Patching – geeignet für einfachere Betriebsabläufe
- `pg_lsclusters` listet installierte PostgreSQL-Cluster unter Debian/Ubuntu auf
- Ansible ist agentenlos (verbindet sich über SSH)

## Fallstricke {#gotchas}

- Terraform `destroy` löscht alle verwalteten Ressourcen einschließlich der Daten – mit Lifecycle-Regeln absichern
- Verwaltete PostgreSQL-Dienste unterstützen unter Umständen nicht alle Erweiterungen
- Das Vergrößern der Festplatte einer Cloud-VM erfordert möglicherweise einen Neustart der Instanz
- Idempotenz von Ansible-Playbooks: Handler werden nur ausgeführt, wenn die Task „changed“ meldet
- Auf Nicht-LTS-Ubuntu-Versionen immer `DEBIAN_FRONTEND=noninteractive` verwenden

## Siehe auch {#see-also}

- [[postgresql-configuration-tuning]] - Tuning nach der Installation
- [[postgresql-ha-patroni]] - Patroni-Deployment über Ansible
- [[postgresql-docker-kubernetes]] - containerbasierte Deployments
- [[backup-and-recovery]] - Automatisierung der Backup-Konfiguration
