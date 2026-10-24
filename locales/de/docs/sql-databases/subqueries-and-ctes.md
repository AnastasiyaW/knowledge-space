---
title: "Unterabfragen und CTEs"
category: concepts
tags: [sql-databases, sql, subquery, cte, common-table-expression, exists, derived-table, correlated]
level: 3
source_sha256: 94ef2760a1a68f5966909b5560a65e3fab391dbb8b9d77262335c4f7a4780079
translation: machine
translated_at: '2026-10-24'
---
# Unterabfragen und CTEs {#subqueries-and-ctes}

Unterabfragen sind Abfragen, die in andere Abfragen eingebettet sind. CTEs (Common Table Expressions) stellen benannte, wiederverwendbare Abfrageblöcke bereit, die komplexes SQL besser lesbar machen.

## Wichtige Fakten {#key-facts}

- Skalare Unterabfragen liefern einen einzelnen Wert zurück; Tabellen-Unterabfragen liefern mehrere Zeilen
- Korrelierte Unterabfragen werden einmal pro äußerer Zeile ausgeführt (kann teuer sein)
- EXISTS bricht beim ersten Treffer ab – effizienter als IN für Existenzprüfungen
- CTEs werden mit dem Schlüsselwort `WITH` definiert und können mehrere benannte Blöcke verketten
- PostgreSQL materialisiert CTEs standardmäßig (vor Version 12); für Inlining wird der Hint `NOT MATERIALIZED` verwendet

## Muster {#patterns}

### Skalare Unterabfrage {#scalar-subquery}
```sql
SELECT * FROM users
WHERE id = (SELECT sender_id FROM messages GROUP BY sender_id ORDER BY COUNT(*) DESC LIMIT 1);

-- Scalar subquery in SELECT
SELECT u.name,
  (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;
```

### IN-Unterabfrage {#in-subquery}
```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);

-- NOT IN: find users without orders
SELECT * FROM users WHERE id NOT IN (
  SELECT DISTINCT sender_id FROM messages WHERE sender_id IS NOT NULL
);
```

### EXISTS-Unterabfrage {#exists-subquery}
```sql
-- Users who have at least one order
SELECT * FROM users u WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 1000
);

-- Anti-pattern replacement: safer than NOT IN
SELECT * FROM users u WHERE NOT EXISTS (
  SELECT 1 FROM messages m WHERE m.sender_id = u.id
);
```

### Abgeleitete Tabelle (Unterabfrage in FROM) {#derived-table-subquery-in-from}
```sql
SELECT avg_amount FROM (
  SELECT user_id, AVG(amount) AS avg_amount
  FROM orders GROUP BY user_id
) AS user_avgs
WHERE avg_amount > 500;
```

### CTE (Common Table Expression) {#cte-common-table-expression}
```sql
WITH active_users AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  WHERE created_at > '2024-01-01'
  GROUP BY user_id
),
high_value AS (
  SELECT user_id, SUM(amount) AS total
  FROM orders
  GROUP BY user_id
  HAVING total > 10000
)
SELECT u.*, au.order_count, hv.total
FROM users u
JOIN active_users au ON u.id = au.user_id
JOIN high_value hv ON u.id = hv.user_id;
```

### Rekursive CTE {#recursive-cte}
```sql
-- Organizational hierarchy
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, ot.depth + 1
  FROM employees e
  JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY depth, name;
```

## Fallstricke {#gotchas}

- **NOT IN mit NULL-Werten**: Liefert die Unterabfrage auch nur einen NULL-Wert, gibt `NOT IN` für ALLE Zeilen ein leeres Ergebnis zurück – immer `WHERE col IS NOT NULL` ergänzen oder stattdessen NOT EXISTS verwenden
- Korrelierte Unterabfragen laufen einmal pro äußerer Zeile – nach Möglichkeit als JOIN umschreiben
- `EXISTS` prüft nur die Existenz, nicht die Werte – `SELECT 1` im Inneren ist üblich
- CTEs in PostgreSQL < 12 sind Optimierungsbarrieren (werden immer materialisiert)
- MySQL unterstützt rekursive CTEs erst ab Version 8.0

## Siehe auch {#see-also}

- [[select-fundamentals]] - grundlegende WHERE-Filterung
- [[joins-and-set-operations]] - JOINs als Alternative zu Unterabfragen
- [[window-functions]] - Analysen ohne Unterabfragen
