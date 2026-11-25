---
title: "systemd und Dienste"
category: reference
tags: [linux-cli, systemd, systemctl, services, daemons, init]
level: 3
source_sha256: dea302f7b947665f44d20c60978d2dc3a47052f291f1acbd309fcbb3d4ed3bf5
translation: machine
translated_at: '2026-10-24'
---
# systemd und Dienste {#systemd-and-services}

systemd ist das Standard-Init-System moderner Linux-Distributionen und verwaltet den Lebenszyklus von Diensten, den Bootvorgang und den Systemzustand. Dieser Eintrag behandelt systemctl, Unit-Dateien, die journald-Integration und die Boot-Analyse.

## Wichtige Fakten {#key-facts}

- systemd ist auf den meisten modernen Distributionen PID 1 (Ubuntu, Debian, Fedora, RHEL)
- Drei Hauptkomponenten: systemd (Manager), systemctl (CLI), systemd-analyze (Diagnose)
- Unit-Dateien definieren Dienste, Timer, Mounts und andere verwaltete Objekte
- Dienste (Daemons) laufen im Hintergrund und starten typischerweise beim Booten

## systemctl-Befehle {#systemctl-commands}

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

## Unit-Dateien {#unit-files}

Zu finden in:
- `/lib/systemd/system/` - vom Paket bereitgestellte Units
- `/etc/systemd/system/` - vom Administrator verwaltete Units (höhere Priorität, überschreiben)

## Geschichte der Init-Systeme {#init-systems-history}

| System | Beschreibung |
|--------|--------------|
| **SysV Init** | Klassisch sequenziell, verwendet Runlevels |
| **Upstart** | Ereignisbasiert, paralleles Laden (Canonical) |
| **systemd** | Aktueller Standard: parallel, abhängigkeitsbasiert |

## Boot-Analyse {#boot-analysis}

```bash
systemd-analyze                    # total boot time
systemd-analyze blame              # time per service
systemd-analyze critical-chain     # critical path
systemd-analyze plot > boot.svg    # visual boot timeline
```

## Hardware-Inspektion {#hardware-inspection}

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

## Kernel-Module {#kernel-modules}

```bash
lsmod                        # list loaded modules
modinfo <module>             # module details
sudo modprobe <module>       # load module (resolves deps)
sudo modprobe -r <module>    # remove module
sudo insmod /path/module.ko  # load from file (no dep resolution)
sudo rmmod <module>          # remove module
cat /proc/modules            # loaded modules info
```

## Wichtige Konfigurationsdateien in /etc {#key-config-files-in-etc}

| Datei | Zweck |
|-------|-------|
| `/etc/hostname` | Systemhostname |
| `/etc/hosts` | IP-zu-Hostname-Zuordnung |
| `/etc/fstab` | Konfiguration der Dateisystem-Einbindung |
| `/etc/environment` | Globale Umgebungsvariablen |
| `/etc/bash.bashrc` | Globale Bash-Initialisierung |
| `/etc/crontab` | Systemweite cron-Konfiguration |

## Stolperfallen {#gotchas}

- Nach dem Bearbeiten von Unit-Dateien immer `daemon-reload` ausführen
- `enable` erstellt Symlinks für den Systemstart; der Dienst wird dadurch nicht gestartet – für beides `enable --now` verwenden
- `reload` funktioniert nur, wenn der Dienst dies unterstützt; `restart` funktioniert immer, unterbricht aber Verbindungen
- Manche Dienste benötigen `systemctl reload-or-restart` für sichere Aktualisierungen
- Es gibt weiterhin Distributionen ohne systemd (Alpine, Void, Artix) – dort das jeweils native Init-System verwenden

## Siehe auch {#see-also}

- [[process-management]] - ps, top, kill, Signale
- [[logging-and-journald]] - journalctl für Dienst-Logs
- [[linux-kernel-and-boot]] - Bootsequenz, GRUB, Kernel
- [[cron-and-scheduling]] - Aufgabenplanung
