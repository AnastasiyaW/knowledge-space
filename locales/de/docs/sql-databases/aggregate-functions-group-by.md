---
title: "Aggregatfunktionen und GROUP BY"
category: concepts
tags: [sql-databases, sql, aggregation, group-by, having, count, sum, avg]
level: 3
source_sha256: cb0df95efe3ef4f09ff2e423a536bf2950e93522a3a05c0b28a68d9c5f54554a
translation: machine
translated_at: '2026-10-24'
---
# Aggregatfunktionen und GROUP BY {#aggregate-functions-and-group-by}

Aggregatfunktionen fassen mehrere Zeilen zu einzelnen zusammenfassenden Werten zusammen. GROUP BY unterteilt die Zeilen vor der Aggregation in Gruppen, während HAVING die resultierenden Gruppen filtert.

## Wichtige Fakten {#key-facts}

- `COUNT(*)` zählt alle Zeilen einschließlich NULL-Werten; `COUNT(column)` zählt nur Nicht-NULL-Werte
- `SUM`, `AVG`, `MIN`, `MAX` ignorieren alle NULL-Werte
- `GROUP BY` fasst alle NULL-Werte zu einer einzigen Gruppe zusammen
- HAVING filtert Gruppen nach der Aggregation; WHERE filtert Zeilen vor der Gruppierung
- Aggregatfunktionen können nicht in der WHERE-Klausel verwendet werden

## Muster {#patterns}

### Einfache Aggregation {#basic-aggregation}
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT city) FROM users;
SELECT SUM(amount), AVG(amount), MIN(amount), MAX(amount) FROM orders;
```

### GROUP BY {#group-by}
```sql
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
ORDER BY user_count DESC;

-- Multiple grouping columns
SELECT country_code, district, COUNT(*) AS city_count
FROM city
GROUP BY country_code, district;
```

### HAVING (Filter auf aggregierte Ergebnisse) {#having-filter-on-aggregated-results}
```sql
SELECT genre, COUNT(*) AS cnt
FROM album
GROUP BY genre
HAVING COUNT(*) > 5
ORDER BY cnt DESC;

-- Combine WHERE and HAVING
SELECT continent, AVG(life_expectancy) AS avg_life
FROM country
WHERE population > 1000000        -- filter rows before grouping
GROUP BY continent
HAVING avg_life > 70              -- filter groups after aggregation
ORDER BY avg_life DESC;
```

### COUNT-Performance bei großen Tabellen {#count-performance-on-large-tables}

`SELECT COUNT(*) FROM large_table` erfordert einen vollständigen Tabellen- bzw. Index-Scan - MVCC bedeutet, dass unterschiedliche Transaktionen unterschiedliche Zeilenanzahlen sehen.

**Alternativen für Näherungswerte:**
```sql
-- PostgreSQL: approximate from statistics
SELECT reltuples::bigint FROM pg_class WHERE relname = 'large_table';

-- MySQL: approximate from information_schema
SELECT table_rows FROM information_schema.tables
WHERE table_name = 'large_table';
```

Weitere Strategien: eine materialisierte Zähltabelle, die durch Trigger aktualisiert wird, ein Redis-Zähler, der bei INSERT/DELETE erhöht wird, oder HyperLogLog für die Näherung der Anzahl distinkter Werte.

## Fallstricke {#gotchas}

- `AVG` ignoriert NULL-Werte - `AVG` von `[10, NULL, 20]` ist 15, nicht 10
- Spalten im SELECT müssen entweder in GROUP BY vorkommen oder innerhalb von Aggregatfunktionen stehen
- `COUNT(DISTINCT col)` ist langsamer als `COUNT(*)` - erfordert Deduplizierung
- MySQL erlaubt nicht aggregierte Spalten im SELECT ohne GROUP BY (abhängig von sql_mode) - PostgreSQL nicht

## Siehe auch {#see-also}

- [[select-fundamentals]] - WHERE-Klausel und einfache Filterung
- [[window-functions]] - Aggregationen ohne Zusammenfassung der Zeilen
- [[query-optimization-explain]] - Optimierung von Aggregatabfragen
