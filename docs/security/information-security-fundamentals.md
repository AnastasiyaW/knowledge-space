---
title: Information Security Fundamentals
category: concepts
tags: [security, cia-triad, risk, threat-modeling, defense-in-depth]
---

# Information Security Fundamentals

Core concepts of information security: the CIA triad, threat modeling, risk management, and security architecture patterns. This entry provides the conceptual foundation that all other security topics build upon.

## Key Facts
- **CIA Triad** - Confidentiality (data accessible only to authorized), Integrity (data accurate and unaltered), Availability (systems accessible when needed)
- Prioritization depends on context: banking = integrity first, military = confidentiality first, e-commerce = availability first, healthcare = all three equally
- Risk = Threat x Vulnerability x Impact - a vulnerability without a threat is not a risk
- Defense in Depth: no single layer is sufficient; each layer should be independent
- Zero Trust: "never trust, always verify" - even internal traffic

## The CIA Triad

### Confidentiality
Threats: data breaches, eavesdropping, social engineering.
Controls: encryption, access controls, data classification.

### Integrity
Threats: unauthorized modification, man-in-the-middle, data corruption.
Controls: hashing, digital signatures, version control, checksums.

### Availability
Threats: DDoS, hardware failure, ransomware.
Controls: redundancy, backups, load balancing, disaster recovery.

## Patterns

### Defense in Depth
Multiple independent layers of security controls:
1. Physical security (locks, cameras)
2. Network security (firewalls, IDS/IPS)
3. Host security (antivirus, EDR, hardening)
4. Application security (WAF, input validation)
5. Data security (encryption, DLP, access controls)
6. Administrative controls (policies, training)

### Zero Trust Architecture
- Micro-segmentation of the network
- Least privilege access for every identity
- Continuous verification of every request
- Assume breach at all times
- Encrypt all communications, including internal

### Security Zones (DMZ)
- **Internet** - untrusted
- **DMZ** - semi-trusted, hosts public-facing services
- **Internal network** - trusted, business systems
- **Management network** - highly restricted, infrastructure management
- Firewalls between each zone with strict rule sets

## Assets and Threats

### Asset Categories
- **Information** - databases, intellectual property, customer data
- **Physical** - servers, network equipment, facilities
- **Software** - applications, operating systems, tools
- **Human** - employees, contractors, knowledge
- **Intangible** - reputation, brand, trust

### Threat Actors
| Actor | Motivation | Skill Level |
|-------|-----------|-------------|
| Script kiddies | Curiosity, fame | Low (use existing tools) |
| Hacktivists | Ideological (e.g. Anonymous) | Low-Medium |
| Cybercriminals | Financial (ransomware, carding) | Medium-High |
| Insiders | Grudge, financial, coerced | Varies (have legitimate access) |
| Nation-states | Espionage, disruption (APT28, Lazarus) | Very High |
| Competitors | Corporate espionage | Medium |

## Risk Management

### Qualitative Assessment
Uses descriptive scales (High/Medium/Low). Risk matrix 5x5: Likelihood (1-5) x Impact (1-5). Scores 1-5 = Low (accept), 6-12 = Medium (mitigate/transfer), 13-25 = Critical (mitigate immediately).

### Quantitative Assessment
- Asset Value (AV) - monetary value
- Exposure Factor (EF) - percentage lost (0-1)
- Single Loss Expectancy (SLE) = AV x EF
- Annual Rate of Occurrence (ARO) - expected incidents/year
- Annual Loss Expectancy (ALE) = SLE x ARO

### Risk Treatment Options
1. **Accept** - risk within appetite, control cost exceeds potential loss
2. **Mitigate** - implement controls to reduce likelihood or impact
3. **Transfer** - shift to third party (insurance, outsourcing)
4. **Avoid** - eliminate the activity creating the risk

## Vulnerability Management

### CVE / CVSS / NVD
- **CVE** - unique identifier (CVE-YEAR-NUMBER)
- **CVSS** - 0-10 severity score (Base + Temporal + Environmental)
- **NVD** - NIST-maintained CVE database with CVSS scores

### Patch Management Lifecycle
1. Discovery (scanning for missing patches)
2. Assessment (evaluate applicability and risk)
3. Testing (staging environment)
4. Deployment (phased production rollout)
5. Verification (confirm patches applied)
6. Documentation (audit trail)

## Gotchas
- CVSS base score alone is misleading - always consider environmental context for your organization
- Risk acceptance must be documented with business owner sign-off, not just a security team decision
- "Compliance != Security" - passing an audit does not mean you are secure
- Defense in depth layers must be truly independent - shared credentials across layers defeat the purpose

## See Also
- [[cryptography-and-pki]] - encryption, hashing, digital signatures
- [[authentication-and-authorization]] - MFA, OAuth, Kerberos
- [[compliance-and-regulations]] - GDPR, PCI DSS, ISO 27001
- [[vulnerability-scanning-and-management]] - Nessus, OpenVAS, scanning
