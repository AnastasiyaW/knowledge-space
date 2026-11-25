---
title: "MySQL InnoDB und Storage Engines"
category: concepts
tags: [sql-databases, mysql, innodb, myisam, storage-engine, clustered-index, redo-log]
level: 3
source_sha256: 6302494354580e21ad689052eaf28c2dff0566bd0a62f2f7caead441a5d69b56
translation: machine
translated_at: '2026-10-24'
---
# MySQL InnoDB und Storage Engines {#mysql-innodb-and-storage-engines}

MySQL unterstützt austauschbare Storage Engines. InnoDB (seit 5.5 der Standard) bietet ACID-Transaktionen, Row-Level-Locking und Crash-Recovery. Das Verständnis der Unterschiede zwischen den Engines ist für die MySQL-Administration unerlässlich.

## Vergleich der Storage Engines {#storage-engine-comparison}

| Engine | Transaktionen | Locking | Crash-Recovery | Anmerkungen |
|--------|-------------|---------|----------------|-------|
| **InnoDB** | Ja (ACID) | Row-Level | Redo-Log | Standard seit 5.5. MVCC, FK-Unterstützung |
| **MyISAM** | Nein | Table-Level | REPAIR TABLE | Veraltet. Schnelle Lesezugriffe, keine Crash-Recovery |
| **MEMORY/HEAP** | Nein | Table-Level | N/A (nur RAM) | Daten gehen beim Neustart verloren. Temporäre Tabellen |
| **Archive** | Nein | Row-Level | N/A | Nur INSERT + SELECT. Hohe Kompression |

## InnoDB-Architektur {#innodb-architecture}

- **Clustered Index auf PK:** Die Daten sind physisch nach dem Primärschlüssel sortiert. Jede Tabelle besitzt genau einen.
- **Sekundäre Indizes:** Die Blätter speichern den PK-Wert (nicht einen Row-Pointer). Ein Lookup erfordert zwei Schritte: sekundärer Index -> PK ermitteln -> Clustered Index -> Zeilendaten.
- **Redo-Log:** Das Äquivalent zum WAL. Zirkuläres Log für die Crash-Recovery.
- **Buffer Pool:** Speicherinterner Cache für Daten- und Indexseiten.
- **MVCC:** Read Committed und Repeatable Read über Undo-Logs (Row-Versionierung).

### Schreibverhalten: InnoDB vs. PostgreSQL {#innodb-vs-postgresql-write-behavior}

| Operation | InnoDB | PostgreSQL |
|-----------|--------|------------|
| UPDATE | In-place, sofern es in die Seite passt | Erzeugt ein neues Tupel (vollständige Kopie der Zeile) |
| Sekundärer Index bei UPDATE | Nur aktualisiert, wenn sich eine indizierte Spalte ändert | Alle Indizes werden aktualisiert (außer bei HOT) |
| Row-Locking | Im Speicher (Lock-Manager) | Im Tupel-Header (xmax-Feld) |

Bei UPDATE-lastigen Workloads mit vielen sekundären Indizes hat InnoDB deutlich weniger Write Amplification.

## MySQL-spezifische Lock-Typen {#mysql-specific-lock-types}

- **Gap Lock:** Sperrt die Lücke zwischen Indexeinträgen bei REPEATABLE READ. Verhindert Phantom Reads.
- **Next-Key Lock:** Gap Lock + Record Lock. Standard für RR in InnoDB.
- **Insert-Intention-Lock:** Erlaubt parallele Inserts an unterschiedlichen Positionen innerhalb derselben Lücke.
- **MDL (Metadata Lock):** DDL erwirbt einen exklusiven MDL und blockiert, bis alle DML-Vorgänge abgeschlossen sind.
- **SX-Lock (8.0.20+):** Shared-Exclusive für Online-DDL. Erlaubt parallele Lese- und Schreibzugriffe während bestimmter ALTER-TABLE-Operationen.

## LSM-Tree-Engines {#lsm-tree-engines}

**RocksDB (MyRocks):** LSM-Tree-Engine für MySQL, optimiert für Schreibzugriffe. Alle Schreibvorgänge sind sequenziell (Anhängen an WAL + Memtable). Hintergrund-Compaction führt SSTables zusammen. Bei schreiblastigen Workloads bietet sie einen höheren Schreibdurchsatz als InnoDB. Wird von Facebook eingesetzt.

**B+Tree vs. LSM-Tree:**
- B+Tree (InnoDB): leseoptimiert, Updates in-place, zufälliger I/O beim Schreiben
- LSM-Tree (RocksDB): schreiboptimiert, sequenzielle Schreibzugriffe, Read Amplification durch mehrere SSTables

## Wichtige Fakten {#key-facts}

- InnoDB erstellt automatisch einen Clustered Index auf dem PK. Ohne expliziten PK wird der erste eindeutige NOT-NULL-Index oder eine versteckte 6-Byte-row_id verwendet.
- `utf8` ist in MySQL 3-Byte-UTF-8 (keine Emojis) – immer `utf8mb4` verwenden.
- `SERIAL` = `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`
- Backticks für Bezeichner: `` `table` ``, `` `column` ``
- `SHOW ENGINES;` listet die verfügbaren Storage Engines auf.
- MyISAM wird für neue Anwendungen nicht empfohlen.

## MySQL-Monitoring {#mysql-monitoring}

```sql
SHOW DATABASES;
SHOW TABLES;
DESCRIBE table_name;
SHOW TABLE STATUS;              -- engine, rows, data/index size
SHOW ENGINE INNODB STATUS\G     -- detailed InnoDB metrics
SELECT VERSION();
```

## Fallstricke {#gotchas}

- Zufällige UUIDs als InnoDB-PK: der schlimmste Fall – der Clustered Index und alle sekundären Indizes erben die Zufälligkeit.
- MDL-Kaskade: ALTER TABLE wartet auf ein langes SELECT, danach reihen sich neue SELECTs hinter dem ALTER ein.
- Der Standard-Isolationslevel von InnoDB ist REPEATABLE READ (Gap Locks können unerwartete Blockaden verursachen).
- Verbindungskosten: ein Thread pro Verbindung. Für die Skalierung ProxySQL oder Connection-Pooling in der Anwendung verwenden.
- `TRUNCATE TABLE` setzt AUTO_INCREMENT in MySQL zurück (anders als in PostgreSQL).
- MyISAM-`REPAIR TABLE` läuft nicht automatisch – ohne Eingriff können Daten verloren gehen.

## Siehe auch {#see-also}

- [[btree-and-index-internals]] - Clustered vs. nicht gruppierte Indizes
- [[concurrency-and-locking]] - InnoDB-Lock-Typen
- [[transactions-and-acid]] - Isolationslevel in MySQL vs. PostgreSQL
- [[connection-pooling]] - ProxySQL für das Verbindungsmanagement in MySQL
