---
title: "Spark-Performance-Optimierung"
category: reference
tags: [data-engineering, spark, optimization, partitioning, skew, broadcast]
level: 4
source_sha256: dd810ed7957280bd35cd7b5f7a2e5b969744b853ce5dfa5e274ccbef55c97db0
translation: machine
translated_at: '2026-10-24'
---
# Spark-Performance-Optimierung {#spark-performance-optimization}

Die Optimierung von Spark dreht sich um die Minimierung von Shuffles, die Verwaltung von Partitionen und die effektive Nutzung des Catalyst-Optimizers.

## Partitionsverwaltung {#partition-management}

**Standard-Shuffle-Partitionen:** 200. Konfiguration:

```python
spark.conf.set("spark.sql.shuffle.partitions", 400)
spark.conf.set("spark.default.parallelism", 400)
```

**Optimale Partitionsanzahl:**
```text
num_executors * executor_cores * (2 to 4)
```

**Zielgröße pro Partition:** ~128 MB (Bereich: 64–256 MB).

### Repartition vs. Coalesce {#repartition-vs-coalesce}

```python
df = df.repartition(1000)                    # by count (triggers full shuffle)
df = df.repartition("col1", "col2")          # by columns
df = df.coalesce(10)                         # reduce without full shuffle
```

**Regel:** `coalesce` zum Verkleinern, `repartition` zum Vergrößern.

## Problem kleiner Dateien {#small-file-problem}

Viele kleine Dateien (< 128 MB HDFS-Block) verursachen: NameNode-Overhead, langsames Lesen und zu viele kleine Tasks.

**Lösungen:**
- `repartition(N)` – erzeugt N gleich große Dateien (Shuffle)
- `coalesce(N)` – reduziert Partitionen ohne vollständigen Shuffle (ggf. ungleich groß)

## Data Skew {#data-skew}

Wenn einige Partitionen deutlich mehr Daten enthalten als andere – überlastete Executors, ungenutzte Ressourcen, mögliches OOM.

### Lösung 1: Broadcast Hash Join {#solution-1-broadcast-hash-join}

Für den Join einer großen Tabelle mit einer kleinen Tabelle (die kleine Tabelle muss in den Executor-Speicher passen):

```python
spark.table("big").join(spark.table("small").hint("broadcast"), "key")
# Auto-broadcast threshold:
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 104857600)  # 100MB
```

### Lösung 2: Key Salting {#solution-2-key-salting}

Ein zufälliges Suffix zu den betroffenen Schlüsseln hinzufügen, um die Daten gleichmäßig zu verteilen:

```python
df_big = df_big.withColumn('city', F.concat(
    F.col('city'), F.lit('_'),
    F.floor(F.rand(seed=17) * 5 + 1).cast('string')
))
# Explode corresponding keys in smaller table to match
```

### Lösung 3: Adaptive Query Execution (AQE) {#solution-3-adaptive-query-execution-aqe}

Seit Spark 3.0 automatisch aktiv:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# Skew threshold: partition > 5x median AND > 256MB
```

## Weitere Optimierungstechniken {#other-optimization-techniques}

| Technik | Details |
|-----------|---------|
| **Frühes Filtern** | Vor Shuffles filtern, um das Datenvolumen zu reduzieren |
| **UDFs vermeiden** | UDFs umgehen Catalyst und verursachen Python-JVM-Serialisierung. Native Funktionen verwenden |
| **Caching** | `df.cache()` oder `df.persist(StorageLevel.MEMORY_AND_DISK)` für wiederverwendete DataFrames |
| **Spaltenorientierte Formate** | Parquet/ORC unterstützen Predicate Pushdown und Column Pruning |
| **Executor-Dimensionierung** | 3–5 Cores pro Executor; 1 Core für das Betriebssystem freilassen; 2–3 Tasks pro CPU-Core |

## Stolperfallen {#gotchas}
- `repartition` löst immer einen vollständigen Shuffle aus; `coalesce` tut dies nicht, kann aber ungleichmäßige Partitionen erzeugen
- Broadcast Join: Die kleinere Tabelle muss sowohl in den Driver- als auch in den Executor-Speicher passen
- Die Standardeinstellung von 200 Shuffle-Partitionen kann für große Datenmengen zu wenig oder für kleine Datenmengen zu viel sein
- Caching ist nicht immer vorteilhaft – vor dem Einsatz testen; sichtbar im Storage-Tab der Spark UI
- AQE in Spark 3.0+ behandelt viele Skew-Fälle automatisch

## Siehe auch {#see-also}
- [[apache-spark-core]] – Architekturgrundlagen
- [[pyspark-dataframe-api]] – DataFrame-Operationen
- [[file-formats]] – Vorteile von Parquet/ORC
