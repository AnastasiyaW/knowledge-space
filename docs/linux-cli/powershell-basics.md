---
title: PowerShell Basics
category: reference
tags: [linux-cli, powershell, windows, cmdlets, scripting]
---

# PowerShell Basics

PowerShell is a cross-platform shell and scripting language built on .NET. Unlike bash which pipes text, PowerShell pipes objects. This entry covers cmdlets, navigation, variables, pipelines, and scripts.

## Key Facts

- Cmdlets follow `Verb-Noun` naming: `Get-ChildItem`, `Set-Location`
- Pipelines pass **objects**, not text
- Many Unix aliases work: `ls`, `cd`, `cp`, `mv`, `rm`, `cat`
- **Windows PowerShell** (5.1) = .NET Framework, Windows-only
- **PowerShell** (7+) = .NET Core, cross-platform

## Navigation

```powershell
Set-Location C:\Users\data    # change directory
cd C:\Users\data              # alias
cd ..                         # up one level
cd ~                          # home directory
Get-Location                  # current directory (pwd)
```

## File Operations

```powershell
Get-ChildItem                 # list (ls, dir)
Get-ChildItem -Recurse        # recursive
Get-ChildItem *.txt           # filter

Copy-Item file.txt dest\     # copy (cp)
Copy-Item dir\ dest\ -Recurse
Move-Item file.txt dest\     # move/rename (mv)
Remove-Item file.txt         # delete (rm)
Remove-Item dir\ -Recurse    # delete directory

New-Item file.txt -ItemType File       # create file
New-Item folder -ItemType Directory    # create directory (mkdir)
```

## Variables

```powershell
$myVar = "value"
$num = 42
echo $myVar                   # print (Write-Output)
$myVar.GetType()              # type info
```

### Environment Variables

```powershell
$env:PATH                     # PATH variable
$env:USERNAME                 # current user
$env:COMPUTERNAME             # machine name
$env:TEMP                     # temp directory
$env:MY_VAR = "value"         # set (session only)
```

## Cmdlet Structure

```powershell
Get-Command                   # list all commands
Get-Command -Verb Get         # filter by verb
Get-Help Get-ChildItem        # help
Get-Help Get-ChildItem -Examples  # examples
Get-Alias                     # list all aliases
Get-Alias ls                  # what ls maps to
```

## Pipelines (Object-Based)

```powershell
Get-Process | Where-Object {$_.CPU -gt 10}      # filter
Get-Service | Sort-Object Status                 # sort
Get-ChildItem | Select-Object Name, Length       # select fields
Get-Content file.txt | Measure-Object -Line      # count lines

# $_ = current pipeline object
Get-Process | ForEach-Object { Write-Host $_.Name }
```

## Output and Formatting

```powershell
Write-Host "text"             # console only (not pipeline)
Write-Output "text"           # to pipeline
Write-Error "error"           # error stream

Get-Process | Format-Table    # table view
Get-Process | Format-List     # list view
Get-Process | Out-GridView    # GUI grid (Windows)
```

## Functions

```powershell
function Get-Greeting {
    param([string]$Name = "World")
    Write-Output "Hello, $Name!"
}
Get-Greeting -Name "Alice"
```

## Scripts (.ps1)

```powershell
.\myscript.ps1                # run script
Get-ExecutionPolicy           # check policy
Set-ExecutionPolicy RemoteSigned      # allow local scripts
Set-ExecutionPolicy Bypass -Scope Process  # current session only
```

### Profile (Startup Config)

```powershell
$PROFILE                      # path to profile file
notepad $PROFILE              # edit
```

## Common One-Liners

```powershell
# File operations
Get-ChildItem -Recurse -Filter "*.log"
Select-String -Path *.txt -Pattern "error"
Test-Path C:\file.txt
Get-Content file.txt
"content" | Out-File file.txt
Add-Content file.txt "more"

# Process management
Get-Process
Stop-Process -Name notepad
Start-Process notepad

# Network
Test-NetConnection google.com -Port 80
Invoke-WebRequest https://example.com
```

## Aliases Reference

| Alias | Cmdlet |
|-------|--------|
| `ls`, `dir` | `Get-ChildItem` |
| `cd` | `Set-Location` |
| `cp` | `Copy-Item` |
| `mv` | `Move-Item` |
| `rm`, `del` | `Remove-Item` |
| `cat`, `type` | `Get-Content` |
| `echo` | `Write-Output` |
| `pwd` | `Get-Location` |
| `ps` | `Get-Process` |
| `kill` | `Stop-Process` |

## Gotchas

- PowerShell aliases look like Unix but pass objects, not text - piping behavior differs
- `-Recurse` not `-r` (PowerShell uses full parameter names)
- `rm` in PowerShell is `Remove-Item`, not GNU rm - different flags
- Execution policy may block scripts - check with `Get-ExecutionPolicy`
- `Write-Host` does NOT go to pipeline - use `Write-Output` for piping
- String comparison is case-insensitive by default (use `-ceq` for case-sensitive)

## See Also

- [[wsl]] - WSL bash vs PowerShell differences
- [[terminal-basics]] - Linux shell fundamentals
- [[bash-scripting]] - Bash scripting comparison
