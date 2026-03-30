---
title: Message Queues and Event Streaming
category: reference
tags: [messaging, kafka, rabbitmq, async, event-driven]
---
# Message Queues and Event Streaming

Message queues enable asynchronous communication between services, decoupling producers from consumers by format contract only. They serve two primary purposes: service independence and load smoothing.

## Key Facts

- Two main purposes: (1) decouple services so they depend only on message format, not on discovery/scaling/availability of each other; (2) smooth load spikes so slow consumers process at their own pace
- Queues are commonly placed before databases to buffer write bursts
- Two paradigms: **message queue** (message consumed once, then deleted) vs **event log** (messages retained, multiple consumers read independently)
- RabbitMQ = classic message queue with exchanges and routing. Kafka = distributed event log with topics and partitions
- Key difference: RabbitMQ can route messages via Direct/Topic/Fanout exchanges. Kafka topics are "straight pipes" - no server-side routing, filtering, or fan-out logic
- [[orchestration-vs-choreography]] determines whether services use request-reply or event-driven patterns
- [[distributed-system-patterns]] covers how queues enable patterns like CQRS, Event Sourcing, Saga

## Patterns

### RabbitMQ exchange types

```
Direct Exchange:
  Producer --> [Exchange] --routing_key="order.created"--> [Queue A]
                          --routing_key="order.paid"----> [Queue B]

Topic Exchange:
  Producer --> [Exchange] --"order.*"---------> [Queue A] (all order events)
                          --"*.created"-------> [Queue B] (all created events)
                          --"order.created"---> both queues

Fanout Exchange:
  Producer --> [Exchange] --> [Queue A]
                          --> [Queue B]  (all queues get all messages)
                          --> [Queue C]
```

### Kafka architecture

```
Topic: "orders"
  Partition 0: [msg0, msg3, msg6, msg9, ...]  --> Consumer A
  Partition 1: [msg1, msg4, msg7, msg10, ...]  --> Consumer B
  Partition 2: [msg2, msg5, msg8, msg11, ...]  --> Consumer C

Consumer Group "processing":
  - Each partition consumed by exactly one consumer in group
  - Adding consumers (up to partition count) = horizontal scaling
  - Messages retained by time/size policy, not consumption

Consumer Group "analytics":
  - Independent read position (offset)
  - Same messages, different processing
```

### When to use which

| Criterion | RabbitMQ | Kafka |
|-----------|----------|-------|
| Message routing | Complex (exchanges) | None (straight pipe) |
| Message retention | Until consumed | Time/size-based |
| Consumer groups | Competing consumers | Independent offsets |
| Ordering | Per-queue | Per-partition |
| Throughput | ~50K msg/s | ~1M+ msg/s |
| Latency | Lower (push) | Higher (pull/batch) |
| Use case | Task queues, RPC | Event streaming, logs |
| Replay | No | Yes (re-read from offset) |

### Delivery guarantees

```
At-most-once:   Fire and forget. May lose messages.
At-least-once:  Retry until ack. May duplicate.
Exactly-once:   Kafka transactions (producer + consumer in same cluster).
                 Cross-system: use idempotent consumers.

Practical approach: at-least-once + idempotent consumer
  - Assign each message a unique ID
  - Consumer checks "have I processed this ID?"
  - Cheaper and simpler than exactly-once infrastructure
```

## Gotchas

- **Symptom**: Consumer lag grows continuously -> **Cause**: Consumer processing slower than producer rate -> **Fix**: Scale consumers (add more to consumer group), or increase partition count. In RabbitMQ, add competing consumers to the queue
- **Symptom**: Message ordering broken in Kafka -> **Cause**: Messages for same entity spread across partitions -> **Fix**: Use entity ID as partition key (e.g., `order_id`). All messages for same order go to same partition, preserving order
- **Symptom**: Lost messages after consumer crash -> **Cause**: Auto-commit offset before processing completes -> **Fix**: Manual offset commit AFTER successful processing. Accept potential redelivery (at-least-once) with idempotent consumer
- **Symptom**: Queue depth grows despite healthy consumers -> **Cause**: Dead letter queue not configured; poison messages block processing -> **Fix**: Configure DLQ with max retry count. After N failures, move message to DLQ for investigation

## See Also

- [[orchestration-vs-choreography]] - How queues fit into service communication
- [[distributed-system-patterns]] - Event-driven architecture patterns
- [[caching-strategies]] - Queues often combined with cache invalidation
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- Book: "Designing Data-Intensive Applications" (Kleppmann) - Chapter 11
