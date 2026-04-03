---
title: SIEM and Incident Response
category: techniques
tags: [security, siem, incident-response, soc, soar, monitoring, forensics]
---

# SIEM and Incident Response

Security Information and Event Management: log collection, correlation rules, alert tuning. Incident response lifecycle: classification, triage, investigation, containment, eradication, recovery, and post-incident review. SOC operations and SOAR automation.

## Key Facts
- SIEM combines log aggregation, normalization, correlation, alerting, and retention
- Correlation rules link events across sources and time to detect attack patterns
- Incident response phases: Classify -> Triage -> Investigate -> Contain -> Eradicate -> Recover -> Review
- MTTD (Mean Time to Detect) and MTTR (Mean Time to Respond) are key SOC metrics
- SOAR automates repetitive response actions (block IP, isolate host, disable account)
- Log source onboarding priority: auth systems -> firewalls -> critical servers -> endpoints -> cloud

## SIEM Architecture
- **Log collection** - agents, syslog receivers, API integrations
- **Normalization** - converting diverse formats to common schema
- **Indexing** - fast search across billions of events
- **Correlation** - linking related events across sources
- **Alerting** - rules trigger notifications
- **Dashboards** - real-time visibility
- **Retention** - long-term storage for investigation and compliance

### Log Collection Methods
- **Agent-based** - software on endpoints forwards logs
- **Agentless** - syslog, WMI, API, file share polling
- **Network tap** - capture traffic directly
- **Cloud API** - native service integrations (CloudTrail, Azure Activity Log)

### Correlation Rules
```
# Brute force detection
IF count(failed_login) > 5 from same source_ip within 5 minutes
THEN alert "Potential brute force"

# Lateral movement
IF successful_login from IP_A to Host_B
AND Host_B not previously accessed from IP_A
AND Host_B has privileged services
THEN alert "Potential lateral movement"

# Data exfiltration
IF outbound_data_volume > threshold from single host
AND destination not in whitelist
AND time outside business hours
THEN alert "Potential data exfiltration"
```

### Alert Tuning
- Start with known-bad indicators (IoCs)
- Add behavioral rules (failed logins, privilege escalation)
- Tune to reduce false positives without missing true positives
- Suppression to prevent alert storms from repeated triggers
- Enrichment: add asset info, threat intel, geolocation

## Incident Response

### Classification
- **Category**: malware, unauthorized access, DDoS, data breach, insider threat, phishing
- **Severity**: Critical (P1), High (P2), Medium (P3), Low (P4)
- **Scope**: single host, network segment, entire environment, customer-facing

### Triage Questions
1. True positive or false positive?
2. What is affected?
3. Is the threat active or historical?
4. What is the business impact?
5. Is escalation needed?

### Investigation Workflow
1. **Scoping** - determine extent of compromise
2. **Evidence collection** - preserve logs, memory dumps, disk images (maintain chain of custody)
3. **Timeline construction** - reconstruct attacker actions
4. **Root cause analysis** - initial access vector
5. **Impact assessment** - what data/systems affected

### Containment
- **Short-term**: isolate systems, disable accounts, block IPs/domains
- **Long-term**: patch vulnerabilities, rebuild if necessary
- Balance: contain threat without destroying evidence

### Eradication
- Remove malware, backdoors, persistence mechanisms
- Reset all potentially compromised credentials
- Patch exploited vulnerabilities
- Re-scan to verify removal

### Recovery
- Restore from clean backups
- Rebuild compromised systems
- Gradual reconnection with enhanced monitoring
- Verify integrity before returning to production

### Post-Incident
- Lessons learned meeting
- Complete documentation (timeline, actions, outcomes)
- Control improvements for identified gaps
- Update detection rules based on findings

## SOC Operations

### Tier Model
| Tier | Role | Responsibilities |
|------|------|-----------------|
| L1 | Alert triage | Initial investigation, false positive ID, escalation |
| L2 | Incident handling | Deep investigation, forensics, threat hunting |
| L3 | Advanced analysis | Malware RE, tool development, process improvement |

### SOC Metrics
- **MTTD** - time from attack to detection
- **MTTR** - time from detection to containment
- **Dwell time** - how long attacker was present
- **False positive rate** - noise vs real alerts
- **Coverage** - percentage of assets monitored

## SOAR (Security Orchestration, Automation and Response)

### Playbook Automations
- **Phishing**: extract IOCs -> check threat intel -> block sender -> quarantine similar emails
- **Malware**: isolate host -> collect evidence -> scan for lateral movement
- **Account compromise**: force password reset -> disable account -> check data access
- **Vulnerability alert**: check affected assets -> determine exposure -> create ticket

Benefits: consistent response, faster (minutes vs hours), scalable, full audit trail.

## Critical Log Sources
- **Authentication**: AD, VPN, SSO
- **Network**: firewalls, IDS/IPS, proxy
- **DNS**: reveals C2 communication, data exfiltration
- **Endpoints**: Windows Event Log, syslog, EDR telemetry
- **Email**: delivery, quarantine, phishing detections
- **Cloud**: CloudTrail, Azure Activity Log, GCP Audit Log
- **Database**: audit logs (queries, schema changes)

## Gotchas
- SIEM is only as good as its log sources - uncovered blind spots are where attackers hide
- Correlation rules need continuous tuning - environment changes make old rules noisy or blind
- Evidence preservation must happen before containment - isolating a system may destroy volatile data
- Incident documentation should happen in real-time, not after the fact (memory degrades under pressure)
- SOAR playbooks must be tested regularly - an untested automated response may cause more damage than the incident

## See Also
- [[security-solutions-architecture]] - IDS/IPS, EDR, DLP implementation
- [[windows-security-and-powershell]] - Windows event IDs for SIEM rules
- [[linux-system-hardening]] - auditd, syslog configuration
- [[compliance-and-regulations]] - compliance-driven monitoring requirements
