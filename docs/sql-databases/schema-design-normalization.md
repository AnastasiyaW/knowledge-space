---
title: Schema Design and Normalization
category: concepts
tags: [sql-databases, schema-design, normalization, 1nf, 2nf, 3nf, denormalization, primary-key, foreign-key]
---

# Schema Design and Normalization

Good schema design balances data integrity (normalization) with read performance (denormalization). The choice impacts every query, join, and index in the system.

## Normal Forms

**1NF (First Normal Form):** Each column contains atomic values (no arrays/lists). Each row unique (has primary key). No repeating groups.

**2NF:** 1NF + every non-key column depends on the entire primary key (not partial). Eliminates partial dependencies from composite keys.

**3NF:** 2NF + no transitive dependencies (non-key column depending on another non-key). Example: if city has country_code, don't also store country_name.

**Practical guideline:** Normalize until queries become too complex or slow, then strategically denormalize. OLTP systems benefit from normalization; OLAP/reporting tolerates more denormalization.

## Key Facts

- Normalization reduces redundancy and enforces integrity through foreign keys
- Denormalization trades integrity for read performance (pre-computed joins, materialized views)
- One-to-One: PK as FK, or unique FK
- One-to-Many: FK on the "many" side
- Many-to-Many: requires junction table with composite PK
- Choose smallest sufficient data types - affects index size, cache efficiency, I/O

## Primary Key Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| Auto-increment (SERIAL) | Ordered, compact, great for clustered index | Leaks count, not for distributed systems |
| UUID v4 | Globally unique, no coordination | Random = bad for indexes (page splits) |
| UUID v7 / ULID | Time-ordered + unique, distributed-friendly | Wider than integer (16 bytes) |

## Patterns

### Typical Application Schema (Telegram Clone)
```sql
-- Users with settings (1:1)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone BIGINT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_settings (
    user_id BIGINT PRIMARY KEY REFERENCES users(id),
    theme VARCHAR(20) DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'en'
);

-- Messages with self-referencing reply chain
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    sender_id BIGINT NOT NULL REFERENCES users(id),
    receiver_id BIGINT NOT NULL REFERENCES users(id),
    reply_to_id BIGINT REFERENCES messages(id),
    body TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Groups with members (M:M)
CREATE TABLE groups (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    owner_id BIGINT REFERENCES users(id)
);

CREATE TABLE group_members (
    group_id BIGINT REFERENCES groups(id),
    user_id BIGINT REFERENCES users(id),
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (group_id, user_id)
);
```

### Denormalization Patterns
```sql
-- Materialized count: avoid COUNT(*) on large tables
ALTER TABLE users ADD COLUMN order_count INTEGER DEFAULT 0;
-- Update via trigger or application logic

-- Pre-computed join: store derived data
ALTER TABLE orders ADD COLUMN user_name VARCHAR(100);
-- Trade-off: faster reads, complex update logic
```

### Design Anti-Pattern: Embedding Lists
```sql
-- BAD: storing comma-separated values
CREATE TABLE users (id INT, hobbies TEXT);  -- hobbies = 'chess,reading,hiking'

-- GOOD: separate table for many-to-many
CREATE TABLE hobbies (id SERIAL PRIMARY KEY, name VARCHAR(50));
CREATE TABLE user_hobbies (user_id INT REFERENCES users(id), hobby_id INT REFERENCES hobbies(id));
```

## Gotchas

- Over-normalization causes excessive JOINs - denormalize hot paths strategically
- ENUM values are hard to modify later; consider a lookup/reference table instead
- Column order in PostgreSQL affects byte alignment - group same-size types together
- Auto-increment PKs leak business information (order count, growth rate)
- Missing indexes on FK columns is a common performance killer

## See Also

- [[ddl-schema-management]] - CREATE TABLE syntax and constraints
- [[data-types-and-nulls]] - choosing appropriate data types
- [[partitioning-and-sharding]] - scaling large tables
- [[btree-and-index-internals]] - UUID impact on index performance
