---
title: "Apache Spark Core-Architektur"
category: tools
tags: [data-engineering, spark, distributed-computing, pyspark, architecture]
level: 3
source_sha256: 7952ae4e9797fd4455229889842cc37107005f3b7e6b108ad5d01ab56e158ec0
translation: machine
translated_at: '2026-10-24'
---
# Apache Spark Core-Architektur {#apache-spark-core-architecture}

Apache Spark ist ein quelloffenes Framework zur verteilten Datenverarbeitung. Wichtige Vorteile gegenüber MapReduce: In-Memory-Berechnung, einheitliche API für Batch, Streaming, ML und Graph sowie Unterstützung für Python, Scala, Java und R.

## Cluster-Komponenten {#cluster-components}

| Komponente | Rolle |
|-----------|------|
| **Cluster Manager** | Verteilt Ressourcen. Optionen: Standalone, YARN, Kubernetes, Mesos |
| **Driver** | Master-Prozess – wandelt die Anwendung in Tasks um, plant diese und verfolgt den Fortschritt |
| **SparkContext / SparkSession** | Einstiegspunkt für die Interaktion mit dem Cluster |
| **Worker Node** | Server bzw. VM, auf dem Executor-Prozesse laufen |
| **Executor** | Prozess auf dem Worker, der Tasks ausführt |
| **Task** | Kleinste Arbeitseinheit – eine Operation auf einer Partition |
| **Partition** | Kleinste logische Dateneinheit. Standardmäßige Shuffle-Partitionen: 200 |

## Deploy-Modi {#deploy-modes}

- **Client-Modus:** Driver auf der absendenden Maschine; wird der Client beendet, werden alle Executors beendet
- **Cluster-Modus:** Driver und Executors laufen beide im Cluster; der Client dient nur zum Absenden
- **Lokaler Modus:** Alles innerhalb einer JVM. `--master local[*]` nutzt alle Kerne. Für Entwicklung und Tests

## Ausführungshierarchie {#execution-hierarchy}

```php
Application -> Job(s) -> Stage(s) -> Task(s)
```

- **Job:** wird durch einen Action-Aufruf erzeugt
- **Stage:** Menge von Tasks ohne Shuffle-Grenze
- **Task:** eine Operation auf einer Partition
- **Shuffle:** Neuverteilung von Daten zwischen Knoten. Wird ausgelöst durch `join`, `groupBy`, `distinct`, `repartition`

## Spark-Stack {#spark-stack}

| Modul | Zweck |
|--------|---------|
| **Spark Core** | Task-Scheduling, Speicherverwaltung, Fehlertoleranz |
| **Spark SQL + DataFrames** | Strukturierte Daten über SQL oder die DataFrame-API |
| **Spark Streaming** | Echtzeitverarbeitung im Micro-Batch-Verfahren |
| **MLlib** | Verteiltes maschinelles Lernen |
| **GraphX** | Graphverarbeitung |

## Datenstrukturen {#data-structures}

### RDD (Resilient Distributed Dataset) {#rdd-resilient-distributed-dataset}
API auf niedrigster Ebene. Unveränderlich, mit Lazy Evaluation und Fehlertoleranz über den DAG-Lineage. Einsatz für unstrukturierte Daten oder Mediendateien.

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])
```

### DataFrame {#dataframe}
Verteilte Sammlung von Spalten mit Namen. Primäres Objekt in PySpark. Catalyst-Optimizer für die Abfrageplanung.

### Dataset {#dataset}
Typisierter DataFrame (nur Scala/Java). In Python nicht verfügbar.

## Lazy Evaluation {#lazy-evaluation}

Spark erstellt einen logischen Plan, der vom **Catalyst Optimizer** optimiert wird (Predicate Pushdown, Constant Folding, Neuordnung von Filtern). Die Ausführung beginnt erst, wenn eine Action aufgerufen wird.

**Transformationen (lazy):**
- **Narrow** (kein Shuffle): `map`, `filter`, `select`, `withColumn`
- **Wide** (löst Shuffle aus): `join`, `groupBy`, `distinct`, `repartition`, `orderBy`

**Actions (lösen Ausführung aus):**
```python
df.show()              # display rows
df.count()             # count rows
df.collect()           # all to driver (OOM risk!)
df.toPandas()          # convert to Pandas (all to driver)
df.write.parquet(path) # write to file
```

## Catalyst-Optimizer-Pipeline {#catalyst-optimizer-pipeline}

1. **Logische Planung:** Parsen -> Analysieren -> Optimieren (Predicate Pushdown, Constant Folding)
2. **Physische Planung:** Erzeugung mehrerer Pläne -> kostenbasierte Auswahl
3. **Tungsten:** Whole-Stage Code Generation für effiziente CPU-Nutzung

## spark-submit {#spark-submit}

```bash
spark-submit \
  --master spark://master:7077 \
  --deploy-mode cluster \
  --executor-memory 4g \
  --executor-cores 4 \
  --num-executors 10 \
  app.py [args]
```

## PySpark vs. Pandas {#pyspark-vs-pandas}

| Merkmal | PySpark | Pandas |
|---------|---------|--------|
| Ausführung | Verteilt | Einzelmaschine |
| Auswertung | Lazy | Eager |
| Veränderlichkeit | Unveränderlich | Veränderlich |
| Skalierung | TB+ | Begrenzt durch RAM |

## Stolperfallen {#gotchas}
- `collect()` und `toPandas()` holen alle Daten in den Driver – OOM-Risiko bei großen Datensätzen
- UDFs umgehen den Catalyst-Optimizer und verursachen Serialisierungs-Overhead zwischen Python und JVM
- `inferSchema=True` liest die gesamte CSV-Datei, um die Datentypen zu bestimmen – langsam bei großen Dateien
- Die Structured-API von Spark Streaming erlaubt keine terminalen Actions innerhalb der Pipeline
- Spark on Kubernetes ist seit Spark 3.1 (März 2021) produktionsreif

## Siehe auch {#see-also}
- [[pyspark-dataframe-api]] – Referenz für DataFrame-Operationen
- [[spark-optimization]] – Performance-Tuning
- [[spark-streaming]] – Echtzeitverarbeitung
- [[etl-elt-pipelines]] – Spark als ETL-Engine
