---
title: "SQL für Data Engineering"
category: reference
tags: [data-engineering, sql, postgresql, window-functions, cte, joins]
level: 3
source_sha256: 3c210c3044760ed2ab8114bb123b94fe4c049785c86f1d0f71d09c7130e54cc1
translation: machine
translated_at: '2026-10-24'
---
# SQL für Data Engineering {#sql-for-data-engineering}

SQL ist die universelle Sprache für Data Engineering. Dieser Eintrag behandelt DE-spezifische SQL-Muster, darunter Window Functions, CTEs, Query-Optimierung und DWH-orientierte Techniken.

## Ausführungsreihenfolge einer Abfrage {#query-execution-order}

```sql
FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT
```

- `WHERE` filtert Zeilen VOR der Aggregation (keine Aggregatfunktionen erlaubt)
- `HAVING` filtert Gruppen NACH der Aggregation (Aggregatfunktionen sind erlaubt)

## Window Functions {#window-functions}

Berechnen Werte über Zeilen hinweg, ohne diese zu einer Zeile zusammenzufassen (im Gegensatz zu GROUP BY).

```sql
function() OVER (
    PARTITION BY col    -- define groups
    ORDER BY col        -- ordering within group
    ROWS BETWEEN ...    -- frame specification
)
```

### Ranking {#ranking}

```sql
ROW_NUMBER() OVER (ORDER BY salary DESC)  -- unique: 1,2,3,4
RANK()       OVER (ORDER BY salary DESC)  -- ties, gaps: 1,1,3,4
DENSE_RANK() OVER (ORDER BY salary DESC)  -- ties, no gaps: 1,1,2,3
NTILE(4)     OVER (ORDER BY salary)       -- divide into buckets
```

### Offset {#offset}

```sql
LAG(col, 1)    OVER (ORDER BY date)  -- previous row
LEAD(col, 1)   OVER (ORDER BY date)  -- next row
FIRST_VALUE(col) OVER (ORDER BY date)
LAST_VALUE(col)  OVER (ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### Aggregate über Fenster {#aggregates-over-windows}

```sql
SUM(revenue) OVER (ORDER BY date) AS cumulative      -- running total
AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
revenue * 100.0 / SUM(revenue) OVER () AS pct_total  -- percent of total
```

### Frame: ROWS vs. RANGE {#frame-rows-vs-range}

- **ROWS**: physische Zeilenpositionen relativ zur aktuellen Zeile
- **RANGE**: Wertedifferenzen in der ORDER-BY-Spalte
- Standard bei ORDER BY: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

## Häufige Muster {#common-patterns}

### Top N pro Gruppe {#top-n-per-group}

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY category ORDER BY revenue DESC
    ) AS rn
    FROM sales
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Deduplizierung {#deduplication}

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY email ORDER BY created_at DESC
    ) AS rn FROM users
)
SELECT * FROM ranked WHERE rn = 1;
```

### Veränderung zum Vorjahr {#year-over-year-change}

```sql
SELECT month, revenue,
    LAG(revenue, 12) OVER (ORDER BY month) AS last_year,
    (revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
        / LAG(revenue, 12) OVER (ORDER BY month) AS yoy_pct
FROM monthly_stats;
```

### Fehlende Datumswerte finden {#find-missing-dates}

```sql
WITH dates AS (
    SELECT generate_series(MIN(date), MAX(date), '1 day')::date AS d
    FROM orders
)
SELECT d FROM dates LEFT JOIN orders ON orders.date = d
WHERE orders.date IS NULL;
```

## JOIN-Typen {#join-types}

| Typ | Beschreibung |
|------|------|
| INNER | Nur passende Zeilen |
| LEFT | Alle aus links + passende rechts |
| RIGHT | Alle aus rechts + passende links |
| FULL | Alle aus beiden, NULLs bei fehlender Übereinstimmung |
| CROSS | Kartesisches Produkt |
| ANTI | `LEFT JOIN ... WHERE b.key IS NULL` |
| SEMI | `WHERE EXISTS (SELECT 1 FROM b WHERE ...)` |

### Warnung zum kartesischen Produkt {#cartesian-product-warning}

Wenn der Join-Schlüssel in BEIDEN Tabellen Duplikate enthält, vervielfachen sich die Zeilen: 2 linke x 2 rechte = 4 Zeilen. **GROUP BY vor dem JOIN** ausführen, um zu deduplizieren.

## CTEs und rekursive Abfragen {#ctes-and-recursive-queries}

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

## NULL-Behandlung {#null-handling}

```sql
COALESCE(x, y, ...)      -- first non-NULL
NULLIF(x, y)             -- NULL if x=y (prevents division by zero)
SELECT total / NULLIF(count, 0) FROM stats;
```

- `COUNT(column)` schließt NULLs aus; `COUNT(*)` zählt alle Zeilen
- `NULL = NULL` ergibt NULL, nicht TRUE. Stattdessen `IS NULL` verwenden
- Mehrere NULLs bilden in DISTINCT/GROUP BY eine einzige Gruppe

## EXPLAIN {#explain}

```sql
EXPLAIN ANALYZE SELECT ...;      -- actual timings
EXPLAIN (BUFFERS, ANALYZE) ...;  -- buffer usage
```

Werkzeug: [explain.tensor.ru](https://explain.tensor.ru) für die visuelle Analyse von Ausführungsplänen.

## Fallstricke {#gotchas}
- `LAST_VALUE()` mit Standard-Frame sieht nur bis zur aktuellen Zeile - UNBOUNDED FOLLOWING muss gesetzt werden
- Ein kartesisches Produkt verfälscht Aggregate nach einem JOIN stillschweigend
- `COUNT(DISTINCT col)` statt `DISTINCT COUNT(col)`
- Subqueries mit `LIMIT 1` liefern genau eine Zeile oder keine - für Skalarwerte sicher
- Die Reihenfolge der Spalten in `GROUP BY` ist unerheblich; in `ORDER BY` ist sie es

## Siehe auch {#see-also}
- [[clickhouse]] - ClickHouse-spezifisches SQL
- [[greenplum-mpp]] - MPP-spezifisches SQL
- [[data-modeling]] - Schema-Design
- [[etl-elt-pipelines]] - SQL im ELT-Kontext
