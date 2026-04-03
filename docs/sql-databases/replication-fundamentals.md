---
title: Replication Fundamentals
category: concepts
tags: [sql-databases, replication, streaming-replication, logical-replication, synchronous, asynchronous, postgresql, read-replica]
---

# Replication Fundamentals

Database replication copies data from a primary to one or more replicas for read scaling, high availability, and geographic distribution. PostgreSQL supports both physical (WAL streaming) and logical replication.

## Replication Types

| Type | Mechanism | Scope | Use Case |
|------|-----------|-------|----------|
| Physical (streaming) | WAL byte-level copy | Entire cluster | HA, read replicas |
| Logical | Row-level changes | Selective tables/databases | Cross-version, selective sync |
| Synchronous | Wait for replica ACK | Configurable | Zero data loss |
| Asynchronous | Stream without waiting | Default | Lower latency, some data loss risk |

## Streaming Replication Setup

### Primary Configuration
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

### Replica Setup
```bash
# Clone primary data
pg_basebackup -h PRIMARY_IP -p 5432 -U repuser -R -D /var/lib/postgresql/15/main
# -R creates standby.signal and writes connection info to postgresql.auto.conf

# Start replica - it auto-connects as streaming standby
systemctl start postgresql
```

### Monitoring Replication
```sql
-- On primary: connected replicas and lag
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
  pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replay_lag_bytes
FROM pg_stat_replication;

-- On replica: lag check
SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(),
  pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn()) AS lag_bytes;
```

## pg_rewind - Fast Replica Re-sync

When a replica diverges (e.g., after split-brain), `pg_rewind` re-synchronizes without full pg_basebackup:

```bash
pg_rewind --target-pgdata=/var/lib/postgresql/15/main \
          --source-server="host=primary port=5432 user=rewind_user"
```

Compares WAL history, copies only changed blocks. Requires `wal_log_hints = on` or data checksums.

## Replication Lag Issues

- **Stale reads:** User writes data, immediately reads from replica, gets old data
- **Solutions:** Read-after-write consistency (route recent writes to primary), causal consistency, sticky sessions

## Key Facts

- Replicas can serve read queries (hot standby) - direct reads to replicas, writes to primary
- Synchronous replication: wait for at least one replica ACK. Stronger consistency, higher write latency
- Semi-synchronous: wait for at least one replica (balance between consistency and performance)
- `pg_promote()` or `pg_ctl promote` to promote standby to primary
- Cascading replication: replica replicates from another replica (reduces primary load)
- Take backups from replica to avoid primary performance impact

## Gotchas

- Synchronous replication: if sync replica goes down, primary write throughput drops to zero until timeout
- Logical replication doesn't replicate DDL changes - schema must be managed separately
- WAL segments on primary must be retained until all replicas have consumed them
- Replication slots prevent WAL cleanup but can fill disk if replica disconnects for long time
- `max_wal_senders` limits concurrent replication connections

## See Also

- [[postgresql-ha-patroni]] - automated failover with Patroni
- [[postgresql-wal-durability]] - WAL internals
- [[backup-and-recovery]] - WAL archiving for PITR
- [[distributed-databases]] - multi-master replication alternatives
