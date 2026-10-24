---
title: "SIEM und Incident Response"
category: techniques
tags: [security, siem, incident-response, soc, soar, monitoring, forensics]
level: 3
source_sha256: 0c37f2c652301a0b202dbac2075e70524d4ecd26a1bd6432cbfa29c233c996ed
translation: machine
translated_at: '2026-10-24'
---
# SIEM und Incident Response {#siem-and-incident-response}

Security Information and Event Management: Log-Erfassung, Korrelationsregeln, Alert-Tuning. Incident-Response-Lebenszyklus: Klassifizierung, Triage, Untersuchung, Eindämmung, Beseitigung, Wiederherstellung und Nachbereitung nach einem Vorfall. SOC-Betrieb und SOAR-Automatisierung.

## Kernfakten {#key-facts}
- SIEM kombiniert Log-Aggregation, Normalisierung, Korrelation, Alarmierung und Aufbewahrung
- Korrelationsregeln verknüpfen Ereignisse über Quellen und Zeit hinweg, um Angriffsmuster zu erkennen
- Phasen der Incident Response: Classify -> Triage -> Investigate -> Contain -> Eradicate -> Recover -> Review
- MTTD (Mean Time to Detect) und MTTR (Mean Time to Respond) sind zentrale SOC-Kennzahlen
- SOAR automatisiert wiederkehrende Reaktionsmaßnahmen (IP blockieren, Host isolieren, Konto deaktivieren)
- Priorität beim Anbinden von Log-Quellen: Authentifizierungssysteme -> Firewalls -> kritische Server -> Endpoints -> Cloud

## SIEM-Architektur {#siem-architecture}
- **Log-Erfassung** - Agenten, Syslog-Empfänger, API-Integrationen
- **Normalisierung** - Umwandlung unterschiedlicher Formate in ein gemeinsames Schema
- **Indizierung** - schnelle Suche über Milliarden von Ereignissen
- **Korrelation** - Verknüpfung zusammengehöriger Ereignisse über Quellen hinweg
- **Alarmierung** - Regeln lösen Benachrichtigungen aus
- **Dashboards** - Echtzeit-Übersicht
- **Aufbewahrung** - Langzeitspeicherung für Untersuchung und Compliance

### Methoden der Log-Erfassung {#log-collection-methods}
- **Agentenbasiert** - Software auf Endpoints leitet Logs weiter
- **Agentenlos** - Syslog, WMI, API, Abfrage von Dateifreigaben
- **Netzwerk-Tap** - Direkte Erfassung des Datenverkehrs
- **Cloud-API** - native Dienstintegrationen (CloudTrail, Azure Activity Log)

