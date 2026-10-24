---
title: "Chargement de données PostgreSQL et FDW"
category: reference
tags: [sql-databases, postgresql, copy, fdw, foreign-data-wrapper, bulk-load, data-import, ogr-fdw]
level: 3
source_sha256: 4ab850f23899db501c3d655628fffebe30fc67ab27132d9a868f7edd3f551717
translation: machine
translated_at: '2026-10-24'
---
# Chargement de données PostgreSQL et FDW {#postgresql-data-loading-and-fdw}

PostgreSQL propose plusieurs méthodes de chargement de données, allant des simples commandes COPY aux Foreign Data Wrappers qui permettent d'interroger des sources de données externes comme des tables classiques.

## Méthodes de chargement (de la plus rapide à la plus lente) {#loading-methods-fast-to-slow}

1. **COPY** (côté serveur, superutilisateur requis) - le plus rapide
2. **\copy** (côté client via psql, sans superutilisateur) - rapide
3. **Foreign Data Wrappers** - interroger des données externes comme des tables
4. **Instructions INSERT** - le plus lent, transactionnel

## Commande COPY {#copy-command}

```sql
-- Server-side COPY (postgres daemon needs file access)
COPY staging FROM '/path/to/file.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- From program output (PG 9.3+)
COPY staging FROM PROGRAM 'curl https://example.com/data.csv' WITH (FORMAT csv, HEADER true);

-- Client-side \copy (psql, no superuser needed)
\copy staging FROM 'local_file.csv' WITH (FORMAT csv, HEADER true)
```

## Foreign Data Wrappers (FDW) {#foreign-data-wrappers-fdw}

### file_fdw - Lecture de fichiers plats {#file_fdw-read-flat-files}
```sql
CREATE EXTENSION file_fdw;
CREATE SERVER svr_file FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE fdt_data (col1 text, col2 int, col3 date)
  SERVER svr_file
  OPTIONS (format 'csv', header 'true', filename '/path/to/file.csv', delimiter ',');
```

### postgres_fdw - Interroger un PostgreSQL distant {#postgres_fdw-query-remote-postgresql}
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

### ogr_fdw - Lecteur universel basé sur GDAL {#ogr_fdw-gdal-powered-universal-reader}
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

Autres FDW : mysql_fdw, oracle_fdw, db2_fdw, tds_fdw (SQL Server), multicorn (Python).

## Fichiers binaires via les Large Objects {#binary-files-via-large-objects}
```sql
-- Store files as binary in database
CREATE TABLE docs (file_name text PRIMARY KEY, doc bytea, doc_oid oid);
UPDATE docs SET doc_oid = lo_import(file_name);   -- store in LO
UPDATE docs SET doc = lo_get(doc_oid);             -- retrieve blob
SELECT lo_unlink(doc_oid) FROM docs;               -- cleanup LO storage
```

## Outils en ligne de commande {#command-line-tools}

```bash
# shp2pgsql: load shapefiles
shp2pgsql -s 4269 -D -d data/file shapefile_table | psql

# ogr2ogr: universal loader (GDAL)
ogr2ogr -f "PostgreSQL" "PG:host=localhost user=postgres dbname=db" data.osm.pbf
ogr2ogr -f "PostgreSQL" "PG:host=localhost user=postgres dbname=db" /data_csv/

# pgloader: migrate from MySQL/SQLite/CSV to PostgreSQL
pgloader mysql://user:pass@host/db postgresql://user:pass@host/db
```

## Optimisations avant chargement {#pre-loading-optimizations}

Avant un chargement massif :
1. Désactiver l'autocommit
2. Supprimer les index (les recréer après le chargement avec `CREATE INDEX CONCURRENTLY`)
3. Supprimer les clés étrangères (les recréer ensuite)
4. Augmenter `maintenance_work_mem` (pour la reconstruction des index)
5. Augmenter `max_wal_size` (réduire la fréquence des checkpoints)

## Points clés {#key-facts}

- COPY est 10 à 100 fois plus rapide que des instructions INSERT individuelles
- \copy fonctionne through le réseau sans accès au système de fichiers du serveur
- Les tables FDW sont interrogeables avec du SQL standard, mais les performances dépendent du support du pushdown
- postgres_fdw prend en charge le pushdown des agrégats et des jointures depuis PG 10
- ogr_fdw lit : les tableurs, les shapefiles, ODBC, dbase, les données OSM, et bien d'autres

## Pièges à éviter {#gotchas}

- Le COPY côté serveur requiert les droits superutilisateur et un accès aux fichiers par le démon postgres
- Les requêtes FDW peuvent être lentes si la table distante entière est récupérée avant le filtrage
- L'API Large Object (lo_import/lo_get) est limitée à 2 Go par objet
- pgloader convertit automatiquement les types MySQL vers PostgreSQL, mais peut nécessiter un ajustement manuel pour les cas particuliers
- COPY FROM PROGRAM exécute la commande sous l'utilisateur système postgres : attention aux implications en matière de sécurité

## Voir aussi {#see-also}

- [[backup-and-recovery]] - pg_dump/pg_restore pour la migration de données
- [[postgresql-configuration-tuning]] - maintenance_work_mem pour les chargements massifs
- [[ddl-schema-management]] - CREATE TABLE pour les tables de transit
- [[distributed-databases]] - Citus pour le chargement de données distribué
