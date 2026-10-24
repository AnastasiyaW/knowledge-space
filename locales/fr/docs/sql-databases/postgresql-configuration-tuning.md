---
title: "Configuration et réglage de PostgreSQL"
category: reference
tags: [sql-databases, postgresql, configuration, tuning, shared-buffers, work-mem, postgresql-conf, pgbench, performance]
level: 3
source_sha256: ad21653eea45dd788251ffb47ea82729bea96de44f7048a3a491fce4bb44ecac
translation: machine
translated_at: '2026-10-24'
---
# Configuration et réglage de PostgreSQL {#postgresql-configuration-and-tuning}

Les performances de PostgreSQL dépendent fortement de la configuration. Les valeurs par défaut sont conservatrices et adaptées au développement, pas aux charges de production.

## Emplacements des fichiers de configuration {#config-file-locations}

| OS | Chemin |
|----|------|
| Ubuntu | `/etc/postgresql/15/main/postgresql.conf` |
| CentOS | `/var/lib/pgsql-15/data/postgresql.conf` |
| macOS | `/usr/local/var/postgres/postgresql.conf` |
| Windows | `C:\Program Files\PostgreSQL\15\data\postgresql.conf` |

Fichiers associés : `pg_hba.conf` (authentification), `pg_ident.conf` (correspondance des utilisateurs).

## Consulter et modifier les paramètres {#viewing-and-changing-parameters}

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

### Types de contexte des paramètres {#parameter-context-types}
- `internal` - non modifiable (défini à la compilation)
- `postmaster` - nécessite un redémarrage du serveur
- `sighup` - relecture des fichiers de configuration (sans redémarrage)
- `superuser` - modifiable à l'exécution par un superutilisateur
- `user` - modifiable à l'exécution par tout utilisateur

## Paramètres de performance clés {#key-performance-parameters}

### Mémoire {#memory}

| Paramètre | Description | Valeur de départ |
|-----------|-------------|----------------|
| `shared_buffers` | Cache principal des pages | 25 % de la RAM |
| `effective_cache_size` | Indication pour le planificateur sur le cache total (OS + PG) | 75 % de la RAM |
| `work_mem` | Mémoire de tri/hachage par opération | 10-64 Mo |
| `maintenance_work_mem` | VACUUM, CREATE INDEX | 256 Mo-1 Go |
| `temp_buffers` | Mémoire des tables temporaires | Valeur par défaut |
| `huge_pages` | Utiliser les huge pages si disponibles | `try` |

**Formule de mémoire :** `shared_buffers + (work_mem + temp_buffers) * max_connections` ne doit pas dépasser la RAM.

**ATTENTION :** Chaque tri/hachage dispose de son propre work_mem, et une même requête peut en utiliser plusieurs. `work_mem * connexions_actives * opérations_par_requête` doit tenir dans la RAM.

### WAL et points de contrôle {#wal-and-checkpoints}
| Paramètre | Description | Valeur de départ |
|-----------|-------------|----------------|
| `max_wal_size` | Taille maximale du WAL entre deux points de contrôle | 4-16 Go |
| `checkpoint_completion_target` | Répartition des E/S sur l'intervalle des points de contrôle | 0.9 |
| `wal_compression` | Compression des enregistrements WAL | on |
| `synchronous_commit` | Synchronisation du WAL au commit | on (le plus sûr) |

### Planificateur de requêtes {#query-planner}
| Paramètre | Description | Valeur de départ |
|-----------|-------------|----------------|
| `random_page_cost` | Coût de lecture aléatoire d'une page | 1.1-2.0 (SSD) |
| `effective_io_concurrency` | Requêtes E/S concurrentes | 200 (SSD), 500-1000 (NVMe) |
| `default_statistics_target` | Nombre de lignes échantillonnées pour les statistiques | 100-500 |
| `jit` | Compilation JIT | on pour l'analytique |

### Connexions {#connections}
| Paramètre | Description | Valeur de départ |
|-----------|-------------|----------------|
| `max_connections` | Nombre maximal de connexions clientes | 50-200 (utiliser un pooler) |
| `idle_in_transaction_session_timeout` | Termine les transactions inactives | 5-30 min |
| `statement_timeout` | Durée maximale d'une requête | spécifique à l'application |

## Accès réseau {#network-access}

```bash
# postgresql.conf
listen_addresses = '*'

# pg_hba.conf - allow remote connections
host  all  all  0.0.0.0/0  scram-sha-256

sudo pg_ctlcluster 15 main restart
```

## Benchmark avec pgbench {#benchmarking-with-pgbench}

```bash
# Initialize test database (~1.5M rows)
pgbench -h HOST -p 5432 -U postgres -i -s 15 benchmark

# Run test: 50 clients, 2 threads, report every 60s, run 3 minutes
pgbench -h HOST -p 5432 -U postgres -c 50 -j 2 -P 60 -T 180 benchmark
```

## Outils de réglage automatique {#auto-tuning-tools}

- **pgtune.leopard.in.ua** - calculateur web basé sur les caractéristiques matérielles
- **pgconfigurator.cybertec.at** - générateur de configuration avancé
- **timescaledb-tune** - outil en ligne de commande pour le réglage automatisé

## Pièges à éviter {#gotchas}

- La valeur par défaut `shared_buffers = 128MB` est bien trop faible pour la production
- `random_page_cost = 4.0` (valeur par défaut) pénalise les parcours d'index sur SSD : la ramener à 1.1-2.0
- Augmenter `max_connections` au-delà de 200 sans pooler provoque un surcoût de changements de contexte
- `effective_cache_size` n'alloue pas de mémoire : c'est une indication pour le planificateur
- Lorsqu'un même paramètre apparaît plusieurs fois, la dernière valeur l'emporte dans le fichier de configuration
- `ALTER SYSTEM SET` écrit dans `postgresql.auto.conf`, qui remplace les valeurs de `postgresql.conf`

## Voir aussi {#see-also}

- [[connection-pooling]] - PgBouncer lorsque max_connections est insuffisant
- [[postgresql-wal-durability]] - détails du réglage du WAL
- [[query-optimization-explain]] - paramètres de coût du planificateur
- [[postgresql-mvcc-vacuum]] - configuration de l'autovacuum
