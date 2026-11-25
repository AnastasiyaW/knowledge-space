---
title: "Interne Speicherstrukturen von Datenbanken"
category: concepts
tags: [sql-databases, storage, pages, heap, row-store, column-store, toast, io, disk]
level: 4
source_sha256: dd406d6a2f24242c6f4b97fa010998f2d1a4ec750021f8c7fb6ea2cc5dae3c18
translation: machine
translated_at: '2026-10-24'
---
# Interne Speicherstrukturen von Datenbanken {#database-storage-internals}

Das Verständnis dafür, wie Datenbanken Daten auf der Festplatte speichern und wieder abrufen, ist grundlegend für die Performance-Optimierung. Jede Abfrage wird letztlich in I/O-Operationen auf Seiten (Pages) übersetzt.

## Speicherarchitektur {#storage-architecture}

### Pages {#pages}
Die kleinste I/O-Einheit. Das Lesen einer einzelnen Zeile bedeutet das Lesen der gesamten Seite. Alle Zeilen dieser Seite werden anschließend im Buffer Pool verfügbar.

| RDBMS | Seitengröße |
|-------|-------------|
| PostgreSQL | 8 KB |
| MySQL InnoDB | 16 KB |
| SQL Server | 8 KB |

Bei 1000 Zeilen mit 3 Zeilen pro Seite ergeben sich etwa 334 Seiten. Ein vollständiger Tabellenscan liest alle 334 Seiten.

### Heap {#heap}
Ungeordnete Sammlung von Seiten, in denen die Tabellendaten liegen. Neue Zeilen werden am Ende angehängt (keine inhärente Sortierung). Ein vollständiger Heap-Scan (sequenzieller Scan) liest jede Seite, was bei selektiven Abfragen teuer ist.

### Row_ID / Tuple_ID {#row_id-tuple_id}
Interner Systembezeichner für jede Zeile:
- **MySQL InnoDB:** row_id = Primärschlüssel (clustered index)
- **PostgreSQL:** `ctid` = (page_number, offset), zeigt auf den physischen Speicherort

### I/O-Operationen {#io-operations}
Eine I/O-Operation liest eine oder mehrere Seiten. Ziel ist es, die Anzahl der I/O-Operationen zu minimieren. Einige I/Os werden aus dem OS-Cache bedient (kein Zugriff auf die Festplatte). I/O ist die primäre Kostenmetrik für die Abfrageperformance.

**SSD vs. HDD:** Wahlfreies Lesen (random read) dauert bei einer SSD etwa 0,1 ms, bei einer HDD etwa 10 ms (100-mal schneller). Sequenzielles Lesen ist bei einer SSD nur etwa 4-mal schneller als wahlfreies Lesen (bei einer HDD 100-mal). Dadurch ändern sich die Optimierungsstrategien: Wahlfreies I/O ist auf einer SSD weniger kostspielig.

## Row- vs. Column-Store {#row-vs-column-store}

**Zeilenorientiert (OLTP-Standard):** Die gesamte Zeile wird zusammen auf derselben Seite gespeichert.
- Geeignet für: `SELECT * FROM emp WHERE id = 1` (alle Spalten, eine Zeile)
- Ungeeignet für: `SELECT SUM(salary) FROM emp` (es werden alle Spalten gelesen, um auf eine zuzugreifen)
- Beispiele: PostgreSQL, MySQL, Oracle, SQL Server

**Spaltenorientiert (OLAP/Analytik):** Jede Spalte wird separat gespeichert.
- Geeignet für: `SUM(salary)`, liest nur die Spalte salary und ignoriert alles andere
- Ungeeignet für: `SELECT * WHERE id = 1`, hier müssen Dateien aller Spalten gelesen werden
- Beispiele: ClickHouse, Redshift, BigQuery, Parquet-Dateien
- Bessere Kompression (Daten gleichen Typs lassen sich gut komprimieren)

## TOAST (PostgreSQL) {#toast-postgresql}

