---
title: PostgreSQL for Data Engineering
category: tools
tags: [data-engineering, postgresql, rdbms, transactions, plpgsql, optimization]
---

# PostgreSQL for Data Engineering

PostgreSQL is the most common RDBMS in data engineering - used as Airflow metastore, source system, and sometimes as analytical database. Understanding its architecture, transactions, and procedural extensions is essential.

## Architecture

- **Client-server model:** postmaster manages backend processes, one per client connection
- **Connection pooling:** pgBouncer or Odyssey for high connection counts
- **Physical storage:** data in 8 KB pages, cached in shared_buffers
- **Logical:** Server -> Database -> Schema -> Objects (tables, indexes, views, functions)

## Transactions (ACID)

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob';
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100 WHERE name = 'Wally';
COMMIT;
```

### Isolation Levels

| Level | Dirty Read | Non-Repeatable | Phantom |
|-------|-----------|---------------|---------|
| Read Committed (default) | No | Possible | Possible |
| Repeatable Read | No | No | No* |
| Serializable | No | No | No |

*PostgreSQL's Repeatable Read also prevents phantoms (stricter than standard).

### MVCC
Each transaction works with a snapshot of data (transaction IDs define visibility).
- **Read Committed:** snapshot per statement
- **Repeatable Read:** snapshot per transaction

## PL/pgSQL

### Functions vs Procedures

| Feature | Function | Procedure |
|---------|----------|-----------|
| Transaction control | No | Yes |
| Use in SELECT | Yes | No |
| Call syntax | `SELECT func()` | `CALL proc()` |

### Triggers

```sql
CREATE OR REPLACE FUNCTION log_changes() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit (id, op) VALUES (NEW.id, 'INSERT');
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit (id, op) VALUES (NEW.id, 'UPDATE');
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit (id, op) VALUES (OLD.id, 'DELETE');
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_changes
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION log_changes();
```

## MERGE (PostgreSQL 15+)

```sql
MERGE INTO products AS p
USING product_updates AS u ON p.id = u.id
WHEN MATCHED THEN UPDATE SET name = u.name, price = u.price
WHEN NOT MATCHED THEN INSERT (id, name, price) VALUES (u.id, u.name, u.price)
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

For PostgreSQL < 15: `INSERT ... ON CONFLICT DO UPDATE`.

## Bulk Operations

```sql
COPY table_name FROM '/path/to/file.csv';
COPY (SELECT * FROM t) TO '/path/to/output.csv';
TRUNCATE TABLE employees;  -- fast clear (vs row-by-row DELETE)
```

## Physical JOIN Methods

| Method | Complexity | Requirement |
|--------|-----------|-------------|
| **Nested Loops** | O(M * N) | Universal |
| **Merge Join** | O(M + N) sorted | Equality, sorted data |
| **Hash Join** | O(N) | Equality, memory for hash table |

## Query Optimization

```sql
EXPLAIN ANALYZE SELECT * FROM bookings;
-- Shows: plan type, cost, actual time, rows, loops
```

### Plan Node Types
- Seq Scan, Index Scan, Index Only Scan
- Nested Loop / Merge Join / Hash Join
- HashAggregate, Sort, Gather (parallel)

### Statistics
```sql
SELECT reltuples, relpages FROM pg_class WHERE relname = 'bookings';
ANALYZE table_name;  -- update statistics
```

## Gotchas
- Empty string `''` is NOT NULL in PostgreSQL (unlike Oracle)
- DateStyle affects date parsing: always use ISO 8601 (`YYYY-MM-DD`)
- Arrays are 1-indexed in PostgreSQL
- `float` types: never use for money (rounding errors)
- UPDATE with FROM: if multiple matches, which row is used is unpredictable
- Cascade deletes are implicit - prefer explicit deletes
- In DWH, constraints often disabled for faster bulk loading

## See Also
- [[sql-for-de]] - SQL patterns and window functions
- [[data-modeling]] - normalization and schema design
- [[greenplum-mpp]] - PostgreSQL-based MPP
- [[docker-for-de]] - running PostgreSQL in Docker
