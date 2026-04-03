---
title: SQL for Analytics
category: tools
tags: [bi-analytics, sql, window-functions, joins, cte, aggregation, analytics]
---

# SQL for Analytics

SQL is the foundational tool for data analysts, but knowing SQL syntax alone doesn't make you an analyst - analytical thinking about what to measure and why is the real skill. This entry covers SQL patterns specifically relevant to BI and product analytics.

## Key Facts

- SQL execution order (important for debugging): FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
- Window functions compute over a "window" of rows without collapsing rows
- CTEs (Common Table Expressions) are cleaner than nested subqueries
- Analytics-specific patterns: cohort retention, funnel analysis, DAU/MAU stickiness
- Connecting Python to SQL databases enables combining SQL querying with pandas analysis

## Patterns

### Core Query Structure

```sql
SELECT column1, column2, COUNT(*) as count
FROM table_name
WHERE condition
GROUP BY column1, column2
HAVING aggregate_condition
ORDER BY column1 DESC
LIMIT 100;
```

### Filtering

```sql
WHERE status = 'active'
WHERE city IN ('Moscow', 'SPb', 'Kazan')
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'
WHERE name LIKE 'Ivan%'          -- starts with
WHERE email LIKE '%@mail.ru'     -- ends with
WHERE phone IS NULL
WHERE status = 'active' AND city = 'Moscow'
WHERE NOT status = 'cancelled'
```

### JOINs

```sql
-- INNER: only matching rows
SELECT u.name, o.order_id, o.amount
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id;

-- LEFT: all left + matching right (NULLs where no match)
SELECT u.name, COUNT(o.order_id) as order_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.name;

-- Multiple JOINs
SELECT u.name, o.order_id, p.product_name
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

### CTEs (Common Table Expressions)

```sql
WITH active_users AS (
    SELECT user_id, name
    FROM users
    WHERE last_activity > CURRENT_DATE - INTERVAL '30 days'
),
user_orders AS (
    SELECT user_id, SUM(amount) as total
    FROM orders
    GROUP BY user_id
)
SELECT a.name, COALESCE(u.total, 0) as total_spent
FROM active_users a
LEFT JOIN user_orders u ON a.user_id = u.user_id;
```

### Window Functions

```sql
-- Ranking
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) as order_num
RANK() OVER (ORDER BY amount DESC) as rank_by_amount
DENSE_RANK() OVER (ORDER BY amount DESC) as dense_rank

-- Running totals and rolling averages
SUM(amount) OVER (ORDER BY order_date) as running_total
AVG(amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) as rolling_7day_avg

-- Lag/Lead (previous/next row access)
LAG(amount, 1) OVER (ORDER BY order_date) as prev_day
LEAD(amount, 1) OVER (ORDER BY order_date) as next_day
amount - LAG(amount, 1) OVER (ORDER BY order_date) as day_change

-- Percentiles
NTILE(10) OVER (ORDER BY total_spent) as decile
PERCENT_RANK() OVER (ORDER BY total_spent) as percentile
```

### Analytics SQL Patterns

**Cohort retention** - see [[cohort-retention-analysis]] for full pattern.

**Funnel analysis:**
```sql
SELECT
    COUNT(CASE WHEN event = 'page_view' THEN user_id END) as step1,
    COUNT(CASE WHEN event = 'add_to_cart' THEN user_id END) as step2,
    COUNT(CASE WHEN event = 'checkout_start' THEN user_id END) as step3,
    COUNT(CASE WHEN event = 'purchase' THEN user_id END) as step4
FROM events
WHERE event_date = CURRENT_DATE;
```

**DAU/MAU stickiness** - see [[product-metrics-framework]] for full pattern.

### Python + SQL Integration

```python
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host='localhost', database='mydb',
    user='analyst', password='pass'
)

df = pd.read_sql("""
    SELECT user_id, COUNT(*) as orders
    FROM orders
    WHERE created_at >= '2024-01-01'
    GROUP BY user_id
    ORDER BY orders DESC
    LIMIT 100
""", conn)

# Jupyter magic
%load_ext sql
%sql postgresql://user:pass@host/db
result = %sql SELECT COUNT(*) FROM orders
```

## Gotchas

- Execution order matters: you can't use a column alias from SELECT in WHERE clause (WHERE runs before SELECT)
- NULL comparisons: `WHERE col = NULL` never matches - use `WHERE col IS NULL`
- Window functions don't reduce row count - use them when you need per-row calculations alongside aggregates
- Correlated subqueries run once per outer row and can be extremely slow - prefer JOINs or CTEs
- `HAVING` filters after aggregation, `WHERE` filters before - confusing them is a common bug

## See Also

- [[pandas-data-analysis]] - Python equivalent of SQL operations
- [[cohort-retention-analysis]] - SQL cohort retention pattern
- [[tableau-fundamentals]] - SQL in Tableau Custom SQL
- [[powerbi-fundamentals]] - DAX as alternative to SQL
