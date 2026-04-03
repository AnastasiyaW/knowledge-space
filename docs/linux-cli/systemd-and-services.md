---
title: systemd and Services
category: reference
tags: [linux-cli, systemd, systemctl, services, daemons, init]
---

# systemd and Services

systemd is the standard init system on modern Linux, managing service lifecycle, boot process, and system state. This entry covers systemctl, unit files, journald integration, and boot analysis.

## Key Facts

- systemd is PID 1 on most modern distros (Ubuntu, Debian, Fedora, RHEL)
- Three main components: systemd (manager), systemctl (CLI), systemd-analyze (diagnostics)
- Unit files define services, timers, mounts, and other managed objects
- Services (daemons) run in the background, typically starting at boot

## systemctl Commands

```bash
systemctl start <service>       # start service
systemctl stop <service>        # stop service
systemctl restart <service>     # stop + start
systemctl reload <service>      # reload config without restart
systemctl status <service>      # show status and recent logs
systemctl enable <service>      # enable autostart at boot
systemctl disable <service>     # disable autostart
systemctl is-active <service>   # check if running
systemctl is-enabled <service>  # check if enabled at boot
systemctl list-units --type=service  # list all services
systemctl list-units --state=running # only running
systemctl --failed              # list failed services
sudo systemctl daemon-reload    # reload unit files after changes
```

## Unit Files

Located in:
- `/lib/systemd/system/` - package-provided units
- `/etc/systemd/system/` - admin-managed units (higher priority, overrides)

## Init Systems History

| System | Description |
|--------|-------------|
| **SysV Init** | Classic sequential, uses runlevels |
| **Upstart** | Event-based, parallel loading (Canonical) |
| **systemd** | Current standard: parallel, dependency-based |

## Boot Analysis

```bash
systemd-analyze                    # total boot time
systemd-analyze blame              # time per service
systemd-analyze critical-chain     # critical path
systemd-analyze plot > boot.svg    # visual boot timeline
```

## Hardware Inspection

```bash
lspci                    # PCI devices (GPU, NIC, etc.)
lspci -v                 # verbose
lspci -v | grep Kernel   # show loaded drivers
lsusb                    # USB devices
lsusb -t                 # tree view
lscpu                    # CPU information
lsscsi                   # SCSI/SATA devices
lshw                     # all hardware (needs install)
lshw --class network     # filter by class
```

## Kernel Modules

```bash
lsmod                        # list loaded modules
modinfo <module>             # module details
sudo modprobe <module>       # load module (resolves deps)
sudo modprobe -r <module>    # remove module
sudo insmod /path/module.ko  # load from file (no dep resolution)
sudo rmmod <module>          # remove module
cat /proc/modules            # loaded modules info
```

## Key Config Files in /etc

| File | Purpose |
|------|---------|
| `/etc/hostname` | System hostname |
| `/etc/hosts` | IP-to-hostname mapping |
| `/etc/fstab` | Filesystem mount config |
| `/etc/environment` | Global environment variables |
| `/etc/bash.bashrc` | Global bash init |
| `/etc/crontab` | System cron config |

## Gotchas

- Always run `daemon-reload` after editing unit files
- `enable` creates symlinks for boot; it does not start the service - use `enable --now` for both
- `reload` only works if the service supports it; `restart` always works but drops connections
- Some services need `systemctl reload-or-restart` for safe updates
- Non-systemd distros still exist (Alpine, Void, Artix) - use their native init

## See Also

- [[process-management]] - ps, top, kill, signals
- [[logging-and-journald]] - journalctl for service logs
- [[linux-kernel-and-boot]] - Boot sequence, GRUB, kernel
- [[cron-and-scheduling]] - Task scheduling
