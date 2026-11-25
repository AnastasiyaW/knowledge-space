---
title: "SQL pour l'analyse de données"
category: tools
tags: [bi-analytics, sql, window-functions, joins, cte, aggregation, analytics]
level: 3
source_sha256: a3e39795621cafbed5f732b8599a7e90898d10b43e7554d4bb20146a5acbb8f9
translation: machine
translated_at: '2026-10-24'
---
# SQL pour l'analyse de données {#sql-for-analytics}

SQL est l'outil de base des analystes de données, mais maîtriser la syntaxe SQL ne suffit pas à faire de vous un analyste. La vraie compétence tient à la réflexion analytique : savoir quoi mesurer et pourquoi. Cette entrée présente les patterns SQL particulièrement utiles pour la BI et l'analyse produit.

## Points clés {#key-facts}

- Ordre d'exécution SQL (important pour le débogage) : FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
- Les fonctions de fenêtrage calculent sur une « fenêtre » de lignes sans regrouper les lignes
- Les CTE (Common Table Expressions) sont plus lisibles que les sous-requêtes imbriquées
- Patterns spécifiques à l'analytique : rétention par cohorte, analyse de tunnel (funnel), stickiness DAU/MAU
- Connecter Python à des bases SQL permet de combiner l'interrogation SQL et l'analyse avec pandas

## Patterns {#patterns}

### Structure de base d'une requête {#core-query-structure}

```sql
SELECT column1, column2, COUNT(*) as count
FROM table_name
WHERE condition
GROUP BY column1, column2
HAVING aggregate_condition
ORDER BY column1 DESC
LIMIT 100;
```

### Filtrage {#filtering}

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

### JOIN {#joins}

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

### CTE (Common Table Expressions) {#ctes-common-table-expressions}

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

### Fonctions de fenêtrage {#window-functions}

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

### Patterns SQL pour l'analytique {#analytics-sql-patterns}

**Rétention par cohorte** - voir [[cohort-retention-analysis]] pour le pattern complet.

**Analyse de tunnel (funnel) :**
```sql
SELECT
    COUNT(CASE WHEN event = 'page_view' THEN user_id END) as step1,
    COUNT(CASE WHEN event = 'add_to_cart' THEN user_id END) as step2,
    COUNT(CASE WHEN event = 'checkout_start' THEN user_id END) as step3,
    COUNT(CASE WHEN event = 'purchase' THEN user_id END) as step4
FROM events
WHERE event_date = CURRENT_DATE;
```

**Stickiness DAU/MAU** - voir [[product-metrics-framework]] pour le pattern complet.

### Intégration Python + SQL {#python-sql-integration}

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

## Pièges courants {#gotchas}

- L'ordre d'exécution compte : on ne peut pas utiliser un alias de colonne défini dans SELECT dans la clause WHERE (WHERE s'exécute avant SELECT)
- Comparaisons avec NULL : `WHERE col = NULL` ne correspond à aucune ligne, utiliser `WHERE col IS NULL`
- Les fonctions de fenêtrage ne réduisent pas le nombre de lignes : à utiliser quand on a besoin de calculs par ligne à côté d'agrégats
- Les sous-requêtes corrélées s'exécutent une fois par ligne externe et peuvent être extrêmement lentes : préférer les JOIN ou les CTE
- `HAVING` filtre après agrégation, `WHERE` filtre avant : les confondre est une erreur fréquente

## Voir aussi {#see-also}

- [[pandas-data-analysis]] - équivalent Python des opérations SQL
- [[cohort-retention-analysis]] - pattern SQL de rétention par cohorte
- [[tableau-fundamentals]] - SQL dans le Custom SQL de Tableau
- [[powerbi-fundamentals]] - DAX comme alternative à SQL
