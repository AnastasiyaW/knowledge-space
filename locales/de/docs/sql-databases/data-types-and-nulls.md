---
title: "Datentypen und NULL-Behandlung"
category: concepts
tags: [sql-databases, sql, data-types, null, mysql, postgresql, varchar, integer, decimal, timestamp]
level: 4
source_sha256: bdc5b18156cbbdf865b5476b31bde5cfdf45cf89020df52f040b2110eb90d03b
translation: machine
translated_at: '2026-10-24'
---
# Datentypen und NULL-Behandlung {#data-types-and-null-handling}

Die Wahl korrekter Datentypen beeinflusst Speicherbedarf, Performance und Datenintegrität. NULL-Behandlung mit dreiwertiger Logik gehört zu den subtilsten Aspekten von SQL.

## MySQL-Datentypen {#mysql-data-types}

### Numerisch {#numeric}
| Typ | Größe | Bereich |
|------|------|-------|
| TINYINT | 1 Byte | -128 bis 127 (UNSIGNED: 0-255) |
| SMALLINT | 2 Bytes | -32768 bis 32767 |
| MEDIUMINT | 3 Bytes | -8M bis 8M |
| INT | 4 Bytes | -2B bis 2B |
| BIGINT | 8 Bytes | -9.2E18 bis 9.2E18 |
| DECIMAL(M,D) | variabel | exakte Genauigkeit (für Geld) |
| FLOAT | 4 Bytes | ~7 Stellen Genauigkeit |
| DOUBLE | 8 Bytes | ~15 Stellen Genauigkeit |

### Zeichenketten {#string}
| Typ | Max. Größe | Hinweise |
|------|----------|-------|
| CHAR(N) | 255 | feste Länge, mit Leerzeichen aufgefüllt |
| VARCHAR(N) | 65,535 Bytes | variable Länge, 1-2 Bytes Overhead |
| TEXT | 65 KB | |
| MEDIUMTEXT | 16 MB | |
| LONGTEXT | 4 GB | |
| ENUM | 1-2 Bytes | ein Wert aus vordefinierter Liste |

### Datum/Zeit {#datetime}
| Typ | Format | Hinweise |
|------|--------|-------|
| DATE | YYYY-MM-DD | |
| TIME | HH:MM:SS | |
| DATETIME | YYYY-MM-DD HH:MM:SS | 8 Bytes, ohne Zeitzone |
| TIMESTAMP | gleiches Format | 4 Bytes, UTC-Konvertierung, Bereich 1970-2038 |
| YEAR | YYYY | 1 Byte |

## PostgreSQL-Datentypen {#postgresql-data-types}

| Typ | Hinweise |
|------|-------|
| SERIAL / BIGSERIAL | auto-inkrementierender Integer (4/8 Bytes) |
| INTEGER, BIGINT, SMALLINT | exakte Ganzzahlen |
| NUMERIC(p,s) / DECIMAL | exakter Dezimalwert |
| REAL, DOUBLE PRECISION | Gleitkommazahl |
| VARCHAR(n), TEXT | kein Performanceunterschied in PG |
| CHAR(n) | feste Länge, selten verwendet |
| BOOLEAN | true/false/null |
| DATE, TIME, TIMESTAMP | Standard-Datum/Zeit |
| TIMESTAMPTZ | Zeitstempel mit Zeitzone (bevorzugt) |
| INTERVAL | Zeitdauer |
| JSON / JSONB | natives JSON (JSONB ist binär, indexierbar) |
| UUID | 128-Bit-universell eindeutiger Identifikator |
| BYTEA | Binärdaten |
| INET, CIDR | IP-Adressen |

## NULL-Behandlung - Dreiwertige Logik {#null-handling-three-valued-logic}

NULL steht für fehlende/unbekannte Daten. Es ist KEIN Wert an sich.

```sql
-- Any comparison with NULL yields UNKNOWN
NULL = NULL    -- UNKNOWN (not TRUE)
NULL != 5      -- UNKNOWN (not TRUE)
NULL > 0       -- UNKNOWN

-- Correct NULL checks
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- COALESCE: first non-NULL argument
SELECT name, COALESCE(phone, 'No phone') FROM users;

-- NULLIF: returns NULL if arguments are equal
SELECT NULLIF(score, 0) FROM results;  -- avoid division by zero
```

## Wichtige Fakten {#key-facts}

- NULL-Speicher: 1 Bit pro nullable Spalte im NULL-Bitmap der Zeile
- `COUNT(*)` zählt alle Zeilen; `COUNT(column)` schließt NULLs aus
- SUM, AVG, MIN, MAX ignorieren alle NULLs
- GROUP BY fasst alle NULLs zu einer Gruppe zusammen
- NULLs in UNIQUE-Indizes: die meisten RDBMS erlauben mehrere NULLs; SQL Server standardmäßig nicht
- PostgreSQL: kein Performanceunterschied zwischen VARCHAR(n) und TEXT
- Für Geldbeträge immer DECIMAL/NUMERIC verwenden - FLOAT/DOUBLE haben Rundungsfehler

## Häufig verwendete Funktionen {#common-functions}

