---
title: "PostgreSQL für Data Engineering"
category: tools
tags: [data-engineering, postgresql, rdbms, transactions, plpgsql, optimization]
level: 3
source_sha256: 8a207e8d3c96b520062a6717dbad9b206c344f0cc9aa64445a9003df0ac21e70
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL für Data Engineering {#postgresql-for-data-engineering}

PostgreSQL ist das gebräuchlichste RDBMS im Data Engineering. Es wird als Metastore für Airflow, als Quellsystem und manchmal auch als analytische Datenbank eingesetzt. Das Verständnis seiner Architektur, seiner Transaktionen und seiner prozeduralen Erweiterungen ist essenziell.

## Architektur {#architecture}

- **Client-Server-Modell:** Der Postmaster verwaltet Backend-Prozesse, einen pro Client-Verbindung
- **Connection Pooling:** pgBouncer oder Odyssey bei hoher Anzahl an Verbindungen
- **Physische Speicherung:** Daten in 8-KB-Seiten, gecacht in shared_buffers
- **Logisch:** Server -> Datenbank -> Schema -> Objekte (Tabellen, Indizes, Views, Funktionen)

## Transaktionen (ACID) {#transactions-acid}

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob';
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100 WHERE name = 'Wally';
COMMIT;
```

### Isolationsstufen {#isolation-levels}

| Stufe | Dirty Read | Non-Repeatable | Phantom |
|-------|-----------|---------------|---------|
| Read Committed (Standard) | Nein | Möglich | Möglich |
| Repeatable Read | Nein | Nein | Nein* |
| Serializable | Nein | Nein | Nein |

*Das Repeatable Read von PostgreSQL verhindert auch Phantome (strenger als der Standard).

### MVCC {#mvcc}
Jede Transaktion arbeitet mit einem Snapshot der Daten (Transaktions-IDs definieren die Sichtbarkeit).
- **Read Committed:** Snapshot pro Statement
- **Repeatable Read:** Snapshot pro Transaktion

## PL/pgSQL {#plpgsql}

### Funktionen vs. Prozeduren {#functions-vs-procedures}

| Merkmal | Funktion | Prozedur |
|---------|----------|-----------|
| Transaktionssteuerung | Nein | Ja |
| Verwendung in SELECT | Ja | Nein |
| Aufrufsyntax | `SELECT func()` | `CALL proc()` |

### Trigger {#triggers}

```sql
CREATE OR REPLACE FUNCTION log_changes() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit (id, op) VALUES (NEW.id, 'INSERT');
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit (id, op) VALUES (NEW.id, 'UPDATE');
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit (id, op) VALUES (OLD.id, 'DELETE');
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_changes
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION log_changes();
```

## MERGE (PostgreSQL 15+) {#merge-postgresql-15}

```sql
MERGE INTO products AS p
USING product_updates AS u ON p.id = u.id
WHEN MATCHED THEN UPDATE SET name = u.name, price = u.price
WHEN NOT MATCHED THEN INSERT (id, name, price) VALUES (u.id, u.name, u.price)
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

Für PostgreSQL < 15: `INSERT ... ON CONFLICT DO UPDATE`.

## Bulk-Operationen {#bulk-operations}

```sql
COPY table_name FROM '/path/to/file.csv';
COPY (SELECT * FROM t) TO '/path/to/output.csv';
TRUNCATE TABLE employees;  -- fast clear (vs row-by-row DELETE)
```

## Physische JOIN-Methoden {#physical-join-methods}

| Methode | Komplexität | Voraussetzung |
|--------|-----------|-------------|
| **Nested Loops** | O(M * N) | Universell |
| **Merge Join** | O(M + N) sortiert | Gleichheitsbedingung, sortierte Daten |
| **Hash Join** | O(N) | Gleichheitsbedingung, Speicher für Hash-Tabelle |

## Query-Optimierung {#query-optimization}

```sql
EXPLAIN ANALYZE SELECT * FROM bookings;
-- Shows: plan type, cost, actual time, rows, loops
```

### Plan-Knotentypen {#plan-node-types}
- Seq Scan, Index Scan, Index Only Scan
- Nested Loop / Merge Join / Hash Join
- HashAggregate, Sort, Gather (parallel)

### Statistiken {#statistics}
```sql
SELECT reltuples, relpages FROM pg_class WHERE relname = 'bookings';
ANALYZE table_name;  -- update statistics
```

## Fallstricke {#gotchas}
- Der Leerstring `''` ist in PostgreSQL NICHT NULL (anders als bei Oracle)
- DateStyle beeinflusst das Parsen von Datumswerten: immer ISO 8601 verwenden (`YYYY-MM-DD`)
- Arrays sind in PostgreSQL 1-indiziert
- `float`-Typen niemals für Geldbeträge verwenden (Rundungsfehler)
- UPDATE mit FROM: Gibt es mehrere Treffer, ist nicht vorhersagbar, welche Zeile verwendet wird
- Kaskadierendes Löschen erfolgt implizit - explizite Löschvorgänge bevorzugen
- Im DWH werden Constraints oft deaktiviert, um Bulk-Loads zu beschleunigen

## Siehe auch {#see-also}
- [[sql-for-de]] - SQL-Muster und Window Functions
- [[data-modeling]] - Normalisierung und Schema-Design
- [[greenplum-mpp]] - PostgreSQL-basiertes MPP
- [[docker-for-de]] - PostgreSQL in Docker betreiben
