---
title: "Analyse du trafic réseau"
category: tools
tags: [security, tcpdump, wireshark, nmap, packet-analysis, forensics]
level: 3
source_sha256: 9594a2b031f379ab96af91f3b8c24c8bc214baa76cfde58e3a3e223af36557e2
translation: machine
translated_at: '2026-10-24'
---
# Analyse du trafic réseau {#network-traffic-analysis}

Capture et analyse de paquets avec tcpdump et Wireshark, scan de ports avec nmap, et outils de diagnostic réseau. Compétences essentielles pour la détection de menaces, l'investigation d'incidents et la criminalistique réseau.

## Faits clés {#key-facts}
- tcpdump capture les paquets en ligne de commande ; Wireshark fournit une analyse graphique
- Les filtres de capture de Wireshark (syntaxe BPF) filtrent pendant la capture ; les filtres d'affichage filtrent pour la visualisation
- Les scripts NSE de nmap étendent le scan avec des contrôles de vulnérabilités et de l'énumération
- Les fichiers pcap sont le format standard des captures de paquets (utilisables à la fois par tcpdump et Wireshark)
- La prise d'empreinte de la pile TCP/IP révèle le système d'exploitation, même à travers un VPN (outil p0f)

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
- **Filtres de capture** (syntaxe BPF) : `host 10.0.0.1 and port 443`
- **Filtres d'affichage** : `http.request.method == "POST"`, `tcp.flags.syn == 1`, `dns.qry.name contains "evil"`
- **Follow TCP Stream** : reconstruit la conversation complète
- **Hiérarchie des protocoles** : affiche la répartition du trafic par protocole
- **Expert Info** : identifie automatiquement les anomalies
- **Statistiques Conversations** / **Points de terminaison**

### Filtres d'affichage utiles {#useful-display-filters}
```bash
http.request.method == "POST"          # HTTP POST requests
tcp.flags.syn == 1 && tcp.flags.ack == 0   # SYN packets (new connections)
dns.qry.name contains "malicious"     # DNS queries for domain
tls.handshake.type == 1               # TLS ClientHello
ip.addr == 10.0.0.0/8                 # Internal traffic
tcp.analysis.retransmission           # Retransmissions (network issues)
```

## nmap (scan réseau) {#nmap-network-scanning}
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

## Prise d'empreinte de la pile TCP/IP {#tcpip-stack-fingerprinting}
Les détails d'implémentation au niveau du système d'exploitation transparaissent dans l'analyse des paquets :
- TTL initial (Linux : 64, Windows : 128)
- Taille de la fenêtre TCP
- Ordre des options TCP
- Comportement du bit Don't Fragment

Outil : `p0f` détecte le système d'exploitation passivement, même à travers un VPN (le VPN encapsule au niveau L3 et plus, tandis que les paramètres TCP proviennent du système d'exploitation source).

## Diagnostic réseau {#network-diagnostics}
```bash
ping -c 4 host                # ICMP connectivity test
traceroute host               # Path tracing
mtr host                      # Combined ping + traceroute (live)
dig example.com               # DNS lookup
ss -tulnp                     # Listening sockets with processes
lsof -i :80                   # What process is using port 80
netstat -tulnp                # Legacy equivalent of ss
```

## Pièges courants {#gotchas}
- Les captures de paquets peuvent contenir des données sensibles (mots de passe en clair dans HTTP, jetons de session) : à traiter comme confidentielles
- Les fichiers pcap volumineux consomment beaucoup d'espace disque : filtrer pendant la capture lorsque c'est possible
- Les scans nmap génèrent un trafic réseau important et peuvent déclencher des alertes IDS/IPS
- Le scan UDP (`nmap -sU`) est très lent, car les ports fermés ne répondent pas
- Les filtres d'affichage et les filtres de capture de Wireshark utilisent une syntaxe différente (erreur fréquente)

## Voir aussi {#see-also}
- [[firewall-and-ids-ips]] - IDS/IPS qui analysent le trafic réseau
- [[penetration-testing-methodology]] - nmap dans le contexte des tests d'intrusion
- [[network-security-and-protocols]] - bases des protocoles
- [[siem-and-incident-response]] - journaux réseau dans le SIEM
