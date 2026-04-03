---
title: Compliance and Regulations
category: concepts
tags: [security, compliance, gdpr, pci-dss, iso-27001, nist, audit]
---

# Compliance and Regulations

Regulatory frameworks and compliance requirements: ISO 27001, NIST Cybersecurity Framework, PCI DSS, GDPR, policy hierarchy, risk assessment for compliance, evidence collection, and audit preparation.

## Key Facts
- Compliance != Security - passing an audit does not mean you are secure
- GDPR fines: up to 4% of annual global turnover or EUR 20M (whichever higher)
- GDPR requires 72-hour breach notification to supervisory authority
- PCI DSS requires quarterly vulnerability scans and annual penetration tests
- ISO 27001 uses Plan-Do-Check-Act cycle with 114 controls across 14 domains
- NIST CSF: five functions - Identify, Protect, Detect, Respond, Recover

## International Standards

### ISO 27001 (ISMS)
Information Security Management System:
- Plan-Do-Check-Act continuous improvement cycle
- Annex A: 114 controls across 14 domains
- Risk-based approach - controls selected based on assessment
- Certification requires external audit
- Globally recognized

### NIST Cybersecurity Framework
Five functions: **Identify** -> **Protect** -> **Detect** -> **Respond** -> **Recover**
- Tiers: Partial (1), Risk Informed (2), Repeatable (3), Adaptive (4)
- Implementation profiles: current state vs target state
- Voluntary but widely adopted

### NIST 800-53
Comprehensive security control catalog:
- 20 control families (AC, AU, CM, IA, IR, SC, SI, etc.)
- Controls mapped to impact levels (Low, Moderate, High)
- Foundation for FedRAMP, FISMA compliance

### PCI DSS
Payment Card Industry Data Security Standard:
- 12 requirements for handling cardholder data
- Network segmentation, encryption, access control, monitoring
- Quarterly vulnerability scans (ASV)
- Annual penetration tests
- Compliance levels based on transaction volume
- SAQ for smaller merchants, ROC for large ones

### GDPR
EU data protection with extraterritorial reach:
- **Lawful basis**: consent, contract, legal obligation, vital interest, public interest, legitimate interest
- **Data subject rights**: access, rectification, erasure (right to be forgotten), portability, objection
- **DPO** required for large-scale processing
- **72-hour breach notification**
- **Privacy by Design** - security built in from the start
- **Data minimization** - collect only what is needed

## Policy Hierarchy
1. **Security Policy** - high-level objectives and management commitment
2. **Standards** - mandatory requirements (encryption standards, password standards)
3. **Procedures** - step-by-step implementation instructions
4. **Guidelines** - recommendations and best practices (optional)

## Risk Assessment for Compliance
1. Asset inventory - what needs protecting
2. Threat identification
3. Vulnerability identification
4. Impact assessment
5. Likelihood assessment
6. Map risk treatment to compliance requirements:
   - Regulation requires encryption -> implement AES-256 at rest
   - Regulation requires logging -> deploy audit trail system
   - Regulation requires breach detection -> implement SIEM with alerting

## Evidence Collection
| Evidence Type | Examples |
|---------------|----------|
| Configuration | System settings screenshots, exports |
| Scan reports | Vulnerability scans, pentest results |
| Log samples | Demonstrating monitoring capability |
| Policy documents | Approved and current versions |
| Training records | Employee awareness completion |
| Incident reports | Demonstrating response capability |
| Change management | Controlled modification records |

## Audit Preparation

### Internal Audit
- Regular self-assessment against frameworks
- Gap analysis: current state vs required state
- Remediation planning with owners and deadlines
- Maintain evidence repository continuously

### External Audit
- Pre-audit readiness assessment
- Organize documents and evidence
- Prepare key personnel for interviews
- Understand sampling methodology
- Plan corrective actions for findings

### Finding Severity
| Level | Meaning |
|-------|---------|
| Major nonconformity | Significant control failure, blocks certification |
| Minor nonconformity | Control exists but has gaps |
| Observation | Area for improvement, not a failure |
| Opportunity for improvement | Suggestion, not a finding |

## Gotchas
- Compliance frameworks overlap significantly - map controls once, apply to multiple standards
- "Tick-box compliance" creates false sense of security - compliance is a minimum, not a ceiling
- GDPR "right to be forgotten" conflicts with backup retention - have a documented process
- PCI DSS scope reduction via network segmentation saves enormous compliance effort
- Audit evidence must be contemporaneous (from the audit period), not prepared after the fact
- Third-party/vendor compliance (SOC 2 reports) does not mean your use of their service is compliant

## See Also
- [[information-security-fundamentals]] - risk management concepts
- [[siem-and-incident-response]] - compliance-driven monitoring
- [[security-solutions-architecture]] - implementing controls
- [[database-security]] - data protection requirements
