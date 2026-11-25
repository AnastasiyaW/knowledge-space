---
title: "Query-Optimierung und EXPLAIN"
category: concepts
tags: [sql-databases, explain, explain-analyze, query-plan, optimizer, sequential-scan, index-scan, postgresql, mysql, performance]
level: 4
source_sha256: 978fe76033d74e9fdbfa49a64f5d25a0ce4385033f34be0064a6e4d23dc9adf9
translation: machine
translated_at: '2026-10-24'
---
# Query-Optimierung und EXPLAIN {#query-optimization-and-explain}

EXPLAIN zeigt, wie die Datenbank die Ausführung einer Abfrage plant. EXPLAIN ANALYZE führt die Abfrage tatsächlich aus und liefert die gemessenen Werte. Das Verständnis der Plan-Operatoren und des Kostenmodells ist für die Diagnose langsamer Abfragen unerlässlich.

## EXPLAIN-Ausgabe {#explain-output}

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM orders WHERE user_id = 42;
```

Wichtige Felder der Ausgabe:
- **cost:** startup_cost..total_cost in willkürlichen Einheiten (NICHT Millisekunden)
- **rows:** geschätzte Anzahl zurückgegebener Zeilen (basierend auf Tabellenstatistiken)
- **width:** durchschnittliche Zeilengröße in Bytes
- **actual time:** Millisekunden (nur bei ANALYZE), first_row..total
- **loops:** Anzahl der Ausführungen dieses Knotens
- **Buffers:** shared hit (Cache) im Vergleich zu read (Festplatte)

### Kosteneinheiten (PostgreSQL) {#cost-units-postgresql}
```toml
seq_page_cost = 1.0       -- baseline: sequential page read
random_page_cost = 4.0    -- random page read (lower to 1.1-2.0 for SSD)
cpu_tuple_cost = 0.01     -- processing one row
cpu_index_tuple_cost = 0.005
cpu_operator_cost = 0.0025
```

## Plan-Knotentypen {#plan-node-types}

| Operator | Beschreibung | Hinweise zur Performance |
|----------|--------------|--------------------------|
| Seq Scan | Vollständiger Tabellenscan | Kosten proportional zur Tabellengröße |
| Index Scan | B+Tree-Lookup + Heap-Zugriff | 2+ I/Os pro Zeile (Index + Heap) |
| Index Only Scan | Alle Daten aus dem Index, kein Heap-Zugriff | Am schnellsten – erfordert Covering Index und aktuelle Visibility Map |
| Bitmap Index Scan | Bitmap aufbauen, Seiten sequenziell lesen | Gut bei mittlerer Selektivität |
| Nested Loop Join | Für jede äußere Zeile die innere Tabelle scannen | Gut, wenn die innere Tabelle einen Index hat oder klein ist |
| Hash Join | Hash aus der kleineren Tabelle aufbauen, dann prüfen | Gut für große Gleichheitsjoins |
| Merge Join | Beide Eingaben sortiert, Merge-Sort-Durchlauf | Gut, wenn die Eingaben bereits sortiert sind |
| Sort | Externe Sortierung bei mehr als work_mem | Erzeugt temporäre Dateien, wenn der Speicher nicht ausreicht |
| Aggregate | GROUP-BY-Verarbeitung | Hash- oder sortbasiert |
| Gather | Koordination paralleler Abfragen | |

## Visualisierungswerkzeuge {#visualization-tools}

- https://explain.tensor.ru - interaktive Visualisierung von Plänen
- https://tatiyants.com/pev - Plan-Visualisierer
- https://explain.depesz.com - detaillierte Analyse

## Checkliste zur Abfrage-Optimierung {#query-optimization-checklist}

### SQL-Ebene {#sql-level}
- UNION ALL statt UNION verwenden, wenn Duplikate akzeptabel sind
- Nur benötigte Spalten auswählen (`SELECT *` vermeiden)
- DISTINCT möglichst vermeiden (weist oft auf einen fehlerhaften JOIN hin)
- Bei zusammengesetzten Indizes die erste Spalte in den Abfragen verwenden
- EXISTS/IN dort verwenden, wo es passt
- Kleine Tabellen: Vollscan ist schneller als Index-Scan (passt in eine Seite)
- Funktionen auf indizierten Spalten deaktivieren die Indexnutzung

### Datenbankebene {#database-level}
- `ANALYZE` regelmäßig ausführen, um aktuelle Statistiken zu erhalten
- `work_mem` für komplexe Abfragen mit Sortierungen/Hashes anpassen
- `random_page_cost = 1.1-2.0` für SSD-Speicher setzen
- `default_statistics_target` erhöhen, um bessere Kardinalitätsschätzungen zu erhalten
- `pg_stat_statements` aktivieren, um langsame und häufige Abfragen zu finden

### Architekturebene {#architecture-level}
- Connection Pooler einsetzen, wenn max_connections > 100–200
- Read-Replicas für lesintensive Workloads in Betracht ziehen
- Materialisierte Sichten für wiederholte, aufwendige Aggregationen
- Große Tabellen nach Datum/Bereich partitionieren
- Große DML-Operationen in Batches aufteilen

## Muster {#patterns}

### Veraltete Statistiken diagnostizieren {#diagnosing-stale-statistics}
```sql
-- Compare estimated vs actual rows - large discrepancy = stale stats
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'active';
-- If estimated: 100, actual: 50000 -> run ANALYZE
ANALYZE orders;
```

### Index-Nutzung erzwingen (nur zum Testen) {#forcing-index-use-testing-only}
```sql
-- PostgreSQL: disable seq scan to test if index would help
SET enable_seqscan = off;
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;
RESET enable_seqscan;

