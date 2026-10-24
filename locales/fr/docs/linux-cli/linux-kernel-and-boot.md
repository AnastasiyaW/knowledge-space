---
title: "Noyau Linux et processus de démarrage"
category: concepts
tags: [linux-cli, kernel, boot, grub, init, modules, memory]
level: 3
source_sha256: d19a070499c9f5704ed887f5856753a450d0d2988a40cdfc78eb1dfa256c3c95
translation: machine
translated_at: '2026-10-24'
---
# Noyau Linux et processus de démarrage {#linux-kernel-and-boot-process}

Le noyau est le cœur du système d'exploitation, qui sert d'intermédiaire entre le matériel et les programmes utilisateur. Cette entrée couvre l'architecture du noyau, les modules, la séquence de démarrage, la gestion de la mémoire et les systèmes d'initialisation.

## Points clés {#key-facts}

- Linux utilise un **noyau modulaire** : les modules se chargent et se déchargent sans redémarrage
- Techniquement, « Linux » désigne le noyau ; le système d'exploitation = programmes GNU + noyau Linux
- Les versions de noyau LTS bénéficient d'une maintenance étendue
- systemd est PID 1 sur les distributions modernes

## Fonctions du noyau {#kernel-functions}

1. **Prise en charge des périphériques** : USB, webcams, périphériques d'entrée
2. **Stockage des données** : gestion de la RAM, stockage persistant, système de fichiers virtuel
3. **Accès réseau** : réseau physique et virtuel
4. **Ordonnancement des tâches** : partage du temps CPU, priorités
5. **Sécurité** : permissions de fichiers, contrôle d'accès aux ressources

## Version du noyau {#kernel-version}

Format : `A.B.C[.D]` (par ex. `5.4.20`, `6.1.52`)

```bash
uname -r          # kernel version only
uname -a          # all system info
uname -v          # version and build info
```

## Espace noyau et espace utilisateur {#kernel-space-vs-user-space}

- **Espace noyau** : privilégié, accès direct au matériel (pilotes, FS)
- **Espace utilisateur** : restreint, programmes utilisateur
- Communication via des **appels système**

## Séquence de démarrage {#boot-sequence}

1. **BIOS/UEFI** : initialisation du matériel, POST
2. **Table de partitions** : recherche du périphérique amorçable
3. **Chargeur de démarrage GRUB** : chargé depuis le secteur de démarrage
4. **Noyau** : GRUB charge `vmlinuz` depuis `/boot`
5. **initrd/initramfs** : système de fichiers racine temporaire pour le démarrage précoce
6. **systemd (PID 1)** : démarre l'ensemble des services

### Configuration de GRUB {#grub-configuration}

```bash
# User config (edit this)
/etc/default/grub

# Generated config (do NOT edit directly)
/boot/grub/grub.cfg

# Regenerate after editing
sudo update-grub                    # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL
```

### Contenu de /boot {#boot-contents}

- `vmlinuz` : image du noyau compressée
- `initrd.img` : disque RAM initial
- `/boot/grub/` : fichiers du chargeur de démarrage

## Modules du noyau {#kernel-modules}

```bash
lsmod                        # list loaded modules
modinfo <module>             # detailed info
sudo modprobe <module>       # load (resolves dependencies)
sudo modprobe -r <module>    # remove
sudo insmod /path/module.ko  # load from file (no deps)
sudo rmmod <module>          # remove
cat /proc/modules            # module info file
```

## Systèmes d'initialisation {#init-systems}

| Système | Description |
|--------|-------------|
| **SysV Init** | Classique, séquentiel, niveaux d'exécution (runlevels) |
| **Upstart** | Basé sur les événements, parallèle (Canonical) |
| **systemd** | Standard actuel, parallèle, basé sur les dépendances |

## Gestion de la mémoire {#memory-management}

### Mémoire virtuelle {#virtual-memory}

- Page mémoire = 4 Ko
- Le noyau alloue la mémoire à la demande des processus
- Éviction de cache LRU (Least Recently Used)

### Swap {#swap}

Étend la mémoire virtuelle au-delà de la RAM physique.

- Peut être une partition ou un fichier
- Activable et désactivable à l'exécution
- Utilisé pour l'état de mise en veille prolongée (hibernation)

### OOM Killer {#oom-killer}

Lorsque la RAM est épuisée, l'OOM Killer termine des processus pour libérer de la mémoire. Chaque processus possède un **score OOM** (plus il est élevé, plus le processus risque d'être tué).

## Création de processus {#process-creation}

1. Attribution d'un nom
2. Ajout à la liste des processus
3. Détermination de la priorité
4. Formation du bloc de contrôle de processus (PCB)
5. Allocation des ressources

## Signaux {#signals}

| Signal | Numéro | Description |
|--------|--------|-------------|
| SIGHUP | 1 | Fin de session / rechargement |
| SIGINT | 2 | Interruption (Ctrl+C) |
| SIGKILL | 9 | Arrêt forcé |
| SIGTERM | 15 | Arrêt propre |
| SIGSTOP | 19 | Suspension (Ctrl+Z) |

```bash
kill -l                    # list all signals
kill -9 PID                # SIGKILL
kill -15 PID               # SIGTERM (default)
killall process            # kill by name
```

## Analyse du démarrage {#boot-analysis}

```bash
systemd-analyze                    # total boot time
systemd-analyze blame              # time per service
systemd-analyze critical-chain     # boot critical path
systemd-analyze plot > boot.svg    # visual timeline
```

## Pièges à éviter {#gotchas}

- Vérifier la stabilité d'un module avant de le charger en production
- `insmod` ne résout pas les dépendances ; `modprobe` le fait
- Modifier `/boot/grub/grub.cfg` directement est écrasé par `update-grub`
- La sélection de l'OOM Killer n'est pas toujours prévisible : des services critiques peuvent être tués
- Le swap sur SSD use les cellules d'écriture ; le swap sur HDD entraîne de la latence

## Voir aussi {#see-also}

- [[systemd-and-services]] - systemctl, cycle de vie des services
- [[disks-and-filesystems]] - Partition de démarrage, LUKS, fstab
- [[process-management]] - États des processus, signaux, kill
- [[monitoring-and-performance]] - Surveillance de la mémoire et de la charge
