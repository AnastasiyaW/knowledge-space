---
title: Filesystem Hierarchy Standard
category: concepts
tags: [linux-cli, filesystem, fhs, directories]
---

# Filesystem Hierarchy Standard

Linux follows the Filesystem Hierarchy Standard (FHS). There are no drive letters - everything starts from a single root `/`. All devices, network filesystems, and special interfaces are attached via mounting. This entry covers the directory layout and the "everything is a file" philosophy.

## Key Facts

- Single root `/` - no drive letters (C:, D:)
- Case-sensitive filesystem
- All physical devices, network mounts, virtual interfaces appear as files under the tree
- Config files live in `/etc`, logs in `/var/log`, user data in `/home`

## Standard Directory Layout

| Directory | Purpose |
|-----------|---------|
| `/` | Root of filesystem tree |
| `/bin` | Essential user binaries (ls, cp, mv, bash) |
| `/sbin` | System binaries (iptables, reboot, fdisk) |
| `/boot` | Kernel, initrd, GRUB bootloader |
| `/dev` | Device files (hardware interfaces) |
| `/etc` | System-wide configuration files |
| `/home` | User home directories |
| `/lib`, `/lib64` | Shared libraries for `/bin` and `/sbin` |
| `/media` | Auto-mounted removable devices (USB, CD) |
| `/mnt` | Manual/temporary mount point |
| `/opt` | Optional/third-party software |
| `/proc` | Virtual FS: process and kernel info |
| `/root` | Root user's home directory |
| `/run` | Runtime data (PIDs, sockets) - cleared on reboot |
| `/srv` | Service data (web, FTP) |
| `/sys` | Kernel device/driver info |
| `/tmp` | Temporary files - cleared on reboot |
| `/usr` | User programs, libraries, documentation |
| `/var` | Variable data: logs, mail, caches |

## Everything Is a File

Unix philosophy: devices, directories, pipes, sockets - all represented as files.

| Symbol in `ls -l` | Type |
|-------------------|------|
| `-` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |
| `b` | Block device (random access: HDD, SSD) |
| `c` | Character device (sequential: terminal, keyboard) |
| `p` | Named pipe (FIFO) |
| `s` | Socket |

## Special Filesystems

| Type | Mount | Purpose |
|------|-------|---------|
| **procfs** | `/proc` | Process info, kernel parameters (required by `ps`, `top`) |
| **sysfs** | `/sys` | Kernel device/driver info |
| **tmpfs** | `/tmp`, `/run` | RAM-backed, fast, cleared on reboot |
| **devfs** | `/dev` | Device files (managed by `udev` at boot) |

## Filesystem Types for Disk Partitions

- **ext4** - standard Linux default
- **ext3** - older journaling FS
- **XFS** - high-performance, default on RHEL/CentOS
- **btrfs** - modern: snapshots, compression, subvolumes
- **NTFS/FAT32** - Windows filesystems (read/write supported)

### Virtual/Overlay Filesystems

- **VFS** - kernel abstraction for uniform FS access
- **NFS** - mount remote filesystem over network
- **AUFS** - merge multiple filesystems (used by Docker)
- **EncFS** - transparent file encryption

## Disk Usage Commands

```bash
df -h                    # mounted filesystems and space usage
df -h /home              # specific mount
du -sh /var/log          # total size of directory
du -h --max-depth=1 /    # size per top-level directory
lsblk                    # list block devices
```

## Archive Utilities

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

## Gotchas

- `/tmp` has sticky bit by default - everyone can write, but only file owners can delete their own files
- `/proc` files have size 0 in `ls` but contain data when read (generated on the fly by kernel)
- `/run` vs `/var/run`: `/run` is tmpfs (cleared on reboot), `/var/run` may persist
- `/home` is often a separate partition - reinstalling OS preserves user data

## See Also

- [[disks-and-filesystems]] - Partitions, formatting, ext4 internals, LVM
- [[file-permissions]] - Permission model, chmod, chown
- [[links-and-inodes]] - Inodes, hard links, symlinks
