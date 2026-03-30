---
title: Window Functions
category: syntax
tags: [sql, window-function, over, partition-by, row-number, rank, lag, lead, frame]
---

# Window Functions

Window functions perform calculations across a set of rows related to the current row without collapsing them into groups (unlike GROUP BY). They are essential for rankings, running totals, moving averages, and gap-and-island analysis.

## Key Facts

- Window functions use `OVER()` clause to define the window: `function() OVER (PARTITION BY ... ORDER BY ... frame_clause)`
- Unlike aggregate functions with GROUP BY, window functions do NOT collapse rows - every input row produces an output row
- **PARTITION BY** divides rows into groups (like GROUP BY, but without collapsing); omit to treat entire result set as one partition
- **ORDER BY** within OVER defines row ordering within each partition
- **Frame clause** defines the subset of rows in the partition relative to current row (ROWS, RANGE, GROUPS)
- Window functions execute AFTER WHERE, GROUP BY, HAVING but BEFORE ORDER BY and LIMIT
- See [[select-fundamentals]] for clause execution order
- See [[common-table-expressions]] for combining CTEs with window functions

## Patterns

### Ranking functions

```sql
-- ROW_NUMBER: unique sequential number (no ties)
-- RANK: same rank for ties, gaps after ties (1,2,2,4)
-- DENSE_RANK: same rank for ties, no gaps (1,2,2,3)
SELECT name, department, salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn,
    RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS drnk
FROM employees;

-- Top-N per group pattern (top 3 salaries per department)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
) ranked
WHERE rn <= 3;
```

### Offset functions (LAG / LEAD)

```sql
-- Compare each month's revenue to the previous month
SELECT month, revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) AS month_over_month,
    LEAD(revenue, 1) OVER (ORDER BY month) AS next_month
FROM monthly_revenue;

-- FIRST_VALUE / LAST_VALUE
SELECT name, salary,
    FIRST_VALUE(name) OVER (ORDER BY salary DESC) AS highest_paid,
    LAST_VALUE(name) OVER (
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_paid
FROM employees;
```

### Running totals and moving averages

```sql
-- Running total
SELECT order_date, amount,
    SUM(amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS running_total
FROM orders;

-- 7-day moving average
SELECT day, value,
    AVG(value) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_metrics;

-- Cumulative percentage
SELECT name, salary,
    SUM(salary) OVER (ORDER BY salary) * 100.0 /
    SUM(salary) OVER () AS cumulative_pct
FROM employees;
```

### Named windows (avoid repetition)

```sql
SELECT name, department, salary,
    SUM(salary)  OVER dept_window AS dept_total,
    AVG(salary)  OVER dept_window AS dept_avg,
    RANK()       OVER dept_window AS dept_rank
FROM employees
WINDOW dept_window AS (PARTITION BY department ORDER BY salary DESC);
```

### Frame clause specification

```sql
-- Default frame: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
-- ROWS BETWEEN: counts physical rows
-- RANGE BETWEEN: groups by value (rows with same ORDER BY value = same frame)
-- GROUPS BETWEEN: (PostgreSQL 11+) counts distinct peer groups

-- Explicit frame examples:
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW      -- all rows from start to current
ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING               -- sliding window of 7 rows
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING       -- current row to end
RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW  -- PostgreSQL: time-based window
```

## Gotchas

- **LAST_VALUE default frame** - the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which means LAST_VALUE returns the current row, not the actual last row. Always specify `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`
- **Window functions in WHERE** - you cannot use window functions in WHERE clause (they execute after WHERE). Wrap in a subquery or CTE
- **Performance** - window functions requiring sorts (ORDER BY) benefit from indexes. Multiple different OVER() specs may cause multiple sorts
- **ROWS vs RANGE** - RANGE groups duplicate values together; ROWS treats each row independently. With duplicates in ORDER BY, these produce different results for running aggregates
- **MySQL support** - MySQL 8.0+ supports window functions. Earlier versions do not have them at all

## See Also

- [[common-table-expressions]] - using CTEs with window functions for multi-step analytics
- [[query-optimization-explain]] - identifying window sort operations in plans
- [PostgreSQL window function docs](https://www.postgresql.org/docs/current/tutorial-window.html)
- [MySQL window function docs](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)
