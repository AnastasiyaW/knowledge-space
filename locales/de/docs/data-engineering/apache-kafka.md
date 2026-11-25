---
title: "Apache Kafka"
category: tools
tags: [data-engineering, kafka, streaming, pubsub, message-broker, event-driven]
level: 2
source_sha256: bcc94e3cd20e0442924f9913b79e78331a80163e59682fe63253fd1944de219b
translation: machine
translated_at: '2026-10-24'
---
# Apache Kafka {#apache-kafka}

Apache Kafka ist eine verteilte Event-Streaming-Plattform. Sie entkoppelt Producer von Consumern über einen persistenten Message Broker und ermöglicht dadurch datenbasierte Pipelines mit hohem Durchsatz und Fehlertoleranz sowie Echtzeitanalysen.

## Warum PubSub {#why-pubsub}

Direkte Client-zu-Client-Kommunikation scheitert, wenn:
- ein Consumer offline ist (der Producer hat keinen Ort, an den er senden kann)
- mehrere Consumer dieselben Events benötigen
- der Producer alle Consumer im Voraus kennen muss

**Lösung:** Publisher senden an den Broker, Subscriber lesen vom Broker.

**Alternativen:** RabbitMQ, Apache Pulsar, AWS Kinesis, GCP Pub/Sub

## Architektur {#architecture}

| Komponente | Rolle |
|-----------|------|
| **Broker** | Server, die Nachrichten speichern |
| **Producer** | Senden Nachrichten an Topics |
| **Consumer** | Lesen Nachrichten aus Topics |
| **Topics** | Logische Trennung von Nachrichtentypen |
| **Partitionen** | Topics werden in geordnete Partitionen aufgeteilt; jede Nachricht erhält einen Offset |
| **Consumer Groups** | Mehrere Consumer teilen sich die Last auf einem Topic |

## Wichtige Eigenschaften {#key-properties}
- Hoher Durchsatz, horizontal skalierbar
- Persistente Speicherung (konfigurierbare Aufbewahrung: Tage bis Monate)
- Nachrichten sind innerhalb einer Partition geordnet (nicht über Partitionen hinweg)
- Consumer Groups ermöglichen parallele Verarbeitung

## Anwendungsfälle {#use-cases}
- Nachrichtenaustausch zwischen Services
- Echtzeit-Monitoring und -Analysen
- Log-Aggregation
- Erfassung von Metriken
- Event Sourcing

## Wofür Kafka NICHT geeignet ist {#what-kafka-is-not-for}
- Langzeitspeicherung (dafür ein geeignetes DWH verwenden)
- Erstellung von Trainingsdatensätzen (Daten zuerst in einen Speicher verschieben)
- Komplexe Transformationen (stattdessen Spark/Flink nachgelagert verwenden)

## Tooling {#tooling}
- **Kafka Tool / Offset Explorer** - GUI zum Durchsuchen von Brokern, Topics, Partitionen
- **Confluent Platform** - verwaltetes Kafka mit zusätzlichen Tools (Schema Registry, ksqlDB)
- **KafkaStreams** - schlanke Bibliothek für Stream-Verarbeitung

## Integration mit Spark {#integration-with-spark}

```python
# Spark Structured Streaming from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:9092") \
    .option("subscribe", "topic_name") \
    .load()
```

## Stolperfallen {#gotchas}
- Nachrichten sind nur innerhalb einer Partition geordnet - nicht über Partitionen hinweg
- Consumer-Lag muss überwacht werden (Consumer fallen hinter die Producer zurück)
- Die Anzahl der Partitionen kann nach der Erstellung nicht verringert werden
- Die Aufbewahrung ist zeitbasiert oder größenbasiert - Daten verschwinden nach Ablauf der Aufbewahrungsfrist

## Siehe auch {#see-also}
- [[spark-streaming]] - Engine für Stream-Verarbeitung
- [[etl-elt-pipelines]] - Pipeline-Muster
- [[data-lineage-metadata]] - Überwachung des Consumer-Lags
