---
title: Network Traffic Analysis
category: tools
tags: [security, tcpdump, wireshark, nmap, packet-analysis, forensics]
---

# Network Traffic Analysis

Packet capture and analysis with tcpdump and Wireshark, port scanning with nmap, and network diagnostic tools. Essential skills for threat detection, incident investigation, and network forensics.

## Key Facts
- tcpdump captures packets on the command line; Wireshark provides GUI analysis
- Wireshark capture filters (BPF syntax) filter during capture; display filters filter for viewing
- nmap NSE scripts extend scanning with vulnerability checks and enumeration
- pcap files are the standard format for packet captures (usable by both tcpdump and Wireshark)
- TCP/IP stack fingerprinting reveals OS even through VPN (p0f tool)

## tcpdump
```bash
tcpdump -i eth0                         # Capture on interface
tcpdump -i eth0 port 80                 # Filter by port
tcpdump -i eth0 host 192.168.1.100      # Filter by host
tcpdump -i eth0 -w capture.pcap         # Save to file
tcpdump -r capture.pcap                 # Read capture file
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets only
tcpdump -i eth0 -n -c 100 port 443     # No DNS resolve, limit to 100 packets
```

## Wireshark
- **Capture filters** (BPF syntax): `host 10.0.0.1 and port 443`
- **Display filters**: `http.request.method == "POST"`, `tcp.flags.syn == 1`, `dns.qry.name contains "evil"`
- **Follow TCP Stream** - reconstructs full conversation
- **Protocol hierarchy** - shows traffic distribution by protocol
- **Expert Info** - automatically identifies anomalies
- **Conversations** / **Endpoints** statistics

### Useful Display Filters
```
http.request.method == "POST"          # HTTP POST requests
tcp.flags.syn == 1 && tcp.flags.ack == 0   # SYN packets (new connections)
dns.qry.name contains "malicious"     # DNS queries for domain
tls.handshake.type == 1               # TLS ClientHello
ip.addr == 10.0.0.0/8                 # Internal traffic
tcp.analysis.retransmission           # Retransmissions (network issues)
```

## nmap (Network Scanning)
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

## TCP/IP Stack Fingerprinting
OS-level implementation details leak through packet analysis:
- Initial TTL (Linux: 64, Windows: 128)
- TCP window size
- TCP options ordering
- Don't Fragment bit behavior

Tool: `p0f` detects OS passively even through VPN (VPN encapsulates at L3+, TCP parameters originate from source OS).

## Network Diagnostics
```bash
ping -c 4 host                # ICMP connectivity test
traceroute host               # Path tracing
mtr host                      # Combined ping + traceroute (live)
dig example.com               # DNS lookup
ss -tulnp                     # Listening sockets with processes
lsof -i :80                   # What process is using port 80
netstat -tulnp                # Legacy equivalent of ss
```

## Gotchas
- Packet captures can contain sensitive data (passwords in plaintext HTTP, session tokens) - handle as confidential
- Large pcap files consume significant disk space - filter during capture when possible
- nmap scans generate significant network traffic and may trigger IDS/IPS alerts
- UDP scanning (`nmap -sU`) is very slow because closed ports don't respond
- Wireshark display filters and capture filters use different syntax (common mistake)

## See Also
- [[firewall-and-ids-ips]] - IDS/IPS that analyze network traffic
- [[penetration-testing-methodology]] - nmap in pentesting context
- [[network-security-and-protocols]] - protocol fundamentals
- [[siem-and-incident-response]] - network logs in SIEM
