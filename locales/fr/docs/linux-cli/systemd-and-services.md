---
title: "systemd et les services"
category: reference
tags: [linux-cli, systemd, systemctl, services, daemons, init]
level: 3
source_sha256: dea302f7b947665f44d20c60978d2dc3a47052f291f1acbd309fcbb3d4ed3bf5
translation: machine
translated_at: '2026-10-24'
---
# systemd et les services {#systemd-and-services}

systemd est le système d'init standard sous Linux moderne, qui gère le cycle de vie des services, le processus de démarrage et l'état du système. Cette entrée couvre systemctl, les fichiers d'unités, l'intégration avec journald et l'analyse du démarrage.

## Points clés {#key-facts}

- systemd est PID 1 sur la plupart des distributions modernes (Ubuntu, Debian, Fedora, RHEL)
- Trois composants principaux : systemd (gestionnaire), systemctl (CLI), systemd-analyze (diagnostics)
- Les fichiers d'unités définissent les services, les timers, les montages et d'autres objets gérés
- Les services (daemons) s'exécutent en arrière-plan, généralement démarrés au boot

## Commandes systemctl {#systemctl-commands}

```bash
systemctl start <service>       # start service
systemctl stop <service>        # stop service
systemctl restart <service>     # stop + start
systemctl reload <service>      # reload config without restart
systemctl status <service>      # show status and recent logs
systemctl enable <service>      # enable autostart at boot
systemctl disable <service>     # disable autostart
systemctl is-active <service>   # check if running
systemctl is-enabled <service>  # check if enabled at boot
systemctl list-units --type=service  # list all services
systemctl list-units --state=running # only running
systemctl --failed              # list failed services
sudo systemctl daemon-reload    # reload unit files after changes
```

## Fichiers d'unités {#unit-files}

Emplacements :
- `/lib/systemd/system/` - unités fournies par les paquets
- `/etc/systemd/system/` - unités gérées par l'administrateur (priorité plus élevée, surcharges)

## Historique des systèmes d'init {#init-systems-history}

| Système | Description |
|---------|-------------|
| **SysV Init** | Classique, séquentiel, utilise des niveaux d'exécution (runlevels) |
| **Upstart** | Basé sur les événements, chargement parallèle (Canonical) |
| **systemd** | Standard actuel : parallèle, basé sur les dépendances |

## Analyse du démarrage {#boot-analysis}

```bash
systemd-analyze                    # total boot time
systemd-analyze blame              # time per service
systemd-analyze critical-chain     # critical path
systemd-analyze plot > boot.svg    # visual boot timeline
```

## Inspection du matériel {#hardware-inspection}

```bash
lspci                    # PCI devices (GPU, NIC, etc.)
lspci -v                 # verbose
lspci -v | grep Kernel   # show loaded drivers
lsusb                    # USB devices
lsusb -t                 # tree view
lscpu                    # CPU information
lsscsi                   # SCSI/SATA devices
lshw                     # all hardware (needs install)
lshw --class network     # filter by class
```

## Modules du noyau {#kernel-modules}

```bash
lsmod                        # list loaded modules
modinfo <module>             # module details
sudo modprobe <module>       # load module (resolves deps)
sudo modprobe -r <module>    # remove module
sudo insmod /path/module.ko  # load from file (no dep resolution)
sudo rmmod <module>          # remove module
cat /proc/modules            # loaded modules info
```

## Principaux fichiers de configuration dans /etc {#key-config-files-in-etc}

| Fichier | Rôle |
|---------|------|
| `/etc/hostname` | Nom d'hôte du système |
| `/etc/hosts` | Correspondance IP-nom d'hôte |
| `/etc/fstab` | Configuration des montages de systèmes de fichiers |
| `/etc/environment` | Variables d'environnement globales |
| `/etc/bash.bashrc` | Initialisation globale de bash |
| `/etc/crontab` | Configuration cron système |

## Pièges courants {#gotchas}

- Exécutez toujours `daemon-reload` après avoir modifié des fichiers d'unités
- `enable` crée des liens symboliques pour le démarrage ; il ne démarre pas le service - utilisez `enable --now` pour les deux
- `reload` ne fonctionne que si le service le supporte ; `restart` fonctionne toujours mais interrompt les connexions
- Certains services nécessitent `systemctl reload-or-restart` pour des mises à jour sûres
- Les distributions non systemd existent encore (Alpine, Void, Artix) - utilisez leur système d'init natif

## Voir aussi {#see-also}

- [[process-management]] - ps, top, kill, signaux
- [[logging-and-journald]] - journalctl pour les journaux de services
- [[linux-kernel-and-boot]] - Séquence de démarrage, GRUB, noyau
- [[cron-and-scheduling]] - Planification des tâches
