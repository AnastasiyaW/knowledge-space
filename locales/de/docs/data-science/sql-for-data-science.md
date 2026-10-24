---
title: "SQL für Data Science"
category: tools
tags: [data-science, sql, queries, analytics, window-functions]
level: 3
source_sha256: b2c16d2f6b6ca5d476bb789e724802647f88ade182f1d721a682212994105f14
translation: machine
translated_at: '2026-10-24'
---
# SQL für Data Science {#sql-for-data-science}

SQL ist die universelle Sprache für das Extrahieren von Daten aus Datenbanken. Jeder Data Scientist braucht SQL-Kenntnisse – es ist oft der erste Schritt in jeder Analyse-Pipeline.

## Grundlegende Befehle {#core-commands}

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

## Operatoren {#operators}

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

## Window Functions {#window-functions}

Berechnet Werte über eine Menge von Zeilen, die mit der aktuellen Zeile in Beziehung stehen. Unverzichtbar für Analysen.

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

## Subqueries und CTEs {#subqueries-and-ctes}

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

## Datumsfunktionen {#date-functions}

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

## Muster für Data Science {#patterns-for-ds}

### Deduplizierung {#deduplicate}
```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as rn
    FROM users
)
SELECT * FROM ranked WHERE rn = 1;
```

### Pivot / Kreuztabellierung {#pivot-cross-tabulation}
```sql
SELECT user_id,
    SUM(CASE WHEN category = 'A' THEN amount ELSE 0 END) as cat_a,
    SUM(CASE WHEN category = 'B' THEN amount ELSE 0 END) as cat_b
FROM transactions
GROUP BY user_id;
```

### Perzentil {#percentile}
```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median_salary
FROM employees;
```

## Fallstricke {#gotchas}
- `WHERE` filtert Zeilen vor der Aggregation; `HAVING` filtert nach `GROUP BY`
- `NULL != NULL` ist wahr. Verwende `IS NULL` statt `= NULL`
- `COUNT(*)` zählt alle Zeilen; `COUNT(col)` schließt NULLs aus
- Window Functions reduzieren die Zeilenanzahl nicht (im Gegensatz zu GROUP BY)
- Verschiedene SQL-Dialekte haben unterschiedliche Funktionsnamen (DATE_TRUNC vs. DATE_FORMAT)

## Siehe auch {#see-also}
- [[pandas-eda]] - pandas-Entsprechungen von SQL-Operationen
- [[bi-dashboards]] - SQL treibt BI-Abfragen an
- [[ds-workflow]] - SQL im Schritt der Datenerhebung
