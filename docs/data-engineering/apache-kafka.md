---
title: Apache Kafka
category: tools
tags: [data-engineering, kafka, streaming, pubsub, message-broker, event-driven]
---

# Apache Kafka

Apache Kafka is a distributed event streaming platform. It decouples producers from consumers via a persistent message broker, enabling high-throughput, fault-tolerant data pipelines and real-time analytics.

## Why PubSub

Direct client-to-client communication fails when:
- Consumer goes offline (producer has nowhere to send)
- Multiple consumers need the same events
- Producer must know all consumers in advance

**Solution:** Publishers send to broker, subscribers read from broker.

**Alternatives:** RabbitMQ, Apache Pulsar, AWS Kinesis, GCP Pub/Sub

## Architecture

| Component | Role |
|-----------|------|
| **Brokers** | Servers storing messages |
| **Producers** | Send messages to topics |
| **Consumers** | Read messages from topics |
| **Topics** | Logical separation of message types |
| **Partitions** | Topics split into ordered partitions; each message gets an offset |
| **Consumer groups** | Multiple consumers sharing load on a topic |

## Key Properties
- High throughput, horizontally scalable
- Persistent storage (configurable retention: days to months)
- Messages are ordered within a partition (not across partitions)
- Consumer groups enable parallel consumption

## Use Cases
- Messaging between services
- Real-time monitoring and analytics
- Log aggregation
- Metric collection
- Event sourcing

## What Kafka is NOT For
- Long-term storage (use a proper DWH)
- Building training datasets (move data to storage first)
- Complex transformations (use Spark/Flink downstream)

## Tooling
- **Kafka Tool / Offset Explorer** - GUI to browse brokers, topics, partitions
- **Confluent Platform** - managed Kafka with additional tools (Schema Registry, ksqlDB)
- **KafkaStreams** - lightweight stream processing library

## Integration with Spark

```python
# Spark Structured Streaming from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:9092") \
    .option("subscribe", "topic_name") \
    .load()
```

## Gotchas
- Messages are ordered within a partition only - not across partitions
- Consumer lag must be monitored (consumers falling behind producers)
- Partition count cannot be decreased after creation
- Retention is time-based or size-based - data disappears after retention period

## See Also
- [[spark-streaming]] - stream processing engine
- [[etl-elt-pipelines]] - pipeline patterns
- [[data-lineage-metadata]] - monitoring consumer lag
