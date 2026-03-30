---
title: Ansible Configuration Management
category: iac
tags: [ansible, playbooks, roles, inventory, configuration-management, automation]
---
# Ansible Configuration Management

Agentless configuration management and orchestration using SSH and YAML playbooks.

## Key Facts

- **Agentless** = Ansible connects via SSH (Linux) or WinRM (Windows); no agent installation on targets
- **Inventory** = list of managed hosts; static file or dynamic (AWS, Azure, GCP discovery)
- **Playbook** = YAML file with ordered list of plays; each play targets host group and runs tasks
- **Task** = single unit of work using a **module** (e.g., `apt`, `copy`, `service`, `template`)
- **Role** = reusable collection of tasks, handlers, templates, variables; standard directory structure
- **Idempotent** = running same playbook twice produces same result; modules handle "already done" state
- **Handlers** = tasks triggered by `notify`; run once at end of play (e.g., restart service after config change)
- **Jinja2** templates used for dynamic configuration files; variables from inventory, vars files, or facts
- **Facts** = system information gathered automatically (`ansible_os_family`, `ansible_hostname`, etc.)
- **Ansible Galaxy** = community repository for roles and collections
- [[terraform-iac]] creates infrastructure; Ansible configures it (complementary tools)
- [[ci-cd-pipelines]] can trigger Ansible playbooks as deployment step

## Patterns

```ini
# inventory.ini
[webservers]
web1.example.com ansible_user=ubuntu
web2.example.com ansible_user=ubuntu

[dbservers]
db1.example.com ansible_user=admin

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

```yaml
# playbook.yml
---
- name: Configure web servers
  hosts: webservers
  become: true
  vars:
    app_port: 8080
    nginx_worker_processes: auto

  tasks:
    - name: Update apt cache
      apt:
        update_cache: true
        cache_valid_time: 3600

    - name: Install packages
      apt:
        name:
          - nginx
          - python3-pip
          - supervisor
        state: present

    - name: Deploy nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/default
        owner: root
        group: root
        mode: '0644'
      notify: Restart nginx

    - name: Copy application files
      copy:
        src: app/
        dest: /opt/myapp/
        owner: www-data
      notify: Restart app

    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted

    - name: Restart app
      supervisorctl:
        name: myapp
        state: restarted
```

```
# Role directory structure
roles/
  webserver/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
      nginx.conf.j2
    files/
      app.conf
    vars/
      main.yml
    defaults/          # lowest priority variables
      main.yml
    meta/
      main.yml         # role dependencies
```

```bash
# Run playbook
ansible-playbook -i inventory.ini playbook.yml
ansible-playbook playbook.yml --limit webservers
ansible-playbook playbook.yml --check              # dry run
ansible-playbook playbook.yml --diff               # show file changes
ansible-playbook playbook.yml -e "app_port=9090"   # extra vars (highest priority)

# Ad-hoc commands
ansible all -i inventory.ini -m ping
ansible webservers -m shell -a "uptime"
ansible webservers -m apt -a "name=nginx state=present" --become

# Galaxy
ansible-galaxy init my_role                        # create role scaffold
ansible-galaxy install geerlingguy.docker          # install role
ansible-galaxy collection install community.general
```

## Gotchas

- Variable precedence (low to high): defaults -> inventory -> playbook vars -> extra vars (`-e`); 22 levels total
- `become: true` = run as root via sudo; must be set at play or task level
- Handlers only run ONCE even if notified multiple times; they run at END of play, not immediately
- `ansible-playbook --check` (dry run) may fail on tasks that depend on previous task results
- `copy` module copies from control node; `fetch` copies FROM remote; mixing them up is common
- Large file transfers over SSH are slow; use `synchronize` module (rsync wrapper) for large dirs
- Python must be installed on managed hosts; `raw` module works without Python for bootstrap
- YAML gotcha: `yes`/`no`/`true`/`false` are booleans; quote strings that look like booleans: `"yes"`

## See Also

- [[terraform-iac]] - infrastructure provisioning (Ansible configures what Terraform creates)
- [[ci-cd-pipelines]] - Ansible in deployment pipelines
- [[monitoring-observability]] - Ansible can deploy monitoring agents
- [[sre-sli-slo-sla]] - Ansible for automation reducing toil
- Ansible docs: https://docs.ansible.com/ansible/latest/
- Ansible Galaxy: https://galaxy.ansible.com/
