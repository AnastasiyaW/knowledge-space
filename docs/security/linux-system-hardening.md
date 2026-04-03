---
title: Linux System Hardening
category: techniques
tags: [security, linux, hardening, ssh, fail2ban, auditd, sysctl]
---

# Linux System Hardening

Linux security hardening: user management, file permissions, SSH configuration, fail2ban, firewall setup, sysctl kernel parameters, auditd for system auditing, and CIS benchmark compliance.

## Key Facts
- SSH key-based auth + disabled password auth + non-default port + fail2ban = baseline SSH security
- SetUID root binaries are privilege escalation targets - audit regularly with `find / -perm -4000`
- `auditd` provides kernel-level auditing of file access, system calls, and authentication events
- ASLR (`kernel.randomize_va_space = 2`) is essential and should never be disabled
- AIDE (file integrity monitoring) detects unauthorized file modifications
- CIS Benchmarks provide comprehensive, industry-accepted hardening guides

## User Management
```bash
useradd -m -s /bin/bash username      # Create user
usermod -aG sudo username             # Add to sudo group
usermod -L username                    # Lock account
userdel -r username                    # Delete user + home
chage -M 90 username                  # Max password age 90 days
```

### /etc/passwd and /etc/shadow
```
# /etc/passwd: username:x:UID:GID:comment:home:shell
# /etc/shadow: username:$6$salt$hash:last_change:min:max:warn:inactive:expire
# Hash prefixes: $6$ = SHA-512, $5$ = SHA-256, $y$ = yescrypt
```

### Sudo Hardening
```bash
visudo                                 # Always use visudo (syntax check)
# Secure patterns:
username ALL=(ALL) /usr/bin/systemctl restart nginx   # Limited command
%admin ALL=(ALL:ALL) ALL               # Group-based access

# DANGEROUS - avoid:
username ALL=(ALL) NOPASSWD: ALL       # No password for everything
```

## File Permissions
```bash
chmod 755 file     # rwxr-xr-x (owner full, group/others read+execute)
chmod 600 file     # rw------- (owner only)
chown user:group file
```

### Special Bits
- **SetUID** (4000): `chmod u+s file` - runs as file owner. Find all: `find / -perm -4000 -type f`
- **SetGID** (2000): `chmod g+s dir` - new files inherit group
- **Sticky bit** (1000): `chmod +t /tmp` - only file owner can delete

### ACLs
```bash
getfacl file
setfacl -m u:username:rwx file
setfacl -m g:groupname:rx file
setfacl -x u:username file         # Remove
setfacl -b file                    # Remove all
```

## SSH Hardening

### /etc/ssh/sshd_config
```
Port 2222                      # Non-default port
PermitRootLogin no             # No root SSH
PasswordAuthentication no      # Key-only
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers user1 user2         # Whitelist
LoginGraceTime 30
ClientAliveInterval 300        # Disconnect idle
X11Forwarding no
```

### Key Generation
```bash
ssh-keygen -t ed25519 -C "comment"
ssh-copy-id user@server
```

### fail2ban
```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 2222
maxretry = 3
findtime = 600       # 10 min window
bantime = 3600       # 1 hour ban
```
Monitors `auth.log`, bans IPs after N failed attempts using iptables rules.

## Kernel Parameters (sysctl)
```bash
# /etc/sysctl.conf or /etc/sysctl.d/*.conf
net.ipv4.ip_forward = 0                    # Disable IP forwarding
net.ipv4.conf.all.accept_redirects = 0     # Ignore ICMP redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.tcp_syncookies = 1               # SYN flood protection
net.ipv4.conf.all.rp_filter = 1           # Reverse path filtering
net.ipv4.conf.all.log_martians = 1        # Log suspicious packets
kernel.randomize_va_space = 2              # ASLR (full randomization)
fs.suid_dumpable = 0                       # No core dumps for SUID

sysctl -p                                  # Apply changes
```

## System Auditing

### auditd
```bash
apt install auditd
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
auditctl -a always,exit -F arch=b64 -S execve    # Log all command execution
ausearch -k passwd_changes                         # Search audit logs
aureport --auth                                     # Authentication report
```

### Log Analysis
Key files in `/var/log/`:
- `auth.log` / `secure` - authentication events
- `syslog` / `messages` - general system messages
- `kern.log` - kernel messages
- `faillog` - failed logins

### journald
```bash
journalctl -u nginx                    # Logs for service
journalctl --since "1 hour ago"
journalctl -p err                      # Filter by priority
```

## File Integrity Monitoring (AIDE)
```bash
apt install aide
aideinit                    # Create baseline database
aide --check                # Check for changes
aide --update               # Update database after authorized changes
```

## Rootkit Detection
```bash
chkrootkit                  # Scan for known rootkit signatures
rkhunter --check            # Rootkit hunter
```

## CIS Benchmark Highlights
- Mount `/tmp` with `noexec,nodev,nosuid`
- Disable unnecessary services
- Ensure `rsyslog` or `journald` is configured
- Enable audit for privilege escalation events
- Remove compilers from production servers if not needed
- Disable USB storage (`modprobe -r usb-storage`)

## Gotchas
- Changing SSH port alone is security by obscurity - always combine with key auth + fail2ban
- fail2ban with too many SSH connections from the same host can lock YOU out - whitelist your IPs
- `auditd` on busy systems generates massive log volume - tune rules carefully
- `chkrootkit` has false positives on some distros - verify findings manually
- Kernel module loading (`modprobe`) can be used to load rootkits - restrict with Secure Boot

## See Also
- [[linux-os-fundamentals]] - filesystem, processes, kernel
- [[firewall-and-ids-ips]] - iptables configuration
- [[privilege-escalation-techniques]] - what hardening prevents
- [[siem-and-incident-response]] - log forwarding and monitoring
