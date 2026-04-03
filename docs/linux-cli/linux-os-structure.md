---
title: Linux OS Structure
category: concepts
tags: [linux-cli, kernel, userspace, sockets, architecture]
---

# Linux OS Structure

Linux architecture separates kernel space from user space, uses files as universal abstractions, and provides IPC mechanisms including sockets and pipes. This entry covers the two-layer model, file type details, and inter-process communication.

## Kernel Space vs User Space

- **Kernel space** - privileged memory for kernel processes (drivers, FS drivers). Full hardware access.
- **User space** - lower-priority memory for user-launched processes.
- **System calls** - the interface between user programs and kernel services.

## Users in Linux

A "user" is an account - not always human. System services run as dedicated users.

| Type | UID Range | Examples |
|------|-----------|---------|
| Superuser | 0 | root |
| System users | 1-99 | daemon, sshd, www-data |
| Regular users | 1000+ | Human accounts |

User info stored in: `/etc/passwd`, `/etc/shadow`, `/etc/group`

## File Types (Detailed)

| Type | Marker | Description |
|------|--------|-------------|
| Regular file | `-` | Data, text, binaries, scripts, images |
| Directory | `d` | Filename-to-inode mappings |
| Symbolic link | `l` | Path reference to another file |
| Block device | `b` | Random-access hardware (HDD, SSD, USB) |
| Character device | `c` | Sequential access (terminal, keyboard) |
| Named pipe | `p` | Unidirectional IPC |
| Socket | `s` | Bidirectional IPC |

### ls -l Output

```
-rwxr-xr-- 1 user group 4096 Jan 15 10:30 filename
^          ^ ^    ^     ^    ^             ^
type+perms links owner group size  date   name
```

## Sockets

Bidirectional IPC mechanism - same machine or over network.

| Type | Protocol | Description |
|------|----------|-------------|
| Stream | TCP | Reliable, ordered byte stream |
| Datagram | UDP | Unreliable, unordered messages |
| Sequential packet | - | Reliable fixed-length datagrams |
| Raw | Various | Direct protocol access |

### Socket Domains

- **Unix domain** - IPC on same machine (fast, no network overhead)
- **Internet domain** - network communication (IPv4/IPv6)

"Cannot open socket" error usually means insufficient permissions - may need `sudo` or specific capabilities.

## Device Files

Application -> device file -> kernel driver -> physical device

Device files in `/dev/` are created by `udev` at boot:
- Block devices (`b`): data in fixed-size blocks, random access (HDD, SSD)
- Character devices (`c`): sequential byte stream (terminal, keyboard)

Redirecting to device files sends data directly: `cat doc.txt > /dev/lp0` (print)

## Filesystem Hierarchy (Quick Reference)

```
/bin      Essential user binaries (available in single-user mode)
/sbin     System admin binaries (iptables, reboot, fdisk)
/etc      Configuration files
/dev      Device files
/proc     Process info (virtual FS)
/var      Variable data (logs, caches, mail)
/tmp      Temporary files (cleared on reboot)
/usr      User applications and libraries
/home     User home directories
/root     Root user's home
/boot     Kernel and bootloader
/opt      Optional software
/mnt      Manual mount point
/media    Auto-mounted removable media
/sys      Kernel device/driver info (virtual FS)
```

## Security Mechanisms Overview

| Mechanism | Purpose |
|-----------|---------|
| **DAC** | File owner controls access |
| **ACL** | Per-user/group fine-grained permissions |
| **Capabilities** | Specific privileges without full root |
| **Namespaces** | Resource isolation (PIDs, network, FS) - container foundation |
| **MAC** (SELinux, AppArmor) | Centralized mandatory policy |
| **Seccomp** | Restrict available syscalls |
| **Audit** | Security event logging |

## Gotchas

- `/proc` and `/sys` files appear to have size 0 but contain dynamic kernel data
- Block devices support random access; character devices are sequential only
- Unix domain sockets are faster than TCP for same-machine IPC (no network stack)
- Namespaces are the foundation of Docker containers - not a new concept, kernel-level
- Every running program is a process, even shell commands

## See Also

- [[linux-kernel-and-boot]] - Kernel architecture, modules, boot process
- [[filesystem-hierarchy]] - FHS directory standard
- [[linux-security]] - Security mechanisms in depth
- [[users-and-groups]] - User management
