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

## Gotchas

- Serializable doesn't literally serialize transactions - uses dependency tracking (SSI in PG)
- `SELECT FOR UPDATE` in transaction-level pooling (PgBouncer) can cause unexpected lock release
- Two transactions both doing `SELECT FOR SHARE` then UPDATE on same row = deadlock
- Lost updates are possible even at Read Committed - use `SELECT FOR UPDATE` or higher isolation

## See Also

- [[concurrency-and-locking]] - lock types, deadlocks, advisory locks
- [[postgresql-wal-durability]] - WAL and durability trade-offs
- [[postgresql-mvcc-vacuum]] - MVCC implementation details
- [[connection-pooling]] - pooling modes and transaction behavior
