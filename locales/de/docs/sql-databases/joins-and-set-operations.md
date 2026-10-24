---
title: "JOINs und Mengenoperationen"
category: concepts
tags: [sql-databases, sql, join, inner-join, left-join, cross-join, union, intersect, except, anti-join]
level: 3
source_sha256: 936e7d1b2431f0399976db70e839bb3953888984b7eb359a7e2f8aaa4fac2492
translation: machine
translated_at: '2026-10-24'
---
# JOINs und Mengenoperationen {#joins-and-set-operations}

JOINs kombinieren Zeilen aus zwei oder mehr Tabellen anhand zusammengehöriger Spalten. Mengenoperationen kombinieren Ergebnismengen vertikal. Beide sind grundlegend für relationale Abfragen.

## Kernfakten {#key-facts}

- INNER JOIN liefert nur übereinstimmende Zeilen aus beiden Tabellen
- LEFT JOIN liefert alle Zeilen der linken Tabelle, mit NULL-Werten, wenn es rechts keine Übereinstimmung gibt
- CROSS JOIN erzeugt ein kartesisches Produkt (jede Zeile wird mit jeder Zeile kombiniert)
- JOIN-Spalten sollten für die Performance immer indiziert sein
- UNION entfernt Duplikate (erfordert Sortierung); UNION ALL behält Duplikate bei (schneller)
- MySQL bietet kein natives FULL OUTER JOIN - es wird mit einem UNION aus LEFT und RIGHT JOIN emuliert

## Muster {#patterns}

### INNER JOIN {#inner-join}
```sql
SELECT u.firstname, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### LEFT JOIN (LEFT OUTER JOIN) {#left-join-left-outer-join}
```sql
SELECT u.firstname, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Anti-join: find users with no orders
SELECT u.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### CROSS JOIN {#cross-join}
```sql
-- Cartesian product: every size paired with every color
SELECT * FROM sizes CROSS JOIN colors;
```

### Self-JOIN {#self-join}
```sql
-- Employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### JOINs über mehrere Tabellen {#multi-table-joins}
```sql
SELECT c.name AS city, co.name AS country, cl.language
FROM city c
JOIN country co ON c.country_code = co.code
JOIN country_language cl ON co.code = cl.country_code
WHERE cl.is_official = 'T';
```

### JOIN mit Aggregation {#join-with-aggregation}
```sql
SELECT u.firstname, COUNT(pm.id) AS msg_count
FROM users u
LEFT JOIN private_messages pm ON u.id = pm.sender_id
GROUP BY u.id, u.firstname
ORDER BY msg_count DESC;
```

### Mengenoperationen {#set-operations}
```sql
-- UNION: combine results, remove duplicates
SELECT city FROM customers UNION SELECT city FROM suppliers;

-- UNION ALL: combine results, keep duplicates (faster)
SELECT city FROM customers UNION ALL SELECT city FROM suppliers;

-- INTERSECT: rows in both (PostgreSQL; MySQL uses INNER JOIN or IN)
SELECT genre FROM rock_albums INTERSECT SELECT genre FROM metal_albums;

-- EXCEPT: rows in first but not second (MySQL: LEFT JOIN WHERE IS NULL)
SELECT genre FROM all_albums EXCEPT SELECT genre FROM jazz_albums;
```

### FULL OUTER JOIN (MySQL-Workaround) {#full-outer-join-mysql-workaround}
```sql
-- MySQL doesn't support FULL OUTER JOIN directly
SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.t1_id
UNION
SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.t1_id;
```

## Stolperfallen {#gotchas}

- Die implizite Join-Syntax (`FROM t1, t2 WHERE t1.id = t2.fk`) ist ein Anti-Pattern - verwende immer das explizite JOIN
- Mengenoperationen erfordern die gleiche Anzahl an Spalten und kompatible Datentypen
- Spaltennamen im Ergebnis von UNION stammen von der ersten Abfrage
- JOINs sind im Allgemeinen schneller als korrelierte Subqueries
- Eine fehlende JOIN-Bedingung erzeugt versehentlich ein kartesisches Produkt (sehr große Ergebnismenge)

## Siehe auch {#see-also}

- [[subqueries-and-ctes]] - EXISTS als Alternative zu JOINs
- [[index-strategies]] - Indizierung von FK-Spalten für die JOIN-Performance
- [[query-optimization-explain]] - Hash Join vs. Merge Join vs. Nested Loop
