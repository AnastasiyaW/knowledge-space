---
title: PostgreSQL Backup and Point-in-Time Recovery
category: reference
tags: [postgresql, backup, pitr, pg-basebackup, pg-probackup, wal-g, wal-archiving, restore]
---

# PostgreSQL Backup and Point-in-Time Recovery

PostgreSQL offers multiple backup strategies: logical (pg_dump), physical (pg_basebackup), and continuous archiving (WAL + base backup) for PITR. Production systems should use PITR-capable backups with tools like pg_probackup or WAL-G.

## Key Facts

- **Logical backup** (pg_dump/pg_dumpall) - SQL or custom-format dump. Portable across versions, table-level granularity. Slow for large databases, no PITR
- **Physical backup** (pg_basebackup) - file-level copy of the data directory. Fast, includes all databases. Basis for streaming replication setup
- **PITR** (Point-in-Time Recovery) - restore to any moment in time by replaying WAL from a base backup. Requires continuous WAL archiving
- **pg_probackup** - advanced backup tool: incremental backups (PAGE/DELTA), parallel backup/restore, backup catalog, merge, validation, retention policies
- **WAL-G** - backup tool by Yandex. Supports cloud storage (S3, GCS, Azure). Delta backups, WAL compression, encryption
- **Timelines** - each PITR attempt creates a new timeline. Prevents confusion between WAL from different recovery branches
- See [[postgresql-replication-ha]] for how WAL archiving relates to replication
- See [[postgresql-configuration-tuning]] for archive-related settings

## Patterns

### pg_dump (logical backup)

```bash
# Full database dump (custom format - compressed, restorable selectively)
pg_dump -Fc -j 4 -f /backup/mydb.dump mydb

# Specific tables
pg_dump -Fc -t users -t orders mydb > tables.dump

# Restore from custom format
pg_restore -d mydb -j 4 /backup/mydb.dump

# All databases
pg_dumpall > /backup/all_databases.sql

# Schema only (for migrations/documentation)
pg_dump --schema-only mydb > schema.sql
```

### pg_basebackup (physical backup)

```bash
# Create base backup with WAL streaming
pg_basebackup -h primary_host -U replicator \
    -D /backup/base \
    -Ft -z \           # tar format, compressed
    -Xs \              # stream WAL during backup
    -P                 # show progress

# The backup can be used to start a replica or as PITR starting point
```

### WAL archiving for PITR

```ini
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'           # simple local
# Or cloud storage:
# archive_command = 'wal-g wal-push %p'              # WAL-G to S3
# archive_command = 'pg_probackup archive-push -B /backup --instance=main %p'
```

### PITR recovery

```bash
# 1. Stop PostgreSQL
# 2. Move current data directory aside
# 3. Restore base backup
# 4. Create recovery configuration

# PostgreSQL 12+ uses postgresql.auto.conf + recovery.signal
cat > /var/lib/postgresql/data/postgresql.auto.conf << EOF
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '2024-06-15 14:30:00 UTC'
recovery_target_action = 'promote'
EOF

touch /var/lib/postgresql/data/recovery.signal

# 5. Start PostgreSQL - it replays WAL up to target time
# 6. After recovery, verify data, then drop recovery.signal
```

### pg_probackup workflow

```bash
# Initialize backup catalog
pg_probackup init -B /backup

# Add instance
pg_probackup add-instance -B /backup --instance=main -D /var/lib/postgresql/data

# Full backup
pg_probackup backup -B /backup --instance=main -b FULL --stream -j 4

# Incremental backup (PAGE mode - only changed pages)
pg_probackup backup -B /backup --instance=main -b PAGE --stream -j 4

# DELTA mode (changed files since last full)
pg_probackup backup -B /backup --instance=main -b DELTA --stream -j 4

# Validate backups
pg_probackup validate -B /backup --instance=main

# Retention policy (keep 7 days + 4 full backups)
pg_probackup delete -B /backup --instance=main \
    --retention-redundancy=4 --retention-window=7 --delete-expired

# Restore to specific time
pg_probackup restore -B /backup --instance=main \
    -D /var/lib/postgresql/data_restored \
    --recovery-target-time="2024-06-15 14:30:00+00"
```

### WAL-G with S3

```bash
# Environment setup
export WALG_S3_PREFIX=s3://my-bucket/wal-g
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export PGHOST=/var/run/postgresql

# Full backup
wal-g backup-push /var/lib/postgresql/data

# List backups
wal-g backup-list

# Restore latest
wal-g backup-fetch /var/lib/postgresql/data_restored LATEST

# Delete old backups (keep last 7)
wal-g delete retain FULL 7 --confirm
```

## Gotchas

- **pg_dump is NOT a point-in-time snapshot** - for large databases, pg_dump takes time, and the dump reflects different points for different tables unless using `--serializable-deferrable` (PostgreSQL 9.1+)
- **WAL archiving gap** - if archive_command fails silently, WAL files accumulate locally (pg_wal fills up) and you lose the archive chain. Monitor archive_command failures
- **PITR creates new timeline** - after recovery, WAL is on a new timeline (e.g., timeline 2). Replicas on timeline 1 cannot follow without resync. Use `recovery_target_timeline = 'latest'` on replicas
- **pg_probackup incremental ratio** - PAGE-level incremental backups are very efficient (~2-10% of full backup size) but require WAL between backups for validation
- **Restore time** - physical restore is much faster than pg_restore of a logical dump (especially for databases >100GB). Plan RTO accordingly
- **Test restores regularly** - an untested backup is not a backup. Schedule periodic restore drills

## See Also

- [[postgresql-replication-ha]] - WAL streaming for replication
- [[postgresql-configuration-tuning]] - WAL and archive settings
- [PostgreSQL continuous archiving](https://www.postgresql.org/docs/current/continuous-archiving.html)
- [pg_probackup docs](https://pg-probackup.readthedocs.io/)
- [WAL-G GitHub](https://github.com/wal-g/wal-g)
