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
