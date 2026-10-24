---
title: "Data Governance und Katalog"
category: concepts
tags: [data-engineering, data-governance, data-catalog, dama, metadata]
level: 2
source_sha256: 6cbfd32be0a4febc5219c05726ac95fbde49ae845169915c06de222771ac266b
translation: machine
translated_at: '2026-10-24'
---
# Data Governance und Katalog {#data-governance-and-catalog}

Data Governance ist das Rahmenwerk aus Rollen, Richtlinien, Standards und Metriken, das ein wirksames Datenmanagement sicherstellt. Ein Data Catalog ist ein strukturiertes Inventar von Datenbeständen, das es Nutzern ermöglicht, Daten zu finden, zu verstehen und ihnen zu vertrauen.

## Datenmanagement vs. Governance {#data-management-vs-governance}

- **Datenmanagement:** operative Prozesse (wie Rollen verwaltet, Compliance nachverfolgt und Standards gepflegt werden)
- **Data Governance:** Rahmenwerk, das die Frage „Wer entscheidet was“ über Daten beantwortet

## DAMA-DMBOK-Disziplinen {#dama-dmbok-disciplines}

| Disziplin | Beschreibung |
|-----------|-------------|
| Data Governance | Rollen, Richtlinien, Standards, Metriken |
| Data Architecture | Logische/physische Struktur der Datenbestände |
| Data Modeling | ER-Diagramme, DDL, dbt-Modelle |
| Data Storage | Backups, Sicherheit, Deployment |
| Data Security | Schutz von PII/PHI, Verschlüsselung, DSGVO |
| Data Integration | ETL/ELT-Prozesse |
| Master Data & Reference | Standardisierte Definitionen, Deduplizierung |
| DWH & BI | Analytische Verarbeitung, Reporting |
| Metadata Management | Erfassen und Kategorisieren von Metadaten |
| Data Quality | Überwachung, Definition von Integrität |

## Data Catalog {#data-catalog}

Durchsuchbares Inventar mit:
- Name und Beschreibung des Datensatzes
- Speicherort (Datenbank, Schema, Tabelle)
- Eigentümer / Steward
- Aktualisierungsfrequenz, Schema, Spaltenbeschreibungen
- Tags, Klassifizierungen, Nutzungsstatistiken

### Werkzeuge {#tools}

| Werkzeug | Typ |
|----------|-----|
| **Apache Atlas** | Open-Source-Metadatenverwaltung |
| **DataHub** (LinkedIn) | Open-Source-Metadatenplattform |
| **Amundsen** (Lyft) | Open-Source-Datenerkennung |
| **Alation, Collibra** | Kommerzielle Kataloge |

## Governance-Rollen {#governance-roles}
- **Data Owner:** fachliche Verantwortung für einen Datenbereich
- **Data Steward:** tägliche Qualitäts- und Metadatenpflege
- **Data Custodian:** technische Umsetzung der Richtlinien

## DSGVO und Compliance {#gdpr-and-compliance}

Zentrale Anforderungen:
- Recht auf Auskunft, Berichtigung, Löschung
- Datenminimierung, Zweckbindung
- Datenschutz durch Technikgestaltung und datenschutzfreundliche Voreinstellungen
- Meldung von Datenschutzverletzungen innerhalb von 72 Stunden

### Umsetzung {#implementation}
- Datenklassifizierung und Tagging (PII-, PHI-Markierungen)
- Verschlüsselung im Ruhezustand und bei der Übertragung
- Zugriffskontrolle und Audit-Logging
- Anonymisierung / Pseudonymisierung
- Aufbewahrungsrichtlinien und automatisierte Löschung

## Frameworks {#frameworks}
- **TOGAF** - Framework für Unternehmensarchitektur
- **Zachman** - Architekturmatrix
- **DAMA DMBOK2** - Data Management Body of Knowledge

## Stolperfallen {#gotchas}
- Ein Data Lake ohne Governance wird zum „Data Swamp“
- Hashing ist KEINE Verschlüsselung: Hashing ist nicht umkehrbar, Verschlüsselung ist umkehrbar
- Klassifizierung muss automatisiert werden – manuelles Tagging skaliert nicht
- Governance ohne Durchsetzung ist Dokumentation, keine Governance

## Siehe auch {#see-also}
- [[data-quality]] - Qualitätsdimensionen und Überwachung
- [[data-lineage-metadata]] - Lineage und Herkunftsnachweis
- [[data-lake-lakehouse]] - Governance im Lake-Kontext
