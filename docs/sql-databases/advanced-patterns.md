---
title: Advanced SQL - Window Functions, Subqueries, Date Functions
category: concepts
tags: [misc, sql, postgresql, mysql, window-functions, subqueries, analytics]
---

# Advanced SQL - Window Functions, Subqueries, Date Functions

Advanced SQL patterns beyond basic CRUD - window functions for analytics, correlated subqueries, date manipulation, and common query patterns for reporting.

## Key Facts

- Window functions operate over a "window" of rows without reducing row count (unlike GROUP BY)
- `ROW_NUMBER()` gives unique sequential numbers; `RANK()` has gaps on ties; `DENSE_RANK()` has no gaps
- `HAVING` filters on aggregate results after GROUP BY; `WHERE` filters rows before grouping
- Correlated subqueries reference the outer query and run once per row (can be slow)
- `EXISTS` is more efficient than `IN` for existence checks with large subquery results
- `LAG`/`LEAD` access previous/next row values without self-joins

## Patterns

### GROUP BY and Aggregations

```sql
SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000
ORDER BY avg_salary DESC
LIMIT 5;

-- Common aggregate functions
COUNT(*), COUNT(DISTINCT col)
SUM(col), AVG(col), MIN(col), MAX(col)
STRING_AGG(col, ', ' ORDER BY col)  -- PostgreSQL
GROUP_CONCAT(col ORDER BY col SEPARATOR ', ')  -- MySQL
```

### Subqueries

```sql
-- Derived table (subquery in FROM)
SELECT dept, avg_sal
FROM (
    SELECT department AS dept, AVG(salary) AS avg_sal
    FROM employees GROUP BY department
) AS dept_averages
WHERE avg_sal > 60000;

-- Scalar subquery in WHERE
SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Correlated subquery (references outer query, runs once per row)
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary) FROM employees
    WHERE department = e.department
);

-- EXISTS (efficient existence check)
SELECT c.name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### Window Functions

```sql
-- Syntax
function() OVER (
    PARTITION BY col    -- reset window per group
    ORDER BY col        -- ordering within window
    ROWS/RANGE BETWEEN ... AND CURRENT ROW  -- frame
)
```

**Ranking functions**:
```sql
ROW_NUMBER() OVER(PARTITION BY dept ORDER BY salary DESC)
-- unique sequential: 1, 2, 3, 4

RANK() OVER(ORDER BY score DESC)
-- gaps on ties: 1, 2, 2, 4

DENSE_RANK() OVER(ORDER BY score DESC)
-- no gaps: 1, 2, 2, 3

NTILE(4) OVER(ORDER BY salary)
-- divide into N equal buckets (quartiles)
```

**Offset functions**:
```sql
LAG(salary, 1, 0) OVER(ORDER BY hire_date)   -- previous row
LEAD(salary, 1, 0) OVER(ORDER BY hire_date)  -- next row

FIRST_VALUE(salary) OVER(PARTITION BY dept ORDER BY hire_date)

LAST_VALUE(salary) OVER(
    PARTITION BY dept ORDER BY hire_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
-- LAST_VALUE requires explicit UNBOUNDED frame!
```

**Distribution functions**:
```sql
CUME_DIST() OVER(ORDER BY score)
-- fraction of rows <= current row (0 to 1)

PERCENT_RANK() OVER(ORDER BY score)
-- relative rank: (rank - 1) / (total_rows - 1)
```

**Running totals and moving averages**:
```sql
SUM(amount) OVER(ORDER BY date)
-- running total (default: UNBOUNDED PRECEDING to CURRENT ROW)

AVG(amount) OVER(ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
-- 7-day moving average

SUM(amount) OVER(PARTITION BY dept ORDER BY date)
-- running total per department
```

### Common Query Patterns

```sql
-- Top N per group
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY dept ORDER BY salary DESC) AS rn
    FROM employees
) t WHERE rn <= 3;

-- Running total with percentage of total
SELECT date, amount,
    SUM(amount) OVER(ORDER BY date) AS running_total,
    amount / SUM(amount) OVER() * 100 AS pct_of_total
FROM sales;

-- Year-over-year comparison
SELECT year, revenue,
    LAG(revenue, 1) OVER(ORDER BY year) AS prev_year,
    (revenue - LAG(revenue, 1) OVER(ORDER BY year))
      / LAG(revenue, 1) OVER(ORDER BY year) * 100 AS yoy_pct
FROM annual_revenue;
```

### Date and Time Functions

```sql
-- PostgreSQL
EXTRACT(YEAR FROM date_col)
EXTRACT(DOW FROM date_col)  -- day of week (0=Sunday)
DATE_TRUNC('month', timestamp_col)
date_col + INTERVAL '7 days'
AGE(timestamp1, timestamp2)

-- MySQL
YEAR(date_col), MONTH(date_col), DAY(date_col)
DATE_FORMAT(date_col, '%Y-%m')
DATEDIFF(date1, date2)
DATE_ADD(date_col, INTERVAL 7 DAY)
```

## Gotchas

- `LAST_VALUE` default frame ends at CURRENT ROW, not end of partition - must specify `UNBOUNDED FOLLOWING`
- `HAVING` only works with GROUP BY; it filters aggregated results, not individual rows
- Correlated subqueries execute once per outer row - can be O(N^2); consider JOINs or window functions instead
- `NULL` in `COUNT(col)` is not counted; `COUNT(*)` counts all rows including nulls
- `SUM(amount) OVER()` (empty OVER clause) = total across entire result set
- Window functions cannot be used in WHERE clause - use a subquery or CTE

## See Also

- [[database-patterns]] - PostgreSQL with pgx in Go
- [[web-scraping]] - scraping data that often needs SQL processing
