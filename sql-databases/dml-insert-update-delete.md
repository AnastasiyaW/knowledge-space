---
title: DML - INSERT, UPDATE, DELETE, UPSERT
category: syntax
tags: [sql, insert, update, delete, upsert, on-conflict, merge, returning, bulk, postgresql, mysql]
---

# DML - INSERT, UPDATE, DELETE, UPSERT

Data Manipulation Language operations modify table data. Beyond basic syntax, understanding UPSERT patterns, bulk operations, RETURNING clause, and safe UPDATE/DELETE practices is essential for production work.

## Key Facts

- **INSERT ... RETURNING** (PostgreSQL) - returns inserted rows including generated values (IDs, defaults). MySQL equivalent: `LAST_INSERT_ID()`
- **UPSERT** - INSERT or UPDATE if exists. PostgreSQL: `INSERT ... ON CONFLICT ... DO UPDATE`. MySQL: `INSERT ... ON DUPLICATE KEY UPDATE`
- **MERGE** (SQL standard) - combined INSERT/UPDATE/DELETE in one statement. PostgreSQL 15+ supports MERGE. MySQL does not
- **UPDATE ... FROM** (PostgreSQL) - join another table in UPDATE. MySQL uses multi-table UPDATE syntax
- **DELETE with JOIN** - PostgreSQL: `DELETE ... USING`. MySQL: `DELETE t1 FROM t1 JOIN t2 ...`
- **Bulk INSERT** performance - multi-row VALUES is much faster than single-row inserts. COPY (PostgreSQL) or LOAD DATA (MySQL) is fastest for large loads
- See [[transactions-and-acid]] for wrapping DML in transactions
- See [[data-integrity-constraints]] for constraint violations during DML

## Patterns

### INSERT variations

```sql
-- Basic insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Multi-row insert (much faster than individual inserts)
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com');

-- INSERT from SELECT
INSERT INTO user_archive (id, name, email, archived_at)
SELECT id, name, email, now() FROM users WHERE status = 'deleted';

-- RETURNING (PostgreSQL) - get generated values
INSERT INTO orders (customer_id, total)
VALUES (1, 99.99)
RETURNING id, created_at;
```

### UPSERT (INSERT or UPDATE)

```sql
-- PostgreSQL: ON CONFLICT
INSERT INTO product_inventory (product_id, quantity)
VALUES (42, 10)
ON CONFLICT (product_id)
DO UPDATE SET quantity = product_inventory.quantity + EXCLUDED.quantity;

-- ON CONFLICT DO NOTHING (skip if exists)
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email) DO NOTHING;

-- MySQL: ON DUPLICATE KEY UPDATE
INSERT INTO product_inventory (product_id, quantity)
VALUES (42, 10)
ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity);

-- PostgreSQL 15+: MERGE
MERGE INTO product_inventory t
USING (VALUES (42, 10)) AS s(product_id, quantity)
ON t.product_id = s.product_id
WHEN MATCHED THEN
    UPDATE SET quantity = t.quantity + s.quantity
WHEN NOT MATCHED THEN
    INSERT (product_id, quantity) VALUES (s.product_id, s.quantity);
```

### UPDATE patterns

```sql
-- Basic UPDATE
UPDATE users SET status = 'inactive', updated_at = now()
WHERE last_login < now() - INTERVAL '1 year';

-- UPDATE with JOIN (PostgreSQL)
UPDATE orders SET status = 'vip_order'
FROM customers c
WHERE orders.customer_id = c.id AND c.tier = 'vip';

-- UPDATE with JOIN (MySQL)
UPDATE orders o
JOIN customers c ON o.customer_id = c.id
SET o.status = 'vip_order'
WHERE c.tier = 'vip';

-- UPDATE RETURNING (PostgreSQL)
UPDATE products SET price = price * 1.1
WHERE category = 'premium'
RETURNING id, name, price AS new_price;

-- Conditional UPDATE with CASE
UPDATE employees SET
    bonus = CASE
        WHEN rating >= 4.5 THEN salary * 0.20
        WHEN rating >= 3.5 THEN salary * 0.10
        ELSE salary * 0.05
    END
WHERE department = 'engineering';
```

### DELETE patterns

```sql
-- Basic DELETE
DELETE FROM sessions WHERE expires_at < now();

-- DELETE with JOIN (PostgreSQL: USING)
DELETE FROM order_items
USING orders
WHERE order_items.order_id = orders.id AND orders.status = 'cancelled';

-- DELETE with RETURNING (PostgreSQL)
DELETE FROM expired_tokens
WHERE expires_at < now()
RETURNING token_id, user_id;

-- TRUNCATE (fastest way to empty a table, non-transactional in some cases)
TRUNCATE TABLE sessions;
TRUNCATE TABLE orders CASCADE;  -- also truncates referencing tables
```

### Bulk loading (fastest)

```sql
-- PostgreSQL COPY (fastest import method)
COPY users (name, email) FROM '/path/to/file.csv' WITH (FORMAT csv, HEADER true);
-- From stdin (psql)
\copy users (name, email) FROM 'file.csv' CSV HEADER

-- MySQL LOAD DATA (fastest import method)
LOAD DATA INFILE '/path/to/file.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(name, email);
```

## Gotchas

- **UPDATE without WHERE** - updates ALL rows. Always double-check WHERE clause before executing. Use `BEGIN; UPDATE ...; SELECT count(*); ROLLBACK;` to verify scope
- **DELETE without WHERE** - deletes ALL rows. Same precaution applies
- **UPSERT race conditions** - `ON CONFLICT` in PostgreSQL is atomic within a single statement. But check for unique constraint violations when using in concurrent environments without explicit locking
- **RETURNING not available in MySQL** - MySQL has no RETURNING clause. Use `LAST_INSERT_ID()` for auto-increment values only
- **TRUNCATE vs DELETE** - TRUNCATE is DDL (not DML), resets sequences, cannot have WHERE clause, may not fire triggers, and cannot be rolled back in MySQL (can in PostgreSQL)
- **COPY requires superuser or pg_read_server_files** - for server-side COPY. Use `\copy` in psql for client-side file loading

## See Also

- [[transactions-and-acid]] - transactional DML guarantees
- [[data-integrity-constraints]] - handling constraint violations in DML
- [PostgreSQL INSERT docs](https://www.postgresql.org/docs/current/sql-insert.html)
- [MySQL INSERT docs](https://dev.mysql.com/doc/refman/8.0/en/insert.html)
