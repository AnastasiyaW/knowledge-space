---
title: Privilege Escalation Techniques
category: techniques
tags: [security, privilege-escalation, linux, windows, post-exploitation]
---

# Privilege Escalation Techniques

Post-exploitation privilege escalation on Linux and Windows systems: SUID binaries, sudo misconfigurations, kernel exploits, Windows token impersonation, unquoted service paths, and automated enumeration tools.

## Key Facts
- Privilege escalation turns low-privilege access into root/SYSTEM
- GTFOBins.github.io catalogs Linux binaries exploitable for privesc
- LOLBAS (Living Off the Land Binaries and Scripts) is the Windows equivalent
- WinPEAS/LinPEAS automate enumeration of escalation vectors
- Token impersonation (Potato attacks) is the most common Windows service account escalation

## Linux Privilege Escalation

### SUID Binaries
```bash
find / -perm -4000 -type f 2>/dev/null
# Check each result against GTFOBins.github.io
```
SUID programs run with the file owner's privileges. If a root-owned SUID binary allows arbitrary commands, it provides root access.

### Sudo Misconfigurations
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

### Cron Jobs
```bash
cat /etc/crontab
ls -la /etc/cron.*
# Look for cron jobs running as root that execute writable scripts
# If script is world-writable: inject reverse shell
```

### Writable PATH Directories
If a directory in root's `PATH` is world-writable, place a malicious binary named the same as a command root executes.

### Kernel Exploits
```bash
uname -a            # Check kernel version
# Search exploit-db.com or searchsploit for kernel version
# Examples: Dirty COW (CVE-2016-5195), Dirty Pipe (CVE-2022-0847)
```

### LinPEAS
Automated enumeration script - checks all the above plus:
- Interesting files (configs with passwords, .ssh keys)
- Docker group membership (container escape)
- Capabilities (`getcap -r / 2>/dev/null`)
- NFS no_root_squash shares

## Windows Privilege Escalation

### Token Impersonation (Potato Attacks)
When a service account has `SeImpersonatePrivilege`:
- **JuicyPotato** - DCOM-based (Windows Server 2016/2019)
- **PrintSpoofer** - print spooler abuse
- **GodPotato** - latest variant, works on modern Windows
- Escalates from service account to SYSTEM

### Unquoted Service Paths
```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "C:\Windows"
```
If service path is `C:\Program Files\My App\service.exe` (unquoted), Windows tries:
1. `C:\Program.exe`
2. `C:\Program Files\My.exe`
3. `C:\Program Files\My App\service.exe`

Place malicious executable at an earlier checked path.

### AlwaysInstallElevated
```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
If both = 1: create malicious `.msi` that installs with SYSTEM privileges.

### WinPEAS
Automated enumeration - checks services, registry, scheduled tasks, credentials, permissions.

### Credential Locations
- **SAM database** - `C:\Windows\System32\config\SAM` (NTLM hashes)
- **LSASS memory** - cached credentials (Mimikatz target)
- **Registry** - autologon passwords, VNC passwords
- **Unattend/sysprep files** - deployment credentials
- **Browser saved passwords**

## Lateral Movement
Moving between machines in a compromised network:
- **PsExec** - remote execution via SMB (requires admin creds)
- **WMI** - Windows Management Instrumentation remote exec
- **WinRM** - PowerShell remoting
- **Pass-the-Hash** - authenticate with NTLM hash directly
- **RDP** - Remote Desktop with captured credentials

## Gotchas
- Kernel exploits can crash the system - test carefully and have a plan
- SUID on scripts (bash, python) may not work as expected due to interpreter protections
- Modern Linux kernels and Windows versions patch many classic privesc vectors - always check exact version
- Docker group membership = root equivalent (mount host filesystem)
- `sudo -l` output with `env_keep` can allow `LD_PRELOAD` injection

## See Also
- [[penetration-testing-methodology]] - full pentesting workflow
- [[active-directory-attacks]] - domain-level lateral movement
- [[linux-system-hardening]] - preventing privilege escalation
- [[windows-security-and-powershell]] - Windows security controls
