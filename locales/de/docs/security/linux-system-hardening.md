---
title: "Linux-Systemhärtung"
category: techniques
tags: [security, linux, hardening, ssh, fail2ban, auditd, sysctl]
level: 4
source_sha256: 6bbc533a17e1fd3e0c46a38988c6ecb188b326e4f3d3373304fe787896b7d51e
translation: machine
translated_at: '2026-10-24'
---
# Linux-Systemhärtung {#linux-system-hardening}

Härtung der Linux-Sicherheit: Benutzerverwaltung, Dateiberechtigungen, SSH-Konfiguration, fail2ban, Firewall-Einrichtung, sysctl-Kernelparameter, auditd für die Systemüberwachung und Einhaltung der CIS-Benchmarks.

## Wichtige Fakten {#key-facts}
- SSH-Schlüsselauthentifizierung + deaktivierte Passwortauthentifizierung + nicht standardmäßiger Port + fail2ban = Basis-SSH-Sicherheit
- SetUID-Root-Binaries sind Ziele für Rechteausweitung - regelmäßig prüfen mit `find / -perm -4000`
- `auditd` bietet kernelbasierte Überwachung von Dateizugriffen, Systemaufrufen und Authentifizierungsereignissen
- ASLR (`kernel.randomize_va_space = 2`) ist unverzichtbar und sollte niemals deaktiviert werden
- AIDE (Dateiintegritätsüberwachung) erkennt unautorisierte Dateiänderungen
- CIS-Benchmarks bieten umfassende, branchenweit anerkannte Härtungsleitfäden

## Benutzerverwaltung {#user-management}
```bash
useradd -m -s /bin/bash username      # Create user
usermod -aG sudo username             # Add to sudo group
usermod -L username                    # Lock account
userdel -r username                    # Delete user + home
chage -M 90 username                  # Max password age 90 days
```

### /etc/passwd und /etc/shadow {#etcpasswd-and-etcshadow}
```markdown
# /etc/passwd: username:x:UID:GID:comment:home:shell
# /etc/shadow: username:$6$salt$hash:last_change:min:max:warn:inactive:expire
# Hash prefixes: $6$ = SHA-512, $5$ = SHA-256, $y$ = yescrypt
```

### Sudo-Härtung {#sudo-hardening}
```bash
visudo                                 # Always use visudo (syntax check)
# Secure patterns:
username ALL=(ALL) /usr/bin/systemctl restart nginx   # Limited command
%admin ALL=(ALL:ALL) ALL               # Group-based access

# DANGEROUS - avoid:
username ALL=(ALL) NOPASSWD: ALL       # No password for everything
```

## Dateiberechtigungen {#file-permissions}
```bash
chmod 755 file     # rwxr-xr-x (owner full, group/others read+execute)
chmod 600 file     # rw------- (owner only)
chown user:group file
```

### Spezialbits {#special-bits}
- **SetUID** (4000): `chmod u+s file` - läuft mit den Rechten des Dateieigentümers. Alle finden: `find / -perm -4000 -type f`
- **SetGID** (2000): `chmod g+s dir` - neue Dateien erben die Gruppe
- **Sticky Bit** (1000): `chmod +t /tmp` - nur der Dateieigentümer kann löschen

### ACLs {#acls}
```bash
getfacl file
setfacl -m u:username:rwx file
setfacl -m g:groupname:rx file
setfacl -x u:username file         # Remove
setfacl -b file                    # Remove all
```

## SSH-Härtung {#ssh-hardening}

### /etc/ssh/sshd_config {#etcsshsshd_config}
```kotlin
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

### Schlüsselerzeugung {#key-generation}
```bash
ssh-keygen -t ed25519 -C "comment"
ssh-copy-id user@server
```

### fail2ban {#fail2ban}
```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 2222
maxretry = 3
findtime = 600       # 10 min window
bantime = 3600       # 1 hour ban
```
Überwacht `auth.log` und sperrt IP-Adressen nach N fehlgeschlagenen Versuchen mithilfe von iptables-Regeln.

## Kernelparameter (sysctl) {#kernel-parameters-sysctl}
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

## Systemüberwachung {#system-auditing}

### auditd {#auditd}
```bash
apt install auditd
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
auditctl -a always,exit -F arch=b64 -S execve    # Log all command execution
ausearch -k passwd_changes                         # Search audit logs
aureport --auth                                     # Authentication report
```

### Log-Analyse {#log-analysis}
Wichtige Dateien in `/var/log/`:
- `auth.log` / `secure` - Authentifizierungsereignisse
- `syslog` / `messages` - allgemeine Systemmeldungen
- `kern.log` - Kernelmeldungen
- `faillog` - fehlgeschlagene Anmeldungen

### journald {#journald}
```bash
journalctl -u nginx                    # Logs for service
journalctl --since "1 hour ago"
journalctl -p err                      # Filter by priority
```

## Dateiintegritätsüberwachung (AIDE) {#file-integrity-monitoring-aide}
```bash
apt install aide
aideinit                    # Create baseline database
aide --check                # Check for changes
aide --update               # Update database after authorized changes
```

## Rootkit-Erkennung {#rootkit-detection}
```bash
chkrootkit                  # Scan for known rootkit signatures
rkhunter --check            # Rootkit hunter
```

## Highlights der CIS-Benchmarks {#cis-benchmark-highlights}
- `/tmp` mit `noexec,nodev,nosuid` einbinden
- Nicht benötigte Dienste deaktivieren
- Sicherstellen, dass `rsyslog` oder `journald` konfiguriert ist
- Auditing für Ereignisse der Rechteausweitung aktivieren
- Compiler auf Produktionsservern entfernen, sofern nicht benötigt
- USB-Speicher deaktivieren (`modprobe -r usb-storage`)

## Stolperfallen {#gotchas}
- Das Ändern des SSH-Ports allein ist Security by Obscurity - immer mit Schlüsselauthentifizierung + fail2ban kombinieren
- fail2ban kann DICH aussperren, wenn zu viele SSH-Verbindungen vom selben Host kommen - eigene IPs auf die Whitelist setzen
- `auditd` erzeugt auf stark ausgelasteten Systemen enorme Logmengen - Regeln sorgfältig abstimmen
- `chkrootkit` liefert auf manchen Distributionen Fehlalarme - Befunde manuell überprüfen
- Das Laden von Kernelmodulen (`modprobe`) kann zum Laden von Rootkits missbraucht werden - mit Secure Boot einschränken

## Siehe auch {#see-also}
- [[linux-os-fundamentals]] - Dateisystem, Prozesse, Kernel
- [[firewall-and-ids-ips]] - iptables-Konfiguration
- [[privilege-escalation-techniques]] - was die Härtung verhindert
- [[siem-and-incident-response]] - Log-Weiterleitung und Überwachung
