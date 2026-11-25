---
title: "DML - INSERT, UPDATE, DELETE"
category: concepts
tags: [sql-databases, sql, insert, update, delete, truncate, dml, bulk-operations]
level: 3
source_sha256: c9427d3b0bf946cccc283c3687cc5c652aae8d41d229a02d9dd94dcc0bdbee6c
translation: machine
translated_at: '2026-10-24'
---
# DML - INSERT, UPDATE, DELETE {#dml-insert-update-delete}

Data Manipulation Language (DML) Anweisungen verändern Tabellendaten. Das Verständnis ihres Verhaltens, ihrer Performance-Eigenschaften und ihrer Auswirkungen auf Transaktionen ist für Produktivsysteme entscheidend.

## Key Facts {#key-facts}

- INSERT, UPDATE, DELETE sind transaktional (können zurückgerollt werden)
- TRUNCATE ist in den meisten RDBMS DDL - schneller als DELETE, kann aber in MySQL nicht zurückgerollt werden bzw. ist in PostgreSQL transaktional
- Ein Multi-Row-INSERT ist deutlich schneller als einzelne INSERT-Anweisungen
- UPDATE schreibt in PostgreSQL die gesamte Zeile neu (MVCC); InnoDB ändert nach Möglichkeit direkt an Ort und Stelle
- DELETE markiert Zeilen nur zur Entfernung - der Speicher wird durch VACUUM (PostgreSQL) bzw. durch den Hintergrund-Purge (InnoDB) freigegeben

## Patterns {#patterns}

### INSERT {#insert}
```sql
-- Single row
INSERT INTO users (firstname, lastname, email) VALUES ('Alice', 'Smith', 'alice@example.com');

-- Multi-row (much faster than individual inserts)
INSERT INTO users (firstname, lastname) VALUES ('Bob', 'Jones'), ('Carol', 'Lee');

-- INSERT from SELECT
INSERT INTO archive_orders SELECT * FROM orders WHERE created_at < '2023-01-01';

-- INSERT with RETURNING (PostgreSQL)
INSERT INTO users (name, email) VALUES ('Dave', 'dave@example.com') RETURNING id, created_at;

-- UPSERT: INSERT ... ON CONFLICT (PostgreSQL)
INSERT INTO users (email, name) VALUES ('bob@example.com', 'Bob')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- UPSERT: INSERT ... ON DUPLICATE KEY UPDATE (MySQL)
INSERT INTO users (email, name) VALUES ('bob@example.com', 'Bob')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

### UPDATE {#update}
```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
UPDATE users SET firstname = 'New', lastname = 'Name' WHERE id = 5;

-- Batch update with calculated values
UPDATE orders SET total = quantity * unit_price WHERE total IS NULL;

-- UPDATE from another table (PostgreSQL)
UPDATE orders o SET status = 'archived'
FROM users u WHERE o.user_id = u.id AND u.deleted = true;
```

### DELETE {#delete}
```sql
DELETE FROM users WHERE id = 1;
DELETE FROM orders WHERE created_at < '2020-01-01';

-- Delete with subquery
DELETE FROM album WHERE band_id IN (SELECT id FROM band WHERE country = 'DE');
```

### TRUNCATE {#truncate}
```sql
TRUNCATE TABLE users;              -- fast delete all rows
TRUNCATE TABLE users RESTART IDENTITY;  -- reset auto_increment (PostgreSQL)
-- MySQL: TRUNCATE always resets AUTO_INCREMENT
```

### Batch-Operationen für große Tabellen {#batch-operations-for-large-tables}
```sql
-- Avoid updating millions of rows at once - batch in chunks
UPDATE users SET status = 'inactive'
WHERE id IN (SELECT id FROM users WHERE last_login < '2023-01-01' LIMIT 10000);
-- Repeat until no rows affected, VACUUM between batches (PostgreSQL)
```

### CREATE TABLE AS SELECT {#create-table-as-select}
```sql
CREATE TABLE rock_albums AS SELECT * FROM album WHERE genre = 'rock';
```

## Gotchas {#gotchas}

- TRUNCATE kann in MySQL nicht zurückgerollt werden (es ist DDL); PostgreSQL-TRUNCATE ist transaktional
- Große DELETE/UPDATE-Operationen können zu Lock-Contention und Bloat führen - daher in Batches aufteilen
- PostgreSQL-UPDATE erzeugt eine neue Zeilenversion (Dead Tuple) - VACUUM ist nötig, um den Speicher zurückzugewinnen
- Das Hinzufügen einer Spalte mit DEFAULT auf einer großen Tabelle erfordert vor PG 11 einen Batch-Update-Ansatz
- Bei UPDATE/DELETE in Produktivsystemen immer ein WHERE angeben - fehlt es, sind alle Zeilen betroffen
- Foreign-Key-CASCADE kann unerwartet zu Massenlöschungen führen

## See Also {#see-also}

- [[ddl-schema-management]] - CREATE TABLE, ALTER TABLE, Constraints
- [[transactions-and-acid]] - Einbetten von DML in Transaktionen
- [[postgresql-mvcc-vacuum]] - Dead Tuples durch UPDATE/DELETE
- [[data-types-and-nulls]] - Datentypen für INSERT-Werte
