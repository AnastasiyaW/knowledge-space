---
title: Linux User Security and Access Control
category: system-security
tags: [linux, users, permissions, sudo, root, access-control, privilege-escalation]
---

# Linux User Security and Access Control

## Key Facts

- Linux user types: root (UID=0, full system access), system users (UID 1-100, service accounts like sshd, daemon), regular users (UID>100)
- User information stored in `/etc/passwd` (readable by all) and `/etc/shadow` (readable only by root - contains password hashes)
- `/etc/passwd` fields: username:x:UID:GID:full_name:home_dir:login_shell
- `sudo` grants temporary root privileges to authorized users listed in `/etc/sudoers` (edit with `visudo` only)
- Kernel space vs user space: kernel runs in privileged ring 0, user processes in ring 3 - system calls bridge the gap
- [[password-hashing]] in `/etc/shadow` uses `$id$salt$hash` format with configurable algorithms
- [[disk-encryption-lvm]] protects data at rest from physical access attacks

## Patterns

```bash
# User management
useradd -m -s /bin/bash -G sudo newuser  # Create user with home dir and sudo group
passwd newuser                            # Set password
usermod -aG docker newuser               # Add to group
userdel -r olduser                       # Remove user and home dir

# Check user info
id username          # UID, GID, groups
cat /etc/passwd      # All users
cat /etc/shadow      # Password hashes (root only)
getent passwd        # NSS-aware user listing

# Sudo configuration (/etc/sudoers via visudo)
# username ALL=(ALL:ALL) ALL           # Full sudo access
# %admin ALL=(ALL) ALL                 # Group-based sudo
# deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

```bash
# File permissions
chmod 640 /etc/shadow      # Owner read+write, group read, no other
chown root:shadow /etc/shadow
chmod u+s /usr/bin/passwd  # SetUID - runs as file owner (root)

# Find SUID binaries (potential privilege escalation)
find / -perm -4000 -type f 2>/dev/null

# Find world-writable files
find / -perm -002 -type f 2>/dev/null
```

```bash
# User space vs kernel space
# System call trace - see what a process asks the kernel
strace -c ls /tmp  # Summary of system calls
strace -e open,read cat /etc/passwd  # Filter specific calls
```

## Gotchas

- `/etc/passwd` is world-readable by design - passwords were moved to `/etc/shadow` long ago; the `x` in password field indicates shadow password
- SetUID on shell scripts is a security risk - most modern systems ignore SUID bit on interpreted scripts
- `sudo su` gives root shell but `sudo -i` is preferred - it properly initializes root environment
- System users (daemon, www-data) should have `/usr/sbin/nologin` as shell - prevents interactive login
- `/etc/sudoers` syntax error locks out sudo access - always use `visudo` which validates syntax before saving
- `root` can read all files regardless of permission bits - file permissions are NOT a defense against root compromise

## See Also

- [CWE-250 Execution with Unnecessary Privileges](https://cwe.mitre.org/data/definitions/250.html)
- [NIST SP 800-123 Guide to General Server Security](https://csrc.nist.gov/publications/detail/sp/800-123/final)
- [Linux man page: capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html)
