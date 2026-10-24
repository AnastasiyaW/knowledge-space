---
title: "Transaktionen und ACID-Eigenschaften"
category: concepts
tags: [sql-databases, transaction, acid, isolation-level, read-committed, repeatable-read, serializable, snapshot-isolation]
level: 4
source_sha256: d2f8001ee8f2f502fd4f8c3c6b01d9953ef64241937ec843d2bcc4d37e73cc22
translation: machine
translated_at: '2026-10-24'
---
# Transaktionen und ACID-Eigenschaften {#transactions-and-acid-properties}

Transaktionen fassen mehrere Abfragen zu einer atomaren Arbeitseinheit zusammen. Die ACID-Eigenschaften (Atomicity, Consistency, Isolation, Durability) garantieren eine zuverlässige Datenverarbeitung, selbst bei gleichzeitigem Zugriff und Systemausfällen.

## Lebenszyklus einer Transaktion {#transaction-lifecycle}

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- verify >= 100
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Or ROLLBACK; to undo all changes
```

Reine Lesetransaktionen sind gültig und werden für konsistente Snapshots (Reports) verwendet.

## ACID-Eigenschaften {#acid-properties}

**Atomicity:** Entweder erfolgreich alle Abfragen oder alle werden zurückgerollt. Ein Absturz zwischen den beiden UPDATEs oben löst beim Recovery automatisch ein Rollback aus, sodass kein partieller Zustand entsteht.

**Consistency:** Zwei Dimensionen: (1) Datenkonsistenz – referenzielle Integrität, CHECK-Constraints, UNIQUE-Constraints; (2) Lesekonsistenz – ob der nächste Lesevorgang gerade committete Daten sieht (das C aus dem CAP-Theorem).

**Isolation:** Steuert die Sichtbarkeit von Änderungen gleichzeitiger Transaktionen. Siehe Isolationsstufen weiter unten.

**Durability:** Committete Änderungen überleben Abstürze. Umgesetzt wird dies über WAL (Write-Ahead Log). `fsync()` erzwingt den physischen Schreibvorgang auf die Festplatte, ist aber teuer. `synchronous_commit = off` in PostgreSQL tauscht das Risiko für die Dauerhaftigkeit (ein Fenster von ca. 600 ms) gegen 3x schnellere Commits.

## Lesephänomene {#read-phenomena}

| Phänomen | Beschreibung |
|-----------|-------------|
| Dirty Read | Lesen nicht committeter Daten einer anderen Transaktion |
| Non-Repeatable Read | Dieselbe Zeile liefert innerhalb einer Transaktion zwischen zwei Lesevorgängen unterschiedliche Werte |
| Phantom Read | Erneutes Ausführen einer Bereichsabfrage liefert neue Zeilen, die von einer anderen Transaktion eingefügt wurden |
| Lost Update | Zwei Transaktionen lesen dieselbe Zeile und aktualisieren sie beide, die zweite überschreibt die Änderung der ersten |

## Isolationsstufen {#isolation-levels}

| Stufe | Dirty Read | Non-Repeatable | Phantom | Lost Update |
|-------|-----------|----------------|---------|-------------|
| Read Uncommitted | Ja | Ja | Ja | Ja |
| Read Committed | Nein | Ja | Ja | Ja |
| Repeatable Read | Nein | Nein | Ja* | Nein |
| Serializable | Nein | Nein | Nein | Nein |

*PostgreSQL implementiert Repeatable Read als Snapshot Isolation – damit werden auch Phantome verhindert. MySQL InnoDB verwendet bei RR Next-Key-Locking.

**Read Committed** (Standard in PostgreSQL, Oracle): Jede Anweisung sieht nur Daten, die vor ihrem Beginn committet wurden. Standard für die meisten Produktivanwendungen.

**Repeatable Read:** Die Transaktion sieht einen Snapshot vom Transaktionsbeginn. PostgreSQL = Snapshot Isolation (optimistisch, Konflikte werden beim Commit erkannt). MySQL = Next-Key-Locking (pessimistisch, Konflikte werden durch Sperren verhindert).

**Serializable:** Transaktionen werden so ausgeführt, als wären sie seriell abgearbeitet worden. PostgreSQL verwendet SSI (Serializable Snapshot Isolation) – nebenläufige Ausführung mit Abhängigkeitsverfolgung, bricht bei einer Anomalie ab.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Or globally:
ALTER DATABASE mydb SET DEFAULT_TRANSACTION_ISOLATION TO 'read committed';
```

## Implementierungsansätze {#implementation-approaches}

**Pessimistisch (Locking):** Zeilen bzw. Seiten werden vor der Änderung gesperrt. Bei Konflikten wird gewartet. `SELECT FOR UPDATE` ist pessimistisches Serializable. Am besten geeignet für Workloads mit hoher Konkurrenz.

