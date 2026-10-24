---
title: "Windows-Sicherheit und PowerShell"
category: techniques
tags: [security, windows, powershell, active-directory, event-log, registry, hardening]
level: 3
source_sha256: dd89fe188679af48a0ef05882b8efb46d51b3330f52f5960f5040abc408cd4fe
translation: machine
translated_at: '2026-10-24'
---
# Windows-Sicherheit und PowerShell {#windows-security-and-powershell}

Interne Sicherheitsmechanismen von Windows: Credential-Speicherung (SAM, LSASS), PowerShell für Security-Operationen, kritische Windows-Event-Log-IDs, sicherheitsrelevante Registry-Schlüssel, Group Policy, AppLocker, NTFS-Berechtigungen und Windows-Hardening-Baselines.

## Wichtige Fakten {#key-facts}
- SAM speichert lokale NTLM-Hashes unter `C:\Windows\System32\config\SAM`
- Der LSASS-Prozess hält Credentials im Speicher - primäres Ziel für Mimikatz
- Event-ID 4625 = fehlgeschlagene Anmeldung; 4624 = erfolgreiche Anmeldung; 1102 = Audit-Log gelöscht (Warnsignal)
- AppLocker bietet Application Whitelisting nach Publisher, Pfad oder Datei-Hash
- Group Policy wird hierarchisch angewendet: Local -> Site -> Domain -> OU
- CIS Benchmark: Passwörter mit 14+ Zeichen, Sperre nach 5 Versuchen, SMBv1 deaktivieren

## Credential-Speicherung {#credential-storage}

### SAM (Security Account Manager) {#sam-security-account-manager}
Lokale Kontendatenbank unter `C:\Windows\System32\config\SAM`. Enthält NTLM-Hashes der Passwörter lokaler Benutzer.

### LSASS (Local Security Authority Subsystem Service) {#lsass-local-security-authority-subsystem-service}
Verarbeitet die Authentifizierung und hält Credentials im Speicher. Mimikatz extrahiert Klartext-Passwörter, wenn WDigest aktiviert ist.

### NTLM vs. Kerberos {#ntlm-vs-kerberos}
- **NTLMv1** - schwach, angreifbar durch Rainbow Tables
- **NTLMv2** - verbessert, aber weiterhin anfällig für Relay-Angriffe
- **Kerberos** - ticketbasiert, Standard in AD, sicherer

## PowerShell-Security-Operationen {#powershell-security-operations}

### Event-Log-Abfragen {#event-log-queries}
```powershell
# Failed logins
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 50

# Successful logins
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624} -MaxEvents 50

# New service installed
Get-WinEvent -FilterHashtable @{LogName='System'; ID=7045}

# Process creation with command line
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4688} |
    Select-Object TimeCreated, @{N='CommandLine';E={$_.Properties[8].Value}}
```

### Benutzerenumeration {#user-enumeration}
```powershell
Get-LocalUser                               # Local users
Get-LocalGroupMember Administrators          # Local admins
Get-ADUser -Filter * -Properties LastLogonDate  # AD users (RSAT required)
Get-ADGroupMember "Domain Admins"            # Domain admins
```

### Netzwerk und Prozesse {#network-and-process}
```powershell
Get-Process | Select-Object Name, Id, CPU, Path
Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"}
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"}
Test-NetConnection -ComputerName host -Port 443
```

## Kritische Event-IDs {#critical-event-ids}
| Event-ID | Log | Beschreibung |
|----------|-----|-------------|
| 4624 | Security | Erfolgreiche Anmeldung |
| 4625 | Security | Fehlgeschlagene Anmeldung |
| 4634 | Security | Abmeldung |
| 4648 | Security | Anmeldung mit expliziten Credentials (runas) |
| 4672 | Security | Besondere Berechtigungen zugewiesen (Admin) |
| 4688 | Security | Prozesserstellung |
| 4697 | Security | Dienst installiert |
| 7045 | System | Neuer Dienst installiert |
| 4720 | Security | Benutzerkonto erstellt |
| 4726 | Security | Benutzerkonto gelöscht |
| 4732 | Security | Mitglied zu Sicherheitsgruppe hinzugefügt |
| 1102 | Security | Audit-Log gelöscht (WARNSIGNAL) |

