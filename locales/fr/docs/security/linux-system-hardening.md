---
title: "Durcissement du système Linux"
category: techniques
tags: [security, linux, hardening, ssh, fail2ban, auditd, sysctl]
level: 4
source_sha256: 6bbc533a17e1fd3e0c46a38988c6ecb188b326e4f3d3373304fe787896b7d51e
translation: machine
translated_at: '2026-10-24'
---
# Durcissement du système Linux {#linux-system-hardening}

Durcissement de la sécurité Linux : gestion des utilisateurs, permissions de fichiers, configuration SSH, fail2ban, mise en place du pare-feu, paramètres du noyau sysctl, auditd pour l'audit système et conformité aux benchmarks CIS.

## Points clés {#key-facts}
- Authentification SSH par clé + authentification par mot de passe désactivée + port non standard + fail2ban = sécurité SSH de base
- Les binaires SetUID root sont des cibles d'élévation de privilèges - à auditer régulièrement avec `find / -perm -4000`
- `auditd` assure un audit au niveau du noyau des accès aux fichiers, des appels système et des événements d'authentification
- ASLR (`kernel.randomize_va_space = 2`) est indispensable et ne doit jamais être désactivé
- AIDE (surveillance de l'intégrité des fichiers) détecte les modifications non autorisées de fichiers
- Les benchmarks CIS fournissent des guides de durcissement complets et reconnus par l'industrie

## Gestion des utilisateurs {#user-management}
```bash
useradd -m -s /bin/bash username      # Create user
usermod -aG sudo username             # Add to sudo group
usermod -L username                    # Lock account
userdel -r username                    # Delete user + home
chage -M 90 username                  # Max password age 90 days
```

### /etc/passwd et /etc/shadow {#etcpasswd-and-etcshadow}
```markdown
# /etc/passwd: username:x:UID:GID:comment:home:shell
# /etc/shadow: username:$6$salt$hash:last_change:min:max:warn:inactive:expire
# Hash prefixes: $6$ = SHA-512, $5$ = SHA-256, $y$ = yescrypt
```

### Durcissement de sudo {#sudo-hardening}
```bash
visudo                                 # Always use visudo (syntax check)
# Secure patterns:
username ALL=(ALL) /usr/bin/systemctl restart nginx   # Limited command
%admin ALL=(ALL:ALL) ALL               # Group-based access

# DANGEROUS - avoid:
username ALL=(ALL) NOPASSWD: ALL       # No password for everything
```

## Permissions de fichiers {#file-permissions}
```bash
chmod 755 file     # rwxr-xr-x (owner full, group/others read+execute)
chmod 600 file     # rw------- (owner only)
chown user:group file
```

### Bits spéciaux {#special-bits}
- **SetUID** (4000) : `chmod u+s file` - s'exécute avec les droits du propriétaire du fichier. Tout trouver : `find / -perm -4000 -type f`
- **SetGID** (2000) : `chmod g+s dir` - les nouveaux fichiers héritent du groupe
- **Sticky bit** (1000) : `chmod +t /tmp` - seul le propriétaire du fichier peut le supprimer

### ACL {#acls}
```bash
getfacl file
setfacl -m u:username:rwx file
setfacl -m g:groupname:rx file
setfacl -x u:username file         # Remove
setfacl -b file                    # Remove all
```

## Durcissement SSH {#ssh-hardening}

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

### Génération de clés {#key-generation}
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
Surveille `auth.log` et bannit les IP après N tentatives échouées au moyen de règles iptables.

## Paramètres du noyau (sysctl) {#kernel-parameters-sysctl}
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

## Audit système {#system-auditing}

### auditd {#auditd}
```bash
apt install auditd
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
auditctl -a always,exit -F arch=b64 -S execve    # Log all command execution
ausearch -k passwd_changes                         # Search audit logs
aureport --auth                                     # Authentication report
```

### Analyse des journaux {#log-analysis}
Fichiers clés dans `/var/log/` :
- `auth.log` / `secure` - événements d'authentification
- `syslog` / `messages` - messages système généraux
- `kern.log` - messages du noyau
- `faillog` - connexions échouées

### journald {#journald}
```bash
journalctl -u nginx                    # Logs for service
journalctl --since "1 hour ago"
journalctl -p err                      # Filter by priority
```

## Surveillance de l'intégrité des fichiers (AIDE) {#file-integrity-monitoring-aide}
```bash
apt install aide
aideinit                    # Create baseline database
aide --check                # Check for changes
aide --update               # Update database after authorized changes
```

## Détection de rootkits {#rootkit-detection}
```bash
chkrootkit                  # Scan for known rootkit signatures
rkhunter --check            # Rootkit hunter
```

## Points saillants des benchmarks CIS {#cis-benchmark-highlights}
- Monter `/tmp` avec `noexec,nodev,nosuid`
- Désactiver les services inutiles
- S'assurer que `rsyslog` ou `journald` est configuré
- Activer l'audit des événements d'élévation de privilèges
- Supprimer les compilateurs des serveurs de production s'ils ne sont pas nécessaires
- Désactiver le stockage USB (`modprobe -r usb-storage`)

## Pièges à éviter {#gotchas}
- Changer le port SSH seul relève de la sécurité par l'obscurité - toujours le combiner avec l'authentification par clé + fail2ban
- fail2ban avec trop de connexions SSH depuis le même hôte peut VOUS verrouiller hors du système - ajoutez vos IP à la liste blanche
- `auditd` sur des systèmes chargés génère un volume de journaux considérable - réglez les règles avec soin
- `chkrootkit` produit des faux positifs sur certaines distributions - vérifiez les résultats manuellement
- Le chargement de modules noyau (`modprobe`) peut servir à charger des rootkits - restreignez-le avec Secure Boot

## Voir aussi {#see-also}
- [[linux-os-fundamentals]] - système de fichiers, processus, noyau
- [[firewall-and-ids-ips]] - configuration d'iptables
- [[privilege-escalation-techniques]] - ce que le durcissement empêche
- [[siem-and-incident-response]] - transfert et surveillance des journaux
