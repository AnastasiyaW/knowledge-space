---
title: "PostgreSQL-Datenimport und FDW"
category: reference
tags: [sql-databases, postgresql, copy, fdw, foreign-data-wrapper, bulk-load, data-import, ogr-fdw]
level: 3
source_sha256: 4ab850f23899db501c3d655628fffebe30fc67ab27132d9a868f7edd3f551717
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL-Datenimport und FDW {#postgresql-data-loading-and-fdw}

PostgreSQL bietet mehrere Methoden zum Laden von Daten, von einfachen COPY-Befehlen bis zu Foreign Data Wrappers, die externe Datenquellen als reguläre Tabellen abfragbar machen.

## Lademethoden (von schnell bis langsam) {#loading-methods-fast-to-slow}

1. **COPY** (serverseitig, Superuser erforderlich) - am schnellsten
2. **\copy** (clientseitig über psql, kein Superuser nötig) - schnell
3. **Foreign Data Wrappers** - externe Daten als Tabellen abfragen
4. **INSERT**-Anweisungen - am langsamsten, transaktional

## COPY-Befehl {#copy-command}

```sql
-- Server-side COPY (postgres daemon needs file access)
COPY staging FROM '/path/to/file.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- From program output (PG 9.3+)
COPY staging FROM PROGRAM 'curl https://example.com/data.csv' WITH (FORMAT csv, HEADER true);

-- Client-side \copy (psql, no superuser needed)
\copy staging FROM 'local_file.csv' WITH (FORMAT csv, HEADER true)
```

## Foreign Data Wrappers (FDW) {#foreign-data-wrappers-fdw}

### file_fdw - Flache Dateien lesen {#file_fdw-read-flat-files}
```sql
CREATE EXTENSION file_fdw;
CREATE SERVER svr_file FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE fdt_data (col1 text, col2 int, col3 date)
  SERVER svr_file
  OPTIONS (format 'csv', header 'true', filename '/path/to/file.csv', delimiter ',');
```

### postgres_fdw - Entfernte PostgreSQL-Datenbank abfragen {#postgres_fdw-query-remote-postgresql}
```sql
CREATE EXTENSION postgres_fdw;
CREATE SERVER remote_db FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'remote.host.com', dbname 'db', port '5432');
CREATE USER MAPPING FOR public SERVER remote_db
  OPTIONS (user 'u', password 'p');
CREATE SCHEMA remote_public;
IMPORT FOREIGN SCHEMA public FROM SERVER remote_db INTO remote_public;
-- PG 10+: aggregate pushdown (COUNT, MAX) for cross-database queries
```

### ogr_fdw - Universeller Leser auf Basis von GDAL {#ogr_fdw-gdal-powered-universal-reader}
```sql
CREATE EXTENSION ogr_fdw;
-- CSV files
CREATE SERVER svr_csv FOREIGN DATA WRAPPER ogr_fdw
  OPTIONS (datasource '/data/csvs', format 'CSV');
IMPORT FOREIGN SCHEMA ogr_all FROM SERVER svr_csv INTO staging;

-- Excel spreadsheets (each sheet = table)
CREATE SERVER svr_rates FOREIGN DATA WRAPPER ogr_fdw
  OPTIONS (datasource '/path/Rates.xlsx', format 'XLSX',
           config_options 'OGR_XLSX_HEADERS=FORCE');

-- SQL Server via ODBC
CREATE SERVER svr_sqlserver FOREIGN DATA WRAPPER ogr_fdw
  OPTIONS (datasource 'ODBC:user/pass@DSN', format 'ODBC');
```

Weitere FDWs: mysql_fdw, oracle_fdw, db2_fdw, tds_fdw (SQL Server), multicorn (Python).

## Binärdateien über Large Objects {#binary-files-via-large-objects}
```sql
-- Store files as binary in database
CREATE TABLE docs (file_name text PRIMARY KEY, doc bytea, doc_oid oid);
UPDATE docs SET doc_oid = lo_import(file_name);   -- store in LO
UPDATE docs SET doc = lo_get(doc_oid);             -- retrieve blob
SELECT lo_unlink(doc_oid) FROM docs;               -- cleanup LO storage
```

## Kommandozeilenwerkzeuge {#command-line-tools}

```bash
# shp2pgsql: load shapefiles
shp2pgsql -s 4269 -D -d data/file shapefile_table | psql

# ogr2ogr: universal loader (GDAL)
ogr2ogr -f "PostgreSQL" "PG:host=localhost user=postgres dbname=db" data.osm.pbf
ogr2ogr -f "PostgreSQL" "PG:host=localhost user=postgres dbname=db" /data_csv/

# pgloader: migrate from MySQL/SQLite/CSV to PostgreSQL
pgloader mysql://user:pass@host/db postgresql://user:pass@host/db
```

## Optimierungen vor dem Laden {#pre-loading-optimizations}

Vor einem Bulk-Load:
1. Autocommit deaktivieren
2. Indizes löschen (nach dem Laden mit `CREATE INDEX CONCURRENTLY` neu erstellen)
3. Fremdschlüssel löschen (danach neu anlegen)
4. `maintenance_work_mem` erhöhen (für den Neuaufbau von Indizes)
5. `max_wal_size` erhöhen (seltenere Checkpoints)

## Wichtige Fakten {#key-facts}

- COPY ist 10- bis 100-mal schneller als einzelne INSERT-Anweisungen
- \copy funktioniert über das Netzwerk, ohne Zugriff auf das Dateisystem des Servers
- FDW-Tabellen sind mit regulärem SQL abfragbar, die Performance hängt jedoch von der Unterstützung für Pushdown ab
- postgres_fdw unterstützt Aggregat- und Join-Pushdown seit PG 10
- ogr_fdw liest unter anderem Tabellenkalkulationen, Shapefiles, ODBC, dBase, OSM-Daten und weitere Formate

## Stolperfallen {#gotchas}

- Serverseitiges COPY erfordert Superuser-Rechte und Dateizugriff für den postgres-Daemon
- FDW-Abfragen können langsam sein, wenn die gesamte entfernte Tabelle geholt wird, bevor gefiltert wird
- Die Large-Object-API (lo_import/lo_get) hat eine Größenbeschränkung von 2 GB pro Objekt
- pgloader ordnet MySQL-Typen automatisch PostgreSQL-Typen zu, in Randfällen kann aber eine manuelle Anpassung nötig sein
- COPY FROM PROGRAM führt den Befehl als Betriebssystembenutzer postgres aus - das hat Sicherheitsimplikationen

## Siehe auch {#see-also}

- [[backup-and-recovery]] - pg_dump/pg_restore für Datenmigration
- [[postgresql-configuration-tuning]] - maintenance_work_mem für Bulk-Loads
- [[ddl-schema-management]] - CREATE TABLE für Staging-Tabellen
- [[distributed-databases]] - Citus für verteiltes Laden von Daten
