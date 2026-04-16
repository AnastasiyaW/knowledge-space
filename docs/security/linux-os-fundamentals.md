---
title: Linux OS Fundamentals for Security
category: concepts
tags: [security, linux, filesystem, kernel, boot-process, disk-encryption]
---

# Linux OS Fundamentals for Security

Linux operating system internals relevant to security: filesystem hierarchy, user model, kernel vs user space, boot process, disk encryption (LUKS), filesystem internals (inodes), device management, and package management.

## Key Facts
- Everything in Linux is a file (regular files, directories, devices, sockets, pipes)
- Root (UID 0) has unlimited access; system users (1-999) run services; regular users (1000+)
- `/etc/shadow` stores password hashes (root-readable only); `/etc/passwd` is world-readable
- LUKS provides full disk encryption with passphrase required at boot
- Kernel space has direct hardware access; user space accesses hardware only via system calls
- UEFI Secure Boot prevents unsigned kernel/module loading

## Filesystem Hierarchy (FHS)
```javascript
/bin     Essential user binaries
/sbin    System binaries (fdisk, iptables)
/etc     Configuration files
/home    User home directories
/root    Root's home
/var     Variable data (logs, databases)
/tmp     Temporary (cleared on reboot)
/usr     User programs and libraries
/dev     Device files
/proc    Virtual FS - process/kernel info
/sys     Virtual FS - hardware/driver info
/boot    Bootloader, kernel, initramfs
```

## User Model
- `/etc/passwd` format: `username:x:UID:GID:comment:home:shell`
- `/etc/shadow` format: `username:$hash:last_change:min:max:warn:inactive:expire`
- `/etc/group` - group membership definitions
- System users run services with minimal privileges (www-data, mysql, nobody)

## Kernel Architecture

### User Space vs Kernel Space
- **Kernel space** - privileged mode, direct hardware access, memory management, scheduling
- **User space** - unprivileged, applications run here
- **System calls** - interface between spaces (open, read, write, fork, exec, socket)

### Kernel Modules
```bash
lsmod                    # List loaded modules
modprobe <module>        # Load module
rmmod <module>           # Remove module
modinfo <module>         # Module information
```
Security risk: rootkits loaded as kernel modules can hide processes, files, connections.

## Boot Process
1. Power -> BIOS/UEFI POST
2. BIOS loads MBR / UEFI reads EFI partition
3. GRUB bootloader loads kernel + initramfs
4. Kernel initializes hardware, mounts root filesystem
5. systemd (PID 1) starts user-space services
6. Login prompt

### BIOS vs UEFI
| Feature | BIOS | UEFI |
|---------|------|------|
| Bit width | 16-bit | 32/64-bit |
| Partitioning | MBR (4 primary, 2TB max) | GPT (128 partitions, 9.4 ZB) |
| Security | None | Secure Boot |
| Boot speed | Sequential | Parallel |

## Disk Encryption (LUKS)
- Encrypts entire partition or logical volume
- Passphrase required at boot (before OS loads)
- Can use key files on separate USB device
- Standard for full-disk encryption on Linux

## Disk and Filesystem Management
```bash
lsblk                          # List block devices
fdisk /dev/sda                 # MBR partition editor
gdisk /dev/sda                 # GPT partition editor
mkfs.ext4 /dev/sda1            # Format as ext4
mount /dev/sda1 /mnt           # Mount
umount /mnt                    # Unmount
fsck /dev/sda1                 # Check/repair (unmounted only!)
```
Persistent mounts: `/etc/fstab`.

## Inodes
Every file has an inode containing: type, permissions, owner, size, timestamps, data block pointers, link count. Inode does NOT contain the filename (stored in directory entry).
```bash
ls -i          # Show inode numbers
df -i          # Show inode usage
```

## Deleted File Recovery
When a file is deleted, the inode is marked free but data blocks remain until overwritten:
- **extundelete** - ext3/ext4 recovery
- **testdisk / photorec** - multi-filesystem recovery
- Act fast: more disk activity = more data overwritten

## Package Management
```bash
# Debian/Ubuntu (APT)
apt update && apt upgrade
apt install <package>
dpkg -l                    # List installed
dpkg -S /path/to/file      # Find owning package

# Red Hat (RPM/DNF)
dnf install <package>
rpm -qa                    # List all installed
rpm -qf /path/to/file      # Find owning package
```

## Process Management
```bash
ps aux                     # All processes
ps -ef --forest            # Process tree
top / htop                 # Interactive monitor
strace -p PID              # Trace system calls
kill PID / kill -9 PID    # Terminate
nice -n 10 command         # Adjusted priority
ss -tulnp                  # Listening sockets with process info
lsof -i :80               # Process using port 80
```

## Gotchas
- `/etc/passwd` is world-readable by design - password hashes are in `/etc/shadow`
- `fsck` on a mounted filesystem causes data corruption
- Deleted files are recoverable until overwritten - use `shred` for secure deletion
- Zombie processes (state Z) are not resource leaks - they just have uncollected exit status
- `/proc` and `/sys` are virtual - they exist only in memory, not on disk

## See Also
- [[linux-system-hardening]] - SSH, fail2ban, auditd, sysctl
- [[privilege-escalation-techniques]] - SUID, sudo, kernel exploits
- [[network-security-and-protocols]] - Linux networking
