---
title: DDL and Schema Management
category: concepts
tags: [sql-databases, sql, ddl, create-table, alter-table, constraints, foreign-key, primary-key]
---

# DDL and Schema Management

Data Definition Language (DDL) creates, modifies, and drops database objects. Proper DDL includes constraints that enforce data integrity at the database level.

## Key Facts

- DDL includes CREATE, ALTER, DROP, TRUNCATE
- PRIMARY KEY = unique + NOT NULL, creates clustered index in InnoDB
- FOREIGN KEY enforces referential integrity with CASCADE/RESTRICT/SET NULL actions
- MySQL `SERIAL` = `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`
- PostgreSQL `SERIAL` = auto-incrementing integer (prefer `GENERATED ALWAYS AS IDENTITY` in modern PG)
- ALTER TABLE lock behavior varies by operation - some block all reads, others allow concurrent DML

## Patterns

### CREATE TABLE
```sql
-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    age SMALLINT CHECK (age > 0),
    created_at TIMESTAMP DEFAULT NOW()
);

-- MySQL
CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100) COMMENT 'surname',
    phone BIGINT UNSIGNED UNIQUE,
    email VARCHAR(255),
    created_at DATETIME DEFAULT NOW(),
    INDEX idx_users_name(firstname, lastname)
) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Table Relationships
```sql
-- One-to-Many: FK in the many-side table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2)
);

-- One-to-One: PK as FK
CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    theme VARCHAR(20) DEFAULT 'light'
);

-- Many-to-Many: junction table
CREATE TABLE group_members (
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id),
    PRIMARY KEY (group_id, user_id)
);
```

### ALTER TABLE
```sql
ALTER TABLE users ADD COLUMN birthday DATE;
ALTER TABLE users ALTER COLUMN birthday SET NOT NULL;  -- PostgreSQL
ALTER TABLE users MODIFY COLUMN birthday DATE NOT NULL; -- MySQL
ALTER TABLE users RENAME COLUMN birthday TO date_of_birth;
ALTER TABLE users DROP COLUMN date_of_birth;

-- Add foreign key
ALTER TABLE orders ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

### Foreign Key Actions
```sql
ON DELETE CASCADE    -- delete children when parent deleted
ON DELETE RESTRICT   -- prevent parent deletion if children exist (default)
ON DELETE SET NULL   -- set FK to NULL when parent deleted
ON UPDATE CASCADE    -- update FK when parent PK changes
```

### DROP
```sql
DROP TABLE IF EXISTS temp_data;
DROP DATABASE IF EXISTS test_db;
```

### ENUM Types (MySQL)
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    media_type ENUM('text', 'image', 'audio', 'video'),
    status ENUM('sent', 'delivered', 'read')
);
-- ENUM stores as integer internally (1-2 bytes). Good for fixed lists.
```

## Gotchas

- ALTER TABLE ADD COLUMN in PostgreSQL acquires ACCESS EXCLUSIVE lock (blocks reads) for most operations
- MySQL `utf8` is only 3-byte UTF-8 (no emoji) - always use `utf8mb4`
- Adding NOT NULL column without DEFAULT fails if table has rows
- PostgreSQL 11+ handles ADD COLUMN with DEFAULT efficiently; pre-11 requires batch update approach
- MDL (Metadata Lock) in MySQL: DDL blocked until all active DML finishes, and new DML queues behind DDL

## See Also

- [[data-types-and-nulls]] - choosing appropriate data types
- [[schema-design-normalization]] - normalization and relationship patterns
- [[index-strategies]] - indexes created by constraints
- [[concurrency-and-locking]] - lock implications of DDL operations
