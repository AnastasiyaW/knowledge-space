---
title: Subqueries and CTEs
category: concepts
tags: [sql-databases, sql, subquery, cte, common-table-expression, exists, derived-table, correlated]
---

# Subqueries and CTEs

Subqueries are queries nested inside other queries. CTEs (Common Table Expressions) provide named, reusable query blocks that improve readability for complex SQL.

## Key Facts

- Scalar subqueries return a single value; table subqueries return multiple rows
- Correlated subqueries execute once per outer row (can be expensive)
- EXISTS stops at first match - more efficient than IN for existence checks
- CTEs are defined with `WITH` keyword and can chain multiple named blocks
- PostgreSQL materializes CTEs by default (pre-12); use `NOT MATERIALIZED` hint for inlining

## Patterns

### Scalar Subquery
```sql
SELECT * FROM users
WHERE id = (SELECT sender_id FROM messages GROUP BY sender_id ORDER BY COUNT(*) DESC LIMIT 1);

-- Scalar subquery in SELECT
SELECT u.name,
  (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;
```

### IN Subquery
```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);

-- NOT IN: find users without orders
SELECT * FROM users WHERE id NOT IN (
  SELECT DISTINCT sender_id FROM messages WHERE sender_id IS NOT NULL
);
```

### EXISTS Subquery
```sql
-- Users who have at least one order
SELECT * FROM users u WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 1000
);

-- Anti-pattern replacement: safer than NOT IN
SELECT * FROM users u WHERE NOT EXISTS (
  SELECT 1 FROM messages m WHERE m.sender_id = u.id
);
```

### Derived Table (Subquery in FROM)
```sql
SELECT avg_amount FROM (
  SELECT user_id, AVG(amount) AS avg_amount
  FROM orders GROUP BY user_id
) AS user_avgs
WHERE avg_amount > 500;
```

### CTE (Common Table Expression)
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

### Recursive CTE
```sql
-- Organizational hierarchy
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, ot.depth + 1
  FROM employees e
  JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY depth, name;
```

## Gotchas

- **NOT IN with NULLs**: If subquery returns ANY NULL, `NOT IN` returns empty result for ALL rows - always add `WHERE col IS NOT NULL` or use NOT EXISTS instead
- Correlated subqueries run once per outer row - rewrite as JOIN when possible
- `EXISTS` only checks for existence, not values - `SELECT 1` inside is convention
- CTEs in PostgreSQL < 12 are optimization fences (always materialized)
- MySQL does not support recursive CTEs before version 8.0

## See Also

- [[select-fundamentals]] - basic WHERE filtering
- [[joins-and-set-operations]] - JOINs as alternative to subqueries
- [[window-functions]] - analytics without subqueries
