---
title: Joins and Set Operations
category: syntax
tags: [sql, join, inner-join, outer-join, cross-join, union, intersect, except]
---

# Joins and Set Operations

Joins combine rows from two or more tables based on related columns. Set operations combine result sets of two queries. Understanding join types, execution mechanics, and when to choose joins vs set operations is fundamental for SQL work.

## Key Facts

- **INNER JOIN** - returns only rows with matching values in both tables (default JOIN type)
- **LEFT JOIN** (LEFT OUTER JOIN) - returns all rows from left table plus matched rows from right; unmatched right-side columns become NULL
- **RIGHT JOIN** - mirror of LEFT JOIN; all rows from right table (rarely used - reorder tables and use LEFT JOIN instead)
- **FULL OUTER JOIN** - returns all rows from both tables; NULLs where no match. MySQL does NOT support FULL OUTER JOIN natively
- **CROSS JOIN** - cartesian product of both tables (every row x every row). No ON clause
- **SELF JOIN** - joining a table to itself; requires table aliases
- **LATERAL JOIN** (PostgreSQL) - subquery in FROM can reference columns from preceding tables. MySQL 8.0+ supports `LATERAL` keyword
- See [[select-fundamentals]] for WHERE clause filtering on joined results
- See [[indexes-and-btree]] for index strategies that speed up joins

## Patterns

### Join types in practice

```sql
-- INNER JOIN: orders with their customers
SELECT o.id, c.name, o.total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN: all customers, even without orders
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;

-- Anti-join: customers WITHOUT orders (LEFT JOIN + IS NULL)
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

-- Equivalent with NOT EXISTS (often same plan)
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- CROSS JOIN: generate combinations
SELECT colors.name, sizes.name
FROM colors CROSS JOIN sizes;

-- SELF JOIN: employee with their manager
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### LATERAL join (PostgreSQL, MySQL 8.0+)

```sql
-- Top 3 orders per customer using LATERAL
SELECT c.name, top_orders.*
FROM customers c
CROSS JOIN LATERAL (
    SELECT o.id, o.total
    FROM orders o
    WHERE o.customer_id = c.id
    ORDER BY o.total DESC
    LIMIT 3
) AS top_orders;
```

### Set operations

```sql
-- UNION: combine results, remove duplicates
SELECT email FROM customers
UNION
SELECT email FROM newsletter_subscribers;

-- UNION ALL: combine results, keep duplicates (faster - no dedup)
SELECT email FROM customers
UNION ALL
SELECT email FROM newsletter_subscribers;

-- INTERSECT: rows in both queries
SELECT email FROM customers
INTERSECT
SELECT email FROM newsletter_subscribers;

-- EXCEPT (MINUS in Oracle): rows in first but not second
SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers;
```

### FULL OUTER JOIN workaround for MySQL

```sql
-- MySQL doesn't support FULL OUTER JOIN, simulate with UNION
SELECT a.*, b.* FROM table_a a LEFT JOIN table_b b ON a.id = b.a_id
UNION
SELECT a.*, b.* FROM table_a a RIGHT JOIN table_b b ON a.id = b.a_id;
```

## Gotchas

- **JOIN on nullable columns** - `NULL = NULL` is NULL (not TRUE), so rows with NULLs in join columns won't match in INNER JOIN. Use `IS NOT DISTINCT FROM` in PostgreSQL for NULL-safe joins
- **Accidental CROSS JOIN** - forgetting the ON clause in INNER JOIN produces a cartesian product; can be catastrophic on large tables
- **Column ambiguity** - always alias tables and qualify column names in multi-table queries
- **Join order matters for LEFT JOIN** - `A LEFT JOIN B LEFT JOIN C` is different from `A LEFT JOIN (B LEFT JOIN C)` in terms of which NULLs propagate
- **UNION removes duplicates** - this requires a sort/hash operation; use UNION ALL when you know there are no duplicates or duplicates are acceptable
- **Set operations require matching column count and types** - the column names come from the first query

## See Also

- [[query-optimization-explain]] - how the optimizer chooses join algorithms (nested loop, hash, merge)
- [[common-table-expressions]] - using CTEs to structure complex multi-join queries
- [PostgreSQL JOIN docs](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [MySQL JOIN docs](https://dev.mysql.com/doc/refman/8.0/en/join.html)
