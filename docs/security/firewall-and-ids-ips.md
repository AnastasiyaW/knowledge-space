---
title: Firewalls and IDS/IPS
category: tools
tags: [security, firewall, iptables, ids, ips, snort, suricata, waf]
---

# Firewalls and IDS/IPS

Network and application-layer security controls: iptables/ufw for Linux firewalls, Windows Defender Firewall, Snort and Suricata for intrusion detection/prevention, and WAF (ModSecurity, cloud WAFs) for web application protection.

## Key Facts
- IDS detects and alerts; IPS detects and blocks inline
- Signature-based detection is fast and accurate for known attacks but misses zero-days
- Anomaly-based detection catches novel attacks but has higher false positive rates
- Suricata is multi-threaded (faster than Snort) and compatible with Snort rules
- WAF should start in detection mode before enabling blocking to tune false positives
- iptables default policy should be DROP for INPUT, ACCEPT for OUTPUT

## iptables (Linux)

### Basic Setup
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

### ufw (Uncomplicated Firewall)
```bash
ufw enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow from 192.168.1.0/24 to any port 3306
ufw status verbose
```

## Windows Firewall
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
Profiles: Domain, Private, Public. Managed via `wf.msc` GUI or PowerShell.

## Network Firewall Architecture

### Deployment Topologies

Two fundamental approaches to firewall placement:

1. **Host-based firewall**: installed on each individual host. Each server/workstation runs its own firewall (iptables, Windows Firewall). Must be configured per host or automated via Ansible/Puppet
2. **Network firewall**: single device protecting an entire network segment. Filters transit traffic between zones. Configured once for the entire network

**Standard corporate topology**: firewall sits between the internet uplink and the LAN (server/workstation network). All traffic must pass through the firewall, which may be combined with the router.

### Network Zones

```
Internet
    |
[Firewall/Router]
    |           |
  [DMZ]       [LAN]
  (web,mail)  (internal servers, workstations)
```

- **DMZ (Demilitarized Zone)**: hosts accessible from the internet (web servers, mail). Firewall allows inbound to DMZ but blocks DMZ-to-LAN
- **LAN**: internal network. Firewall blocks all inbound from internet, allows outbound
- **Management zone**: separate VLAN for firewall/router management interfaces

### IPSet for Efficient Rule Management

IPSet creates named sets of IPs, networks, or ports that can be referenced in iptables rules. Far more efficient than individual rules for large blocklists:

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

**Performance**: iptables with 10,000 individual IP rules = O(n) per packet. IPSet with 10,000 IPs = O(1) hash lookup. For large blocklists (geo-blocking, threat intel feeds), IPSet is essential.

### Traffic Flow Through Firewall

Packet traversal order in iptables/netfilter:

```
Incoming -> PREROUTING (NAT/mangle) -> routing decision
  -> INPUT (for firewall itself)
  -> FORWARD (transit traffic to other hosts)
Outgoing -> OUTPUT -> POSTROUTING (NAT/masquerade)
```

For a network firewall, most rules go in the FORWARD chain (transit traffic). INPUT chain protects the firewall host itself.

### NAT vs Masquerading

Two methods for sharing a public IP with a LAN:

| Feature | NAT (SNAT) | Masquerading |
|---------|-----------|--------------|
| IP type | Static | Dynamic (DHCP/PPPoE) |
| Rule syntax | `--to-source <IP>` | `-j MASQUERADE` |
| Performance | Better (cached) | Slight overhead |
| Use when | Server with fixed IP | Home/VPN with dynamic IP |

```bash
# NAT with static IP (preferred for servers)
iptables -t nat -A POSTROUTING -s 10.0.0.0/16 -j SNAT --to-source 65.108.243.108

# Masquerading with dynamic IP
iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE
```

**Always prefer NAT over masquerading when you have a static IP** - it caches the source address mapping and avoids per-packet lookups.

### Complete Firewall Setup for Gateway

