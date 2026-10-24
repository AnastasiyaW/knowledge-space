---
title: "SQL avancé - Fonctions de fenêtrage, sous-requêtes, fonctions de date"
category: concepts
tags: [sql, postgresql, mysql, window-functions, subqueries, analytics]
level: 4
source_sha256: b0d5ba384ce369e432362e6629d36389e074d9db87343aba0a49bb1b3a6732e3
translation: machine
translated_at: '2026-10-24'
---
# SQL avancé - Fonctions de fenêtrage, sous-requêtes, fonctions de date {#advanced-sql-window-functions-subqueries-date-functions}

Motifs SQL avancés au-delà du CRUD de base : fonctions de fenêtrage pour l'analyse, sous-requêtes corrélées, manipulation de dates et motifs de requêtes courants pour le reporting.

## Points clés {#key-facts}

- Les fonctions de fenêtrage opèrent sur une « fenêtre » de lignes sans réduire le nombre de lignes (contrairement à GROUP BY)
- `ROW_NUMBER()` donne des numéros séquentiels uniques ; `RANK()` laisse des trous en cas d'égalité ; `DENSE_RANK()` n'en laisse pas
- `HAVING` filtre les résultats agrégés après GROUP BY ; `WHERE` filtre les lignes avant le regroupement
- Les sous-requêtes corrélées référencent la requête externe et s'exécutent une fois par ligne (peuvent être lentes)
- `EXISTS` est plus efficace que `IN` pour les vérifications d'existence avec de gros résultats de sous-requête
- `LAG`/`LEAD` accèdent aux valeurs de la ligne précédente/suivante sans auto-jointures

## Motifs {#patterns}

### GROUP BY et agrégations {#group-by-and-aggregations}

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

### Sous-requêtes {#subqueries}

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

### Fonctions de fenêtrage {#window-functions}

```sql
-- Syntax
function() OVER (
    PARTITION BY col    -- reset window per group
    ORDER BY col        -- ordering within window
    ROWS/RANGE BETWEEN ... AND CURRENT ROW  -- frame
)
```

**Fonctions de classement** :
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

**Fonctions de décalage** :
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

**Fonctions de distribution** :
```sql
CUME_DIST() OVER(ORDER BY score)
-- fraction of rows <= current row (0 to 1)

PERCENT_RANK() OVER(ORDER BY score)
-- relative rank: (rank - 1) / (total_rows - 1)
```

**Totaux cumulés et moyennes mobiles** :
```sql
SUM(amount) OVER(ORDER BY date)
-- running total (default: UNBOUNDED PRECEDING to CURRENT ROW)

AVG(amount) OVER(ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
-- 7-day moving average

SUM(amount) OVER(PARTITION BY dept ORDER BY date)
-- running total per department
```

### Motifs de requêtes courants {#common-query-patterns}

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

### Fonctions de date et d'heure {#date-and-time-functions}

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

## Pièges {#gotchas}

- Le cadre par défaut de `LAST_VALUE` se termine à CURRENT ROW, et non à la fin de la partition : il faut spécifier `UNBOUNDED FOLLOWING`
- `HAVING` ne fonctionne qu'avec GROUP BY ; il filtre les résultats agrégés, et non les lignes individuelles
- Les sous-requêtes corrélées s'exécutent une fois par ligne externe : cela peut atteindre O(N^2) ; envisagez plutôt des JOIN ou des fonctions de fenêtrage
- `NULL` dans `COUNT(col)` n'est pas compté ; `COUNT(*)` compte toutes les lignes, y compris les valeurs nulles
- `SUM(amount) OVER()` (clause OVER vide) = total sur l'ensemble du résultat
- Les fonctions de fenêtrage ne peuvent pas être utilisées dans la clause WHERE : utilisez une sous-requête ou un CTE

## Voir aussi {#see-also}

- [[database-patterns]] - PostgreSQL avec pgx en Go
- [[web-scraping]] - scraping de données qui nécessitent souvent un traitement SQL
