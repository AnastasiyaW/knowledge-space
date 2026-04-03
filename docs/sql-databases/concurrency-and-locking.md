---
title: Concurrency and Locking
category: concepts
tags: [sql-databases, locks, deadlock, advisory-lock, pessimistic, optimistic, two-phase-locking, postgresql, mysql]
---

# Concurrency and Locking

Database locking controls concurrent access to shared data. Understanding lock types, granularity, and deadlock patterns is essential for building reliable concurrent applications.

## PostgreSQL Table Lock Types (8 Levels)

From lightest to heaviest:

| Lock | Acquired By | Blocks |
|------|-------------|--------|
| ACCESS SHARE | SELECT | Only ACCESS EXCLUSIVE |
| ROW SHARE | SELECT FOR UPDATE/SHARE | ACCESS EXCLUSIVE, EXCLUSIVE |
| ROW EXCLUSIVE | INSERT, UPDATE, DELETE | SHARE and above |
| SHARE UPDATE EXCLUSIVE | VACUUM, ANALYZE, CREATE INDEX CONCURRENTLY | Itself and above |
| SHARE | CREATE INDEX (non-concurrent) | ROW EXCLUSIVE and above (NOT itself) |
| SHARE ROW EXCLUSIVE | CREATE TRIGGER, ALTER TABLE ADD FK | Itself and above |
| EXCLUSIVE | REFRESH MATERIALIZED VIEW CONCURRENTLY | Everything except ACCESS SHARE |
| ACCESS EXCLUSIVE | DROP TABLE, TRUNCATE, VACUUM FULL, most ALTER TABLE | Everything including SELECT |

Key insight: Different ALTER TABLE operations acquire different lock levels.

## PostgreSQL Row Lock Types

| Lock | Acquired By | Blocks |
|------|-------------|--------|
| FOR KEY SHARE | SELECT FOR KEY SHARE | Only FOR UPDATE |
| FOR SHARE | SELECT FOR SHARE | UPDATE, DELETE, FOR UPDATE |
| FOR NO KEY UPDATE | UPDATE on non-key columns | FOR SHARE and above |
| FOR UPDATE | DELETE, UPDATE on key columns | Everything |

Implementation: PostgreSQL stores row locks in tuple header (`xmax` field), not in memory. Saves memory but SELECT FOR UPDATE can dirty pages.

## MySQL InnoDB Lock Types

- **Shared (S):** `SELECT ... FOR SHARE`. Multiple holders allowed.
- **Exclusive (X):** `SELECT ... FOR UPDATE`, INSERT, UPDATE, DELETE. Single holder.
- **Intention locks (IS/IX):** Table-level signals that transaction intends to lock rows.
- **Gap lock:** Locks gap between index records. Prevents phantom reads at REPEATABLE READ.
- **Next-key lock:** Gap lock + record lock. Default at RR in InnoDB.
- **Insert intention lock:** Allows concurrent inserts at different positions within same gap.
- **MDL (Metadata Lock):** DDL acquires MDL exclusive, blocked until all active DML finishes.

## Patterns

### Double-Booking Prevention
```sql
-- Pessimistic: SELECT FOR UPDATE
BEGIN;
SELECT * FROM seats WHERE seat_id = 42 AND status = 'available' FOR UPDATE;
UPDATE seats SET status = 'booked', user_id = 123 WHERE seat_id = 42;
COMMIT;

-- Optimistic: unique constraint
ALTER TABLE bookings ADD CONSTRAINT uq_seat_event UNIQUE (seat_id, event_id);
-- Second booking attempt fails with constraint violation
```

### Advisory Locks (PostgreSQL)
```sql
-- Session-level: held until explicit release or session end
SELECT pg_advisory_lock(42);      -- lock ID 42
-- Do work across multiple transactions...
SELECT pg_advisory_unlock(42);

-- Transaction-level: released on COMMIT/ROLLBACK
SELECT pg_advisory_xact_lock(42);
```

Advisory locks don't block row modifications and can span transactions. Useful for application-level locking without actual rows.

### Deadlock Pattern
```sql
-- Session 1:                    -- Session 2:
BEGIN;                            BEGIN;
UPDATE t SET v=1 WHERE id=1;     UPDATE t SET v=2 WHERE id=2;
-- holds lock on id=1             -- holds lock on id=2
UPDATE t SET v=1 WHERE id=2;     UPDATE t SET v=2 WHERE id=1;
-- waits for id=2                 -- waits for id=1 -> DEADLOCK
```

### Two-Phase Locking (2PL)

Growing phase (acquire locks) then shrinking phase (release locks). Strict 2PL holds all locks until COMMIT/ROLLBACK. Guarantees conflict serializability.

## Key Facts

- PostgreSQL: VACUUM acquires SHARE UPDATE EXCLUSIVE (allows concurrent reads and writes)
- VACUUM FULL acquires ACCESS EXCLUSIVE (blocks everything including SELECT)
- Weak locks use fast-path optimization (16 slots per backend) - heavily partitioned tables can exceed this
- PostgreSQL detects deadlocks automatically and kills one transaction (victim)
- Even zero-row DML acquires ROW EXCLUSIVE lock on the table
- MDL cascade in MySQL: ALTER TABLE waits for long SELECT, new SELECTs queue behind ALTER

## Gotchas

- `SELECT FOR SHARE` by two transactions, then one tries UPDATE = deadlock
- Advisory locks span transactions in session mode - leaks possible if not explicitly released
- PgBouncer transaction-mode pooling releases advisory session locks unexpectedly
- INSERTed tuples don't need row locks in PostgreSQL - they're invisible to other transactions
- Deadlock detection adds overhead - design lock ordering to prevent deadlocks

## See Also

- [[transactions-and-acid]] - isolation levels and read phenomena
- [[postgresql-mvcc-vacuum]] - MVCC as alternative to locking
- [[mysql-innodb-engine]] - InnoDB locking internals
- [[connection-pooling]] - lock behavior with connection poolers