Step-by-step for a dual-interface gateway protecting a LAN:

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

**Critical order:** Allow SSH *before* setting DROP policy. Reversing this locks you out immediately.

### Packet Marking and Policy Routing

Route traffic by port using iptables mangle table + ip rule:

```bash
# Mark SSH packets (port 22) with mark 0x2
iptables -t mangle -A PREROUTING -i eth0 -p tcp --dport 22 -j CONNMARK --set-mark 0x2
iptables -t mangle -A OUTPUT -j CONNMARK --restore-mark

# Create routing table 120 for marked packets
ip route add default via 172.31.0.1 dev eth0 table 120

# Route marked packets through table 120
ip rule add fwmark 0x2 lookup 120
```

This sends SSH traffic through a different gateway than general traffic - useful for split routing, VPN bypass, or directing traffic through monitoring systems.

### Traffic Mirroring for IDS

Redirect traffic copies to an analysis system without affecting the original flow:

- **Small scale:** Use iptables mangle to mark and queue packets for IDS processing on the same host
- **Large scale:** Mirror traffic to a separate interface/host using `tc` (traffic control) or DPDK for high-performance packet processing
- **Tunneling:** Wrap mirrored traffic in GRE/VXLAN to preserve original headers across the network

## IDS/IPS

### Types
- **NIDS/NIPS** - network-based, monitors traffic at strategic points
- **HIDS/HIPS** - host-based, monitors activity on individual hosts
- **Signature-based** - matches known attack patterns
- **Anomaly-based** - baseline deviation detection
- **Hybrid** - combines both approaches

### Snort Rules
```
# Rule syntax: action protocol src_ip src_port -> dst_ip dst_port (options)
alert tcp any any -> $HOME_NET 80 (msg:"SQL Injection Attempt"; \
    content:"UNION SELECT"; nocase; sid:1000001; rev:1;)

alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force"; \
    flow:to_server; threshold:type both, track by_src, count 5, seconds 60; \
    sid:1000002; rev:1;)
```

Rule components: `alert`/`drop`/`log` action, protocol, source/destination, `content` string match, `pcre` regex, `flow` direction, `threshold` rate-based, `sid` unique identifier.

### Suricata
Modern multi-threaded alternative to Snort:
- Compatible with Snort rules
- EVE JSON logging (easier SIEM integration)
- Built-in protocol parsing (HTTP, TLS, DNS, SMB)
- File extraction capability
- Better performance on multi-core systems

## WAF (Web Application Firewall)

### ModSecurity
```
# Rule examples
SecRule REQUEST_URI "@contains /admin" \
    "id:1001,phase:1,deny,status:403,msg:'Admin access blocked'"

SecRule ARGS "@detectSQLi" \
    "id:1002,phase:2,deny,status:403,msg:'SQL Injection detected'"
```
- **OWASP Core Rule Set (CRS)** - comprehensive default ruleset
- Modes: detection only (log) vs blocking (deny)

### Cloud WAFs
- **AWS WAF** - integrates with CloudFront, ALB, API Gateway
- **Cloudflare WAF** - edge-based, managed rulesets
- **Azure Front Door WAF** - Microsoft cloud WAF
- Features: managed rule updates, custom rules, rate limiting, bot detection

## Gotchas
- IPS false positives can block legitimate traffic - always start in detection mode
- Snort is single-threaded - Suricata is better for high-throughput networks
- WAF bypass techniques exist for most signatures (encoding, fragmentation, case variation)
- iptables rules are processed in order - put most-matched rules first for performance
- ufw is a frontend for iptables - both cannot be managed independently without conflicts
- Cloud WAF adds latency but removes the burden of rule maintenance

## See Also
- [[network-security-and-protocols]] - underlying network fundamentals
- [[network-traffic-analysis]] - tcpdump, Wireshark
- [[web-application-security-fundamentals]] - attacks that WAFs protect against
- [[siem-and-incident-response]] - alert correlation from IDS/IPS
