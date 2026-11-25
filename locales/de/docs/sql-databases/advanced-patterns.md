---
title: "Fortgeschrittenes SQL - Window-Funktionen, Subqueries, Datumsfunktionen"
category: concepts
tags: [sql, postgresql, mysql, window-functions, subqueries, analytics]
level: 4
source_sha256: b0d5ba384ce369e432362e6629d36389e074d9db87343aba0a49bb1b3a6732e3
translation: machine
translated_at: '2026-10-24'
---
# Fortgeschrittenes SQL - Window-Funktionen, Subqueries, Datumsfunktionen {#advanced-sql-window-functions-subqueries-date-functions}

Fortgeschrittene SQL-Muster jenseits von einfachen CRUD-Operationen: Window-Funktionen für Analysen, korrelierte Subqueries, Datumsmanipulation und gängige Abfragemuster für Reporting.

## Key Facts {#key-facts}

- Window-Funktionen arbeiten über ein "Window" von Zeilen, ohne die Zeilenanzahl zu reduzieren (anders als GROUP BY)
- `ROW_NUMBER()` liefert eindeutige, fortlaufende Nummern; `RANK()` hat bei Gleichständen Lücken; `DENSE_RANK()` hat keine Lücken
- `HAVING` filtert aggregierte Ergebnisse nach GROUP BY; `WHERE` filtert Zeilen vor der Gruppierung
- Korrelierte Subqueries referenzieren die äußere Abfrage und laufen einmal pro Zeile (kann langsam sein)
- `EXISTS` ist bei großen Subquery-Ergebnissen für Existenzprüfungen effizienter als `IN`
- `LAG`/`LEAD` greifen auf vorherige/nächste Zeilenwerte zu, ohne Self-Joins

## Patterns {#patterns}

### GROUP BY and Aggregations {#group-by-and-aggregations}

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

### Subqueries {#subqueries}

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

### Window Functions {#window-functions}

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

### Common Query Patterns {#common-query-patterns}

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

### Date and Time Functions {#date-and-time-functions}

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

## Gotchas {#gotchas}

- Der Standard-Frame von `LAST_VALUE` endet bei CURRENT ROW, nicht am Ende der Partition - `UNBOUNDED FOLLOWING` muss explizit angegeben werden
- `HAVING` funktioniert nur mit GROUP BY; es filtert aggregierte Ergebnisse, nicht einzelne Zeilen
- Korrelierte Subqueries werden einmal pro äußerer Zeile ausgeführt - können O(N^2) sein; stattdessen JOINs oder Window-Funktionen in Betracht ziehen
- `NULL` in `COUNT(col)` wird nicht gezählt; `COUNT(*)` zählt alle Zeilen einschließlich Nullwerten
- `SUM(amount) OVER()` (leere OVER-Klausel) = Summe über das gesamte Ergebnis
- Window-Funktionen können nicht in der WHERE-Klausel verwendet werden - stattdessen eine Subquery oder CTE nutzen

## See Also {#see-also}

- [[database-patterns]] - PostgreSQL mit pgx in Go
- [[web-scraping]] - Scraping von Daten, die oft SQL-Verarbeitung benötigen
