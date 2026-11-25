---
title: "Festplatten und Dateisysteme"
category: reference
tags: [linux-cli, disks, partitions, ext4, lvm, luks, mount, fstab]
level: 4
source_sha256: 3e7a51929e936b81ae971cf27b0dbeae53aed6e26e10b141516cbd755ee21968
translation: machine
translated_at: '2026-10-24'
---
# Festplatten und Dateisysteme {#disks-and-filesystems}

Dieser Eintrag behandelt die Benennung von Datenträgern, Partitionierung, Formatierung, Einhängen (Mounten), die Interna von Dateisystemen (ext3/ext4), LVM, LUKS-Verschlüsselung, Zustandsprüfung und Dateiwiederherstellung.

## Gerätebenennung {#device-naming}

Alle Geräte befinden sich in `/dev/`.

| Muster | Gerätetyp |
|--------|-----------|
| `/dev/sda`, `/dev/sdb` | SATA/SCSI-Festplatten (a, b, c ...) |
| `/dev/sda1`, `/dev/sda2` | Festplattenpartitionen (1, 2 ...) |
| `/dev/nvme0n1`, `/dev/nvme0n1p1` | NVMe-SSD und Partitionen |
| `/dev/sr0` | optisches Laufwerk |
| `/dev/null` | verwirft alle Schreibvorgänge |
| `/dev/zero` | liefert Null-Bytes |
| `/dev/random`, `/dev/urandom` | Quellen für Zufallsdaten |

Gerätedateitypen: `b` (Block), `c` (Zeichen), `l` (Symlink), `p` (Pipe).

## Partitionierung {#partitioning}

### Partitionstabellen {#partition-tables}

- **MBR** - veraltet, maximal 2TB, maximal 4 primäre Partitionen
- **GPT** - modern, unterstützt mehr als 2TB, bis zu 128 Partitionen

### Werkzeuge {#tools}

```bash
sudo fdisk -l              # list all disks and partitions
sudo fdisk /dev/sda        # MBR partitioning (interactive)
sudo gdisk /dev/sda        # GPT partitioning
sudo parted /dev/sda print # view partitions (both MBR/GPT)
sudo parted /dev/sda mklabel gpt
sudo parted /dev/sda mkpart primary ext4 1MiB 100GiB
```

## Formatierung (Erstellen von Dateisystemen) {#formatting-creating-filesystems}

```bash
mkfs.ext4 /dev/sda1        # ext4
mkfs.xfs /dev/sda2         # XFS
mkfs.btrfs /dev/sda3       # Btrfs
mkfs.vfat /dev/sdb1        # FAT32 (USB drives)
```

## Einhängen (Mounten) {#mounting}

```bash
sudo mount /dev/sda1 /mnt/data          # mount partition
sudo mount -t ext4 /dev/sda1 /mnt/data  # specify type
sudo umount /mnt/data                    # unmount by mount point
sudo umount /dev/sda1                    # unmount by device
df -h                                    # show mounted filesystems
lsblk                                    # list block devices
mount -a                                 # mount all from /etc/fstab
```

### /etc/fstab - dauerhafte Einhängungen {#etcfstab-persistent-mounts}

```ini
# device      mountpoint  fstype  options            dump  pass
/dev/sda1     /           ext4    errors=remount-ro  0     1
/dev/sda2     /home       ext4    defaults           0     2
UUID=abc123   /data       ext4    defaults           0     2
/dev/sda3     swap        swap    sw                 0     0
```

Spalten: Gerät, Einhängepunkt, Dateisystem, Optionen, Dump-Flag, Reihenfolge der fsck-Prüfung.

## ext3/ext4-Journaling-Modi {#ext3ext4-journaling-modes}

| Modus | Beschreibung |
|-------|--------------|
| **journal** | vollständig - Metadaten UND Daten im Journal |
| **ordered** | Standard - Metadaten im Journal, Daten werden vorher geschrieben |
| **writeback** | nur Metadaten - am schnellsten, weniger sicher |

