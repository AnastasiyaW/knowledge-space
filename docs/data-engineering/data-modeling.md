---
title: Data Modeling and Normalization
category: concepts
tags: [data-engineering, data-modeling, normalization, er-diagrams, database-design]
---

# Data Modeling and Normalization

Data modeling is the process of analyzing requirements and creating data structures. Three stages: conceptual (business entities), logical (ER diagrams with attributes/keys), physical (DDL scripts with indexes/partitions). Normalization eliminates redundancy through functional dependencies.

## Normal Forms

**Mnemonic:** "Data depends on the key [1NF], the whole key [2NF], and nothing but the key [3NF]."

### First Normal Form (1NF)
- All values are **atomic** (no arrays, no composite values)
- No duplicate rows
- Has a primary key

### Second Normal Form (2NF)
- Satisfies 1NF
- Every non-key attribute depends on the **entire** primary key
- Only relevant for composite keys - if PK is simple, 2NF is automatic

### Third Normal Form (3NF)
- Satisfies 2NF
- No **transitive dependencies**: non-key A depends on non-key B which depends on PK
- **Fix:** extract the transitively dependent group into a separate table

### Beyond 3NF
- **BCNF, 4NF, 5NF** - rarely needed in practice
- **6NF** - extreme decomposition, one attribute per table. Used in [[data-vault#anchor-modeling|anchor modeling]]

## Functional Dependencies

`{X} -> {Y}` means: if two tuples agree on X, they must agree on Y. Each X value determines exactly one Y value.

### Anomalies (When Normalization is Insufficient)

| Anomaly | Problem |
|---------|---------|
| **Update** | Changing info requires updating ALL rows containing that entity |
| **Delete** | Deleting last related row loses the entity data entirely |
| **Insert** | Cannot insert an entity that has no related records yet |

## Keys

| Key Type | Definition |
|----------|-----------|
| **Candidate key** | Unique + irreducible subset of attributes |
| **Primary key** | Chosen candidate key |
| **Alternative key** | Non-chosen candidate keys |
| **Surrogate key** | System-generated ID (auto-increment, UUID) |
| **Natural key** | Business attribute (email, SSN) |
| **Composite key** | Multiple attributes forming a candidate key |

**Prefer surrogate keys** when multiple candidates exist or natural key may change.

## ER Diagrams

### Cardinality Types

| Type | Implementation |
|------|---------------|
| **1:1** | FK with UNIQUE constraint |
| **1:M** | FK in the "many" table |
| **M:M** | Junction table with FKs to both |

### Notations

**Martin (Crow's Foot)** - most practical, expected in interviews:
- Rectangles = entities with attributes listed inside
- Crow's foot (fork) = "many", single line = "one"
- Circle = "zero" (optional), dash = "one" (mandatory)

**Chen Notation** - academic: rectangles (entities), diamonds (relationships), ovals (attributes)

## Normalization vs Denormalization

| Criterion | Normalized (3NF) | Denormalized |
|-----------|------------------|-------------|
| Data integrity | Better (no anomalies) | Worse |
| INSERT/UPDATE/DELETE | Faster (smaller tables) | Slower |
| SELECT (reads) | Slower (many JOINs) | Faster (wide tables) |
| Best for | OLTP (write integrity) | OLAP (read speed, marts) |

## Deduplication Patterns

```sql
-- Method 1: CTE + ROW_NUMBER (most common)
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY key_col1, key_col2
        ORDER BY load_date DESC
    ) AS rn
    FROM source_table
)
SELECT * FROM ranked WHERE rn = 1;

-- Method 2: QUALIFY (Snowflake, BigQuery, DuckDB)
SELECT * FROM source_table
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY key_col1, key_col2
    ORDER BY load_date DESC
) = 1;

-- Method 3: DISTINCT ON (PostgreSQL only)
SELECT DISTINCT ON (key_col1, key_col2) *
FROM source_table
ORDER BY key_col1, key_col2, load_date DESC;
```

## Gotchas
- Relations (mathematical) have no duplicate tuples and no ordering. Tables (physical) can violate both
- A relation is automatically in 1NF by definition (set theory). Tables need explicit checking
- In DWH, constraints (PK, FK) are often disabled for faster bulk loading
- Most production DWHs are hybrids - Data Vault or 3NF in core, dimensional in marts

## See Also
- [[dimensional-modeling]] - star/snowflake schemas
- [[data-vault]] - Hub/Link/Satellite methodology
- [[dwh-architecture]] - where models are applied
- [[sql-for-de]] - SQL implementation of models
