---
title: Async and Event-Based APIs
category: reference
tags: [async, websocket, sse, webhooks, polling, concurrency, api]
---

# Async and Event-Based APIs

Asynchronous APIs enable non-blocking communication. Critical for real-time features, long-running operations, and scalable architectures.

## Sync vs Async Comparison

| Attribute | Synchronous | Asynchronous |
|-----------|------------|--------------|
| Execution | Waits for response | Continues without waiting |
| Resource usage | Less efficient (idle during wait) | More efficient (parallel) |
| Scalability | Lower (blocking) | Higher (parallel processing) |
| Code complexity | Simpler, sequential | More complex, non-linear |
| Data consistency | Fewer issues | Potential ordering problems |

## HTTP-Based Async Mechanisms

### Callback
Client provides URL for server to call when response ready.
- **Low latency**, moderate complexity
- Problem: "callback hell" with nested callbacks, security concerns

### Polling
Client repeatedly sends requests at intervals.
- **Simple** implementation, high latency, high server load
- Use case: monitoring dashboards, news feeds

### Long Polling
Server holds request open until new data available.
- **Low-moderate latency**, moderate server load
- Use case: chat apps, live sports scores

| Feature | Callback | Polling | Long Polling |
|---------|----------|---------|--------------|
| Complexity | Moderate | Simple | Moderate |
| Latency | Low | High | Low-moderate |
| Server load | Low-moderate | High | Moderate |

## Advanced Async Technologies

### Webhooks
Server sends HTTP POST to predefined client endpoint when event occurs. Event-driven, eliminates polling.

**Use cases:** Payment notifications, CI/CD triggers, subscription updates.

**Considerations:**
- Retry logic for failed deliveries
- HMAC signature for security
- Idempotency keys for duplicate handling

### WebSockets
Full-duplex bidirectional communication over single long-lived connection. Supports text and binary data.

```php
HTTP upgrade handshake -> persistent WebSocket connection
Client <---> Server (bidirectional)
```

**Use cases:** Real-time chat, online auctions, collaborative editing, gaming.

**Drawbacks:** Connection management complexity, stateful connections harder to scale, load balancer considerations.

### Server-Sent Events (SSE)
Unidirectional server-to-client stream over HTTP. Simpler than WebSockets.

**Use cases:** Stock tickers, notifications, live feeds, progress updates.

**Advantages over WebSocket:** Works with standard HTTP infrastructure, automatic reconnection, simpler implementation.

## Concurrency and Consistency

### Optimistic Locking (Preferred for web APIs)

**ETag-based (recommended for high load):**
```bash
GET /resource -> ETag: "v5"
PUT /resource + If-Match: "v5"
  Success: 200 OK + new ETag
  Conflict: 412 Precondition Failed
```

**Timestamp-based (simpler):**
```bash
GET /resource -> Last-Modified: timestamp
PUT /resource + If-Unmodified-Since: timestamp
  Conflict: 412 Precondition Failed
```

### Pessimistic Locking (For high-cost conflicts)
```bash
POST /resource?lock=true -> lockToken
PUT /resource + X-Lock-Token: token -> update + release
Already locked -> 409 Conflict
```

Use pessimistic locking for financial transactions where conflicts are very costly.

## AsyncAPI Specification

Similar to OpenAPI but for event-driven APIs. Describes channels (topics/queues), messages, schemas, and server bindings for Kafka, RabbitMQ, WebSocket, MQTT.

## Gotchas

- **WebSocket through load balancers** - sticky sessions or connection-aware routing required
- **SSE connection limit** - browsers limit concurrent SSE connections per domain (~6)
- **Webhook security** - always verify HMAC signatures, never trust payload without verification
- **Polling interval** - too frequent wastes resources, too infrequent creates stale data
- **Optimistic locking timestamps** - not precise enough under high load, prefer ETags

## See Also

- [[http-rest-fundamentals]] - HTTP protocol foundation
- [[microservices-communication]] - Service communication patterns
- [[message-broker-patterns]] - Kafka, RabbitMQ for backend async
- [[api-documentation-specs]] - AsyncAPI specification
