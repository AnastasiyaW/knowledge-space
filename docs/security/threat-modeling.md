---
title: Threat Modeling
category: concepts
tags: [security, threat-modeling, risk-assessment, information-security, compliance]
---

# Threat Modeling

Systematic process for identifying, evaluating, and documenting potential threats to an organization's information assets. Produces formal threat model documents that drive security controls, architecture decisions, and compliance.

## Key Facts
- General threat model covers the entire organization's infrastructure; private models cover specific systems
- Start with the general model, then derive private models for individual information resources
- Threat databases (national vulnerability registries) provide standardized threat catalogs
- A threat model is a living document - must be updated when infrastructure, assets, or threat landscape changes
- Threat models are required by most security compliance frameworks (ISO 27001, NIST, local regulations)

## General vs Private Threat Models

### General Threat Model

Covers the entire information infrastructure of an organization - all systems, networks, and data assets collectively.

**Purpose**: establish a baseline of threats applicable across the organization. Private models are then derived from it.

**Development process**:

1. **Inventory information assets**: identify all information resources (HR systems, production control, customer databases, internal networks)
2. **Consult threat databases**: use national/international vulnerability databases for standardized threat catalogs
3. **If a prior threat register exists**: use it as the foundation - it already filters threats relevant to the organization
4. **Map threats to assets**: determine which threats apply to which categories of systems
5. **Assess likelihood and impact**: rank threats by probability and potential damage
6. **Document countermeasures**: existing and planned security controls per threat

### Private Threat Model

Covers a specific information resource or group of identical resources.

**Examples**:
- Employee personal data processing system
- Customer personal data processing system
- Industrial control system (SCADA/ICS) for a production line
- Group of identical systems across multiple facilities (same vendor, same components)

**Derivation from general model**:

1. Start from the general threat model
2. Filter threats to only those relevant to the specific system
3. Add system-specific threats not covered in the general model
4. Detail specific attack vectors for the system's architecture
5. Map to system-specific security controls
6. Document residual risks after controls are applied

## Threat Model Structure

### Minimal Document Sections

```
1. Scope and boundaries
   - What is covered (systems, networks, data flows)
   - What is explicitly excluded

2. Asset inventory
   - Information assets and their classification
   - Processing systems and their locations
   - Data flows between systems

3. Threat catalog
   - Threat ID, description, source
   - Applicable assets
   - Likelihood rating (1-5)
   - Impact rating (1-5)

4. Vulnerability assessment
   - Known vulnerabilities per asset
   - Exploitation difficulty

5. Existing countermeasures
   - Controls already in place
   - Effectiveness assessment

6. Residual risk
   - Threats not fully mitigated
   - Accepted risk vs planned remediation

7. Recommendations
   - Prioritized list of additional controls
```

## Common Frameworks

| Framework | Focus | Best For |
|-----------|-------|----------|
| **STRIDE** | Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation | Software/application threat modeling |
| **PASTA** | Process for Attack Simulation and Threat Analysis | Risk-centric, business-aligned |
| **OCTAVE** | Operationally Critical Threat, Asset, and Vulnerability Evaluation | Organization-wide risk assessment |
| **DREAD** | Damage, Reproducibility, Exploitability, Affected users, Discoverability | Threat rating/prioritization |

### STRIDE Per Element

Apply STRIDE categories to each component in a data flow diagram:

| Component | Relevant STRIDE Threats |
|-----------|------------------------|
| External entity | Spoofing |
| Process | All six categories |
| Data store | Tampering, Information Disclosure, Denial of Service |
| Data flow | Tampering, Information Disclosure, Denial of Service |
| Trust boundary | All threats at boundary crossings |

## Practical Workflow

```
1. Define scope -> 2. Build DFD -> 3. Identify threats (STRIDE/catalog)
    -> 4. Rate risk (likelihood x impact) -> 5. Plan mitigations
    -> 6. Document -> 7. Review periodically
```

### Data Flow Diagram (DFD)

The foundation of threat modeling - shows how data moves through the system:

```
[User] --HTTPS--> [Web Server] --SQL--> [Database]
                       |
                  [Auth Service] --LDAP--> [Active Directory]
```

Mark trust boundaries (dashed lines) where privilege level changes. Threats concentrate at trust boundary crossings.

## Gotchas
- **General model first**: skipping the general model and going straight to private models leads to gaps - organization-wide threats get missed when each team only considers their own system
- **Threat model != vulnerability scan**: threat modeling is strategic (what COULD happen), vulnerability scanning is tactical (what IS exploitable now). Both are needed, neither replaces the other
- **Stale threat models are dangerous**: a threat model from 2 years ago may miss cloud migration, new remote work patterns, or emerging attack techniques. Review at minimum annually and after any major infrastructure change
- **Identical systems across facilities**: when multiple sites run the same system (same vendor, same config), a single private threat model can cover all instances - no need to duplicate

## See Also
- [[information-security-fundamentals]] - core security concepts
- [[compliance-and-regulations]] - regulatory frameworks requiring threat models
- [[vulnerability-scanning-and-management]] - tactical complement to strategic threat modeling
- [[security-solutions-architecture]] - implementing controls identified by threat models
