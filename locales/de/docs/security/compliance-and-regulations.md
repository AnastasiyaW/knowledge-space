---
title: "Compliance und Regulierung"
category: concepts
tags: [security, compliance, gdpr, pci-dss, iso-27001, nist, audit]
level: 2
source_sha256: f14b8af06066ad54b15ae611151bce7f6683ffdfaa7834f5a7792c9b08cd130b
translation: machine
translated_at: '2026-10-24'
---
# Compliance und Regulierung {#compliance-and-regulations}

Regulatorische Rahmenwerke und Compliance-Anforderungen: ISO 27001, NIST Cybersecurity Framework, PCI DSS, DSGVO, Richtlinienhierarchie, Risikobewertung für Compliance, Nachweiserhebung und Audit-Vorbereitung.

## Wichtige Fakten {#key-facts}
- Compliance != Security - das Bestehen eines Audits bedeutet nicht, dass Sie sicher sind
- DSGVO-Bußgelder: bis zu 4 % des weltweiten Jahresumsatzes oder 20 Mio. EUR (je nachdem, welcher Betrag höher ist)
- Die DSGVO verlangt eine Meldung von Datenschutzverletzungen an die Aufsichtsbehörde innerhalb von 72 Stunden
- PCI DSS verlangt vierteljährliche Schwachstellenscans und jährliche Penetrationstests
- ISO 27001 verwendet den Plan-Do-Check-Act-Zyklus mit 114 Maßnahmen in 14 Domänen
- NIST CSF: fünf Funktionen - Identify, Protect, Detect, Respond, Recover

## Internationale Standards {#international-standards}

### ISO 27001 (ISMS) {#iso-27001-isms}
Informationssicherheits-Managementsystem:
- Plan-Do-Check-Act-Zyklus zur kontinuierlichen Verbesserung
- Anhang A: 114 Maßnahmen in 14 Domänen
- Risikobasierter Ansatz - Maßnahmen werden auf Grundlage der Bewertung ausgewählt
- Die Zertifizierung erfordert ein externes Audit
- Weltweit anerkannt

### NIST Cybersecurity Framework {#nist-cybersecurity-framework}
Fünf Funktionen: **Identify** -> **Protect** -> **Detect** -> **Respond** -> **Recover**
- Stufen (Tiers): Partial (1), Risk Informed (2), Repeatable (3), Adaptive (4)
- Implementierungsprofile: Ist-Zustand vs. Soll-Zustand
- Freiwillig, aber weit verbreitet

### NIST 800-53 {#nist-800-53}
Umfassender Katalog von Sicherheitsmaßnahmen:
- 20 Maßnahmenfamilien (AC, AU, CM, IA, IR, SC, SI usw.)
- Maßnahmen sind Auswirkungsstufen zugeordnet (Low, Moderate, High)
- Grundlage für FedRAMP- und FISMA-Compliance

### PCI DSS {#pci-dss}
Payment Card Industry Data Security Standard:
- 12 Anforderungen für die Verarbeitung von Karteninhaberdaten
- Netzwerksegmentierung, Verschlüsselung, Zugriffskontrolle, Überwachung
- Vierteljährliche Schwachstellenscans (ASV)
- Jährliche Penetrationstests
- Compliance-Stufen auf Basis des Transaktionsvolumens
- SAQ für kleinere Händler, ROC für große

### DSGVO {#gdpr}
EU-Datenschutzverordnung mit extraterritorialer Wirkung:
- **Rechtsgrundlage**: Einwilligung, Vertrag, rechtliche Verpflichtung, lebenswichtige Interessen, öffentliches Interesse, berechtigtes Interesse
- **Betroffenenrechte**: Auskunft, Berichtigung, Löschung (Recht auf Vergessenwerden), Datenübertragbarkeit, Widerspruch
- **DSB** erforderlich bei umfangreicher Verarbeitung
- **Meldung von Datenschutzverletzungen innerhalb von 72 Stunden**
- **Privacy by Design** - Sicherheit von Beginn an integriert
- **Datenminimierung** - nur erheben, was erforderlich ist

