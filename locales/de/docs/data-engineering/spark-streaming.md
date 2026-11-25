---
title: "Spark Streaming"
category: tools
tags: [data-engineering, spark, streaming, structured-streaming, micro-batch]
level: 3
source_sha256: 397fb165c8d3dea0209b0a3fa73dfbf36776cbbd2784ac656347fd1e971a9e82
translation: machine
translated_at: '2026-10-24'
---
# Spark Streaming {#spark-streaming}

Spark Streaming verarbeitet Echtzeitdaten per Micro-Batching: Der eingehende Stream wird in kleine Batch-Jobs aufgeteilt, die von Spark Core verarbeitet werden. Structured Streaming (empfohlen) behandelt den Stream als unbegrenzten DataFrame.

## Zwei Ansätze {#two-approaches}

| | Classic DStreams | Structured Streaming |
|---|---|---|
| Abstraktion | Stream als Micro-Batch-RDDs | Stream als unendlicher DataFrame |
| Seiteneffekte | Erlaubt | Nur Eingabe -> Transformation -> Ausgabe |
| API | Niedrigere Ebene | Gleiche DataFrame-API wie bei Batch |
| Status | Veraltet | **Empfohlen** |

## Muster für Structured Streaming {#structured-streaming-pattern}

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("streaming").getOrCreate()

# Source (Kafka)
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:9092") \
    .option("subscribe", "topic_name") \
    .load()

# Process
result = df.selectExpr("CAST(value AS STRING)")

# Sink
query = result.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
```

## DStreams-API (veraltet) {#dstreams-api-legacy}

```python
from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, batchDuration=1)  # 1-second ticks
# Define source, transformations
ssc.start()
ssc.awaitTermination()
```

## Zustellungsgarantien {#delivery-guarantees}

| Garantie | Bedeutung | Abwägung |
|-----------|---------|-----------|
| **At-most-once** | Nachrichten können verloren gehen, werden aber nie dupliziert | Am schnellsten |
| **At-least-once** | Nachrichten gehen nie verloren, können aber dupliziert werden | Erfordert Deduplizierung |
| **Exactly-once** | Nachrichten werden genau einmal zugestellt | Am komplexesten, transaktionale Unterstützung erforderlich |

## Typische Pipeline {#typical-pipeline}

```php
Kafka -> Spark Structured Streaming -> Database/DWH
```

## Wichtige Fakten {#key-facts}
- Structured Streaming erlaubt keine terminalen Aktionen (count, collect) mitten in der Pipeline
- Fensterfunktionen wirken über zeitbasierte Fenster
- Streaming-Daten lassen sich per Joins mit statischen (gecachten) Daten kombinieren
- Trigger: zeitbasiert, nach Ereignisanzahl oder kontinuierlich

## Stolperfallen {#gotchas}
- Spark Streaming ist KEIN echtes Streaming, sondern Micro-Batching
- Entwicklung und Debugging sind schwieriger als bei Batch; für Prototyping Jupyter verwenden
- Ausgabemodi von Structured Streaming: `append`, `complete`, `update`
- Zustandsverwaltung erhöht die Komplexität bei Aggregationen über Zeitfenster

## Siehe auch {#see-also}
- [[apache-kafka]] - Message-Broker
- [[apache-spark-core]] - Spark-Architektur
- [[etl-elt-pipelines]] - Batch- vs. Stream-Verarbeitung
