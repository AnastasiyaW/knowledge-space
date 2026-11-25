---
title: "Grundlagen der Informationssicherheit"
category: concepts
tags: [security, cia-triad, risk, threat-modeling, defense-in-depth]
level: 2
source_sha256: 04613f51d205263c6e9580cab9c69454d5ec7cd906b8bfafa8bdc4f37a926f6a
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der Informationssicherheit {#information-security-fundamentals}

Grundlegende Konzepte der Informationssicherheit: die CIA-Triade, Bedrohungsmodellierung, Risikomanagement und Muster für die Sicherheitsarchitektur. Dieser Eintrag bildet die konzeptionelle Grundlage, auf der alle anderen Sicherheitsthemen aufbauen.

## Wichtige Fakten {#key-facts}
- **CIA-Triade** - Vertraulichkeit (Daten nur für Berechtigte zugänglich), Integrität (Daten korrekt und unverändert), Verfügbarkeit (Systeme bei Bedarf erreichbar)
- Die Priorisierung hängt vom Kontext ab: Banken = Integrität zuerst, Militär = Vertraulichkeit zuerst, E-Commerce = Verfügbarkeit zuerst, Gesundheitswesen = alle drei gleich gewichtet
- Risiko = Bedrohung x Schwachstelle x Auswirkung - eine Schwachstelle ohne Bedrohung ist kein Risiko
- Defense in Depth: Keine einzelne Schicht ist ausreichend; jede Schicht sollte unabhängig sein
- Zero Trust: "never trust, always verify" - auch interner Datenverkehr

## Die CIA-Triade {#the-cia-triad}

### Vertraulichkeit {#confidentiality}
Bedrohungen: Datenlecks, Abhören, Social Engineering.
Maßnahmen: Verschlüsselung, Zugriffskontrollen, Datenklassifizierung.

### Integrität {#integrity}
Bedrohungen: unautorisierte Änderungen, Man-in-the-Middle, Datenkorruption.
Maßnahmen: Hashing, digitale Signaturen, Versionskontrolle, Prüfsummen.

### Verfügbarkeit {#availability}
Bedrohungen: DDoS, Hardwareausfall, Ransomware.
Maßnahmen: Redundanz, Backups, Lastverteilung, Notfallwiederherstellung.

## Muster {#patterns}

### Defense in Depth {#defense-in-depth}
Mehrere unabhängige Schichten von Sicherheitskontrollen:
1. Physische Sicherheit (Schlösser, Kameras)
2. Netzwerksicherheit (Firewalls, IDS/IPS)
3. Host-Sicherheit (Antivirus, EDR, Härtung)
4. Anwendungssicherheit (WAF, Eingabevalidierung)
5. Datensicherheit (Verschlüsselung, DLP, Zugriffskontrollen)
6. Administrative Kontrollen (Richtlinien, Schulungen)

### Zero-Trust-Architektur {#zero-trust-architecture}
- Mikrosegmentierung des Netzwerks
- Least-Privilege-Zugriff für jede Identität
- Kontinuierliche Überprüfung jeder Anfrage
- Immer von einem Einbruch ausgehen
- Alle Kommunikation verschlüsseln, auch die interne

### Sicherheitszonen (DMZ) {#security-zones-dmz}
- **Internet** - nicht vertrauenswürdig
- **DMZ** - teilweise vertrauenswürdig, hostet öffentlich erreichbare Dienste
- **Internes Netzwerk** - vertrauenswürdig, Geschäftssysteme
- **Management-Netzwerk** - stark eingeschränkt, Infrastrukturverwaltung
- Firewalls zwischen allen Zonen mit strengen Regelwerken

## Assets und Bedrohungen {#assets-and-threats}

### Asset-Kategorien {#asset-categories}
- **Information** - Datenbanken, geistiges Eigentum, Kundendaten
- **Physisch** - Server, Netzwerkgeräte, Anlagen
- **Software** - Anwendungen, Betriebssysteme, Werkzeuge
- **Human** - Mitarbeitende, Auftragnehmer, Wissen
- **Immateriell** - Reputation, Marke, Vertrauen

### Bedrohungsakteure {#threat-actors}
| Akteur | Motivation | Kompetenzniveau |
|-------|-----------|-------------|
| Script Kiddies | Neugier, Ruhm | Niedrig (nutzen vorhandene Werkzeuge) |
| Hacktivisten | Ideologisch (z. B. Anonymous) | Niedrig bis mittel |
| Cyberkriminelle | Finanziell (Ransomware, Carding) | Mittel bis hoch |
| Insider | Groll, finanziell, erzwungen | Unterschiedlich (verfügen über legitimen Zugriff) |
| Nationalstaaten | Spionage, Störung (APT28, Lazarus) | Sehr hoch |
| Wettbewerber | Wirtschaftsspionage | Mittel |

## Risikomanagement {#risk-management}

### Qualitative Bewertung {#qualitative-assessment}
Verwendet beschreibende Skalen (Hoch/Mittel/Niedrig). Risikomatrix 5x5: Eintrittswahrscheinlichkeit (1-5) x Auswirkung (1-5). Werte 1-5 = Niedrig (akzeptieren), 6-12 = Mittel (mindern/übertragen), 13-25 = Kritisch (sofort mindern).

### Quantitative Bewertung {#quantitative-assessment}
- Asset-Wert (AV) - monetärer Wert
- Expositionsfaktor (EF) - prozentualer Verlust (0-1)
- Single Loss Expectancy (SLE) = AV x EF
- Annual Rate of Occurrence (ARO) - erwartete Vorfälle pro Jahr
- Annual Loss Expectancy (ALE) = SLE x ARO

### Optionen zur Risikobehandlung {#risk-treatment-options}
1. **Akzeptieren** - Risiko innerhalb der Risikobereitschaft, Kosten der Maßnahme übersteigen den potenziellen Verlust
2. **Mindern** - Maßnahmen umsetzen, um Eintrittswahrscheinlichkeit oder Auswirkung zu reduzieren
3. **Übertragen** - auf Dritte verlagern (Versicherung, Outsourcing)
4. **Vermeiden** - die risikoverursachende Tätigkeit beenden

## Schwachstellenmanagement {#vulnerability-management}

### CVE / CVSS / NVD {#cve-cvss-nvd}
- **CVE** - eindeutige Kennung (CVE-JAHR-NUMMER)
- **CVSS** - Schweregrad-Score von 0-10 (Base + Temporal + Environmental)
- **NVD** - von NIST gepflegte CVE-Datenbank mit CVSS-Scores

### Lebenszyklus des Patchmanagements {#patch-management-lifecycle}
1. Erkennung (Scannen nach fehlenden Patches)
2. Bewertung (Anwendbarkeit und Risiko prüfen)
3. Test (Staging-Umgebung)
4. Ausrollen (gestaffelter Produktionsrollout)
5. Verifikation (Anwendung der Patches bestätigen)
6. Dokumentation (Audit-Trail)

## Fallstricke {#gotchas}
- Der CVSS-Basisscore allein ist irreführend - immer den Umgebungskontext der eigenen Organisation berücksichtigen
- Risikoakzeptanz muss mit Freigabe durch den Fachverantwortlichen dokumentiert werden, nicht nur als Entscheidung des Sicherheitsteams
- "Compliance != Security" - ein bestandenes Audit bedeutet nicht, dass man sicher ist
- Die Schichten der Defense in Depth müssen wirklich unabhängig sein - gemeinsam genutzte Zugangsdaten über Schichten hinweg heben den Zweck auf

## Siehe auch {#see-also}
- [[cryptography-and-pki]] - Verschlüsselung, Hashing, digitale Signaturen
- [[authentication-and-authorization]] - MFA, OAuth, Kerberos
- [[compliance-and-regulations]] - GDPR, PCI DSS, ISO 27001
- [[vulnerability-scanning-and-management]] - Nessus, OpenVAS, Scanning
