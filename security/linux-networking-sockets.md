---
title: Linux Networking and Sockets
category: network-security
tags: [linux, sockets, networking, tcp, udp, firewall, iptables]
---

# Linux Networking and Sockets

## Key Facts

- Sockets provide inter-process communication (IPC) - processes exchange data locally (Unix domain sockets) or over network (TCP/UDP sockets)
- Socket types: stream (TCP, reliable ordered), datagram (UDP, unreliable unordered), raw (direct IP access, requires root)
- Unix domain sockets use filesystem paths instead of IP:port - faster than TCP loopback for local IPC
- `netstat -tlnp` / `ss -tlnp` shows listening TCP sockets with associated processes
- iptables/nftables: kernel-level packet filtering firewall - controls network access at the lowest level
- [[linux-kernel-security]] manages network stack in kernel space; socket API bridges to user space
- [[network-identifiers]] are the external view of what sockets expose internally

## Patterns

```bash
# Socket and network diagnostics
ss -tlnp                  # TCP listening sockets with process names
ss -tunp                  # All TCP/UDP connections
netstat -tlnp             # Legacy equivalent
lsof -i :8080             # What process uses port 8080
lsof -i -P -n             # All network connections

# DNS diagnostics
dig example.com           # DNS lookup
nslookup example.com      # Alternative DNS lookup
cat /etc/resolv.conf      # DNS resolver configuration
```

```bash
# iptables firewall rules
# View current rules
iptables -L -n -v

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Drop everything else
iptables -A INPUT -j DROP

# Save rules (Debian/Ubuntu)
iptables-save > /etc/iptables/rules.v4

# Rate limit SSH connections (brute-force protection)
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
  -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
  -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
```

```python
# Python socket server example
import socket

def create_tcp_server(host='0.0.0.0', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print(f"Listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello")
```

## Gotchas

- Binding to `0.0.0.0` exposes service on ALL interfaces including public - use `127.0.0.1` for local-only services
- `TIME_WAIT` sockets (after connection close) can exhaust port range - tune `net.ipv4.tcp_tw_reuse` for high-connection servers
- Unix domain sockets have filesystem permissions - but often created world-accessible by default; check with `ls -la /var/run/*.sock`
- iptables rules are evaluated top-to-bottom, first match wins - order matters critically
- Docker bypasses iptables INPUT chain by default (uses DOCKER chain) - firewall rules may not apply to container ports
- `SO_REUSEADDR` allows binding to a port in `TIME_WAIT` state but `SO_REUSEPORT` allows multiple processes on same port (load balancing)

## See Also

- [Linux socket(7) man page](https://man7.org/linux/man-pages/man7/socket.7.html)
- [NIST SP 800-41 Guidelines on Firewalls](https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final)
- [iptables tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html)
