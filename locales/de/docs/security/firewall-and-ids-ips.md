---
title: "Firewalls und IDS/IPS"
category: tools
tags: [security, firewall, iptables, ids, ips, snort, suricata, waf]
level: 3
source_sha256: 0c5604db383747a88091cf3a2244f0213e2b39fe661b37a5e6115444a9b5bfc7
translation: machine
translated_at: '2026-10-24'
---
# Firewalls und IDS/IPS {#firewalls-and-idsips}

Sicherheitskontrollen auf Netzwerk- und Anwendungsebene: iptables/ufw für Linux-Firewalls, die Windows-Defender-Firewall, Snort und Suricata für Intrusion Detection/Prevention sowie WAF (ModSecurity, Cloud-WAFs) zum Schutz von Webanwendungen.

## Wichtige Fakten {#key-facts}
- IDS erkennt und alarmiert; IPS erkennt und blockiert inline
- Signaturbasierte Erkennung ist schnell und präzise bei bekannten Angriffen, übersieht aber Zero-Day-Angriffe
- Anomaliebasierte Erkennung findet neuartige Angriffe, weist aber höhere Raten an Fehlalarmen (False Positives) auf
- Suricata ist multithreaded (schneller als Snort) und kompatibel mit Snort-Regeln
- Eine WAF sollte zunächst im Erkennungsmodus betrieben werden, bevor das Blockieren aktiviert wird, um Fehlalarme zu justieren
- Die Default-Policy von iptables sollte für INPUT auf DROP und für OUTPUT auf ACCEPT stehen

## iptables (Linux) {#iptables-linux}

### Grundeinrichtung {#basic-setup}
```bash
# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH, HTTP, HTTPS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Drop invalid packets
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# Rate limiting (SSH brute force protection)
iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/min --limit-burst 3 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP

# NAT masquerading
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Logging dropped packets
iptables -A INPUT -j LOG --log-prefix "DROPPED: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### ufw (Uncomplicated Firewall) {#ufw-uncomplicated-firewall}
```bash
ufw enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow from 192.168.1.0/24 to any port 3306
ufw status verbose
```

## Windows-Firewall {#windows-firewall}
```powershell
# View enabled rules
Get-NetFirewallRule | Where-Object {$_.Enabled -eq 'True'} |
    Select-Object DisplayName, Direction, Action

# Create rule
New-NetFirewallRule -DisplayName "Block Telnet" -Direction Inbound `
    -Protocol TCP -LocalPort 23 -Action Block

# Enable/disable
Enable-NetFirewallRule -DisplayName "Block Telnet"
Disable-NetFirewallRule -DisplayName "Block Telnet"
```
Profile: Domäne, Privat, Öffentlich. Verwaltung über die GUI `wf.msc` oder PowerShell.

## Architektur von Netzwerk-Firewalls {#network-firewall-architecture}

### Bereitstellungstopologien {#deployment-topologies}

Zwei grundlegende Ansätze für die Platzierung von Firewalls:

1. **Host-basierte Firewall**: auf jedem einzelnen Host installiert. Jeder Server bzw. jede Workstation betreibt eine eigene Firewall (iptables, Windows-Firewall). Muss pro Host konfiguriert oder über Ansible/Puppet automatisiert werden
2. **Netzwerk-Firewall**: einzelnes Gerät, das ein gesamtes Netzwerksegment schützt. Filtert den Transitverkehr zwischen Zonen. Wird einmal für das gesamte Netzwerk konfiguriert

**Übliche Unternehmenstopologie**: Die Firewall sitzt zwischen dem Internet-Uplink und dem LAN (Server- bzw. Workstation-Netz). Der gesamte Verkehr muss die Firewall passieren, die auch mit dem Router kombiniert sein kann.

### Netzwerkzonen {#network-zones}

```text
Internet
    |
[Firewall/Router]
    |           |
  [DMZ]       [LAN]
  (web,mail)  (internal servers, workstations)
```

- **DMZ (Demilitarisierte Zone)**: Hosts, die aus dem Internet erreichbar sind (Webserver, Mailserver). Die Firewall erlaubt eingehenden Verkehr in die DMZ, blockiert aber DMZ-zu-LAN
- **LAN**: internes Netzwerk. Die Firewall blockiert sämtlichen eingehenden Verkehr aus dem Internet und erlaubt ausgehenden Verkehr
- **Management-Zone**: separates VLAN für die Management-Schnittstellen von Firewall und Router

### IPSet für effiziente Regelverwaltung {#ipset-for-efficient-rule-management}

