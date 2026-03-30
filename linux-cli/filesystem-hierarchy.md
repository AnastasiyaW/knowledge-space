---
title: Filesystem Hierarchy and Disk Management
category: concepts
tags: [filesystem, fhs, directories, mount, df, du, tar]
---
# Filesystem Hierarchy and Disk Management

Standard Linux directory structure, disk usage, mounting, and archiving.

## Key Facts

- Linux follows the Filesystem Hierarchy Standard (FHS)
- `/` - root of entire filesystem tree
- `/etc` - system-wide configuration files
- `/home` - user home directories (each user gets `/home/username`)
- `/var` - variable data (logs in `/var/log`, caches, spool)
- `/tmp` - temporary files (cleared on reboot, has [[file-permissions]] sticky bit)
- `/bin`, `/usr/bin` - essential/user command binaries
- `/sbin`, `/usr/sbin` - system/admin binaries
- `/dev` - device files (disks, terminals, pseudo-devices)
- `/media` - mount point for removable media (USB, CD) - default auto-mount location
- `/mnt` - temporary mount point for manual mounts
- `/opt` - optional/third-party software
- `~` - shortcut for current user's home directory
- Everything in Linux is a file - devices, pipes, sockets all appear in the filesystem

## Patterns

```bash
# Disk usage overview
df -h                        # Filesystem usage, human-readable
du -sh /var/log              # Total size of directory
du -sh *                     # Size of each item in current dir

# Mount/unmount filesystem
sudo mount /dev/sdb1 /mnt/usb     # Mount USB drive
sudo umount /mnt/usb               # Unmount (not "unmount"!)

# Check mounted filesystems
mount | grep sdb
df -h | grep sdb

# Create tar archive
tar -cf archive.tar /path/to/dir           # Create archive
tar -czf archive.tar.gz /path/to/dir       # Create gzipped archive
tar -cjf archive.tar.bz2 /path/to/dir     # Create bzip2 archive

# Extract tar archive
tar -xf archive.tar                        # Extract
tar -xzf archive.tar.gz                    # Extract gzipped
tar -xf archive.tar -C /target/dir         # Extract to specific dir

# List archive contents
tar -tf archive.tar

# Zip/unzip (install if needed: sudo apt install zip)
zip -r archive.zip /path/to/dir
unzip archive.zip

# Check what's in key directories
ls /etc/ssh/           # SSH configuration
ls /var/log/           # System logs
cat /etc/os-release    # OS version info
```

## Gotchas

- Command is `umount`, NOT `unmount` - common spelling mistake
- `/tmp` has sticky bit by default - users can create files but cannot delete other users' files
- `df -h` shows filesystem (partition) usage; `du -sh` shows directory size - different things
- Mounting over a non-empty directory hides existing contents (they return when unmounted)
- `/dev/sda` = whole disk, `/dev/sda1` = first partition - mounting the wrong one causes errors
- `tar -czf` order matters for some versions: flags before archive name, then files

## See Also

- [[file-permissions]] - directory permissions including sticky bit
- [[file-operations]] - navigating and manipulating the filesystem
- [[links-and-inodes]] - how files are referenced on disk
- `man hier` - https://man7.org/linux/man-pages/man7/hier.7.html
- FHS specification: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html
