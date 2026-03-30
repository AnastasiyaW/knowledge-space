---
title: Distributed System Patterns
category: patterns
tags: [distributed-systems, cqrs, event-sourcing, circuit-breaker, scaling]
---
# Distributed System Patterns

Reusable architectural patterns for solving common problems in distributed systems: scaling, consistency, fault tolerance, and data management.

## Key Facts

- Distributed systems are inherently complex: network is unreliable, latency is non-zero, bandwidth is finite (Fallacies of Distributed Computing)
- Little's Law: L = lambda * W (queue length = arrival rate * processing time). Fundamental for capacity planning
- The longer the processing time, the larger the queue. Queues before slow services ([[message-queues]]) prevent cascading failures
- Every rule/pattern can be broken IF done consciously with understanding of consequences
- Patterns are tools, not mandates. Using a pattern because it's "best practice" without understanding the tradeoff is cargo-cult architecture
- See [[cap-theorem]] for the fundamental consistency/availability tradeoff
- See [[quality-attributes]] for how quality requirements select patterns

## Patterns

### Scaling patterns

```
Vertical scaling:
  Bigger machine (more CPU, RAM, disk)
  + Simple, no code changes
  - Hard limit, expensive at top
  - Single point of failure

Horizontal scaling:
  More machines behind load balancer
  + Linear capacity growth
  + Fault tolerant (one node fails, others serve)
  - Requires stateless services (see [[caching-strategies]])
  - Distributed coordination complexity

Database scaling:
  Read replicas:    Primary (writes) --> Replicas (reads)
  Sharding:         Data partitioned by key across nodes
  CQRS:             Separate read/write models and stores
```

### CQRS (Command Query Responsibility Segregation)

```
Traditional:
  [Service] --> [Single DB] (reads + writes)

CQRS:
  [Write API] --> [Write DB (normalized)]
                    |
                 [Event/Sync]
                    |
  [Read API]  --> [Read DB (denormalized, optimized)]

Write side:
  - Normalized data model
  - Strong consistency (ACID)
  - Lower throughput OK

Read side:
  - Denormalized for query patterns
  - Eventually consistent
  - Optimized for fast reads

When to use:
  - Read/write ratio > 10:1
  - Read and write patterns are fundamentally different
  - Need independent scaling of reads vs writes
```

### Event Sourcing

```
Traditional: store current state
  Order: { status: "shipped", total: 100 }

Event Sourcing: store all events
  Event 1: OrderCreated    { items: [...], total: 100 }
  Event 2: PaymentReceived { amount: 100 }
  Event 3: OrderShipped    { tracking: "ABC123" }

Current state = replay all events (or read from snapshot)

Benefits:
  + Complete audit trail
  + Can rebuild state at any point in time
  + Natural fit with [[message-queues]] and choreography
  - Storage grows indefinitely (snapshot to mitigate)
  - Complex to query (need projections/read models)
```

### Circuit Breaker

```
States:
  CLOSED (normal):
    Requests pass through
    Count failures

  OPEN (failing):
    Requests fail immediately (fast-fail)
    Don't hit the broken service
    Timer running

  HALF-OPEN (testing):
    Allow ONE request through
    If succeeds -> CLOSED
    If fails    -> OPEN (reset timer)

            failure_threshold
  [CLOSED] -----------------> [OPEN]
     ^                          |
     |         timeout          |
     |                          v
     +-----success--------- [HALF-OPEN]
     |                          |
     +-----failure------------>+

Implementation: Resilience4j (Java), Polly (.NET), custom
Or use [[service-mesh]] which provides this automatically
```

### Retry with exponential backoff

```python
def retry_with_backoff(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)  # 1, 2, 4, 8, 16
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)

# Jitter prevents thundering herd when multiple
# clients retry simultaneously
```

### Idempotency pattern

```
Problem: retries can cause duplicate processing

Solution: idempotency key
  Client: POST /orders
    Idempotency-Key: "uuid-abc-123"

  Server:
    1. Check: is "uuid-abc-123" in idempotency store?
    2. Yes -> return cached result (no re-processing)
    3. No  -> process, store result keyed by UUID
    4. Return result

Store: Redis with TTL (e.g., 24h) or database table
Key: client-generated UUID or hash of request body
```

### Bulkhead pattern

```
Problem: one slow service consumes all threads/connections
  ThreadPool (size=100):
    Service A calls: 90 threads (stuck on slow B)
    Service C calls: 10 threads (starved)

Solution: isolated resource pools
  Pool for Service B (max 30):
    Service B calls: 30 threads max
    If pool exhausted -> fast-fail, don't block others

  Pool for Service C (max 30):
    Service C calls: always have 30 threads available

  Pool for Service D (max 40):
    ...
```

## Gotchas

- **Symptom**: Downstream service recovers but circuit breaker stays open -> **Cause**: Half-open test request happens to fail (transient) -> **Fix**: In half-open state, allow a small percentage of requests (not just one). Use success rate threshold, not single request
- **Symptom**: Retry storm takes down recovering service -> **Cause**: All clients retry simultaneously with same backoff schedule -> **Fix**: Add jitter (random delay component) to backoff. Different clients should retry at different times
- **Symptom**: Event sourcing event store grows to terabytes -> **Cause**: No snapshots, replaying from beginning for each read -> **Fix**: Implement periodic snapshots. Current state = last snapshot + events after snapshot
- **Symptom**: CQRS read model is stale causing user confusion -> **Cause**: Event processing lag between write and read stores -> **Fix**: After write, redirect user to the write service's response (not read model). Show "processing" state. Or accept eventual consistency and communicate it in UI

## See Also

- [[cap-theorem]] - Fundamental tradeoff driving pattern selection
- [[message-queues]] - Infrastructure enabling event-driven patterns
- [[orchestration-vs-choreography]] - Saga pattern for distributed transactions
- [[service-mesh]] - Infrastructure implementing circuit breaker, retry
- [[quality-attributes]] - Requirements that determine which patterns to apply
- Microsoft: [Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)
- Martin Fowler: [CQRS](https://martinfowler.com/bliki/CQRS.html)
- Martin Fowler: [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- Martin Fowler: [Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html)
- Book: "Designing Data-Intensive Applications" (Kleppmann)
