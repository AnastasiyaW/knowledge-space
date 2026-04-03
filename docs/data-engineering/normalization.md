---
title: Database Normalization
category: concepts
tags: [normalization, denormalization, 1nf, 2nf, 3nf, bcnf, normal-forms]
---

# Database Normalization

Normalization is the process of structuring a relational database to reduce data redundancy and improve data integrity. It applies a series of rules (normal forms) that progressively eliminate anomalies in INSERT, UPDATE, and DELETE operations.

## Key Facts

- **1NF (First Normal Form)**: each column holds atomic (indivisible) values; no repeating groups or arrays. Every row is uniquely identifiable
- **2NF (Second Normal Form)**: satisfies 1NF + every non-key attribute depends on the entire primary key (eliminates partial dependencies). Relevant only for composite keys
- **3NF (Third Normal Form)**: satisfies 2NF + no non-key attribute depends on another non-key attribute (eliminates transitive dependencies). The standard target for OLTP databases
- **BCNF (Boyce-Codd NF)**: stricter version of 3NF. Every determinant is a candidate key. Rarely needed in practice
- **Denormalization**: intentionally adding redundancy (duplicating columns, pre-computing aggregates) to speed up reads. Standard practice for [[data-warehouse]] and [[data-modeling]] (star/snowflake schemas)
- Trade-off: normalization reduces storage and anomalies but increases JOIN count; denormalization reduces JOINs but increases storage and update complexity

## Patterns

### Normalization progression example

```sql
-- UNNORMALIZED: repeating groups
-- order_id | customer | items
-- 1        | Alice    | "Widget:3, Gadget:1"

-- 1NF: atomic values, separate rows
CREATE TABLE orders_1nf (
    order_id    INT,
    customer    VARCHAR(100),
    item_name   VARCHAR(100),
    quantity    INT,
    PRIMARY KEY (order_id, item_name)
);

-- 2NF: remove partial dependency (customer depends only on order_id)
CREATE TABLE orders_2nf (
    order_id    INT PRIMARY KEY,
    customer    VARCHAR(100)
);
CREATE TABLE order_items_2nf (
    order_id    INT REFERENCES orders_2nf,
    item_name   VARCHAR(100),
    quantity    INT,
    PRIMARY KEY (order_id, item_name)
);

-- 3NF: remove transitive dependency
-- if customer -> customer_city, extract customer table
CREATE TABLE customers_3nf (
    customer_id   SERIAL PRIMARY KEY,
    name          VARCHAR(100),
    city          VARCHAR(100)
);
```

### When to denormalize

```
OLTP (3NF)                    OLAP (Denormalized)
+-----------+                 +------------------+
| customers |---+             | fact_sales       |
+-----------+   |             |   customer_name  |  <-- duplicated
| orders    |---+             |   product_name   |  <-- duplicated
+-----------+   |             |   revenue        |
| products  |---+             |   order_date     |
+-----------+                 +------------------+
Many JOINs, low redundancy    Few JOINs, high redundancy
```

## Gotchas

- Do not normalize a data warehouse into 3NF. [[data-modeling]] uses denormalized star schemas for a reason: analytical queries scan millions of rows, and JOINs are expensive at scale
- 2NF only matters when you have composite primary keys. With surrogate single-column PKs, 1NF -> 3NF is the practical path
- Over-normalization (4NF, 5NF) adds complexity without practical benefit for most applications. 3NF/BCNF is sufficient
- Denormalization requires maintaining consistency on updates. Use triggers, materialized views, or [[etl-and-elt]] pipelines to keep denormalized copies in sync

## See Also

- [[data-modeling]] - dimensional modeling (denormalized by design)
- [[postgresql-for-data-engineering]] - implementing normalized schemas
- https://en.wikipedia.org/wiki/Database_normalization - theory reference
