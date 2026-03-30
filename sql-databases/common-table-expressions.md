---
title: Common Table Expressions (CTEs)
category: syntax
tags: [sql, cte, with, recursive, materialized, postgresql, mysql]
---

# Common Table Expressions (CTEs)

CTEs provide named temporary result sets defined within a single SQL statement using the `WITH` clause. They improve readability, enable recursion, and can be materialized or inlined depending on the engine.

## Key Facts

- CTEs are defined with `WITH name AS (query)` and referenced by name in the main query
- Multiple CTEs can be chained: `WITH a AS (...), b AS (SELECT ... FROM a) SELECT ... FROM b`
- **Recursive CTEs** use `WITH RECURSIVE` and consist of a base case UNION ALL'd with a recursive term
- PostgreSQL 12+: CTEs are inlined (optimized away) by default unless they are recursive or referenced multiple times. Use `MATERIALIZED` / `NOT MATERIALIZED` to control
- MySQL 8.0+ supports CTEs and recursive CTEs. Before 8.0 - no CTE support at all
- CTEs in PostgreSQL DML: you can use CTEs with INSERT/UPDATE/DELETE (writeable CTEs)
- See [[subqueries-and-derived-tables]] for comparison with derived tables
- See [[window-functions]] for CTEs combined with analytics

## Patterns

### Basic CTE for readability

```sql
WITH monthly_revenue AS (
    SELECT date_trunc('month', order_date) AS month,
           SUM(total) AS revenue
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY 1
),
monthly_costs AS (
    SELECT date_trunc('month', cost_date) AS month,
           SUM(amount) AS costs
    FROM expenses
    WHERE cost_date >= '2024-01-01'
    GROUP BY 1
)
SELECT r.month,
       r.revenue,
       c.costs,
       r.revenue - COALESCE(c.costs, 0) AS profit
FROM monthly_revenue r
LEFT JOIN monthly_costs c ON r.month = c.month
ORDER BY r.month;
```

### Recursive CTE - hierarchical data

```sql
-- Employee org chart traversal
WITH RECURSIVE org_tree AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 AS depth, ARRAY[id] AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive term
    SELECT e.id, e.name, e.manager_id, t.depth + 1,
           t.path || e.id
    FROM employees e
    INNER JOIN org_tree t ON e.manager_id = t.id
    WHERE t.depth < 10  -- safety limit to prevent infinite loops
)
SELECT * FROM org_tree ORDER BY path;
```

### Recursive CTE - generating series (MySQL alternative)

```sql
-- Generate date series (PostgreSQL has generate_series, MySQL doesn't)
WITH RECURSIVE dates AS (
    SELECT DATE '2024-01-01' AS dt
    UNION ALL
    SELECT dt + INTERVAL '1 day'
    FROM dates
    WHERE dt < '2024-12-31'
)
SELECT dt FROM dates;
```

### Writeable CTE (PostgreSQL only)

```sql
-- Archive old orders and return archived count
WITH archived AS (
    DELETE FROM orders
    WHERE order_date < '2023-01-01'
    RETURNING *
)
INSERT INTO orders_archive SELECT * FROM archived;

-- UPDATE with CTE returning modified rows
WITH updated AS (
    UPDATE products SET price = price * 1.1
    WHERE category = 'premium'
    RETURNING id, name, price
)
SELECT * FROM updated;
```

### Materialization control (PostgreSQL 12+)

```sql
-- Force materialization (useful when CTE is referenced multiple times)
WITH stats AS MATERIALIZED (
    SELECT department, AVG(salary) AS avg_sal FROM employees GROUP BY department
)
SELECT * FROM stats WHERE avg_sal > 50000
UNION ALL
SELECT * FROM stats WHERE avg_sal < 30000;

-- Force inlining (useful when you want the optimizer to push predicates)
WITH filtered AS NOT MATERIALIZED (
    SELECT * FROM large_table
)
SELECT * FROM filtered WHERE id = 42;  -- predicate pushed into CTE scan
```

## Gotchas

- **Recursive CTE infinite loops** - always include a termination condition (depth limit or WHERE clause). PostgreSQL has no built-in cycle detection prior to v14. PostgreSQL 14+ adds `CYCLE` clause
- **Performance with materialized CTEs** - in PostgreSQL <12, CTEs were ALWAYS materialized (optimization fence). This could kill performance when a CTE returns many rows but only a few are needed
- **MySQL CTE limitations** - MySQL does not support writeable CTEs (INSERT/UPDATE/DELETE inside WITH). Also no MATERIALIZED hint
- **CTE vs temporary table** - CTEs exist only for the duration of one statement. For multi-statement reuse within a transaction, use temp tables
- **Column naming** - CTE column names can be defined explicitly: `WITH cte(col1, col2) AS (...)`. This is cleaner than relying on implicit names from the SELECT list

## See Also

- [[subqueries-and-derived-tables]] - when to use subqueries vs CTEs
- [[window-functions]] - combining CTEs with windowed analytics
- [PostgreSQL WITH docs](https://www.postgresql.org/docs/current/queries-with.html)
- [MySQL WITH docs](https://dev.mysql.com/doc/refman/8.0/en/with.html)
