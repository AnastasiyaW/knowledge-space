---
title: "Linux-Betriebssystemstruktur"
category: concepts
tags: [linux-cli, kernel, userspace, sockets, architecture]
level: 3
source_sha256: f107469349406f512257c33ace4936f764d989351b34a1f77b15ae81f9c9b09a
translation: machine
translated_at: '2026-10-24'
---
# Linux-Betriebssystemstruktur {#linux-os-structure}

Die Linux-Architektur trennt den Kernel-Space vom User-Space, verwendet Dateien als universelle Abstraktionen und stellt IPC-Mechanismen bereit, darunter Sockets und Pipes. Dieser Eintrag behandelt das Zwei-Schichten-Modell, Details zu Dateitypen und die Interprozesskommunikation.

## Kernel-Space vs. User-Space {#kernel-space-vs-user-space}

- **Kernel-Space** - privilegierter Speicher für Kernel-Prozesse (Treiber, Dateisystemtreiber). Voller Hardwarezugriff.
- **User-Space** - Speicher mit niedrigerer Priorität für vom Benutzer gestartete Prozesse.
- **Systemaufrufe** - die Schnittstelle zwischen Benutzerprogrammen und Kernel-Diensten.

## Benutzer in Linux {#users-in-linux}

Ein „Benutzer" ist ein Konto - nicht immer ein Mensch. Systemdienste laufen unter eigenen Benutzern.

| Typ | UID-Bereich | Beispiele |
|------|-----------|---------|
| Superuser | 0 | root |
| Systembenutzer | 1-99 | daemon, sshd, www-data |
| Reguläre Benutzer | 1000+ | Menschliche Konten |

Benutzerinformationen gespeichert in: `/etc/passwd`, `/etc/shadow`, `/etc/group`

## Dateitypen (Detailliert) {#file-types-detailed}

| Typ | Kennzeichen | Beschreibung |
|------|-----------|-------------|
| Reguläre Datei | `-` | Daten, Text, Binärdateien, Skripte, Bilder |
| Verzeichnis | `d` | Zuordnungen von Dateinamen zu Inodes |
| Symbolischer Link | `l` | Pfadverweis auf eine andere Datei |
| Blockgerät | `b` | Wahlfreier Zugriff auf Hardware (HDD, SSD, USB) |
| Zeichengerät | `c` | Sequenzieller Zugriff (Terminal, Tastatur) |
| Named Pipe | `p` | Unidirektionale IPC |
| Socket | `s` | Bidirektionale IPC |

### ls -l Ausgabe {#ls-l-output}

```text
-rwxr-xr-- 1 user group 4096 Jan 15 10:30 filename
^          ^ ^    ^     ^    ^             ^
type+perms links owner group size  date   name
```

## Sockets {#sockets}

Bidirektionaler IPC-Mechanismus - auf derselben Maschine oder über das Netzwerk.

| Typ | Protokoll | Beschreibung |
|------|----------|-------------|
| Stream | TCP | Zuverlässiger, geordneter Byte-Strom |
| Datagram | UDP | Unzuverlässige, ungeordnete Nachrichten |
| Sequential Packet | - | Zuverlässige Datagramme fester Länge |
| Raw | Verschiedene | Direkter Protokollzugriff |

### Socket-Domänen {#socket-domains}

- **Unix-Domäne** - IPC auf derselben Maschine (schnell, kein Netzwerk-Overhead)
- **Internet-Domäne** - Netzwerkkommunikation (IPv4/IPv6)

Die Fehlermeldung „Cannot open socket" bedeutet meist unzureichende Berechtigungen - eventuell wird `sudo` oder eine bestimmte Capability benötigt.

## Gerätedateien {#device-files}

Anwendung -> Gerätedatei -> Kernel-Treiber -> physisches Gerät

Gerätedateien in `/dev/` werden beim Booten von `udev` erstellt:
- Blockgeräte (`b`): Daten in Blöcken fester Größe, wahlfreier Zugriff (HDD, SSD)
- Zeichengeräte (`c`): sequenzieller Byte-Strom (Terminal, Tastatur)

Umleitung auf Gerätedateien sendet Daten direkt: `cat doc.txt > /dev/lp0` (Drucken)

## Dateisystemhierarchie (Kurzreferenz) {#filesystem-hierarchy-quick-reference}

```javascript
/bin      Essential user binaries (available in single-user mode)
/sbin     System admin binaries (iptables, reboot, fdisk)
/etc      Configuration files
/dev      Device files
/proc     Process info (virtual FS)
/var      Variable data (logs, caches, mail)
/tmp      Temporary files (cleared on reboot)
/usr      User applications and libraries
/home     User home directories
/root     Root user's home
/boot     Kernel and bootloader
/opt      Optional software
/mnt      Manual mount point
/media    Auto-mounted removable media
/sys      Kernel device/driver info (virtual FS)
```

## Übersicht der Sicherheitsmechanismen {#security-mechanisms-overview}

| Mechanismus | Zweck |
|-----------|---------|
| **DAC** | Der Dateibesitzer steuert den Zugriff |
| **ACL** | Feingranulare Berechtigungen pro Benutzer/Gruppe |
| **Capabilities** | Bestimmte Privilegien ohne vollständiges Root |
| **Namespaces** | Ressourcenisolation (PIDs, Netzwerk, Dateisystem) - Grundlage für Container |
| **MAC** (SELinux, AppArmor) | Zentrale verpflichtende Richtlinie |
| **Seccomp** | Verfügbare Systemaufrufe einschränken |
| **Audit** | Protokollierung von Sicherheitsereignissen |

## Stolperfallen {#gotchas}

- `/proc`- und `/sys`-Dateien erscheinen mit Größe 0, enthalten aber dynamische Kerneldaten
- Blockgeräte unterstützen wahlfreien Zugriff; Zeichengeräte nur sequenziell
- Unix-Domain-Sockets sind für IPC auf derselben Maschine schneller als TCP (kein Netzwerk-Stack)
- Namespaces sind die Grundlage von Docker-Containern - kein neues Konzept, sondern auf Kernel-Ebene
- Jedes laufende Programm ist ein Prozess, auch Shell-Befehle

## Siehe auch {#see-also}

- [[linux-kernel-and-boot]] - Kernel-Architektur, Module, Bootvorgang
- [[filesystem-hierarchy]] - FHS-Verzeichnisstandard
- [[linux-security]] - Sicherheitsmechanismen im Detail
- [[users-and-groups]] - Benutzerverwaltung
