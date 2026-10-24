---
title: "Nebenläufigkeit und Sperren"
category: concepts
tags: [sql-databases, locks, deadlock, advisory-lock, pessimistic, optimistic, two-phase-locking, postgresql, mysql]
level: 3
source_sha256: c80e5fad992fb838bbe5eeb36cd88c7e0d8aee996ce4e8c863be0f6b502f3283
translation: machine
translated_at: '2026-10-24'
---
# Nebenläufigkeit und Sperren {#concurrency-and-locking}

Datenbanksperren steuern den nebenläufigen Zugriff auf gemeinsam genutzte Daten. Das Verständnis von Sperrtypen, Granularität und Deadlock-Mustern ist für den Bau zuverlässiger nebenläufiger Anwendungen unerlässlich.

## PostgreSQL-Tabellensperren (8 Stufen) {#postgresql-table-lock-types-8-levels}

Von der leichtesten zur schwersten:

| Sperre | Erworben durch | Blockiert |
|--------|----------------|-----------|
| ACCESS SHARE | SELECT | Nur ACCESS EXCLUSIVE |
| ROW SHARE | SELECT FOR UPDATE/SHARE | ACCESS EXCLUSIVE, EXCLUSIVE |
| ROW EXCLUSIVE | INSERT, UPDATE, DELETE | SHARE und stärker |
| SHARE UPDATE EXCLUSIVE | VACUUM, ANALYZE, CREATE INDEX CONCURRENTLY | Sich selbst und stärker |
| SHARE | CREATE INDEX (nicht nebenläufig) | ROW EXCLUSIVE und stärker (NICHT sich selbst) |
| SHARE ROW EXCLUSIVE | CREATE TRIGGER, ALTER TABLE ADD FK | Sich selbst und stärker |
| EXCLUSIVE | REFRESH MATERIALIZED VIEW CONCURRENTLY | Alles außer ACCESS SHARE |
| ACCESS EXCLUSIVE | DROP TABLE, TRUNCATE, VACUUM FULL, die meisten ALTER TABLE | Alles, einschließlich SELECT |

Wichtige Erkenntnis: Verschiedene ALTER TABLE-Operationen erwerben unterschiedliche Sperrstufen.

## PostgreSQL-Zeilensperren {#postgresql-row-lock-types}

| Sperre | Erworben durch | Blockiert |
|--------|----------------|-----------|
| FOR KEY SHARE | SELECT FOR KEY SHARE | Nur FOR UPDATE |
| FOR SHARE | SELECT FOR SHARE | UPDATE, DELETE, FOR UPDATE |
| FOR NO KEY UPDATE | UPDATE auf Nicht-Schlüsselspalten | FOR SHARE und stärker |
| FOR UPDATE | DELETE, UPDATE auf Schlüsselspalten | Alles |

Implementierung: PostgreSQL speichert Zeilensperren im Tupel-Header (Feld `xmax`), nicht im Speicher. Das spart Speicher, aber SELECT FOR UPDATE kann dazu führen, dass Seiten als modifiziert markiert werden.

## MySQL-InnoDB-Sperrtypen {#mysql-innodb-lock-types}

- **Shared (S):** `SELECT ... FOR SHARE`. Mehrere Halter erlaubt.
- **Exclusive (X):** `SELECT ... FOR UPDATE`, INSERT, UPDATE, DELETE. Nur ein Halter.
- **Intention-Sperren (IS/IX):** Sperren auf Tabellenebene, die signalisieren, dass eine Transaktion Zeilen sperren will.
- **Gap-Lock:** Sperrt die Lücke zwischen Indexeinträgen. Verhindert Phantom-Reads bei REPEATABLE READ.
- **Next-Key-Lock:** Gap-Lock plus Zeilensperre. Standard bei RR in InnoDB.
- **Insert-Intention-Lock:** Erlaubt gleichzeitiges Einfügen an unterschiedlichen Positionen innerhalb derselben Lücke.
- **MDL (Metadata Lock):** DDL erwirbt eine exklusive MDL, die blockiert, bis alle aktiven DML-Operationen beendet sind.

