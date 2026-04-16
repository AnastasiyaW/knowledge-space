---
title: Distributed Transactions and Patterns
category: concepts
tags: [sql-databases, distributed-transactions, two-phase-commit, saga, eventual-consistency, double-booking]
---

# Distributed Transactions and Patterns

When data spans multiple databases or services, maintaining consistency requires patterns beyond single-database ACID. The two main approaches - 2PC and Saga - trade off between consistency guarantees and availability.

## Two-Phase Commit (2PC)

Coordinator asks all participants to prepare (phase 1), then commit (phase 2). If any participant votes no, all abort.

**Problem:** Coordinator failure during commit phase = participants stuck in uncertain state (blocking protocol). Synchronous, high latency.

**Use case:** When strong consistency is required across databases and latency is acceptable.

## Saga Pattern

Sequence of local transactions with compensating transactions for rollback. Each step commits independently.

```php
Step 1: Reserve inventory  -> Compensate: Release inventory
Step 2: Charge payment     -> Compensate: Refund payment
Step 3: Ship order         -> Compensate: Cancel shipment
```

If step N fails, execute compensating transactions for steps N-1...1.

**Types:** Choreography (events between services) vs orchestration (central coordinator).

**Pros:** Better availability than 2PC, no blocking. **Cons:** Complex compensation logic, eventual consistency.

## Double-Booking Prevention

### Pessimistic (SELECT FOR UPDATE)
```sql
BEGIN;
SELECT * FROM seats WHERE id = 42 AND status = 'available' FOR UPDATE;
-- Row locked. If available:
UPDATE seats SET status = 'booked', user_id = 123 WHERE id = 42;
COMMIT;
```

### Optimistic (Unique Constraint)
```sql
ALTER TABLE bookings ADD CONSTRAINT uq_seat_event UNIQUE (seat_id, event_id);
-- Second booking fails with constraint violation - app catches and retries
```

### Advisory Locks
```sql
SELECT pg_advisory_lock(42);  -- lock seat 42
-- Check and book...
SELECT pg_advisory_unlock(42);
```

### Serializable Isolation
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Database detects conflicts automatically - simplest code, higher abort rate
```

## Hash Tables in Databases

Used internally for: hash joins (build on smaller table, probe with larger), hash aggregation (GROUP BY), hash partitioning, hash indexes.

Collision strategies: chaining (linked lists), open addressing (linear/quadratic probing), cuckoo hashing (two hash functions, O(1) guaranteed).

## Key Facts

- 2PC is a blocking protocol - participant failure during commit blocks all others
- Saga provides eventual consistency, not strong consistency
- Compensating transactions must be idempotent (safe to retry)
- `SELECT FOR UPDATE` is the simplest double-booking prevention in single-database scenarios
- Serializable isolation in PostgreSQL uses SSI (Serializable Snapshot Isolation) - not actual serial execution

## Gotchas

- 2PC coordinator is a single point of failure - requires its own HA
- Saga compensation logic can be as complex as the original business logic
- Eventual consistency means users may see stale data temporarily
- `SELECT FOR UPDATE` blocks concurrent access - high contention = bottleneck
- Advisory locks in PgBouncer transaction mode: released when connection returns to pool

## See Also

- [[transactions-and-acid]] - single-database ACID guarantees
- [[concurrency-and-locking]] - lock types for preventing conflicts
- [[distributed-databases]] - databases with built-in distributed transactions
- [[partitioning-and-sharding]] - cross-shard transaction challenges