### Anmeldetypen (Event 4624) {#logon-types-event-4624}
| Typ | Beschreibung |
|------|-------------|
| 2 | Interaktiv (Konsole) |
| 3 | Netzwerk (SMB, zugeordnete Laufwerke) |
| 4 | Batch (geplante Tasks) |
| 5 | Dienst (Dienstkonto) |
| 7 | Entsperren |
| 10 | RemoteInteractive (RDP) |
| 11 | CachedInteractive (zwischengespeicherte Domain-Credentials) |

## Sicherheitsrelevante Windows-Registry-Schlüssel {#windows-registry-security-keys}
```text
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run         # Auto-start
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce     # One-time auto-start
HKLM\SYSTEM\CurrentControlSet\Services                      # Windows services
HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid           # Machine ID
HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server      # RDP settings
```

Monitoring: **Sysmon** protokolliert Registry-Änderungen (Event-ID 12/13/14). **RegRipper** dient der forensischen Analyse.

## Group Policy (GPO) {#group-policy-gpo}
- Anwendung: Local -> Site -> Domain -> OU
- Aktualisierung: `gpupdate /force`
- Angewendete Richtlinien anzeigen: `gpresult /r`
- Wichtige Sicherheits-GPOs: Passwortrichtlinie, Software-Einschränkung, Firewall-Regeln, Audit-Einstellungen

## NTFS und EFS {#ntfs-and-efs}
- **NTFS-Berechtigungen**: Lesen, Schreiben, Ausführen, Ändern, Vollzugriff
- Vererbung fließt von Eltern- zu Kindobjekt; explizite Berechtigungen überschreiben geerbte
- `icacls` für die Verwaltung von Berechtigungen über die Kommandozeile
- **EFS** (Encrypting File System) - transparente Verschlüsselung auf Dateiebene, gebunden an das Benutzerzertifikat

## AppLocker {#applocker}
Application Whitelisting - erlaubte Programme, Skripte und DLLs festlegen:
- Regeln nach: Publisher-Zertifikat, Dateipfad, Datei-Hash
- Modi: Nur Audit (protokollieren), Enforce (blockieren)

## Windows-Hardening (CIS Benchmark) {#windows-hardening-cis-benchmark}
- Passwort: 14+ Zeichen, Komplexität, keine Wiederverwendung der letzten 24
- Kontosperrung: 5 Versuche, 15 Minuten Sperre
- SMBv1 deaktivieren
- Windows Defender Credential Guard aktivieren
- Audit-Richtlinien aktivieren (Anmeldung, Objektzugriff, Privilegienverwendung, Prozessverfolgung)
- LAPS (Local Administrator Password Solution) ausrollen
- Attack Surface Reduction-Regeln aktivieren
- Nicht benötigte Dienste und Features deaktivieren

## Gotchas {#gotchas}
- Event-ID 1102 (Audit-Log gelöscht) ist fast immer bösartig - sofort alarmieren
- Die PowerShell-Execution-Policy ist keine Sicherheitsgrenze - sie verhindert versehentliche Ausführung, nicht Angreifer
- NTLM-Relay-Angriffe funktionieren auch dann, wenn NTLMv2 erzwungen wird - NTLM wo immer möglich vollständig deaktivieren
- Sysmon muss separat ausgerollt und konfiguriert werden - Windows protokolliert Prozess-Kommandozeilen standardmäßig nicht
- GPO-"Last writer wins" kann in komplexen OU-Strukturen zu Richtlinienkonflikten führen

## Siehe auch {#see-also}
- [[active-directory-attacks]] - AD-spezifische Angriffstechniken
- [[privilege-escalation-techniques]] - Windows-Privilegienerweiterung
- [[siem-and-incident-response]] - Windows-Event-Log im SIEM
- [[authentication-and-authorization]] - Kerberos, NTLM-Protokolle
