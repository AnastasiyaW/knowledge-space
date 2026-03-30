---
title: Stored Procedures, Functions, and Triggers
category: syntax
tags: [sql, stored-procedure, function, trigger, plpgsql, postgresql, mysql]
---

# Stored Procedures, Functions, and Triggers

Server-side code executed within the database engine. Functions return values, procedures execute actions (and can manage transactions in PostgreSQL 11+). Triggers fire automatically on DML events. These enable encapsulating business logic at the database level.

## Key Facts

- **Functions** return a value (scalar, table, or set). Called with SELECT or in expressions. PostgreSQL: PL/pgSQL, SQL, PL/Python, PL/Perl. MySQL: SQL only
- **Procedures** (PostgreSQL 11+, MySQL) - called with CALL. Can commit/rollback transactions within the procedure body. Cannot be used in SELECT
- **Triggers** - fire BEFORE/AFTER INSERT/UPDATE/DELETE on a table. Can modify the row (BEFORE triggers), audit changes, or enforce complex business rules
- **PL/pgSQL** - PostgreSQL's procedural language. Variables, IF/THEN, loops, exception handling, RAISE notices
- **Immutable/Stable/Volatile** (PostgreSQL) - function volatility categories. IMMUTABLE: always returns same result for same input (enables optimization). STABLE: reads but doesn't modify database. VOLATILE: default, may modify database
- See [[data-integrity-constraints]] for simpler alternatives to trigger-based validation
- See [[transactions-and-acid]] for transaction control in procedures

## Patterns

### PostgreSQL functions

```sql
-- Simple scalar function
CREATE OR REPLACE FUNCTION calculate_tax(amount NUMERIC, rate NUMERIC DEFAULT 0.20)
RETURNS NUMERIC
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    RETURN round(amount * rate, 2);
END;
$$;

SELECT calculate_tax(100.00);         -- 20.00
SELECT calculate_tax(100.00, 0.08);   -- 8.00

-- Table-returning function
CREATE OR REPLACE FUNCTION get_overdue_orders(days_overdue INT DEFAULT 30)
RETURNS TABLE(order_id BIGINT, customer_name TEXT, due_date DATE, days_late INT)
LANGUAGE sql
STABLE
AS $$
    SELECT o.id, c.name, o.due_date,
           (current_date - o.due_date)::INT
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE o.status = 'pending'
      AND o.due_date < current_date - days_overdue * INTERVAL '1 day';
$$;

SELECT * FROM get_overdue_orders(60);
```

### PostgreSQL procedures (PG 11+)

```sql
-- Procedure with transaction control
CREATE OR REPLACE PROCEDURE transfer_funds(
    sender_id BIGINT,
    receiver_id BIGINT,
    amount NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Debit sender
    UPDATE accounts SET balance = balance - amount WHERE id = sender_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Sender account % not found', sender_id;
    END IF;

    -- Credit receiver
    UPDATE accounts SET balance = balance + amount WHERE id = receiver_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Receiver account % not found', receiver_id;
    END IF;

    -- Can commit/rollback within procedure
    COMMIT;
END;
$$;

CALL transfer_funds(1, 2, 100.00);
```

### Triggers

```sql
-- PostgreSQL: audit trigger
CREATE OR REPLACE FUNCTION audit_trigger_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, new_data, changed_at)
        VALUES (TG_TABLE_NAME, 'INSERT', to_jsonb(NEW), now());
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, old_data, new_data, changed_at)
        VALUES (TG_TABLE_NAME, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), now());
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, old_data, changed_at)
        VALUES (TG_TABLE_NAME, 'DELETE', to_jsonb(OLD), now());
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER users_audit
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();

-- Updated_at trigger (very common pattern)
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_modified_column();
```

### MySQL stored procedures

```sql
DELIMITER //
CREATE PROCEDURE get_customer_orders(IN cust_id INT)
BEGIN
    SELECT o.id, o.total, o.status
    FROM orders o
    WHERE o.customer_id = cust_id
    ORDER BY o.created_at DESC;
END //
DELIMITER ;

CALL get_customer_orders(42);
```

## Gotchas

- **Trigger performance** - triggers add overhead to every DML operation. A trigger on a high-throughput table can significantly slow inserts. Audit triggers on busy tables should be lightweight (write to unlogged table or use logical decoding instead)
- **Function volatility misclassification** - marking a VOLATILE function as IMMUTABLE can cause wrong results (the optimizer may cache or pre-evaluate it). But marking IMMUTABLE correctly enables index use and plan caching
- **PL/pgSQL exception handling** - `EXCEPTION WHEN` blocks create a subtransaction (savepoint) for each call, which has performance cost. Don't use exceptions for flow control
- **MySQL trigger limitations** - MySQL allows only one trigger per event per timing (one BEFORE INSERT, one AFTER INSERT). Cannot use CALL in MySQL triggers (before 8.0)
- **Function in WHERE clause** - calling a volatile function in WHERE prevents index use. Mark functions IMMUTABLE/STABLE when appropriate
- **Recursive trigger loops** - a trigger on table A that modifies table B, which has a trigger modifying table A, creates infinite recursion. PostgreSQL limits recursion depth (default `max_stack_depth`)

## See Also

- [[data-integrity-constraints]] - prefer constraints over triggers for simple validation
- [[transactions-and-acid]] - transaction management in procedures
- [PostgreSQL PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL CREATE TRIGGER](https://www.postgresql.org/docs/current/sql-createtrigger.html)
- [MySQL stored procedures](https://dev.mysql.com/doc/refman/8.0/en/stored-routines.html)
