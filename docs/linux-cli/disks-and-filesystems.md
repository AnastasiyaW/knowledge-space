---
title: Disks and Filesystems
category: reference
tags: [linux-cli, disks, partitions, ext4, lvm, luks, mount, fstab]
---

# Disks and Filesystems

This entry covers disk device naming, partitioning, formatting, mounting, filesystem internals (ext3/ext4), LVM, LUKS encryption, health checking, and file recovery.

## Device Naming

All devices reside in `/dev/`.

| Pattern | Device Type |
|---------|------------|
| `/dev/sda`, `/dev/sdb` | SATA/SCSI disks (a, b, c...) |
| `/dev/sda1`, `/dev/sda2` | Disk partitions (1, 2...) |
| `/dev/nvme0n1`, `/dev/nvme0n1p1` | NVMe SSD and partitions |
| `/dev/sr0` | Optical drive |
| `/dev/null` | Discards all writes |
| `/dev/zero` | Returns null bytes |
| `/dev/random`, `/dev/urandom` | Random data sources |

Device file types: `b` (block), `c` (character), `l` (symlink), `p` (pipe).

## Partitioning

### Partition Tables

- **MBR** - legacy, max 2TB, max 4 primary partitions
- **GPT** - modern, supports >2TB, up to 128 partitions

### Tools

```bash
sudo fdisk -l              # list all disks and partitions
sudo fdisk /dev/sda        # MBR partitioning (interactive)
sudo gdisk /dev/sda        # GPT partitioning
sudo parted /dev/sda print # view partitions (both MBR/GPT)
sudo parted /dev/sda mklabel gpt
sudo parted /dev/sda mkpart primary ext4 1MiB 100GiB
```

## Formatting (Creating Filesystems)

```bash
mkfs.ext4 /dev/sda1        # ext4
mkfs.xfs /dev/sda2         # XFS
mkfs.btrfs /dev/sda3       # Btrfs
mkfs.vfat /dev/sdb1        # FAT32 (USB drives)
```

## Mounting

```bash
sudo mount /dev/sda1 /mnt/data          # mount partition
sudo mount -t ext4 /dev/sda1 /mnt/data  # specify type
sudo umount /mnt/data                    # unmount by mount point
sudo umount /dev/sda1                    # unmount by device
df -h                                    # show mounted filesystems
lsblk                                    # list block devices
mount -a                                 # mount all from /etc/fstab
```

### /etc/fstab - Persistent Mounts

```
# device      mountpoint  fstype  options            dump  pass
/dev/sda1     /           ext4    errors=remount-ro  0     1
/dev/sda2     /home       ext4    defaults           0     2
UUID=abc123   /data       ext4    defaults           0     2
/dev/sda3     swap        swap    sw                 0     0
```

Columns: device, mount point, filesystem, options, dump flag, fsck pass order.

## ext3/ext4 Journaling Modes

| Mode | Description |
|------|-------------|
| **journal** | Full - metadata AND data journaled |
| **ordered** | Default - metadata journaled, data written first |
| **writeback** | Metadata only - fastest, less safe |

## LVM (Logical Volume Manager)

Flexible disk management: pool physical volumes into volume groups, then carve logical volumes.

```
Physical Volumes (PV) -> Volume Groups (VG) -> Logical Volumes (LV)
```

```bash
pvcreate /dev/sda2                      # create PV
vgcreate vg0 /dev/sda2                  # create VG
lvcreate -L 20G -n root vg0            # create 20GB LV
mkfs.ext4 /dev/vg0/root                # format LV
```

## LUKS Disk Encryption

```bash
cryptsetup luksFormat /dev/sda2              # encrypt partition
cryptsetup luksOpen /dev/sda2 cryptdisk      # unlock
mkfs.ext4 /dev/mapper/cryptdisk              # format
mount /dev/mapper/cryptdisk /mnt/secure      # mount

# Close
umount /mnt/secure
cryptsetup luksClose cryptdisk
```

Typical encrypted LVM layout:
- `/boot` = **unencrypted** (kernel must load to decrypt the rest)
- Everything else (root, home, swap) inside LUKS -> LVM

Config: `/etc/crypttab` (analogous to fstab for encrypted volumes).

Pre-encryption: `dd if=/dev/urandom of=/dev/sda2 bs=1M` prevents metadata leakage.

## Disk Health

### SMART Monitoring

```bash
sudo apt install smartmontools
sudo smartctl -a /dev/sda          # full SMART report
sudo smartctl -H /dev/sda          # health status
sudo smartctl -t short /dev/sda    # short self-test
sudo smartctl -t long /dev/sda     # long self-test
```

### Bad Sectors

```bash
sudo badblocks -n /dev/sdb1               # non-destructive test
sudo badblocks -we /dev/sdb1 > bad.txt    # write-mode test
```

### fsck - Filesystem Check

```bash
sudo fsck /dev/sdb1                # basic check (must be unmounted)
sudo fsck -y /dev/sdb1             # auto-fix
sudo touch /forcefsck              # force check on next reboot
```

## File Recovery (ext4magic)

When deleted, data remains on disk until overwritten. Act immediately.

```bash
sudo apt install ext4magic
date -d "-10 minutes" +%s                              # get timestamp
sudo ext4magic /dev/sdb1 -a <timestamp> -f / -l        # list recoverable
sudo ext4magic /dev/sdb1 -a <timestamp> -f / -j journal.dump  # recover
# Recovered files go to ./RECOVERDIR/
```

## Gotchas

- Never run `fsck` on a mounted filesystem
- LUKS has no password recovery - lose the passphrase, lose the data
- `/boot` must be unencrypted for LUKS boot
- `dd` writes without confirmation and can destroy data - double-check device names
- `umount` fails if any process has files open in the mount - use `lsof` to find them
- NVMe partition naming uses `p` prefix: `nvme0n1p1`, not `nvme0n11`

## See Also

- [[filesystem-hierarchy]] - FHS directory layout
- [[links-and-inodes]] - Inode internals, ext4 structure
- [[linux-kernel-and-boot]] - Boot process and GRUB
- [[monitoring-and-performance]] - Disk I/O monitoring
