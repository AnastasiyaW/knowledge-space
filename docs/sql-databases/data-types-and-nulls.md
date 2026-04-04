---
title: Data Types and NULL Handling
category: concepts
tags: [sql-databases, sql, data-types, null, mysql, postgresql, varchar, integer, decimal, timestamp]
---

# Data Types and NULL Handling

Choosing correct data types affects storage, performance, and data integrity. NULL handling with three-valued logic is one of SQL's most subtle aspects.

## MySQL Data Types

### Numeric
| Type | Size | Range |
|------|------|-------|
| TINYINT | 1 byte | -128 to 127 (UNSIGNED: 0-255) |
| SMALLINT | 2 bytes | -32768 to 32767 |
| MEDIUMINT | 3 bytes | -8M to 8M |
| INT | 4 bytes | -2B to 2B |
| BIGINT | 8 bytes | -9.2E18 to 9.2E18 |
| DECIMAL(M,D) | variable | exact precision (for money) |
| FLOAT | 4 bytes | ~7 digits precision |
| DOUBLE | 8 bytes | ~15 digits precision |

### String
| Type | Max Size | Notes |
|------|----------|-------|
| CHAR(N) | 255 | fixed length, padded with spaces |
| VARCHAR(N) | 65,535 bytes | variable length, 1-2 bytes overhead |
| TEXT | 65 KB | |
| MEDIUMTEXT | 16 MB | |
| LONGTEXT | 4 GB | |
| ENUM | 1-2 bytes | one value from predefined list |

### Date/Time
| Type | Format | Notes |
|------|--------|-------|
| DATE | YYYY-MM-DD | |
| TIME | HH:MM:SS | |
| DATETIME | YYYY-MM-DD HH:MM:SS | 8 bytes, no timezone |
| TIMESTAMP | same format | 4 bytes, UTC conversion, range 1970-2038 |
| YEAR | YYYY | 1 byte |

## PostgreSQL Data Types

| Type | Notes |
|------|-------|
| SERIAL / BIGSERIAL | auto-incrementing integer (4/8 bytes) |
| INTEGER, BIGINT, SMALLINT | exact integers |
| NUMERIC(p,s) / DECIMAL | exact decimal |
| REAL, DOUBLE PRECISION | floating point |
| VARCHAR(n), TEXT | no performance difference in PG |
| CHAR(n) | fixed-length, rarely used |
| BOOLEAN | true/false/null |
| DATE, TIME, TIMESTAMP | standard date/time |
| TIMESTAMPTZ | timestamp with timezone (preferred) |
| INTERVAL | time duration |
| JSON / JSONB | native JSON (JSONB is binary, indexable) |
| UUID | 128-bit universally unique identifier |
| BYTEA | binary data |
| INET, CIDR | IP addresses |

## NULL Handling - Three-Valued Logic

NULL represents missing/unknown data. It is NOT a value itself.

```sql
-- Any comparison with NULL yields UNKNOWN
NULL = NULL    -- UNKNOWN (not TRUE)
NULL != 5      -- UNKNOWN (not TRUE)
NULL > 0       -- UNKNOWN

-- Correct NULL checks
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- COALESCE: first non-NULL argument
SELECT name, COALESCE(phone, 'No phone') FROM users;

-- NULLIF: returns NULL if arguments are equal
SELECT NULLIF(score, 0) FROM results;  -- avoid division by zero
```

## Key Facts

- NULL storage: 1-bit per nullable column in row's NULL bitmap
- `COUNT(*)` counts all rows; `COUNT(column)` excludes NULLs
- SUM, AVG, MIN, MAX all ignore NULLs
- GROUP BY treats all NULLs as one group
- NULLs in UNIQUE indexes: most RDBMS allow multiple NULLs; SQL Server does not by default
- PostgreSQL: no performance difference between VARCHAR(n) and TEXT
- Always use DECIMAL/NUMERIC for money - FLOAT/DOUBLE have rounding errors

## Common Functions

### String Functions
```sql
CONCAT(s1, s2)              -- concatenate (both)
LENGTH(s) / CHAR_LENGTH(s)  -- byte/character length
UPPER(s) / LOWER(s)         -- case conversion
TRIM(s) / LTRIM(s) / RTRIM(s)
SUBSTRING(s, pos, len)      -- extract substring
REPLACE(s, from, to)        -- replace occurrences
LEFT(s, n) / RIGHT(s, n)   -- first/last n characters
```

