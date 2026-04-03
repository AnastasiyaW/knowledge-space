---
title: Messaging Models
category: concepts
tags: [kafka, messaging, queue, pub-sub, log, architecture]
---

# Messaging Models

Three fundamental messaging models exist in distributed systems; Kafka uses the log-based model which subsumes both queue and pub-sub patterns.

## Key Facts

- **Queue Model (Competing Consumers)**: messages go to a queue, exactly one consumer receives each message; consumed messages are removed; used for task distribution and load balancing
- **Pub-Sub Model (Fan-Out)**: messages published to a topic, every subscriber receives a copy; used for event notification where multiple systems need the same data
- **Log-Based Model (Kafka)**: messages appended to an immutable, ordered log; consumers maintain their own offset (position); messages retained by time/size policy, not by consumption
- Log-based model enables: multiple independent [[consumer-groups]] reading at their own pace, replay capability by resetting offset, no message loss on consumer failure
- Traditional queues (RabbitMQ, ActiveMQ, SQS) focus on message delivery and task distribution; log-based streaming (Kafka, Pulsar, Redpanda) focuses on event storage and stream processing
- Kafka is NOT a message broker - it is a distributed commit log (write-ahead log)
- Key difference from traditional queues: reading a topic 10 times requires 10 consumer groups (10 x 8 bytes per partition overhead), not 10 copies of data

## Patterns

| Property | Traditional Queue | Log-Based Streaming |
|----------|------------------|---------------------|
| Message lifecycle | Deleted after consumption | Retained by policy |
| Ordering | Per-queue (or none) | Per-partition guaranteed |
| Replay | Not possible | Possible (reset offset) |
| Consumer groups | Competing consumers | Independent consumer groups |
| Throughput | Moderate | Very high (sequential I/O) |
| Use case | Task distribution | Event sourcing, analytics, CDC |

### Communication Patterns

| Pattern | Notation | Description |
|---------|----------|-------------|
| Put/Take | 1 -> 1 | One-to-one, single consumer |
| Publish/Subscribe | 1 -> * | One-to-many, all subscribers receive |
| Request/Response | 1 <-> 1 | Synchronous, bidirectional |

### Protocols

AMQP, MQTT, STOMP, NATS, ZeroMQ, Kafka's custom binary protocol.

## Gotchas

- **"Kafka is just another message broker"** is false - Kafka's log-based architecture is fundamentally different from traditional queue-based brokers; it always persists messages regardless of consumption
- **Queue model cannot replay** - once a message is consumed and acknowledged, it is gone; this is a fundamental architectural difference, not a configuration option
- **Pub-sub without retention** means consumer must be online when the message is published; Kafka solves this by retaining messages for a configurable period

## See Also

- [[delivery-semantics]] - at-most-once, at-least-once, exactly-once guarantees
- [[consumer-groups]] - how Kafka implements both queue and pub-sub patterns via consumer groups
- [[broker-architecture]] - how Kafka stores and serves messages
- [Apache Kafka Design: Motivation](https://kafka.apache.org/documentation/#design_motivation)
