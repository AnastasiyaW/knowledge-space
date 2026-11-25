---
title: "Netzwerkverkehrsanalyse"
category: tools
tags: [security, tcpdump, wireshark, nmap, packet-analysis, forensics]
level: 3
source_sha256: 9594a2b031f379ab96af91f3b8c24c8bc214baa76cfde58e3a3e223af36557e2
translation: machine
translated_at: '2026-10-24'
---
# Netzwerkverkehrsanalyse {#network-traffic-analysis}

Paketmitschnitt und -analyse mit tcpdump und Wireshark, Portscans mit nmap sowie Netzwerkdiagnosewerkzeuge. Unverzichtbare Fähigkeiten für die Erkennung von Bedrohungen, die Untersuchung von Vorfällen und die Netzwerkforensik.

## Wichtige Fakten {#key-facts}
- tcpdump zeichnet Pakete auf der Kommandozeile auf; Wireshark bietet eine grafische Analyseoberfläche
- Wireshark-Capture-Filter (BPF-Syntax) filtern während der Aufzeichnung; Display-Filter dienen dem Filtern zur Anzeige
- nmap-NSE-Skripte erweitern das Scanning um Schwachstellenprüfungen und Enumeration
- pcap-Dateien sind das Standardformat für Paketmitschnitte (verwendbar sowohl mit tcpdump als auch mit Wireshark)
- TCP/IP-Stack-Fingerprinting verrät das Betriebssystem selbst über VPN (Werkzeug p0f)

## tcpdump {#tcpdump}
```bash
tcpdump -i eth0                         # Capture on interface
tcpdump -i eth0 port 80                 # Filter by port
tcpdump -i eth0 host 192.168.1.100      # Filter by host
tcpdump -i eth0 -w capture.pcap         # Save to file
tcpdump -r capture.pcap                 # Read capture file
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets only
tcpdump -i eth0 -n -c 100 port 443     # No DNS resolve, limit to 100 packets
```

## Wireshark {#wireshark}
- **Capture-Filter** (BPF-Syntax): `host 10.0.0.1 and port 443`
- **Display-Filter**: `http.request.method == "POST"`, `tcp.flags.syn == 1`, `dns.qry.name contains "evil"`
- **Follow TCP Stream** - rekonstruiert die vollständige Kommunikation
- **Protocol Hierarchy** - zeigt die Verteilung des Verkehrs nach Protokoll
- **Expert Info** - erkennt Anomalien automatisch
- **Conversations** / **Endpoints** Statistiken

### Nützliche Display-Filter {#useful-display-filters}
```bash
http.request.method == "POST"          # HTTP POST requests
tcp.flags.syn == 1 && tcp.flags.ack == 0   # SYN packets (new connections)
dns.qry.name contains "malicious"     # DNS queries for domain
tls.handshake.type == 1               # TLS ClientHello
ip.addr == 10.0.0.0/8                 # Internal traffic
tcp.analysis.retransmission           # Retransmissions (network issues)
```

## nmap (Netzwerkscanning) {#nmap-network-scanning}
```bash
nmap host                    # Default scan (top 1000 ports)
nmap -sS host                # SYN scan (stealth, requires root)
nmap -sV host                # Service version detection
nmap -O host                 # OS detection
nmap -A host                 # Aggressive (OS + version + scripts + traceroute)
nmap -p- host                # All 65535 ports
nmap -sU host                # UDP scan
nmap -sn 192.168.1.0/24     # Host discovery only

# NSE scripts
nmap --script vuln host              # Vulnerability scripts
nmap --script smb-vuln-ms17-010 host # Specific CVE
nmap --script http-enum host         # HTTP directory enum
```

## TCP/IP-Stack-Fingerprinting {#tcpip-stack-fingerprinting}
Implementierungsdetails des Betriebssystems werden durch die Paketanalyse sichtbar:
- Initiale TTL (Linux: 64, Windows: 128)
- TCP-Fenstergröße
- Reihenfolge der TCP-Optionen
- Verhalten des Don't-Fragment-Bits

Werkzeug: `p0f` erkennt das Betriebssystem passiv, auch hinter einem VPN (das VPN kapselt auf Layer 3 und höher, die TCP-Parameter stammen vom Quell-Betriebssystem).

## Netzwerkdiagnose {#network-diagnostics}
```bash
ping -c 4 host                # ICMP connectivity test
traceroute host               # Path tracing
mtr host                      # Combined ping + traceroute (live)
dig example.com               # DNS lookup
ss -tulnp                     # Listening sockets with processes
lsof -i :80                   # What process is using port 80
netstat -tulnp                # Legacy equivalent of ss
```

## Stolperfallen {#gotchas}
- Paketmitschnitte können sensible Daten enthalten (Passwörter in unverschlüsseltem HTTP, Session-Token) - als vertraulich behandeln
- Große pcap-Dateien belegen erheblichen Speicherplatz - nach Möglichkeit bereits während der Aufzeichnung filtern
- nmap-Scans erzeugen erheblichen Netzwerkverkehr und können IDS/IPS-Alarme auslösen
- UDP-Scanning (`nmap -sU`) ist sehr langsam, weil geschlossene Ports nicht antworten
- Wireshark-Display-Filter und Capture-Filter verwenden unterschiedliche Syntax (häufiger Fehler)

## Siehe auch {#see-also}
- [[firewall-and-ids-ips]] - IDS/IPS, die Netzwerkverkehr analysieren
- [[penetration-testing-methodology]] - nmap im Kontext von Penetrationstests
- [[network-security-and-protocols]] - Grundlagen der Protokolle
- [[siem-and-incident-response]] - Netzwerklogs im SIEM
