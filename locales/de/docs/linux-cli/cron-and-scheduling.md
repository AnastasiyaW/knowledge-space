---
title: "Cron und Aufgabenplanung"
category: reference
tags: [linux-cli, cron, crontab, at, scheduling, automation]
level: 3
source_sha256: a0c20611c5d44fe30467773bdef6b5d20066c5bfade8862acf41a6576d0f4d67
translation: machine
translated_at: '2026-10-24'
---
# Cron und Aufgabenplanung {#cron-and-task-scheduling}

cron verwaltet wiederkehrende geplante Aufgaben; `at` führt Aufgaben einmalig zu einem künftigen Zeitpunkt aus. Dieser Eintrag behandelt die crontab-Syntax, spezielle Kurzformen, einmalige Planung und die Verwaltung der Systemzeit.

## cron - Wiederkehrende Aufgaben {#cron-recurring-tasks}

### Dienstverwaltung {#service-management}

```bash
systemctl status cron       # check status
sudo systemctl start cron   # start
sudo systemctl enable cron  # enable at boot
```

### crontab-Befehle {#crontab-commands}

```bash
crontab -l                  # list current user's tasks
crontab -e                  # edit tasks (opens in $EDITOR)
crontab -r                  # delete ALL tasks for current user
crontab -u username -l      # list another user's tasks (needs sudo)
```

### crontab-Syntax {#crontab-syntax}

```text
* * * * * /path/to/command
| | | | |
| | | | +-- day of week (0-7, 0 and 7 = Sunday)
| | | +---- month (1-12 or jan-dec)
| | +------ day of month (1-31)
| +-------- hour (0-23)
+---------- minute (0-59)
```

Spezielle Werte:
- `*` - jede Einheit
- `*/n` - alle n Einheiten (z. B. `*/5` = alle 5 Minuten)
- `1,15` - bestimmte Werte
- `1-5` - Bereich
- `jan,jul,oct` - benannte Monate

### Beispiele {#examples}

```bash
15 * * * * /run/script.sh             # every hour at :15
0 22 * * 1-5 /run/script.sh          # 22:00 Mon-Fri
0 0 1,15 * * /run/script.sh          # midnight on 1st and 15th
*/5 * * * * /run/script.sh            # every 5 minutes
0 9 * * * /run/script.sh              # daily at 9:00
```

### Spezielle Kurzformen {#special-shortcuts}

```text
@reboot    # run once at startup
@hourly    # = 0 * * * *
@daily     # = 0 0 * * *
@weekly    # = 0 0 * * 0
@monthly   # = 0 0 1 * *
```

### Protokollierung von cron {#cron-logging}

```bash
grep CRON /var/log/syslog
journalctl -u cron
```

Referenz: https://crontab.guru/ - interaktiver Syntax-Tester

## at - Einmalige Aufgaben {#at-one-time-tasks}

```bash
at 10pm                    # interactive mode, Ctrl+D to save
at 8:00am tomorrow
at -f script.sh 8:00am    # schedule a script
at now + 2 hours
at 14:30 Jul 31

atq                        # list pending jobs
atrm 3                     # cancel job #3
```

### at installieren {#install-at}

```bash
sudo apt install at
sudo systemctl enable --now atd
```

### batch {#batch}

Wie `at`, wird aber nur ausgeführt, wenn die Systemlast unter einen Schwellenwert fällt.

## Systemzeit {#system-time}

### date {#date}

```bash
date                            # display current date/time
date +"%Y-%m-%d %H:%M:%S"      # formatted output
sudo date --set="2024-09-06 20:43:40"  # set manually (disable NTP first)
```

### hwclock - Hardwareuhr {#hwclock-hardware-clock}

```bash
hwclock                     # show hardware clock
hwclock --systohc           # sync hw clock from system time
hwclock --hctosys           # sync system time from hw clock
```

### NTP-Synchronisation {#ntp-sync}

```bash
timedatectl status          # show time, timezone, NTP status
timedatectl set-ntp true    # enable NTP
timedatectl set-timezone Europe/Moscow
```

Hinweis: Eine aktive NTP-Synchronisation überschreibt manuelles `date --set` sofort.

## Fallstricke {#gotchas}

- `crontab -r` löscht ALLE Aufgaben ohne Rückfrage - gefährlich
- Minute 60 und Stunde 24 sind ungültig (0-59 bzw. 0-23)
- Cron-Jobs laufen mit einer minimalen Umgebung - verwende vollständige Pfade für Befehle
- `@reboot` wird einmal beim Systemstart ausgeführt, nicht beim Neustart des cron-Dienstes
- Sind sowohl Tag des Monats als auch Wochentag gesetzt, läuft cron, wenn EINES von beiden zutrifft (ODER-Verknüpfung)
- cron versendet die Ausgabe von Jobs per E-Mail - leite sie nach `/dev/null` oder in eine Logdatei um, um eine Anhäufung von E-Mails zu vermeiden

## Siehe auch {#see-also}

- [[bash-scripting]] - Schreiben von Skripten für die Planung
- [[systemd-and-services]] - systemd-Timer als Alternative zu cron
- [[logging-and-journald]] - Anzeigen der cron-Protokolle
