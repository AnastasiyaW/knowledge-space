---
title: "Index-Strategien"
category: concepts
tags: [sql-databases, index, composite-index, covering-index, partial-index, sargable, index-only-scan, create-index-concurrently]
level: 3
source_sha256: ad276054591fbf1f402fe5979a8cc9b088bcf318e23217472de564e59fec6e28
translation: machine
translated_at: '2026-10-24'
---
# Index-Strategien {#index-strategies}

Indizes beschleunigen Lesezugriffe, verlangsamen aber Schreibzugriffe. Welche Indizes angelegt werden, in welcher Spaltenreihenfolge und von welchem Typ, ist entscheidend für die Performance im Produktivbetrieb.

## Index-Scan-Typen (PostgreSQL) {#index-scan-types-postgresql}

| Scan-Typ | Beschreibung | Wann verwendet |
|-----------|-------------|-----------|
| Sequential Scan | Liest die gesamte Heap-Datei seitenweise | Kein nutzbarer Index, großer Ergebnisanteil, kleine Tabelle |
| Index Scan | Durchläuft den B+Tree, holt passende Heap-Seiten | Selektive Abfrage, wenige passende Zeilen |
| Index-Only Scan | Liefert Daten aus dem Index ohne Heap-Zugriff | Alle Spalten im Index (Covering), Visibility Map ist aktuell |
| Bitmap Index Scan | Erstellt eine Bitmap passender Seiten, liest sequenziell | Mittlere Selektivität, mehrere Indizes kombinierbar |

## Wichtige Fakten {#key-facts}

- Zusammengesetzter Index auf (a, b, c) nutzbar für WHERE a=1, WHERE a=1 AND b=2, aber NICHT für WHERE b=2 allein
- Covering Index enthält alle Spalten, die die Abfrage benötigt - eliminiert den Heap-Zugriff vollständig
- Partieller/gefilterter Index: indiziert nur Zeilen, die einer Bedingung entsprechen (kleiner, schneller zu pflegen)
- SARGable: `WHERE col = 5` nutzt den Index; `WHERE YEAR(col) = 2024` NICHT (Funktion auf der Spalte)
- Jeder Index verursacht Mehraufwand bei INSERT/UPDATE/DELETE - in OLTP-Systemen Überindizierung vermeiden

## Muster {#patterns}

### Zusammengesetzter Index {#composite-index}
```sql
-- Column order matters: equality columns first, then range
CREATE INDEX idx_orders ON orders (status, created_at);
-- Usable for: WHERE status = 'active' AND created_at > '2024-01-01'
-- Usable for: WHERE status = 'active'
-- NOT usable for: WHERE created_at > '2024-01-01' (skips leftmost column)
```

### Covering Index (Index-Only Scan) {#covering-index-index-only-scan}
```sql
-- PostgreSQL: INCLUDE for non-key columns in leaf pages
CREATE INDEX idx_orders_covering ON orders (user_id) INCLUDE (amount, status);
-- Query can be answered entirely from index:
SELECT amount, status FROM orders WHERE user_id = 42;
```

### Partieller/Gefilterter Index {#partialfiltered-index}
```sql
-- Index only active users (much smaller than full index)
CREATE INDEX idx_active_users ON users (email) WHERE status = 'active';
-- Only used when query includes WHERE status = 'active'
```

### CREATE INDEX CONCURRENTLY {#create-index-concurrently}
```sql
-- PostgreSQL: build index without blocking DML
CREATE INDEX CONCURRENTLY idx_name ON table (column);
-- Takes longer, two table scans, can't run in transaction, may fail (cleanup required)

-- MySQL equivalent: online DDL
ALTER TABLE t ADD INDEX idx_name (column), ALGORITHM=INPLACE, LOCK=NONE;
```

### Erzeugen von Testdaten {#generating-test-data}
```sql
-- PostgreSQL: generate millions of rows for index testing
INSERT INTO grades (g) SELECT floor(random() * 100) FROM generate_series(1, 10000000);
```

## Auswahl des Indexes durch den Optimizer {#optimizer-index-selection}

Wenn mehrere Indizes existieren, schätzt der Optimizer die Kosten anhand von:
- Tabellengröße und Statistiken aus `pg_stats`
- Index-Selektivität (welcher Anteil der Zeilen passt)
- Korrelation (physische Reihenfolge vs. Indexreihenfolge)
- Kostenparameter (`seq_page_cost`, `random_page_cost`)

Hint-Mechanismen: Erweiterung `pg_hint_plan` (PostgreSQL), `USE INDEX`/`FORCE INDEX` (MySQL). Dem Optimizer sollte man grundsätzlich vertrauen, solange EXPLAIN ANALYZE nicht zeigt, dass er falsch liegt.

## Besonderheiten von SQL Server {#sql-server-specifics}

- **Columnstore-Indizes:** Spaltenorientierte Speicherung für OLAP. Zeilen werden zu Rowgroups (~1 Mio. Zeilen) zusammengefasst, Verarbeitung im Batch-Modus (~900 Zeilen auf einmal). Mit Rowstore-Indizes kombinierbar.
- **Hash-Indizes:** Nur für speicheroptimierte Tabellen. O(1)-Punktabfragen, nicht für Bereichsabfragen geeignet.
- **Included Columns:** Nicht-Schlüsselspalten im Blattknoten, für Covering ohne Auswirkung auf die Sortierreihenfolge.

