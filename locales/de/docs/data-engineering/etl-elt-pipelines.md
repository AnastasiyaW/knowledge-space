---
title: "ETL/ELT-Pipelines"
category: concepts
tags: [data-engineering, etl, elt, pipelines, data-integration]
level: 3
source_sha256: 287713e6dd499afaa5b6f53aae04ee3c248838600a1e95746190a5d261a84930
translation: machine
translated_at: '2026-10-24'
---
_ETL/ELT-Pipelines

---
title: ETL/ELT-Pipelines
category: concepts
tags: [data-engineering, etl, elt, pipelines, data-integration]
---

# ETL/ELT-Pipelines {#etlelt-pipelines}

ETL (Extract-Transform-Load) und ELT (Extract-Load-Transform) sind die beiden grundlegenden Muster, um Daten aus Quellsystemen in analytische Speicher zu überführen. Der Unterschied liegt darin, wo die Transformation stattfindet: außerhalb oder innerhalb des Zielsystems.

## ETL vs. ELT {#etl-vs-elt}

| Aspekt | ETL | ELT |
|--------|-----|-----|
| Ort der Transformation | Externe Engine (Spark, Python) | Innerhalb des Ziel-DWH (SQL) |
| Geeignet für | Komplexe Transformationen, Legacy-Systeme | Cloud-DWH mit starker Rechenleistung |
| Latenz | Höher (zusätzlicher Zwischenschritt) | Niedriger |
| Flexibilität | Mehr Kontrolle über die Transformation | Abhängig von den SQL-Fähigkeiten des Zielsystems |
| Moderne Werkzeuge | Spark, Airflow + Python | dbt, Snowflake, BigQuery |

## Drei Schritte {#three-steps}

1. **Extract (E):** Daten aus den Quellen abrufen, gegen Spezifikationen validieren, in einem Zwischenbereich zwischenspeichern
2. **Transform (T):** Formatkonvertierung, Normalisierung der Kodierung, Aggregation, Bereinigung, Deduplizierung, Geschäftslogik
3. **Load (L):** Transformierte Daten und Metadaten in das Zielsystem schreiben (DWH, Data Mart, Lake)

## Architektur der Datenschichten {#data-layers-architecture}

```php
Sources -> [STG/Raw] -> [Core/DDS] -> [Marts] -> BI/Analytics
```

| Schicht | Zweck |
|---------|-------|
| **Staging / Raw / ODS** | Rohdaten aus den Quellen, minimale Transformation, bewahrt das ursprüngliche Format. Entkoppelt die Extraktion von der Transformation |
| **Core / DDS (Integration)** | Bereinigte, integrierte, historisch nachverfolgte Daten. Hier werden Data Vault, 3NF oder dimensionale Modellierung angewendet |
| **Mart / Presentation** | Geschäftsfertige, aggregierte Sichten (Star-Schema, flache Tabellen). Jeder Mart bedient bestimmte Konsumenten |

## Verarbeitungsmodi der Pipeline {#pipeline-processing-modes}

| Modus | Latenz | Komplexität | Geeignet für |
|------|---------|-----------|----------|
| **Batch** | Minuten bis Stunden | Niedrig | BI, Reporting, historische Analysen |
| **Micro-Batch** | Sekunden bis Minuten | Mittel | Nahezu Echtzeit-Dashboards |
| **Stream** | Millisekunden | Hoch | Betrugserkennung, Monitoring, Echtzeit-Features |

### Lambda-Architektur {#lambda-architecture}
- **Batch-Schicht:** vollständige, korrekte Daten mit höherer Latenz
- **Speed-Schicht:** Echtzeit-Näherungswerte
- **Serving-Schicht:** führt beide für Abfragen zusammen

## Muster {#patterns}

### Typische Spark-ETL {#typical-spark-etl}

```python
from pyspark.sql import SparkSession, functions as f

spark = SparkSession.builder.appName("etl").getOrCreate()

# Extract
df = spark.read.csv("s3a://bucket/raw/*.csv", header=True, schema=schema)

# Transform
result = (df
    .filter(f.col("vendor_id").isNotNull())
    .groupBy("vendor_id", f.to_date("pickup_datetime").alias("dt"))
    .agg(
        f.sum("total_amount").alias("sum_amount"),
        f.avg("tip_amount").alias("avg_tips")
    )
)

# Load
result.write.mode("overwrite").parquet("s3a://bucket/mart/daily_summary/")
```

### Schreibmodi {#write-modes}
- `overwrite` - vorhandene Daten ersetzen
- `append` - zu vorhandenen Daten hinzufügen
- `ignore` - überspringen, wenn Daten vorhanden sind
- `error` (Standard) - fehlschlagen, wenn Daten vorhanden sind

### Python-Skript für Datenmigration {#python-data-migration-script}

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://user:pass@host:port/db')
df = pd.read_sql("SELECT * FROM source WHERE dt BETWEEN %s AND %s", engine, params=[start_dt, end_dt])
df.to_sql('target_table', engine, if_exists='append', index=False)
```

## Wichtige Fakten {#key-facts}
- **Idempotenz** ist entscheidend: Ein erneuter Lauf der Pipeline mit denselben Eingaben muss dieselben Ausgaben erzeugen. Verwenden Sie den Modus `overwrite` oder Löschen-vor-Einfügen
- **Inkrementelle Ladevorgänge** verarbeiten nur neue oder geänderte Daten mithilfe von Wasserzeichen (Watermarks), CDC oder Zeitstempeln der letzten Änderung
- **Frühzeitige Filterung** verschiebt Filter möglichst nah an die Quelle, um das Datenvolumen zu reduzieren
- **Schema-first:** Explizite Schemata definieren, statt sich auf Inferenz zu verlassen
- **Partitionierte Schreibvorgänge** (`partitionBy("year", "month")`) ermöglichen effiziente nachgelagerte Lesevorgänge

## Fallstricke {#gotchas}
- Der Airflow-Parameter `schedule_interval` definiert das Intervall zwischen Läufen, nicht die Laufzeit. Ein DAG mit `@daily` und `start_date=2024-01-01` läuft erstmals am `2024-01-02`
- `catchup=True` (Standard) holt alle verpassten Intervalle seit `start_date` nach – das kann das System überlasten
- SCD2-Joins über Satelliten mit unterschiedlichen Änderungsfrequenzen verursachen eine kartesische Explosion über Datumsbereiche
- Problem kleiner Dateien: Zu viele Partitionen erzeugen winzige Dateien, was die Leistung von HDFS/S3 verschlechtert

## Siehe auch {#see-also}
- [[apache-airflow]] - Orchestrierung von Pipelines
- [[apache-spark-core]] - verteilte Verarbeitungs-Engine
- [[dwh-architecture]] - Architektur des Zielspeichers
- [[data-quality]] - Validierung von Pipelines
- [[data-lake-lakehouse]] - moderne Speicherziele
