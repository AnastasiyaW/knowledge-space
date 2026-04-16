---
title: Windows Security and PowerShell
category: techniques
tags: [security, windows, powershell, active-directory, event-log, registry, hardening]
---

# Windows Security and PowerShell

Windows security internals: credential storage (SAM, LSASS), PowerShell for security operations, Windows Event Log critical IDs, registry security keys, Group Policy, AppLocker, NTFS permissions, and Windows hardening baselines.

## Key Facts
- SAM stores local NTLM hashes at `C:\Windows\System32\config\SAM`
- LSASS process caches credentials in memory - primary target for Mimikatz
- Event ID 4625 = failed logon; 4624 = successful logon; 1102 = audit log cleared (red flag)
- AppLocker provides application whitelisting by publisher, path, or file hash
- Group Policy applies hierarchically: Local -> Site -> Domain -> OU
- CIS Benchmark: 14+ char passwords, lockout after 5 attempts, disable SMBv1

## Credential Storage

### SAM (Security Account Manager)
Local account database at `C:\Windows\System32\config\SAM`. Contains NTLM hashes of local user passwords.

### LSASS (Local Security Authority Subsystem Service)
Handles authentication, caches credentials in memory. Mimikatz extracts cleartext passwords if WDigest is enabled.

### NTLM vs Kerberos
- **NTLMv1** - weak, rainbow table attackable
- **NTLMv2** - improved but still vulnerable to relay attacks
- **Kerberos** - ticket-based, default in AD, more secure

## PowerShell Security Operations

### Event Log Queries
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

### User Enumeration
```powershell
Get-LocalUser                               # Local users
Get-LocalGroupMember Administrators          # Local admins
Get-ADUser -Filter * -Properties LastLogonDate  # AD users (RSAT required)
Get-ADGroupMember "Domain Admins"            # Domain admins
```

### Network and Process
```powershell
Get-Process | Select-Object Name, Id, CPU, Path
Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"}
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"}
Test-NetConnection -ComputerName host -Port 443
```

## Critical Event IDs
| Event ID | Log | Description |
|----------|-----|-------------|
| 4624 | Security | Successful logon |
| 4625 | Security | Failed logon |
| 4634 | Security | Logoff |
| 4648 | Security | Explicit credential logon (runas) |
| 4672 | Security | Special privileges assigned (admin) |
| 4688 | Security | Process creation |
| 4697 | Security | Service installed |
| 7045 | System | New service installed |
| 4720 | Security | User account created |
| 4726 | Security | User account deleted |
| 4732 | Security | Member added to security group |
| 1102 | Security | Audit log cleared (RED FLAG) |

### Logon Types (Event 4624)
| Type | Description |
|------|-------------|
| 2 | Interactive (console) |
| 3 | Network (SMB, mapped drives) |
| 4 | Batch (scheduled tasks) |
| 5 | Service (service account) |
| 7 | Unlock |
| 10 | RemoteInteractive (RDP) |
| 11 | CachedInteractive (cached domain creds) |

## Windows Registry Security Keys
```text
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run         # Auto-start
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce     # One-time auto-start
HKLM\SYSTEM\CurrentControlSet\Services                      # Windows services
HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid           # Machine ID
HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server      # RDP settings
```

Monitoring: **Sysmon** logs registry changes (Event ID 12/13/14). **RegRipper** for forensic analysis.

## Group Policy (GPO)
- Applied: Local -> Site -> Domain -> OU
- Refresh: `gpupdate /force`
- View applied: `gpresult /r`
- Key security GPOs: password policy, software restriction, firewall rules, audit settings

## NTFS and EFS
- **NTFS permissions**: Read, Write, Execute, Modify, Full Control
- Inheritance flows parent -> child; explicit overrides inherited
- `icacls` for CLI permission management
- **EFS** (Encrypting File System) - transparent file-level encryption tied to user certificate

## AppLocker
Application whitelisting - specify allowed executables/scripts/DLLs:
- Rules by: publisher certificate, file path, file hash
- Modes: Audit only (log), Enforce (block)

## Windows Hardening (CIS Benchmark)
- Password: 14+ chars, complexity, no reuse of last 24
- Account lockout: 5 attempts, 15 min lockout
- Disable SMBv1
- Enable Windows Defender Credential Guard
- Enable audit policies (logon, object access, privilege use, process tracking)
- Deploy LAPS (Local Administrator Password Solution)
- Enable Attack Surface Reduction rules
- Disable unnecessary services and features

## Gotchas
- Event ID 1102 (audit log cleared) is almost always malicious - alert on this immediately
- PowerShell execution policy is not a security boundary - it prevents accidental execution, not attackers
- NTLM relay attacks work even if NTLMv2 is enforced - disable NTLM entirely where possible
- Sysmon must be deployed and configured separately - Windows does not log process command lines by default
- GPO "Last writer wins" can cause policy conflicts in complex OU structures

## See Also
- [[active-directory-attacks]] - AD-specific attack techniques
- [[privilege-escalation-techniques]] - Windows privesc vectors
- [[siem-and-incident-response]] - Windows event log in SIEM
- [[authentication-and-authorization]] - Kerberos, NTLM protocols
