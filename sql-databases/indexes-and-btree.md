---
title: Indexes and B-Tree Internals
category: concepts
tags: [sql, index, btree, gin, gist, hash, covering-index, partial-index, postgresql, mysql]
---

# Indexes and B-Tree Internals

Indexes are data structures that speed up data retrieval at the cost of write overhead and storage space. B-tree is the default and most common index type. Understanding index internals, when they are used, and when they are NOT used is critical for query performance.

## Key Facts

- **B-tree** - default index type in both PostgreSQL and MySQL/InnoDB. Balanced tree with O(log n) lookups. Supports =, <, >, <=, >=, BETWEEN, IN, IS NULL, LIKE 'prefix%'
- **Hash index** - only supports equality (=). PostgreSQL: WAL-logged since v10 (safe). MySQL/InnoDB: not supported as user-created (memory engine only)
- **GIN** (Generalized Inverted Index) - PostgreSQL-specific. Optimal for full-text search, JSONB containment (`@>`, `?`, `?|`, `?&`), arrays, tsvector
- **GiST** (Generalized Search Tree) - PostgreSQL-specific. For geometric/spatial data, range types, full-text search (lossy but smaller than GIN)
- **BRIN** (Block Range Index) - PostgreSQL. Tiny index for physically sorted data (e.g., timestamp in append-only tables). Stores min/max per block range
- MySQL InnoDB uses **clustered index** on primary key - table data is physically stored in PK order. PostgreSQL heap tables are NOT clustered by default
- See [[query-optimization-explain]] for verifying index usage with EXPLAIN
- See [[postgresql-vacuum-and-mvcc]] for how dead tuples affect index bloat

## Patterns

### Creating indexes

```sql
-- Basic B-tree index
CREATE INDEX idx_users_email ON users (email);

-- Unique index (enforces uniqueness constraint)
CREATE UNIQUE INDEX idx_users_email_unique ON users (email);

-- Multi-column (composite) index
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date DESC);

-- Partial index (PostgreSQL) - index only matching rows
CREATE INDEX idx_orders_active ON orders (customer_id)
WHERE status = 'active';

-- Covering index (INCLUDE) - avoid heap lookup (index-only scan)
-- PostgreSQL 11+, MySQL 8.0+ (using INCLUDE in PG, covered by composite in MySQL)
CREATE INDEX idx_orders_cover ON orders (customer_id)
INCLUDE (order_date, total);

-- Expression index
CREATE INDEX idx_users_lower_email ON users (LOWER(email));

-- GIN index for JSONB
CREATE INDEX idx_products_attrs ON products USING GIN (attributes);

-- BRIN index for time-series
CREATE INDEX idx_events_ts ON events USING BRIN (created_at);
```

### MySQL InnoDB clustered index

```sql
-- InnoDB ALWAYS has a clustered index:
-- 1. PRIMARY KEY (explicitly defined)
-- 2. First UNIQUE NOT NULL index
-- 3. Hidden 6-byte auto-generated row ID

-- Secondary indexes in InnoDB store the PK value (not row pointer)
-- This means: secondary index lookup -> get PK -> PK lookup (double lookup)
-- Covering index avoids the second lookup:
CREATE INDEX idx_covering ON orders (status, customer_id, total);
-- Query using only columns in the index = "Using index" in EXPLAIN
```

### Composite index column order rules

```sql
-- "Leftmost prefix" rule: composite index (a, b, c) can be used for:
--   WHERE a = ?
--   WHERE a = ? AND b = ?
--   WHERE a = ? AND b = ? AND c = ?
--   WHERE a = ? ORDER BY b
-- CANNOT be used for:
--   WHERE b = ?              (skips leftmost column)
--   WHERE b = ? AND c = ?   (skips leftmost column)

-- Rule of thumb for column order:
-- 1. Equality conditions first (WHERE col = ?)
-- 2. Range conditions next (WHERE col > ?)
-- 3. Columns for ORDER BY last

-- Example: frequently filtered by status (equality) and sorted by date
CREATE INDEX idx_orders_status_date ON orders (status, order_date DESC);
```

## Gotchas

- **Index not used for LIKE '%suffix'** - B-tree can only use left-anchored patterns. For suffix search, use reverse() + expression index or GIN with pg_trgm
- **Too many indexes kill write performance** - every INSERT/UPDATE/DELETE must update all indexes. Monitor unused indexes with `pg_stat_user_indexes` (PostgreSQL)
- **NULL handling** - B-tree indexes include NULLs in PostgreSQL (can satisfy IS NULL queries). MySQL InnoDB also indexes NULLs. But: IS NOT NULL predicates often result in full scan if most rows are non-null
- **Index bloat** - in PostgreSQL, dead tuples from MVCC bloat indexes. REINDEX or pg_repack to reclaim. See [[postgresql-vacuum-and-mvcc]]
- **Selectivity matters** - indexes on low-cardinality columns (e.g., boolean, status with 3 values) may not be used because sequential scan is faster. Exception: partial indexes targeting rare values
- **MySQL: covering secondary index** - if query accesses only columns present in a secondary index, InnoDB avoids the clustered index lookup ("Using index" in EXPLAIN). Add frequently selected columns to composite index

## See Also

- [[query-optimization-explain]] - reading EXPLAIN output to verify index usage
- [[postgresql-vacuum-and-mvcc]] - VACUUM's role in maintaining index health
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [MySQL InnoDB index docs](https://dev.mysql.com/doc/refman/8.0/en/innodb-index-types.html)
