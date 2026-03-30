---
title: Network Identifiers and IP Security
category: network-security
tags: [ip-address, ipv4, ipv6, proxy, vpn, network, identification]
---

# Network Identifiers and IP Security

## Key Facts

- Network identifiers are used by anti-fraud and security systems to track and verify users at the network layer
- IPv4 address space is exhausted; IPv6 provides vastly larger address space with native IPsec support built into packet headers
- IP address classification: residential ISP (trusted), hosting/datacenter (suspicious for consumer activity), mobile carrier (moderate trust)
- ASN (Autonomous System Number) reveals whether IP belongs to ISP, cloud provider, or VPN service
- [[tls-fingerprinting]] extracts TLS ClientHello parameters to identify client software without decryption
- [[anti-fraud-systems]] treat datacenter IPs as high-risk by default
- Proxy types: HTTP/HTTPS proxy, SOCKS4/5, residential proxy (routed through real ISP connections), mobile proxy

## Patterns

```python
# IP reputation check pattern
import ipaddress
import requests

def check_ip_risk(ip: str) -> dict:
    """Evaluate IP address risk factors"""
    addr = ipaddress.ip_address(ip)
    result = {
        'ip': ip,
        'version': addr.version,  # 4 or 6
        'is_private': addr.is_private,
        'is_loopback': addr.is_loopback,
    }
    # Check against threat intelligence
    # ASN lookup reveals hosting vs residential
    return result

# Common proxy detection headers to check
PROXY_HEADERS = [
    'X-Forwarded-For',
    'X-Real-IP',
    'Via',
    'Forwarded',
    'X-Forwarded-Host',
    'X-Forwarded-Proto',
]
```

```bash
# Passive OS fingerprinting via network stack
# p0f - identifies OS from TCP/IP stack behavior
p0f -i eth0 -o /var/log/p0f.log

# nmap OS detection
nmap -O target_ip
```

## Gotchas

- IPv6 address can uniquely identify a device (EUI-64 embeds MAC address) unless privacy extensions (RFC 4941) are enabled
- WebRTC can leak real IP address even behind VPN/proxy - must be explicitly disabled in browser
- IP geolocation databases are inaccurate for mobile carriers and VPN endpoints - can show wrong country/city
- Multiple users behind NAT share the same public IP - IP alone is insufficient for unique identification
- DNS leak reveals real ISP even when using VPN if DNS requests go through default resolver
- TLS fingerprint (JA3/JA4) can identify specific browser version even through proxy - changing IP alone is insufficient

## See Also

- [IANA IPv4 Address Space](https://www.iana.org/assignments/ipv4-address-space/)
- [RFC 4941 - Privacy Extensions for IPv6](https://datatracker.ietf.org/doc/html/rfc4941)
- [JA3 TLS Fingerprinting](https://github.com/salesforce/ja3)
- [NIST SP 800-77 Guide to IPsec VPNs](https://csrc.nist.gov/publications/detail/sp/800-77/rev-1/final)
