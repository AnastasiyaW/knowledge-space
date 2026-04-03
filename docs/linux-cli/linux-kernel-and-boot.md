---
title: Linux Kernel and Boot Process
category: concepts
tags: [linux-cli, kernel, boot, grub, init, modules, memory]
---

# Linux Kernel and Boot Process

The kernel is the core of the operating system, mediating between hardware and user programs. This entry covers kernel architecture, modules, the boot sequence, memory management, and init systems.

## Key Facts

- Linux uses a **modular kernel** - modules load/unload without reboot
- Technically, "Linux" is the kernel; the OS = GNU programs + Linux kernel
- LTS kernel versions receive extended maintenance
- systemd is PID 1 on modern distros

## Kernel Functions

1. **Device support** - USB, webcams, input devices
2. **Data storage** - RAM management, persistent storage, virtual FS
3. **Network access** - physical and virtual networking
4. **Task scheduling** - CPU time sharing, priorities
5. **Security** - file permissions, resource access control

## Kernel Version

Format: `A.B.C[.D]` (e.g., `5.4.20`, `6.1.52`)

```bash
uname -r          # kernel version only
uname -a          # all system info
uname -v          # version and build info
```

## Kernel Space vs User Space

- **Kernel space** - privileged, direct hardware access (drivers, FS)
- **User space** - restricted, user programs
- Communication via **system calls**

## Boot Sequence

1. **BIOS/UEFI** - hardware init, POST
2. **Partition table** - find bootable device
3. **GRUB bootloader** - loaded from boot sector
4. **Kernel** - GRUB loads `vmlinuz` from `/boot`
5. **initrd/initramfs** - temporary root FS for early boot
6. **systemd (PID 1)** - starts all services

### GRUB Configuration

```bash
# User config (edit this)
/etc/default/grub

# Generated config (do NOT edit directly)
/boot/grub/grub.cfg

# Regenerate after editing
sudo update-grub                    # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL
```

### /boot Contents

- `vmlinuz` - compressed kernel image
- `initrd.img` - initial RAM disk
- `/boot/grub/` - bootloader files

## Kernel Modules

```bash
lsmod                        # list loaded modules
modinfo <module>             # detailed info
sudo modprobe <module>       # load (resolves dependencies)
sudo modprobe -r <module>    # remove
sudo insmod /path/module.ko  # load from file (no deps)
sudo rmmod <module>          # remove
cat /proc/modules            # module info file
```

## Init Systems

| System | Description |
|--------|-------------|
| **SysV Init** | Classic sequential, runlevels |
| **Upstart** | Event-based, parallel (Canonical) |
| **systemd** | Current standard, parallel, dependency-based |

## Memory Management

### Virtual Memory

- Memory page = 4 KB
- Kernel allocates on process request
- LRU (Least Recently Used) cache eviction

### Swap

Extends virtual memory beyond physical RAM.

- Can be partition or file
- Attach/detach at runtime
- Used for hibernation state

### OOM Killer

When RAM exhausted: OOM Killer terminates processes to free memory. Each process has an **OOM score** (higher = more likely to be killed).

## Process Creation

1. Name assigned
2. Added to process list
3. Priority determined
4. Process control block (PCB) formed
5. Resources allocated

## Signals

| Signal | Number | Description |
|--------|--------|-------------|
| SIGHUP | 1 | Hangup / reload |
| SIGINT | 2 | Interrupt (Ctrl+C) |
| SIGKILL | 9 | Force kill |
| SIGTERM | 15 | Graceful terminate |
| SIGSTOP | 19 | Pause (Ctrl+Z) |

```bash
kill -l                    # list all signals
kill -9 PID                # SIGKILL
kill -15 PID               # SIGTERM (default)
killall process            # kill by name
```

## Boot Analysis

```bash
systemd-analyze                    # total boot time
systemd-analyze blame              # time per service
systemd-analyze critical-chain     # boot critical path
systemd-analyze plot > boot.svg    # visual timeline
```

## Gotchas

- Verify module stability before loading in production
- `insmod` does not resolve dependencies; `modprobe` does
- Editing `/boot/grub/grub.cfg` directly is overwritten by `update-grub`
- OOM Killer selection is not always predictable - critical services can be killed
- Swap on SSD causes write wear; swap on HDD causes latency

## See Also

- [[systemd-and-services]] - systemctl, service lifecycle
- [[disks-and-filesystems]] - Boot partition, LUKS, fstab
- [[process-management]] - Process states, signals, kill
- [[monitoring-and-performance]] - Memory and load monitoring
