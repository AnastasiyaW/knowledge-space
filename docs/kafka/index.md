---
title: Kafka & Message Queues
type: MOC
---

# Kafka & Message Queues

## Core Concepts
- [[broker-architecture]] - Broker cluster, controller election (ZooKeeper/KRaft), log segments, retention
- [[topics-and-partitions]] - Topics, partitions, ordering, key-based routing, cleanup policies
- [[consumer-groups]] - Group protocol, partition assignment, offset management, rebalancing
- [[kafka-replication-fundamentals]] - ISR, HW/LEO, acks + min.insync.replicas
- [[kafka-fault-tolerance]] - Unclean leader election, rack-aware replication, multi-DC patterns

## Stream Processing
- [[kafka-streams]] - KStream/KTable, stateful ops, windowing, joins, exactly-once, interactive queries
- [[ksqldb]] - SQL over streams, push/pull queries, windowed aggregations, persistent queries

## Integration
- [[kafka-connect]] - Source/sink connectors, SMTs, REST API, DLQ, error handling
- [[schema-registry]] - Schema evolution, compatibility modes, Avro/Protobuf/JSON Schema, subject strategies

## Patterns & Best Practices
- [[kafka-producer-fundamentals]] - Acks modes, batching, compression, retries, send patterns
- [[kafka-producer-advanced-patterns]] - Custom partitioners, headers, interceptors, backpressure, idempotent producer
- [[kafka-transactions]] - Idempotent producer, transactional API, exactly-once semantics, zombie fencing

## Operations & Security
- [[kafka-cluster-management]] - Sizing, rolling upgrades, disk failure, partition reassignment
- [[kafka-monitoring-and-tuning]] - JMX metrics, Prometheus/Grafana, OS/JVM/broker tuning
- [[kafka-backup-and-dr]] - MirrorMaker 2, backup strategies, disaster recovery patterns
- [[kafka-security]] - SSL/TLS, SASL, ACLs, listeners, RBAC, audit logging

## Additional References

- [[admin-api]] - The Admin API (kafka-clients library) provides programmatic cluster management for topics, consumer
- [[alpakka-kafka]] - Alpakka Kafka connects Kafka topics to Akka Streams pipelines, providing reactive backpressure
- [[confluent-rest-proxy]] - The Confluent REST Proxy provides an HTTP-based interface to Kafka (default port 8082), enabling
- [[consumer-configuration]] - Complete reference for Kafka consumer configuration parameters with defaults, tuning guidelines
- [[cqrs-pattern]] - CQRS (Command Query Responsibility Segregation) separates the write path (Command API with event
- [[delivery-semantics]] - Kafka supports three delivery semantics - at-most-once, at-least-once, and exactly-once - each with
- [[docker-development-setup]] - Minimal Docker Compose configurations for local Kafka development using KRaft mode (no ZooKeeper)
- [[event-sourcing]] - Event sourcing stores every state change as an immutable event in Kafka rather than overwriting
- [[idempotent-producer]] - The idempotent producer assigns a PID (Producer ID) and sequence numbers to each message, allowing
- [[kafka-messaging-fundamentals]] - Kafka delivery guarantees, consumer group mechanics, rebalancing strategies, and integration
- [[kafka-monitoring]] - Kafka exposes metrics via JMX
- [[kafka-queues-v4]] - Kafka 4.0 introduces work queue semantics where each message is processed by only one consumer in a
- [[kafka-streams-state-stores]] - State stores provide local key-value storage per Kafka Streams task, backed by RocksDB on disk and
- [[kafka-streams-time-semantics]] - Stream processing time semantics based on the Google Dataflow model define how events are grouped
- [[kafka-streams-windowing]] - Windowed operations group stream records into finite time intervals for aggregation, supporting
- [[kafka-troubleshooting]] - Common Kafka problems mapped to symptoms, root causes, and fixes for both producer-side and
- [[messaging-models]] - Three fundamental messaging models exist in distributed systems
- [[mirrormaker]] - MirrorMaker 2 (MM2) replicates topics between Kafka clusters for disaster recovery and
- [[nats-comparison]] - NATS is a lightweight messaging system with three layers (Core, JetStream, Clustering), offering
- [[offsets-and-commits]] - An offset is a sequential message number within a partition, assigned on write
- [[partitioning-strategies]] - Kafka partitioning determines how messages are distributed across partitions using key hashing
- [[rebalancing-deep-dive]] - Rebalancing is the process of redistributing partition assignments among consumers in a group
- [[saga-pattern]] - The Saga pattern manages distributed transactions across microservices via Kafka using either
- [[spring-kafka]] - Spring Kafka provides declarative, annotation-based Kafka integration with KafkaTemplate for
- [[transactional-outbox]] - The Transactional Outbox pattern writes events to an outbox table within the same database
- [[zero-copy-and-disk-io]] - Kafka achieves high throughput through sequential disk I/O, OS page cache utilization, and
- [[zio-kafka]] - ZIO Kafka provides purely functional Kafka integration using ZIO Streams, wrapping the standard