Die Oversized-Attribute Storage Technique. Eine Zeilenversion muss in eine 8-KB-Seite passen.

- Große Werte werden automatisch komprimiert und/oder in eine separate TOAST-Tabelle ausgelagert
- Die TOAST-Tabelle besitzt einen eigenen Index
- Wird nur gelesen, wenn auf das große Attribut zugegriffen wird
- Unveränderte TOAST-Teile werden bei einem UPDATE der Zeile nicht dupliziert
- `SELECT *` erzwingt das Abrufen und Dekomprimieren aller TOAST-Spalten

## Write Amplification {#write-amplification}

Ein einzelner logischer Schreibvorgang verursacht mehrere physische Schreibvorgänge.

**PostgreSQL:** Das Aktualisieren einer beliebigen Spalte schreibt das gesamte Tupel neu (neue Version im Heap). Alle Indizes, die auf das alte Tupel verweisen, müssen neue Einträge erhalten. Ein HOT-Update (Heap-Only Tuple) vermeidet Indexaktualisierungen, wenn (1) die aktualisierten Spalten nicht indiziert sind UND (2) das neue Tupel auf dieselbe Seite passt.

**MySQL InnoDB:** Ein UPDATE ändert das Tupel an Ort und Stelle (sofern es auf die Seite passt). Sekundärindizes werden nur aktualisiert, wenn sich eine indizierte Spalte ändert. Bei schreiblastigen Workloads mit vielen UPDATEs ist die Write Amplification deutlich geringer.

**Migration bei Uber (2016):** Hauptmotivation war die Write Amplification von Postgres bei vielen Sekundärindizes. Die In-place-Updates von MySQL reduzierten das Schreib-I/O. Postgres wurde inzwischen durch HOT-Updates verbessert.

## Wichtige Fakten {#key-facts}

- Die Seitengröße bestimmt den Verzweigungsgrad des B+-Baums: Größere Seiten bedeuten mehr Schlüssel pro Knoten und damit einen flacheren Baum
- PostgreSQL speichert Zeilensperren im Tupel-Header, nicht im Speicher
- Vollständiges Schreiben von Seiten (`full_page_writes = on`) verhindert das Problem der zerrissenen Seiten (torn page), verdoppelt aber die Größe des WAL
- Der OS-Page-Cache kann Lesezugriffe ohne Festplatten-I/O bedienen. `effective_cache_size` informiert den Planner darüber
- `O_DIRECT` umgeht den OS-Cache zugunsten der datenbankeigenen Zwischenspeicherung

## Details zur Festplattenspeicherung {#disk-storage-details}

- Daten werden als Dateien gespeichert, die vom Dateisystem verwaltet werden (ext4, XFS, NTFS)
- SSDs verändern die Optimierung: `random_page_cost` sollte 1,1 bis 2,0 betragen (gegenüber 4,0 bei HDDs)
- NVMe: `effective_io_concurrency = 500-1000`; SATA-SSD: 200; HDD: Anzahl der Spindeln

## Fallstricke {#gotchas}

- `SELECT *` bremst die Performance, weil TOAST-Spalten geladen werden und Index-only Scans verhindert werden
- Das Hinzufügen von Spalten zu einer Tabelle verschlechtert bestehende `SELECT *`-Abfragen stillschweigend
- Memory-mapped I/O (mmap) vs. gepufferte I/O: PostgreSQL verwendet gepufferte I/O über `shared_buffers`
- Das OS kann Schreibvorgänge im Speicher zwischenspeichern. `fsync()` erzwingt das physische Schreiben auf die Festplatte

## Siehe auch {#see-also}

- [[btree-and-index-internals]] - Indexdatenstrukturen und Seitenteilungen (page splits)
- [[postgresql-mvcc-vacuum]] - Dead Tuples und Freigabe von Speicherplatz
- [[postgresql-wal-durability]] - Write-Ahead-Log für die Wiederherstellung nach Abstürzen
- [[query-optimization-explain]] - I/O-Kosten in Abfrageplänen verstehen