### String-Funktionen {#string-functions}
```sql
CONCAT(s1, s2)              -- concatenate (both)
LENGTH(s) / CHAR_LENGTH(s)  -- byte/character length
UPPER(s) / LOWER(s)         -- case conversion
TRIM(s) / LTRIM(s) / RTRIM(s)
SUBSTRING(s, pos, len)      -- extract substring
REPLACE(s, from, to)        -- replace occurrences
LEFT(s, n) / RIGHT(s, n)   -- first/last n characters
```

### Numerische Funktionen {#numeric-functions}
```sql
ROUND(n, d)  -- round to d decimal places
CEIL(n)      -- round up
FLOOR(n)     -- round down
ABS(n)       -- absolute value
MOD(n, m)    -- modulo
```

### Datumsfunktionen {#date-functions}
```sql
-- PostgreSQL
NOW(), CURRENT_DATE, CURRENT_TIMESTAMP
EXTRACT(YEAR FROM date_col)
AGE(timestamp1, timestamp2)         -- returns interval
date_col + INTERVAL '1 month'
TO_CHAR(date_col, 'YYYY-MM-DD')

-- MySQL
NOW(), CURDATE(), CURTIME()
YEAR(d) / MONTH(d) / DAY(d)
DATE_ADD(d, INTERVAL 1 DAY)
DATEDIFF(d1, d2)                    -- difference in days
TIMESTAMPDIFF(HOUR, d1, d2)
DATE_FORMAT(d, '%Y-%m-%d')
STR_TO_DATE(s, '%d/%m/%Y')
```

### Generierte Spalten (MySQL 8.0+, PostgreSQL 12+) {#generated-columns-mysql-80-postgresql-12}

Berechnete Spalten, gespeichert oder zur Laufzeit berechnet:
```sql
-- MySQL: STORED (on disk) or VIRTUAL (computed at read)
CREATE TABLE users (
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(101) GENERATED ALWAYS AS (CONCAT(first_name, ' ', last_name)) STORED
);
-- Can index STORED generated columns
CREATE INDEX idx_fullname ON users (full_name);

-- PostgreSQL 12+: only STORED
ALTER TABLE users ADD COLUMN full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED;
```

### JSON-Spalten-Muster {#json-column-patterns}

```sql
-- PostgreSQL JSONB: binary storage, indexable
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB NOT NULL
);

-- GIN index for containment queries
CREATE INDEX idx_payload ON events USING GIN (payload);

-- Query with operators
SELECT * FROM events WHERE payload @> '{"type": "click"}';         -- contains
SELECT * FROM events WHERE payload ->> 'user_id' = '42';           -- text extraction
SELECT * FROM events WHERE (payload -> 'meta' ->> 'score')::int > 90;  -- nested + cast

-- MySQL 8.0: JSON with generated column for indexing
ALTER TABLE events ADD COLUMN event_type VARCHAR(50)
    GENERATED ALWAYS AS (JSON_UNQUOTE(JSON_EXTRACT(payload, '$.type'))) STORED;
CREATE INDEX idx_event_type ON events (event_type);
```

### UUID als Primärschlüssel {#uuid-as-primary-key}

```sql
-- PostgreSQL: native UUID type
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);
-- Pro: no sequential guessing, safe for distributed systems
-- Con: larger than INT (16 bytes vs 4), random = fragmented B-tree inserts

-- UUIDv7 (time-sorted) available via extensions - preserves insert order
-- Better B-tree locality than UUIDv4
```

### Unerwartete Typumwandlungen {#unexpected-type-coercions}

```sql
-- MySQL silently truncates
INSERT INTO t (tinyint_col) VALUES (999);  -- stores 127 (max) with warning
-- PostgreSQL raises error for out-of-range

-- MySQL string-to-number coercion
SELECT * FROM users WHERE phone = 0;
-- Matches ALL rows where phone is a non-numeric string (coerced to 0)!
-- Always use: WHERE phone = '0'
```

## Stolperfallen {#gotchas}

- MySQL-`utf8` umfasst nur 3 Bytes (keine Emojis) - immer `utf8mb4` verwenden
- TIMESTAMP hat eine Grenze im Jahr 2038; für zukunftssichere Datumswerte DATETIME oder TIMESTAMPTZ verwenden
- FLOAT-Arithmetik: `0.1 + 0.2 != 0.3` - für exakte Vergleiche DECIMAL verwenden
- PostgreSQL SERIAL ist zugunsten von `GENERATED ALWAYS AS IDENTITY` veraltet
- NULL bei NOT IN: liefert die Unterabfrage einen NULL-Wert, gibt NOT IN ein leeres Ergebnis zurück
- Impliziter Typ-Cast in MySQL: `WHERE varchar_col = 0` trifft nicht-numerische Strings - Stringvergleiche immer in Anführungszeichen setzen
- JSONB in PostgreSQL ist ~30% größer als JSON, aber bei Abfragen deutlich schneller - immer JSONB bevorzugen, außer man benötigt die exakte Formatierungserhaltung
- UUID-Primärschlüssel verursachen B-Baum-Seitenteilungen bei zufälligen Inserts - UUIDv7 (zeitlich sortierbar) für bessere Schreibperformance erwägen
- Generierte Spalten können nicht auf andere generierte Spalten verweisen oder Unterabfragen verwenden

## Siehe auch {#see-also}

- [[ddl-schema-management]] - CREATE TABLE mit Datentypen
- [[schema-design-normalization]] - Auswahl von Typen beim Schema-Design
- [[select-fundamentals]] - CASE-Ausdrücke und berechnete Felder
