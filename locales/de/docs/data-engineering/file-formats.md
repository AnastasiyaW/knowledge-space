---
title: "Dateiformate für Big Data"
category: reference
tags: [data-engineering, parquet, orc, avro, file-formats, columnar]
level: 2
source_sha256: 16cc63ca23429f4b5a02a14b86cc3cebc8e5922cbaf40b716536d1dae8b1bf20
translation: machine
translated_at: '2026-10-24'
---
# Dateiformate für Big Data {#file-formats-for-big-data}

Die Wahl des richtigen Dateiformats beeinflusst maßgeblich die Speichereffizienz, die Abfrageleistung und die Kompatibilität innerhalb des Hadoop/Spark-Ökosystems.

## Formatvergleich {#format-comparison}

| Format | Typ | Splittable | Schema | Kompression | Einsatzzweck |
|--------|-----|-----------|--------|-------------|----------|
| **Text/CSV** | Zeilen | Ja (unkomprimiert) | Nein | Extern | Einfacher Datenaustausch |
| **SequenceFile** | Zeilen (binäres KV) | Ja | Nein | Block/Datensatz | Zwischendaten von MR |
| **Avro** | Zeilen (binär) | Ja | Eingebettet | Block | Schema-Evolution, Streaming |
| **ORC** | Spaltenorientiert | Ja | Eingebettet | Spaltenweise | Hive-optimierte Analysen |
| **Parquet** | Spaltenorientiert | Ja | Eingebettet | Spaltenweise | Ökosystemübergreifende Analysen |

## Parquet vs. CSV {#parquet-vs-csv}

| Merkmal | Parquet | CSV |
|---------|---------|-----|
| Erhalt des Schemas | Ja (Namen + Typen) | Nein (Typen gehen verloren) |
| Kompression | Integriert, spaltenorientiert | Standardmäßig keine |
| Größe | Deutlich kleiner | Größer |
| Typsicherheit | Date bleibt Date | Date wird zu String |
| Predicate Pushdown | Ja | Nein |
| Spaltenauswahl (Column Pruning) | Ja | Nein |

## Wann was verwenden {#when-to-use-what}

| Format | Anwendungsfall |
|--------|----------------|
| **Parquet** | Standard für Analysen. Funktioniert mit Spark, Presto, Hive, Impala |
| **ORC** | Hive-optimierte Workloads. Bessere Kompression als Parquet in Hive |
| **Avro** | Schema-Evolution, Kafka-Nachrichten, Streaming-Ingest |
| **CSV/JSON** | Datenaustausch, APIs, menschenlesbare Staging-Daten |

## Wichtige Fakten {#key-facts}
- Spaltenorientierte Formate (Parquet, ORC) lesen nur die benötigten Spalten – entscheidend für breite analytische Tabellen
- Predicate Pushdown: Die Abfrage-Engine verlagert Filter in die Speicherschicht und liest nur passende Row Groups
- Parquet und ORC unterstützen beide verschachtelte Datenstrukturen
- Avro ist der Standard für die Serialisierung von Kafka-Nachrichten mit Schema Registry
- Für Big Data sollten immer Parquet/ORC bevorzugt werden; CSV nur für den Datenaustausch verwenden

## Fallstricke {#gotchas}
- CSV mit `inferSchema=True` in Spark liest die gesamte Datei – langsam bei großen Datenmengen
- Parquet-Dateien sind nicht menschenlesbar – CSV-Kopien für die Fehlersuche aufbewahren
- Kompressionscodecs (Snappy, GZIP, ZSTD) beeinflussen den Kompromiss zwischen Lesegeschwindigkeit und Dateigröße
- ORC ist eng an Hive gekoppelt; Parquet ist ökosystemneutraler

## Siehe auch {#see-also}
- [[hadoop-hdfs]] - Speicherschicht
- [[apache-spark-core]] - Lese-/Schreibformate in Spark
- [[clickhouse-engines]] - Kompression in ClickHouse
- [[data-lake-lakehouse]] - offene Tabellenformate (Delta, Iceberg, Hudi)
