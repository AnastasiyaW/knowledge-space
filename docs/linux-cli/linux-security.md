---
title: Linux Security
category: concepts
tags: [linux-cli, security, dac, mac, selinux, namespaces, malware, pentesting]
---

# Linux Security

Linux provides multiple layers of security: from basic file permissions (DAC) to mandatory access control (MAC), process isolation (namespaces), and audit systems. This entry covers security mechanisms, common threats, reconnaissance techniques, and security testing tools.

## Security Mechanisms

| Mechanism | Description |
|-----------|-------------|
| **DAC** | Discretionary Access Control - file owner sets policy |
| **ACL** | Fine-grained per-user/group permissions |
| **Capabilities** | Specific elevated privileges without full root |
| **Namespaces** | Isolate PIDs, hostnames, UIDs, networks, FS - foundation of containers |
| **MAC** | Mandatory Access Control - centralized, even owner can't override (SELinux, AppArmor) |
| **Seccomp** | Restrict process to only needed syscalls |
| **Audit** | Log all security-relevant events |
| **Integrity** | Verify system file integrity via hashes |

### LSM (Linux Security Modules) API

Provides the framework for all security mechanisms to communicate with the kernel. Implementations: SELinux, AppArmor, Smack.

## System Reconnaissance

Commands an attacker (or admin auditing) would use:

```bash
hostname                          # machine name
uname -a                          # kernel version and distro
cat /etc/*-release                # distribution info
cat /etc/passwd                   # user list
ps aux                            # running processes
systemctl list-units --state=running  # running services
```

Information gathered: kernel CVEs, user accounts for password attacks, service purposes, privilege escalation paths.

## Privilege Escalation

Most exploits target kernel vulnerabilities for maximum privileges.

```bash
uname -a              # kernel version
cat /etc/*-release    # distro info
```

Exploit sources: exploit-db.com, cvedetails.com, packetstormsecurity.org, cve.mitre.org

### Transferring Exploits with netcat

```bash
# Receiver (target):
nc -l -p 1234 > exploit_file

# Sender:
nc <target_ip> 1234 < exploit_file
```

## Malware Types

| Type | Description |
|------|-------------|
| **Virus** | Self-replicates by injecting into other programs |
| **Trojan** | Disguised malware, no self-propagation (includes ransomware) |
| **Rootkit** | Hides malware at deep system level |
| **Backdoor** | Persistent remote access |
| **Botnet** | Network of infected devices under remote control |
| **Exploit** | Code targeting specific vulnerability |

## chroot

Changes apparent root directory for a process.

```bash
# Rescue mode example
mount /dev/sda1 /mnt
mount -o bind /dev /mnt/dev
mount -o bind /proc /mnt/proc
mount -o bind /sys /mnt/sys
chroot /mnt /bin/bash
# Now inside broken system - repair bootloader, reset passwords
exit
umount /mnt/{dev,proc,sys}
umount /mnt
```

Warning: chroot is NOT a security boundary on its own.

## Security Testing Tools

| Tool | Purpose |
|------|---------|
| **Metasploit** | Vulnerability testing and exploitation framework |
| **Nmap** | Network scanning and inventory |
| **Wireshark** | Packet inspection |
| **Nikto** | Web server vulnerability scanner |
| **SQLmap** | Database security testing |
| **OWASP ZAP** | Web application security |
| **John the Ripper** | Offline password cracking |
| **Hydra** | Online brute-force authentication |
| **Maltego** | OSINT and link analysis |

### John the Ripper

```bash
john /etc/shadow                    # crack shadow file
john --wordlist=wordlist.txt hash   # dictionary attack
john --show /etc/shadow             # show cracked
```

### Hydra

```bash
hydra -l admin -P wordlist.txt ssh://192.168.1.10
hydra -L users.txt -P pass.txt ftp://192.168.1.10
```

### Nikto

```bash
nikto -h <IP_or_hostname>
nikto -h <hostname> -ssl           # HTTPS
nikto -h <IP> -Format msf+        # export for Metasploit
```

## Security Distros

| Distro | Base | Focus |
|--------|------|-------|
| **Kali Linux** | Debian | General pentesting |
| **Parrot OS** | Debian | Cloud, anonymity, crypto |
| **BlackArch** | Arch | Huge tool repository |
| **BackBox** | Ubuntu | Minimal pentesting |

## Attack Stages

1. **Reconnaissance** - gather system information
2. **Scanning** - identify services, versions, vulnerabilities
3. **Gaining access** - exploit vulnerabilities
4. **Maintaining access** - backdoors, new users
5. **Covering tracks** - clean/corrupt logs

## Gotchas

- "Linux is inherently secure" is a myth - security requires proper configuration
- Linux malware exists - especially targeting servers, IoT, cloud
- chroot can be escaped by a root process - not suitable as sole isolation
- Running services as root increases attack surface - use dedicated service accounts
- Kernel exploits give highest privileges - keep kernel updated
- Namespaces (containers) provide better isolation than chroot but are not VMs

## See Also

- [[file-permissions]] - DAC, ACL, special bits
- [[users-and-groups]] - Account management, sudo
- [[firewall-and-iptables]] - Network security
- [[ssh-remote-access]] - Remote access hardening
- [[logging-and-journald]] - auditd, security logging
