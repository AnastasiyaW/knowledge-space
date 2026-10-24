---
title: "SQL pour l'ingénierie des données"
category: reference
tags: [data-engineering, sql, postgresql, window-functions, cte, joins]
level: 3
source_sha256: 3c210c3044760ed2ab8114bb123b94fe4c049785c86f1d0f71d09c7130e54cc1
translation: machine
translated_at: '2026-10-24'
---
# SQL pour l'ingénierie des données {#sql-for-data-engineering}

SQL est le langage universel de l'ingénierie des données. Cette entrée couvre les patrons SQL spécifiques à l'ingénierie des données, notamment les fonctions de fenêtrage, les CTE, l'optimisation des requêtes et les techniques orientées entrepôt de données (DWH).

## Ordre d'exécution des requêtes {#query-execution-order}

```sql
FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT
```

- `WHERE` filtre les lignes AVANT l'agrégation (sans fonctions d'agrégation)
- `HAVING` filtre les groupes APRÈS l'agrégation (peut utiliser des agrégats)

## Fonctions de fenêtrage {#window-functions}

Calcule sur des lignes sans les regrouper (contrairement à GROUP BY).

```sql
function() OVER (
    PARTITION BY col    -- define groups
    ORDER BY col        -- ordering within group
    ROWS BETWEEN ...    -- frame specification
)
```

### Classement {#ranking}

```sql
ROW_NUMBER() OVER (ORDER BY salary DESC)  -- unique: 1,2,3,4
RANK()       OVER (ORDER BY salary DESC)  -- ties, gaps: 1,1,3,4
DENSE_RANK() OVER (ORDER BY salary DESC)  -- ties, no gaps: 1,1,2,3
NTILE(4)     OVER (ORDER BY salary)       -- divide into buckets
```

### Décalage {#offset}

```sql
LAG(col, 1)    OVER (ORDER BY date)  -- previous row
LEAD(col, 1)   OVER (ORDER BY date)  -- next row
FIRST_VALUE(col) OVER (ORDER BY date)
LAST_VALUE(col)  OVER (ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### Agrégats sur fenêtres {#aggregates-over-windows}

```sql
SUM(revenue) OVER (ORDER BY date) AS cumulative      -- running total
AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
revenue * 100.0 / SUM(revenue) OVER () AS pct_total  -- percent of total
```

### Cadre : ROWS vs RANGE {#frame-rows-vs-range}

- **ROWS** : positions physiques des lignes par rapport à la ligne courante
- **RANGE** : différences de valeurs dans la colonne de ORDER BY
- Par défaut avec ORDER BY : `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

## Patrons courants {#common-patterns}

### Top N par groupe {#top-n-per-group}

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY category ORDER BY revenue DESC
    ) AS rn
    FROM sales
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Déduplication {#deduplication}

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY email ORDER BY created_at DESC
    ) AS rn FROM users
)
SELECT * FROM ranked WHERE rn = 1;
```

### Variation d'une année sur l'autre {#year-over-year-change}

```sql
SELECT month, revenue,
    LAG(revenue, 12) OVER (ORDER BY month) AS last_year,
    (revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
        / LAG(revenue, 12) OVER (ORDER BY month) AS yoy_pct
FROM monthly_stats;
```

### Trouver les dates manquantes {#find-missing-dates}

```sql
WITH dates AS (
    SELECT generate_series(MIN(date), MAX(date), '1 day')::date AS d
    FROM orders
)
SELECT d FROM dates LEFT JOIN orders ON orders.date = d
WHERE orders.date IS NULL;
```

## Types de JOIN {#join-types}

| Type | Description |
|------|------|
| INNER | Uniquement les lignes correspondantes |
| LEFT | Toutes les lignes de gauche + les correspondances de droite |
| RIGHT | Toutes les lignes de droite + les correspondances de gauche |
| FULL | Toutes les lignes des deux tables, NULL en l'absence de correspondance |
| CROSS | Produit cartésien |
| ANTI | `LEFT JOIN ... WHERE b.key IS NULL` |
| SEMI | `WHERE EXISTS (SELECT 1 FROM b WHERE ...)` |

### Avertissement sur le produit cartésien {#cartesian-product-warning}

Lorsque la clé de jointure contient des doublons dans LES DEUX tables, les lignes se multiplient : 2 lignes à gauche x 2 lignes à droite = 4 lignes. **Faire un GROUP BY avant le JOIN** pour dédupliquer.

## CTE et requêtes récursives {#ctes-and-recursive-queries}

```sql
WITH RECURSIVE hierarchy AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e JOIN hierarchy h ON e.manager_id = h.id
)
SELECT * FROM hierarchy;
```

## Gestion des NULL {#null-handling}

```sql
COALESCE(x, y, ...)      -- first non-NULL
NULLIF(x, y)             -- NULL if x=y (prevents division by zero)
SELECT total / NULLIF(count, 0) FROM stats;
```

- `COUNT(colonne)` exclut les NULL ; `COUNT(*)` compte toutes les lignes
- `NULL = NULL` vaut NULL, et non TRUE. Utiliser `IS NULL`
- Plusieurs NULL = un seul groupe dans DISTINCT/GROUP BY

## EXPLAIN {#explain}

```sql
EXPLAIN ANALYZE SELECT ...;      -- actual timings
EXPLAIN (BUFFERS, ANALYZE) ...;  -- buffer usage
```

Outil : [explain.tensor.ru](https://explain.tensor.ru) pour l'analyse visuelle des plans d'exécution.

## Pièges à éviter {#gotchas}
- `LAST_VALUE()` avec le cadre par défaut ne voit que jusqu'à la ligne courante - il faut définir UNBOUNDED FOLLOWING
- Le produit cartésien gonfle silencieusement les agrégats après un JOIN
- `COUNT(DISTINCT col)` et non `DISTINCT COUNT(col)`
- Les sous-requêtes avec `LIMIT 1` renvoient une ligne ou aucune - sûr pour un scalaire
- L'ordre des colonnes dans `GROUP BY` n'a pas d'importance ; celui de `ORDER BY` en a une

## Voir aussi {#see-also}
- [[clickhouse]] - SQL spécifique à ClickHouse
- [[greenplum-mpp]] - SQL spécifique à MPP
- [[data-modeling]] - conception de schéma
- [[etl-elt-pipelines]] - SQL dans le contexte ELT
