---
title: SELECT Fundamentals and Clause Ordering
category: syntax
tags: [sql, select, where, group-by, having, order-by, limit, distinct]
---

# SELECT Fundamentals and Clause Ordering

The SELECT statement is the primary data retrieval mechanism in SQL. Understanding the logical execution order of its clauses (which differs from the written order) is critical for writing correct queries and debugging unexpected results.

## Key Facts

- Written order: `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT`
- Logical execution order: `FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT/OFFSET`
- Because SELECT is evaluated after GROUP BY, you cannot use column aliases in WHERE or GROUP BY (PostgreSQL exception: you can use aliases in ORDER BY)
- `DISTINCT` eliminates duplicate rows from the result set AFTER SELECT evaluation
- `NULL` comparisons require `IS NULL` / `IS NOT NULL` - standard comparison operators return NULL (not true/false) when comparing with NULL
- PostgreSQL supports `DISTINCT ON (expression)` which keeps the first row per distinct group - not available in MySQL
- See [[joins-and-set-operations]] for combining data from multiple tables
- See [[query-optimization-explain]] for analyzing SELECT performance

## Patterns

### Logical execution order (critical for debugging)

```sql
-- This FAILS because WHERE runs before SELECT (alias not yet available)
SELECT price * quantity AS total
FROM orders
WHERE total > 100;  -- ERROR: column "total" does not exist

-- Correct: repeat the expression or use a subquery/CTE
SELECT price * quantity AS total
FROM orders
WHERE price * quantity > 100;

-- Or use CTE (see [[common-table-expressions]])
WITH calculated AS (
    SELECT *, price * quantity AS total FROM orders
)
SELECT * FROM calculated WHERE total > 100;
```

### Filtering patterns

```sql
-- IN vs multiple OR (equivalent, IN is cleaner)
SELECT * FROM users WHERE status IN ('active', 'pending', 'trial');

-- BETWEEN is inclusive on both ends
SELECT * FROM events WHERE event_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Pattern matching
SELECT * FROM products WHERE name LIKE '%widget%';      -- case-sensitive
SELECT * FROM products WHERE name ILIKE '%widget%';      -- PostgreSQL: case-insensitive
SELECT * FROM products WHERE name LIKE 'A___';           -- exactly 4 chars starting with A

-- NULL-safe comparison (PostgreSQL)
SELECT * FROM users WHERE email IS DISTINCT FROM 'test@example.com';  -- treats NULL != value as TRUE
```

### GROUP BY with HAVING

```sql
-- HAVING filters groups, WHERE filters rows before grouping
SELECT department, COUNT(*) AS emp_count, AVG(salary) AS avg_salary
FROM employees
WHERE hire_date >= '2020-01-01'       -- filters ROWS
GROUP BY department
HAVING COUNT(*) >= 5                   -- filters GROUPS
ORDER BY avg_salary DESC;

-- PostgreSQL: GROUP BY with ROLLUP for subtotals
SELECT department, job_title, SUM(salary) AS total
FROM employees
GROUP BY ROLLUP (department, job_title);
```

### LIMIT/OFFSET pagination

```sql
-- Basic pagination (page 3, 20 items per page)
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 40;

-- Keyset pagination (much faster for large offsets)
SELECT * FROM products
WHERE id > 1000                  -- last seen id from previous page
ORDER BY id LIMIT 20;

-- MySQL uses same LIMIT syntax; alternative form:
-- SELECT * FROM products LIMIT 40, 20;  -- LIMIT offset, count
```

## Gotchas

- **ORDER BY is not guaranteed without explicit clause** - even if results seem ordered, the database engine is free to return rows in any order
- **OFFSET performance degrades linearly** - `OFFSET 1000000` still scans 1M rows; use keyset pagination for large datasets
- **GROUP BY requires all non-aggregate columns** - unlike MySQL with `ONLY_FULL_GROUP_BY` disabled, PostgreSQL strictly requires every non-aggregated column in GROUP BY
- **DISTINCT applies to entire row** - `SELECT DISTINCT a, b` deduplicates on the combination of a AND b, not just a
- **NULL sorting differs** - PostgreSQL sorts NULLs last in ASC (first in DESC) by default; use `NULLS FIRST` / `NULLS LAST` to control

## See Also

- [[common-table-expressions]] - CTEs and WITH clause for readable queries
- [[subqueries-and-derived-tables]] - Subqueries in SELECT, FROM, WHERE
- [PostgreSQL SELECT docs](https://www.postgresql.org/docs/current/sql-select.html)
- [MySQL SELECT docs](https://dev.mysql.com/doc/refman/8.0/en/select.html)
