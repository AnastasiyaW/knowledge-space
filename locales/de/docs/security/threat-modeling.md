---
title: "Bedrohungsmodellierung"
category: concepts
tags: [security, threat-modeling, risk-assessment, information-security, compliance]
level: 3
source_sha256: 9758fbc8a05793b7a6fe6f4ef43ad2f0a3cc80aabce3364df2e5c6ef867bcb69
translation: machine
translated_at: '2026-10-24'
---
# Bedrohungsmodellierung {#threat-modeling}

Systematischer Prozess zur Identifizierung, Bewertung und Dokumentation potenzieller Bedrohungen für die Informationswerte einer Organisation. Er erzeugt formale Bedrohungsmodell-Dokumente, die Sicherheitskontrollen, Architekturentscheidungen und Compliance steuern.

## Wichtige Fakten {#key-facts}
- Das allgemeine Bedrohungsmodell umfasst die gesamte Infrastruktur der Organisation; private Modelle beziehen sich auf bestimmte Systeme
- Zuerst das allgemeine Modell erstellen, dann private Modelle für einzelne Informationsressourcen ableiten
- Bedrohungsdatenbanken (nationale Schwachstellenregister) stellen standardisierte Bedrohungskataloge bereit
- Ein Bedrohungsmodell ist ein lebendes Dokument – es muss aktualisiert werden, wenn sich Infrastruktur, Werte oder die Bedrohungslage ändern
- Bedrohungsmodelle sind in den meisten Security-Compliance-Frameworks vorgeschrieben (ISO 27001, NIST, lokale Vorschriften)

## Allgemeines vs. privates Bedrohungsmodell {#general-vs-private-threat-models}

### Allgemeines Bedrohungsmodell {#general-threat-model}

Deckt die gesamte Informationsinfrastruktur einer Organisation ab – alle Systeme, Netzwerke und Datenwerte zusammen.

**Zweck**: Eine Ausgangsbasis für Bedrohungen festlegen, die in der gesamten Organisation gelten. Private Modelle werden daraus abgeleitet.

**Entwicklungsprozess**:

1. **Informationswerte erfassen**: Alle Informationsressourcen identifizieren (HR-Systeme, Produktionssteuerung, Kundendatenbanken, interne Netzwerke)
2. **Bedrohungsdatenbanken heranziehen**: Nationale/internationale Schwachstellendatenbanken für standardisierte Bedrohungskataloge nutzen
3. **Falls ein früheres Bedrohungsregister existiert**: Dieses als Grundlage verwenden – es filtert bereits die für die Organisation relevanten Bedrohungen
4. **Bedrohungen den Werten zuordnen**: Bestimmen, welche Bedrohungen auf welche Kategorien von Systemen zutreffen
5. **Eintrittswahrscheinlichkeit und Auswirkung bewerten**: Bedrohungen nach Wahrscheinlichkeit und potenziellem Schaden priorisieren
6. **Gegenmaßnahmen dokumentieren**: Bestehende und geplante Sicherheitskontrollen pro Bedrohung

### Privates Bedrohungsmodell {#private-threat-model}

Deckt eine bestimmte Informationsressource oder eine Gruppe identischer Ressourcen ab.

**Beispiele**:
- System zur Verarbeitung personenbezogener Mitarbeiterdaten
- System zur Verarbeitung personenbezogener Kundendaten
- Industrielles Steuerungssystem (SCADA/ICS) für eine Produktionslinie
- Gruppe identischer Systeme über mehrere Standorte hinweg (gleicher Hersteller, gleiche Komponenten)

**Ableitung aus dem allgemeinen Modell**:

1. Vom allgemeinen Bedrohungsmodell ausgehen
2. Bedrohungen auf die für das konkrete System relevanten einschränken
3. Systemspezifische Bedrohungen ergänzen, die im allgemeinen Modell nicht abgedeckt sind
4. Konkrete Angriffsvektoren für die Architektur des Systems detaillieren
5. Systemspezifischen Sicherheitskontrollen zuordnen
6. Nach Anwendung der Kontrollen die Restrisiken dokumentieren

