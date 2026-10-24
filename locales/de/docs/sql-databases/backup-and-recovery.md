---
title: "Backup und Wiederherstellung"
category: reference
tags: [sql-databases, postgresql, backup, pg-dump, pg-basebackup, pg-probackup, wal-g, pitr, point-in-time-recovery]
level: 3
source_sha256: af582d28fe5ae61281ad0b1050a09ceb3b03a558e111f0eb1c0e0da1ee391aa2
translation: machine
translated_at: '2026-10-24'
---
# Backup und Wiederherstellung {#backup-and-recovery}

PostgreSQL bietet mehrere Backup-Strategien, von logischen Dumps bis zur kontinuierlichen WAL-Archivierung. Welche davon passt, hängt von der Datenbankgröße, den RPO/RTO-Anforderungen und der Bereitschaft zur operativen Komplexität ab.

## Vergleich der Backup-Tools {#backup-tools-comparison}

| Tool | Typ | Inkrementell | Parallel | Cloud-nativ |
|------|-----|--------------|----------|-------------|
| pg_dump | Logisch | Nein | Nur Restore | Nein |
| pg_basebackup | Physisch | Nein | Nein | Nein |
| pg_probackup | Physisch | Ja (FULL/PAGE/DELTA) | Ja | S3 via Ceph |
| WAL-G | Physisch | Ja (Delta) | Ja | S3/GCS/Azure |

## pg_dump / pg_dumpall {#pg_dump-pg_dumpall}

Logisches Backup – exportiert SQL-Anweisungen. Funktioniert über PostgreSQL-Versionen hinweg.

```bash
# Single table
pg_dump -h HOST -p 5432 -U user -d dbname --table=tablename > dump.sql

# Custom format (compressed, parallel restore)
pg_dump -Fc dbname > dump.custom
pg_restore -d newdb -j 4 dump.custom  # parallel restore with 4 jobs

# All databases + roles
pg_dumpall > full_dump.sql
```

## pg_basebackup {#pg_basebackup}

Physisches Backup – kopiert das gesamte Datenverzeichnis. Grundlage für Streaming-Replikation.

```bash
pg_basebackup -h PRIMARY_IP -p 5432 -U repuser -R -D /path/to/data
# -R creates standby.signal + connection info
# --no-slot avoids replication slot creation
```

## pg_probackup {#pg_probackup}

Erweitertes Backup-Werkzeug: inkrementelle Backups, Validierung, Multi-Thread-Operationen.

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

**Im großen Maßstab (1500+ Instanzen):** DELTA-only-Strategie (keine periodischen FULL-Backups), `--no-validate` und `--no-sync` während des Backups, Merge-Retention. Inkrementelles Verhältnis ~0,12 (12 % der Größe eines vollständigen Backups).

## WAL-G {#wal-g}

Cloud-natives Backup mit Unterstützung für S3/GCS/Azure.

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

## PITR (Point-in-Time Recovery) {#pitr-point-in-time-recovery}

Nutzt WAL-Archivierung, um auf einen beliebigen Zeitpunkt wiederherzustellen.

```bash
# Enable WAL archiving (postgresql.conf)
archive_mode = on
archive_command = 'cp %p /archive/%f'

# Restore to specific time
recovery_target_time = '2024-06-15 14:30:00'
```

Jede Wiederherstellung erzeugt eine neue Timeline. `pg_rewind` synchronisiert divergierte Replikate erneut, ohne vollständiges Neukopieren.

## Optimierungen vor dem Laden (Bulk Load) {#pre-loading-optimizations-bulk-load}

Vor dem Bulk-Laden großer Datenmengen:
1. Autocommit deaktivieren
2. Indizes löschen (nach dem Laden neu erstellen)
3. Fremdschlüssel löschen (danach neu erstellen)
4. `maintenance_work_mem` erhöhen
5. `max_wal_size` erhöhen

## Datenprüfsummen {#data-checksums}

```bash
# Enable at initdb or via utility (requires shutdown)
pg_checksums --enable -D /var/lib/postgresql/15/main
```

Erkennt stille Datenkorruption (Bitrot). ~1–2 % Overhead beim Lesen. Wird während des Backups validiert (erkennt Block-Korruption). Prüfen mit: `SHOW data_checksums;`

## Checkliste für Produktions-Backups {#production-backup-checklist}

- Backups von einem Replikat erstellen (vermeidet Leistungseinbußen auf dem Primary)
- Restores regelmäßig testen (automatisierte Restore-Tests)
- Erfolg von `archive_command` überwachen
- Aufbewahrungsrichtlinie: 7–30 Tage, je nach Anforderungen
- Backup-Speicher vom Datenbankspeicher trennen
- RPO (Recovery Point Objective): wie viel Datenverlust akzeptabel ist
- RTO (Recovery Time Objective): wie schnell die Wiederherstellung abgeschlossen sein muss

## Stolperfallen {#gotchas}

- pg_dump ist logisch – es bewahrt keine physischen Optimierungen (Tabellenreihenfolge, TOAST)
- pg_basebackup kopiert das gesamte Datenverzeichnis – langsam bei großen Datenbanken
- Verlorene WAL-Segmente unterbrechen die Backup-Kette für PITR
- Replikations-Slots verhindern das Bereinigen von WAL, können aber die Festplatte füllen
- Die Parallelität von `pg_restore -j` funktioniert nur mit dem Custom-Format (`-Fc`)
- PostgreSQL-Timelines: WAL-Dateien enthalten eine Timeline-ID – WAL nicht aus dem falschen Wiederherstellungszweig abspielen

## Siehe auch {#see-also}

- [[postgresql-wal-durability]] – Konfiguration der WAL-Archivierung
- [[replication-fundamentals]] – pg_basebackup für die Einrichtung von Replikaten
- [[postgresql-ha-patroni]] – Erstellen von Replikaten aus einem Backup in Patroni
- [[postgresql-data-loading]] – Optimierung des Bulk-Ladens
