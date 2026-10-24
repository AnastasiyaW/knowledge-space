---
title: "Grundlagen des Linux-Betriebssystems für Sicherheit"
category: concepts
tags: [security, linux, filesystem, kernel, boot-process, disk-encryption]
level: 3
source_sha256: 8be16dab731ce6ff11c6e1f909a4899ed1dc70c0ecaf7d338329e24ab9a6575b
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen des Linux-Betriebssystems für Sicherheit {#linux-os-fundamentals-for-security}

Für die Sicherheit relevante Interna des Linux-Betriebssystems: Dateisystemhierarchie, Benutzermodell, Kernel- vs. Userspace, Bootprozess, Festplattenverschlüsselung (LUKS), Dateisysteminterna (Inodes), Gerateverwaltung und Paketverwaltung.

## Kernfakten {#key-facts}
- In Linux ist alles eine Datei (reguläre Dateien, Verzeichnisse, Geräte, Sockets, Pipes)
- Root (UID 0) hat uneingeschränkten Zugriff; Systembenutzer (1–999) betreiben Dienste; reguläre Benutzer (1000+)
- `/etc/shadow` speichert Passwort-Hashes (nur für root lesbar); `/etc/passwd` ist für alle lesbar
- LUKS bietet vollständige Festplattenverschlüsselung, beim Booten ist eine Passphrase erforderlich
- Der Kernel-Space hat direkten Hardwarezugriff; der Userspace greift nur über Systemaufrufe auf Hardware zu
- UEFI Secure Boot verhindert das Laden unsignierter Kernel oder Module

## Dateisystemhierarchie (FHS) {#filesystem-hierarchy-fhs}
```javascript
/bin     Essential user binaries
/sbin    System binaries (fdisk, iptables)
/etc     Configuration files
/home    User home directories
/root    Root's home
/var     Variable data (logs, databases)
/tmp     Temporary (cleared on reboot)
/usr     User programs and libraries
/dev     Device files
/proc    Virtual FS - process/kernel info
/sys     Virtual FS - hardware/driver info
/boot    Bootloader, kernel, initramfs
```

## Benutzermodell {#user-model}
- Format von `/etc/passwd`: `username:x:UID:GID:comment:home:shell`
- Format von `/etc/shadow`: `username:$hash:last_change:min:max:warn:inactive:expire`
- `/etc/group` - Definitionen der Gruppenmitgliedschaften
- Systembenutzer betreiben Dienste mit minimalen Rechten (www-data, mysql, nobody)

## Kernel-Architektur {#kernel-architecture}

### Userspace vs. Kernel-Space {#user-space-vs-kernel-space}
- **Kernel-Space** - privilegierter Modus, direkter Hardwarezugriff, Speicherverwaltung, Scheduling
- **Userspace** - unprivilegiert, hier laufen die Anwendungen
- **Systemaufrufe** - Schnittstelle zwischen den Bereichen (open, read, write, fork, exec, socket)

### Kernel-Module {#kernel-modules}
```bash
lsmod                    # List loaded modules
modprobe <module>        # Load module
rmmod <module>           # Remove module
modinfo <module>         # Module information
```
Sicherheitsrisiko: Als Kernel-Module geladene Rootkits können Prozesse, Dateien und Verbindungen verbergen.

## Bootprozess {#boot-process}
1. Stromversorgung -> BIOS/UEFI-POST
2. BIOS lädt MBR / UEFI liest die EFI-Partition
3. GRUB-Bootloader lädt Kernel + initramfs
4. Kernel initialisiert die Hardware und bindet das Root-Dateisystem ein
5. systemd (PID 1) startet Dienste im Userspace
6. Login-Aufforderung

### BIOS vs. UEFI {#bios-vs-uefi}
| Merkmal | BIOS | UEFI |
|---------|------|------|
| Bitbreite | 16-Bit | 32/64-Bit |
| Partitionierung | MBR (4 primäre, max. 2TB) | GPT (128 Partitionen, 9.4 ZB) |
| Sicherheit | Keine | Secure Boot |
| Bootgeschwindigkeit | Sequenziell | Parallel |

## Festplattenverschlüsselung (LUKS) {#disk-encryption-luks}
- Verschlüsselt eine gesamte Partition oder ein logisches Volume
- Beim Booten (noch vor dem Laden des Betriebssystems) ist eine Passphrase erforderlich
- Schlüsseldateien können auf einem separaten USB-Gerät liegen
- Standard für vollständige Festplattenverschlüsselung unter Linux

## Festplatten- und Dateisystemverwaltung {#disk-and-filesystem-management}
```bash
lsblk                          # List block devices
fdisk /dev/sda                 # MBR partition editor
gdisk /dev/sda                 # GPT partition editor
mkfs.ext4 /dev/sda1            # Format as ext4
mount /dev/sda1 /mnt           # Mount
umount /mnt                    # Unmount
fsck /dev/sda1                 # Check/repair (unmounted only!)
```
Dauerhafte Einbindungen: `/etc/fstab`.

## Inodes {#inodes}
Jede Datei hat einen Inode, der Folgendes enthält: Typ, Berechtigungen, Eigentümer, Größe, Zeitstempel, Zeiger auf Datenblöcke, Linkanzahl. Der Inode enthält NICHT den Dateinamen (dieser wird im Verzeichniseintrag gespeichert).
```bash
ls -i          # Show inode numbers
df -i          # Show inode usage
```

## Wiederherstellung gelöschter Dateien {#deleted-file-recovery}
Beim Löschen einer Datei wird der Inode als frei markiert, die Datenblöcke bleiben jedoch erhalten, bis sie überschrieben werden:
- **extundelete** - Wiederherstellung für ext3/ext4
- **testdisk / photorec** - Wiederherstellung für mehrere Dateisysteme
- Schnell handeln: Je mehr Plattenaktivität, desto mehr Daten werden überschrieben

## Paketverwaltung {#package-management}
```bash
# Debian/Ubuntu (APT)
apt update && apt upgrade
apt install <package>
dpkg -l                    # List installed
dpkg -S /path/to/file      # Find owning package

# Red Hat (RPM/DNF)
dnf install <package>
rpm -qa                    # List all installed
rpm -qf /path/to/file      # Find owning package
```

## Prozessverwaltung {#process-management}
```bash
ps aux                     # All processes
ps -ef --forest            # Process tree
top / htop                 # Interactive monitor
strace -p PID              # Trace system calls
kill PID / kill -9 PID    # Terminate
nice -n 10 command         # Adjusted priority
ss -tulnp                  # Listening sockets with process info
lsof -i :80               # Process using port 80
```

## Fallstricke {#gotchas}
- `/etc/passwd` ist absichtlich für alle lesbar – die Passwort-Hashes stehen in `/etc/shadow`
- `fsck` auf einem eingebundenen Dateisystem führt zu Datenkorruption
- Gelöschte Dateien sind wiederherstellbar, bis sie überschrieben werden – für sicheres Löschen `shred` verwenden
- Zombie-Prozesse (Status Z) sind keine Ressourcenlecks – sie enthalten lediglich einen nicht abgeholten Exit-Status
- `/proc` und `/sys` sind virtuell – sie existieren nur im Speicher, nicht auf der Festplatte

## Siehe auch {#see-also}
- [[linux-system-hardening]] - SSH, fail2ban, auditd, sysctl
- [[privilege-escalation-techniques]] - SUID, sudo, Kernel-Exploits
- [[network-security-and-protocols]] - Linux-Netzwerk
