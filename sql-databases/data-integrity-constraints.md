---
title: Data Integrity and Constraints
category: concepts
tags: [sql, constraints, primary-key, foreign-key, unique, check, not-null, normalization, postgresql, mysql]
---

# Data Integrity and Constraints

Constraints enforce data integrity rules at the database level. They prevent invalid data from being stored regardless of application bugs or direct SQL access. Proper constraint design is a cornerstone of reliable database schemas.

## Key Facts

- **PRIMARY KEY** = NOT NULL + UNIQUE. One per table. Defines the row identity. Creates an implicit index
- **FOREIGN KEY** references PRIMARY KEY (or UNIQUE) in another table. Enforces referential integrity
- **UNIQUE** constraint allows multiple NULLs by default in PostgreSQL (each NULL is distinct). MySQL also allows multiple NULLs in UNIQUE columns
- **CHECK** constraint validates column values against a boolean expression. PostgreSQL supports complex check expressions; MySQL 8.0.16+ supports CHECK (earlier versions parse but ignore)
- **NOT NULL** prevents NULL values. Applied at column level
- **EXCLUDE** constraint (PostgreSQL-only) prevents overlapping ranges. Uses GiST index
- See [[transactions-and-acid]] for how constraints relate to ACID Consistency
- See [[indexes-and-btree]] for indexes automatically created by constraints

## Patterns

### Constraint types

```sql
-- PRIMARY KEY
CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT NOT NULL
);

-- FOREIGN KEY with cascade
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    total NUMERIC(10,2) NOT NULL CHECK (total >= 0)
);

-- Named constraints (better error messages, easier to drop)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2),
    category TEXT,
    CONSTRAINT products_price_positive CHECK (price > 0),
    CONSTRAINT products_name_unique UNIQUE (name, category)
);

-- EXCLUDE constraint (PostgreSQL - no overlapping reservations)
CREATE TABLE reservations (
    room_id INT,
    during TSRANGE,
    EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);
```

### Foreign key actions

```sql
-- ON DELETE / ON UPDATE options:
-- CASCADE    - delete/update child rows automatically
-- SET NULL   - set FK column to NULL
-- SET DEFAULT - set FK column to default value
-- RESTRICT  - prevent parent deletion if children exist (immediate check)
-- NO ACTION - same as RESTRICT but checked at end of statement/transaction (default)

ALTER TABLE orders ADD CONSTRAINT fk_customer
    FOREIGN KEY (customer_id) REFERENCES customers(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;
```

### Deferrable constraints (PostgreSQL)

```sql
-- Deferrable: constraint checked at COMMIT instead of each statement
-- Useful for circular references or bulk loading
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    manager_id INT REFERENCES employees(id) DEFERRABLE INITIALLY DEFERRED
);

-- Temporarily defer constraints in a transaction
SET CONSTRAINTS ALL DEFERRED;
INSERT INTO departments (id, manager_id) VALUES (1, 10);
INSERT INTO employees (id, department_id) VALUES (10, 1);  -- circular ref OK
COMMIT;  -- both constraints checked here
```

### Normalization quick reference

```
1NF: Atomic values (no arrays/nested structures in columns, each row unique)
2NF: 1NF + every non-key column depends on entire primary key (no partial dependencies)
3NF: 2NF + no transitive dependencies (non-key depends on non-key)
BCNF: 3NF + every determinant is a candidate key

Practical rule: normalize to 3NF, denormalize intentionally for read performance
```

## Gotchas

- **Foreign key performance** - FK columns should ALWAYS be indexed. PostgreSQL does NOT auto-create indexes on FK columns (unlike the referenced PK). Without an index, cascading deletes cause full table scans on child table
- **MySQL CHECK ignored before 8.0.16** - MySQL parsed CHECK constraints but silently ignored them. Always verify your MySQL version supports actual enforcement
- **Cascading deletes** - CASCADE can delete unexpectedly large amounts of data. Use with caution and always understand the dependency graph
- **Deferred constraints** - only available in PostgreSQL. MySQL does not support deferred constraint checking
- **UNIQUE and NULL** - PostgreSQL: UNIQUE treats each NULL as distinct (multiple NULLs allowed). To prevent this: `CREATE UNIQUE INDEX ON table (col) WHERE col IS NOT NULL;`
- **Schema migration with constraints** - adding NOT NULL to existing column requires `ALTER TABLE ... SET NOT NULL` with a concurrent scan. For large tables, this can lock for a long time. Consider adding CHECK constraint first, then NOT NULL

## See Also

- [[transactions-and-acid]] - constraints as part of ACID Consistency guarantee
- [[schema-design-data-types]] - choosing appropriate data types for constrained columns
- [PostgreSQL constraints docs](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [MySQL CREATE TABLE / constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table.html)
