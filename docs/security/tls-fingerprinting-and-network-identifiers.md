---
title: TLS Fingerprinting and Network Identifiers
category: concepts
tags: [security, fingerprinting, ip-analysis, geolocation, vpn-detection, anti-fraud]
---

# TLS Fingerprinting and Network Identifiers

Network-level identification techniques: IP address classification and reputation, geolocation methods and spoofing detection, VPN/proxy/Tor detection, IPv6 privacy implications, and Wi-Fi signal analysis.

## Key Facts
- IP classification: residential (low risk), datacenter (high risk), mobile/CGNAT (moderate), Tor exit (very high)
- IP geolocation is accurate to city level ~80% for residential IPs
- Comparing claimed location vs IP location vs timezone vs language settings detects spoofing
- IPv6 can leak real network information even when IPv4 is routed through VPN
- "Impossible travel" detection: user in Moscow then Tokyo within 5 minutes = fraud signal
- Wi-Fi BSSID analysis can verify or contradict claimed physical location

## IP Address Classification
Anti-fraud categorizes IPs by type:

| Type | Risk Level | Notes |
|------|-----------|-------|
| Residential | Low | ISP-assigned consumer IPs |
| Datacenter/hosting | High | Indicates VPN/proxy/bot |
| Mobile carrier (CGNAT) | Moderate | Shared among many users |
| Tor exit nodes | Very high | Known exit node lists |

Example: a sysadmin accessing PayPal from datacenter Wi-Fi gets flagged because the IP belongs to a hosting provider, not a residential ISP.

## IP Geolocation
- **City level** - ~80% accurate for residential IPs
- **ISP identification** - highly reliable
- **VPN/proxy detection** - IP reputation databases (MaxMind, IP2Proxy)
- Cross-reference: claimed location vs IP location vs timezone (`Intl.DateTimeFormat().resolvedOptions().timeZone`) vs browser language

## Geolocation Methods
1. **GPS** - most accurate (meters), mobile only
2. **Wi-Fi positioning** - triangulation from known AP locations, 10-50m accuracy
3. **Cell tower** - carrier-based, 100-300m urban, km in rural
4. **IP geolocation** - city level, unreliable for mobile carriers
5. **Bluetooth beacons** - indoor positioning

## Spoofing Detection
- **Cross-referencing**: GPS says New York but IP is from Germany
- **Timezone mismatch**: JavaScript timezone vs IP-based timezone
- **Impossible travel**: location A then location B in impossibly short time
- **Wi-Fi BSSID inconsistency**: claiming location X but connected to APs at location Y

## IPv6 Security Implications
- 128-bit address space (vs IPv4 32-bit)
- Native IPsec support built into packet headers
- Many VPN/proxy tools lack full IPv6 support - IPv6 traffic may bypass VPN
- Dual-stack environments create additional fingerprinting surface
- IPv6 address embedding MAC address (SLAAC without privacy extensions) can identify device

## Wi-Fi Signal Analysis
- **Signal attenuation** - USB dimmers control signal strength, faking distance to APs
- **Shielding** - conductive paint/fabric blocks Wi-Fi (requires grounding)
- **MAC address spoofing** - changing adapter MAC to avoid tracking

## Cookie Time Bomb Technique
Manipulating system clock before visiting sites causes cookies to be issued with past dates, making device appear to have visited previously. Works on sites that trust client-reported time for cookie timestamps.

## Gotchas
- Datacenter IPs are not always malicious - remote workers using VPNs, corporate proxies
- Mobile carrier CGNAT means thousands of users share one IP - cannot attribute to individual
- IP reputation databases have latency - new VPN/proxy IPs take days to weeks to be flagged
- GPS spoofing is trivial on rooted/jailbroken devices
- IPv6 privacy extensions generate random interface IDs but the /64 prefix still identifies the network

## See Also
- [[browser-and-device-fingerprinting]] - browser-level fingerprinting
- [[anti-fraud-behavioral-analysis]] - behavioral signals
- [[network-security-and-protocols]] - TCP/IP fundamentals
- [[cryptography-and-pki]] - TLS protocol details