IPSet legt benannte Mengen von IPs, Netzen oder Ports an, die in iptables-Regeln referenziert werden können. Für große Blocklisten deutlich effizienter als einzelne Regeln:

```bash
# Create a set for blocked IPs
ipset create blocklist hash:ip

# Add entries
ipset add blocklist 203.0.113.5
ipset add blocklist 198.51.100.0/24

# Reference in iptables
iptables -A INPUT -m set --match-set blocklist src -j DROP

# List set contents
ipset list blocklist

# Save/restore (persistent across reboots)
ipset save > /etc/ipset.conf
ipset restore < /etc/ipset.conf
```

**Performance**: iptables mit 10.000 einzelnen IP-Regeln entspricht O(n) pro Paket. IPSet mit 10.000 IPs entspricht einem O(1)-Hash-Lookup. Für große Blocklisten (Geo-Blocking, Threat-Intel-Feeds) ist IPSet unverzichtbar.

### Paketdurchlauf durch die Firewall {#traffic-flow-through-firewall}

Reihenfolge der Paketverarbeitung in iptables/netfilter:

```php
Incoming -> PREROUTING (NAT/mangle) -> routing decision
  -> INPUT (for firewall itself)
  -> FORWARD (transit traffic to other hosts)
Outgoing -> OUTPUT -> POSTROUTING (NAT/masquerade)
```

Bei einer Netzwerk-Firewall gehört der größte Teil der Regeln in die FORWARD-Chain (Transitverkehr). Die INPUT-Chain schützt den Firewall-Host selbst.

### NAT vs. Masquerading {#nat-vs-masquerading}

Zwei Methoden, eine öffentliche IP für ein LAN gemeinsam zu nutzen:

| Merkmal | NAT (SNAT) | Masquerading |
|---------|-----------|--------------|
| IP-Typ | Statisch | Dynamisch (DHCP/PPPoE) |
| Regelsyntax | `--to-source <IP>` | `-j MASQUERADE` |
| Performance | Besser (gecacht) | Leicht erhöhter Overhead |
| Einsatz bei | Server mit fester IP | Heimnetz/VPN mit dynamischer IP |

```bash
# NAT with static IP (preferred for servers)
iptables -t nat -A POSTROUTING -s 10.0.0.0/16 -j SNAT --to-source 65.108.243.108

# Masquerading with dynamic IP
iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE
```

**Bei einer statischen IP ist immer NAT dem Masquerading vorzuziehen** – es speichert die Zuordnung der Quelladresse im Cache und vermeidet so Lookups für jedes Paket.

### Vollständige Firewall-Konfiguration für ein Gateway {#complete-firewall-setup-for-gateway}

Schrittweise Anleitung für ein Gateway mit zwei Schnittstellen, das ein LAN schützt:

```bash
# 1. Enable IP forwarding (persistent)
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

# 2. Allow SSH before setting DROP policy (avoid lockout!)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 3. Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 4. Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 5. NAT for LAN
iptables -t nat -A POSTROUTING -s 10.0.0.0/16 -j SNAT --to-source <PUBLIC_IP>

# 6. Allow LAN to internet (FORWARD chain)
iptables -A FORWARD -s 10.0.0.0/16 -j ACCEPT
iptables -A FORWARD -d 10.0.0.0/16 -m state --state ESTABLISHED,RELATED -j ACCEPT

# 7. Save rules
iptables-save > /etc/iptables/rules.v4
```

**Kritische Reihenfolge:** SSH *vor* dem Setzen der DROP-Policy erlauben. Die umgekehrte Reihenfolge sperrt sofort aus.

### Paketmarkierung und Policy-Routing {#packet-marking-and-policy-routing}

Verkehr anhand des Ports mit der mangle-Tabelle von iptables und `ip rule` routen:

```bash
# Mark SSH packets (port 22) with mark 0x2
iptables -t mangle -A PREROUTING -i eth0 -p tcp --dport 22 -j CONNMARK --set-mark 0x2
iptables -t mangle -A OUTPUT -j CONNMARK --restore-mark

# Create routing table 120 for marked packets
ip route add default via 172.31.0.1 dev eth0 table 120

# Route marked packets through table 120
ip rule add fwmark 0x2 lookup 120
```

Damit wird SSH-Verkehr über ein anderes Gateway geleitet als der allgemeine Verkehr – nützlich für Split-Routing, VPN-Umgehung oder das Leiten von Verkehr über Monitoring-Systeme.

