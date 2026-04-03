---
title: Subqueries and Common Table Expressions
category: concepts
tags: [sql-databases, subqueries, cte, derived-tables, exists]
---

# Subqueries and Common Table Expressions

Subqueries are queries nested within other queries. CTEs (Common Table Expressions) provide named temporary result sets for improved readability. Both are essential for breaking complex logic into manageable pieces.

## Scalar Subqueries

Return a single value. Used in SELECT list, WHERE clause, or anywhere a single value is expected.

```sql
-- In WHERE
SELECT * FROM album WHERE year = (SELECT MAX(year) FROM album);

-- In SELECT (correlated)
SELECT u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;
```

## Table Subqueries (IN / NOT IN)

Return a set of values for membership testing.

```sql
-- Users who sent messages
SELECT * FROM users WHERE id IN (
    SELECT DISTINCT sender_id FROM private_messages
);

-- Users who did NOT send messages
SELECT * FROM users WHERE id NOT IN (
    SELECT DISTINCT sender_id FROM private_messages
    WHERE sender_id IS NOT NULL  -- CRITICAL: prevent NULL trap
);
```

**NOT IN with NULL trap**: If the subquery returns ANY NULL value, `NOT IN` returns empty result for ALL rows. Always add `WHERE column IS NOT NULL` inside the subquery, or use NOT EXISTS instead.

## EXISTS / NOT EXISTS

Tests for the existence of rows. More efficient than IN for large subqueries because it stops at first match.

```sql
-- Users with at least one message
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM private_messages pm WHERE pm.sender_id = u.id
);

-- Users without messages (safer than NOT IN)
SELECT * FROM users u WHERE NOT EXISTS (
    SELECT 1 FROM private_messages pm WHERE pm.sender_id = u.id
);
```

## Derived Tables (Subquery in FROM)

```sql
SELECT avg_amount FROM (
    SELECT user_id, AVG(amount) AS avg_amount
    FROM orders
    GROUP BY user_id
) AS user_avgs
WHERE avg_amount > 500;
```

## Common Table Expressions (CTE)

Named temporary result sets defined with WITH clause. Improve readability for complex queries.

```sql
WITH active_users AS (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    WHERE created_at > '2024-01-01'
    GROUP BY user_id
),
high_value AS (
    SELECT user_id, SUM(amount) AS total
    FROM orders
    GROUP BY user_id
    HAVING total > 10000
)
SELECT u.*, au.order_count, hv.total
FROM users u
JOIN active_users au ON u.id = au.user_id
JOIN high_value hv ON u.id = hv.user_id;
```

### Recursive CTEs

For hierarchical or graph-like data traversal:

```sql
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    -- Recursive case: subordinates
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

## Patterns

### CTE Materialization

PostgreSQL 12+ allows optimizer to inline CTEs (previously always materialized). Use `MATERIALIZED` / `NOT MATERIALIZED` hints:

```sql
WITH cached_data AS MATERIALIZED (
    SELECT * FROM expensive_view
)
SELECT * FROM cached_data WHERE id = 42;
```

### Correlated vs Non-Correlated Subqueries

Non-correlated subqueries execute once. Correlated subqueries execute once per outer row - can be slow on large datasets. Rewrite as JOINs when possible:

```sql
-- Slow: correlated subquery (executes per row)
SELECT * FROM users u
WHERE (SELECT MAX(amount) FROM orders WHERE user_id = u.id) > 1000;

-- Faster: JOIN approach
SELECT u.* FROM users u
JOIN (SELECT user_id, MAX(amount) AS max_amt FROM orders GROUP BY user_id) o
ON u.id = o.user_id
WHERE o.max_amt > 1000;
```

## Gotchas

- NOT IN with NULLs silently returns empty results - prefer NOT EXISTS
- Correlated subqueries in SELECT list run once per row - use JOINs for large datasets
- CTEs in MySQL were always materialized until 8.0.14; check your version
- Recursive CTEs without proper termination condition cause infinite loops - use LIMIT or depth counter as safety
- `log_temp_files` in PostgreSQL helps detect queries with runaway temporary file generation from infinite recursive CTEs

## See Also

- [[joins-and-set-operations]] - JOINs as alternative to subqueries
- [[window-functions]] - analytics without collapsing rows
- [[select-fundamentals]] - base query structure
- [[query-optimization-explain]] - comparing subquery vs JOIN plans
