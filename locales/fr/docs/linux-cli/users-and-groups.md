---
title: "Utilisateurs et groupes"
category: reference
tags: [linux-cli, users, groups, sudo, su, passwd]
level: 3
source_sha256: b34886103428037ed20aa31117ff6884f4493d943056bb3a258f7857de901cd0
translation: machine
translated_at: '2026-10-24'
---
# Utilisateurs et groupes {#users-and-groups}

Linux est un système multi-utilisateurs. Les utilisateurs peuvent être des comptes humains, des comptes de services système ou le superutilisateur (root). Les groupes regroupent les utilisateurs pour des permissions partagées. Cette entrée couvre la gestion des utilisateurs, les fichiers d'authentification et l'élévation de privilèges.

## Types d'utilisateurs {#user-types}

| Type | Plage d'UID | Exemples |
|------|-------------|----------|
| Superutilisateur (root) | 0 | Accès complet au système |
| Utilisateurs système | 1-999 | daemon, sshd, www-data |
| Utilisateurs standards | 1000+ | Comptes humains |

## Fichiers clés {#key-files}

| Fichier | Rôle |
|---------|------|
| `/etc/passwd` | Comptes utilisateurs (lisible par tous) |
| `/etc/shadow` | Hachages des mots de passe (root uniquement) |
| `/etc/group` | Définitions des groupes |

### Format de /etc/passwd {#etcpasswd-format}

```text
username:x:UID:GID:GECOS:home_dir:shell
alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash
```

## Interroger les informations utilisateur {#querying-user-info}

```bash
whoami              # current username
id                  # UID, GID, all groups
id username         # info for specific user
groups              # groups of current user
groups username     # groups of specific user
who                 # who is logged in
w                   # logged in + what they're doing
last                # login history
lastlog             # all users' last login dates
```

## Créer des utilisateurs {#creating-users}

```bash
# useradd - low-level, minimal
sudo useradd username                     # no home, no password
sudo useradd -m username                  # with home directory
sudo useradd -m -s /bin/bash username     # with home + bash shell

# adduser - interactive wrapper (Debian/Ubuntu)
sudo adduser username                     # prompts for password, info

# Set password
sudo passwd username
```

## Modifier des utilisateurs {#modifying-users}

```bash
sudo usermod -s /bin/bash user       # change shell
sudo usermod -d /new/home user       # change home directory
sudo usermod -l newname oldname      # rename user
sudo usermod -aG group user          # add to supplementary group (-a = APPEND)
sudo usermod -G g1,g2 user           # set supplementary groups (REPLACES existing)
sudo usermod -L user                 # lock account
sudo usermod -U user                 # unlock account
```

## Supprimer des utilisateurs {#deleting-users}

```bash
sudo userdel username           # delete user (keep home)
sudo userdel -r username        # delete user AND home directory
```

## Gestion des groupes {#group-management}

```bash
sudo groupadd groupname         # create group
sudo groupdel groupname         # delete group
sudo groupmod -n new old        # rename group
```

## Changer d'utilisateur {#switching-users}

### su (Substitute User) {#su-substitute-user}

```bash
su username             # switch (keeps current environment)
su - username           # switch with full login environment
su -                    # switch to root (full login)
sudo su                 # switch to root via sudo
```

### sudo (Superuser Do) {#sudo-superuser-do}

```bash
sudo command            # run as root
sudo -u username cmd    # run as specific user
sudo -i                 # interactive root shell
sudo -b command         # background execution
```

**su vs sudo :**
- `su` requiert le **mot de passe de l'utilisateur cible** ; aucune journalisation
- `sudo` requiert **votre** mot de passe ; toutes les actions sont journalisées ; nécessite une configuration dans `/etc/sudoers`

### visudo {#visudo}

```bash
sudo visudo             # safely edit /etc/sudoers (validates syntax)
```

Accorder l'accès sudo :
```bash
sudo usermod -aG sudo username    # Debian/Ubuntu
sudo usermod -aG wheel username   # RHEL/CentOS/Fedora
```

## Modèles courants {#patterns}

### Créer un utilisateur avec configuration complète {#create-user-with-full-setup}

```bash
sudo useradd -m -s /bin/bash -G sudo newuser
sudo passwd newuser
```

### Lister tous les utilisateurs réels {#list-all-real-users}

```bash
awk -F: '$3 >= 1000 && $3 < 65534 {print $1}' /etc/passwd
```

## Pièges courants {#gotchas}

- `usermod -G` sans `-a` **remplace** tous les groupes secondaires : utilisez toujours `-aG` pour ajouter
- `useradd` ne crée PAS de répertoire personnel par défaut : utilisez l'option `-m`
- Les comptes verrouillés (`usermod -L`) ajoutent un préfixe `!` au hachage du mot de passe dans `/etc/shadow`
- Le compte root peut être désactivé sur certaines distributions (Ubuntu) : utilisez `sudo` à la place
- Supprimer un utilisateur ne termine pas ses processus en cours

## Voir aussi {#see-also}

- [[file-permissions]] - Modèle de permissions, chmod, ACLs
- [[ssh-remote-access]] - Authentification par clés
- [[linux-security]] - DAC, MAC, capacités
