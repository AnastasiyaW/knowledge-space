---
title: "PostgreSQL-Konfiguration und Tuning"
category: reference
tags: [sql-databases, postgresql, configuration, tuning, shared-buffers, work-mem, postgresql-conf, pgbench, performance]
level: 3
source_sha256: ad21653eea45dd788251ffb47ea82729bea96de44f7048a3a491fce4bb44ecac
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL-Konfiguration und Tuning {#postgresql-configuration-and-tuning}

Die Performance von PostgreSQL hängt stark von einer passenden Konfiguration ab. Die Standardeinstellungen sind konservativ und für die Entwicklung gedacht, nicht für Produktionslasten.

## Speicherorte der Konfigurationsdateien {#config-file-locations}

| OS | Pfad |
|----|------|
| Ubuntu | `/etc/postgresql/15/main/postgresql.conf` |
| CentOS | `/var/lib/pgsql-15/data/postgresql.conf` |
| macOS | `/usr/local/var/postgres/postgresql.conf` |
| Windows | `C:\Program Files\PostgreSQL\15\data\postgresql.conf` |

Weitere relevante Dateien: `pg_hba.conf` (Authentifizierung), `pg_ident.conf` (Benutzerzuordnung).

## Parameter anzeigen und ändern {#viewing-and-changing-parameters}

```sql
SHOW config_file;
SHOW shared_buffers;
SELECT current_setting('max_connections');

-- Persistent change (writes to postgresql.auto.conf, does NOT apply immediately)
ALTER SYSTEM SET shared_buffers = '2GB';
-- Then reload or restart:
SELECT pg_reload_conf();  -- for sighup-context params
-- pg_ctl restart          -- for postmaster-context params

-- Session-level (temporary)
SET work_mem = '256MB';

-- Reset
ALTER SYSTEM RESET shared_buffers;
```

### Parameter-Kontexttypen {#parameter-context-types}
- `internal` - nicht änderbar (zur Kompilierzeit festgelegt)
- `postmaster` - erfordert einen Neustart des Servers
- `sighup` - Konfigurationsdateien werden neu eingelesen (kein Neustart)
- `superuser` - zur Laufzeit durch Superuser änderbar
- `user` - zur Laufzeit durch jeden Benutzer änderbar

## Wichtige Leistungsparameter {#key-performance-parameters}

### Speicher {#memory}

| Parameter | Beschreibung | Richtwert |
|-----------|-------------|----------------|
| `shared_buffers` | Haupt-Seitencache | 25 % des RAM |
| `effective_cache_size` | Planer-Hinweis für den Gesamtcache (OS + PG) | 75 % des RAM |
| `work_mem` | Sort-/Hash-Speicher pro Operation | 10-64 MB |
| `maintenance_work_mem` | VACUUM, CREATE INDEX | 256 MB-1 GB |
| `temp_buffers` | Speicher für temporäre Tabellen | Standard |
| `huge_pages` | Huge Pages verwenden, falls verfügbar | `try` |

**Speicherformel:** `shared_buffers + (work_mem + temp_buffers) * max_connections` darf den RAM nicht überschreiten.

**WARNUNG:** Jede Sort- bzw. Hash-Operation erhält ihr eigenes work_mem, und eine einzelne Abfrage kann mehrere davon benötigen. `work_mem * active_connections * operations_per_query` muss in den RAM passen.

### WAL und Checkpoints {#wal-and-checkpoints}
| Parameter | Beschreibung | Richtwert |
|-----------|-------------|----------------|
| `max_wal_size` | Maximale WAL-Menge zwischen Checkpoints | 4-16 GB |
| `checkpoint_completion_target` | I/O über das Checkpoint-Intervall verteilen | 0.9 |
| `wal_compression` | WAL-Datensätze komprimieren | on |
| `synchronous_commit` | WAL-Sync beim Commit | on (am sichersten) |

### Query-Planer {#query-planner}
| Parameter | Beschreibung | Richtwert |
|-----------|-------------|----------------|
| `random_page_cost` | Kosten für zufälliges Seitenlesen | 1.1-2.0 (SSD) |
| `effective_io_concurrency` | Gleichzeitige I/O-Anfragen | 200 (SSD), 500-1000 (NVMe) |
| `default_statistics_target` | Für Statistiken gesampelte Zeilen | 100-500 |
| `jit` | JIT-Kompilierung | on für Analytics |

### Verbindungen {#connections}
| Parameter | Beschreibung | Richtwert |
|-----------|-------------|----------------|
| `max_connections` | Maximale Client-Verbindungen | 50-200 (Pooler verwenden) |
| `idle_in_transaction_session_timeout` | Idle-Transaktionen beenden | 5-30 Min. |
| `statement_timeout` | Maximale Abfragedauer | anwendungsspezifisch |

## Netzwerkzugriff {#network-access}

```bash
# postgresql.conf
listen_addresses = '*'

# pg_hba.conf - allow remote connections
host  all  all  0.0.0.0/0  scram-sha-256

sudo pg_ctlcluster 15 main restart
```

## Benchmarking mit pgbench {#benchmarking-with-pgbench}

```bash
# Initialize test database (~1.5M rows)
pgbench -h HOST -p 5432 -U postgres -i -s 15 benchmark

# Run test: 50 clients, 2 threads, report every 60s, run 3 minutes
pgbench -h HOST -p 5432 -U postgres -c 50 -j 2 -P 60 -T 180 benchmark
```

## Auto-Tuning-Werkzeuge {#auto-tuning-tools}

- **pgtune.leopard.in.ua** - Web-Rechner auf Basis der Hardware-Spezifikation
- **pgconfigurator.cybertec.at** - erweiterter Konfigurationsgenerator
- **timescaledb-tune** - CLI-Werkzeug für automatisiertes Tuning

## Fallstricke {#gotchas}

- Der Standardwert `shared_buffers = 128MB` ist für Produktion viel zu niedrig
- `random_page_cost = 4.0` (Standard) benachteiligt Index-Scans auf SSDs - auf 1.1-2.0 senken
- Ein Erhöhen von `max_connections` über 200 ohne Pooler verursacht Overhead durch Kontextwechsel
- `effective_cache_size` alloziert keinen Speicher - es ist ein Planer-Hinweis
- Taucht derselbe Parameter mehrfach auf, gilt in der Konfigurationsdatei der letzte Wert
- `ALTER SYSTEM SET` schreibt in `postgresql.auto.conf` und überschreibt `postgresql.conf`

## Siehe auch {#see-also}

- [[connection-pooling]] - PgBouncer, wenn max_connections nicht ausreicht
- [[postgresql-wal-durability]] - Details zum WAL-Tuning
- [[query-optimization-explain]] - Kostenparameter des Planers
- [[postgresql-mvcc-vacuum]] - Konfiguration von Autovacuum
