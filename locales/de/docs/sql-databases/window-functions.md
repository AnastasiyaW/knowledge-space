---
title: "Fensterfunktionen"
category: concepts
tags: [sql-databases, sql, window-function, row-number, rank, lag, lead, running-total, partition-by]
level: 3
source_sha256: 6a651b88b1827fce94dd391f8a87196aa83f1e07df3c0d25038863484c4c5242
translation: machine
translated_at: '2026-10-24'
---
# Fensterfunktionen {#window-functions}

Fensterfunktionen führen Berechnungen über eine Menge von Zeilen durch, die mit der aktuellen Zeile in Beziehung stehen, ohne die Zeilen wie GROUP BY zusammenzufassen. Sie arbeiten auf einem „Fenster“, das durch die Klauseln PARTITION BY und ORDER BY definiert wird.

## Wichtige Fakten {#key-facts}

- Fensterfunktionen werden nach WHERE, GROUP BY und HAVING ausgeführt – sie sehen das gefilterte bzw. aggregierte Ergebnis
- PARTITION BY unterteilt die Zeilen in Gruppen; ORDER BY legt die Reihenfolge innerhalb jeder Partition fest
- Die Frame-Klausel (ROWS BETWEEN) steuert, welche Zeilen die Funktion berücksichtigt
- Standard-Frame: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, sofern ORDER BY vorhanden ist
- Fensterfunktionen können nicht in WHERE oder HAVING verwendet werden – bei Bedarf in eine Subquery oder CTE auslagern

## Muster {#patterns}

### Rangfunktionen {#ranking-functions}
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

### Aggregierte Fensterfunktionen {#aggregate-window-functions}
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

### Offset-Funktionen {#offset-functions}
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

### Angabe des Fensterrahmens {#window-frame-specification}
```sql
-- ROWS BETWEEN controls which rows the function sees:
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW    -- cumulative from start
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW            -- rolling 3-row window
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- entire partition
ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING             -- current + next row
```

### Benannte Fenster (Wiederverwendung) {#named-windows-reuse}
```sql
SELECT
  ROW_NUMBER() OVER w AS rn,
  SUM(amount) OVER w AS running_total
FROM orders
WINDOW w AS (PARTITION BY user_id ORDER BY created_at);
```

## Fallstricke {#gotchas}

- `LAST_VALUE` sieht mit dem Standard-Frame nur bis zur aktuellen Zeile – für den tatsächlich letzten Wert `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` verwenden
- ROWS vs. RANGE: ROWS zählt physische Zeilen, RANGE fasst Zeilen mit gleichen ORDER-BY-Werten zusammen
- Fensterfunktionen können nicht verschachtelt werden: `SUM(ROW_NUMBER() OVER (...)) OVER (...)` ist ungültig
- Performance: Jede Fensterfunktion kann einen eigenen Sortierdurchlauf erfordern

## Siehe auch {#see-also}

- [[aggregate-functions-group-by]] - GROUP-BY-Aggregation (fasst Zeilen zusammen)
- [[query-optimization-explain]] - Verständnis der Sortierkosten durch Fensterfunktionen
- [[select-fundamentals]] - CASE-Ausdrücke in Kombination mit Fensterfunktionen
