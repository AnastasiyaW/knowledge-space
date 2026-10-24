---
title: "Data Lake und Lakehouse"
category: concepts
tags: [data-engineering, data-lake, lakehouse, delta-lake, iceberg, hudi]
level: 2
source_sha256: 4847fa62e0c87af4c56f10eefcdd546246d2d4c83a6b665c0d14e758b215a50f
translation: machine
translated_at: '2026-10-24'
---
# Data Lake und Lakehouse {#data-lake-and-lakehouse}

Ein Data Lake speichert alle Datentypen ohne strikte Schemavorgabe (Schema-on-Read). Ein Lakehouse kombiniert die Flexibilität der Data-Lake-Speicherung mit DWH-Funktionen wie ACID-Transaktionen und SQL-Zugriff.

## Data Lake {#data-lake}

### Was gespeichert wird {#what-it-stores}
- **Strukturiert:** Datenbanktabellen, CSV
- **Semi-strukturiert:** JSON, XML, Avro
- **Unstrukturiert:** Logs, Video, Bilder, Text

### Vorteile {#advantages}
- Skalierbar (horizontal durch Hinzufügen von Knoten)
- Wirtschaftlich (basiert auf Open Source: Hadoop, S3)
- Universell (alle Datentypen in einem System)
- Schnelles Testen von Hypothesen (kein vorgelagertes Schemadesign)

### Nachteile {#disadvantages}
- Geringe Datenqualität ohne Governance-Kontrollen
- Kann ohne Katalogisierung zu einem "Data Swamp" werden
- Schwierige Bestimmung des Datenwerts

### Modernes Muster {#modern-pattern}
1. Der Data Lake sammelt alle Rohdaten
2. DWH (oder Lakehouse) speichert verarbeitete analytische Daten

## Data Lakehouse {#data-lakehouse}

Kombiniert die Speicherung eines Data Lake mit DWH-Funktionen:
- Metadatenkataloge und Schemas
- Unterstützung für ACID-Transaktionen
- SQL-Zugriff auf die Daten
- Optimiert für BI- und ML-Workloads

## Offene Tabellenformate {#open-table-formats}

| Technologie | Wichtige Merkmale |
|-----------|--------------|
| **Delta Lake** | ACID-Transaktionen, Time Travel, Schema-Evolution, Z-Ordering |
| **Apache Iceberg** | Hidden Partitioning, Partition Evolution, Snapshot-Isolation, herstellerneutral |
| **Apache Hudi** | Upserts, inkrementelle Verarbeitung, Änderungen auf Datensatzebene, Compaction |

Alle drei bieten:
- ACID-Semantik auf Objektspeichern (S3, GCS, ADLS)
- Schema-Evolution ohne Neuschreiben der Daten
- Time Travel / Snapshot-Abfragen
- Metadatenverwaltung zur Abfrageoptimierung

## Wichtige Fakten {#key-facts}
- S3 ist für Speicherung 5-10x günstiger als HDFS
- Ein Lakehouse ermöglicht BI und ML auf denselben Daten ohne Kopieren
- Die Trennung von Speicher und Rechenleistung erlaubt unabhängige Skalierung
- Implementierungen: Databricks (Delta Lake), Snowflake, Apache Iceberg auf Spark/Trino

## Stolperfallen {#gotchas}
- Ein Data Lake ohne Governance wird zum "Data Swamp" – immer katalogisieren und dokumentieren
- Tabellenformate erfordern eine Abfrage-Engine, die sie versteht (Spark, Trino, Flink)
- Time Travel verursacht Speicherkosten – alte Snapshots müssen regelmäßig bereinigt werden
- Schema-Evolution bedeutet nicht schemalos – Schemas definieren, damit Daten auffindbar bleiben

## Siehe auch {#see-also}
- [[dwh-architecture]] - DWH-Vergleich und Entwicklung
- [[file-formats]] - Parquet, ORC, Avro im Detail
- [[data-governance-catalog]] - Vermeidung eines Data Swamps
- [[cloud-data-platforms]] - Cloud-Implementierungen
