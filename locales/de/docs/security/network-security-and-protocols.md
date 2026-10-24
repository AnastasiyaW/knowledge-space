---
title: "Netzwerksicherheit und Protokolle"
category: concepts
tags: [security, networking, osi, tcp-ip, dns, dhcp, vpn, firewall]
level: 3
source_sha256: eb064525297a1f2f65234655e88efa251c46d6c096092822e27a62f90ee73e55
translation: machine
translated_at: '2026-10-24'
---
# Netzwerksicherheit und Protokolle {#network-security-and-protocols}

Netzwerkgrundlagen aus Sicherheitsperspektive: OSI-Modell, TCP/IP-Stack, DNS-Mechanik, DHCP, VPN-Technologien (OpenVPN, WireGuard) und E-Mail-Authentifizierung (SPF/DKIM/DMARC).

## Wichtige Fakten {#key-facts}
- OSI-Modell: Bitübertragungsschicht, Sicherungsschicht, Vermittlungsschicht, Transportschicht, Sitzungsschicht, Darstellungsschicht, Anwendungsschicht
- TCP ist zuverlässig und geordnet; UDP ist schnell und verbindungslos
- Private IP-Bereiche: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- DNS-Auflösung: Client-Cache -> /etc/hosts -> Resolver-Cache -> Root -> TLD -> autoritativer Server
- WireGuard ist einfacher, schneller und besser prüfbar als OpenVPN (4000 LOC gegenüber 100K+)
- SPF + DKIM + DMARC zusammen verhindern E-Mail-Spoofing

## OSI-Modell (sicherheitsrelevant) {#osi-model-security-relevant}
| Schicht | Name | Sicherheitsrelevante Aspekte |
|-------|------|-----------------|
| 7 | Anwendung | HTTP-, DNS-, SMTP-Angriffe, WAF |
| 4 | Transport | TCP/UDP, Port-Scanning, SYN-Floods |
| 3 | Vermittlung | IP-Spoofing, Routing-Angriffe, Firewalls |
| 2 | Sicherung | ARP-Spoofing, MAC-Flooding, 802.1X |
| 1 | Bitübertragung | Abhören von Leitungen, physischer Zugriff |

## TCP/IP {#tcpip}

### TCP-Three-Way-Handshake {#tcp-three-way-handshake}

TCP baut vor der Datenübertragung in drei Schritten eine zuverlässige Verbindung auf:

```php
Client                    Server
  |--- SYN (seq=x) ------->|     Step 1: Client sends SYN with random sequence number
  |<-- SYN-ACK (seq=y, -----|     Step 2: Server responds with SYN-ACK, acknowledges x+1
  |    ack=x+1)             |
  |--- ACK (ack=y+1) ----->|     Step 3: Client acknowledges, connection established
```

**Sicherheitsimplikationen**:
- **SYN-Flood-Angriff**: Ein Angreifer sendet viele SYN-Pakete, ohne den Handshake abzuschließen, und erschöpft so die Ressourcen des Servers. Gegenmaßnahmen: SYN-Cookies, Ratenbegrenzung
- Die zufällige Sequenznummer verhindert Connection-Hijacking (vorhersagbare Sequenznummern wurden historisch ausgenutzt)
- Der Verbindungsabbau erfolgt über einen vierstufigen FIN-Handshake (FIN -> ACK -> FIN -> ACK)

### TCP vs. UDP {#tcp-vs-udp}

| Merkmal | TCP | UDP |
|---------|-----|-----|
| Zustellung | Garantiert, geordnet | Best-Effort, ungeordnet |
| Handshake | Three-Way | Keiner |
| Overhead | Höher (Header, Bestätigungen) | Minimal |
| Anwendungsfälle | HTTP, SSH, E-Mail, Dateiübertragung | DNS, VoIP, Streaming, Gaming |
| Verbindung | Zustandsbehaftet | Zustandslos |

### Routing und Routing-Tabellen {#routing-and-route-tables}

Pakete werden anhand der Routing-Tabelle weitergeleitet – einer Menge von Regeln, die Zielnetze auf Next-Hop-Gateways abbilden:

```bash
# View routing table
ip route show
# or legacy:
route -n

# Typical output:
# default via 192.168.1.1 dev eth0    <- default gateway
# 192.168.1.0/24 dev eth0 scope link  <- directly connected network
# 10.0.0.0/8 via 192.168.1.254 dev eth0  <- static route

# Add static route
ip route add 10.0.0.0/8 via 192.168.1.254 dev eth0

# Delete route
ip route del 10.0.0.0/8
```

**Routenauswahl**: Die spezifischste Übereinstimmung gewinnt (längstes Präfix). Ein Paket an 10.1.2.3 passt auf /24 besser als auf /8, wenn beide Routen existieren. Passt keine spezifische Route, wird das Standard-Gateway verwendet.

**Sicherheit**: Nicht autorisierte Routenänderungen können Datenverkehr umleiten (Route Poisoning). In produktiven Netzen sollte RPKI/ROA zur Validierung von BGP-Routen eingesetzt werden.

### IPv4-Subnetting (CIDR) {#ipv4-subnetting-cidr}
```text
/24 = 255.255.255.0     = 254 usable hosts
/25 = 255.255.255.128   = 126 usable hosts
/26 = 255.255.255.192   = 62 usable hosts
/16 = 255.255.0.0       = 65534 usable hosts
```

### IPv6 {#ipv6}
- 128-Bit-Adressen: `2001:0db8:85a3::8a2e:0370:7334`
- Link-lokal: `fe80::/10`; Global Unicast: `2000::/3`
- Native IPsec-Unterstützung in den Protokoll-Headern
- Dual-Stack-Umgebungen erzeugen zusätzliche Angriffsfläche für Fingerprinting
- Viele Sicherheitswerkzeuge bieten noch keine vollständige IPv6-Unterstützung

### Routing {#routing}
```bash
ip route show
ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0
ip route add default via 192.168.1.1
traceroute example.com
mtr example.com          # Combined ping + traceroute
```

## DNS {#dns}

### Record-Typen {#record-types}
| Record | Zweck |
|--------|---------|
| A / AAAA | Hostname zu IPv4 / IPv6 |
| MX | Mailserver (mit Priorität) |
| CNAME | Alias auf einen anderen Hostnamen |
| TXT | Textrecords (SPF, DKIM, Verifizierung) |
| PTR | Reverse-DNS (IP zu Hostname) |
| NS | Nameserver der Domain |
| SOA | Zonen-Metadaten (Seriennummer, Refresh, Retry) |
| SRV | Dienstlokalisierung (AD, SIP) |

### Beispiel einer Zonendatei {#zone-file-example}
```text
$TTL 3600
@    IN SOA  ns1.example.com. admin.example.com. (2024010101 3600 600 86400 3600)
@    IN NS   ns1.example.com.
@    IN A    93.184.216.34
www  IN A    93.184.216.34
@    IN MX   10 mail.example.com.
@    IN TXT  "v=spf1 mx -all"
```

### DNS-Sicherheit {#dns-security}
- Zonentransfers (AXFR) sollten nur auf autorisierte Secondary-Server beschränkt werden
- DNSSEC signiert DNS-Records, um Manipulationen zu verhindern
- DNS-over-HTTPS (DoH) bzw. DNS-over-TLS (DoT) verschlüsseln DNS-Anfragen

## E-Mail-Authentifizierung {#email-authentication}
- **SPF** – DNS-TXT-Record mit den IPs der autorisierten Mailserver
- **DKIM** – kryptografische Signatur in den E-Mail-Headern (belegt die Integrität der Nachricht)
- **DMARC** – Richtlinie für den Umgang mit SPF-/DKIM-Fehlschlägen (none/quarantine/reject)

## VPN {#vpn}

### OpenVPN {#openvpn}
```bash
# Server setup with easy-rsa for PKI
apt install openvpn easy-rsa
# Config: /etc/openvpn/server.conf
# Uses TLS for control channel, symmetric encryption for data
```