## LVM (Logical Volume Manager) {#lvm-logical-volume-manager}

Flexible Datenträgerverwaltung: physische Volumes werden zu Volume Groups zusammengefasst, aus denen anschließend logische Volumes geschnitten werden.

```php
Physical Volumes (PV) -> Volume Groups (VG) -> Logical Volumes (LV)
```

```bash
pvcreate /dev/sda2                      # create PV
vgcreate vg0 /dev/sda2                  # create VG
lvcreate -L 20G -n root vg0            # create 20GB LV
mkfs.ext4 /dev/vg0/root                # format LV
```

## LUKS-Festplattenverschlüsselung {#luks-disk-encryption}

```bash
cryptsetup luksFormat /dev/sda2              # encrypt partition
cryptsetup luksOpen /dev/sda2 cryptdisk      # unlock
mkfs.ext4 /dev/mapper/cryptdisk              # format
mount /dev/mapper/cryptdisk /mnt/secure      # mount

# Close
umount /mnt/secure
cryptsetup luksClose cryptdisk
```

Typisches verschlüsseltes LVM-Layout:
- `/boot` = **unverschlüsselt** (der Kernel muss geladen werden, um den Rest zu entschlüsseln)
- Alles Übrige (Root, Home, Swap) innerhalb von LUKS -> LVM

Konfiguration: `/etc/crypttab` (analog zu fstab für verschlüsselte Volumes).

Vorab-Verschlüsselung: `dd if=/dev/urandom of=/dev/sda2 bs=1M` verhindert das Auslesen von Metadaten.

## Festplattenzustand {#disk-health}

### SMART-Überwachung {#smart-monitoring}

```bash
sudo apt install smartmontools
sudo smartctl -a /dev/sda          # full SMART report
sudo smartctl -H /dev/sda          # health status
sudo smartctl -t short /dev/sda    # short self-test
sudo smartctl -t long /dev/sda     # long self-test
```

### Defekte Sektoren {#bad-sectors}

```bash
sudo badblocks -n /dev/sdb1               # non-destructive test
sudo badblocks -we /dev/sdb1 > bad.txt    # write-mode test
```

### fsck - Dateisystemprüfung {#fsck-filesystem-check}

```bash
sudo fsck /dev/sdb1                # basic check (must be unmounted)
sudo fsck -y /dev/sdb1             # auto-fix
sudo touch /forcefsck              # force check on next reboot
```

## Dateiwiederherstellung (ext4magic) {#file-recovery-ext4magic}

Gelöschte Daten bleiben auf der Festplatte, bis sie überschrieben werden. Sofort handeln.

```bash
sudo apt install ext4magic
date -d "-10 minutes" +%s                              # get timestamp
sudo ext4magic /dev/sdb1 -a <timestamp> -f / -l        # list recoverable
sudo ext4magic /dev/sdb1 -a <timestamp> -f / -j journal.dump  # recover
# Recovered files go to ./RECOVERDIR/
```

## Fallstricke {#gotchas}

- Niemals `fsck` auf einem eingehängten Dateisystem ausführen
- LUKS bietet keine Passwortwiederherstellung - wer die Passphrase verliert, verliert die Daten
- `/boot` muss für einen LUKS-Start unverschlüsselt sein
- `dd` schreibt ohne Rückfrage und kann Daten zerstören - Gerätenamen doppelt prüfen
- `umount` schlägt fehl, sobald ein Prozess Dateien im Einhängepunkt geöffnet hat - mit `lsof` lassen sich diese finden
- Bei NVMe-Partitionen wird das Präfix `p` verwendet: `nvme0n1p1`, nicht `nvme0n11`

## Siehe auch {#see-also}

- [[filesystem-hierarchy]] - Verzeichnisstruktur nach FHS
- [[links-and-inodes]] - Inode-Interna, ext4-Aufbau
- [[linux-kernel-and-boot]] - Bootvorgang und GRUB
- [[monitoring-and-performance]] - Überwachung der Festplatten-E/A
