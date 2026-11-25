---
title: "PostgreSQL MVCC und VACUUM"
category: concepts
tags: [sql-databases, postgresql, mvcc, vacuum, autovacuum, dead-tuples, hot-update, write-amplification, bloat]
level: 3
source_sha256: e3602ba4c62dbd9f8b1826ca27e9cff1cad15d41a6a41b121f4aa1233ffc59b3
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL MVCC und VACUUM {#postgresql-mvcc-and-vacuum}

PostgreSQL verwendet Multi-Version Concurrency Control (MVCC), bei dem sich Leser und Schreiber nie gegenseitig blockieren. Der Preis dafür sind tote Tupel (Dead Tuples), die durch UPDATE- und DELETE-Operationen entstehen und von VACUUM bereinigt werden müssen.

## MVCC-Mechanik {#mvcc-mechanics}

Jedes UPDATE erzeugt eine neue Zeilenversion (Tupel) im Heap. Die alte Version wird als tot markiert, bleibt aber bestehen, bis VACUUM sie entfernt. DELETE markiert das Tupel als tot, gibt den Speicherplatz jedoch nicht frei. Jede Transaktion sieht einen konsistenten Snapshot, der sich nach ihrem Isolationslevel richtet.

## VACUUM {#vacuum}

VACUUM gibt Speicherplatz von toten Tupeln frei und aktualisiert die Statistiken für den Query-Planer.

**Reguläres VACUUM:** Markiert den Speicherplatz toter Tupel als innerhalb der Tabelle wiederverwendbar. Gibt den Speicher **nicht** an das Betriebssystem zurück. Erlaubt gleichzeitige Lese- und Schreibzugriffe (SHARE UPDATE EXCLUSIVE-Lock).

**VACUUM FULL:** Schreibt die gesamte Tabelle neu und gibt den Speicher an das Betriebssystem zurück. Blockiert **jeden** Zugriff (ACCESS EXCLUSIVE-Lock). Nur verwenden, wenn die Tabelle stark aufgebläht ist.

**Autovacuum:** Hintergrundprozess, der VACUUM automatisch anhand von Schwellenwerten für tote Tupel ausführt. Niemals deaktivieren: veraltete Statistiken führen zu schlechten Abfrageplänen sowie zu Bloat bei Tabellen und Indizes.

## Wichtige Fakten {#key-facts}

- Ein HOT-Update (Heap-Only Tuple) vermeidet Indexaktualisierungen, wenn (1) die geänderten Spalten nicht indiziert sind UND (2) das neue Tupel auf derselben Seite Platz findet
- Autovacuum-Konfiguration: `autovacuum_vacuum_threshold` + `autovacuum_vacuum_scale_factor * reltuples`
- `pg_stat_user_tables.n_dead_tup` zeigt die Anzahl toter Tupel pro Tabelle an
- VACUUM aktualisiert auch die Visibility Map (wird für Index-Only-Scans benötigt)
- PostgreSQL-Prozesse: postmaster, backend (pro Verbindung), background writer, WAL writer, checkpointer, autovacuum launcher, stats collector

## Muster {#patterns}

### Bloat und tote Tupel überwachen {#monitoring-bloat-and-dead-tuples}
```sql
-- Dead tuples per table
SELECT schemaname, relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::numeric / GREATEST(n_live_tup, 1) * 100, 2) AS dead_pct,
  last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Table bloat estimation
SELECT * FROM pgstattuple('my_table');

-- Check shared buffer contents
CREATE EXTENSION pg_buffercache;
```

### Autovacuum-Tuning {#autovacuum-tuning}
```sql
-- Per-table autovacuum settings for high-churn tables
ALTER TABLE hot_table SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- trigger at 1% dead tuples (default 20%)
  autovacuum_analyze_scale_factor = 0.01,
  autovacuum_vacuum_cost_delay = 0        -- no throttling for this table
);
```

### Spalte mit Default-Wert hinzufügen (vor PG11) {#adding-column-with-default-pre-pg11}
```sql
-- Pre-PG11: batch update to avoid full table rewrite
ALTER TABLE big_table ADD COLUMN new_col INTEGER;
-- Then batch-update in chunks of 10-100K rows:
UPDATE big_table SET new_col = 42 WHERE id BETWEEN 1 AND 100000;
VACUUM big_table;  -- between batches
-- Finally: ALTER TABLE big_table ALTER COLUMN new_col SET DEFAULT 42;
-- PG 11+: ADD COLUMN with DEFAULT is instant (no rewrite)
```

## PostgreSQL-Architektur (Prozesse) {#postgresql-architecture-processes}

| Prozess | Rolle |
|---------|------|
| Postmaster | Haupt-Daemon, startet Backends per fork |
| Backend | Ein Prozess pro Verbindung – Parsing, Planung, Ausführung |
| Background Writer | Schreibt geänderte Seiten periodisch auf die Festplatte |
| WAL Writer | Schreibt WAL-Puffer auf die Festplatte |
| Checkpointer | Sorgt für einen konsistenten Plattenzustand in den Checkpoint-Intervallen |
| Autovacuum Launcher | Startet Vacuum-Worker |
| Stats Collector | Sammelt Abfragestatistiken für den Optimizer |
| WAL Sender/Receiver | Streaming-Replikation |

Shared Memory: shared_buffers (Seiten-Cache), WAL-Puffer, Lock-Tabellen, Proc-Array.

## Stolperfallen {#gotchas}

- Autovacuum niemals deaktivieren – das führt zu veralteten Statistiken, Bloat und Leistungseinbußen
- VACUUM FULL benötigt einen exklusiven Lock und verdoppelt temporär den Plattenbedarf
- Lang laufende Transaktionen verhindern, dass VACUUM Tupel bereinigt, die sie möglicherweise noch sehen (Risiko eines Transaktions-ID-Wraparounds)
- `idle_in_transaction_session_timeout` verhindert, dass lange inaktive Transaktionen VACUUM blockieren
- Write Amplification: Das UPDATE einer beliebigen Spalte schreibt das gesamte Tupel neu und aktualisiert alle Indizes (sofern kein HOT-Update vorliegt)
- Ubers Migration von Postgres nach MySQL wurde durch Write Amplification bei vielen Sekundärindizes motiviert

## Siehe auch {#see-also}

- [[transactions-and-acid]] – MVCC und Isolationslevel
- [[database-storage-internals]] – Seiten, Heaps, Write Amplification
- [[concurrency-and-locking]] – Lock-Typen während VACUUM
- [[query-optimization-explain]] – veraltete Statistiken, die zu schlechten Plänen führen
