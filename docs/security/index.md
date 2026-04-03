---
title: Security & Cybersecurity
type: MOC
---

# Security & Cybersecurity

## Foundations
- [[information-security-fundamentals]] - CIA triad, risk management, defense in depth, zero trust, threat actors
- [[cryptography-and-pki]] - symmetric/asymmetric encryption, hashing, TLS/SSL, PKI, digital signatures
- [[authentication-and-authorization]] - MFA, JWT, OAuth 2.0/OIDC, Kerberos, RBAC, PAM
- [[compliance-and-regulations]] - ISO 27001, NIST CSF, PCI DSS, GDPR, audit preparation

## Web Application Security
- [[web-application-security-fundamentals]] - XSS, CSRF, SSRF, XXE, IDOR, path traversal, OWASP Top 10
- [[sql-injection-deep-dive]] - in-band, blind, out-of-band SQLi, sqlmap, parameterized queries, NoSQL injection
- [[burp-suite-and-web-pentesting]] - proxy, repeater, intruder, scanner, complementary tools
- [[secure-backend-development]] - NestJS/Express security patterns, validation, guards, ORM safety
- [[web-server-security]] - Nginx/Apache config, TLS with Let's Encrypt, reverse proxy, security headers

## Offensive Security
- [[penetration-testing-methodology]] - recon, scanning, exploitation, Metasploit, wireless attacks, reporting
- [[privilege-escalation-techniques]] - Linux SUID/sudo/kernel, Windows tokens/services, lateral movement
- [[active-directory-attacks]] - Kerberoasting, Golden/Silver Ticket, DCSync, BloodHound, Mimikatz
- [[osint-and-reconnaissance]] - Shodan, Google Dorking, metadata extraction, username/email investigation
- [[social-engineering-and-phishing]] - phishing types, pretexting, email authentication (SPF/DKIM/DMARC)

## Network Security
- [[network-security-and-protocols]] - OSI model, TCP/IP, DNS, DHCP, VPN (OpenVPN, WireGuard), email auth
- [[firewall-and-ids-ips]] - iptables/ufw, Windows Firewall, Snort, Suricata, WAF (ModSecurity, cloud)
- [[network-traffic-analysis]] - tcpdump, Wireshark, nmap, TCP/IP fingerprinting, diagnostics

## System Security
- [[linux-os-fundamentals]] - filesystem hierarchy, kernel, boot process, disk encryption (LUKS), processes
- [[linux-system-hardening]] - SSH config, fail2ban, auditd, sysctl, file permissions, CIS benchmarks
- [[windows-security-and-powershell]] - SAM/LSASS, Event IDs, registry, GPO, AppLocker, PowerShell security

## Enterprise Security
- [[siem-and-incident-response]] - SIEM architecture, correlation rules, incident lifecycle, SOC tiers, SOAR
- [[security-solutions-architecture]] - EDR, DLP, IAM/PAM, implementation lifecycle, change management
- [[vulnerability-scanning-and-management]] - Nessus, OpenVAS, CVSS, patch management, prioritization
- [[database-security]] - user privileges, encryption, auditing, backup security, cloud database security

## Anti-Fraud & Forensics
- [[browser-and-device-fingerprinting]] - canvas, WebGL, AudioContext, evercookies, hardware signals
- [[tls-fingerprinting-and-network-identifiers]] - IP classification, geolocation, VPN detection, IPv6 leaks
- [[anti-fraud-behavioral-analysis]] - mouse/keystroke dynamics, payment fraud, velocity checks, BIN analysis
- [[deepfake-and-document-forensics]] - deepfake detection, document forgery, image forensics (ELA), email analysis

## Security Scripting
- [[python-for-security]] - socket programming, port scanning, log analysis, HTTP testing, tool integration
