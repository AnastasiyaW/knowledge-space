---
title: Message Broker Patterns
category: concepts
tags: [messaging, pub-sub, queue, delivery-guarantees, message-broker]
---

# Message Broker Patterns

Message brokers decouple services (dependencies reduced to message format only) and enable asynchronous processing (producer sends and moves on, consumer processes at own pace).

## Two Fundamental Patterns

### Publish-Subscribe (Pub-Sub)
Producer publishes to topic. **All subscribers** receive a copy. Messages are broadcast.

- Good for: event notifications ("order created" consumed by shipping, analytics, notifications simultaneously)
- Problem: every consumer gets every message - no built-in work distribution

### Message Queue (Point-to-Point)
Producer sends to queue. **Only one consumer** receives each message. Once consumed, gone for others.

- Good for: work distribution via **competing consumers** - 10 consumers on one queue = 10x throughput
- Key benefit: guaranteed single processing

### Choosing Between Them

| Question | Pub-Sub | Queue |
|----------|---------|-------|
| How many consumers per message? | Multiple | One |
| Should all consumers see every message? | Yes | No |
| Need guaranteed single processing? | No | Yes |
| Need work distribution / load balancing? | No | Yes |

**Trend:** Pub-sub and log models (Kafka) increasingly common. Many brokers support both patterns.

## Push vs Pull

| Model | Broker | Consumer Control | Latency | Example |
|-------|--------|-----------------|---------|---------|
| **Push** | Sends immediately | Must handle incoming rate | Low | RabbitMQ default |
| **Pull** | Waits for request | Controls pace and position | Variable | Kafka |

Push can overwhelm slow consumers (use prefetch count). Pull adds delay if polling infrequently.

## Delivery Guarantees

| Level | Behavior | Trade-off |
|-------|----------|-----------|
| **At most once** | Fire and forget | Fastest, messages can be lost |
| **At least once** | Delivered 1+ times, may duplicate | Most common, consumer must be idempotent |
| **Exactly once** | Delivered exactly once | Most expensive, often = at-least-once + idempotent consumer |

## Broker Architecture

### Federation
Multiple independent brokers connected together. Geographic distribution, loose coupling, isolated failure domains.

### Clustering
Tightly coupled brokers sharing state. High availability, automatic failover. More complex networking.

## Choosing a Broker

| Criteria | Kafka | RabbitMQ |
|----------|-------|----------|
| Data volume | High (100K+ msg/sec) | Moderate |
| Retention | Stored after consumption | Deleted after consumption |
| Ordering | Per-partition | Per-queue (FIFO) |
| Consumer model | Pull | Push |
| Routing | Simple (topic/partition) | Flexible (exchanges) |
| Replay | Yes (any offset) | No |
| Use case | Event streaming, big data | Task queues, request-response |

**Decision framework:**
1. High volume -> Kafka
2. Reliable delivery of small volumes -> RabbitMQ
3. Need flexible routing (exchanges, topics, headers) -> RabbitMQ
4. Need log replay / event sourcing -> Kafka
5. Strict global ordering -> single Kafka partition

## Gotchas

- **Competing consumers with pub-sub** - 3 consumers each processing every message = 3x duplicates. Use consumer groups (Kafka) or queue model
- **At-least-once without idempotency** - consumer processes message, ack lost due to network, message redelivered and processed again
- **Broker as database** - brokers are for message passing, not long-term storage (except Kafka with retention policies)
- **Message ordering** - only guaranteed within a single partition (Kafka) or single queue (RabbitMQ), not across

## See Also

- [[kafka-architecture]] - Deep dive into Kafka
- [[rabbitmq-architecture]] - Deep dive into RabbitMQ
- [[microservices-communication]] - Where brokers fit in service architecture
- [[data-serialization-formats]] - JSON, Avro, Protobuf for message payloads
- [[queueing-theory]] - Why systems degrade under load
