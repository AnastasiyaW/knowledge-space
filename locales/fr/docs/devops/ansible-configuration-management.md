---
title: "Gestion de configuration avec Ansible"
category: concepts
tags: [devops, ansible, configuration-management, automation, playbooks, iac]
level: 3
source_sha256: 9646272d90b4d018e0c7c13b3b498035b289cc353f58b0ee449087d0248a54e8
translation: machine
translated_at: '2026-10-24'
---
# Gestion de configuration avec Ansible {#ansible-configuration-management}

Ansible est un outil d'automatisation sans agent pour l'orchestration, la gestion de configuration, le provisionnement et le déploiement. Il se connecte via SSH et décrit l'état souhaité dans des playbooks YAML.

## Avantages clés {#key-advantages}

- **Sans agent** - aucun logiciel à installer sur les cibles, seul un accès SSH est nécessaire
- **Déclaratif** - décrire l'état souhaité, Ansible veille à sa mise en œuvre
- **Idempotent** - une exécution répétée produit le même résultat
- **YAML simple** - les playbooks sont lisibles par un humain et versionnables
- **Vaste écosystème** - Ansible Galaxy pour les rôles communautaires

## Architecture {#architecture}

Le nœud de contrôle envoie des « modules » aux nœuds gérés via SSH. Les modules s'exécutent, renvoient leurs résultats, puis sont supprimés.

```bash
ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory.ini playbook.yml -vvv
```

## Inventaire {#inventory}

```ini
[webservers]
www1.example.com
www2.example.com

[dbservers]
db1.example.com
```

## Commandes ad hoc {#ad-hoc-commands}

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

## Rôles {#roles}

Unités d'automatisation réutilisables à structure standardisée :

```bash
ansible-galaxy init myrole     # create skeleton
```

Structure : `defaults/`, `vars/`, `tasks/`, `files/`, `templates/`, `meta/`

Installation à partir des dépendances :
```bash
ansible-galaxy install -r requirements.yml
```

## Débogage {#debugging}

Niveaux de verbosité : `-v` à `-vvvv`. Plus le nombre est élevé, plus le détail est important.

## Idempotence {#idempotency}

Les modules vérifient l'état courant avant toute modification. Les modules `shell`/`command` nécessitent des garde-fous (`creates`, `removes`, `when`) pour être idempotents.

## Pièges courants {#gotchas}

- Les modules `shell`/`command` ne sont pas idempotents par défaut - utiliser les paramètres `creates`/`removes`
- Les erreurs d'indentation YAML sont le problème le plus fréquent
- `become: yes` est nécessaire pour l'élévation de privilèges (sudo)

## Voir aussi {#see-also}

- [[terraform-iac]] - provisionnement d'infrastructure (complémentaire)
- [[sre-automation-and-toil]] - philosophie de l'automatisation
- [[cicd-pipelines]] - Ansible dans la CI/CD
