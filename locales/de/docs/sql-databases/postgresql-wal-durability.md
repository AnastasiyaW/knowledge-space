---
title: "PostgreSQL WAL und Dauerhaftigkeit"
category: concepts
tags: [sql-databases, postgresql, wal, write-ahead-log, durability, checkpoint, fsync, crash-recovery]
level: 3
source_sha256: 3f36bded270f4892db07d3b6d615ad6bcbe2aa477a11cf8685d89984720c9110
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL WAL und Dauerhaftigkeit {#postgresql-wal-and-durability}

Das Write-Ahead Log (WAL) ist die Grundlage für Crash-Recovery und Replikation in PostgreSQL. Es stellt sicher, dass committete Transaktionen jeden Ausfall überstehen, indem Änderungen in ein sequenzielles Log geschrieben werden, bevor die Datenseiten verändert werden.

## So funktioniert WAL {#how-wal-works}

1. Transaktion ändert Daten in shared_buffers (Speicher)
2. WAL-Eintrag wird in die WAL-Puffer geschrieben
3. Bei COMMIT wird das WAL auf die Festplatte geschrieben (sequenzieller Schreibvorgang - schnell)
4. Die eigentlichen Datenseiten werden verzögert durch den Background Writer bzw. Checkpointer geschrieben
5. Bei einem Absturz: WAL ab dem letzten Checkpoint wiedergeben, um den committeten Zustand zu rekonstruieren

WAL-Segmente sind standardmäßig 16-MB-Dateien. Das Pendant in MySQL InnoDB ist der „redo log“.

## Wichtige Parameter {#key-parameters}

```sql
-- WAL detail level
wal_level = replica    -- minimal | replica | logical
-- 'minimal' = crash recovery only
-- 'replica' = streaming replication support
-- 'logical' = logical replication/decoding

-- Durability vs performance
synchronous_commit = on
-- 'on' (default): WAL flushed to disk on each commit (safest)
-- 'off': buffered, async flush. 3x faster, risk ~600ms of lost commits on crash
-- 'remote_apply': WAL applied on replica before confirming

-- Full page writes (torn page protection)
full_page_writes = on  -- write full page to WAL on first modification after checkpoint

-- WAL compression
wal_compression = on   -- reduces WAL size, slight CPU overhead
```

## Checkpoints {#checkpoints}

Checkpoint: Ein Hintergrundprozess schreibt alle Dirty Pages auf die Festplatte und schreibt einen Checkpoint-Eintrag in das WAL. Nach dem Checkpoint können ältere WAL-Dateien wiederverwendet werden.

```sql
-- Checkpoint frequency controls
max_wal_size = '4GB'          -- trigger checkpoint when WAL reaches this size
checkpoint_timeout = '5min'    -- max time between checkpoints
checkpoint_completion_target = 0.9  -- spread I/O over 90% of interval
```

## OS-Cache und fsync {#os-cache-and-fsync}

Das Betriebssystem puffert Schreiboperationen im Speicher (Page Cache). Ein Stromausfall vor dem Leeren des Caches bedeutet Datenverlust, selbst wenn die Datenbank die Daten „geschrieben“ hat.

- `fsync()` erzwingt einen physischen Schreibvorgang auf die Festplatte - teuer
- Batteriegepufferter Schreibcache (BBWC) auf RAID-Controllern macht fsync schnell
- `wal_sync_method = fdatasync` (Linux-Standard) oder `open_datasync`

## Trade-offs zwischen Dauerhaftigkeit und Performance {#durability-vs-performance-trade-offs}

| Einstellung | Verhalten | Risiko |
|-------------|-----------|--------|
| `synchronous_commit = on` | WAL wird pro Commit geschrieben | Keines - volle Dauerhaftigkeit |
| `synchronous_commit = off` | WAL wird gepuffert, asynchrones Schreiben | Verlust der letzten ~600 ms an Commits |
| Gebündelte Commits | Mehrere Commits werden in einem fsync zusammengefasst | Höherer Durchsatz, geringfügig erhöhtes Risiko pro Transaktion |
| Dedizierte WAL-Festplatte | Separate Festplatte für WAL-Dateien | 2- bis 30-fache Verbesserung bei Schreibvorgängen |

## WAL für Replikation {#wal-for-replication}

```sql
-- Required for streaming replication
wal_level = replica
max_wal_senders = 10
```

WAL-Segmente werden zu Replicas gestreamt, um eine kontinuierliche Replikation zu ermöglichen. WAL-Archivierung ermöglicht PITR (Point-in-Time Recovery).

## Vergleich mit anderen Datenbanken {#comparison-with-other-databases}

| Datenbank | Mechanismus | Anmerkungen |
|-----------|-------------|-------------|
| PostgreSQL | WAL (16-MB-Segmente) | Sequenzielles Log + verzögerte Datenschreibvorgänge |
| MySQL InnoDB | Redo Log | Ähnlich wie WAL, fester zirkulärer Log |
| Redis | RDB + AOF (optional) | Speicherbasiert by design, Dauerhaftigkeit optional |
| MongoDB | Journal (WiredTiger) | Checkpoint alle 60 s oder bei 2 GB |
| Cassandra | Commit Log + Memtable | WAL-Äquivalent + SSTable-Flush |

## Fallstricke {#gotchas}

- `synchronous_commit = off` riskiert den Verlust nur der letzten ~600 ms committeter Transaktionen, NICHT eine Datenkorruption
- `full_page_writes = on` verdoppelt etwa die WAL-Größe, verhindert aber Korruption durch unvollständig geschriebene Seiten (Torn Pages)
- Fehlschlagende WAL-Archivierung unterbricht die Backup-Kette - die Erfolgsrate von `archive_command` überwachen
- Ein großes `max_wal_size` reduziert die Checkpoint-Häufigkeit, erhöht aber die Wiederherstellungszeit nach einem Absturz
- Datenprüfsummen (`initdb -k` oder `pg_checksums`) erkennen stille Korruption, verursachen aber etwa 1-2 % Mehraufwand beim Lesen

## Siehe auch {#see-also}

- [[transactions-and-acid]] - ACID-Eigenschaft der Dauerhaftigkeit
- [[backup-and-recovery]] - WAL-Archivierung für PITR
- [[replication-fundamentals]] - WAL-basierte Streaming-Replikation
- [[postgresql-configuration-tuning]] - Optimierung der WAL-Parameter
