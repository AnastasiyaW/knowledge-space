---
title: Backup and Recovery
category: reference
tags: [sql-databases, postgresql, backup, pg-dump, pg-basebackup, pg-probackup, wal-g, pitr, point-in-time-recovery]
---

# Backup and Recovery

PostgreSQL offers multiple backup strategies from logical dumps to continuous WAL archiving. The choice depends on database size, RPO/RTO requirements, and operational complexity tolerance.

## Backup Tools Comparison

| Tool | Type | Incremental | Parallel | Cloud-Native |
|------|------|------------|----------|-------------|
| pg_dump | Logical | No | Restore only | No |
| pg_basebackup | Physical | No | No | No |
| pg_probackup | Physical | Yes (FULL/PAGE/DELTA) | Yes | S3 via Ceph |
| WAL-G | Physical | Yes (delta) | Yes | S3/GCS/Azure |

## pg_dump / pg_dumpall

Logical backup - exports SQL statements. Works across PostgreSQL versions.

```bash
# Single table
pg_dump -h HOST -p 5432 -U user -d dbname --table=tablename > dump.sql

# Custom format (compressed, parallel restore)
pg_dump -Fc dbname > dump.custom
pg_restore -d newdb -j 4 dump.custom  # parallel restore with 4 jobs

# All databases + roles
pg_dumpall > full_dump.sql
```

## pg_basebackup

Physical backup - copies entire data directory. Base for streaming replication.

```bash
pg_basebackup -h PRIMARY_IP -p 5432 -U repuser -R -D /path/to/data
# -R creates standby.signal + connection info
# --no-slot avoids replication slot creation
```

## pg_probackup

Advanced backup utility: incremental backups, validation, multi-threaded operations.

```bash
# Initialize catalog
pg_probackup init -B /backup/catalog
pg_probackup add-instance -B /backup/catalog -D /var/lib/postgresql/15/main --instance main

# Full backup
pg_probackup backup -B /backup/catalog --instance main -b FULL --stream

# Incremental (PAGE mode - only changed pages)
pg_probackup backup -B /backup/catalog --instance main -b PAGE --stream

# Restore
pg_probackup restore -B /backup/catalog --instance main -i BACKUP_ID
```

**At scale (1500+ instances):** DELTA-only strategy (no periodic FULL), `--no-validate` and `--no-sync` during backup, merge retention. Incremental ratio ~0.12 (12% of full backup size).

## WAL-G

Cloud-native backup with S3/GCS/Azure support.

```bash
# Configure for S3
export WALG_S3_PREFIX=s3://my-bucket/pg-backups
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# Full backup
wal-g backup-push /var/lib/postgresql/15/main

# Restore latest
wal-g backup-fetch /var/lib/postgresql/15/main LATEST
```

## PITR (Point-in-Time Recovery)

Uses WAL archiving to restore to any point in time.

```bash
# Enable WAL archiving (postgresql.conf)
archive_mode = on
archive_command = 'cp %p /archive/%f'

# Restore to specific time
recovery_target_time = '2024-06-15 14:30:00'
```

Each recovery creates a new timeline. `pg_rewind` re-syncs diverged replicas without full re-copy.

## Pre-Loading Optimizations (Bulk Load)

Before bulk loading large datasets:
1. Disable autocommit
2. Drop indexes (recreate after load)
3. Drop foreign keys (recreate after)
4. Increase `maintenance_work_mem`
5. Increase `max_wal_size`

## Data Checksums

```bash
# Enable at initdb or via utility (requires shutdown)
pg_checksums --enable -D /var/lib/postgresql/15/main
```

Detects silent data corruption (bitrot). ~1-2% read overhead. Validated during backup (catches block corruption). Check: `SHOW data_checksums;`

## Production Backup Checklist

- Take backups from replica (avoid primary performance impact)
- Test restores regularly (automated restore testing)
- Monitor `archive_command` success
- Retention policy: 7-30 days depending on requirements
- Separate backup storage from database storage
- RPO (Recovery Point Objective): how much data loss is acceptable
- RTO (Recovery Time Objective): how fast must recovery complete

## Gotchas

- pg_dump is logical - does not preserve physical optimizations (table order, TOAST)
- pg_basebackup copies entire data directory - slow for large databases
- Lost WAL segments break backup chain for PITR
- Replication slots prevent WAL cleanup but can fill disk
- `pg_restore -j` parallelism only works with custom format (`-Fc`)
- PostgreSQL timelines: WAL files include timeline ID - don't replay WAL from wrong recovery branch

## See Also

- [[postgresql-wal-durability]] - WAL archiving configuration
- [[replication-fundamentals]] - pg_basebackup for replica setup
- [[postgresql-ha-patroni]] - replica creation from backup in Patroni
- [[postgresql-data-loading]] - bulk load optimization