### Traffic-Mirroring für IDS {#traffic-mirroring-for-ids}

Kopien des Verkehrs an ein Analysesystem umleiten, ohne den ursprünglichen Fluss zu beeinflussen:

- **Kleine Umgebung:** iptables-mangle verwenden, um Pakete zu markieren und für die IDS-Verarbeitung auf demselben Host in eine Queue zu stellen
- **Große Umgebung:** Verkehr mit `tc` (Traffic Control) oder DPDK für performante Paketverarbeitung auf eine separate Schnittstelle bzw. einen separaten Host spiegeln
- **Tunnelung:** gespiegelten Verkehr in GRE/VXLAN kapseln, damit die ursprünglichen Header über das Netzwerk erhalten bleiben

## IDS/IPS {#idsips}

### Typen {#types}
- **NIDS/NIPS** – netzwerkbasiert, überwacht den Verkehr an strategischen Punkten
- **HIDS/HIPS** – hostbasiert, überwacht die Aktivität auf einzelnen Hosts
- **Signaturbasiert** – gleicht mit bekannten Angriffsmustern ab
- **Anomaliebasiert** – Erkennung von Abweichungen von einer Baseline
- **Hybrid** – kombiniert beide Ansätze

### Snort-Regeln {#snort-rules}
```bash
# Rule syntax: action protocol src_ip src_port -> dst_ip dst_port (options)
alert tcp any any -> $HOME_NET 80 (msg:"SQL Injection Attempt"; \
    content:"UNION SELECT"; nocase; sid:1000001; rev:1;)

alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force"; \
    flow:to_server; threshold:type both, track by_src, count 5, seconds 60; \
    sid:1000002; rev:1;)
```

Bestandteile einer Regel: Aktion `alert`/`drop`/`log`, Protokoll, Quelle/Ziel, `content`-Zeichenkettenabgleich, `pcre`-Regex, `flow`-Richtung, `threshold` für ratenbasierte Auswertung, `sid` als eindeutige Kennung.

### Suricata {#suricata}
Moderne, multithreaded Alternative zu Snort:
- Kompatibel mit Snort-Regeln
- EVE-JSON-Logging (einfachere SIEM-Integration)
- Integrierte Protokollanalyse (HTTP, TLS, DNS, SMB)
- Extraktion von Dateien möglich
- Bessere Performance auf Mehrkernsystemen

## WAF (Web Application Firewall) {#waf-web-application-firewall}

### ModSecurity {#modsecurity}
```markdown
# Rule examples
SecRule REQUEST_URI "@contains /admin" \
    "id:1001,phase:1,deny,status:403,msg:'Admin access blocked'"

SecRule ARGS "@detectSQLi" \
    "id:1002,phase:2,deny,status:403,msg:'SQL Injection detected'"
```
- **OWASP Core Rule Set (CRS)** – umfassendes Standard-Regelwerk
- Modi: nur Erkennung (Logging) vs. Blockieren (Deny)

### Cloud-WAFs {#cloud-wafs}
- **AWS WAF** – integriert in CloudFront, ALB, API Gateway
- **Cloudflare WAF** – edge-basiert, verwaltete Regelsets
- **Azure Front Door WAF** – Cloud-WAF von Microsoft
- Funktionen: verwaltete Regel-Updates, eigene Regeln, Ratenbegrenzung, Bot-Erkennung

## Stolperfallen {#gotchas}
- IPS-Fehlalarme können legitimen Verkehr blockieren – immer zuerst im Erkennungsmodus starten
- Snort ist single-threaded – für Netze mit hohem Durchsatz ist Suricata besser geeignet
- Für die meisten Signaturen existieren WAF-Umgehungstechniken (Encoding, Fragmentierung, Groß-/Kleinschreibung)
- iptables-Regeln werden der Reihe nach abgearbeitet – häufig getroffene Regeln zuerst platzieren, um die Performance zu verbessern
- ufw ist ein Frontend für iptables – beide lassen sich nicht unabhängig voneinander verwalten, ohne Konflikte zu erzeugen
- Eine Cloud-WAF verursacht zusätzliche Latenz, nimmt aber die Last der Regelpflege ab

## Siehe auch {#see-also}
- [[network-security-and-protocols]] – zugrunde liegende Netzwerkgrundlagen
- [[network-traffic-analysis]] – tcpdump, Wireshark
- [[web-application-security-fundamentals]] – Angriffe, gegen die WAFs schützen
- [[siem-and-incident-response]] – Alarmkorrelation aus IDS/IPS
