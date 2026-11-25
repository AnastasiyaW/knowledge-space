---
title: "Filesystem Hierarchy Standard"
category: concepts
tags: [linux-cli, filesystem, fhs, directories]
level: 3
source_sha256: 0a116d7c529345203175b21a5a5682b4a13b39b184311494e9f56d900a9f66e5
translation: machine
translated_at: '2026-10-24'
---
# Filesystem Hierarchy Standard {#filesystem-hierarchy-standard}

Linux folgt dem Filesystem Hierarchy Standard (FHS). Es gibt keine Laufwerksbuchstaben, alles beginnt an einer einzigen Wurzel `/`. Alle Geräte, Netzwerkdateisysteme und speziellen Schnittstellen werden per Mounting eingebunden. Dieser Eintrag beschreibt das Verzeichnislayout und die Philosophie „Alles ist eine Datei“.

## Wichtige Fakten {#key-facts}

- Einzelne Wurzel `/` - keine Laufwerksbuchstaben (C:, D:)
- Case-sensitives Dateisystem
- Alle physischen Geräte, Netzwerk-Mounts und virtuellen Schnittstellen erscheinen als Dateien im Verzeichnisbaum
- Konfigurationsdateien liegen in `/etc`, Logs in `/var/log`, Benutzerdaten in `/home`

## Standardisiertes Verzeichnislayout {#standard-directory-layout}

| Verzeichnis | Zweck |
|-------------|-------|
| `/` | Wurzel des Dateisystembaums |
| `/bin` | Essenzielle Benutzerbinärdateien (ls, cp, mv, bash) |
| `/sbin` | Systembinärdateien (iptables, reboot, fdisk) |
| `/boot` | Kernel, initrd, GRUB-Bootloader |
| `/dev` | Gerätedateien (Hardwareschnittstellen) |
| `/etc` | Systemweite Konfigurationsdateien |
| `/home` | Home-Verzeichnisse der Benutzer |
| `/lib`, `/lib64` | Shared Libraries für `/bin` und `/sbin` |
| `/media` | Automatisch eingebundene Wechselmedien (USB, CD) |
| `/mnt` | Manueller/temporärer Mountpoint |
| `/opt` | Optionale/Drittanbieter-Software |
| `/proc` | Virtuelles FS: Prozess- und Kerneninformationen |
| `/root` | Home-Verzeichnis des Root-Benutzers |
| `/run` | Laufzeitdaten (PIDs, Sockets) - wird beim Neustart geleert |
| `/srv` | Dienstdaten (Web, FTP) |
| `/sys` | Geräte-/Treiberinformationen des Kernels |
| `/tmp` | Temporäre Dateien - werden beim Neustart geleert |
| `/usr` | Benutzerprogramme, Bibliotheken, Dokumentation |
| `/var` | Variable Daten: Logs, Mail, Caches |

## Alles ist eine Datei {#everything-is-a-file}

Unix-Philosophie: Geräte, Verzeichnisse, Pipes, Sockets - alles wird als Datei dargestellt.

| Symbol in `ls -l` | Typ |
|-------------------|-----|
| `-` | Reguläre Datei |
| `d` | Verzeichnis |
| `l` | Symbolischer Link |
| `b` | Blockgerät (wahlfreier Zugriff: HDD, SSD) |
| `c` | Zeichengerät (sequenziell: Terminal, Tastatur) |
| `p` | Named Pipe (FIFO) |
| `s` | Socket |

## Spezielle Dateisysteme {#special-filesystems}

| Typ | Mount | Zweck |
|-----|-------|-------|
| **procfs** | `/proc` | Prozessinformationen, Kernel-Parameter (benötigt von `ps`, `top`) |
| **sysfs** | `/sys` | Geräte-/Treiberinformationen des Kernels |
| **tmpfs** | `/tmp`, `/run` | RAM-basiert, schnell, wird beim Neustart geleert |
| **devfs** | `/dev` | Gerätedateien (beim Booten von `udev` verwaltet) |

## Dateisystemtypen für Plattenpartitionen {#filesystem-types-for-disk-partitions}

- **ext4** - gängiger Linux-Standard
- **ext3** - älteres Journaling-Dateisystem
- **XFS** - leistungsstark, Standard bei RHEL/CentOS
- **btrfs** - modern: Snapshots, Komprimierung, Subvolumes
- **NTFS/FAT32** - Windows-Dateisysteme (Lese- und Schreibzugriff unterstützt)

### Virtuelle/Overlay-Dateisysteme {#virtualoverlay-filesystems}

- **VFS** - Kernel-Abstraktionsschicht für einheitlichen Dateisystemzugriff
- **NFS** - Einbindung eines entfernten Dateisystems über das Netzwerk
- **AUFS** - Zusammenführung mehrerer Dateisysteme (von Docker verwendet)
- **EncFS** - transparente Dateiverschlüsselung

## Befehle zur Speicherbelegung {#disk-usage-commands}

```bash
df -h                    # mounted filesystems and space usage
df -h /home              # specific mount
du -sh /var/log          # total size of directory
du -h --max-depth=1 /    # size per top-level directory
lsblk                    # list block devices
```

## Archivierungswerkzeuge {#archive-utilities}

```bash
# tar
tar -czf archive.tar.gz dir/         # create gzip archive
tar -xzf archive.tar.gz              # extract
tar -tf archive.tar.gz               # list contents

# zip
zip -r archive.zip dir/
unzip archive.zip
unzip -l archive.zip                  # list contents
```

## Stolperfallen {#gotchas}

- `/tmp` hat standardmäßig das Sticky-Bit gesetzt - jeder kann schreiben, aber nur die Besitzer können ihre eigenen Dateien löschen
- Dateien unter `/proc` haben in `ls` die Größe 0, enthalten beim Lesen aber Daten (werden vom Kernel dynamisch erzeugt)
- `/run` vs. `/var/run`: `/run` ist ein tmpfs (wird beim Neustart geleert), `/var/run` kann erhalten bleiben
- `/home` ist häufig eine separate Partition - eine Neuinstallation des Betriebssystems erhält die Benutzerdaten

## Siehe auch {#see-also}

- [[disks-and-filesystems]] - Partitionen, Formatierung, ext4-Interna, LVM
- [[file-permissions]] - Berechtigungsmodell, chmod, chown
- [[links-and-inodes]] - Inodes, Hardlinks, Symlinks