## Aufbau des Bedrohungsmodells {#threat-model-structure}

### Minimale Dokumentabschnitte {#minimal-document-sections}

```bash
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

## Gängige Frameworks {#common-frameworks}

| Framework | Schwerpunkt | Geeignet für |
|-----------|-------------|--------------|
| **STRIDE** | Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation | Bedrohungsmodellierung von Software/Anwendungen |
| **PASTA** | Process for Attack Simulation and Threat Analysis | Risikozentriert, geschäftsorientiert |
| **OCTAVE** | Operationally Critical Threat, Asset, and Vulnerability Evaluation | Risikobewertung für die gesamte Organisation |
| **DREAD** | Damage, Reproducibility, Exploitability, Affected users, Discoverability | Bewertung und Priorisierung von Bedrohungen |

### STRIDE je Element {#stride-per-element}

Die STRIDE-Kategorien auf jede Komponente eines Datenflussdiagramms anwenden:

| Komponente | Relevante STRIDE-Bedrohungen |
|------------|------------------------------|
| Externe Entität | Spoofing (Identitätsvortäuschung) |
| Prozess | Alle sechs Kategorien |
| Datenspeicher | Tampering (Manipulation), Information Disclosure (Informationsoffenlegung), Denial of Service (Dienstverweigerung) |
| Datenfluss | Tampering (Manipulation), Information Disclosure (Informationsoffenlegung), Denial of Service (Dienstverweigerung) |
| Vertrauensgrenze | Alle Bedrohungen an Grenzübergängen |

## Praktischer Ablauf {#practical-workflow}

```php
1. Define scope -> 2. Build DFD -> 3. Identify threats (STRIDE/catalog)
    -> 4. Rate risk (likelihood x impact) -> 5. Plan mitigations
    -> 6. Document -> 7. Review periodically
```

### Datenflussdiagramm (DFD) {#data-flow-diagram-dfd}

Die Grundlage der Bedrohungsmodellierung – es zeigt, wie sich Daten durch das System bewegen:

```php
[User] --HTTPS--> [Web Server] --SQL--> [Database]
                       |
                  [Auth Service] --LDAP--> [Active Directory]
```

Vertrauensgrenzen (gestrichelte Linien) dort markieren, wo sich die Privilegienstufe ändert. Bedrohungen konzentrieren sich an Grenzübergängen der Vertrauensgrenzen.

## Stolperfallen {#gotchas}
- **Zuerst das allgemeine Modell**: Wer das allgemeine Modell überspringt und direkt zu privaten Modellen geht, erzeugt Lücken – organisationsweite Bedrohungen bleiben unentdeckt, wenn jedes Team nur das eigene System betrachtet
- **Bedrohungsmodell != Schwachstellenscan**: Die Bedrohungsmodellierung ist strategisch (was KÖNNTE passieren), der Schwachstellenscan ist taktisch (was ist JETZT ausnutzbar). Beide werden benötigt, keines ersetzt das andere
- **Veraltete Bedrohungsmodelle sind gefährlich**: Ein Bedrohungsmodell von vor zwei Jahren kann Cloud-Migration, neue Remote-Arbeitsmuster oder aufkommende Angriffstechniken übersehen. Mindestens jährlich und nach jeder größeren Infrastrukturänderung überprüfen
- **Identische Systeme an mehreren Standorten**: Betreiben mehrere Standorte dasselbe System (gleicher Hersteller, gleiche Konfiguration), kann ein einziges privates Bedrohungsmodell alle Instanzen abdecken – eine Duplizierung ist nicht nötig

## Siehe auch {#see-also}
- [[information-security-fundamentals]] - zentrale Sicherheitskonzepte
- [[compliance-and-regulations]] - regulatorische Frameworks, die Bedrohungsmodelle verlangen
- [[vulnerability-scanning-and-management]] - taktische Ergänzung zur strategischen Bedrohungsmodellierung
- [[security-solutions-architecture]] - Umsetzung der durch Bedrohungsmodelle identifizierten Kontrollen
