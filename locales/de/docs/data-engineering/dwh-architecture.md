---
title: "Data-Warehouse-Architektur"
category: concepts
tags: [data-engineering, dwh, data-warehouse, olap, oltp, architecture]
level: 3
source_sha256: 6b1e53e88c61416e603d7d64eced4eae2e1ec17a385a5f722b31bc235048566e
translation: machine
translated_at: '2026-10-24'
---
# Data-Warehouse-Architektur {#data-warehouse-architecture}

Ein Data Warehouse (DWH) ist eine themenorientierte, integrierte, nicht-volatile, zeitvariante Sammlung von Daten, die zur Unterstützung von Entscheidungsprozessen organisiert ist (Bill Inmon). Ein DWH existiert, weil OLTP- und OLAP-Workloads in einem einzigen System grundsätzlich nicht miteinander vereinbar sind.

## OLTP vs. OLAP {#oltp-vs-olap}

| Merkmal | OLTP | OLAP |
|---------------|------|------|
| Zweck | Transaktionsverarbeitung | Analytische Abfragen |
| Abfragen | Einfach, häufig, identisch | Komplex, selten, ad hoc |
| Benutzer | Viele gleichzeitige | Wenige Analysten |
| Daten | Aktuell, operativ | Historisch, aggregiert |
| Operationen | Lesen/Schreiben (CRUD) | Überwiegend Lesen |
| Latenz | Mikro-/Millisekunden | Sekunden bis Minuten |
| Beispiele | PostgreSQL, MySQL (pro Service) | Snowflake, ClickHouse, Greenplum |

## DWH-Eigenschaften (Inmon) {#dwh-properties-inmon}

| Eigenschaft | Bedeutung |
|----------|---------|
| **Themenorientiert** | Deckt bestimmte Geschäftsbereiche ab; irrelevante Daten werden ausgeschlossen |
| **Integriert** | Keine Widersprüche zwischen Daten aus verschiedenen Quellen |
| **Nicht-volatil** | Daten werden nur angehängt, nie geändert oder gelöscht |
| **Zeitvariant** | Behält maximale historische Tiefe bei |

## DWH-Schichten {#dwh-layers}

```rust
Sources -> Staging Area -> Central Warehouse -> Data Marts -> BI/Analytics
```

| Schicht | Zweck |
|-------|---------|
| **Staging Area** | Landung von Rohdaten, Bereinigung und Normalisierung vor dem Laden |
| **MDM (Stammdaten)** | Referenz- und Nachschlagedaten zur Sicherstellung der Konsistenz |
| **Zentrales Warehouse** | Historische, themenorientierte, integrierte Daten |
| **Data Marts / Cubes** | Spezialisierte Sichten für bestimmte analytische Aufgaben |

## Entwurfsansätze {#design-approaches}

### Kimball (Bottom-Up) {#kimball-bottom-up}
- DWH = Sammlung von Data Marts
- Marts pro Bedarf der Nutzer entwerfen (Star Schema)
- Schnell im Liefern von Geschäftswert
- **Nachteile:** Marts können Kennzahlen unterschiedlich definieren; schwer zu standardisieren

### Inmon (Top-Down) {#inmon-top-down}
- Zuerst unternehmensweites DWH aufbauen (3NF), dann Marts ableiten
- Einzige Quelle der Wahrheit, bessere Konsistenz
- **Nachteile:** längere initiale Entwicklung, komplexer

### Data Vault 2.0 {#data-vault-20}
- Verarbeitet viele Quellen mit unterschiedlichen Schemata
- Nur anhängend (Append-only), vollständige Nachvollziehbarkeit
- Geschäftsregeln in der Mart-Schicht isoliert
- Details siehe [[data-vault]]

## Plattformentwicklung {#platform-evolution}

```rust
Gen 1: RDBMS DWH (Oracle, DB2) - 1990s
  -> Rigid schema, ETL, batch only

Gen 2: Hadoop ecosystem (HDFS + MapReduce) - 2007+
  -> Data Lake, schema-on-read, horizontal scale

Gen 3: Cloud DWH + Lakehouse - 2015+
  -> Snowflake, Databricks, BigQuery
  -> ELT, auto-scaling, separation of compute/storage

Gen 4: Data Mesh / Data Products - 2020+
  -> Domain-owned data, self-serve platform, federated governance
```

## Auswahl der Architektur {#choosing-architecture}

| Szenario | Empfehlung |
|----------|-------------|
| Kleines Unternehmen, strukturierte Daten, BI-Fokus | Cloud DWH (Snowflake, BigQuery) |
| Gemischte Datentypen, ML-Workloads | Data Lakehouse (Databricks, Iceberg) |
| Unternehmen, viele Quellen, Compliance | Hybrid aus DWH und Data Lake |
| Echtzeit- und Batch-Analytik | Lambda/Kappa mit Streaming-Schicht |
| Viele autonome Data-Teams | Data Mesh mit Self-Service-Plattform |

## Stolperfallen {#gotchas}
- Denormalisierung im Star Schema tauscht Speicher gegen Abfrageleistung - für OLAP akzeptabel
- Data Vault erzeugt viele Joins - die Mart-Schicht muss für akzeptable Abfrageleistung vorab joinen
- OLTP-Datenbanken sollten niemals direkt für Analysen abgefragt werden - immer in das DWH replizieren
- Das Batch-Fenster muss vor Geschäftsbeginn abgeschlossen sein - SLA-Verletzungen überwachen und alarmieren
- Ein Data Lake ohne Governance wird zum „Data Swamp“

## Siehe auch {#see-also}
- [[data-modeling]] - Theorie der Normalisierung
- [[dimensional-modeling]] - Kimballs Star- und Snowflake-Schemata
- [[data-vault]] - Data-Vault-Methodik
- [[data-lake-lakehouse]] - Lake- und Lakehouse-Muster
- [[cloud-data-platforms]] - Cloud-DWH-Implementierungen
