---
title: Kafka & Message Queues
type: MOC
---

# Kafka & Message Queues

## Core Concepts
- [[broker-architecture]] - Broker cluster, controller election (ZooKeeper/KRaft), log segments, retention
- [[topics-and-partitions]] - Topics, partitions, ordering, key-based routing, cleanup policies
- [[consumer-groups]] - Group protocol, partition assignment, offset management, rebalancing
- [[replication-and-fault-tolerance]] - ISR, HW/LEO, acks + min.insync.replicas, multi-DC patterns

## Stream Processing
- [[kafka-streams]] - KStream/KTable, stateful ops, windowing, joins, exactly-once, interactive queries
- [[ksqldb]] - SQL over streams, push/pull queries, windowed aggregations, persistent queries

## Integration
- [[kafka-connect]] - Source/sink connectors, SMTs, REST API, DLQ, error handling
- [[schema-registry]] - Schema evolution, compatibility modes, Avro/Protobuf/JSON Schema, subject strategies

## Patterns & Best Practices
- [[producer-patterns]] - Acks modes, batching, compression, retries, idempotent producer, backpressure
- [[kafka-transactions]] - Idempotent producer, transactional API, exactly-once semantics, zombie fencing

## Operations & Security
- [[kafka-cluster-operations]] - Sizing, rolling upgrades, monitoring, tuning, MirrorMaker 2, DR
- [[kafka-security]] - SSL/TLS, SASL, ACLs, listeners, RBAC, audit logging
