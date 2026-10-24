---
title: "Techniques d'élévation de privilèges"
category: techniques
tags: [security, privilege-escalation, linux, windows, post-exploitation]
level: 4
source_sha256: e3353659d2475a3e460419c520d626e16f6a0e2c5917383b515a999255bbe50c
translation: machine
translated_at: '2026-10-24'
---
# Techniques d'élévation de privilèges {#privilege-escalation-techniques}

Élévation de privilèges en post-exploitation sur les systèmes Linux et Windows : binaires SUID, mauvaises configurations de sudo, exploits noyau, usurpation de jetons Windows, chemins de service non entre guillemets et outils d'énumération automatisée.

## Faits clés {#key-facts}
- L'élévation de privilèges transforme un accès à faibles privilèges en accès root/SYSTEM
- GTFOBins.github.io recense les binaires Linux exploitables pour l'élévation de privilèges
- LOLBAS (Living Off the Land Binaries and Scripts) est l'équivalent pour Windows
- WinPEAS/LinPEAS automatisent l'énumération des vecteurs d'élévation
- L'usurpation de jetons (attaques Potato) est l'élévation la plus courante depuis un compte de service Windows

## Élévation de privilèges sous Linux {#linux-privilege-escalation}

### Binaires SUID {#suid-binaries}
```bash
find / -perm -4000 -type f 2>/dev/null
# Check each result against GTFOBins.github.io
```
Les programmes SUID s'exécutent avec les privilèges du propriétaire du fichier. Si un binaire SUID appartenant à root permet d'exécuter des commandes arbitraires, il donne un accès root.

### Mauvaises configurations de sudo {#sudo-misconfigurations}
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

### Tâches cron {#cron-jobs}
```bash
cat /etc/crontab
ls -la /etc/cron.*
# Look for cron jobs running as root that execute writable scripts
# If script is world-writable: inject reverse shell
```

### Répertoires accessibles en écriture dans le PATH {#writable-path-directories}
Si un répertoire du `PATH` de root est accessible en écriture par tous, placez un binaire malveillant portant le même nom qu'une commande exécutée par root.

### Exploits noyau {#kernel-exploits}
```bash
uname -a            # Check kernel version
# Search exploit-db.com or searchsploit for kernel version
# Examples: Dirty COW (CVE-2016-5195), Dirty Pipe (CVE-2022-0847)
```

### LinPEAS {#linpeas}
Script d'énumération automatisé : vérifie tous les points ci-dessus, ainsi que :
- Fichiers intéressants (configurations contenant des mots de passe, clés .ssh)
- Appartenance au groupe docker (évasion de conteneur)
- Capacités (`getcap -r / 2>/dev/null`)
- Partages NFS avec no_root_squash

## Élévation de privilèges sous Windows {#windows-privilege-escalation}

### Usurpation de jetons (attaques Potato) {#token-impersonation-potato-attacks}
Lorsqu'un compte de service possède `SeImpersonatePrivilege` :
- **JuicyPotato** - basé sur DCOM (Windows Server 2016/2019)
- **PrintSpoofer** - abus du spouleur d'impression
- **GodPotato** - variante la plus récente, fonctionne sur les versions modernes de Windows
- Élévation du compte de service vers SYSTEM

### Chemins de service non entre guillemets {#unquoted-service-paths}
```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "C:\Windows"
```
Si le chemin du service est `C:\Program Files\My App\service.exe` (sans guillemets), Windows essaie :
1. `C:\Program.exe`
2. `C:\Program Files\My.exe`
3. `C:\Program Files\My App\service.exe`

Placez un exécutable malveillant à un chemin vérifié plus tôt.

### AlwaysInstallElevated {#alwaysinstallelevated}
```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
Si les deux valeurs sont égales à 1 : créez un fichier `.msi` malveillant qui s'installe avec les privilèges SYSTEM.

### WinPEAS {#winpeas}
Énumération automatisée : vérifie les services, le registre, les tâches planifiées, les identifiants et les permissions.

### Emplacements des identifiants {#credential-locations}
- **Base SAM** - `C:\Windows\System32\config\SAM` (hachages NTLM)
- **Mémoire de LSASS** - identifiants en cache (cible de Mimikatz)
- **Registre** - mots de passe d'ouverture de session automatique, mots de passe VNC
- **Fichiers unattend/sysprep** - identifiants de déploiement
- **Mots de passe enregistrés dans les navigateurs**

## Mouvement latéral {#lateral-movement}
Déplacement entre machines dans un réseau compromis :
- **PsExec** - exécution à distance via SMB (nécessite des identifiants administrateur)
- **WMI** - exécution à distance via Windows Management Instrumentation
- **WinRM** - PowerShell remoting
- **Pass-the-Hash** - authentification directe avec un hachage NTLM
- **RDP** - Bureau à distance avec des identifiants obtenus

## Pièges courants {#gotchas}
- Les exploits noyau peuvent faire planter le système : testez avec précaution et prévoyez un plan de repli
- Le bit SUID appliqué à des scripts (bash, python) peut ne pas fonctionner comme prévu en raison des protections de l'interpréteur
- Les noyaux Linux et les versions de Windows récents corrigent de nombreux vecteurs classiques : vérifiez toujours la version exacte
- L'appartenance au groupe docker équivaut à root (montage du système de fichiers de l'hôte)
- La sortie de `sudo -l` avec `env_keep` peut permettre une injection via `LD_PRELOAD`

## Voir aussi {#see-also}
- [[penetration-testing-methodology]] - processus complet de test d'intrusion
- [[active-directory-attacks]] - mouvement latéral au niveau du domaine
- [[linux-system-hardening]] - prévention de l'élévation de privilèges
- [[windows-security-and-powershell]] - contrôles de sécurité Windows
