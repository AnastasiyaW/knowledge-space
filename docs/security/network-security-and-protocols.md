---
title: Network Security and Protocols
category: concepts
tags: [security, networking, osi, tcp-ip, dns, dhcp, vpn, firewall]
---

# Network Security and Protocols

Network fundamentals from a security perspective: OSI model, TCP/IP stack, DNS mechanics, DHCP, VPN technologies (OpenVPN, WireGuard), and email authentication (SPF/DKIM/DMARC).

## Key Facts
- OSI model: Physical, Data Link, Network, Transport, Session, Presentation, Application
- TCP is reliable and ordered; UDP is fast and connectionless
- Private IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- DNS resolution: client cache -> /etc/hosts -> resolver cache -> root -> TLD -> authoritative
- WireGuard is simpler, faster, and more auditable than OpenVPN (4000 LOC vs 100K+)
- SPF + DKIM + DMARC together prevent email spoofing

## OSI Model (Security Relevant)
| Layer | Name | Security Concern |
|-------|------|-----------------|
| 7 | Application | HTTP, DNS, SMTP attacks, WAF |
| 4 | Transport | TCP/UDP, port scanning, SYN floods |
| 3 | Network | IP spoofing, routing attacks, firewalls |
| 2 | Data Link | ARP spoofing, MAC flooding, 802.1X |
| 1 | Physical | Wiretapping, physical access |

## TCP/IP

### TCP Three-Way Handshake

TCP establishes a reliable connection before data transfer using three steps:

```php
Client                    Server
  |--- SYN (seq=x) ------->|     Step 1: Client sends SYN with random sequence number
  |<-- SYN-ACK (seq=y, -----|     Step 2: Server responds with SYN-ACK, acknowledges x+1
  |    ack=x+1)             |
  |--- ACK (ack=y+1) ----->|     Step 3: Client acknowledges, connection established
```

**Security implications**:
- **SYN flood attack**: attacker sends many SYN packets without completing the handshake, exhausting server resources. Mitigation: SYN cookies, rate limiting
- The random sequence number prevents connection hijacking (predictable sequences were exploited historically)
- Connection teardown uses a four-step FIN handshake (FIN -> ACK -> FIN -> ACK)

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Delivery | Guaranteed, ordered | Best-effort, unordered |
| Handshake | Three-way | None |
| Overhead | Higher (headers, acks) | Minimal |
| Use cases | HTTP, SSH, email, file transfer | DNS, VoIP, streaming, gaming |
| Connection | Stateful | Stateless |

### Routing and Route Tables

Packets are forwarded based on the routing table - a set of rules mapping destination networks to next-hop gateways:

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

**Route selection**: most specific match wins (longest prefix). A packet to 10.1.2.3 matches /24 over /8 if both exist. If no specific route matches, the default gateway is used.

**Security**: unauthorized route changes can redirect traffic (route poisoning). Use RPKI/ROA for BGP route validation in production networks.

### IPv4 Subnetting (CIDR)
```text
/24 = 255.255.255.0     = 254 usable hosts
/25 = 255.255.255.128   = 126 usable hosts
/26 = 255.255.255.192   = 62 usable hosts
/16 = 255.255.0.0       = 65534 usable hosts
```

### IPv6
- 128-bit addresses: `2001:0db8:85a3::8a2e:0370:7334`
- Link-local: `fe80::/10`; Global unicast: `2000::/3`
- Native IPsec support in protocol headers
- Dual-stack environments create additional fingerprinting surface
- Many security tools still lack full IPv6 support

### Routing
```bash
ip route show
ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0
ip route add default via 192.168.1.1
traceroute example.com
mtr example.com          # Combined ping + traceroute
```

## DNS

### Record Types
| Record | Purpose |
|--------|---------|
| A / AAAA | Hostname to IPv4 / IPv6 |
| MX | Mail server (with priority) |
| CNAME | Alias to another hostname |
| TXT | Text records (SPF, DKIM, verification) |
| PTR | Reverse DNS (IP to hostname) |
| NS | Nameserver for domain |
| SOA | Zone metadata (serial, refresh, retry) |
| SRV | Service location (AD, SIP) |

### Zone File Example
```text
$TTL 3600
@    IN SOA  ns1.example.com. admin.example.com. (2024010101 3600 600 86400 3600)
@    IN NS   ns1.example.com.
@    IN A    93.184.216.34
www  IN A    93.184.216.34
@    IN MX   10 mail.example.com.
@    IN TXT  "v=spf1 mx -all"
```

### DNS Security
- Zone transfer (AXFR) should be restricted to authorized secondaries only
- DNSSEC signs DNS records to prevent tampering
- DNS-over-HTTPS (DoH) / DNS-over-TLS (DoT) encrypt DNS queries

## Email Authentication
- **SPF** - DNS TXT record listing authorized mail server IPs
- **DKIM** - cryptographic signature in email headers (proves message integrity)
- **DMARC** - policy for handling SPF/DKIM failures (none/quarantine/reject)

## VPN

### OpenVPN
```bash
# Server setup with easy-rsa for PKI
apt install openvpn easy-rsa
# Config: /etc/openvpn/server.conf
# Uses TLS for control channel, symmetric encryption for data
```

### WireGuard
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

## DHCP
```css
# /etc/dhcp/dhcpd.conf
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    default-lease-time 600;
}
```
Security: DHCP starvation attack (exhaust pool), rogue DHCP server (MITM). Defense: DHCP snooping on managed switches.

## SNMP
- v1/v2c: community strings in plaintext (essentially passwords)
- v3: authentication + encryption (always use v3)
- Exposed SNMP = full device configuration exposure

## Network Diagnostics Toolkit

Essential utilities for verifying connectivity and troubleshooting:

### ping - ICMP Reachability
```bash
# Basic connectivity check
ping -c 5 example.com

# Specify interface
ping -c 3 -I eth0 192.168.1.1

# Large packet test (MTU/fragmentation issues)
ping -c 3 -s 1400 example.com
```

**Interpretation:**
- `Destination Host Unreachable` - routing problem, check default gateway
- `Request timed out` - host is down or ICMP is blocked
- Packet loss >0% - unstable connection or congestion
- RTT variation - network jitter, check intermediate hops

**Limitation:** Many hosts block ICMP. A failed ping does not prove the host is down.

### traceroute - Path Discovery
```bash
# Trace route to destination (max 30 hops)
traceroute -m 30 example.com

# Use TCP instead of UDP (better firewall traversal)
traceroute -T -p 443 example.com
```

Shows each router hop between source and destination. Asterisks (`* * *`) indicate hops that don't respond - this is normal for routers configured to drop ICMP TTL-exceeded messages.

### dig / nslookup - DNS Verification
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

**Practical use:** After migrating a domain to a new server, query multiple public DNS servers to verify propagation:
```bash
for ns in 1.1.1.1 8.8.8.8 77.88.8.8; do
    echo "=== $ns ===" && dig @$ns example.com +short
done
```

## Gotchas
- IPv6 can leak real network information even when IPv4 is routed through VPN
- DNS queries are unencrypted by default - ISP/network admin can see all domains visited
- WireGuard does not do NAT traversal out of the box in all configurations
- DHCP logs correlate IP assignments to MAC/hostname - critical for incident investigation
- SNMPv1/v2c community strings are often "public"/"private" by default

## See Also
- [[firewall-and-ids-ips]] - iptables, Snort, Suricata
- [[network-traffic-analysis]] - tcpdump, Wireshark, nmap
- [[linux-system-hardening]] - sysctl network parameters
- [[cryptography-and-pki]] - TLS certificates, PKI
