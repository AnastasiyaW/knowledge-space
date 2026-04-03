---
title: Window Functions
category: concepts
tags: [sql-databases, sql, window-function, row-number, rank, lag, lead, running-total, partition-by]
---

# Window Functions

Window functions perform calculations across a set of rows related to the current row without collapsing rows like GROUP BY. They operate on a "window" defined by PARTITION BY and ORDER BY clauses.

## Key Facts

- Window functions run after WHERE, GROUP BY, HAVING - they see the filtered/aggregated result
- PARTITION BY divides rows into groups; ORDER BY determines order within each partition
- Frame clause (ROWS BETWEEN) controls which rows the function considers
- Default frame: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` when ORDER BY is present
- Cannot use window functions in WHERE or HAVING - wrap in subquery/CTE if needed

## Patterns

### Ranking Functions
```sql
-- ROW_NUMBER: unique sequential number (no ties)
SELECT *, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank FROM employees;

-- With partitioning: rank within each department
SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- RANK: same rank for ties, gaps after (1, 2, 2, 4)
SELECT *, RANK() OVER (ORDER BY salary DESC) AS rank FROM employees;

-- DENSE_RANK: same rank for ties, no gaps (1, 2, 2, 3)
SELECT *, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank FROM employees;

-- NTILE: divide into N equal groups
SELECT *, NTILE(4) OVER (ORDER BY salary) AS quartile FROM employees;
```

### Aggregate Window Functions
```sql
-- Running total
SELECT *, SUM(amount) OVER (ORDER BY created_at) AS running_total FROM orders;

-- Moving average (3-row window)
SELECT *, AVG(amount) OVER (
  ORDER BY created_at ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS moving_avg FROM orders;

-- Cumulative count per partition
SELECT department, hire_date,
  COUNT(*) OVER (PARTITION BY department ORDER BY hire_date) AS running_count
FROM employees;
```

### Offset Functions
```sql
-- LAG: access previous row value
SELECT *, LAG(amount, 1) OVER (ORDER BY created_at) AS prev_amount FROM orders;

-- LEAD: access next row value
SELECT *, LEAD(amount, 1) OVER (ORDER BY created_at) AS next_amount FROM orders;

-- Sales difference from previous period
SELECT *, amount - LAG(amount, 1) OVER (ORDER BY created_at) AS diff FROM orders;

-- FIRST_VALUE / LAST_VALUE
SELECT *, FIRST_VALUE(name) OVER (PARTITION BY dept ORDER BY salary DESC) AS top_earner
FROM employees;
```

### Window Frame Specification
```sql
-- ROWS BETWEEN controls which rows the function sees:
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW    -- cumulative from start
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW            -- rolling 3-row window
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- entire partition
ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING             -- current + next row
```

### Named Windows (Reuse)
```sql
SELECT
  ROW_NUMBER() OVER w AS rn,
  SUM(amount) OVER w AS running_total
FROM orders
WINDOW w AS (PARTITION BY user_id ORDER BY created_at);
```

## Gotchas

- `LAST_VALUE` with default frame only sees up to current row - use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` for true last value
- ROWS vs RANGE: ROWS counts physical rows, RANGE groups rows with equal ORDER BY values
- Window functions cannot be nested: `SUM(ROW_NUMBER() OVER (...)) OVER (...)` is invalid
- Performance: each window function may require a separate sort pass

## See Also

- [[aggregate-functions-group-by]] - GROUP BY aggregation (collapses rows)
- [[query-optimization-explain]] - understanding sort costs from window functions
- [[select-fundamentals]] - CASE expressions combined with window functions
