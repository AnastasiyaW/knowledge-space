---
title: Transactions and ACID Properties
category: concepts
tags: [sql-databases, transaction, acid, isolation-level, read-committed, repeatable-read, serializable, snapshot-isolation]
---

# Transactions and ACID Properties

Transactions group multiple queries into an atomic unit of work. ACID properties (Atomicity, Consistency, Isolation, Durability) guarantee reliable data processing even under concurrent access and system failures.

## Transaction Lifecycle

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- verify >= 100
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Or ROLLBACK; to undo all changes
```

Read-only transactions are valid - used for consistent snapshots (reports).

## ACID Properties

**Atomicity:** All queries succeed or all rollback. A crash between the two UPDATEs above triggers automatic rollback on recovery - no partial state.

**Consistency:** Two dimensions: (1) data consistency - referential integrity, CHECK constraints, UNIQUE constraints; (2) read consistency - whether next read sees just-committed data (CAP theorem's C).

**Isolation:** Controls visibility of concurrent transaction changes. See isolation levels below.

**Durability:** Committed changes survive crashes. Implemented via WAL (write-ahead log). `fsync()` forces physical disk write but is expensive. `synchronous_commit = off` in PostgreSQL trades durability risk (~600ms window) for 3x faster commits.

## Read Phenomena

| Phenomenon | Description |
|-----------|-------------|
| Dirty Read | Reading uncommitted data from another transaction |
| Non-Repeatable Read | Same row returns different values between reads in one transaction |
| Phantom Read | Re-executing range query returns new rows inserted by another transaction |
| Lost Update | Two transactions read same row, both update, second overwrites first |

## Isolation Levels

| Level | Dirty Read | Non-Repeatable | Phantom | Lost Update |
|-------|-----------|----------------|---------|-------------|
| Read Uncommitted | Yes | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes | Yes |
| Repeatable Read | No | No | Yes* | No |
| Serializable | No | No | No | No |

*PostgreSQL implements Repeatable Read as Snapshot Isolation - prevents phantoms too. MySQL InnoDB uses next-key locking at RR.

**Read Committed** (default in PostgreSQL, Oracle): Each statement sees only data committed before it began. Default for most production use.

**Repeatable Read:** Transaction sees snapshot from start. PostgreSQL = snapshot isolation (optimistic, detect conflicts at commit). MySQL = next-key locking (pessimistic, prevent conflicts with locks).

**Serializable:** Transactions execute as if serialized. PostgreSQL uses SSI (Serializable Snapshot Isolation) - concurrent execution with dependency tracking, aborts on anomaly.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Or globally:
ALTER DATABASE mydb SET DEFAULT_TRANSACTION_ISOLATION TO 'read committed';
```

## Implementation Approaches

**Pessimistic (locking):** Lock rows/pages before modification. Block on conflict. `SELECT FOR UPDATE` is pessimistic serializable. Best for high-contention workloads.

**Optimistic (MVCC):** No locks during execution. Track changes, fail on conflict at commit. Better for low-contention, read-heavy workloads.

## Key Facts

- PostgreSQL: RR = Snapshot Isolation (no phantom reads, unlike MySQL)
- PostgreSQL does not support READ UNCOMMITTED (treated as Read Committed)
- MySQL InnoDB default is REPEATABLE READ with gap locks
- `SELECT FOR UPDATE` acquires exclusive row lock until transaction ends
- Long transactions hold connections and locks - set `idle_in_transaction_session_timeout`

### Claiming Rows Pattern (Concurrent Workers)

Multiple workers claim tasks without conflicts:
```sql
-- Atomically claim next unclaimed row
UPDATE tasks
SET status = 'processing', worker_id = :my_id, claimed_at = NOW()
WHERE id = (
    SELECT id FROM tasks
    WHERE status = 'pending'
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED  -- skip rows locked by other workers
)
RETURNING *;
```
`SKIP LOCKED` (PostgreSQL 9.5+, MySQL 8.0+) - worker skips locked rows instead of waiting, enabling true parallel work queue.

### Advisory Locks (Application-Level Locking)

```sql
-- PostgreSQL: application-level named locks (not tied to rows)
SELECT pg_advisory_lock(12345);     -- blocks until acquired
-- ... critical section ...
SELECT pg_advisory_unlock(12345);

-- Try without blocking:
SELECT pg_try_advisory_lock(12345); -- returns true/false immediately

-- Session-level: released on disconnect
-- Transaction-level: released on COMMIT/ROLLBACK
SELECT pg_advisory_xact_lock(12345);
```
Use case: prevent duplicate cron job execution, coordinate external resource access.

### Savepoints (Partial Rollback)

```sql
BEGIN;
INSERT INTO orders (user_id, amount) VALUES (1, 100);

SAVEPOINT sp1;
INSERT INTO order_items (order_id, product_id) VALUES (1, 999);  -- might fail
-- If this fails:
ROLLBACK TO SAVEPOINT sp1;
-- order INSERT is preserved, only order_items rolled back

INSERT INTO order_items (order_id, product_id) VALUES (1, 42);  -- retry
COMMIT;  -- commits order + corrected order_items
```

## Gotchas

- Serializable doesn't literally serialize transactions - uses dependency tracking (SSI in PG)
- `SELECT FOR UPDATE` in transaction-level pooling (PgBouncer) can cause unexpected lock release
- Two transactions both doing `SELECT FOR SHARE` then UPDATE on same row = deadlock
- Lost updates are possible even at Read Committed - use `SELECT FOR UPDATE` or higher isolation
- `SKIP LOCKED` silently skips rows - if all rows are locked, returns empty result (not an error)
- Advisory locks are NOT automatically released on transaction end (session-level variant) - always explicitly unlock or use `pg_advisory_xact_lock`
- Savepoints inside `autocommit` mode have no effect - always use within explicit `BEGIN`
- Long-running transactions in MVCC hold old row versions alive, preventing VACUUM - set `idle_in_transaction_session_timeout`

## See Also

- [[concurrency-and-locking]] - lock types, deadlocks, advisory locks
- [[postgresql-wal-durability]] - WAL and durability trade-offs
- [[postgresql-mvcc-vacuum]] - MVCC implementation details
- [[connection-pooling]] - pooling modes and transaction behavior
