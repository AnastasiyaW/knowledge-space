---
title: "Verteilte Transaktionen und Muster"
category: concepts
tags: [sql-databases, distributed-transactions, two-phase-commit, saga, eventual-consistency, double-booking]
level: 4
source_sha256: 75178f1623ae7c5692f1feff79fb88a07a60ce833a78c9264fe51f976f4f81da
translation: machine
translated_at: '2026-10-24'
---
# Verteilte Transaktionen und Muster {#distributed-transactions-and-patterns}

Wenn Daten über mehrere Datenbanken oder Services verteilt sind, erfordert die Konsistenz Muster, die über ACID in einer einzelnen Datenbank hinausgehen. Die beiden Hauptansätze, 2PC und Saga, stellen einen Kompromiss zwischen Konsistenzgarantien und Verfügbarkeit dar.

## Two-Phase Commit (2PC) {#two-phase-commit-2pc}

Der Koordinator fordert alle Teilnehmer auf, sich vorzubereiten (Phase 1), und anschließend zu committen (Phase 2). Stimmt ein Teilnehmer mit Nein, werden alle abgebrochen.

**Problem:** Fällt der Koordinator während der Commit-Phase aus, bleiben die Teilnehmer in einem unsicheren Zustand hängen (blockierendes Protokoll). Synchron, hohe Latenz.

**Anwendungsfall:** Wenn über mehrere Datenbanken hinweg starke Konsistenz erforderlich ist und Latenz akzeptabel ist.

## Saga-Muster {#saga-pattern}

Eine Folge lokaler Transaktionen mit kompensierenden Transaktionen für das Zurückrollen. Jeder Schritt wird unabhängig committet.

```php
Step 1: Reserve inventory  -> Compensate: Release inventory
Step 2: Charge payment     -> Compensate: Refund payment
Step 3: Ship order         -> Compensate: Cancel shipment
```

Schlägt Schritt N fehl, werden die kompensierenden Transaktionen für die Schritte N-1 bis 1 ausgeführt.

**Arten:** Choreographie (Events zwischen Services) vs. Orchestrierung (zentraler Koordinator).

**Vorteile:** Bessere Verfügbarkeit als 2PC, kein Blockieren. **Nachteile:** Komplexe Kompensationslogik, eventuelle Konsistenz.

## Double-Booking-Prävention {#double-booking-prevention}

### Pessimistisch (SELECT FOR UPDATE) {#pessimistic-select-for-update}
```sql
BEGIN;
SELECT * FROM seats WHERE id = 42 AND status = 'available' FOR UPDATE;
-- Row locked. If available:
UPDATE seats SET status = 'booked', user_id = 123 WHERE id = 42;
COMMIT;
```

### Optimistisch (Unique Constraint) {#optimistic-unique-constraint}
```sql
ALTER TABLE bookings ADD CONSTRAINT uq_seat_event UNIQUE (seat_id, event_id);
-- Second booking fails with constraint violation - app catches and retries
```

### Advisory Locks {#advisory-locks}
```sql
SELECT pg_advisory_lock(42);  -- lock seat 42
-- Check and book...
SELECT pg_advisory_unlock(42);
```

### Serializable-Isolation {#serializable-isolation}
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Database detects conflicts automatically - simplest code, higher abort rate
```

## Hash-Tabellen in Datenbanken {#hash-tables-in-databases}

Intern verwendet für: Hash-Joins (Aufbau über die kleinere Tabelle, Abfrage mit der größeren), Hash-Aggregation (GROUP BY), Hash-Partitionierung, Hash-Indizes.

Kollisionsstrategien: Verkettung (verkettete Listen), offene Adressierung (lineares/quadratisches Sondieren), Cuckoo-Hashing (zwei Hash-Funktionen, O(1) garantiert).

## Wichtige Fakten {#key-facts}

- 2PC ist ein blockierendes Protokoll – der Ausfall eines Teilnehmers während des Commits blockiert alle anderen
- Saga bietet eventuelle Konsistenz, keine starke Konsistenz
- Kompensierende Transaktionen müssen idempotent sein (sicher wiederholbar)
- `SELECT FOR UPDATE` ist die einfachste Double-Booking-Prävention in Szenarien mit einer einzelnen Datenbank
- Serializable-Isolation in PostgreSQL verwendet SSI (Serializable Snapshot Isolation) – nicht die tatsächliche serielle Ausführung

## Fallstricke {#gotchas}

- Der 2PC-Koordinator ist ein Single Point of Failure – er benötigt eine eigene Hochverfügbarkeit
- Die Kompensationslogik einer Saga kann so komplex sein wie die ursprüngliche Geschäftslogik
- Eventuelle Konsistenz bedeutet, dass Benutzer vorübergehend veraltete Daten sehen können
- `SELECT FOR UPDATE` blockiert konkurrierende Zugriffe – hohe Konkurrenz wird zum Engpass
- Advisory Locks im Transaktionsmodus von PgBouncer werden freigegeben, sobald die Verbindung in den Pool zurückkehrt

## Siehe auch {#see-also}

- [[transactions-and-acid]] - ACID-Garantien einer einzelnen Datenbank
- [[concurrency-and-locking]] - Sperrtypen zur Vermeidung von Konflikten
- [[distributed-databases]] - Datenbanken mit integrierten verteilten Transaktionen
- [[partitioning-and-sharding]] - Herausforderungen bei shardübergreifenden Transaktionen
