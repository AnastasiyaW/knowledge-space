---
title: DML - INSERT, UPDATE, DELETE
category: concepts
tags: [sql-databases, sql, insert, update, delete, truncate, dml, bulk-operations]
---

# DML - INSERT, UPDATE, DELETE

Data Manipulation Language (DML) statements modify table data. Understanding their behavior, performance characteristics, and transaction implications is critical for production systems.

## Key Facts

- INSERT, UPDATE, DELETE are transactional (can be rolled back)
- TRUNCATE is DDL in most RDBMS - faster than DELETE but cannot be rolled back (MySQL) or is transactional (PostgreSQL)
- Multi-row INSERT is significantly faster than individual INSERT statements
- UPDATE rewrites entire row in PostgreSQL (MVCC); InnoDB modifies in-place if possible
- DELETE only marks rows for removal - space reclaimed by VACUUM (PostgreSQL) or background purge (InnoDB)

## Patterns

### INSERT
```sql
-- Single row
INSERT INTO users (firstname, lastname, email) VALUES ('Alice', 'Smith', 'alice@example.com');

-- Multi-row (much faster than individual inserts)
INSERT INTO users (firstname, lastname) VALUES ('Bob', 'Jones'), ('Carol', 'Lee');

-- INSERT from SELECT
INSERT INTO archive_orders SELECT * FROM orders WHERE created_at < '2023-01-01';

-- INSERT with RETURNING (PostgreSQL)
INSERT INTO users (name, email) VALUES ('Dave', 'dave@example.com') RETURNING id, created_at;

-- UPSERT: INSERT ... ON CONFLICT (PostgreSQL)
INSERT INTO users (email, name) VALUES ('bob@example.com', 'Bob')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- UPSERT: INSERT ... ON DUPLICATE KEY UPDATE (MySQL)
INSERT INTO users (email, name) VALUES ('bob@example.com', 'Bob')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

### UPDATE
```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
UPDATE users SET firstname = 'New', lastname = 'Name' WHERE id = 5;

-- Batch update with calculated values
UPDATE orders SET total = quantity * unit_price WHERE total IS NULL;

-- UPDATE from another table (PostgreSQL)
UPDATE orders o SET status = 'archived'
FROM users u WHERE o.user_id = u.id AND u.deleted = true;
```

### DELETE
```sql
DELETE FROM users WHERE id = 1;
DELETE FROM orders WHERE created_at < '2020-01-01';

-- Delete with subquery
DELETE FROM album WHERE band_id IN (SELECT id FROM band WHERE country = 'DE');
```

### TRUNCATE
```sql
TRUNCATE TABLE users;              -- fast delete all rows
TRUNCATE TABLE users RESTART IDENTITY;  -- reset auto_increment (PostgreSQL)
-- MySQL: TRUNCATE always resets AUTO_INCREMENT
```

### Batch Operations for Large Tables
```sql
-- Avoid updating millions of rows at once - batch in chunks
UPDATE users SET status = 'inactive'
WHERE id IN (SELECT id FROM users WHERE last_login < '2023-01-01' LIMIT 10000);
-- Repeat until no rows affected, VACUUM between batches (PostgreSQL)
```

### CREATE TABLE AS SELECT
```sql
CREATE TABLE rock_albums AS SELECT * FROM album WHERE genre = 'rock';
```

## Gotchas

- TRUNCATE cannot be rolled back in MySQL (it's DDL); PostgreSQL TRUNCATE is transactional
- Large DELETE/UPDATE operations can cause lock contention and bloat - batch them
- PostgreSQL UPDATE creates a new row version (dead tuple) - requires VACUUM to reclaim
- Adding column with DEFAULT on large table before PG 11 requires batch update approach
- Always include WHERE on UPDATE/DELETE in production - missing WHERE affects all rows
- Foreign key CASCADE can cause unexpected mass deletions

## See Also

- [[ddl-schema-management]] - CREATE TABLE, ALTER TABLE, constraints
- [[transactions-and-acid]] - wrapping DML in transactions
- [[postgresql-mvcc-vacuum]] - dead tuples from UPDATE/DELETE
- [[data-types-and-nulls]] - data types for INSERT values
