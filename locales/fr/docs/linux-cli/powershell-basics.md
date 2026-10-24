---
title: "Bases de PowerShell"
category: reference
tags: [linux-cli, powershell, windows, cmdlets, scripting]
level: 3
source_sha256: ea554d44ae28ad18dd4b42213f1f680492b844eb39fce6714bfa6a528cfc1a23
translation: machine
translated_at: '2026-10-24'
---
# Bases de PowerShell {#powershell-basics}

PowerShell est un shell et un langage de script multiplateforme construit sur .NET. Contrairement à bash qui transmet du texte dans ses pipelines, PowerShell transmet des objets. Cette entrée couvre les cmdlets, la navigation, les variables, les pipelines et les scripts.

## Points clés {#key-facts}

- Les cmdlets suivent la convention de nommage `Verbe-Nom` : `Get-ChildItem`, `Set-Location`
- Les pipelines transmettent des **objets**, et non du texte
- De nombreux alias Unix fonctionnent : `ls`, `cd`, `cp`, `mv`, `rm`, `cat`
- **Windows PowerShell** (5.1) = .NET Framework, Windows uniquement
- **PowerShell** (7+) = .NET Core, multiplateforme

## Navigation {#navigation}

```powershell
Set-Location C:\Users\data    # change directory
cd C:\Users\data              # alias
cd ..                         # up one level
cd ~                          # home directory
Get-Location                  # current directory (pwd)
```

## Opérations sur les fichiers {#file-operations}

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

## Variables {#variables}

```powershell
$myVar = "value"
$num = 42
echo $myVar                   # print (Write-Output)
$myVar.GetType()              # type info
```

### Variables d'environnement {#environment-variables}

```powershell
$env:PATH                     # PATH variable
$env:USERNAME                 # current user
$env:COMPUTERNAME             # machine name
$env:TEMP                     # temp directory
$env:MY_VAR = "value"         # set (session only)
```

## Structure des cmdlets {#cmdlet-structure}

```powershell
Get-Command                   # list all commands
Get-Command -Verb Get         # filter by verb
Get-Help Get-ChildItem        # help
Get-Help Get-ChildItem -Examples  # examples
Get-Alias                     # list all aliases
Get-Alias ls                  # what ls maps to
```

## Pipelines (basés sur les objets) {#pipelines-object-based}

```powershell
Get-Process | Where-Object {$_.CPU -gt 10}      # filter
Get-Service | Sort-Object Status                 # sort
Get-ChildItem | Select-Object Name, Length       # select fields
Get-Content file.txt | Measure-Object -Line      # count lines

# $_ = current pipeline object
Get-Process | ForEach-Object { Write-Host $_.Name }
```

## Sortie et mise en forme {#output-and-formatting}

```powershell
Write-Host "text"             # console only (not pipeline)
Write-Output "text"           # to pipeline
Write-Error "error"           # error stream

Get-Process | Format-Table    # table view
Get-Process | Format-List     # list view
Get-Process | Out-GridView    # GUI grid (Windows)
```

## Fonctions {#functions}

```powershell
function Get-Greeting {
    param([string]$Name = "World")
    Write-Output "Hello, $Name!"
}
Get-Greeting -Name "Alice"
```

## Scripts (.ps1) {#scripts-ps1}

```powershell
.\myscript.ps1                # run script
Get-ExecutionPolicy           # check policy
Set-ExecutionPolicy RemoteSigned      # allow local scripts
Set-ExecutionPolicy Bypass -Scope Process  # current session only
```

### Profil (configuration au démarrage) {#profile-startup-config}

```powershell
$PROFILE                      # path to profile file
notepad $PROFILE              # edit
```

## Commandes courantes sur une ligne {#common-one-liners}

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

## Référence des alias {#aliases-reference}

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

## Pièges à éviter {#gotchas}

- Les alias PowerShell ressemblent à ceux d'Unix mais transmettent des objets, et non du texte : le comportement des pipelines diffère
- `-Recurse` et non `-r` (PowerShell utilise les noms complets des paramètres)
- `rm` dans PowerShell est `Remove-Item`, et non rm de GNU : les options ne sont pas les mêmes
- La stratégie d'exécution peut bloquer les scripts : vérifiez-la avec `Get-ExecutionPolicy`
- `Write-Host` n'envoie PAS dans le pipeline : utilisez `Write-Output` pour le transmettre
- La comparaison de chaînes est insensible à la casse par défaut (utilisez `-ceq` pour une comparaison sensible à la casse)

## Voir aussi {#see-also}

- [[wsl]] - Différences entre bash sous WSL et PowerShell
- [[terminal-basics]] - Fondamentaux du shell Linux
- [[bash-scripting]] - Comparaison avec le scripting Bash
