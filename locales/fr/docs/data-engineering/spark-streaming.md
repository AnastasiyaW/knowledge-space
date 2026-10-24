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

Spark Streaming traite des données en temps réel par micro-lots : le flux entrant est découpé en petits jobs batch exécutés par Spark Core. Structured Streaming (recommandé) traite le flux comme un DataFrame non borné.

## Deux approches {#two-approaches}

| | DStreams classiques | Structured Streaming |
|---|---|---|
| Abstraction | Flux sous forme de RDD en micro-lots | Flux sous forme de DataFrame infini |
| Effets de bord | Autorisés | Entrée -> transformation -> sortie uniquement |
| API | Plus bas niveau | Même API DataFrame que le batch |
| Statut | Legacy | **Recommandé** |

## Pattern Structured Streaming {#structured-streaming-pattern}

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

## API DStreams (Legacy) {#dstreams-api-legacy}

```python
from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, batchDuration=1)  # 1-second ticks
# Define source, transformations
ssc.start()
ssc.awaitTermination()
```

## Garanties de livraison {#delivery-guarantees}

| Garantie | Signification | Compromis |
|-----------|---------|-----------|
| **At-most-once** | Des messages peuvent être perdus, jamais dupliqués | Le plus rapide |
| **At-least-once** | Des messages ne sont jamais perdus, mais peuvent être dupliqués | Nécessite une déduplication |
| **Exactly-once** | Des messages sont délivrés exactement une fois | Le plus complexe, nécessite un support transactionnel |

## Pipeline type {#typical-pipeline}

```php
Kafka -> Spark Structured Streaming -> Database/DWH
```

## Points clés {#key-facts}
- Structured Streaming n'autorise pas les actions terminales (count, collect) au milieu du pipeline
- Les fonctions de fenêtrage s'appliquent sur des fenêtres temporelles
- Il est possible de combiner des données en streaming avec des données statiques (mises en cache) via des jointures
- Déclencheurs (triggers) : basés sur le temps, sur le nombre d'événements, ou continus

## Pièges courants {#gotchas}
- Spark Streaming n'est PAS un véritable streaming : c'est du micro-batching
- Le développement et le débogage sont plus difficiles qu'en batch : utilisez Jupyter pour le prototypage
- Modes de sortie de Structured Streaming : `append`, `complete`, `update`
- La gestion d'état ajoute de la complexité pour les agrégations sur des fenêtres temporelles

## Voir aussi {#see-also}
- [[apache-kafka]] - courtier de messages
- [[apache-spark-core]] - architecture de Spark
- [[etl-elt-pipelines]] - traitement batch vs streaming
