---
title: SQL for Data Science
category: tools
tags: [data-science, sql, queries, analytics, window-functions]
---

# SQL for Data Science

SQL is the universal language for extracting data from databases. Every data scientist needs SQL fluency - it's often the first step in any analysis pipeline.

## Core Commands

```sql
-- Basic query
SELECT col1, col2 FROM table
WHERE condition
ORDER BY col1 DESC
LIMIT 100;

-- Aggregation
SELECT category, COUNT(*), AVG(price), SUM(sales)
FROM products
GROUP BY category
HAVING COUNT(*) > 10;

-- Joins
SELECT a.*, b.name
FROM orders a
INNER JOIN customers b ON a.customer_id = b.id;   -- matching rows only
LEFT JOIN customers b ON a.customer_id = b.id;     -- all from left
RIGHT JOIN customers b ON a.customer_id = b.id;    -- all from right
FULL OUTER JOIN customers b ON a.customer_id = b.id; -- all from both
```

## Operators

```sql
-- Comparison: =, !=, <>, >, <, >=, <=
-- Logical: AND, OR, NOT
-- Special operators:
WHERE col IN ('a', 'b', 'c')
WHERE col BETWEEN 10 AND 20
WHERE col LIKE '%pattern%'
WHERE col IS NULL
WHERE col IS NOT NULL
WHERE EXISTS (SELECT 1 FROM other_table WHERE ...)
```

## Window Functions

Compute values across a set of rows related to the current row. Essential for analytics.

```sql
-- Row number, rank, dense_rank
SELECT *,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM students;

-- Partition: rank within groups
SELECT category, product, revenue,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank_in_cat
FROM sales;

-- Running total
SELECT date, amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- LAG / LEAD: access previous/next rows
SELECT date, revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_day,
    LEAD(revenue) OVER (ORDER BY date) as next_day
FROM daily_revenue;

-- Rolling average
SELECT date, revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    as rolling_7d
FROM daily_revenue;
```

## Subqueries and CTEs

```sql
-- CTE (Common Table Expression) - cleaner than nested subqueries
WITH monthly_revenue AS (
    SELECT DATE_TRUNC('month', date) as month,
           SUM(revenue) as total
    FROM sales
    GROUP BY 1
)
SELECT month, total,
    LAG(total) OVER (ORDER BY month) as prev_month,
    total - LAG(total) OVER (ORDER BY month) as delta
FROM monthly_revenue;
```

## Date Functions

```sql
-- PostgreSQL
DATE_TRUNC('month', date_col)      -- truncate to month
EXTRACT(dow FROM date_col)          -- day of week
date_col + INTERVAL '7 days'        -- date arithmetic
AGE(date1, date2)                   -- interval between dates
NOW()                                -- current timestamp

-- MySQL
DATE_FORMAT(date_col, '%Y-%m')
DATEDIFF(date1, date2)
DATE_ADD(date_col, INTERVAL 7 DAY)
```

## Patterns for DS

### Deduplicate
```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as rn
    FROM users
)
SELECT * FROM ranked WHERE rn = 1;
```

### Pivot / Cross-Tabulation
```sql
SELECT user_id,
    SUM(CASE WHEN category = 'A' THEN amount ELSE 0 END) as cat_a,
    SUM(CASE WHEN category = 'B' THEN amount ELSE 0 END) as cat_b
FROM transactions
GROUP BY user_id;
```

### Percentile
```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median_salary
FROM employees;
```

## Gotchas
- `WHERE` filters rows before aggregation; `HAVING` filters after `GROUP BY`
- `NULL != NULL` is true. Use `IS NULL` not `= NULL`
- `COUNT(*)` counts all rows; `COUNT(col)` excludes NULLs
- Window functions don't reduce rows (unlike GROUP BY)
- Different SQL dialects have different function names (DATE_TRUNC vs DATE_FORMAT)

## See Also
- [[pandas-eda]] - pandas equivalents of SQL operations
- [[bi-dashboards]] - SQL powers BI queries
- [[ds-workflow]] - SQL in the data collection step
