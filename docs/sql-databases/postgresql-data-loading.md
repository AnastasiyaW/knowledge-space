---
title: PostgreSQL Data Loading and FDW
category: reference
tags: [sql-databases, postgresql, copy, fdw, foreign-data-wrapper, bulk-load, data-import, ogr-fdw]
---

# PostgreSQL Data Loading and FDW

PostgreSQL provides multiple methods for loading data, from simple COPY commands to Foreign Data Wrappers that make external data sources queryable as regular tables.

## Loading Methods (Fast to Slow)

1. **COPY** (server-side, superuser required) - fastest
2. **\copy** (client-side via psql, no superuser) - fast
3. **Foreign Data Wrappers** - query external data as tables
4. **INSERT** statements - slowest, transactional

## COPY Command

```sql
-- Server-side COPY (postgres daemon needs file access)
COPY staging FROM '/path/to/file.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- From program output (PG 9.3+)
COPY staging FROM PROGRAM 'curl https://example.com/data.csv' WITH (FORMAT csv, HEADER true);

-- Client-side \copy (psql, no superuser needed)
\copy staging FROM 'local_file.csv' WITH (FORMAT csv, HEADER true)
```

## Foreign Data Wrappers (FDW)

### file_fdw - Read Flat Files
```sql
CREATE EXTENSION file_fdw;
CREATE SERVER svr_file FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE fdt_data (col1 text, col2 int, col3 date)
  SERVER svr_file
  OPTIONS (format 'csv', header 'true', filename '/path/to/file.csv', delimiter ',');
```

### postgres_fdw - Query Remote PostgreSQL
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

### ogr_fdw - GDAL-Powered Universal Reader
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

Other FDWs: mysql_fdw, oracle_fdw, db2_fdw, tds_fdw (SQL Server), multicorn (Python).

## Binary Files via Large Objects
```sql
-- Store files as binary in database
CREATE TABLE docs (file_name text PRIMARY KEY, doc bytea, doc_oid oid);
UPDATE docs SET doc_oid = lo_import(file_name);   -- store in LO
UPDATE docs SET doc = lo_get(doc_oid);             -- retrieve blob
SELECT lo_unlink(doc_oid) FROM docs;               -- cleanup LO storage
```

## Command-Line Tools

```bash
# shp2pgsql: load shapefiles
shp2pgsql -s 4269 -D -d data/file shapefile_table | psql

# ogr2ogr: universal loader (GDAL)
ogr2ogr -f "PostgreSQL" "PG:host=localhost user=postgres dbname=db" data.osm.pbf
ogr2ogr -f "PostgreSQL" "PG:host=localhost user=postgres dbname=db" /data_csv/

# pgloader: migrate from MySQL/SQLite/CSV to PostgreSQL
pgloader mysql://user:pass@host/db postgresql://user:pass@host/db
```

## Pre-Loading Optimizations

Before bulk loading:
1. Disable autocommit
2. Drop indexes (recreate after load with `CREATE INDEX CONCURRENTLY`)
3. Drop foreign keys (recreate after)
4. Increase `maintenance_work_mem` (for index rebuild)
5. Increase `max_wal_size` (reduce checkpoint frequency)

## Key Facts

- COPY is 10-100x faster than individual INSERT statements
- \copy works over network without server filesystem access
- FDW tables are queryable with regular SQL but performance depends on pushdown support
- postgres_fdw supports aggregate and join pushdown since PG 10
- ogr_fdw reads: spreadsheets, shapefiles, ODBC, dbase, OSM data, and more

## Gotchas

- Server-side COPY requires superuser and file access by postgres daemon
- FDW queries may be slow if entire remote table is fetched before filtering
- Large Object API (lo_import/lo_get) has 2GB size limit per object
- pgloader auto-maps MySQL types to PostgreSQL but may need manual tuning for edge cases
- COPY FROM PROGRAM runs the command as the postgres OS user - security implications

## See Also

- [[backup-and-recovery]] - pg_dump/pg_restore for data migration
- [[postgresql-configuration-tuning]] - maintenance_work_mem for bulk loads
- [[ddl-schema-management]] - CREATE TABLE for staging tables
- [[distributed-databases]] - Citus for distributed data loading
