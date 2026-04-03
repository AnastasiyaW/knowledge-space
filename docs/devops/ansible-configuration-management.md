---
title: Ansible Configuration Management
category: concepts
tags: [devops, ansible, configuration-management, automation, playbooks, iac]
---

# Ansible Configuration Management

Ansible is an agentless automation tool for orchestration, configuration management, provisioning, and deployment. It connects via SSH and describes desired state in YAML playbooks.

## Key Advantages

- **Agentless** - no software to install on targets, only SSH access needed
- **Declarative** - describe desired state, Ansible ensures it
- **Idempotent** - running multiple times produces same result
- **Simple YAML** - playbooks are human-readable, version-controllable
- **Large ecosystem** - Ansible Galaxy for community roles

## Architecture

Control node pushes "modules" to managed nodes via SSH. Modules execute, report results, and are removed.

```bash
ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory.ini playbook.yml -vvv
```

## Inventory

```ini
[webservers]
www1.example.com
www2.example.com

[dbservers]
db1.example.com
```

## Ad-Hoc Commands

```bash
ansible all -m ping -i inventory.ini
ansible www1.example.com -i inventory.ini -a "date"
```

## Playbooks

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

## Roles

Reusable automation units with standardized structure:

```bash
ansible-galaxy init myrole     # create skeleton
```

Structure: `defaults/`, `vars/`, `tasks/`, `files/`, `templates/`, `meta/`

Install from requirements:
```bash
ansible-galaxy install -r requirements.yml
```

## Debugging

Verbosity levels: `-v` to `-vvvv`. Higher = more detail.

## Idempotency

Modules check current state before changes. `shell`/`command` modules need guards (`creates`, `removes`, `when`) to be idempotent.

## Gotchas

- `shell`/`command` modules are not idempotent by default - use `creates`/`removes` parameters
- YAML indentation errors are the most common issue
- `become: yes` needed for privilege escalation (sudo)

## See Also

- [[terraform-iac]] - infrastructure provisioning (complementary)
- [[sre-automation-and-toil]] - automation philosophy
- [[cicd-pipelines]] - Ansible in CI/CD
