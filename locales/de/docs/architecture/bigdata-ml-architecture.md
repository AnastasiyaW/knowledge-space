---
title: "Big Data und ML-Architektur"
category: concepts
tags: [bigdata, machine-learning, data-pipeline, etl, data-lake, data-warehouse, mlops]
level: 4
source_sha256: 823c926fc6606e0e3e009ce22827b4f44d7948e61fb7d1dfe41a46da8aa6f647
translation: machine
translated_at: '2026-10-24'
---
# Big Data und ML-Architektur {#big-data-and-ml-architecture}

Architektur für die Verarbeitung großer Datenmengen und die Integration von ML-Modellen in den Produktivbetrieb. Der Architekt wählt geeignete Verarbeitungsplattformen, entwirft Datenpipelines und stellt die Data Governance sicher.

## Datenverarbeitungsparadigmen {#data-processing-paradigms}

| Paradigma | Verarbeitung | Technologien | Geeignet für |
|----------|-----------|--------------|----------|
| **Batch** | Zeitgesteuerte Intervalle, große Volumen | Hadoop, Spark, Hive | ETL, Berichte, historische Analysen |
| **Stream** | Kontinuierlich, Echtzeit | Kafka Streams, Flink, Storm | Betrugserkennung, Echtzeit-Empfehlungen |

### Lambda-Architektur {#lambda-architecture}
Kombiniert Batch und Stream. Batch-Schicht (korrekt), Speed-Schicht (Echtzeit), Serving-Schicht führt beide zusammen. **Nachteil:** Pflege zweier Codebasen.

### Kappa-Architektur {#kappa-architecture}
Ausschließlich Stream-Verarbeitung für alles. Neuverarbeitung durch Wiedergabe des Streams. Einfacher, aber nicht für alle Workloads geeignet.

## Datenspeicherlösungen {#data-storage-solutions}

| Lösung | Ansatz | Technologien | Risiko |
|----------|----------|-------------|------|
| **Data Lake** | Rohdaten, Schema-on-Read | HDFS, S3, Azure Data Lake | "Data Swamp" ohne Governance |
| **Data Warehouse** | Aufbereitete Daten, Schema-on-Write | Snowflake, BigQuery, Redshift, ClickHouse | Starre Schemaänderungen |
| **Data Lakehouse** | Flexibilität des Lake + Struktur des Warehouse | Delta Lake, Apache Iceberg, Hudi | Neuer, weniger ausgereift |

### Ansätze zur Datenmodellierung {#data-modeling-approaches}

| Modell | Laden | Änderungsverfolgung | Geeignet für |
|-------|---------|----------------|----------|
| **Inmon (3NF)** | Komplex (Abhängigkeitsreihenfolge) | Schlecht | Bereits normalisierte Quellen |
| **Kimball (Star)** | Einfacher | SCD Typ 2 erhöht die Komplexität | Einfache Analysen |
| **Data Vault** | Am einfachsten (unabhängige Ladevorgänge) | Nativ (Satelliten + Zeitstempel) | Sich entwickelnde, veränderliche Daten |
| **Anchor Model** | Am flexibelsten | Am flexibelsten | Extreme Flexibilitätsanforderungen |

## ETL vs. ELT {#etl-vs-elt}

| Ansatz | Prozess | Geeignet für |
|----------|---------|----------|
| **ETL** | Transformation vor dem Laden | Klassisches DWH |
| **ELT** | Rohdaten laden, im Ziel transformieren | Moderne Cloud-DWH (nutzt skalierbare Rechenleistung) |

## ML-Pipeline {#ml-pipeline}

```php
Data collection -> Preparation/cleaning -> Feature engineering ->
  Model training -> Evaluation -> Deployment -> Monitoring/retraining
```

### Muster für die Modellbereitstellung {#model-serving-patterns}

