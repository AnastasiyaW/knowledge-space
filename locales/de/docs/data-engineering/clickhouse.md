---
title: "ClickHouse"
category: tools
tags: [data-engineering, clickhouse, olap, columnar, analytics, database]
level: 3
source_sha256: 1a98d0e5f157926866ae0d05c9a331100bda9c7be64ae7e4fa0cf0fd603d6242
translation: machine
translated_at: '2026-10-24'
---
# ClickHouse {#clickhouse}

ClickHouse ist ein spaltenorientiertes DBMS für OLAP-Workloads. Entwickelt bei Yandex für Yandex.Metrica (13 Billionen Datensätze, 20 Milliarden Ereignisse/Tag). Optimiert auf Durchsatz statt Latenz: Milliarden Zeilen/Sekunde, ~50 ms Latenz akzeptabel, ~100 Abfragen/Sekunde pro Server.

## Wann ClickHouse einsetzen {#when-to-use-clickhouse}

| Profil | Eignung |
|--------|---------|
| Log-Management (flache breite Tabellen, nur Anfügen) | Hervorragend |
| Zeitreihen (Streaming-Inserts, einfache Aggregationen) | Hervorragend |
| Analytisches DWH (Stern-/Schneeflockenschema, ETL-Inserts) | Gut |
| Stark normalisiertes DWH (Data Vault, häufige Änderungen) | Schlecht |

## Was ClickHouse NICHT ist {#what-clickhouse-is-not}
Kein vollwertiges RDBMS: keine Transaktionen, keine Konsistenzgarantien, keine Cursor, keine gespeicherten Prozeduren, keine UNIQUE-/FOREIGN-KEY-Constraints. PRIMARY KEY erzwingt KEINE Eindeutigkeit. Nur partielle UPDATE/DELETE-Operationen als asynchrone Mutationen über ALTER TABLE.

## Spaltenorientierte Speicherung {#columnar-storage}

Daten werden spaltenweise gespeichert. Das Lesen von 3 Spalten aus einer breiten Tabelle liest ~3 % der Daten gegenüber einem vollständigen Zeilen-Scan. Sortierte Spalten komprimieren durch RLE stark.

**Regel:** Weniger Spalten im SELECT bedeutet weniger I/O. Immer die benötigten Spalten angeben, `SELECT *` vermeiden.

## Physische Speicherung {#physical-storage}

```php
Table
  -> Partitions (independent file groups on disk)
    -> Granules (default 8192 rows)
      -> Files: primary.idx, [column].mrk2, [column].bin
```

### Richtlinien für Partitionen {#partition-guidelines}
- Das Attribut MUSS in Abfragen vorkommen, andernfalls kein Partition Pruning
- Größe: wenige GB bis 150 GB pro Partition
- Typisch: `PARTITION BY toYYYYMM(date_column)`

```sql
SELECT partition, formatReadableSize(sum(bytes))
FROM system.parts WHERE table = 'my_table'
GROUP BY partition;
```

## Primärschlüssel und Granules {#primary-key-and-granules}

**Kritische Regel:** Der Primärschlüssel wirkt von links nach rechts. Für `ORDER BY (a, b, c)`:
- Filter auf `a` nutzt den Index
- Filter auf `a AND b` nutzt den Index
- Filter nur auf `b` **kann den Index nicht nutzen** und liest alle Granules

**PK in ClickHouse != PK in relationalen Datenbanken:** Keine Eindeutigkeit, keine FK-Referenzen. Reine Optimierung für die Leseperformance.

## DML {#dml}

```sql
INSERT INTO table VALUES (...), (...);
INSERT INTO table SELECT ... FROM other_table;

-- Async mutations (not instant!)
ALTER TABLE table UPDATE col = val WHERE condition;
ALTER TABLE table DELETE WHERE condition;
OPTIMIZE TABLE table FINAL;  -- force merge
```

## ClickHouse-spezifische Funktionen {#clickhouse-specific-functions}

### Approximative vs. exakte Zählung {#approximate-vs-exact-counting}

| Funktion | Genauigkeit | Performance |
|----------|-------------|-------------|
| `uniq()` | Approximativ (HyperLogLog) | Schnell |
| `uniqExact()` | Exakt | Langsam, hoher Speicherbedarf |
| `uniqCombined()` | Hybrid | Ausgewogen |

### Aggregat-Suffixe {#aggregate-suffixes}

```sql
sumIf(amount, status = 'completed')   -- conditional sum
countIf(id, type = 'click')           -- conditional count
avgIf(score, score > 0)               -- conditional average
```

### Quantile {#quantiles}

```sql
SELECT quantile(0.5)(price) AS median_approx FROM prices;
SELECT quantileExact(0.5)(salary) AS median_exact FROM employees;
SELECT quantiles(0.25, 0.5, 0.75)(price) AS quartiles FROM prices;
```

## Erweiterte JOINs {#extended-joins}

| Typ | Verhalten |
|-----|-----------|
| LEFT SEMI JOIN | Linke Zeilen mit Treffer (keine rechten Spalten) |
| LEFT ANTI JOIN | Linke Zeilen OHNE Treffer |
| LEFT ANY JOIN | Ein zufälliger Treffer aus der rechten Tabelle |
| ASOF JOIN | Zuordnung über den nächstliegenden geordneten Wert |

### ASOF JOIN {#asof-join}

```sql
SELECT m.time, m.value, e.event
FROM metrics m
ASOF LEFT JOIN events e
  ON m.user_id = e.user_id AND m.time >= e.time;
```

## Abfrageanalyse {#query-analysis}

```sql
EXPLAIN PLAN indexes = 1 SELECT ...;
```

**Optimal:** Filter sowohl auf den Partitionsschlüssel ALS AUCH auf den Primärschlüssel für zweistufiges Pruning.

## Fallstricke {#gotchas}
- UPDATE/DELETE sind asynchrone Mutationen und nicht für häufige Einzelzeilen-Operationen ausgelegt
- Deduplizierung bei ReplacingMergeTree erfolgt während der Merges, nicht sofort; `SELECT ... FINAL` verwenden
- Primärschlüssel erzwingt keine Eindeutigkeit
- UDFs verlangsamen ClickHouse erheblich
- Immer korrekte Datentypen verwenden (UInt32 statt String für IDs), damit die Kompression greift

## Siehe auch {#see-also}
- [[clickhouse-engines]] – MergeTree-Familie und Auswahl der Engine
- [[dwh-architecture]] – ClickHouse als OLAP-Schicht
- [[sql-for-de]] – SQL-Muster
