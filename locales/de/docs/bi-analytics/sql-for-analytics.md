---
title: "SQL für Analytics"
category: tools
tags: [bi-analytics, sql, window-functions, joins, cte, aggregation, analytics]
level: 3
source_sha256: a3e39795621cafbed5f732b8599a7e90898d10b43e7554d4bb20146a5acbb8f9
translation: machine
translated_at: '2026-10-24'
---
# SQL für Analytics {#sql-for-analytics}

SQL ist das grundlegende Werkzeug für Datenanalysten, aber die Kenntnis der SQL-Syntax allein macht noch keinen Analysten – analytisches Denken darüber, was gemessen werden soll und warum, ist die eigentliche Fähigkeit. Dieser Eintrag behandelt SQL-Muster, die speziell für BI und Product Analytics relevant sind.

## Key Facts {#key-facts}

- SQL-Ausführungsreihenfolge (wichtig für das Debugging): FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
- Window Functions berechnen über ein "Fenster" von Zeilen, ohne Zeilen zu aggregieren
- CTEs (Common Table Expressions) sind übersichtlicher als verschachtelte Subqueries
- Analytics-spezifische Muster: Cohort Retention, Funnel-Analyse, DAU/MAU-Stickiness
- Die Anbindung von Python an SQL-Datenbanken ermöglicht die Kombination von SQL-Abfragen mit pandas-Analysen

## Patterns {#patterns}

### Core Query Structure {#core-query-structure}

```sql
SELECT column1, column2, COUNT(*) as count
FROM table_name
WHERE condition
GROUP BY column1, column2
HAVING aggregate_condition
ORDER BY column1 DESC
LIMIT 100;
```

### Filtering {#filtering}

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

### JOINs {#joins}

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

### CTEs (Common Table Expressions) {#ctes-common-table-expressions}

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

### Window Functions {#window-functions}

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

### Analytics SQL Patterns {#analytics-sql-patterns}

**Cohort Retention** – siehe [[cohort-retention-analysis]] für das vollständige Muster.

**Funnel-Analyse:**
```sql
SELECT
    COUNT(CASE WHEN event = 'page_view' THEN user_id END) as step1,
    COUNT(CASE WHEN event = 'add_to_cart' THEN user_id END) as step2,
    COUNT(CASE WHEN event = 'checkout_start' THEN user_id END) as step3,
    COUNT(CASE WHEN event = 'purchase' THEN user_id END) as step4
FROM events
WHERE event_date = CURRENT_DATE;
```

**DAU/MAU-Stickiness** – siehe [[product-metrics-framework]] für das vollständige Muster.

### Python + SQL Integration {#python-sql-integration}

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

## Gotchas {#gotchas}

- Die Ausführungsreihenfolge ist wichtig: Ein Spaltenalias aus SELECT kann nicht in der WHERE-Klausel verwendet werden (WHERE wird vor SELECT ausgeführt)
- NULL-Vergleiche: `WHERE col = NULL` liefert nie einen Treffer – stattdessen `WHERE col IS NULL` verwenden
- Window Functions reduzieren die Zeilenanzahl nicht – sie eignen sich, wenn Berechnungen pro Zeile zusammen mit Aggregaten benötigt werden
- Korrelierte Subqueries werden einmal pro äußerer Zeile ausgeführt und können extrem langsam sein – JOINs oder CTEs bevorzugen
- `HAVING` filtert nach der Aggregation, `WHERE` filtert davor – die Verwechslung ist ein häufiger Fehler

## See Also {#see-also}

- [[pandas-data-analysis]] – Python-Entsprechung zu SQL-Operationen
- [[cohort-retention-analysis]] – SQL-Muster für Cohort Retention
- [[tableau-fundamentals]] – SQL in Tableau Custom SQL
- [[powerbi-fundamentals]] – DAX als Alternative zu SQL
