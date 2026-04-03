---
title: NATS Comparison
category: reference
tags: [nats, kafka-alternative, jetstream, pub-sub, queue-groups, kv-store]
---

# NATS Comparison

NATS is a lightweight messaging system with three layers (Core, JetStream, Clustering), offering simpler operations and lower latency than Kafka at the cost of weaker ordering guarantees and a smaller ecosystem.

## Key Facts

- NATS Core: fast non-persistent messaging; messages are ephemeral (no persistence, no buffer)
- NATS JetStream: adds persistence with replay, quorum replication, durable consumers
- Subject format: `a.b.c.d` (dot-separated); wildcards: `*` (single token), `>` (remainder)
- **Queue Groups**: built-in load balancing - multiple consumers subscribe with queue group name, each message delivered to only ONE consumer
- **Request/Response**: native pattern via temporary INBOX subscriptions
- Clustering: mesh + superclusters (cluster of clusters) + leaf nodes (edge nodes)
- Built-in **Key/Value Store** (distributed, versioned map on JetStream) and **Object Store** (content-addressed blobs)
- NATS Execution Engine (Nex): serverless - deploy JS functions, WebAssembly, Linux binaries

## Patterns

### NATS vs Kafka

| Aspect | NATS | Kafka |
|--------|------|-------|
| Core model | Messaging (ephemeral default) | Distributed log (persistent default) |
| Persistence | Optional (JetStream) | Always |
| Work queues | Built-in queue groups | Consumer groups |
| Request/Reply | Native pattern | Not native |
| KV Store | Built-in | Not built-in |
| Ordering | Per subject (weaker) | Per partition (strict) |
| Ecosystem | Smaller | Large Apache ecosystem |
| Clustering | Mesh + superclusters + leaf | Broker cluster + controller |
| Protocol | Custom binary, lightweight | Custom binary, heavier |

### JetStream Consumer Ack Modes

| Mode | Behavior |
|------|----------|
| Explicit | Consumer acks each message; unacked redelivered after AckWait |
| All | Acking message N implicitly acks all up to N |
| None | No acks required, fire-and-forget |

### When to Use NATS vs Kafka

| Requirement | Recommendation |
|-------------|---------------|
| Event loss tolerance, high throughput, simple delivery | NATS |
| Streaming, high durability, strict FIFO, replay | Kafka |
| IoT, ultra-low latency | NATS |
| Complex processing, CDC, event sourcing | Kafka |
| Quick start, simple setup | NATS |
| Large ecosystem, many connectors | Kafka |

## Gotchas

- **NATS Core messages are ephemeral** - if no subscriber is listening when a message is published, it is lost; JetStream adds persistence
- **NATS ordering is per-subject, not per-partition** - weaker than Kafka's per-partition ordering guarantee
- **KV Store has limits** - 1MB value cap, no cross-key transactions
- **Object Store objects are immutable** - no partial writes, sequential access only

## See Also

- [[messaging-models]] - queue, pub-sub, log-based models comparison
- [[broker-architecture]] - Kafka's architecture for comparison
- [NATS Documentation](https://docs.nats.io/)
