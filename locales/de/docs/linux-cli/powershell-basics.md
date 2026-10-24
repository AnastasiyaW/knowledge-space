---
title: "PowerShell-Grundlagen"
category: reference
tags: [linux-cli, powershell, windows, cmdlets, scripting]
level: 3
source_sha256: ea554d44ae28ad18dd4b42213f1f680492b844eb39fce6714bfa6a528cfc1a23
translation: machine
translated_at: '2026-10-24'
---
# PowerShell-Grundlagen {#powershell-basics}

PowerShell ist eine plattformübergreifende Shell und Skriptsprache auf Basis von .NET. Anders als bash, das Text durch Pipes leitet, leitet PowerShell Objekte durch Pipes. Dieser Eintrag behandelt Cmdlets, Navigation, Variablen, Pipelines und Skripte.

## Wichtige Fakten {#key-facts}

- Cmdlets folgen der Namenskonvention `Verb-Noun`: `Get-ChildItem`, `Set-Location`
- Pipelines übergeben **Objekte**, nicht Text
- Viele Unix-Aliase funktionieren: `ls`, `cd`, `cp`, `mv`, `rm`, `cat`
- **Windows PowerShell** (5.1) = .NET Framework, nur unter Windows
- **PowerShell** (7+) = .NET Core, plattformübergreifend

## Navigation {#navigation}

```powershell
Set-Location C:\Users\data    # change directory
cd C:\Users\data              # alias
cd ..                         # up one level
cd ~                          # home directory
Get-Location                  # current directory (pwd)
```

## Dateioperationen {#file-operations}

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

## Variablen {#variables}

```powershell
$myVar = "value"
$num = 42
echo $myVar                   # print (Write-Output)
$myVar.GetType()              # type info
```

### Umgebungsvariablen {#environment-variables}

```powershell
$env:PATH                     # PATH variable
$env:USERNAME                 # current user
$env:COMPUTERNAME             # machine name
$env:TEMP                     # temp directory
$env:MY_VAR = "value"         # set (session only)
```

## Cmdlet-Aufbau {#cmdlet-structure}

```powershell
Get-Command                   # list all commands
Get-Command -Verb Get         # filter by verb
Get-Help Get-ChildItem        # help
Get-Help Get-ChildItem -Examples  # examples
Get-Alias                     # list all aliases
Get-Alias ls                  # what ls maps to
```

## Pipelines (objektbasiert) {#pipelines-object-based}

```powershell
Get-Process | Where-Object {$_.CPU -gt 10}      # filter
Get-Service | Sort-Object Status                 # sort
Get-ChildItem | Select-Object Name, Length       # select fields
Get-Content file.txt | Measure-Object -Line      # count lines

# $_ = current pipeline object
Get-Process | ForEach-Object { Write-Host $_.Name }
```

## Ausgabe und Formatierung {#output-and-formatting}

```powershell
Write-Host "text"             # console only (not pipeline)
Write-Output "text"           # to pipeline
Write-Error "error"           # error stream

Get-Process | Format-Table    # table view
Get-Process | Format-List     # list view
Get-Process | Out-GridView    # GUI grid (Windows)
```

## Funktionen {#functions}

```powershell
function Get-Greeting {
    param([string]$Name = "World")
    Write-Output "Hello, $Name!"
}
Get-Greeting -Name "Alice"
```

## Skripte (.ps1) {#scripts-ps1}

```powershell
.\myscript.ps1                # run script
Get-ExecutionPolicy           # check policy
Set-ExecutionPolicy RemoteSigned      # allow local scripts
Set-ExecutionPolicy Bypass -Scope Process  # current session only
```

### Profil (Startkonfiguration) {#profile-startup-config}

```powershell
$PROFILE                      # path to profile file
notepad $PROFILE              # edit
```

## Häufige Einzeiler {#common-one-liners}

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

## Alias-Referenz {#aliases-reference}

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

## Stolperfallen {#gotchas}

- PowerShell-Aliase sehen aus wie Unix-Befehle, geben aber Objekte statt Text weiter - das Pipe-Verhalten unterscheidet sich
- `-Recurse` statt `-r` (PowerShell verwendet vollständige Parameternamen)
- `rm` in PowerShell ist `Remove-Item`, nicht GNU rm - andere Flags
- Die Ausführungsrichtlinie kann Skripte blockieren - prüfen mit `Get-ExecutionPolicy`
- `Write-Host` gelangt NICHT in die Pipeline - für Pipes `Write-Output` verwenden
- Zeichenkettenvergleiche sind standardmäßig nicht case-sensitiv (für Groß-/Kleinschreibung `-ceq` verwenden)

## Siehe auch {#see-also}

- [[wsl]] - WSL-Bash vs. PowerShell: Unterschiede
- [[terminal-basics]] - Grundlagen der Linux-Shell
- [[bash-scripting]] - Bash-Skripting im Vergleich
