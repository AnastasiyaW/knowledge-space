---
title: "SELECT-Grundlagen"
category: concepts
tags: [sql-databases, sql, select, where, order-by, limit, filtering, case]
level: 2
source_sha256: 16f849e2d8ff86f430323d964515049dc74b7c4eef4957713acce7c7bd83df43
translation: machine
translated_at: '2026-10-24'
---
# SELECT-Grundlagen {#select-fundamentals}

Die SELECT-Anweisung ist das wichtigste Werkzeug zum Lesen von Daten aus relationalen Datenbanken. Die Beherrschung ihrer Klauseln und der Ausführungsreihenfolge ist unerlässlich für das Schreiben effizienter Abfragen.

## Ausführungsreihenfolge von Abfragen {#query-execution-order}

Die logische Verarbeitungsreihenfolge unterscheidet sich von der geschriebenen Syntax:

```sql
FROM / JOIN  ->  WHERE  ->  GROUP BY  ->  HAVING  ->  SELECT  ->  DISTINCT  ->  ORDER BY  ->  LIMIT / OFFSET
```

Dies erklärt, warum Spaltenaliase in ORDER BY funktionieren, nicht aber in WHERE.

## Wichtige Fakten {#key-facts}

- `SELECT *` ist in Produktivumgebungen schädlich - verhindert Index-only-Scans, lädt TOAST-Daten, erhöht die Netzwerkkosten und ist unvorhersehbar, wenn Spalten hinzugefügt werden
- `DISTINCT` erfordert Sortierung/Hashing - nach Möglichkeit vermeiden
- `LIMIT N OFFSET M` verschlechtert sich linear mit M (scannt und verwirft M Zeilen)
- SQL-Schlüsselwörter sind nicht case-sensitiv; üblich sind GROSSGESCHRIEBENE Schlüsselwörter und kleingeschriebene Bezeichner
- MySQL `LIKE` ist standardmäßig nicht case-sensitiv; PostgreSQL `LIKE` ist case-sensitiv (stattdessen `ILIKE` verwenden)

## Muster {#patterns}

### Auswahl einfacher Spalten {#basic-column-selection}
```sql
SELECT * FROM users;
SELECT firstname, lastname FROM users;
SELECT firstname AS name, lastname AS surname FROM users;
SELECT DISTINCT city FROM users;
```

### Filtern mit WHERE-Klausel {#where-clause-filtering}
```sql
-- Comparison: =, !=, <>, <, >, <=, >=
SELECT * FROM users WHERE age > 25;
SELECT * FROM users WHERE city = 'Moscow' AND age >= 18;

-- Range (inclusive both ends)
SELECT * FROM users WHERE age BETWEEN 18 AND 65;

-- Set membership
SELECT * FROM users WHERE city IN ('Moscow', 'London', 'Tokyo');

-- Pattern matching (% = any chars, _ = one char)
SELECT * FROM users WHERE name LIKE 'A%';
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- NULL checks (never use = NULL)
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;
```

### ORDER BY und LIMIT {#order-by-and-limit}
```sql
SELECT * FROM users ORDER BY lastname ASC, firstname DESC;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- skip 20, take 10
```

### Berechnete Felder und CASE {#computed-fields-and-case}
```sql
SELECT name, population / surface_area AS density FROM country;
SELECT CONCAT(name, ' (', code, ')') AS info FROM country;  -- MySQL
SELECT name || ' (' || code || ')' AS info FROM country;     -- PostgreSQL

SELECT name,
  CASE
    WHEN age < 18 THEN 'minor'
    WHEN age BETWEEN 18 AND 65 THEN 'adult'
    ELSE 'senior'
  END AS category
FROM users;

-- Simple CASE
SELECT name,
  CASE status WHEN 'A' THEN 'Active' WHEN 'I' THEN 'Inactive' ELSE 'Unknown' END
FROM users;

-- CASE in aggregation
SELECT continent,
  SUM(CASE WHEN life_expectancy > 70 THEN 1 ELSE 0 END) AS healthy_count
FROM country GROUP BY continent;
```

### Keyset-Pagination (Alternative zu OFFSET) {#keyset-pagination-alternative-to-offset}
```sql
-- Instead of slow OFFSET:
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 10;
-- Uses index, constant time regardless of "page number"
```

## Fallstricke {#gotchas}

- `OFFSET 10000 LIMIT 10` scannt und verwirft 10.000 Zeilen - bei großen Offsets Keyset-Pagination verwenden
- `NULL`-Vergleiche mit `=` oder `!=` ergeben immer UNKNOWN (Zeile wird ausgeschlossen)
- `WHERE phone != '123'` liefert KEINE Zeilen zurück, in denen phone IS NULL ist - `OR phone IS NULL` ergänzen
- Sortierung nach Spaltenposition (`ORDER BY 2`) ist zulässig, aber fragil - in Produktivumgebungen vermeiden
- Keyset-Pagination kann nicht zu einer beliebigen Seite springen - nur "nächste"/"vorherige"

## Siehe auch {#see-also}

- [[aggregate-functions-group-by]] - COUNT, SUM, AVG mit GROUP BY und HAVING
- [[joins-and-set-operations]] - Kombinieren von Daten aus mehreren Tabellen
- [[subqueries-and-ctes]] - verschachtelte Abfragen und Common Table Expressions
- [[window-functions]] - zeilenbezogene Berechnungen über Partitionen hinweg