| Muster | Beschreibung | Anwendungsfall |
|---------|-------------|----------|
| **Batch-Vorhersage** | Vorab berechnete Vorhersagen | Empfehlungen, Risikobewertungen |
| **Echtzeit-Inferenz** | Online-Vorhersage über API | Suche, Betrugserkennung |
| **Edge-Inferenz** | Auf dem Gerät | Mobile Geräte, IoT |
| **Eingebettetes Modell** | Modell im App-Code | Leichtgewichtige Vorhersagen |

### MLOps {#mlops}
Anwendung von DevOps auf ML: Versionierung von Daten und Modellen, automatisierte Trainingspipelines, A/B-Tests für Deployments, Überwachung von Model Drift.

**Feature Store:** Zentrales Repository für ML-Features. Konsistenz zwischen Training und Serving. Produkte: Feast, Tecton, Vertex AI Feature Store.

## Beispiel für eine Datenpipeline-Architektur {#data-pipeline-architecture-example}

```bash
[Source 1C] --> [Kafka topic] --> [Airflow orchestrator] --> [DWH (PostgreSQL)]
[Source CRM] --> [Kafka topic] -->                               |
[External API] --> [API Fetcher] -->                             |
                                                          [Data Marts]
                                                               |
                                                          [BI Dashboard]
```

**Wichtige Entscheidungen:**
- Interne Systeme **pushen** Änderungen an Kafka (die Quelle weiß, wann sich Daten ändern)
- Externe API: **Pull** (unser System ruft sie periodisch ab)
- Airflow für die ETL-Orchestrierung (Monitoring, Wiederholungen, Fehlerbehandlung)
- Eigene PHP/Python-Skripte sind dringend abzuraten – stattdessen geeignete Orchestrierung verwenden

## Technologie-Stack {#technology-stack}

| Kategorie | Technologien |
|----------|-------------|
| Batch-Verarbeitung | Hadoop, Spark, Hive |
| Stream-Verarbeitung | Kafka Streams, Flink, Spark Streaming |
| Speicher | HDFS, S3, Delta Lake |
| Data Warehouse | Snowflake, BigQuery, Redshift, ClickHouse |
| Orchestrierung | Airflow, Prefect, Dagster |
| ML-Plattformen | MLflow, Kubeflow, SageMaker, Vertex AI |
| Datenqualität | Great Expectations, dbt-Tests |

## Architekturüberlegungen {#architecture-considerations}

- **Volumen** – TB vs. PB bestimmt die Wahl von Speicher und Verarbeitung
- **Geschwindigkeit** – Echtzeitanforderungen bestimmen Stream- vs. Batch-Verarbeitung
- **Vielfalt** – strukturiert/semi-strukturiert/unstrukturiert beeinflusst den Speicher
- **Data Governance** – Datenschutz (DSGVO), Zugriffskontrolle, Audit-Trails, Lineage
- **Kosten** – passende Dimensionierung der Rechenleistung, Speicher-Tiering, Spot-Instanzen
- **Datenqualität** – Garbage in = Garbage out. Am Eingang der Pipeline validieren

## Fallstricke {#gotchas}

- **Data Lake ohne Governance** wird zum "Data Swamp" – niemand kann Daten finden oder ihnen vertrauen
- **Echtzeit ist nicht immer nötig** – ein täglicher Batch kann genügen, etwa für eine Geschäftsleitung, die Morgenberichte prüft
- **Quelldaten ändern sich nachträglich** – Verkaufsdaten können sich über ein Jahr oder länger ändern (Erstattungen, Neuberechnungen). Für unveränderliche Historie entwerfen (Data Vault)
- **Pull aus der Quelldatenbank ist riskant** – man kennt nicht alle Datenänderungen, und Schemaänderungen brechen Skripte. Push-Modell bevorzugen

## Siehe auch {#see-also}

- [[kafka-architecture]] - Event-Streaming für Datenpipelines
- [[database-selection]] - OLTP vs. OLAP, Datenbanktypen
- [[distributed-systems-fundamentals]] - Partitionierung und Replikation für Big Data
- [[devops-cicd]] - MLOps als Erweiterung von DevOps
