---
title: "Ansible-Konfigurationsmanagement"
category: concepts
tags: [devops, ansible, configuration-management, automation, playbooks, iac]
level: 3
source_sha256: 9646272d90b4d018e0c7c13b3b498035b289cc353f58b0ee449087d0248a54e8
translation: machine
translated_at: '2026-10-24'
---
# Ansible-Konfigurationsmanagement {#ansible-configuration-management}

Ansible ist ein agentenloses Automatisierungswerkzeug für Orchestrierung, Konfigurationsmanagement, Provisionierung und Deployment. Es verbindet sich über SSH und beschreibt den gewünschten Zustand in YAML-Playbooks.

## Wichtige Vorteile {#key-advantages}

- **Agentenlos** - keine Software auf den Zielsystemen zu installieren, nur SSH-Zugriff nötig
- **Deklarativ** - den gewünschten Zustand beschreiben, Ansible stellt ihn sicher
- **Idempotent** - mehrfaches Ausführen liefert dasselbe Ergebnis
- **Einfaches YAML** - Playbooks sind menschenlesbar und versionierbar
- **Großes Ökosystem** - Ansible Galaxy für Community-Rollen

## Architektur {#architecture}

Der Control Node überträgt „Module“ per SSH an die verwalteten Knoten. Module werden ausgeführt, melden ihre Ergebnisse zurück und werden anschließend wieder entfernt.

```bash
ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory.ini playbook.yml -vvv
```

## Inventory {#inventory}

```ini
[webservers]
www1.example.com
www2.example.com

[dbservers]
db1.example.com
```

## Ad-hoc-Befehle {#ad-hoc-commands}

```bash
ansible all -m ping -i inventory.ini
ansible www1.example.com -i inventory.ini -a "date"
```

## Playbooks {#playbooks}

```yaml
- hosts: webservers
  become: yes
  vars:
    http_port: 80
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

## Rollen {#roles}

Wiederverwendbare Automatisierungseinheiten mit standardisierter Struktur:

```bash
ansible-galaxy init myrole     # create skeleton
```

Struktur: `defaults/`, `vars/`, `tasks/`, `files/`, `templates/`, `meta/`

Installation aus Requirements:
```bash
ansible-galaxy install -r requirements.yml
```

## Debugging {#debugging}

Ausführlichkeitsstufen: `-v` bis `-vvvv`. Höher = mehr Details.

## Idempotenz {#idempotency}

Module prüfen den aktuellen Zustand, bevor sie Änderungen vornehmen. Die Module `shell`/`command` benötigen Absicherungen (`creates`, `removes`, `when`), um idempotent zu sein.

## Stolperfallen {#gotchas}

- Die Module `shell`/`command` sind standardmäßig nicht idempotent - Parameter `creates`/`removes` verwenden
- YAML-Einrückungsfehler sind das häufigste Problem
- `become: yes` ist für Rechteerweiterung (sudo) nötig

## Siehe auch {#see-also}

- [[terraform-iac]] - Infrastrukturbereitstellung (ergänzend)
- [[sre-automation-and-toil]] - Automatisierungsphilosophie
- [[cicd-pipelines]] - Ansible in CI/CD