## Richtlinienhierarchie {#policy-hierarchy}
1. **Sicherheitsrichtlinie** - übergeordnete Ziele und Bekenntnis der Geschäftsleitung
2. **Standards** - verbindliche Anforderungen (Verschlüsselungsstandards, Passwortstandards)
3. **Verfahren** - schrittweise Anleitungen zur Umsetzung
4. **Leitlinien** - Empfehlungen und bewährte Praktiken (optional)

## Risikobewertung für Compliance {#risk-assessment-for-compliance}
1. Asset-Inventar - was geschützt werden muss
2. Bedrohungsidentifikation
3. Schwachstellenidentifikation
4. Auswirkungsbewertung
5. Eintrittswahrscheinlichkeit
6. Risikobehandlung den Compliance-Anforderungen zuordnen:
   - Regulierung verlangt Verschlüsselung -> AES-256 für ruhende Daten implementieren
   - Regulierung verlangt Protokollierung -> Audit-Trail-System einrichten
   - Regulierung verlangt Erkennung von Datenschutzverletzungen -> SIEM mit Alarmierung implementieren

## Nachweiserhebung {#evidence-collection}
| Nachweistyp | Beispiele |
|-------------|-----------|
| Konfiguration | Screenshots und Exporte von Systemeinstellungen |
| Scan-Berichte | Schwachstellenscans, Pentest-Ergebnisse |
| Log-Stichproben | Nachweis der Überwachungsfähigkeit |
| Richtliniendokumente | Genehmigte und aktuelle Versionen |
| Schulungsnachweise | Abschluss der Sensibilisierungsschulungen für Mitarbeiter |
| Vorfallberichte | Nachweis der Reaktionsfähigkeit |
| Change Management | Nachweise kontrollierter Änderungen |

## Audit-Vorbereitung {#audit-preparation}

### Internes Audit {#internal-audit}
- Regelmäßige Selbstbewertung anhand der Rahmenwerke
- Gap-Analyse: Ist-Zustand vs. Soll-Zustand
- Planung der Behebung mit Verantwortlichen und Fristen
- Evidenz-Repository kontinuierlich pflegen

### Externes Audit {#external-audit}
- Bewertung der Auditbereitschaft vor dem Audit
- Dokumente und Nachweise organisieren
- Schlüsselpersonal auf Interviews vorbereiten
- Stichprobenmethodik verstehen
- Korrekturmaßnahmen für Feststellungen planen

### Schweregrad von Feststellungen {#finding-severity}
| Stufe | Bedeutung |
|-------|-----------|
| Major Nonconformity | Erhebliches Maßnahmenversagen, verhindert die Zertifizierung |
| Minor Nonconformity | Maßnahme existiert, weist aber Lücken auf |
| Observation | Verbesserungsbereich, kein Versagen |
| Opportunity for Improvement | Vorschlag, keine Feststellung |

## Stolperfallen {#gotchas}
- Compliance-Rahmenwerke überschneiden sich stark - Maßnahmen einmal abbilden und auf mehrere Standards anwenden
- "Compliance nach Checkliste" erzeugt falsche Sicherheit - Compliance ist ein Minimum, keine Obergrenze
- Das "Recht auf Vergessenwerden" der DSGVO steht im Konflikt mit Backup-Aufbewahrung - einen dokumentierten Prozess festlegen
- Die Reduzierung des PCI-DSS-Geltungsbereichs durch Netzwerksegmentierung spart enormen Compliance-Aufwand
- Audit-Nachweise müssen zeitnah sein (aus dem Prüfzeitraum stammen), nicht nachträglich erstellt werden
- Compliance von Drittanbietern/Dienstleistern (SOC-2-Berichte) bedeutet nicht, dass Ihre Nutzung ihres Dienstes konform ist

## Siehe auch {#see-also}
- [[information-security-fundamentals]] - Konzepte des Risikomanagements
- [[siem-and-incident-response]] - überwachungsgetriebene Compliance
- [[security-solutions-architecture]] - Umsetzung von Maßnahmen
- [Database Security](database-security.md) - Anforderungen an den Datenschutz
