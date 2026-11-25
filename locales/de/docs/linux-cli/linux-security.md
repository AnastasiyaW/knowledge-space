---
title: "Linux-Sicherheit"
category: concepts
tags: [linux-cli, security, dac, mac, selinux, namespaces, malware, pentesting]
level: 4
source_sha256: fe7bac2638a03a9c90ee6a1adb69be58e9eb39b9a66bf3b830e5cd7d653e6b9c
translation: machine
translated_at: '2026-10-24'
---
# Linux-Sicherheit {#linux-security}

Linux bietet mehrere Sicherheitsebenen: von grundlegenden Dateiberechtigungen (DAC) über verpflichtende Zugriffskontrolle (MAC) und Prozessisolation (Namespaces) bis zu Audit-Systemen. Dieser Eintrag behandelt Sicherheitsmechanismen, gängige Bedrohungen, Reconnaissance-Techniken und Werkzeuge für Sicherheitstests.

## Sicherheitsmechanismen {#security-mechanisms}

| Mechanismus | Beschreibung |
|-------------|-------------|
| **DAC** | Discretionary Access Control: Der Dateieigentümer legt die Richtlinie fest |
| **ACL** | Feingranulare Berechtigungen pro Benutzer/Gruppe |
| **Capabilities** | Bestimmte erweiterte Privilegien ohne vollen Root-Zugriff |
| **Namespaces** | Isolieren PIDs, Hostnamen, UIDs, Netzwerke, Dateisysteme; Grundlage von Containern |
| **MAC** | Mandatory Access Control: zentral verwaltet, selbst der Eigentümer kann sie nicht überschreiben (SELinux, AppArmor) |
| **Seccomp** | Beschränkt einen Prozess auf die benötigten Syscalls |
| **Audit** | Protokolliert alle sicherheitsrelevanten Ereignisse |
| **Integrity** | Überprüft die Integrität von Systemdateien über Hashes |

### LSM (Linux Security Modules) API {#lsm-linux-security-modules-api}

Stellt das Framework bereit, über das alle Sicherheitsmechanismen mit dem Kernel kommunizieren. Implementierungen: SELinux, AppArmor, Smack.

## Systemaufklärung (Reconnaissance) {#system-reconnaissance}

Befehle, die ein Angreifer (oder ein Administrator bei einem Audit) verwendet:

```bash
hostname                          # machine name
uname -a                          # kernel version and distro
cat /etc/*-release                # distribution info
cat /etc/passwd                   # user list
ps aux                            # running processes
systemctl list-units --state=running  # running services
```

Gewonnene Informationen: Kernel-CVEs, Benutzerkonten für Passwortangriffe, Zweck von Diensten, Pfade zur Rechteerweiterung.

## Rechteerweiterung (Privilege Escalation) {#privilege-escalation}

Die meisten Exploits zielen auf Kernel-Schwachstellen ab, um maximale Privilegien zu erlangen.

```bash
uname -a              # kernel version
cat /etc/*-release    # distro info
```

Exploit-Quellen: exploit-db.com, cvedetails.com, packetstormsecurity.org, cve.mitre.org

### Exploits mit netcat übertragen {#transferring-exploits-with-netcat}

```bash
# Receiver (target):
nc -l -p 1234 > exploit_file

# Sender:
nc <target_ip> 1234 < exploit_file
```

## Malware-Typen {#malware-types}

| Typ | Beschreibung |
|-----|-------------|
| **Virus** | Repliziert sich selbst, indem er sich in andere Programme einschleust |
| **Trojaner** | Getarnte Malware, ohne eigene Verbreitung (umfasst Ransomware) |
| **Rootkit** | Verbirgt Malware auf tiefer Systemebene |
| **Backdoor** | Dauerhafter Fernzugriff |
| **Botnet** | Netzwerk infizierter Geräte unter Fernsteuerung |
| **Exploit** | Code, der eine bestimmte Schwachstelle ausnutzt |

## chroot {#chroot}

Ändert das scheinbare Root-Verzeichnis für einen Prozess.

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

Warnung: chroot ist allein KEINE Sicherheitsgrenze.

## Werkzeuge für Sicherheitstests {#security-testing-tools}

| Werkzeug | Zweck |
|----------|-------|
| **Metasploit** | Framework zum Testen und Ausnutzen von Schwachstellen |
| **Nmap** | Netzwerkscans und Bestandsaufnahme |
| **Wireshark** | Paketanalyse |
| **Nikto** | Scanner für Schwachstellen in Webservern |
| **SQLmap** | Tests der Datenbanksicherheit |
| **OWASP ZAP** | Sicherheit von Webanwendungen |
| **John the Ripper** | Offline-Passwortknacken |
| **Hydra** | Online-Brute-Force-Authentifizierung |
| **Maltego** | OSINT und Link-Analyse |

### John the Ripper {#john-the-ripper}

```bash
john /etc/shadow                    # crack shadow file
john --wordlist=wordlist.txt hash   # dictionary attack
john --show /etc/shadow             # show cracked
```

### Hydra {#hydra}

```bash
hydra -l admin -P wordlist.txt ssh://192.168.1.10
hydra -L users.txt -P pass.txt ftp://192.168.1.10
```

### Nikto {#nikto}

```bash
nikto -h <IP_or_hostname>
nikto -h <hostname> -ssl           # HTTPS
nikto -h <IP> -Format msf+        # export for Metasploit
```

## Sicherheits-Distributionen {#security-distros}

| Distribution | Basis | Schwerpunkt |
|--------------|-------|-------------|
| **Kali Linux** | Debian | Allgemeines Pentesting |
| **Parrot OS** | Debian | Cloud, Anonymität, Kryptografie |
| **BlackArch** | Arch | Umfangreiches Tool-Repository |
| **BackBox** | Ubuntu | Minimales Pentesting |

## Angriffsphasen {#attack-stages}

1. **Reconnaissance**: Systeminformationen sammeln
2. **Scanning**: Dienste, Versionen und Schwachstellen identifizieren
3. **Gaining access**: Schwachstellen ausnutzen
4. **Maintaining access**: Backdoors, neue Benutzer anlegen
5. **Covering tracks**: Logs bereinigen oder manipulieren

## Fallstricke {#gotchas}

- „Linux ist von Natur aus sicher“ ist ein Mythos: Sicherheit erfordert eine korrekte Konfiguration
- Linux-Malware existiert, insbesondere mit Ziel Server, IoT und Cloud
- chroot kann von einem Root-Prozess verlassen werden: nicht als alleinige Isolation geeignet
- Dienste als Root zu betreiben vergrößert die Angriffsfläche: dedizierte Dienstkonten verwenden
- Kernel-Exploits gewähren höchste Privilegien: Kernel stets aktuell halten
- Namespaces (Container) bieten bessere Isolation als chroot, sind aber keine VMs

## Siehe auch {#see-also}

- [[file-permissions]]: DAC, ACL, Sonderbits
- [[users-and-groups]]: Kontoverwaltung, sudo
- [[firewall-and-iptables]]: Netzwerksicherheit
- [[ssh-remote-access]]: Härtung des Fernzugriffs
- [[logging-and-journald]]: auditd, Sicherheitsprotokollierung