-- MySQL: force specific index
SELECT * FROM orders FORCE INDEX (idx_user_id) WHERE user_id = 42;
```

### Monitoring-Erweiterungen {#monitoring-extensions}
```sql
-- pg_stat_statements: find slowest/most frequent queries
CREATE EXTENSION pg_stat_statements;
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;

-- auto_explain: automatically log slow query plans
ALTER SYSTEM SET auto_explain.log_min_duration = '1s';
```

### Deferred Joins (MySQL-Optimierung) {#deferred-joins-mysql-optimization}

Bei Paginierung mit OFFSET auf großen Tabellen liest die Datenbank die Zeilen trotzdem und verwirft sie:
```sql
-- SLOW: reads and discards 100000 rows
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000;

-- FAST: deferred join - only fetch IDs first, then join for data
SELECT p.* FROM posts p
INNER JOIN (
    SELECT id FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000
) AS sub ON p.id = sub.id;
-- Inner query uses covering index (id, created_at), outer fetches full rows only for 20 results
```

### Cursor-basierte Paginierung (Alternative zu OFFSET) {#cursor-based-pagination-alternative-to-offset}

```sql
-- Instead of OFFSET (scans discarded rows):
SELECT * FROM posts ORDER BY id DESC LIMIT 20 OFFSET 100000;

-- Use cursor (seeks directly via index):
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 20;
-- O(1) seek vs O(N) scan - cursor pagination is constant time regardless of page depth
```

### Muster Zeitstempel statt Booleans {#timestamps-vs-booleans-pattern}

```sql
-- Instead of boolean columns with unclear semantics:
ALTER TABLE orders ADD COLUMN is_shipped BOOLEAN DEFAULT FALSE;

-- Use timestamp - carries both state AND timing:
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMP NULL;
-- NULL = not shipped, non-NULL = shipped (and you know when)
-- WHERE shipped_at IS NOT NULL = WHERE is_shipped = TRUE
-- Bonus: indexable, sortable, auditable
```

### Summentabellen für aufwendige Aggregationen {#summary-tables-for-expensive-aggregations}

```sql
-- Instead of running COUNT(*) GROUP BY on millions of rows:
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY,
    order_count INT,
    total_revenue DECIMAL(12,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate periodically or via trigger
INSERT INTO daily_stats (date, order_count, total_revenue)
SELECT DATE(created_at), COUNT(*), SUM(amount)
FROM orders
WHERE DATE(created_at) = CURRENT_DATE
ON CONFLICT (date) DO UPDATE SET
    order_count = EXCLUDED.order_count,
    total_revenue = EXCLUDED.total_revenue,
    updated_at = CURRENT_TIMESTAMP;
```

### EXPLAIN-Warnsignale {#explain-red-flags-to-watch-for}

| Warnsignal | Bedeutung | Maßnahme |
|------------|-----------|----------|
| Seq Scan auf großer Tabelle | Fehlender oder ungenutzter Index | Index hinzufügen, SARGability prüfen |
| Zeilenschätzung stark abweichend | Veraltete Statistiken | `ANALYZE table` |
| Sort mit Festplattenzugriff | `work_mem` zu klein | `work_mem` erhöhen oder sortierten Index hinzufügen |
| Nested Loop mit Seq Scan auf innerer Tabelle | Fehlender Index auf der Join-Spalte | Index auf dem Join-Schlüssel der inneren Tabelle hinzufügen |
| Hash Join lagert auf Festplatte aus | `work_mem` zu klein für die Hash-Tabelle | `work_mem` erhöhen |

## Fallstricke {#gotchas}

- EXPLAIN ANALYZE führt die Abfrage tatsächlich aus (auch DML!) – in eine Transaktion einschließen und mit ROLLBACK beenden
- Pläne für Tabellen mit 1000 Zeilen lassen sich nicht auf Millionen hochrechnen – die Kosten des Planers sind nicht linear
- Tabellen mit nur einer Seite erhalten immer einen Sequential Scan, unabhängig von vorhandenen Indizes
- Die Zeitmessung von EXPLAIN ANALYZE schließt Netzwerkübertragung und Formatkonvertierung aus
- Ein hoher Wert für `join_collapse_limit` verbessert den Plan, verlangsamt aber die Planung bei Joins über viele Tabellen
- Nach VACUUM wird die Visibility Map aktualisiert – Index Only Scan kann dann Seq Scan ersetzen
- MySQL `EXPLAIN` zeigt den geschätzten Plan; `EXPLAIN ANALYZE` (ab 8.0.18) zeigt die tatsächliche Ausführung – für eine echte Diagnose immer ANALYZE verwenden
- `SELECT *` verhindert Index-Only-Scans – nur benötigte Spalten angeben, damit ein Covering Index genutzt werden kann
- Korrelierte Unterabfragen werden einmal pro äußerer Zeile ausgeführt – wenn möglich als JOIN oder Lateral Join umschreiben

## Siehe auch {#see-also}

- [[index-strategies]] – Erstellen und Auswählen von Indizes
- [[btree-and-index-internals]] – Verständnis der Scan-Typen
- [[postgresql-configuration-tuning]] – Planer-Parameter
- [[postgresql-mvcc-vacuum]] – VACUUM und Aktualität der Statistiken
