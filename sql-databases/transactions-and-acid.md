---
title: Transactions and ACID Properties
category: concepts
tags: [sql, transaction, acid, isolation-level, read-committed, repeatable-read, serializable, postgresql, mysql]
---

# Transactions and ACID Properties

Transactions group multiple SQL operations into an atomic unit. ACID properties (Atomicity, Consistency, Isolation, Durability) define the guarantees a database provides. Understanding isolation levels is critical for preventing data anomalies in concurrent systems.

## Key Facts

- **Atomicity** - all operations in a transaction succeed or all are rolled back
- **Consistency** - transactions move the database from one valid state to another (constraints are satisfied)
- **Isolation** - concurrent transactions don't interfere with each other (to the degree specified by isolation level)
- **Durability** - committed data survives system crashes (written to WAL/redo log before commit)
- PostgreSQL default isolation: **Read Committed**. MySQL/InnoDB default: **Repeatable Read**
- PostgreSQL uses **MVCC** (Multi-Version Concurrency Control) - readers never block writers, writers never block readers. See [[postgresql-vacuum-and-mvcc]]
- MySQL/InnoDB also uses MVCC but with different locking behavior at higher isolation levels
- See [[postgresql-vacuum-and-mvcc]] for how MVCC implements isolation without locks
- See [[data-integrity-constraints]] for consistency enforcement via constraints

## Patterns

### Isolation levels and anomalies they prevent

```
Level                  | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly
-----------------------|------------|--------------------|--------------|-----------------------
READ UNCOMMITTED       | possible   | possible           | possible     | possible
READ COMMITTED (PG)    | prevented  | possible           | possible     | possible
REPEATABLE READ (MySQL)| prevented  | prevented          | prevented*   | possible
REPEATABLE READ (PG)   | prevented  | prevented          | prevented    | possible
SERIALIZABLE           | prevented  | prevented          | prevented    | prevented

* MySQL REPEATABLE READ prevents phantoms via gap locks
* PG REPEATABLE READ prevents phantoms via snapshot isolation
```

### Basic transaction usage

```sql
-- Explicit transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Rollback on error
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (1, 500);
-- something goes wrong
ROLLBACK;

-- Savepoints for partial rollback
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (1, 500);
SAVEPOINT sp1;
INSERT INTO order_items (order_id, product_id) VALUES (1, 999);  -- might fail
-- Rollback just this insert, keep the order
ROLLBACK TO SAVEPOINT sp1;
COMMIT;
```

### Setting isolation levels

```sql
-- PostgreSQL: per-transaction isolation
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM inventory WHERE product_id = 42;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 42;
COMMIT;

-- PostgreSQL: session-level default
SET default_transaction_isolation = 'repeatable read';

-- MySQL: per-session isolation
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

### Serializable and conflict detection (PostgreSQL)

```sql
-- PostgreSQL serializable uses SSI (Serializable Snapshot Isolation)
-- No explicit locks - detects conflicts at commit time
-- If conflict detected: one transaction gets ERROR, retry needed

-- Pattern: retry loop for serializable transactions
-- Application code should catch serialization_failure (SQLSTATE 40001) and retry

-- Common conflict: two transactions read the same data and write based on it
-- T1: SELECT count(*) FROM orders WHERE status = 'pending'; INSERT INTO summary...
-- T2: INSERT INTO orders (status) VALUES ('pending');
-- With SERIALIZABLE: one of them will fail (dependency cycle detected)
```

### MySQL InnoDB locking at Repeatable Read

```sql
-- InnoDB uses gap locks + next-key locks at REPEATABLE READ to prevent phantoms
-- This means: SELECT ... FOR UPDATE locks a range, not just existing rows

-- Example: this locks the gap preventing inserts where department = 'sales'
SELECT * FROM employees WHERE department = 'sales' FOR UPDATE;

-- Contrast: PostgreSQL REPEATABLE READ uses snapshot isolation (no gap locks)
-- Same query in PG only locks the specific rows found
```

## Gotchas

- **PostgreSQL Read Committed re-evaluates conditions** - within a single statement, concurrent commits can change visible data mid-execution. An UPDATE with WHERE clause re-checks the condition after acquiring the row lock
- **MySQL Repeatable Read hides new commits** - a snapshot is taken at the first read. This prevents phantoms but means you don't see changes committed by others during your transaction
- **Serializable performance** - PostgreSQL SSI has very low overhead compared to traditional locking serializable, but applications MUST handle retry logic for serialization failures
- **Autocommit** - both PostgreSQL and MySQL default to autocommit (each statement is its own transaction). Explicit BEGIN disables autocommit until COMMIT/ROLLBACK
- **Long-running transactions** - in PostgreSQL, long transactions prevent VACUUM from reclaiming dead tuples (see [[postgresql-vacuum-and-mvcc]]). Monitor with `pg_stat_activity`
- **Deadlocks** - both engines detect deadlocks and abort one transaction. Design to acquire locks in consistent order to minimize deadlocks

## See Also

- [[postgresql-vacuum-and-mvcc]] - how MVCC implements transaction isolation
- [[data-integrity-constraints]] - ensuring consistency beyond isolation
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [MySQL InnoDB transaction model](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-model.html)
