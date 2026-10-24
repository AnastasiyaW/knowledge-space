---
title: "Replikationsgrundlagen"
category: concepts
tags: [sql-databases, replication, streaming-replication, logical-replication, synchronous, asynchronous, postgresql, read-replica]
level: 2
source_sha256: c6cef0ffc7132560bdd9f514061e0d3410a5c08afb115b4df146584c08ca07c5
translation: machine
translated_at: '2026-10-24'
---
# Replikationsgrundlagen {#replication-fundamentals}

Datenbankreplikation kopiert Daten von einem Primary auf eine oder mehrere Replicas, um Lesezugriffe zu skalieren, Hochverfügbarkeit zu gewährleisten und Daten geografisch zu verteilen. PostgreSQL unterstützt sowohl die physische Replikation (WAL-Streaming) als auch die logische Replikation.

## Replikationstypen {#replication-types}

| Typ | Mechanismus | Umfang | Anwendungsfall |
|-----|-------------|--------|----------------|
| Physisch (Streaming) | Byteweise Kopie des WAL | Gesamter Cluster | HA, Read Replicas |
| Logisch | Zeilenbasierte Änderungen | Ausgewählte Tabellen/Datenbanken | Versionsübergreifend, selektive Synchronisation |
| Synchron | Warten auf Replica-ACK | Konfigurierbar | Kein Datenverlust |
| Asynchron | Streamen ohne Warten | Standard | Geringere Latenz, Risiko eines gewissen Datenverlusts |

## Einrichtung des Streaming-Replikation {#streaming-replication-setup}

### Konfiguration des Primary {#primary-configuration}
```sql
-- Create replication user
CREATE USER repuser WITH REPLICATION ENCRYPTED PASSWORD 'pass';

-- pg_hba.conf
host  replication  repuser  0.0.0.0/0  scram-sha-256

-- postgresql.conf
listen_addresses = '*'
wal_level = replica
max_wal_senders = 10
```

### Einrichtung der Replica {#replica-setup}
```bash
# Clone primary data
pg_basebackup -h PRIMARY_IP -p 5432 -U repuser -R -D /var/lib/postgresql/15/main
# -R creates standby.signal and writes connection info to postgresql.auto.conf

# Start replica - it auto-connects as streaming standby
systemctl start postgresql
```

### Überwachung der Replikation {#monitoring-replication}
```sql
-- On primary: connected replicas and lag
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
  pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replay_lag_bytes
FROM pg_stat_replication;

-- On replica: lag check
SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(),
  pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn()) AS lag_bytes;
```

## pg_rewind – schnelle Neusynchronisation einer Replica {#pg_rewind-fast-replica-re-sync}

Wenn eine Replica divergiert (z. B. nach einem Split-Brain), synchronisiert `pg_rewind` sie neu, ohne ein vollständiges pg_basebackup zu benötigen:

```bash
pg_rewind --target-pgdata=/var/lib/postgresql/15/main \
          --source-server="host=primary port=5432 user=rewind_user"
```

Vergleicht die WAL-Historie und kopiert nur geänderte Blöcke. Erfordert `wal_log_hints = on` oder Datenprüfsummen.

## Probleme durch Replikationsverzögerung {#replication-lag-issues}

- **Veraltete Lesezugriffe:** Ein Benutzer schreibt Daten, liest sie unmittelbar danach von einer Replica und erhält alte Daten
- **Lösungen:** Read-after-Write-Konsistenz (aktuelle Schreibzugriffe an den Primary leiten), kausale Konsistenz, Sticky Sessions

## Wichtige Fakten {#key-facts}

- Replicas können Leseabfragen bearbeiten (Hot Standby) – Lesezugriffe an Replicas leiten, Schreibzugriffe an den Primary
- Synchrone Replikation: wartet auf mindestens ein ACK einer Replica. Stärkere Konsistenz, höhere Schreiblatenz
- Semisynchron: wartet auf mindestens eine Replica (Abwägung zwischen Konsistenz und Performance)
- `pg_promote()` oder `pg_ctl promote`, um einen Standby zum Primary zu befördern
- Kaskadierende Replikation: Replica repliziert von einer anderen Replica (reduziert die Last des Primary)
- Backups von einer Replica erstellen, um Performance-Beeinträchtigungen des Primary zu vermeiden

## Stolperfallen {#gotchas}

- Synchrone Replikation: Fällt die synchrone Replica aus, sinkt der Schreibdurchsatz des Primary auf null, bis ein Timeout eintritt
- Logische Replikation repliziert keine DDL-Änderungen – das Schema muss separat verwaltet werden
- WAL-Segmente auf dem Primary müssen aufbewahrt werden, bis alle Replicas sie verarbeitet haben
- Replikationsslots verhindern die WAL-Bereinigung, können aber die Festplatte füllen, wenn eine Replica länger getrennt bleibt
- `max_wal_senders` begrenzt die Anzahl gleichzeitiger Replikationsverbindungen

## Siehe auch {#see-also}

- [[postgresql-ha-patroni]] - automatisches Failover mit Patroni
- [[postgresql-wal-durability]] - WAL-Interna
- [[backup-and-recovery]] - WAL-Archivierung für PITR
- [[distributed-databases]] - Alternativen zur Multi-Master-Replikation
