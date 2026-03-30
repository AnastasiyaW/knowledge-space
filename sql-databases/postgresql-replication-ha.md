---
title: PostgreSQL Replication and High Availability
category: concepts
tags: [postgresql, replication, streaming, logical, patroni, etcd, pgbouncer, haproxy, failover, wal]
---

# PostgreSQL Replication and High Availability

PostgreSQL supports both physical (streaming) and logical replication. High availability (HA) clusters use tools like Patroni, etcd, HAProxy, and PgBouncer to provide automatic failover and connection routing.

## Key Facts

- **Streaming replication** (physical) - replica receives WAL stream from primary. Byte-for-byte copy of the database. Replica is read-only (hot standby). Supports synchronous and asynchronous modes
- **Logical replication** (PostgreSQL 10+) - publishes row-level changes via publications/subscriptions. Allows selective table replication, cross-version replication, different schemas on subscriber
- **WAL** (Write-Ahead Log) - every change written to WAL before data files. WAL shipping is the foundation of both replication types and PITR
- **Patroni** - the de facto standard for PostgreSQL HA. Uses distributed consensus (etcd/ZooKeeper/Consul) for leader election. Manages failover, switchover, and replica configuration
- **PgBouncer** - connection pooler, placed between application and PostgreSQL. Essential for HA setups to redirect connections during failover
- **HAProxy** - load balancer for routing read traffic to replicas, write traffic to primary
- See [[transactions-and-acid]] for how replication affects durability guarantees
- See [[postgresql-configuration-tuning]] for WAL-related configuration

## Patterns

### Streaming replication setup

```sql
-- On PRIMARY: postgresql.conf
-- wal_level = replica
-- max_wal_senders = 10
-- wal_keep_size = 1GB (or use replication slots)

-- Create replication user
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'secret';

-- pg_hba.conf: allow replication connections
-- host replication replicator replica_ip/32 md5

-- On REPLICA: create base backup
-- pg_basebackup -h primary_host -U replicator -D /var/lib/postgresql/data -Fp -Xs -P -R
-- The -R flag creates standby.signal and sets primary_conninfo in postgresql.auto.conf

-- Replication slots (prevent WAL cleanup before replica catches up)
SELECT pg_create_physical_replication_slot('replica1_slot');
-- Set in replica's postgresql.auto.conf: primary_slot_name = 'replica1_slot'

-- Monitor replication lag
SELECT client_addr, state, sent_lsn, replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS byte_lag
FROM pg_stat_replication;

-- On replica: check lag
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;
```

### Logical replication

```sql
-- On PUBLISHER (wal_level = logical)
CREATE PUBLICATION my_pub FOR TABLE users, orders;
-- Or all tables:
CREATE PUBLICATION my_pub FOR ALL TABLES;

-- On SUBSCRIBER
CREATE SUBSCRIPTION my_sub
    CONNECTION 'host=publisher_host dbname=mydb user=replicator password=secret'
    PUBLICATION my_pub;

-- Monitor subscription status
SELECT * FROM pg_stat_subscription;

-- Useful for: schema migrations, version upgrades, partial replication, data integration
```

### Patroni HA cluster architecture

```
                    +-----------+
                    |  HAProxy  |  (or keepalived VIP)
                    | :5000 RW  |
                    | :5001 RO  |
                    +-----+-----+
                          |
         +-------+--------+--------+
         |                |                |
  +------+------+  +------+------+  +------+------+
  | PostgreSQL  |  | PostgreSQL  |  | PostgreSQL  |
  |  (leader)   |  | (replica 1) |  | (replica 2) |
  |  Patroni    |  |  Patroni    |  |  Patroni    |
  +------+------+  +------+------+  +------+------+
         |                |                |
         +-------+--------+--------+
                          |
                    +-----+-----+
                    |   etcd    |  (3-node cluster)
                    | (DCS)     |
                    +-----------+
```

### Patroni key configuration

```yaml
# patroni.yml (key sections)
scope: postgres-cluster
name: node1

restapi:
  listen: 0.0.0.0:8008

etcd:
  hosts: etcd1:2379,etcd2:2379,etcd3:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # 1MB max lag for failover candidate
    postgresql:
      use_pg_rewind: true
      parameters:
        max_connections: 100
        shared_buffers: 4GB

postgresql:
  listen: 0.0.0.0:5432
  connect_address: node1:5432
  data_dir: /var/lib/postgresql/data
  authentication:
    replication:
      username: replicator
      password: secret
```

### pg_rewind for fast rejoin

```bash
# After failover, old primary can rejoin as replica using pg_rewind
# (instead of full base backup)
pg_rewind --target-pgdata=/var/lib/postgresql/data \
          --source-server="host=new_primary port=5432 user=postgres" \
          --progress
# Requires wal_log_hints = on or data checksums enabled
```

## Gotchas

- **Synchronous replication latency** - `synchronous_commit = on` with synchronous standby adds network round-trip to every commit. Use only when data loss is unacceptable (financial data)
- **Replication slots prevent WAL cleanup** - if a replica goes down and its slot remains, WAL files accumulate on primary until disk fills. Monitor `pg_replication_slots` and drop inactive slots
- **Split-brain risk** - if etcd/DCS is unavailable, Patroni demotes the leader (safety). This means a DCS failure takes down writes. Use a reliable 3-node etcd cluster
- **pg_rewind requires wal_log_hints or checksums** - without either, pg_rewind cannot detect diverged pages and will fail. Enable one of these before setting up HA
- **Logical replication sequences** - sequence values are NOT replicated by logical replication. After failover to a logical replica, sequences may be behind. Manual sync needed
- **Failover is not instant** - typical automatic failover with Patroni takes 10-30 seconds (DCS TTL + leader election + new leader promotion)

## See Also

- [[postgresql-backup-pitr]] - WAL archiving and point-in-time recovery
- [[postgresql-configuration-tuning]] - WAL and replication settings
- [PostgreSQL streaming replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [Patroni documentation](https://patroni.readthedocs.io/)
