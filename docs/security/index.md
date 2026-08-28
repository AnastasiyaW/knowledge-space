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
- [Database Security](database-security.md) - user privileges, encryption, auditing, backup security, cloud database security

## Anti-Fraud & Forensics
- [[browser-and-device-fingerprinting]] - canvas, WebGL, AudioContext, evercookies, hardware signals
- [[tls-fingerprinting-and-network-identifiers]] - IP classification, geolocation, VPN detection, IPv6 leaks
- [[anti-fraud-behavioral-analysis]] - mouse/keystroke dynamics, payment fraud, velocity checks, BIN analysis
- [[deepfake-and-document-forensics]] - deepfake detection, document forgery, image forensics (ELA), email analysis

## Security Scripting
- [[python-for-security]] - socket programming, port scanning, log analysis, HTTP testing, tool integration

## Additional References

- [[adobe-piracy-patterns]] - Date: 2026-04-03 Context: Defensive security research
- [[ai-agent-production-disasters]] - Analysis of critical production failures caused by autonomous AI coding agents between 2025 and 2026
- [[ai-powered-vulnerability-detection-april-2026]] - State of the art in automated security auditing has shifted from pattern-based SAST to hybrid
- [[ai-vulnerability-detection]] - Date: 2026-04-14 Context: State of AI-powered security scanning as of April 2026
- [[anti-piracy-legal]] - Date: 2026-04-03 Context: Desktop ML inference product
- [[claude-mythos-leak-and-ai-supply-chain-security]] - The unauthorized access to the Claude Mythos Preview (April 2026) serves as a benchmark for AI
- [[computation-obfuscation]] - Date: 2026-04-03 Context: Desktop ML inference product
- [[cwe-079-xss]] - CWE-79: Attacker-controlled data inserted into DOM/HTML without escaping
- [[cwe-089-sql-injection]] - CWE-89: SQL Injection - untrusted data alters query structure
- [[cwe-125-oob-read]] - CWE-125: Out-of-bounds Read - reads past buffer boundaries leak secrets, keys, adjacent heap
- [[cwe-190-integer-overflow]] - CWE-190: Arithmetic produces out-of-range result, wrapping or truncating
- [[cwe-400-resource-consumption]] - CWE-400: Attacker triggers uncontrolled CPU, memory, disk, or fd consumption via regex DoS, hash
- [[cwe-416-use-after-free]] - CWE-416: Use After Free - accessing freed memory enables RCE, info disclosure, DoS
- [[cwe-434-file-upload]] - CWE-434: Unrestricted Upload of Dangerous File Type - uploaded files execute on server
- [[cwe-502-deserialization]] - CWE-502: Deserializing attacker-controlled data enables arbitrary code execution via gadget chains
- [[cwe-787-oob-write]] - CWE-787: Out-of-bounds Write - memory corruption via writes past buffer boundaries
- [[cwe-918-ssrf]] - CWE-918: Server makes HTTP/protocol requests to attacker-controlled URLs, exposing internal
- [[disposable-email-detection]] - Backend reference for detecting throwaway email addresses and multi-account abuse at registration
- [[email-reputation-services]] - Signal categories, vendor service tradeoffs, and a DIY MVP stack for blocking high-risk
- [[hkdf-personalized-weights]] - Date: 2026-04-03 Context: Desktop C++ app, ONNX Runtime inference
- [[licensing-implementation-cpp]] - Date: 2026-04-03 Context: Desktop C++ app (Mac + Windows), self-hosted license server, ONNX models
- [[lora-weight-protection]] - Date: 2026-04-03 Context: Desktop/server image generation with proprietary LoRA adapters on
- [[model-weight-encryption]] - Date: 2026-04-03 Context: Desktop C++ app (Mac + Windows)
- [[onnx-model-protection]] - Date: 2026-04-03 Context: Desktop C++ app (Mac + Windows), ONNX Runtime inference, protection of
- [[output-scrambling-antipiracy]] - Date: 2026-04-03 Context: Desktop C++ app with ONNX inference
- [[piracy-economics]] - Date: 2026-04-03 Context: Desktop ML inference products
- [[remote-kill-switch]] - Date: 2026-04-03 Context: Desktop C++ retouching app (Mac + Windows)
- [[retouch4me-competitive-analysis]] - Date: 2026-04-03 Context: Architectural and product analysis for building a competing retouching
- [[security-telemetry]] - Date: 2026-04-03 Context: Desktop application with online license server
- [[tamper-resistant-counters]] - Date: 2026-04-03 Context: C++, Windows + macOS
- [[threat-modeling]] - Systematic process for identifying, evaluating, and documenting potential threats to an
- [[watermarking-encrypted-models]] - Date: 2026-04-03 Context: C++ desktop retouching app
