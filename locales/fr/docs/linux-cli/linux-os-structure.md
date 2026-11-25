---
title: "Structure de l'OS Linux"
category: concepts
tags: [linux-cli, kernel, userspace, sockets, architecture]
level: 3
source_sha256: f107469349406f512257c33ace4936f764d989351b34a1f77b15ae81f9c9b09a
translation: machine
translated_at: '2026-10-24'
---
# Structure de l'OS Linux {#linux-os-structure}

L'architecture de Linux sépare l'espace noyau de l'espace utilisateur, utilise les fichiers comme abstractions universelles et fournit des mécanismes d'IPC, notamment les sockets et les tubes. Cette entrée couvre le modèle à deux couches, le détail des types de fichiers et la communication inter-processus.

## Espace noyau et espace utilisateur {#kernel-space-vs-user-space}

- **Espace noyau** - mémoire privilégiée pour les processus du noyau (pilotes, pilotes de systèmes de fichiers). Accès complet au matériel.
- **Espace utilisateur** - mémoire à priorité inférieure pour les processus lancés par l'utilisateur.
- **Appels système** - l'interface entre les programmes utilisateur et les services du noyau.

## Utilisateurs dans Linux {#users-in-linux}

Un « utilisateur » est un compte, qui n'est pas toujours humain. Les services système s'exécutent sous des utilisateurs dédiés.

| Type | Plage d'UID | Exemples |
|------|-------------|----------|
| Superutilisateur | 0 | root |
| Utilisateurs système | 1-99 | daemon, sshd, www-data |
| Utilisateurs réguliers | 1000+ | Comptes humains |

Informations utilisateur stockées dans : `/etc/passwd`, `/etc/shadow`, `/etc/group`

## Types de fichiers (détaillé) {#file-types-detailed}

| Type | Marqueur | Description |
|------|----------|-------------|
| Fichier régulier | `-` | Données, texte, binaires, scripts, images |
| Répertoire | `d` | Correspondances nom de fichier vers inode |
| Lien symbolique | `l` | Référence de chemin vers un autre fichier |
| Périphérique bloc | `b` | Matériel à accès aléatoire (HDD, SSD, USB) |
| Périphérique caractère | `c` | Accès séquentiel (terminal, clavier) |
| Tube nommé | `p` | IPC unidirectionnel |
| Socket | `s` | IPC bidirectionnel |

### Sortie de ls -l {#ls-l-output}

```text
-rwxr-xr-- 1 user group 4096 Jan 15 10:30 filename
^          ^ ^    ^     ^    ^             ^
type+perms links owner group size  date   name
```

## Sockets {#sockets}

Mécanisme d'IPC bidirectionnel, sur la même machine ou via le réseau.

| Type | Protocole | Description |
|------|-----------|-------------|
| Flux (stream) | TCP | Flux d'octets fiable et ordonné |
| Datagramme | UDP | Messages non fiables et non ordonnés |
| Paquets séquentiels | - | Datagrammes fiables de longueur fixe |
| Brut (raw) | Divers | Accès direct au protocole |

### Domaines de sockets {#socket-domains}

- **Domaine Unix** - IPC sur la même machine (rapide, sans surcharge réseau)
- **Domaine Internet** - communication réseau (IPv4/IPv6)

L'erreur « Cannot open socket » signifie généralement des permissions insuffisantes ; il peut être nécessaire d'utiliser `sudo` ou des capacités spécifiques.

## Fichiers de périphériques {#device-files}

Application -> fichier de périphérique -> pilote du noyau -> périphérique physique

Les fichiers de périphériques dans `/dev/` sont créés par `udev` au démarrage :
- Périphériques bloc (`b`) : données dans des blocs de taille fixe, accès aléatoire (HDD, SSD)
- Périphériques caractère (`c`) : flux d'octets séquentiel (terminal, clavier)

Rediriger vers un fichier de périphérique envoie les données directement : `cat doc.txt > /dev/lp0` (impression)

## Hiérarchie du système de fichiers (référence rapide) {#filesystem-hierarchy-quick-reference}

```javascript
/bin      Essential user binaries (available in single-user mode)
/sbin     System admin binaries (iptables, reboot, fdisk)
/etc      Configuration files
/dev      Device files
/proc     Process info (virtual FS)
/var      Variable data (logs, caches, mail)
/tmp      Temporary files (cleared on reboot)
/usr      User applications and libraries
/home     User home directories
/root     Root user's home
/boot     Kernel and bootloader
/opt      Optional software
/mnt      Manual mount point
/media    Auto-mounted removable media
/sys      Kernel device/driver info (virtual FS)
```

## Vue d'ensemble des mécanismes de sécurité {#security-mechanisms-overview}

| Mécanisme | Rôle |
|-----------|------|
| **DAC** | Le propriétaire du fichier contrôle l'accès |
| **ACL** | Permissions fines par utilisateur ou groupe |
| **Capacités (capabilities)** | Privilèges spécifiques sans root complet |
| **Espaces de noms (namespaces)** | Isolation des ressources (PID, réseau, FS) - fondement des conteneurs |
| **MAC** (SELinux, AppArmor) | Politique obligatoire centralisée |
| **Seccomp** | Restreint les appels système disponibles |
| **Audit** | Journalisation des événements de sécurité |

## Pièges courants {#gotchas}

- Les fichiers de `/proc` et `/sys` apparaissent avec une taille de 0 mais contiennent des données dynamiques du noyau
- Les périphériques bloc supportent l'accès aléatoire ; les périphériques caractère sont uniquement séquentiels
- Les sockets Unix sont plus rapides que TCP pour l'IPC sur la même machine (pas de pile réseau)
- Les espaces de noms sont le fondement des conteneurs Docker : ce n'est pas un concept nouveau, c'est au niveau du noyau
- Chaque programme en cours d'exécution est un processus, y compris les commandes du shell

## Voir aussi {#see-also}

- [[linux-kernel-and-boot]] - Architecture du noyau, modules, processus de démarrage
- [[filesystem-hierarchy]] - Standard de hiérarchie des répertoires FHS
- [[linux-security]] - Mécanismes de sécurité en détail
- [[users-and-groups]] - Gestion des utilisateurs