**Optimistisch (MVCC):** Während der Ausführung werden keine Sperren gesetzt. Änderungen werden verfolgt, bei einem Konflikt schlägt das Commit fehl. Besser geeignet für Workloads mit geringer Konkurrenz und leselastige Workloads.

## Wichtige Fakten {#key-facts}

- PostgreSQL: RR = Snapshot Isolation (keine Phantom Reads, anders als bei MySQL)
- PostgreSQL unterstützt READ UNCOMMITTED nicht (wird wie Read Committed behandelt)
- Der MySQL-InnoDB-Standard ist REPEATABLE READ mit Gap-Locks
- `SELECT FOR UPDATE` erwirbt eine exklusive Zeilensperre bis zum Ende der Transaktion
- Lange Transaktionen halten Verbindungen und Sperren – `idle_in_transaction_session_timeout` setzen

### Muster zum Beanspruchen von Zeilen (nebenläufige Worker) {#claiming-rows-pattern-concurrent-workers}

Mehrere Worker beanspruchen Aufgaben, ohne sich gegenseitig zu blockieren:
```sql
-- Atomically claim next unclaimed row
UPDATE tasks
SET status = 'processing', worker_id = :my_id, claimed_at = NOW()
WHERE id = (
    SELECT id FROM tasks
    WHERE status = 'pending'
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED  -- skip rows locked by other workers
)
RETURNING *;
```
`SKIP LOCKED` (PostgreSQL 9.5+, MySQL 8.0+) – der Worker überspringt gesperrte Zeilen, statt zu warten. Dadurch wird eine echte parallele Work-Queue möglich.

### Advisory Locks (anwendungsseitiges Locking) {#advisory-locks-application-level-locking}

```sql
-- PostgreSQL: application-level named locks (not tied to rows)
SELECT pg_advisory_lock(12345);     -- blocks until acquired
-- ... critical section ...
SELECT pg_advisory_unlock(12345);

-- Try without blocking:
SELECT pg_try_advisory_lock(12345); -- returns true/false immediately

-- Session-level: released on disconnect
-- Transaction-level: released on COMMIT/ROLLBACK
SELECT pg_advisory_xact_lock(12345);
```
Anwendungsfall: Verhindern, dass ein Cron-Job mehrfach ausgeführt wird, oder Koordination des Zugriffs auf externe Ressourcen.

### Savepoints (teilweises Rollback) {#savepoints-partial-rollback}

```sql
BEGIN;
INSERT INTO orders (user_id, amount) VALUES (1, 100);

SAVEPOINT sp1;
INSERT INTO order_items (order_id, product_id) VALUES (1, 999);  -- might fail
-- If this fails:
ROLLBACK TO SAVEPOINT sp1;
-- order INSERT is preserved, only order_items rolled back

INSERT INTO order_items (order_id, product_id) VALUES (1, 42);  -- retry
COMMIT;  -- commits order + corrected order_items
```

## Stolperfallen {#gotchas}

- Serializable serialisiert Transaktionen nicht wörtlich – es wird mit Abhängigkeitsverfolgung gearbeitet (SSI in PG)
- `SELECT FOR UPDATE` im Transaction-Level-Pooling (PgBouncer) kann zu unerwarteter Freigabe von Sperren führen
- Zwei Transaktionen, die beide zuerst `SELECT FOR SHARE` und danach ein UPDATE auf dieselbe Zeile ausführen, ergeben einen Deadlock
- Lost Updates sind auch bei Read Committed möglich – `SELECT FOR UPDATE` oder eine höhere Isolationsstufe verwenden
- `SKIP LOCKED` überspringt Zeilen stillschweigend – sind alle Zeilen gesperrt, wird ein leeres Ergebnis zurückgegeben (kein Fehler)
- Advisory Locks werden am Transaktionsende nicht automatisch freigegeben (Session-Level-Variante) – immer explizit entsperren oder `pg_advisory_xact_lock` verwenden
- Savepoints im `autocommit`-Modus haben keine Wirkung – immer innerhalb eines expliziten `BEGIN` verwenden
- Lang laufende Transaktionen in MVCC halten alte Zeilenversionen am Leben und verhindern VACUUM – `idle_in_transaction_session_timeout` setzen

## Siehe auch {#see-also}

- [[concurrency-and-locking]] – Sperrtypen, Deadlocks, Advisory Locks
- [[postgresql-wal-durability]] – WAL und Kompromisse bei der Dauerhaftigkeit
- [[postgresql-mvcc-vacuum]] – Details zur MVCC-Implementierung
- [[connection-pooling]] – Pooling-Modi und Transaktionsverhalten
