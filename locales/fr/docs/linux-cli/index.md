---
title: "Linux et ligne de commande"
type: MOC
level: 2
source_sha256: 3d5a842201bfd9af2bfc98ce5564604760e7e5ba036d0368aa255e82cb8e2815
translation: machine
translated_at: '2026-10-24'
---
# Linux et ligne de commande {#linux-command-line}

## Shell et terminal {#shell-terminal}
- [[terminal-basics]] - Shells, commandes essentielles, raccourcis clavier, installation de Linux
- [[text-editors]] - nano et vim : modes, raccourcis, navigation

## Fichiers et système de fichiers {#files-filesystem}
- [[filesystem-hierarchy]] - Arborescence FHS, types de fichiers, utilisation du disque
- [[file-operations]] - Créer, copier, déplacer, supprimer, afficher fichiers et répertoires
- [[file-search-and-grep]] - find, grep, locate, whereis, which
- [[text-processing]] - wc, sort, uniq, cut, awk, sed, tr
- [[io-redirection-and-pipes]] - stdin/stdout/stderr, tubes, enchaînement de commandes, codes de sortie
- [[links-and-inodes]] - Liens durs, liens symboliques, structure des inodes, fonctionnement interne d'ext4
- [[file-permissions]] - chmod, chown, SUID/SGID/sticky, umask, ACL

## Utilisateurs et sécurité {#users-security}
- [[users-and-groups]] - Types d'utilisateurs, passwd/shadow/group, useradd, sudo, su
- [[linux-security]] - DAC/MAC, espaces de noms, seccomp, types de malwares, outils de pentest
- [[firewall-and-iptables]] - Chaînes/cibles/règles iptables, nftables, ufw

## Conteneurs {#containers}
- [[docker-basics]] - Images, conteneurs, volumes, Dockerfile, cycle de vie, nettoyage

## Administration système {#system-administration}
- [[systemd-and-services]] - systemctl, fichiers d'unités, modules du noyau, inspection matérielle
- [[process-management]] - ps, top, htop, kill, signaux, états des processus, priorité
- [[package-management]] - apt, dpkg, snap, yum/dnf, rpm, winget
- [[cron-and-scheduling]] - Syntaxe crontab, at, heure système, NTP
- [[disks-and-filesystems]] - Partitions, ext4, montage, fstab, LVM, chiffrement LUKS
- [[logging-and-journald]] - syslog, rsyslog, journalctl, logrotate, auditd
- [[monitoring-and-performance]] - Mémoire, E/S disque, réseau, charge moyenne, cgroups

## Réseau et accès distant {#networking-remote}
- [[ssh-remote-access]] - Clés SSH, configuration, tunnels, SCP, durcissement de la sécurité

## Scripts {#scripting}
- [[bash-scripting]] - Variables, conditionnelles, boucles, fonctions, débogage
- [[python-and-node-cli]] - Python/pip/venv et Node.js/npm en ligne de commande

## Architecture et fonctionnement interne {#architecture-internals}
- [[linux-kernel-and-boot]] - Noyau, modules, séquence de démarrage, GRUB, systèmes d'init, mémoire
- [[linux-os-structure]] - Espace noyau et espace utilisateur, sockets, fichiers de périphériques, modèle de sécurité

## Interopérabilité avec Windows {#windows-interop}
- [[wsl]] - Installation de WSL, interopérabilité des fichiers, réseau, configuration
- [[powershell-basics]] - Cmdlets, pipelines d'objets, variables, scripts

## Références complémentaires {#additional-references}

- [[disk-data-recovery]] - Récupération de disques défaillants ou de grande capacité (16 To et plus) au niveau bloc : imagerie, réparation des partitions/GPT
- [[ffmpeg-encoding]] - Encodeur multimédia en ligne de commande