## Muster {#patterns}

### Vermeidung von Doppelbuchungen {#double-booking-prevention}
```sql
-- Pessimistic: SELECT FOR UPDATE
BEGIN;
SELECT * FROM seats WHERE seat_id = 42 AND status = 'available' FOR UPDATE;
UPDATE seats SET status = 'booked', user_id = 123 WHERE seat_id = 42;
COMMIT;

-- Optimistic: unique constraint
ALTER TABLE bookings ADD CONSTRAINT uq_seat_event UNIQUE (seat_id, event_id);
-- Second booking attempt fails with constraint violation
```

### Advisory Locks (PostgreSQL) {#advisory-locks-postgresql}
```sql
-- Session-level: held until explicit release or session end
SELECT pg_advisory_lock(42);      -- lock ID 42
-- Do work across multiple transactions...
SELECT pg_advisory_unlock(42);

-- Transaction-level: released on COMMIT/ROLLBACK
SELECT pg_advisory_xact_lock(42);
```

Advisory Locks blockieren keine Zeilenänderungen und können Transaktionen überspannen. Sie eignen sich für Sperren auf Anwendungsebene ohne tatsächliche Zeilen.

### Deadlock-Muster {#deadlock-pattern}
```sql
-- Session 1:                    -- Session 2:
BEGIN;                            BEGIN;
UPDATE t SET v=1 WHERE id=1;     UPDATE t SET v=2 WHERE id=2;
-- holds lock on id=1             -- holds lock on id=2
UPDATE t SET v=1 WHERE id=2;     UPDATE t SET v=2 WHERE id=1;
-- waits for id=2                 -- waits for id=1 -> DEADLOCK
```

### Two-Phase Locking (2PL) {#two-phase-locking-2pl}

Wachstumsphase (Sperren erwerben), dann Schrumpfungsphase (Sperren freigeben). Strict 2PL hält alle Sperren bis COMMIT/ROLLBACK. Garantiert Konfliktserialisierbarkeit.

## Wichtige Fakten {#key-facts}

- PostgreSQL: VACUUM erwirbt SHARE UPDATE EXCLUSIVE (erlaubt gleichzeitiges Lesen und Schreiben)
- VACUUM FULL erwirbt ACCESS EXCLUSIVE (blockiert alles, einschließlich SELECT)
- Schwache Sperren nutzen eine Fast-Path-Optimierung (16 Slots pro Backend); stark partitionierte Tabellen können diese Grenze überschreiten
- PostgreSQL erkennt Deadlocks automatisch und beendet eine Transaktion (Opfer)
- Auch DML ohne betroffene Zeilen erwirbt eine ROW EXCLUSIVE-Sperre auf der Tabelle
- MDL-Kaskade in MySQL: ALTER TABLE wartet auf ein langes SELECT, neue SELECTs reihen sich hinter dem ALTER ein

## Fallstricke {#gotchas}

- `SELECT FOR SHARE` durch zwei Transaktionen, danach versucht eine UPDATE = Deadlock
- Advisory Locks überspannen Transaktionen im Session-Modus; Lecks sind möglich, wenn sie nicht explizit freigegeben werden
- PgBouncer-Pooling im Transaction-Modus gibt Session-Advisory-Locks unerwartet frei
- Eingefügte Tupel benötigen in PostgreSQL keine Zeilensperren; sie sind für andere Transaktionen unsichtbar
- Deadlock-Erkennung verursacht Overhead; entwerfen Sie die Sperrreihenfolge so, dass Deadlocks verhindert werden

## Siehe auch {#see-also}

- [[transactions-and-acid]] - Isolationsstufen und Lesephänomene
- [[postgresql-mvcc-vacuum]] - MVCC als Alternative zu Sperren
- [[mysql-innodb-engine]] - InnoDB-Sperrinterna
- [[connection-pooling]] - Sperrverhalten bei Connection-Poolern
