---
title: "Fonctions de fenêtrage"
category: concepts
tags: [sql-databases, sql, window-function, row-number, rank, lag, lead, running-total, partition-by]
level: 3
source_sha256: 6a651b88b1827fce94dd391f8a87196aa83f1e07df3c0d25038863484c4c5242
translation: machine
translated_at: '2026-10-24'
---
# Fonctions de fenêtrage {#window-functions}

Les fonctions de fenêtrage effectuent des calculs sur un ensemble de lignes liées à la ligne courante, sans regrouper les lignes comme le fait GROUP BY. Elles opèrent sur une « fenêtre » définie par les clauses PARTITION BY et ORDER BY.

## Points clés {#key-facts}

- Les fonctions de fenêtrage s'exécutent après WHERE, GROUP BY et HAVING : elles voient le résultat filtré ou agrégé
- PARTITION BY divise les lignes en groupes ; ORDER BY détermine l'ordre au sein de chaque partition
- La clause de cadre (ROWS BETWEEN) contrôle les lignes que la fonction prend en compte
- Cadre par défaut : `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` lorsque ORDER BY est présent
- Impossible d'utiliser des fonctions de fenêtrage dans WHERE ou HAVING : encapsuler dans une sous-requête ou un CTE si nécessaire

## Modèles {#patterns}

### Fonctions de classement {#ranking-functions}
```sql
-- ROW_NUMBER: unique sequential number (no ties)
SELECT *, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank FROM employees;

-- With partitioning: rank within each department
SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- RANK: same rank for ties, gaps after (1, 2, 2, 4)
SELECT *, RANK() OVER (ORDER BY salary DESC) AS rank FROM employees;

-- DENSE_RANK: same rank for ties, no gaps (1, 2, 2, 3)
SELECT *, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank FROM employees;

-- NTILE: divide into N equal groups
SELECT *, NTILE(4) OVER (ORDER BY salary) AS quartile FROM employees;
```

### Fonctions d'agrégation fenêtrées {#aggregate-window-functions}
```sql
-- Running total
SELECT *, SUM(amount) OVER (ORDER BY created_at) AS running_total FROM orders;

-- Moving average (3-row window)
SELECT *, AVG(amount) OVER (
  ORDER BY created_at ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS moving_avg FROM orders;

-- Cumulative count per partition
SELECT department, hire_date,
  COUNT(*) OVER (PARTITION BY department ORDER BY hire_date) AS running_count
FROM employees;
```

### Fonctions de décalage {#offset-functions}
```sql
-- LAG: access previous row value
SELECT *, LAG(amount, 1) OVER (ORDER BY created_at) AS prev_amount FROM orders;

-- LEAD: access next row value
SELECT *, LEAD(amount, 1) OVER (ORDER BY created_at) AS next_amount FROM orders;

-- Sales difference from previous period
SELECT *, amount - LAG(amount, 1) OVER (ORDER BY created_at) AS diff FROM orders;

-- FIRST_VALUE / LAST_VALUE
SELECT *, FIRST_VALUE(name) OVER (PARTITION BY dept ORDER BY salary DESC) AS top_earner
FROM employees;
```

### Spécification du cadre de fenêtre {#window-frame-specification}
```sql
-- ROWS BETWEEN controls which rows the function sees:
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW    -- cumulative from start
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW            -- rolling 3-row window
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- entire partition
ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING             -- current + next row
```

### Fenêtres nommées (réutilisation) {#named-windows-reuse}
```sql
SELECT
  ROW_NUMBER() OVER w AS rn,
  SUM(amount) OVER w AS running_total
FROM orders
WINDOW w AS (PARTITION BY user_id ORDER BY created_at);
```

## Pièges {#gotchas}

- `LAST_VALUE` avec le cadre par défaut ne voit que jusqu'à la ligne courante : utiliser `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` pour obtenir la vraie dernière valeur
- ROWS ou RANGE : ROWS compte les lignes physiques, RANGE regroupe les lignes ayant des valeurs ORDER BY identiques
- Les fonctions de fenêtrage ne peuvent pas être imbriquées : `SUM(ROW_NUMBER() OVER (...)) OVER (...)` est invalide
- Performance : chaque fonction de fenêtrage peut nécessiter une passe de tri distincte

## Voir aussi {#see-also}

- [[aggregate-functions-group-by]] - agrégation avec GROUP BY (regroupe les lignes)
- [[query-optimization-explain]] - comprendre les coûts de tri liés aux fonctions de fenêtrage
- [[select-fundamentals]] - expressions CASE combinées aux fonctions de fenêtrage