### Numeric Functions
```sql
ROUND(n, d)  -- round to d decimal places
CEIL(n)      -- round up
FLOOR(n)     -- round down
ABS(n)       -- absolute value
MOD(n, m)    -- modulo
```

### Date Functions
```sql
-- PostgreSQL
NOW(), CURRENT_DATE, CURRENT_TIMESTAMP
EXTRACT(YEAR FROM date_col)
AGE(timestamp1, timestamp2)         -- returns interval
date_col + INTERVAL '1 month'
TO_CHAR(date_col, 'YYYY-MM-DD')

-- MySQL
NOW(), CURDATE(), CURTIME()
YEAR(d) / MONTH(d) / DAY(d)
DATE_ADD(d, INTERVAL 1 DAY)
DATEDIFF(d1, d2)                    -- difference in days
TIMESTAMPDIFF(HOUR, d1, d2)
DATE_FORMAT(d, '%Y-%m-%d')
STR_TO_DATE(s, '%d/%m/%Y')
```

### Generated Columns (MySQL 8.0+, PostgreSQL 12+)

Computed columns stored or calculated on the fly:
```sql
-- MySQL: STORED (on disk) or VIRTUAL (computed at read)
CREATE TABLE users (
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(101) GENERATED ALWAYS AS (CONCAT(first_name, ' ', last_name)) STORED
);
-- Can index STORED generated columns
CREATE INDEX idx_fullname ON users (full_name);

-- PostgreSQL 12+: only STORED
ALTER TABLE users ADD COLUMN full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED;
```

### JSON Column Patterns

```sql
-- PostgreSQL JSONB: binary storage, indexable
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB NOT NULL
);

-- GIN index for containment queries
CREATE INDEX idx_payload ON events USING GIN (payload);

-- Query with operators
SELECT * FROM events WHERE payload @> '{"type": "click"}';         -- contains
SELECT * FROM events WHERE payload ->> 'user_id' = '42';           -- text extraction
SELECT * FROM events WHERE (payload -> 'meta' ->> 'score')::int > 90;  -- nested + cast

-- MySQL 8.0: JSON with generated column for indexing
ALTER TABLE events ADD COLUMN event_type VARCHAR(50)
    GENERATED ALWAYS AS (JSON_UNQUOTE(JSON_EXTRACT(payload, '$.type'))) STORED;
CREATE INDEX idx_event_type ON events (event_type);
```

### UUID as Primary Key

```sql
-- PostgreSQL: native UUID type
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);
-- Pro: no sequential guessing, safe for distributed systems
-- Con: larger than INT (16 bytes vs 4), random = fragmented B-tree inserts

-- UUIDv7 (time-sorted) available via extensions - preserves insert order
-- Better B-tree locality than UUIDv4
```

### Unexpected Type Coercions

```sql
-- MySQL silently truncates
INSERT INTO t (tinyint_col) VALUES (999);  -- stores 127 (max) with warning
-- PostgreSQL raises error for out-of-range

-- MySQL string-to-number coercion
SELECT * FROM users WHERE phone = 0;
-- Matches ALL rows where phone is a non-numeric string (coerced to 0)!
-- Always use: WHERE phone = '0'
```

## Gotchas

- MySQL `utf8` is 3-byte only (no emoji) - always use `utf8mb4`
- TIMESTAMP has a 2038 limit; use DATETIME or TIMESTAMPTZ for future-proof dates
- FLOAT arithmetic: `0.1 + 0.2 != 0.3` - use DECIMAL for exact comparisons
- PostgreSQL SERIAL is deprecated in favor of `GENERATED ALWAYS AS IDENTITY`
- NULL in NOT IN: if subquery returns any NULL, NOT IN returns empty result
- MySQL implicit type coercion: `WHERE varchar_col = 0` matches non-numeric strings - always quote string comparisons
- JSONB in PostgreSQL is ~30% larger than JSON but dramatically faster for queries - always prefer JSONB unless you need exact formatting preservation
- UUID primary keys cause B-tree page splits on random inserts - consider UUIDv7 (time-ordered) for better write performance
- Generated columns cannot reference other generated columns or use subqueries

## See Also

- [[ddl-schema-management]] - CREATE TABLE with data types
- [[schema-design-normalization]] - choosing types for schema design
- [[select-fundamentals]] - CASE expressions and computed fields
