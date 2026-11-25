---
title: "MapReduce"
category: concepts
tags: [data-engineering, mapreduce, hadoop, distributed-computing, batch]
level: 3
source_sha256: 1e80955c2a197d8e3ccb866d40bdf96000c7d8f9d15cc7be717a14202a0a98be
translation: machine
translated_at: '2026-10-24'
---
# MapReduce {#mapreduce}

MapReduce ist ein Programmiermodell für verteilte Datenverarbeitung. Es gibt zwei benutzerdefinierte Operationen: Map (transformieren/filtern) und Reduce (aggregieren). Das Framework garantiert, dass alle Datensätze mit demselben Schlüssel beim selben Reducer ankommen.

## Paradigma {#paradigm}

```bash
Map:    (K1, V1) -> list(K2, V2)    -- transform each record
Reduce: (K2, list(V2)) -> list(K3, V3)  -- aggregate by key
```

## Ausführungspipeline {#execution-pipeline}

```php
Input -> Split -> Map -> Spill -> Sort/Merge -> Shuffle -> Reduce -> Output
```

1. **Split:** Das InputFormat teilt die Daten in Blöcke auf. Jeder Split -> ein Mapper
2. **Map:** Jeder Mapper verarbeitet seinen Split über einen RecordReader. Ausgabe in einen Ringpuffer
3. **Spill:** Ist der Puffer voll -> Daten werden auf die lokale Festplatte (NICHT HDFS) ausgelagert. Partitioniert nach `hash(key) % numReducers`
4. **Sort/Merge:** Der Mapper sortiert die Spill-Dateien und führt sie per Merge-Sort pro Reducer-Partition zusammen
5. **Shuffle:** Reducer **holen** die Daten von den Mappern (v2 hat die Richtung gegenüber v1 umgekehrt)
6. **Reduce:** Empfangene Dateien per Merge-Sort zusammenführen und den sortierten Key-Value-Strom verarbeiten
7. **Output:** Eine Ausgabedatei pro Reducer auf HDFS

## Hadoop Streaming (Python) {#hadoop-streaming-python}

```bash
hadoop jar $HADOOP_MAPRED_HOME/hadoop-streaming.jar \
  -mapper mapper.py \
  -reducer reducer.py \
  -file /local/path/mapper.py \
  -file /local/path/reducer.py \
  -input /hdfs/input/ \
  -output /hdfs/output/
```

## Wichtige Details {#key-details}
- **Split != HDFS-Block:** Splits sind logisch (können aus einer DB oder aus S3 stammen); Blöcke sind physisch
- **InputFormat-Typen:** TextInputFormat (Standard), NLineInputFormat (N Zeilen pro Mapper), DBInputFormat
- **Anzahl der Mapper:** Wird durch die Split-Logik des InputFormats bestimmt und lässt sich nicht direkt konfigurieren
- **Anzahl der Reducer:** Konfigurierbar über `mapreduce.job.reduces`
- **`_SUCCESS`-Datei:** Leere Markierung, die den Abschluss des Jobs anzeigt. Dateien, die mit `_` oder `.` beginnen, werden von nachfolgenden Jobs ignoriert
- **Das Ausgabeverzeichnis darf VOR dem Start des Jobs NICHT existieren** (Schutz vor Überschreiben)

## MapReduce v1 vs. v2 {#mapreduce-v1-vs-v2}
- **v1:** Mapper haben Daten an die Reducer gepusht -> DDoS auf die Reducer
- **v2:** Reducer holen die Daten von den Mappern (umgekehrte Richtung)

## Fallstricke {#gotchas}
- Der Overhead für die Container-Initialisierung dominiert bei kleinen Datenmengen (40 s für 100 KB mit 31 Mappern gegenüber 9 s mit 3)
- Split ist NICHT dasselbe wie ein HDFS-Block – es handelt sich um verschiedene Abstraktionsebenen
- Hadoop Streaming (Python) fehlen einige Java-MR-Funktionen (keine Setup-/Cleanup-Hooks)
- MapReduce ist veraltet – für neue Workloads sollte Spark bevorzugt werden

## Siehe auch {#see-also}
- [[hadoop-hdfs]] - Speicherschicht
- [[yarn-resource-management]] - Ressourcenzuteilung
- [[apache-hive]] - SQL-Schnittstelle für MapReduce
- [[apache-spark-core]] - moderner Nachfolger
