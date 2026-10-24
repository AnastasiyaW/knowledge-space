---
title: "Social Engineering und Phishing"
category: concepts
tags: [security, social-engineering, phishing, email-security, human-factors]
level: 3
source_sha256: be8bac5e9ebee7d11d688df8534bb2ff122d3799eff12913f8e708c351a10e31
translation: machine
translated_at: '2026-10-24'
---
# Social Engineering und Phishing {#social-engineering-and-phishing}

Auf Menschen abzielende Angriffsvektoren: Phishing (Spear-Phishing, Whaling, Vishing), Pretexting, Erkennung von E-Mail-Spoofing (SPF/DKIM/DMARC), Analyse von E-Mail-Headern und Untersuchungstechniken für Breach-Datenbanken.

## Wichtige Fakten {#key-facts}
- Spear-Phishing zielt mit personalisierten Inhalten auf bestimmte Personen ab; Whaling zielt auf Führungskräfte
- SPF, DKIM und DMARC verhindern gemeinsam E-Mail-Spoofing; alle drei müssen geprüft werden
- Die weltweiten Verluste durch Business Email Compromise (BEC) übersteigen die Verluste durch Ransomware
- Die `Received:`-Kette im E-Mail-Header zeichnet den vollständigen Übertragungsweg nach
- Breach-Datenbanken (HIBP) ermöglichen Angriffe mit wiederverwendeten Zugangsdaten über mehrere Dienste hinweg
- Physisches Social Engineering (Tailgating, Identitätsvortäuschung) umgeht sämtliche digitalen Kontrollen

## Phishing-Typen {#phishing-types}

| Typ | Ziel | Methode |
|-----|------|---------|
| Phishing | Massen/zufällig | Generische E-Mails, gefälschte Login-Seiten |
| Spear-Phishing | Bestimmte Personen | Personalisierte, kontextbezogene Inhalte |
| Whaling | Führungskräfte/C-Level | Vortäuschung von Vorstand, Rechtsabteilung |
| Vishing | Telefonische Ziele | Sprachbasierte Identitätsvortäuschung |
| Smishing | SMS-Empfänger | Schädliche Links per Textnachricht |

## Werkzeuge für Phishing-Kampagnen {#phishing-campaign-tools}
- **GoPhish** - Open-Source-Framework für Phishing-Simulationen in Awareness-Tests
- **King Phisher** - Toolkit für Phishing-Kampagnen
- Landing Pages zum Abgreifen von Zugangsdaten
- Schädliche Anhänge: Dokumente mit Makros, HTML Smuggling

## Pretexting {#pretexting}
Erfundene Szenarien zur Manipulation von Zielpersonen:
- Vortäuschung des IT-Supports („Wir benötigen Ihre Zugangsdaten, um ein Problem zu beheben“)
- Vortäuschung eines Lieferanten („Rechnungszahlung überfällig“)
- Vortäuschung einer Führungskraft („Überweisung dringend erforderlich“)
- Physisch: Tailgating durch gesicherte Türen, Tragen gefälschter Ausweise

## E-Mail-Authentifizierung {#email-authentication}

### SPF (Sender Policy Framework) {#spf-sender-policy-framework}
DNS-TXT-Eintrag, der die IP-Adressen autorisierter Mailserver auflistet:
```ini
v=spf1 mx ip4:203.0.113.0/24 include:_spf.google.com -all
```

### DKIM (DomainKeys Identified Mail) {#dkim-domainkeys-identified-mail}
Kryptografische Signatur im E-Mail-Header, die die Integrität der Nachricht und die sendende Domain belegt.

### DMARC (Domain-based Message Authentication) {#dmarc-domain-based-message-authentication}
Richtlinie für den Umgang mit SPF- und DKIM-Fehlern:
```ini
v=DMARC1; p=reject; rua=mailto:dmarc@example.com
```
Richtlinien: `none` (nur überwachen), `quarantine` (Spam-Ordner), `reject` (blockieren).

## Analyse von E-Mail-Headern {#email-header-analysis}
```sql
Received: chain          - full routing path (read bottom-up)
X-Originating-IP         - sender's real IP
Message-ID               - domain should match sender
Return-Path vs From      - mismatch = likely spoofing
Authentication-Results    - SPF/DKIM/DMARC pass/fail
```

## Untersuchung von Breach-Datenbanken {#breach-database-investigation}
- **Have I Been Pwned** (HIBP) - legitime Prüfung auf Datenlecks
- **DeHashed / IntelX** - erweiterte Suche in Breach-Daten (inklusive Passwörter)
- E-Mail-Adresse -> Passwort aus einem Datenleck -> Wiederverwendung desselben Passworts bei anderen Diensten
- Holehe: Prüfung, ob eine E-Mail-Adresse bei Diensten registriert ist, ohne den Benutzer zu alarmieren

## Stolperfallen {#gotchas}
- Ein bestandener SPF-Check allein verhindert kein Spoofing des Anzeigenamens (From: "CEO Name" <attacker@evil.com>)
- DMARC mit `p=none` bietet nur Überwachung, aber keinen Schutz; erforderlich sind `p=quarantine` oder `p=reject`
- Schulungen zur Security-Awareness senken die Klickraten, beseitigen sie aber nie vollständig (manche Mitarbeitenden klicken immer)
- Fortgeschrittenes Phishing nutzt kompromittierte legitime Konten und besteht sämtliche Authentifizierungsprüfungen
- KI-generierte Phishing-Inhalte sind von legitimer Kommunikation zunehmend nicht mehr zu unterscheiden

## Siehe auch {#see-also}
- [[penetration-testing-methodology]] - Social Engineering in Penetrationstests
- [[osint-and-reconnaissance]] - Informationsbeschaffung für gezieltes Phishing
- [[siem-and-incident-response]] - Playbooks für die Reaktion auf Phishing
- [[anti-fraud-behavioral-analysis]] - Erkennung von Phishing im großen Maßstab