### Index-Selektivität und wann man NICHT indiziert {#index-selectivity-and-when-not-to-index}

```sql
-- Check selectivity: values near 1.0 = highly selective (good for index)
SELECT COUNT(DISTINCT status)::float / COUNT(*) AS selectivity FROM orders;
-- 0.0001 (4 statuses / 1M rows) = low selectivity, index may not help

-- Rule of thumb: index useful when selecting < 10-15% of rows
-- For low selectivity columns, bitmap scan may still combine with other indexes
```

### Präfix-Indizes (MySQL) {#prefix-indexes-mysql}

Bei langen Zeichenkettenspalten nur die ersten N Zeichen indizieren:
```sql
-- Full index on email wastes space
CREATE INDEX idx_email ON users (email(20));

-- Find optimal prefix length:
SELECT
    COUNT(DISTINCT LEFT(email, 10)) / COUNT(*) AS sel_10,
    COUNT(DISTINCT LEFT(email, 15)) / COUNT(*) AS sel_15,
    COUNT(DISTINCT LEFT(email, 20)) / COUNT(*) AS sel_20,
    COUNT(DISTINCT email) / COUNT(*) AS sel_full
FROM users;
-- Pick smallest N where selectivity approaches full column selectivity
```

### Funktionale Indizes {#functional-indexes}

```sql
-- PostgreSQL: index on expression
CREATE INDEX idx_lower_email ON users (LOWER(email));
-- Now WHERE LOWER(email) = 'user@example.com' uses the index

-- MySQL 8.0+: functional index
CREATE INDEX idx_year ON events ((YEAR(created_at)));
-- WHERE YEAR(created_at) = 2024 can use this index
```

### Unsichtbare Indizes (MySQL 8.0+) {#invisible-indexes-mysql-80}

Auswirkung des Entfernens eines Indexes testen, ohne ihn tatsächlich zu löschen:
```sql
ALTER TABLE orders ALTER INDEX idx_status INVISIBLE;
-- Index ignored by optimizer but still maintained
-- Run queries, check performance
ALTER TABLE orders ALTER INDEX idx_status VISIBLE;  -- restore if needed
```

### Spaltenreihenfolge in zusammengesetzten Indizes {#composite-index-column-ordering}

Regel Gleichheit - Bereich - Sortierung:
```sql
-- Query: WHERE status = 'active' AND created_at > '2024-01-01' ORDER BY amount
-- Best composite index:
CREATE INDEX idx_optimal ON orders (status, created_at, amount);
--  1. status    = equality (exact match, narrows quickly)
--  2. created_at = range (further narrows, but stops B-tree traversal)
--  3. amount    = sort (avoids filesort if after range column in same direction)
```

### Erkennung doppelter und redundanter Indizes {#duplicate-and-redundant-index-detection}

```sql
-- PostgreSQL: find unused indexes
SELECT schemaname, relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes WHERE idx_scan = 0 ORDER BY pg_relation_size(indexrelid) DESC;

-- MySQL: find redundant indexes (index on (a,b) makes index on (a) redundant)
SELECT * FROM sys.schema_redundant_indexes;
```

## Fallstricke {#gotchas}

- Ein normales `CREATE INDEX` erwirbt eine ShareLock (PostgreSQL) und blockiert INSERT/UPDATE/DELETE
- CONCURRENTLY kann fehlschlagen und einen ungültigen Index hinterlassen - dieser muss mit DROP entfernt und der Vorgang wiederholt werden
- Index-only Scans in PostgreSQL setzen eine aktuelle Visibility Map voraus - daher zuerst VACUUM ausführen
- Zu viele Indizes auf schreiblastigen Tabellen verlangsamen INSERT/UPDATE/DELETE erheblich
- Bitmap-Scans kombinieren mehrere Indizes (AND/OR) - manchmal schlagen zwei mittelmäßige Indizes einen perfekten
- MySQL-InnoDB-Sekundärindizes führen immer einen doppelten Zugriff über den gruppierten Index aus
- Präfix-Indizes in MySQL können nicht für ORDER BY oder GROUP BY genutzt werden - nur zum Filtern
- Funktionale Indizes müssen exakt dem Ausdruck in der Abfrage entsprechen - ein Index auf `LOWER(email)` hilft einer Abfrage mit `UPPER(email)` nicht
- Zusätzliche Spalten in einem Covering Index vergrößern den Index und verlangsamen Schreibzugriffe - den Kompromiss messen
- MySQL `FORCE INDEX` ist das letzte Mittel - liegt der Optimizer falsch, zuerst die Statistiken mit `ANALYZE TABLE` korrigieren

## Siehe auch {#see-also}

- [[btree-and-index-internals]] - B+Tree-Struktur und Seitenteilungen
- [[query-optimization-explain]] - Lesen der EXPLAIN-Ausgabe zur Überprüfung der Indexnutzung
- [[concurrency-and-locking]] - Sperrauswirkungen bei der Indexerstellung
- [[postgresql-configuration-tuning]] - Kostenparameter, die die Indexauswahl beeinflussen
