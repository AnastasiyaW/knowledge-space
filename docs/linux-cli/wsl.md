---
title: WSL - Windows Subsystem for Linux
category: reference
tags: [linux-cli, wsl, windows, interop]
---

# WSL - Windows Subsystem for Linux

WSL runs Linux distributions inside Windows. WSL2 uses a real Linux kernel in a lightweight VM. This entry covers installation, file interop, networking, and configuration.

## Key Facts

- WSL2 uses a real Linux kernel (not translation layer like WSL1)
- Windows files accessible at `/mnt/c/`, `/mnt/d/`, etc.
- Linux files from Windows: `\\wsl$\Ubuntu\` in File Explorer
- All standard Linux commands work inside WSL

## Installation

```powershell
wsl --install                   # install WSL + default Ubuntu
wsl --install -d Debian         # specific distro
wsl --list --online             # available distros
wsl --list --verbose            # installed distros
wsl --set-default-version 2     # use WSL2 by default
wsl --set-version Ubuntu 2      # convert existing to WSL2
```

## Launching

```powershell
wsl                             # default distro
wsl -d Ubuntu                   # specific distro
ubuntu                          # direct launch
bash                            # WSL bash
```

## File System Interop

### Linux -> Windows Files

```bash
ls /mnt/c/                          # C: drive
ls /mnt/c/Users/username/Documents
cd /mnt/d/projects
```

### Windows -> Linux Files

```text
\\wsl$\Ubuntu\home\username     # File Explorer
\\wsl.localhost\Ubuntu\         # alternative (WSL2)
```

## Cross-System Commands

### Run Windows Programs from WSL

```bash
notepad.exe file.txt
explorer.exe .                  # current dir in File Explorer
cmd.exe /c "windows-command"
powershell.exe -Command "..."
```

### Run Linux Commands from Windows

```powershell
wsl ls /home
wsl -e bash -c "ls | grep txt"
```

## Configuration

### /etc/wsl.conf (per-distro)

```ini
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"

[network]
hostname = my-wsl
generateHosts = true

[interop]
enabled = true
appendWindowsPath = true    # add Windows PATH to WSL
```

### ~/.wslconfig (global, Windows user home)

```ini
[wsl2]
memory=4GB
processors=2
swap=2GB
localhostForwarding=true
```

## Networking

- WSL2 has its own virtual network interface
- `localhost` from WSL2 usually reaches Windows host
- Windows can reach WSL2 services via `localhost` (auto port forwarding)
- Find Windows host IP: `cat /etc/resolv.conf | grep nameserver | awk '{print $2}'`

## Management

```powershell
wsl --shutdown                  # shutdown all instances
wsl --terminate Ubuntu          # terminate specific distro
wsl --export Ubuntu backup.tar  # backup distro
wsl --import Ubuntu C:\WSL\Ubuntu backup.tar  # restore
wsl --version                   # WSL version info
```

## Key Differences: WSL Bash vs PowerShell

| Feature | WSL Bash | PowerShell |
|---------|----------|------------|
| Path separator | `/` | `\` (or `/`) |
| Recursive flag | `-r` | `-Recurse` |
| Cmdlets | Not supported | `Get-*`, `Set-*` |
| Unix tools | Native | Not native |
| Pipes | Text streams | Object pipelines |

## Gotchas

- Cross-filesystem operations (Linux reading /mnt/c) are slower than native
- WSL2 memory can grow and not be released - set `memory` limit in `.wslconfig`
- `wsl --shutdown` is needed to apply `.wslconfig` changes
- File permissions may not behave as expected on /mnt/c - use `metadata` mount option
- Git performance is much better on Linux filesystem (`~/`) than on `/mnt/c/`

## See Also

- [[terminal-basics]] - Shell fundamentals
- [[powershell-basics]] - PowerShell commands and patterns
- [[package-management]] - apt inside WSL
