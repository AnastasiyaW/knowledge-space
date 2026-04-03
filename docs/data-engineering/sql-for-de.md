---
title: SQL for Data Engineering
category: reference
tags: [data-engineering, sql, postgresql, window-functions, cte, joins]
---

# SQL for Data Engineering

SQL is the universal language for data engineering. This entry covers DE-specific SQL patterns including window functions, CTEs, query optimization, and DWH-oriented techniques.

## Query Execution Order

```
FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT
```

- `WHERE` filters rows BEFORE aggregation (no aggregate functions)
- `HAVING` filters groups AFTER aggregation (can use aggregates)

## Window Functions

Compute across rows without collapsing them (unlike GROUP BY).

```sql
function() OVER (
    PARTITION BY col    -- define groups
    ORDER BY col        -- ordering within group
    ROWS BETWEEN ...    -- frame specification
)
```

### Ranking

```sql
ROW_NUMBER() OVER (ORDER BY salary DESC)  -- unique: 1,2,3,4
RANK()       OVER (ORDER BY salary DESC)  -- ties, gaps: 1,1,3,4
DENSE_RANK() OVER (ORDER BY salary DESC)  -- ties, no gaps: 1,1,2,3
NTILE(4)     OVER (ORDER BY salary)       -- divide into buckets
```

### Offset

```sql
LAG(col, 1)    OVER (ORDER BY date)  -- previous row
LEAD(col, 1)   OVER (ORDER BY date)  -- next row
FIRST_VALUE(col) OVER (ORDER BY date)
LAST_VALUE(col)  OVER (ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### Aggregates Over Windows

```sql
SUM(revenue) OVER (ORDER BY date) AS cumulative      -- running total
AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
revenue * 100.0 / SUM(revenue) OVER () AS pct_total  -- percent of total
```

### Frame: ROWS vs RANGE

- **ROWS**: physical row positions relative to current
- **RANGE**: value differences in ORDER BY column
- Default with ORDER BY: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

## Common Patterns

### Top N Per Group

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY category ORDER BY revenue DESC
    ) AS rn
    FROM sales
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Deduplication

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY email ORDER BY created_at DESC
    ) AS rn FROM users
)
SELECT * FROM ranked WHERE rn = 1;
```

### Year-over-Year Change

```sql
SELECT month, revenue,
    LAG(revenue, 12) OVER (ORDER BY month) AS last_year,
    (revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
        / LAG(revenue, 12) OVER (ORDER BY month) AS yoy_pct
FROM monthly_stats;
```

### Find Missing Dates

```sql
WITH dates AS (
    SELECT generate_series(MIN(date), MAX(date), '1 day')::date AS d
    FROM orders
)
SELECT d FROM dates LEFT JOIN orders ON orders.date = d
WHERE orders.date IS NULL;
```

## JOIN Types

| Type | What |
|------|------|
| INNER | Only matching rows |
| LEFT | All from left + matching right |
| RIGHT | All from right + matching left |
| FULL | All from both, NULLs where no match |
| CROSS | Cartesian product |
| ANTI | `LEFT JOIN ... WHERE b.key IS NULL` |
| SEMI | `WHERE EXISTS (SELECT 1 FROM b WHERE ...)` |

### Cartesian Product Warning

When join key has duplicates in BOTH tables, rows multiply: 2 left x 2 right = 4 rows. **GROUP BY before JOIN** to deduplicate.

## CTEs and Recursive Queries

```sql
WITH RECURSIVE hierarchy AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e JOIN hierarchy h ON e.manager_id = h.id
)
SELECT * FROM hierarchy;
```

## NULL Handling

```sql
COALESCE(x, y, ...)      -- first non-NULL
NULLIF(x, y)             -- NULL if x=y (prevents division by zero)
SELECT total / NULLIF(count, 0) FROM stats;
```

- `COUNT(column)` excludes NULLs; `COUNT(*)` counts all
- `NULL = NULL` is NULL, not TRUE. Use `IS NULL`
- Multiple NULLs = one group in DISTINCT/GROUP BY

## EXPLAIN

```sql
EXPLAIN ANALYZE SELECT ...;      -- actual timings
EXPLAIN (BUFFERS, ANALYZE) ...;  -- buffer usage
```

Tool: [explain.tensor.ru](https://explain.tensor.ru) for visual plan analysis.

## Gotchas
- `LAST_VALUE()` with default frame only sees up to current row - must set UNBOUNDED FOLLOWING
- Cartesian product silently inflates aggregates after JOIN
- `COUNT(DISTINCT col)` not `DISTINCT COUNT(col)`
- Subqueries with `LIMIT 1` return one row or empty - safe for scalar
- `GROUP BY` column order does not matter; `ORDER BY` column order does

## See Also
- [[clickhouse]] - ClickHouse-specific SQL
- [[greenplum-mpp]] - MPP-specific SQL
- [[data-modeling]] - schema design
- [[etl-elt-pipelines]] - SQL in ELT context
