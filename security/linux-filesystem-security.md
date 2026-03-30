---
title: Linux Filesystem Security
category: system-security
tags: [linux, filesystem, permissions, ext4, mounting, fhs, hardening]
---

# Linux Filesystem Security

## Key Facts

- FHS (Filesystem Hierarchy Standard) defines standard directory layout: `/bin`, `/sbin`, `/etc`, `/var`, `/home`, `/tmp`, `/proc`, `/sys`
- `/etc` contains all system configuration files - protecting this directory is critical for system security
- `/tmp` and `/var/tmp` are world-writable - common target for attackers to stage exploits and write web shells
- File permissions model: owner/group/other with read(4)/write(2)/execute(1) bits; special bits: SUID(4000), SGID(2000), sticky(1000)
- Everything in Linux is a file: devices (`/dev/sda`), processes (`/proc/PID/`), kernel parameters (`/sys/`)
- Filesystem types: ext4 (default), XFS (large files), btrfs (snapshots), tmpfs (RAM-based), procfs/sysfs (virtual)
- [[linux-user-security]] controls who can access which files
- [[linux-kernel-security]] enforces filesystem permissions at the kernel level

## Patterns

```bash
# Critical directories for security
/etc/shadow    # Password hashes (root only: 640)
/etc/sudoers   # Sudo configuration (root only: 440)
/etc/ssh/      # SSH server configuration
/var/log/      # System logs (log integrity monitoring)
/tmp/          # World-writable temp (mount with noexec,nosuid)

# Secure mount options in /etc/fstab
# tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev 0 0
# /dev/sda2 /home ext4 defaults,nosuid,nodev 0 2

# noexec - prevent execution of binaries
# nosuid - ignore SUID/SGID bits
# nodev  - prevent device file creation
```

```bash
# Filesystem security audit
# Find world-writable files
find / -xdev -perm -002 -type f 2>/dev/null

# Find SUID/SGID binaries
find / -xdev \( -perm -4000 -o -perm -2000 \) -type f 2>/dev/null

# Find files without owner
find / -xdev -nouser -o -nogroup 2>/dev/null

# Check /tmp permissions
ls -ld /tmp  # Should be drwxrwxrwt (sticky bit set)

# Immutable files (cannot be modified even by root)
chattr +i /etc/resolv.conf   # Set immutable
lsattr /etc/resolv.conf      # Check attributes
chattr -i /etc/resolv.conf   # Remove immutable
```

```bash
# Mounting and unmounting
mount /dev/sdb1 /mnt/data          # Mount device
mount -o ro /dev/sdb1 /mnt/data    # Mount read-only
umount /mnt/data                    # Unmount

# Check mounted filesystems
df -Th                              # Disk usage with filesystem type
mount | column -t                   # All mounts
findmnt                             # Tree view of mounts
```

## Gotchas

- Sticky bit on `/tmp` (the `t` in `drwxrwxrwt`) prevents users from deleting each other's files - if missing, any user can delete any file in `/tmp`
- Mounting `/tmp` as separate partition with `noexec` prevents exploit execution but some legitimate software (package managers) needs exec in `/tmp`
- `/proc/PID/environ` exposes environment variables of running processes - may contain secrets; restrict with `hidepid=2` mount option
- NFS mounts without `root_squash` allow remote root to have root access to shared files
- Symbolic link attacks in `/tmp` - attacker creates symlink to sensitive file, privileged process follows link and overwrites target
- `ext4` does not have built-in checksumming - silent data corruption possible; btrfs and ZFS provide checksums

## See Also

- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [CIS Benchmark - Filesystem Configuration](https://www.cisecurity.org/benchmark/distribution_independent_linux)
- [CWE-552 Files Accessible to External Parties](https://cwe.mitre.org/data/definitions/552.html)