### WireGuard {#wireguard}
```bash
apt install wireguard
wg genkey | tee privatekey | wg pubkey > publickey

# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

wg-quick up wg0
```

## DHCP {#dhcp}
```css
# /etc/dhcp/dhcpd.conf
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    default-lease-time 600;
}
```
Sicherheit: DHCP-Starvation-Angriff (Pool erschöpfen), nicht autorisierter DHCP-Server (MITM). Abwehr: DHCP-Snooping auf verwalteten Switches.

## SNMP {#snmp}
- v1/v2c: Community-Strings im Klartext (praktisch Passwörter)
- v3: Authentifizierung und Verschlüsselung (immer v3verwenden)
- Offenes SNMP bedeutet vollständige Offenlegung der Gerätekonfiguration

## Werkzeuge zur Netzwerkdiagnose {#network-diagnostics-toolkit}

Wichtige Hilfsprogramme zur Überprüfung der Konnektivität und zur Fehlersuche:

### ping - ICMP-Erreichbarkeit {#ping-icmp-reachability}
```bash
# Basic connectivity check
ping -c 5 example.com

# Specify interface
ping -c 3 -I eth0 192.168.1.1

# Large packet test (MTU/fragmentation issues)
ping -c 3 -s 1400 example.com
```

**Interpretation:**
- `Destination Host Unreachable` – Routing-Problem, Standard-Gateway prüfen
- `Request timed out` – Host ist nicht erreichbar oder ICMP ist blockiert
- Paketverlust >0 % – instabile Verbindung oder Überlastung
- RTT-Schwankungen – Netzwerk-Jitter, Zwischenstationen prüfen

**Einschränkung:** Viele Hosts blockieren ICMP. Ein fehlgeschlagenes Ping beweist nicht, dass der Host ausgefallen ist.

### traceroute - Pfaderkennung {#traceroute-path-discovery}
```bash
# Trace route to destination (max 30 hops)
traceroute -m 30 example.com

# Use TCP instead of UDP (better firewall traversal)
traceroute -T -p 443 example.com
```

Zeigt jeden Router-Hop zwischen Quelle und Ziel. Sternchen (`* * *`) kennzeichnen Hops, die nicht antworten – das ist normal bei Routern, die ICMP-TTL-Exceeded-Meldungen verwerfen.

### dig / nslookup - DNS-Überprüfung {#dig-nslookup-dns-verification}
```bash
# Query default resolver
dig example.com

# Query specific nameserver
dig @1.1.1.1 example.com

# Reverse DNS lookup
dig -x 8.8.8.8

# Check a specific record type
dig example.com MX
dig example.com TXT
```

```bash
# nslookup equivalent
nslookup example.com
nslookup example.com 8.8.8.8  # query specific server
nslookup -type=PTR 8.8.8.8    # reverse lookup
```

**Praktische Anwendung:** Nach der Migration einer Domain auf einen neuen Server kann man mehrere öffentliche DNS-Server abfragen, um die Propagierung zu überprüfen:
```bash
for ns in 1.1.1.1 8.8.8.8 77.88.8.8; do
    echo "=== $ns ===" && dig @$ns example.com +short
done
```

## Fallstricke {#gotchas}
- IPv6 kann reale Netzwerkinformationen preisgeben, selbst wenn IPv4 über das VPN geroutet wird
- DNS-Anfragen sind standardmäßig unverschlüsselt – ISP bzw. Netzwerkadministrator können alle besuchten Domains sehen
- WireGuard unterstützt in manchen Konfigurationen kein NAT-Traversal out of the box
- DHCP-Logs verknüpfen IP-Zuweisungen mit MAC-Adressen und Hostnamen – entscheidend für die Incident-Analyse
- SNMPv1/v2c-Community-Strings lauten standardmäßig oft „public“ bzw. „private“

## Siehe auch {#see-also}
- [[firewall-and-ids-ips]] - iptables, Snort, Suricata
- [[network-traffic-analysis]] - tcpdump, Wireshark, nmap
- [[linux-system-hardening]] - sysctl-Netzwerkparameter
- [[cryptography-and-pki]] - TLS-Zertifikate, PKI
