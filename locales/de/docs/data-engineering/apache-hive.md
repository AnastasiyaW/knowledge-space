---
title: "Apache Hive"
category: tools
tags: [data-engineering, hive, sql-on-hadoop, metastore, data-warehouse]
level: 3
source_sha256: 132758362f0bc89d6ee8bc135eb1ac7d6d553d4b8f2eb54342a17d07c370035c
translation: machine
translated_at: '2026-10-24'
---
# Apache Hive {#apache-hive}

Hive ist ein SQL-on-Hadoop-Data-Warehouse-System. Es übersetzt SQL-Abfragen in MapReduce/Tez/Spark-Jobs. Keine Datenbank – es ist eine Abfrageübersetzungsschicht über HDFS-Daten.

## Architektur {#architecture}

```php
Hive Client (CLI/JDBC/Thrift)
       |
   Hive Driver -> Compiler (uses Metastore) -> Executor -> HDFS
```

- **Metastore:** Tabellenschemata, Spaltentypen, Partitionsinformationen, SerDe-Konfiguration. Gespeichert in einer RDBMS (MySQL/PostgreSQL)
- **Compiler:** übersetzt HiveQL anhand der Metadaten in einen MapReduce/Tez-DAG
- **Driver:** nimmt SQL entgegen und steuert Kompilierung und Ausführung

## Tabellentypen {#table-types}

| Typ | Verhalten bei DROP TABLE |
|------|-------------------|
| **Managed** | Löscht Metadaten UND Daten |
| **External** | Löscht nur die Metadaten, Daten bleiben auf HDFS/S3 erhalten |

## JOIN-Strategien {#join-strategies}

### Reduce-Side-Join (Standard) {#reduce-side-join-default}
- Mapper geben Join-Schlüssel und Werte aus beiden Tabellen aus
- Reducer erhalten übereinstimmende Schlüssel und führen den Join durch
- Funktioniert für kleine bis mittelgroße Tabellen. Schlägt bei zwei sehr großen Tabellen fehl (OOM)

### Map-Side-Join (MapJoin) {#map-side-join-mapjoin}
- Kleine Tabelle wird in eine HashMap geladen und über HDFS verteilt
- Jeder Mapper joint mit seinem Split der großen Tabelle
- Für den Join ist keine Reduce-Phase nötig
- Hinweis: `SELECT /*+ MAPJOIN(small_table) */ ...`

### Sort-Merge-Bucket-Join (SMB) {#sort-merge-bucket-join-smb}
- Am effizientesten für zwei große Tabellen
- **Voraussetzungen:**
  1. Beide Tabellen sind nach Join-Schlüssel bucketisiert (`CLUSTERED BY`)
  2. Die Bucket-Anzahlen müssen Vielfache voneinander sein (2:4, 5:10)
  3. Konfiguration: `hive.auto.convert.sortmerge.join=true`
- Der Join erfolgt vollständig in der Map-Phase – kein Shuffle, kein Reduce

## Hive-Besonderheiten {#hive-specifics}
- Verwendet HiveQL (SQL-ähnlich mit Erweiterungen)
- Transaktionen: nur im ORC-Format, Delta-Dateien werden beim Lesen angewendet, Compaction führt sie zusammen
- Kein BEGIN/COMMIT/ROLLBACK – Auto-Commit pro Statement
- Virtuelle Spalten: `INPUT__FILE__NAME`, `BLOCK__OFFSET__INSIDE__FILE`

## Stolperfallen {#gotchas}
- SMB-Join: Werden Daten eingefügt, ohne dass Bucketing erzwungen wird, entstehen stille Fehlergebnisse (schlimmer als Fehler). Immer `hive.enforce.bucketing=true` setzen
- Komplexe Abfragen (JOIN + GROUP BY) erzeugen mehrere verkettete MapReduce-Jobs
- Hive wird für interaktive Abfragen zunehmend durch Spark SQL und Trino/Presto ersetzt
- Der Metastore wird weiterhin weit verbreitet als Schema-Katalog genutzt (auch ohne Hive-Abfragen)

## Siehe auch {#see-also}
- [[hadoop-hdfs]] - zugrunde liegender Speicher
- [[mapreduce]] - Ausführungsengine
- [[apache-spark-core]] - moderne Alternative
- [[file-formats]] - ORC-Format für Hive