### Korrelationsregeln {#correlation-rules}
```bash
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

### Alert-Tuning {#alert-tuning}
- Mit bekannten schädlichen Indikatoren (IoCs) beginnen
- Verhaltensregeln ergänzen (fehlgeschlagene Anmeldungen, Rechteausweitung)
- Abstimmen, um Fehlalarme zu reduzieren, ohne echte Treffer zu verpassen
- Unterdrückung, um Alarmfluten durch wiederholte Auslöser zu verhindern
- Anreicherung: Asset-Informationen, Threat Intelligence, Geolokalisierung hinzufügen

## Incident Response {#incident-response}

### Klassifizierung {#classification}
- **Kategorie**: Malware, unautorisierter Zugriff, DDoS, Datenpanne, Insider-Bedrohung, Phishing
- **Schweregrad**: Critical (P1), High (P2), Medium (P3), Low (P4)
- **Umfang**: einzelner Host, Netzwerksegment, gesamte Umgebung, kundenseitig

### Triage-Fragen {#triage-questions}
1. Echter Treffer oder Fehlalarm?
2. Was ist betroffen?
3. Ist die Bedrohung aktiv oder historisch?
4. Wie hoch ist die geschäftliche Auswirkung?
5. Ist eine Eskalation notwendig?

### Untersuchungsablauf {#investigation-workflow}
1. **Eingrenzung** - Ausmaß der Kompromittierung bestimmen
2. **Beweissicherung** - Logs, Speicherabbilder und Festplatten-Images sichern (Chain of Custody einhalten)
3. **Zeitleiste erstellen** - Aktionen des Angreifers rekonstruieren
4. **Ursachenanalyse** - initialer Zugriffsvektor
5. **Auswirkungsbewertung** - welche Daten und Systeme betroffen sind

### Eindämmung {#containment}
- **Kurzfristig**: Systeme isolieren, Konten deaktivieren, IPs/Domains blockieren
- **Langfristig**: Schwachstellen patchen, bei Bedarf neu aufsetzen
- Abwägung: Bedrohung eindämmen, ohne Beweise zu vernichten

### Beseitigung {#eradication}
- Malware, Backdoors und Persistenzmechanismen entfernen
- Alle potenziell kompromittierten Zugangsdaten zurücksetzen
- Ausgenutzte Schwachstellen patchen
- Erneut scannen, um die Entfernung zu verifizieren

### Wiederherstellung {#recovery}
- Aus sauberen Backups wiederherstellen
- Kompromittierte Systeme neu aufbauen
- Schrittweise Wiederanbindung mit verstärktem Monitoring
- Integrität prüfen, bevor Systeme wieder in den Produktivbetrieb gehen

### Nachbereitung {#post-incident}
- Lessons-Learned-Meeting
- Vollständige Dokumentation (Zeitleiste, Maßnahmen, Ergebnisse)
- Kontrollverbesserungen für festgestellte Lücken
- Erkennungsregeln auf Basis der Erkenntnisse aktualisieren

## SOC-Betrieb {#soc-operations}

### Tier-Modell {#tier-model}
| Tier | Rolle | Verantwortlichkeiten |
|------|------|-----------------|
| L1 | Alert-Triage | Erste Untersuchung, Identifikation von Fehlalarmen, Eskalation |
| L2 | Incident-Bearbeitung | Vertiefte Untersuchung, Forensik, Threat Hunting |
| L3 | Erweiterte Analyse | Malware-Reverse-Engineering, Tool-Entwicklung, Prozessverbesserung |

### SOC-Kennzahlen {#soc-metrics}
- **MTTD** - Zeit von Angriff bis Erkennung
- **MTTR** - Zeit von Erkennung bis Eindämmung
- **Dwell Time** - Dauer, während der der Angreifer im System war
- **Fehlalarmquote** - Verhältnis von Rauschen zu echten Alarmen
- **Abdeckung** - Anteil der überwachten Assets

## SOAR (Security Orchestration, Automation and Response) {#soar-security-orchestration-automation-and-response}

### Playbook-Automatisierungen {#playbook-automations}
- **Phishing**: IoCs extrahieren -> Threat Intelligence prüfen -> Absender blockieren -> ähnliche E-Mails in Quarantäne verschieben
- **Malware**: Host isolieren -> Beweise sichern -> nach lateraler Bewegung suchen
- **Kompromittiertes Konto**: Passwort-Reset erzwingen -> Konto deaktivieren -> Datenzugriffe prüfen
- **Schwachstellen-Alarm**: betroffene Assets prüfen -> Exposition bewerten -> Ticket anlegen

Vorteile: einheitliche Reaktion, schneller (Minuten statt Stunden), skalierbar, lückenlose Audit-Spur.

## Kritische Log-Quellen {#critical-log-sources}
- **Authentifizierung**: AD, VPN, SSO
- **Netzwerk**: Firewalls, IDS/IPS, Proxy
- **DNS**: zeigt C2-Kommunikation und Datenexfiltration
- **Endpoints**: Windows Event Log, Syslog, EDR-Telemetrie
- **E-Mail**: Zustellung, Quarantäne, Phishing-Erkennungen
- **Cloud**: CloudTrail, Azure Activity Log, GCP Audit Log
- **Datenbank**: Audit-Logs (Abfragen, Schemaänderungen)

## Stolperfallen {#gotchas}
- Ein SIEM ist nur so gut wie seine Log-Quellen: Nicht abgedeckte blinde Flecken sind die Orte, an denen sich Angreifer verstecken
- Korrelationsregeln brauchen kontinuierliches Tuning: Umgebungsänderungen machen alte Regeln verrauscht oder blind
- Beweissicherung muss vor der Eindämmung erfolgen: Das Isolieren eines Systems kann flüchtige Daten vernichten
- Incident-Dokumentation sollte in Echtzeit erfolgen, nicht nachträglich (das Gedächtnis lässt unter Druck nach)
- SOAR-Playbooks müssen regelmäßig getestet werden: Eine ungetestete automatisierte Reaktion kann mehr Schaden anrichten als der Vorfall selbst

## Siehe auch {#see-also}
- [[security-solutions-architecture]] - Implementierung von IDS/IPS, EDR, DLP
- [[windows-security-and-powershell]] - Windows-Event-IDs für SIEM-Regeln
- [[linux-system-hardening]] - auditd, Syslog-Konfiguration
- [[compliance-and-regulations]] - Anforderungen an Monitoring aus Compliance-Sicht
