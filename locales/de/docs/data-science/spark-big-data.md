---
title: "Apache Spark und Big-Data-Verarbeitung"
category: tools
tags: [data-science, spark, big-data, distributed, optimization]
level: 3
source_sha256: 14ee00167466f417300b7f7745468378dcccdea024a24b9cda9c1dfaeb792536
translation: machine
translated_at: '2026-10-24'
---
# Apache Spark und Big-Data-Verarbeitung {#apache-spark-and-big-data-processing}

Wenn Daten den Speicher eines einzelnen Rechners übersteigen, verteilt Spark die Berechnung auf Cluster. Das Verständnis des Ausführungsmodells von Spark ist für die Performance entscheidend.

## Architektur {#architecture}

- **SparkContext**: Einstiegspunkt für die Funktionalität
- **Driver**: steuert die Ausführung
- **Worker Node -> Executor -> Task**: Ausführungshierarchie
- **Partition**: Einheit der Datenparallelität
- **Job -> Stage -> Task**: Berechnungshierarchie

## Zentrale Optimierungsregeln {#core-optimization-rules}

- **2–3 Tasks pro CPU-Kern** für optimale Parallelität
- **~128 MB pro Partition** empfohlen
- Datenverzerrung (Data Skew) über die Spark UI überwachen
- Filter so früh wie möglich anwenden (Predicate Pushdown)
- Python-UDFs vermeiden (unterbrechen den Catalyst-Optimizer) – stattdessen integrierte Funktionen verwenden

## Shuffle {#shuffle}

Neuverteilung von Daten über Knoten hinweg. **Die mit Abstand teuerste Operation.**

Auslöser: `groupBy`, `join`, `distinct`, `repartition`, `orderBy`

Shuffle minimieren:
- Vor dem Join filtern
- Kleine Tabellen broadcasten
- `coalesce` (ohne Shuffle) statt `repartition` verwenden, wenn die Anzahl der Partitionen reduziert wird

## Zentrale Techniken {#key-techniques}

### Broadcast Join {#broadcast-join}
Kleine Tabelle an alle Executor senden, Shuffle vermeiden.
```python
from pyspark.sql.functions import broadcast
result = big_df.join(broadcast(small_df), 'key')
```

Verwenden, wenn eine Seite klein ist (< 10 MB Standard, konfigurierbar).

### Caching {#caching}
```python
df.cache()     # in memory
df.persist()   # configurable storage level
df.unpersist() # free memory
```

DataFrames cachen, die mehrfach wiederverwendet werden. Nicht alles cachen – der Speicher ist begrenzt.

### Repartition vs. Coalesce {#repartition-vs-coalesce}
```python
df.repartition(100)     # full shuffle, any number of partitions
df.repartition('key')   # partition by column (useful before groupBy)
df.coalesce(10)         # reduce partitions without shuffle
```

## Data Skew {#data-skew}

**Problem**: eine Partition ist deutlich größer als die anderen -> ein Task benötigt unverhältnismäßig lange.

**Erkennung**: Die Spark UI zeigt die Task-Dauern. Ist das Maximum >> Median, liegt Skew vor.

**Lösungen**:
- **Salting**: einen zufälligen Präfix zum verzerrten Schlüssel hinzufügen und mit der explodierten Dimensionstabelle joinen
- **Broadcast Join**: für die verzerrte Seite, wenn sie klein genug ist
- **Repartitionierung nach einem anderen Schlüssel**: Daten neu verteilen

## Small-File-Problem {#small-file-problem}

Zu viele kleine Dateien = zu viele Tasks = Overhead beim Scheduling.

**Lösung**: Dateien vor dem Schreiben per `coalesce()` oder Repartitionierung zusammenführen.

```python
df.coalesce(10).write.parquet('output/')
```

## Executor-Dimensionierung {#executor-sizing}

- **Speicher**: zu klein = Auslagerung auf die Festplatte (langsam), zu groß = GC-Pausen
- **Kerne**: 5 Kerne pro Executor sind ein guter Standardwert
- Abwägung: mehr Executor mit moderaten Ressourcen vs. weniger mit mehr Ressourcen

## Stolpersteine {#gotchas}
- Spark arbeitet lazy – Transformationen werden erst bei einer Aktion (collect, count, write) ausgeführt
- `collect()` bringt alle Daten zum Driver – bei großen Datenmengen OOM. Stattdessen `take()` oder `show()` verwenden
- Python-UDFs sind aufgrund des Serialisierungsaufwands 10–100× langsamer als integrierte Spark-Funktionen
- Joins auf verzerrten Schlüsseln können ohne Eingriff endlos laufen
- Nach dem Einlesen immer die Anzahl der Partitionen prüfen: `df.rdd.getNumPartitions()`

## Siehe auch {#see-also}
- [[sql-for-data-science]] - Spark SQL verwendet dieselben Konzepte
- [[pandas-eda]] - Die DataFrame-API von Spark ist von pandas inspiriert
- [[ds-workflow]] - Spark in der Datenpipeline
