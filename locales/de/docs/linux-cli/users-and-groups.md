---
title: "Benutzer und Gruppen"
category: reference
tags: [linux-cli, users, groups, sudo, su, passwd]
level: 3
source_sha256: b34886103428037ed20aa31117ff6884f4493d943056bb3a258f7857de901cd0
translation: machine
translated_at: '2026-10-24'
---
# Benutzer und Gruppen {#users-and-groups}

Linux ist ein Mehrbenutzersystem. Benutzer können menschliche Konten, Konten für Systemdienste oder der Superuser (root) sein. Gruppen fassen Benutzer für gemeinsame Berechtigungen zusammen. Dieser Eintrag behandelt die Benutzerverwaltung, die Authentifizierungsdateien und die Rechteerweiterung.

## Benutzertypen {#user-types}

| Typ | UID-Bereich | Beispiele |
|------|-----------|---------|
| Superuser (root) | 0 | Vollständiger Systemzugriff |
| Systembenutzer | 1-999 | daemon, sshd, www-data |
| Reguläre Benutzer | 1000+ | Menschliche Konten |

## Wichtige Dateien {#key-files}

| Datei | Zweck |
|------|---------|
| `/etc/passwd` | Benutzerkonten (für alle lesbar) |
| `/etc/shadow` | Passwort-Hashes (nur root) |
| `/etc/group` | Gruppendefinitionen |

### Format von /etc/passwd {#etcpasswd-format}

```text
username:x:UID:GID:GECOS:home_dir:shell
alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash
```

## Benutzerinformationen abfragen {#querying-user-info}

```bash
whoami              # current username
id                  # UID, GID, all groups
id username         # info for specific user
groups              # groups of current user
groups username     # groups of specific user
who                 # who is logged in
w                   # logged in + what they're doing
last                # login history
lastlog             # all users' last login dates
```

## Benutzer anlegen {#creating-users}

```bash
# useradd - low-level, minimal
sudo useradd username                     # no home, no password
sudo useradd -m username                  # with home directory
sudo useradd -m -s /bin/bash username     # with home + bash shell

# adduser - interactive wrapper (Debian/Ubuntu)
sudo adduser username                     # prompts for password, info

# Set password
sudo passwd username
```

## Benutzer ändern {#modifying-users}

```bash
sudo usermod -s /bin/bash user       # change shell
sudo usermod -d /new/home user       # change home directory
sudo usermod -l newname oldname      # rename user
sudo usermod -aG group user          # add to supplementary group (-a = APPEND)
sudo usermod -G g1,g2 user           # set supplementary groups (REPLACES existing)
sudo usermod -L user                 # lock account
sudo usermod -U user                 # unlock account
```

## Benutzer löschen {#deleting-users}

```bash
sudo userdel username           # delete user (keep home)
sudo userdel -r username        # delete user AND home directory
```

## Gruppenverwaltung {#group-management}

```bash
sudo groupadd groupname         # create group
sudo groupdel groupname         # delete group
sudo groupmod -n new old        # rename group
```

## Zwischen Benutzern wechseln {#switching-users}

### su (Substitute User) {#su-substitute-user}

```bash
su username             # switch (keeps current environment)
su - username           # switch with full login environment
su -                    # switch to root (full login)
sudo su                 # switch to root via sudo
```

### sudo (Superuser Do) {#sudo-superuser-do}

```bash
sudo command            # run as root
sudo -u username cmd    # run as specific user
sudo -i                 # interactive root shell
sudo -b command         # background execution
```

**su vs. sudo:**
- `su` erfordert das **Passwort des Zielbenutzers**; keine Protokollierung
- `sudo` erfordert **dein Passwort**; alle Aktionen werden protokolliert; benötigt die Konfiguration in `/etc/sudoers`

### visudo {#visudo}

```bash
sudo visudo             # safely edit /etc/sudoers (validates syntax)
```

sudo-Zugriff gewähren:
```bash
sudo usermod -aG sudo username    # Debian/Ubuntu
sudo usermod -aG wheel username   # RHEL/CentOS/Fedora
```

## Muster {#patterns}

### Benutzer mit vollständiger Einrichtung anlegen {#create-user-with-full-setup}

```bash
sudo useradd -m -s /bin/bash -G sudo newuser
sudo passwd newuser
```

### Alle echten Benutzer auflisten {#list-all-real-users}

```bash
awk -F: '$3 >= 1000 && $3 < 65534 {print $1}' /etc/passwd
```

## Fallstricke {#gotchas}

- `usermod -G` ohne `-a` **ersetzt** alle zusätzlichen Gruppen – verwende immer `-aG`, um Gruppen anzuhängen
- `useradd` legt standardmäßig kein Home-Verzeichnis an – verwende dafür das Flag `-m`
- Gesperrte Konten (`usermod -L`) erhalten ein `!`-Präfix im Passwort-Hash in `/etc/shadow`
- Das Root-Konto ist auf einigen Distributionen (Ubuntu) deaktiviert – verwende stattdessen `sudo`
- Das Löschen eines Benutzers beendet dessen laufende Prozesse nicht

## Siehe auch {#see-also}

- [[file-permissions]] - Berechtigungsmodell, chmod, ACLs
- [[ssh-remote-access]] - Schlüsselbasierte Authentifizierung
- [[linux-security]] - DAC, MAC, Capabilities
