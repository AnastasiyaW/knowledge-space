---
title: "Disques et systèmes de fichiers"
category: reference
tags: [linux-cli, disks, partitions, ext4, lvm, luks, mount, fstab]
level: 4
source_sha256: 3e7a51929e936b81ae971cf27b0dbeae53aed6e26e10b141516cbd755ee21968
translation: machine
translated_at: '2026-10-24'
---
# Disques et systèmes de fichiers {#disks-and-filesystems}

Cette entrée couvre le nommage des périphériques disque, le partitionnement, le formatage, le montage, le fonctionnement interne des systèmes de fichiers (ext3/ext4), LVM, le chiffrement LUKS, la vérification de l'état de santé et la récupération de fichiers.

## Nommage des périphériques {#device-naming}

Tous les périphériques se trouvent dans `/dev/`.

| Motif | Type de périphérique |
|---------|------------|
| `/dev/sda`, `/dev/sdb` | Disques SATA/SCSI (a, b, c...) |
| `/dev/sda1`, `/dev/sda2` | Partitions de disque (1, 2...) |
| `/dev/nvme0n1`, `/dev/nvme0n1p1` | SSD NVMe et partitions |
| `/dev/sr0` | Lecteur optique |
| `/dev/null` | Supprime toutes les écritures |
| `/dev/zero` | Renvoie des octets nuls |
| `/dev/random`, `/dev/urandom` | Sources de données aléatoires |

Types de fichiers de périphériques : `b` (bloc), `c` (caractère), `l` (lien symbolique), `p` (tube nommé).

## Partitionnement {#partitioning}

### Tables de partitions {#partition-tables}

- **MBR** - ancienne, 2 To maximum, 4 partitions primaires maximum
- **GPT** - moderne, prend en charge plus de 2 To, jusqu'à 128 partitions

### Outils {#tools}

```bash
sudo fdisk -l              # list all disks and partitions
sudo fdisk /dev/sda        # MBR partitioning (interactive)
sudo gdisk /dev/sda        # GPT partitioning
sudo parted /dev/sda print # view partitions (both MBR/GPT)
sudo parted /dev/sda mklabel gpt
sudo parted /dev/sda mkpart primary ext4 1MiB 100GiB
```

## Formatage (création des systèmes de fichiers) {#formatting-creating-filesystems}

```bash
mkfs.ext4 /dev/sda1        # ext4
mkfs.xfs /dev/sda2         # XFS
mkfs.btrfs /dev/sda3       # Btrfs
mkfs.vfat /dev/sdb1        # FAT32 (USB drives)
```

## Montage {#mounting}

```bash
sudo mount /dev/sda1 /mnt/data          # mount partition
sudo mount -t ext4 /dev/sda1 /mnt/data  # specify type
sudo umount /mnt/data                    # unmount by mount point
sudo umount /dev/sda1                    # unmount by device
df -h                                    # show mounted filesystems
lsblk                                    # list block devices
mount -a                                 # mount all from /etc/fstab
```

### /etc/fstab - Montages persistants {#etcfstab-persistent-mounts}

```ini
# device      mountpoint  fstype  options            dump  pass
/dev/sda1     /           ext4    errors=remount-ro  0     1
/dev/sda2     /home       ext4    defaults           0     2
UUID=abc123   /data       ext4    defaults           0     2
/dev/sda3     swap        swap    sw                 0     0
```

Colonnes : périphérique, point de montage, système de fichiers, options, indicateur dump, ordre de passage de fsck.

## Modes de journalisation ext3/ext4 {#ext3ext4-journaling-modes}

| Mode | Description |
|------|-------------|
| **journal** | Complet - métadonnées ET données journalisées |
| **ordered** | Par défaut - métadonnées journalisées, données écrites en premier |
| **writeback** | Métadonnées seulement - le plus rapide, moins sûr |

## LVM (Logical Volume Manager) {#lvm-logical-volume-manager}

Gestion souple des disques : regrouper des volumes physiques dans des groupes de volumes, puis découper des volumes logiques.

```php
Physical Volumes (PV) -> Volume Groups (VG) -> Logical Volumes (LV)
```

```bash
pvcreate /dev/sda2                      # create PV
vgcreate vg0 /dev/sda2                  # create VG
lvcreate -L 20G -n root vg0            # create 20GB LV
mkfs.ext4 /dev/vg0/root                # format LV
```

## Chiffrement de disque LUKS {#luks-disk-encryption}

```bash
cryptsetup luksFormat /dev/sda2              # encrypt partition
cryptsetup luksOpen /dev/sda2 cryptdisk      # unlock
mkfs.ext4 /dev/mapper/cryptdisk              # format
mount /dev/mapper/cryptdisk /mnt/secure      # mount

# Close
umount /mnt/secure
cryptsetup luksClose cryptdisk
```

Disposition typique d'un LVM chiffré :
- `/boot` = **non chiffré** (le noyau doit pouvoir se charger pour déchiffrer le reste)
- Tout le reste (root, home, swap) à l'intérieur de LUKS -> LVM

Configuration : `/etc/crypttab` (équivalent de fstab pour les volumes chiffrés).

Pré-chiffrement : `dd if=/dev/urandom of=/dev/sda2 bs=1M` empêche la fuite de métadonnées.

## Santé des disques {#disk-health}

### Surveillance SMART {#smart-monitoring}

```bash
sudo apt install smartmontools
sudo smartctl -a /dev/sda          # full SMART report
sudo smartctl -H /dev/sda          # health status
sudo smartctl -t short /dev/sda    # short self-test
sudo smartctl -t long /dev/sda     # long self-test
```

### Secteurs défectueux {#bad-sectors}

```bash
sudo badblocks -n /dev/sdb1               # non-destructive test
sudo badblocks -we /dev/sdb1 > bad.txt    # write-mode test
```

### fsck - Vérification du système de fichiers {#fsck-filesystem-check}

```bash
sudo fsck /dev/sdb1                # basic check (must be unmounted)
sudo fsck -y /dev/sdb1             # auto-fix
sudo touch /forcefsck              # force check on next reboot
```

## Récupération de fichiers (ext4magic) {#file-recovery-ext4magic}

Une fois supprimées, les données restent sur le disque jusqu'à être écrasées. Agissez immédiatement.

```bash
sudo apt install ext4magic
date -d "-10 minutes" +%s                              # get timestamp
sudo ext4magic /dev/sdb1 -a <timestamp> -f / -l        # list recoverable
sudo ext4magic /dev/sdb1 -a <timestamp> -f / -j journal.dump  # recover
# Recovered files go to ./RECOVERDIR/
```

## Pièges à éviter {#gotchas}

- Ne jamais exécuter `fsck` sur un système de fichiers monté
- LUKS n'offre aucune récupération de mot de passe : perdre la phrase de passe, c'est perdre les données
- `/boot` doit être non chiffré pour un démarrage LUKS
- `dd` écrit sans confirmation et peut détruire des données : vérifiez bien les noms de périphériques
- `umount` échoue si un processus a des fichiers ouverts dans le montage : utilisez `lsof` pour les identifier
- Le nommage des partitions NVMe utilise le préfixe `p` : `nvme0n1p1`, et non `nvme0n11`

## Voir aussi {#see-also}

- [[filesystem-hierarchy]] - Arborescence FHS des répertoires
- [[links-and-inodes]] - Fonctionnement interne des inodes, structure d'ext4
- [[linux-kernel-and-boot]] - Processus de démarrage et GRUB
- [[monitoring-and-performance]] - Surveillance des E/S disque
