---
title: Linux Kernel Architecture and Security
category: system-security
tags: [linux, kernel, kernel-space, user-space, syscalls, modules, security]
---

# Linux Kernel Architecture and Security

## Key Facts

- Linux kernel operates in privileged mode (ring 0) - full hardware access; user processes run in ring 3 with restricted access
- System calls (syscalls) are the ONLY legitimate way for user-space programs to request kernel services
- Linux uses a modular monolithic kernel - core functionality in kernel space, loadable modules for drivers and features
- Kernel modules can be loaded/unloaded at runtime without reboot: `insmod`, `modprobe`, `rmmod`
- Module types: device drivers, filesystem drivers, network protocol handlers, security modules (SELinux, AppArmor)
- [[linux-user-security]] manages access control in user space; kernel enforces it
- [[disk-encryption-lvm]] uses dm-crypt, a kernel-level subsystem

## Patterns

```bash
# Kernel information
uname -r            # Kernel version
uname -a            # Full system info
cat /proc/version   # Detailed kernel version

# Module management
lsmod               # List loaded modules
modinfo <module>    # Module details
modprobe <module>   # Load module with dependencies
rmmod <module>      # Unload module

# System call tracing
strace ls /tmp                    # Trace all syscalls
strace -e trace=network curl url  # Trace network syscalls only
strace -c command                 # Syscall statistics
```

```bash
# Kernel hardening (sysctl)
# /etc/sysctl.d/99-security.conf

# Disable IP forwarding (unless router)
net.ipv4.ip_forward = 0

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Enable SYN flood protection
net.ipv4.tcp_syncookies = 1

# Disable source routing
net.ipv4.conf.all.accept_source_route = 0

# Log martian packets
net.ipv4.conf.all.log_martians = 1

# Restrict kernel pointer exposure
kernel.kptr_restrict = 2

# Restrict dmesg access
kernel.dmesg_restrict = 1

# Apply: sysctl -p /etc/sysctl.d/99-security.conf
```

```bash
# Boot modes for recovery
# Edit GRUB at boot:
# - Add 'single' to kernel params: single-user mode (root shell, no network)
# - Add 'emergency': minimal shell, read-only filesystem
# - Add 'rescue': attempts to mount filesystems

# GRUB menu: press 'e' at boot, edit linux line, Ctrl+X to boot
```

## Gotchas

- Loadable kernel modules run with full kernel privileges - a malicious module can compromise the entire system
- Module signing (CONFIG_MODULE_SIG) prevents loading unsigned modules but is not enabled in all distributions
- `dmesg` can leak sensitive kernel information (memory addresses) - restrict with `kernel.dmesg_restrict = 1`
- Kernel version disclosure helps attackers identify known CVEs - minimize version exposure in production
- Monolithic kernel means a bug in any kernel code (including drivers) can crash the entire system
- `/proc` and `/sys` virtual filesystems expose kernel internals - restrict access in container environments

## See Also

- [NIST SP 800-123 Guide to General Server Security](https://csrc.nist.gov/publications/detail/sp/800-123/final)
- [Kernel Self Protection Project](https://kernsec.org/wiki/index.php/Kernel_Self_Protection_Project)
- [CIS Linux Benchmark](https://www.cisecurity.org/benchmark/distribution_independent_linux)
