---
title: "Sécurité Windows et PowerShell"
category: techniques
tags: [security, windows, powershell, active-directory, event-log, registry, hardening]
level: 3
source_sha256: dd89fe188679af48a0ef05882b8efb46d51b3330f52f5960f5040abc408cd4fe
translation: machine
translated_at: '2026-10-24'
---
# Sécurité Windows et PowerShell {#windows-security-and-powershell}

Fonctionnement interne de la sécurité Windows : stockage des identifiants (SAM, LSASS), PowerShell pour les opérations de sécurité, ID critiques du journal d'événements Windows, clés de registre de sécurité, Group Policy, AppLocker, permissions NTFS et référentiels de durcissement Windows.

## Points clés {#key-facts}
- La SAM stocke les hachages NTLM des comptes locaux dans `C:\Windows\System32\config\SAM`
- Le processus LSASS met en cache les identifiants en mémoire : cible principale de Mimikatz
- Event ID 4625 = échec de connexion ; 4624 = connexion réussie ; 1102 = journal d'audit effacé (signal d'alerte)
- AppLocker assure la liste blanche d'applications par éditeur, chemin ou empreinte de fichier (hash)
- Les GPO s'appliquent de manière hiérarchique : Local -> Site -> Domaine -> UO
- CIS Benchmark : mots de passe de 14 caractères ou plus, verrouillage après 5 tentatives, désactivation de SMBv1

## Stockage des identifiants {#credential-storage}

### SAM (Security Account Manager) {#sam-security-account-manager}
Base de données des comptes locaux, située dans `C:\Windows\System32\config\SAM`. Elle contient les hachages NTLM des mots de passe des utilisateurs locaux.

### LSASS (Local Security Authority Subsystem Service) {#lsass-local-security-authority-subsystem-service}
Gère l'authentification et met en cache les identifiants en mémoire. Mimikatz extrait les mots de passe en clair si WDigest est activé.

### NTLM vs Kerberos {#ntlm-vs-kerberos}
- **NTLMv1** : faible, vulnérable aux attaques par tables arc-en-ciel
- **NTLMv2** : amélioré, mais toujours vulnérable aux attaques par relais
- **Kerberos** : basé sur des tickets, protocole par défaut dans AD, plus sécurisé

## Opérations de sécurité avec PowerShell {#powershell-security-operations}

### Requêtes sur le journal d'événements {#event-log-queries}
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

### Énumération des utilisateurs {#user-enumeration}
```powershell
Get-LocalUser                               # Local users
Get-LocalGroupMember Administrators          # Local admins
Get-ADUser -Filter * -Properties LastLogonDate  # AD users (RSAT required)
Get-ADGroupMember "Domain Admins"            # Domain admins
```

### Réseau et processus {#network-and-process}
```powershell
Get-Process | Select-Object Name, Id, CPU, Path
Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"}
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"}
Test-NetConnection -ComputerName host -Port 443
```

## ID critiques du journal d'événements {#critical-event-ids}
| Event ID | Journal | Description |
|----------|---------|-------------|
| 4624 | Security | Connexion réussie |
| 4625 | Security | Échec de connexion |
| 4634 | Security | Déconnexion |
| 4648 | Security | Connexion avec identifiants explicites (runas) |
| 4672 | Security | Attribution de privilèges spéciaux (admin) |
| 4688 | Security | Création de processus |
| 4697 | Security | Installation d'un service |
| 7045 | System | Nouveau service installé |
| 4720 | Security | Création d'un compte utilisateur |
| 4726 | Security | Suppression d'un compte utilisateur |
| 4732 | Security | Membre ajouté à un groupe de sécurité |
| 1102 | Security | Journal d'audit effacé (SIGNAL D'ALERTE) |

### Types de connexion (Event 4624) {#logon-types-event-4624}
| Type | Description |
|------|-------------|
| 2 | Interactive (console) |
| 3 | Réseau (SMB, lecteurs réseau mappés) |
| 4 | Batch (tâches planifiées) |
| 5 | Service (compte de service) |
| 7 | Déverrouillage |
| 10 | RemoteInteractive (RDP) |
| 11 | CachedInteractive (identifiants de domaine en cache) |

## Clés de registre de sécurité Windows {#windows-registry-security-keys}
```text
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run         # Auto-start
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce     # One-time auto-start
HKLM\SYSTEM\CurrentControlSet\Services                      # Windows services
HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid           # Machine ID
HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server      # RDP settings
```

Surveillance : **Sysmon** journalise les modifications du registre (Event ID 12/13/14). **RegRipper** sert à l'analyse forensique.

## Group Policy (GPO) {#group-policy-gpo}
- Application : Local -> Site -> Domaine -> UO
- Actualisation : `gpupdate /force`
- Consulter les stratégies appliquées : `gpresult /r`
- GPO de sécurité clés : stratégie de mot de passe, restrictions logicielles, règles de pare-feu, paramètres d'audit

## NTFS et EFS {#ntfs-and-efs}
- **Permissions NTFS** : Lecture, Écriture, Exécution, Modification, Contrôle total
- L'héritage descend du parent vers l'enfant ; une permission explicite prime sur une permission héritée
- `icacls` pour la gestion des permissions en ligne de commande
- **EFS** (Encrypting File System) : chiffrement transparent au niveau des fichiers, lié au certificat de l'utilisateur

## AppLocker {#applocker}
Liste blanche d'applications : définit les exécutables, scripts et DLL autorisés.
- Règles par : certificat de l'éditeur, chemin de fichier, empreinte de fichier (hash)
- Modes : Audit uniquement (journalisation), Enforce (blocage)

## Durcissement Windows (CIS Benchmark) {#windows-hardening-cis-benchmark}
- Mot de passe : 14 caractères ou plus, complexité, pas de réutilisation des 24 derniers
- Verrouillage de compte : 5 tentatives, verrouillage de 15 min
- Désactiver SMBv1
- Activer Windows Defender Credential Guard
- Activer les stratégies d'audit (ouverture de session, accès aux objets, utilisation des privilèges, suivi des processus)
- Déployer LAPS (Local Administrator Password Solution)
- Activer les règles Attack Surface Reduction
- Désactiver les services et fonctionnalités inutiles

## Pièges courants {#gotchas}
- L'Event ID 1102 (journal d'audit effacé) est presque toujours malveillant : à alerter immédiatement
- La stratégie d'exécution PowerShell n'est pas une frontière de sécurité : elle empêche l'exécution accidentelle, pas celle d'un attaquant
- Les attaques par relais NTLM fonctionnent même si NTLMv2 est imposé : désactiver NTLM entièrement dans la mesure du possible
- Sysmon doit être déployé et configuré séparément : Windows ne journalise pas les lignes de commande des processus par défaut
- Le principe « Last writer wins » des GPO peut provoquer des conflits de stratégies dans des structures d'UO complexes

## Voir aussi {#see-also}
- [[active-directory-attacks]] : techniques d'attaque spécifiques à AD
- [[privilege-escalation-techniques]] : vecteurs d'élévation de privilèges sous Windows
- [[siem-and-incident-response]] : journaux d'événements Windows dans le SIEM
- [[authentication-and-authorization]] : protocoles Kerberos et NTLM
