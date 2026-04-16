---
title: RabbitMQ Architecture
category: reference
tags: [rabbitmq, message-queue, exchange, routing, amqp]
---

# RabbitMQ Architecture

RabbitMQ is a message broker built on the queue model. "Smart broker - dumb consumer" pattern: delivery logic on the broker side. Push model by default.

## Message Flow

```php
Producer -> Exchange -> [Binding + Routing Key] -> Queue -> Consumer
```

**Producers never write directly to queues.** Exchange receives all messages and routes them.

## Exchange Types

| Type | Routing Logic | Speed | Use Case |
|------|--------------|-------|----------|
| **Fanout** | Broadcast to ALL bound queues | Fastest | Single queue, broadcast |
| **Direct** | Exact Routing Key match | Fast | Simple routing (most common) |
| **Topic** | Wildcard Routing Key (`*`=one word, `#`=any) | Slower | Complex business logic |
| **Headers** | Header matching (`x-match=all` or `any`) | Slowest | Multiple matching criteria |

**Selection guide:**
1. More than one queue? No -> Fanout
2. Need >1000 msg/sec? Yes -> Direct or Fanout only
3. Must go to exactly one queue? Yes -> Direct

**Topic examples:** `asia.china.done` matches `#.done`, `asia.*.done`, `asia.china.*`

## Queue Types

| Type | Behavior | Use Case |
|------|----------|----------|
| **Classic** | Standard FIFO, one consumer per message | Most common |
| **Quorum** | Distributed replication for fault tolerance | Production reliability |
| **Stream** | Kafka-like, retains data, multiple consumers | High volume, replay |

## Message Structure

| Field | Purpose |
|-------|---------|
| `Payload` | Message body (your data) |
| `Routing Key` | Determines routing via binding |
| `delivery_mode` | 1 = memory only, 2 = persist to disk |
| `mandatory` | Return to producer if no binding match |
| `expiration` | Message TTL |
| `confirm` | Request delivery confirmation |

## Persistence

Messages lost on crash unless:
1. Queue `durable` flag enabled **AND**
2. Producer sends with `delivery_mode = 2`

Both required. Missing either = memory-only storage.

## Delivery Guarantees

### Consumer-side (Ack/Nack)
- **Ack** - successful processing, message removed from queue
- **Nack** - processing failure, message returns to queue (also on connection break)
- **AutoAck** - broker auto-acknowledges on send (at-most-once, fastest)

**Prefetch count** controls unacknowledged messages per consumer. `prefetch_count=1` = strict one-at-a-time.

### Producer-side
Same Ack/Nack mechanism. `confirm` parameter enables full delivery tracking. `mandatory` returns unroutable messages.

### Duplicate risk
Consumer processes message but ack doesn't reach broker (network). Message redelivered. Need idempotent consumers for exactly-once semantics.

## Dead Letter Exchange (DLE)

Failed messages route to DLE instead of being lost. Combine with automatic retry after timeout and error logging.

## High Availability

- Multiple instances behind load balancer
- Quorum Queues for fault tolerance
- Cluster configuration for production

## Design Example

```php
task_queue (Direct)           -> task processing
status_update_queue (Topic)   -> status tracking (*.completed, *.failed)
notification_queue (Fanout)   -> broadcast notifications
priority_queue (Direct)       -> urgent tasks
audit_queue (Direct)          -> compliance logging

Each queue has: Dead Letter Exchange, Quorum Queue, automatic retry
```

## Gotchas

- **No disk persistence by default** - messages lost on crash without explicit `durable` + `delivery_mode=2`
- **Fanout ignores routing key** - binding settings have no effect, all bound queues get everything
- **Prefetch=0** means unlimited - broker sends all messages immediately, can overwhelm consumer
- **Queue names** are globally unique within a vhost - collision possible in multi-team environments
- **Not for massive data streams** - use Kafka for high-volume event streaming

## See Also

- [[kafka-architecture]] - Log-based alternative for high-volume streaming
- [[message-broker-patterns]] - Choosing between brokers, delivery guarantees
- [[microservices-communication]] - Service communication patterns
