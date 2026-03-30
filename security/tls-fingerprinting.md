---
title: TLS Fingerprinting
category: network-security
tags: [tls, ssl, ja3, fingerprinting, traffic-analysis, encryption]
---

# TLS Fingerprinting

## Key Facts

- TLS fingerprinting identifies client software from the TLS ClientHello message - before any encrypted data is exchanged
- JA3 (created by Salesforce) hashes: TLS version, cipher suites, extensions, elliptic curves, EC point formats into a single MD5 hash
- JA4 is the successor to JA3 with improved readability and granularity
- The TLS handshake occurs before HTTP, so even HTTPS traffic can be fingerprinted at the network level
- Different browsers/versions produce different JA3 hashes - Chrome, Firefox, curl, Python requests each have distinct signatures
- [[anti-fraud-systems]] use TLS fingerprint to detect when claimed browser (User-Agent) differs from actual TLS behavior
- [[network-identifiers]] at L3/L4 complement TLS fingerprinting at the session layer
- Google uses passive OS fingerprinting (UNIX-based system) to detect anomalies at the network level before any application data

## Patterns

```python
# JA3 fingerprint structure
# md5(TLSVersion,Ciphers,Extensions,EllipticCurves,EllipticCurvePointFormats)

# Example JA3 hashes (illustrative):
# Chrome 120:   "773906b0efdefa24a7f2b8eb6985bf37"
# Firefox 120:  "b32309a26951912be7dba376398abc3b"
# Python requests: "a]b4e9f5b1edb7d3e7c4d0f8b6c9a2"
# curl:         "456523fc94726331a4d5a2e1d40b2c7a"

# Detecting JA3 mismatch
def detect_ua_tls_mismatch(user_agent: str, ja3_hash: str) -> bool:
    """Flag when User-Agent claims Chrome but TLS fingerprint is Python"""
    known_browser_ja3 = {
        'chrome': ['773906b0...', '...'],
        'firefox': ['b32309a2...', '...'],
    }
    claimed_browser = parse_browser_from_ua(user_agent)
    if claimed_browser in known_browser_ja3:
        return ja3_hash not in known_browser_ja3[claimed_browser]
    return False
```

```bash
# Capture JA3 fingerprints with tshark
tshark -i eth0 -Y "tls.handshake.type == 1" \
  -T fields -e ip.src -e tls.handshake.ja3

# Using zeek (formerly bro) for JA3 logging
# ja3.log is automatically generated with JA3 hashes
```

## Gotchas

- JA3 hash can be spoofed by custom TLS libraries that mimic another client's ClientHello - but this requires significant effort
- TLS 1.3 reduces fingerprint surface compared to TLS 1.2 - fewer cipher suites and extensions vary between clients
- CDN/reverse proxy terminating TLS sees the original JA3 but backend servers do not - JA3 must be captured at the edge
- Browser extensions can modify TLS behavior and change the JA3 hash unexpectedly
- Anti-detect browsers must match both User-Agent AND TLS fingerprint to avoid detection

## See Also

- [JA3 - Salesforce GitHub](https://github.com/salesforce/ja3)
- [JA4+ TLS Fingerprinting](https://github.com/FoxIO-LLC/ja4)
- [NIST SP 800-52 Rev 2 - Guidelines for TLS](https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final)
