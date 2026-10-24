---
title: "Cron et planification de tâches"
category: reference
tags: [linux-cli, cron, crontab, at, scheduling, automation]
level: 3
source_sha256: a0c20611c5d44fe30467773bdef6b5d20066c5bfade8862acf41a6576d0f4d67
translation: machine
translated_at: '2026-10-24'
---
# Cron et planification de tâches {#cron-and-task-scheduling}

cron gère les tâches planifiées récurrentes ; `at` gère l'exécution unique future. Cette entrée couvre la syntaxe de crontab, les raccourcis spéciaux, la planification ponctuelle et la gestion de l'heure système.

## cron - Tâches récurrentes {#cron-recurring-tasks}

### Gestion du service {#service-management}

```bash
systemctl status cron       # check status
sudo systemctl start cron   # start
sudo systemctl enable cron  # enable at boot
```

### Commandes crontab {#crontab-commands}

```bash
crontab -l                  # list current user's tasks
crontab -e                  # edit tasks (opens in $EDITOR)
crontab -r                  # delete ALL tasks for current user
crontab -u username -l      # list another user's tasks (needs sudo)
```

### Syntaxe de crontab {#crontab-syntax}

```text
* * * * * /path/to/command
| | | | |
| | | | +-- day of week (0-7, 0 and 7 = Sunday)
| | | +---- month (1-12 or jan-dec)
| | +------ day of month (1-31)
| +-------- hour (0-23)
+---------- minute (0-59)
```

Valeurs spéciales :
- `*` - chaque unité
- `*/n` - toutes les n unités (par ex. `*/5` = toutes les 5 minutes)
- `1,15` - valeurs spécifiques
- `1-5` - plage
- `jan,jul,oct` - mois nommés

### Exemples {#examples}

```bash
15 * * * * /run/script.sh             # every hour at :15
0 22 * * 1-5 /run/script.sh          # 22:00 Mon-Fri
0 0 1,15 * * /run/script.sh          # midnight on 1st and 15th
*/5 * * * * /run/script.sh            # every 5 minutes
0 9 * * * /run/script.sh              # daily at 9:00
```

### Raccourcis spéciaux {#special-shortcuts}

```text
@reboot    # run once at startup
@hourly    # = 0 * * * *
@daily     # = 0 0 * * *
@weekly    # = 0 0 * * 0
@monthly   # = 0 0 1 * *
```

### Journalisation de cron {#cron-logging}

```bash
grep CRON /var/log/syslog
journalctl -u cron
```

Référence : https://crontab.guru/ - testeur de syntaxe interactif

## at - Tâches ponctuelles {#at-one-time-tasks}

```bash
at 10pm                    # interactive mode, Ctrl+D to save
at 8:00am tomorrow
at -f script.sh 8:00am    # schedule a script
at now + 2 hours
at 14:30 Jul 31

atq                        # list pending jobs
atrm 3                     # cancel job #3
```

### Installer at {#install-at}

```bash
sudo apt install at
sudo systemctl enable --now atd
```

### batch {#batch}

Comme `at`, mais ne s'exécute que lorsque la charge du système descend sous un seuil donné.

## Heure système {#system-time}

### date {#date}

```bash
date                            # display current date/time
date +"%Y-%m-%d %H:%M:%S"      # formatted output
sudo date --set="2024-09-06 20:43:40"  # set manually (disable NTP first)
```

### hwclock - Horloge matérielle {#hwclock-hardware-clock}

```bash
hwclock                     # show hardware clock
hwclock --systohc           # sync hw clock from system time
hwclock --hctosys           # sync system time from hw clock
```

### Synchronisation NTP {#ntp-sync}

```bash
timedatectl status          # show time, timezone, NTP status
timedatectl set-ntp true    # enable NTP
timedatectl set-timezone Europe/Moscow
```

Remarque : un NTP actif écrase immédiatement un `date --set` manuel.

## Pièges à éviter {#gotchas}

- `crontab -r` supprime TOUTES les tâches sans confirmation - dangereux
- Les minutes 60 et les heures 24 sont invalides (0-59 et 0-23)
- Les tâches cron s'exécutent avec un environnement minimal - utilisez des chemins complets pour les commandes
- `@reboot` s'exécute une seule fois au démarrage du système, et non au redémarrage du service cron
- Si le jour du mois et le jour de la semaine sont tous deux définis, cron s'exécute si L'UN OU L'AUTRE correspond (logique OU)
- cron envoie un courriel pour la sortie des tâches - redirigez vers `/dev/null` ou un fichier journal pour éviter l'accumulation de courriels

## Voir aussi {#see-also}

- [[bash-scripting]] - Écrire des scripts à planifier
- [[systemd-and-services]] - Les timers systemd comme alternative à cron
- [[logging-and-journald]] - Consulter les journaux de cron
