---
title: "HBase"
category: tools
tags: [data-engineering, hbase, nosql, columnar, hadoop, key-value]
level: 2
source_sha256: 63f49e4fe6fe4700ad91cdc880155c0bbca4d0ac61e09e4b0a1349c50570fc5f
translation: machine
translated_at: '2026-10-24'
---
# HBase {#hbase}

HBase ist ein spaltenorientierter NoSQL-Speicher im Hadoop-Ökosystem, ausgelegt für Milliarden von Zeilen und Millionen von Spalten. Läuft auf HDFS. Kein SQL, stattdessen API-Methoden (GET, PUT, SCAN, DELETE).

## Datenmodell {#data-model}

```text
Table
  |-- Row Key (primary access path, binary sorted)
  |-- Column Family 1
  |     |-- column1: value (timestamp v3)
  |     |-- column1: value (timestamp v2)  <- versioning
  |     |-- column2: value
  |-- Column Family 2
        |-- columnA: value
```

## Zentrale Konzepte {#key-concepts}

| Konzept | Details |
|---------|---------|
| **Row Key** | Eindeutige ID, JEDER Zugriff erfolgt über den Row Key oder einen Key-Bereich |
| **Column Family** | Wird bei der Erstellung definiert. Gruppiert Spalten mit gemeinsamen Eigenschaften (Komprimierung, TTL, Versionen) |
| **Versionierung** | Integriert. Mehrere Versionen pro Zelle mit Zeitstempeln. Pro Family konfigurierbar |
| **Binäre Speicherung** | Alle Werte werden binär gespeichert. Die Serialisierung übernimmt die Anwendung |
| **Freies Schema** | Spalten werden dynamisch innerhalb bestehender Column Families hinzugefügt |

## HBase vs. RDBMS {#hbase-vs-rdbms}

| Merkmal | HBase | RDBMS |
|---------|-------|-------|
| Schema | Flexibel | Fest |
| Skalierung | Milliarden von Zeilen | Begrenzt (sofern kein MPP) |
| Zugriffsmuster | Key- und Key-Bereichs-Abfragen | Beliebiges SQL |
| Joins | Nicht nativ | Vollständig unterstützt |
| Transaktionen | Zeilenweise atomar | ACID über Tabellen hinweg |
| Abfragesprache | API-Aufrufe | SQL |

## Eigenschaften {#properties}
- Column Families werden getrennt auf HDFS gespeichert
- Effizient für Key- und Key-Bereichs-Abfragen
- TTL für automatisches Ablaufen von Daten
- MapReduce-Integration (Input/Output)
- Versionen werden in absteigender Reihenfolge gespeichert (neueste zuerst)

## Stolperfallen {#gotchas}
- Kein SQL: Der gesamte Zugriff erfolgt über die API mit GET, PUT, SCAN, DELETE
- Das Design des Row Keys ist entscheidend: Ein ungünstiger Key führt zu Hotspots
- Column Families müssen bei der Tabellenerstellung definiert werden
- Nicht geeignet für beliebige analytische Abfragen (dafür Hive/Spark darüber nutzen)

## Siehe auch {#see-also}
- [[hadoop-hdfs]] - zugrunde liegender Speicher
- [[clickhouse]] - alternatives spaltenorientiertes OLAP-System
- [[data-lake-lakehouse]] - NoSQL im Kontext der Datenplattform
