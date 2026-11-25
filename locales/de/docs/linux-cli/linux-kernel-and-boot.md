---
title: "Linux-Kernel und Bootvorgang"
category: concepts
tags: [linux-cli, kernel, boot, grub, init, modules, memory]
level: 3
source_sha256: d19a070499c9f5704ed887f5856753a450d0d2988a40cdfc78eb1dfa256c3c95
translation: machine
translated_at: '2026-10-24'
---
# Linux-Kernel und Bootvorgang {#linux-kernel-and-boot-process}

Der Kernel ist der Kern des Betriebssystems und vermittelt zwischen Hardware und Benutzerprogrammen. Dieser Eintrag behandelt die Kernel-Architektur, Module, den Bootvorgang, die Speicherverwaltung und Init-Systeme.

## Wichtige Fakten {#key-facts}

- Linux verwendet einen **modularen Kernel** - Module werden ohne Neustart geladen und entladen
- Genau genommen ist "Linux" der Kernel; das Betriebssystem besteht aus GNU-Programmen und dem Linux-Kernel
- LTS-Kernel-Versionen erhalten eine verlängerte Wartung
- systemd ist auf modernen Distributionen PID 1

## Kernel-Funktionen {#kernel-functions}

1. **Gerätunterstützung** - USB, Webcams, Eingabegeräte
2. **Datenspeicherung** - RAM-Verwaltung, persistenter Speicher, virtuelles Dateisystem
3. **Netzwerkzugriff** - physische und virtuelle Vernetzung
4. **Task-Scheduling** - Aufteilung der CPU-Zeit, Prioritäten
5. **Sicherheit** - Dateiberechtigungen, Kontrolle des Ressourcenzugriffs

## Kernel-Version {#kernel-version}

Format: `A.B.C[.D]` (z. B. `5.4.20`, `6.1.52`)

```bash
uname -r          # kernel version only
uname -a          # all system info
uname -v          # version and build info
```

## Kernel-Space vs. User-Space {#kernel-space-vs-user-space}

- **Kernel-Space** - privilegiert, direkter Hardwarezugriff (Treiber, Dateisysteme)
- **User-Space** - eingeschränkt, Benutzerprogramme
- Kommunikation über **Systemaufrufe** (System Calls)

## Bootvorgang {#boot-sequence}

1. **BIOS/UEFI** - Hardware-Initialisierung, POST
2. **Partitionstabelle** - bootfähiges Gerät finden
3. **GRUB-Bootloader** - aus dem Bootsektor geladen
4. **Kernel** - GRUB lädt `vmlinuz` aus `/boot`
5. **initrd/initramfs** - temporäres Root-Dateisystem für den frühen Bootvorgang
6. **systemd (PID 1)** - startet alle Dienste

### GRUB-Konfiguration {#grub-configuration}

```bash
# User config (edit this)
/etc/default/grub

# Generated config (do NOT edit directly)
/boot/grub/grub.cfg

# Regenerate after editing
sudo update-grub                    # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL
```

### Inhalt von /boot {#boot-contents}

- `vmlinuz` - komprimiertes Kernel-Image
- `initrd.img` - initiale RAM-Disk
- `/boot/grub/` - Dateien des Bootloaders

## Kernel-Module {#kernel-modules}

```bash
lsmod                        # list loaded modules
modinfo <module>             # detailed info
sudo modprobe <module>       # load (resolves dependencies)
sudo modprobe -r <module>    # remove
sudo insmod /path/module.ko  # load from file (no deps)
sudo rmmod <module>          # remove
cat /proc/modules            # module info file
```

## Init-Systeme {#init-systems}

| System | Beschreibung |
|--------|-------------|
| **SysV Init** | Klassisch sequenziell, Runlevels |
| **Upstart** | Ereignisbasiert, parallel (Canonical) |
| **systemd** | Aktueller Standard, parallel, abhängigkeitsbasiert |

## Speicherverwaltung {#memory-management}

### Virtueller Speicher {#virtual-memory}

- Speicherseite (Page) = 4 KB
- Der Kernel weist Speicher auf Anforderung eines Prozesses zu
- Verdrängung nach LRU (Least Recently Used)

### Swap {#swap}

Erweitert den virtuellen Speicher über den physischen RAM hinaus.

- Kann eine Partition oder eine Datei sein
- Zur Laufzeit aktivierbar und deaktivierbar
- Wird für den Ruhezustand (Hibernation) verwendet

### OOM Killer {#oom-killer}

Ist der RAM erschöpft, beendet der OOM Killer Prozesse, um Speicher freizugeben. Jeder Prozess hat einen **OOM-Score** (je höher, desto wahrscheinlicher wird er beendet).

## Prozesserzeugung {#process-creation}

1. Name wird zugewiesen
2. Aufnahme in die Prozessliste
3. Priorität wird bestimmt
4. Process Control Block (PCB) wird angelegt
5. Ressourcen werden zugewiesen

## Signale {#signals}

| Signal | Nummer | Beschreibung |
|--------|--------|--------------|
| SIGHUP | 1 | Auflegen / neu laden |
| SIGINT | 2 | Unterbrechung (Strg+C) |
| SIGKILL | 9 | Erzwungenes Beenden |
| SIGTERM | 15 | Geordnetes Beenden |
| SIGSTOP | 19 | Anhalten (Strg+Z) |

```bash
kill -l                    # list all signals
kill -9 PID                # SIGKILL
kill -15 PID               # SIGTERM (default)
killall process            # kill by name
```

## Analyse des Bootvorgangs {#boot-analysis}

```bash
systemd-analyze                    # total boot time
systemd-analyze blame              # time per service
systemd-analyze critical-chain     # boot critical path
systemd-analyze plot > boot.svg    # visual timeline
```

## Fallstricke {#gotchas}

- Vor dem Laden in der Produktivumgebung die Stabilität des Moduls prüfen
- `insmod` löst keine Abhängigkeiten auf; `modprobe` schon
- Direktes Bearbeiten von `/boot/grub/grub.cfg` wird durch `update-grub` überschrieben
- Die Auswahl des OOM Killers ist nicht immer vorhersehbar - kritische Dienste können beendet werden
- Swap auf einer SSD verursacht Schreibverschleiß; Swap auf einer HDD verursacht Latenz

## Siehe auch {#see-also}

- [[systemd-and-services]] - systemctl, Lebenszyklus von Diensten
- [[disks-and-filesystems]] - Boot-Partition, LUKS, fstab
- [[process-management]] - Prozesszustände, Signale, kill
- [[monitoring-and-performance]] - Überwachung von Speicher und Last
