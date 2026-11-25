---
title: "Dateiberechtigungen"
category: reference
tags: [linux-cli, permissions, chmod, chown, acl, security]
level: 3
source_sha256: 98cf21b2eebcd3749e552706e608081d620e5f7334504f9859d6fe68abf4670f
translation: machine
translated_at: '2026-10-24'
---
# Dateiberechtigungen {#file-permissions}

Jede Datei und jedes Verzeichnis in Linux hat einen Eigentümer, eine Gruppe und Berechtigungsbits für drei Kategorien: Eigentümer (u), Gruppe (g) und andere (o). Dieser Eintrag behandelt das Auslesen, Setzen und Erweitern von Berechtigungen.

## Wichtige Fakten {#key-facts}

- Drei Berechtigungstypen: Lesen (r=4), Schreiben (w=2), Ausführen (x=1)
- Neue Dateien erhalten standardmäßig 666 minus umask; Verzeichnisse 777 minus umask
- Nur root kann den Dateieigentümer ändern
- ACLs ermöglichen feingranulare Berechtigungen pro Benutzer bzw. pro Gruppe über das Basismodell hinaus

## Berechtigungen auslesen {#reading-permissions}

```bash
ls -l file.txt
# -rw-r--r-- 1 alice users 2048 May 10 14:30 file.txt
```

```typescript
- rw- r-- r--
| |   |   +-- others: read only
| |   +------ group: read only
| +---------- owner: read + write
+------------- type (- = file, d = dir, l = symlink)
```

| Symbol | Bei Dateien | Bei Verzeichnissen |
|--------|-------------|--------------------|
| `r` | Inhalt lesen | Inhalt auflisten |
| `w` | Datei ändern | Dateien darin anlegen/löschen |
| `x` | Als Programm ausführen | Betreten (cd) |

## chmod - Berechtigungen ändern {#chmod-change-permissions}

### Symbolische Notation {#symbolic-notation}

```bash
chmod u+x file          # add execute for owner
chmod g-w file          # remove write for group
chmod o+r file          # add read for others
chmod a+x file          # add execute for all
chmod u+rwx,g-w,o-r file  # multiple changes
chmod u=rwx,g=rx,o= file  # set exact permissions
chmod -R 755 dir/       # recursive
```

Kategorien: `u` = Eigentümer, `g` = Gruppe, `o` = andere, `a` = alle

### Oktale Notation {#octal-notation}

| Oktal | Symbolisch | Typische Verwendung |
|-------|------------|---------------------|
| 755 | rwxr-xr-x | Ausführbare Dateien, Verzeichnisse |
| 644 | rw-r--r-- | Reguläre Dateien |
| 600 | rw------- | Private Dateien (SSH-Schlüssel) |
| 700 | rwx------ | Private Verzeichnisse |
| 777 | rwxrwxrwx | Vollständig offen (vermeiden) |

```bash
chmod 644 file          # rw-r--r--
chmod 755 file          # rwxr-xr-x
chmod 700 file          # rwx------
```

## chown - Eigentümer ändern {#chown-change-owner}

```bash
sudo chown alice file              # change owner
sudo chown alice:devs file         # change owner and group
sudo chown :devs file              # change group only
sudo chown -R alice:devs dir/      # recursive
```

## chgrp - Gruppe ändern {#chgrp-change-group}

```bash
sudo chgrp groupname file
sudo chgrp -R groupname dir/
```

## Spezielle Berechtigungsbits {#special-permission-bits}

### SUID (Set User ID) - Bit 4 {#suid-set-user-id-bit-4}

Ausführbare Datei läuft mit der UID des **Eigentümers** der Datei, nicht mit der UID des Aufrufers.

```bash
chmod u+s file          # set SUID
chmod 4755 file         # octal
# ls -l shows: -rwsr-xr-x
```

Beispiel: `/usr/bin/passwd` hat SUID, damit jeder Benutzer sein Passwort ändern kann.

### SGID (Set Group ID) - Bit 2 {#sgid-set-group-id-bit-2}

Bei ausführbaren Dateien: Ausführung mit der Gruppe der Datei. Bei Verzeichnissen: Neue Dateien erben die Gruppe des Verzeichnisses.

```bash
chmod g+s dir/          # set SGID
chmod 2755 dir/         # octal
# ls -l shows: drwxr-sr-x
```

### Sticky Bit - Bit 1 {#sticky-bit-bit-1}

Bei Verzeichnissen: Benutzer können nur Dateien löschen, die ihnen gehören.

```bash
chmod +t dir/           # set sticky bit
chmod 1777 dir/         # octal
# ls -l shows: drwxrwxrwt
```

`/tmp` hat standardmäßig das Sticky Bit.

## umask - Standardberechtigungen {#umask-default-permissions}

Legt fest, welche Bits von den Standardberechtigungen **entfernt** werden.

```bash
umask              # show current umask
umask -S           # show in symbolic form
umask 022          # set umask
```

Bei umask 022 erhalten Dateien 644 (666-022), Verzeichnisse 755 (777-022).

## ACL - Zugriffskontrolllisten {#acl-access-control-lists}

Feingranulare Berechtigungen für einzelne Benutzer und Gruppen.

```bash
# View
getfacl file

# Set
setfacl -m u:alice:rw file          # give alice read+write
setfacl -m g:devs:r file            # give group read
setfacl -x u:alice file             # remove alice's ACL entry
setfacl -b file                     # remove all ACL entries
setfacl -d -m u:alice:rw dir/       # set default ACL (inherited by new files)
setfacl -R -m u:alice:rw dir/       # recursive
```

ACL-Typen: **Access-ACL** (direkt) und **Default-ACL** (wird von neuen Dateien in Verzeichnissen geerbt).

## chroot - Root-Verzeichnis ändern {#chroot-change-root}

Isoliert einen Prozess, indem dessen scheinbares Root-Verzeichnis geändert wird.

```bash
sudo chroot /new/root command
```

Anwendungsfälle: Trennung von Berechtigungen (Privilege Separation), Wiederherstellungsumgebungen, Honeypots. Allein stellt chroot keine vollständige Sicherheitsgrenze dar.

## Stolperfallen {#gotchas}

- `chmod 777` ist fast nie die richtige Lösung - ermitteln Sie die tatsächlich benötigte Berechtigung
- SUID auf Skripten wird von den meisten Kerneln aus Sicherheitsgründen ignoriert
- `chown` erfordert root, selbst wenn Ihnen die Datei gehört (verhindert UID-Spoofing)
- Das `+`-Kennzeichen in der Ausgabe von `ls -l` (z. B. `drwxr-xr-x+`) bedeutet, dass ACLs gesetzt sind
- umask gilt pro Sitzung - für Persistenz in `~/.bashrc` setzen
- Rekursives chmod auf `/` zerstört das System

## Siehe auch {#see-also}

- [[users-and-groups]] - Benutzerverwaltung und sudo
- [[linux-security]] - Übersicht der Sicherheitsmechanismen
- [[ssh-remote-access]] - Dateiberechtigungen für SSH-Schlüssel
