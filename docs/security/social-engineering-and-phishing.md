---
title: Social Engineering and Phishing
category: concepts
tags: [security, social-engineering, phishing, email-security, human-factors]
---

# Social Engineering and Phishing

Human-targeted attack vectors: phishing (spear, whaling, vishing), pretexting, email spoofing detection (SPF/DKIM/DMARC), email header analysis, and breach database investigation techniques.

## Key Facts
- Spear phishing targets specific individuals with personalized content; whaling targets executives
- SPF + DKIM + DMARC together prevent email spoofing - check all three
- Business Email Compromise (BEC) losses exceed ransomware losses globally
- Email header `Received:` chain traces the full routing path
- Breach databases (HIBP) enable credential reuse attacks across services
- Physical social engineering (tailgating, impersonation) bypasses all digital controls

## Phishing Types

| Type | Target | Method |
|------|--------|--------|
| Phishing | Mass/random | Generic emails, fake login pages |
| Spear phishing | Specific individuals | Personalized content, context-aware |
| Whaling | Executives/C-suite | Impersonating board members, legal |
| Vishing | Phone targets | Voice-based impersonation |
| Smishing | SMS recipients | Malicious links via text message |

## Phishing Campaign Tools
- **GoPhish** - open-source phishing framework for awareness testing
- **King Phisher** - phishing campaign toolkit
- Credential harvesting landing pages
- Malicious attachments: macro-enabled documents, HTML smuggling

## Pretexting
Creating fabricated scenarios to manipulate targets:
- Impersonating IT support ("We need your credentials to fix an issue")
- Vendor impersonation ("Invoice payment overdue")
- Executive impersonation ("Wire transfer needed urgently")
- Physical: tailgating through secured doors, wearing fake badges

## Email Authentication

### SPF (Sender Policy Framework)
DNS TXT record listing authorized mail server IPs:
```ini
v=spf1 mx ip4:203.0.113.0/24 include:_spf.google.com -all
```

### DKIM (DomainKeys Identified Mail)
Cryptographic signature in email headers proving message integrity and sender domain.

### DMARC (Domain-based Message Authentication)
Policy for handling SPF/DKIM failures:
```ini
v=DMARC1; p=reject; rua=mailto:dmarc@example.com
```
Policies: `none` (monitor), `quarantine` (spam folder), `reject` (block).

## Email Header Analysis
```sql
Received: chain          - full routing path (read bottom-up)
X-Originating-IP         - sender's real IP
Message-ID               - domain should match sender
Return-Path vs From      - mismatch = likely spoofing
Authentication-Results    - SPF/DKIM/DMARC pass/fail
```

## Breach Database Investigation
- **Have I Been Pwned** (HIBP) - legitimate breach checking
- **DeHashed / IntelX** - advanced breach data search (includes passwords)
- Email -> password from breach -> credential reuse on other services
- Holehe: check if email is registered on services without alerting the user

## Gotchas
- SPF pass alone does not prevent display-name spoofing (From: "CEO Name" <attacker@evil.com>)
- DMARC `p=none` provides monitoring but no protection - needs `p=quarantine` or `p=reject`
- Security awareness training reduces click rates but never eliminates them (some employees always click)
- Advanced phishing uses compromised legitimate accounts - passes all authentication checks
- AI-generated phishing content is increasingly indistinguishable from legitimate communication

## See Also
- [[penetration-testing-methodology]] - social engineering in pentests
- [[osint-and-reconnaissance]] - gathering information for targeted phishing
- [[siem-and-incident-response]] - phishing response playbooks
- [[anti-fraud-behavioral-analysis]] - detecting phishing at scale
