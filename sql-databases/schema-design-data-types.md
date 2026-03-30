---
title: Schema Design and Data Types
category: concepts
tags: [sql, data-types, schema, serial, identity, uuid, jsonb, array, enum, postgresql, mysql]
---

# Schema Design and Data Types

Choosing appropriate data types affects storage efficiency, query performance, data integrity, and application compatibility. PostgreSQL and MySQL offer different type systems with important differences.

## Key Facts

- **Integer types**: SMALLINT (2B), INTEGER (4B), BIGINT (8B). Use the smallest type that fits your data range
- **SERIAL vs IDENTITY** (PostgreSQL): SERIAL is legacy (creates a sequence + default). IDENTITY (SQL standard, PG 10+) is preferred: `GENERATED ALWAYS AS IDENTITY`
- **AUTO_INCREMENT** (MySQL): equivalent of SERIAL. Only one per table, must be part of a key
- **UUID**: 16 bytes, globally unique. PostgreSQL has native `uuid` type + `gen_random_uuid()` (PG 13+). MySQL stores as CHAR(36) or BINARY(16)
- **JSONB** (PostgreSQL): binary JSON with indexing support (GIN). Stores as decomposed binary, faster to query than JSON. MySQL has JSON type (similar but different indexing)
- **TEXT vs VARCHAR(n)**: in PostgreSQL, TEXT and VARCHAR have identical performance. VARCHAR(n) adds a length check. In MySQL, VARCHAR(255) vs VARCHAR(256) has storage implications (1 vs 2 bytes for length prefix)
- **NUMERIC/DECIMAL**: exact arithmetic for money. NEVER use FLOAT/DOUBLE for financial values
- See [[data-integrity-constraints]] for applying constraints to typed columns
- See [[indexes-and-btree]] for indexing considerations per data type

## Patterns

### PostgreSQL type choices

```sql
-- Primary key: prefer BIGINT IDENTITY for new projects
CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- Or UUID for distributed systems:
    -- id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',       -- array type
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'banned')),
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ENUM type (PostgreSQL)
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered');
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status order_status NOT NULL DEFAULT 'pending'
);

-- Range type (PostgreSQL)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name TEXT,
    during TSTZRANGE NOT NULL
);
```

### MySQL type choices

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    metadata JSON,                   -- MySQL JSON type
    status ENUM('active', 'inactive', 'banned') NOT NULL DEFAULT 'active',
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### JSONB operations (PostgreSQL)

```sql
-- Store and query JSON
INSERT INTO products (name, attrs)
VALUES ('Widget', '{"color": "red", "weight": 1.5, "tags": ["sale", "new"]}');

-- Access fields
SELECT attrs->>'color' AS color,                    -- text
       (attrs->>'weight')::numeric AS weight,        -- cast to numeric
       attrs->'tags' AS tags_json                    -- json
FROM products;

-- Containment query (uses GIN index)
SELECT * FROM products WHERE attrs @> '{"color": "red"}';

-- Path exists
SELECT * FROM products WHERE attrs ? 'weight';

-- Update JSONB field
UPDATE products SET attrs = attrs || '{"on_sale": true}'
WHERE id = 1;

-- Remove key
UPDATE products SET attrs = attrs - 'weight' WHERE id = 1;
```

### Timestamp considerations

```sql
-- PostgreSQL: ALWAYS use TIMESTAMPTZ (stores as UTC, converts on display)
-- TIMESTAMP WITHOUT TIME ZONE loses timezone info - subtle bugs

-- MySQL: TIMESTAMP auto-converts to UTC, DATETIME stores as-is
-- TIMESTAMP range: 1970-2038 (32-bit). DATETIME: 1000-9999 (no timezone)
-- For MySQL, DATETIME is usually safer for dates beyond 2038
```

## Gotchas

- **UUID as primary key** - random UUIDs cause B-tree index fragmentation (random inserts across all leaf pages). Use UUIDv7 (time-ordered) or ULID for better index locality. In MySQL InnoDB, random UUID PK is especially bad because data is physically sorted by PK
- **ENUM limitations** - PostgreSQL ENUM requires ALTER TYPE to add values (cannot remove/reorder). MySQL ENUM stores internally as integers; adding values requires table rebuild in older versions. Consider CHECK constraint + TEXT instead for flexibility
- **TEXT performance in MySQL** - MySQL TEXT/BLOB columns are stored off-page (overflow). VARCHAR is stored inline when possible. This makes TEXT slower for sorting and temporary tables
- **JSONB vs normalized columns** - JSONB is flexible but: no constraint enforcement on fields, no JOIN on JSONB fields without extraction, statistics are less accurate. Use for truly schema-less data, not to avoid schema design
- **Integer overflow** - SERIAL (INTEGER) maxes at 2.1B. For high-volume tables (events, logs), start with BIGINT
- **Character sets** - always use utf8mb4 in MySQL (utf8 is only 3 bytes, cannot store all Unicode). PostgreSQL uses UTF-8 by default

## See Also

- [[data-integrity-constraints]] - constraints on typed columns
- [[indexes-and-btree]] - indexing strategies for different data types
- [PostgreSQL data types](https://www.postgresql.org/docs/current/datatype.html)
- [MySQL data types](https://dev.mysql.com/doc/refman/8.0/en/data-types.html)
