---
title: PostgreSQL HA with Patroni
category: reference
tags: [sql-databases, postgresql, patroni, etcd, haproxy, high-availability, failover, switchover, ha-cluster]
---

# PostgreSQL HA with Patroni

Patroni is a Python daemon running alongside PostgreSQL that manages automatic failover, leader election, and cluster configuration via a distributed configuration store (DCS).

## Architecture

Components: 3+ PostgreSQL instances + Patroni, 3+ etcd nodes (or co-located), HAProxy/PgBouncer for routing.

Patroni bridges PostgreSQL and etcd - PostgreSQL cannot interact with etcd directly. Since v2.0: native Raft protocol available (no external etcd/consul needed).

## Patroni YAML Configuration

```yaml
scope: postgres-cluster
namespace: /db/
name: pg01

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.0.1:8008

etcd:
  hosts: 10.0.0.1:2379,10.0.0.2:2379,10.0.0.3:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
  postgresql:
    parameters:
      max_connections: 100
      shared_buffers: 2GB
      wal_level: replica

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.0.1:5432
  data_dir: /var/lib/postgresql/15/main
  authentication:
    replication:
      username: replicator
      password: rep_pass
    superuser:
      username: postgres
      password: pg_pass
  callbacks:
    on_start: /opt/pgsql/pg_start.sh
    on_stop: /opt/pgsql/pg_stop.sh
    on_role_change: /opt/pgsql/pg_role_change.sh
```

## Key Parameters

- `loop_wait`: seconds between leader key update attempts
- `retry_timeout`: retry interval for key updates
- `ttl`: leader key lifetime. Recommend: >= loop_wait + retry_timeout
- `maximum_lag_on_failover`: max replica lag (bytes) to participate in elections
- `synchronous_mode`: enable synchronous replica
- `synchronous_mode_strict`: master stops if sync replica dies

## Cluster Management (patronictl)

```bash
patronictl -c /etc/patroni.yml list            # cluster status
patronictl -c /etc/patroni.yml edit-config      # edit DCS configuration
patronictl -c /etc/patroni.yml switchover       # planned manual role switch
patronictl -c /etc/patroni.yml failover         # forced failover
patronictl -c /etc/patroni.yml restart postgres pg02  # restart specific node
patronictl -c /etc/patroni.yml reinit postgres pg03   # wipe + pg_basebackup
patronictl -c /etc/patroni.yml pause|resume     # disable/enable auto-failover
```

## HAProxy Configuration

```
listen postgres_write
    bind *:5000
    option httpchk GET /master
    http-check expect status 200
    server pg01 10.0.0.1:5432 check port 8008
    server pg02 10.0.0.2:5432 check port 8008
    server pg03 10.0.0.3:5432 check port 8008

listen postgres_read
    bind *:5001
    option httpchk GET /replica
    http-check expect status 200
    server pg01 10.0.0.1:5432 check port 8008
    server pg02 10.0.0.2:5432 check port 8008
    server pg03 10.0.0.3:5432 check port 8008
```

## REST API for Monitoring

- `GET /master` - returns 200 only for leader, 503 for others
- `GET /replica` - returns 200 for replicas
- `GET /patroni` - returns state, replication status, WAL position

## Node Tags

```yaml
tags:
  nofailover: true       # never becomes master
  noloadbalance: true    # /replica always returns 503
  clonefrom: true        # preferred source for pg_basebackup
  nosync: true           # never becomes synchronous replica
  replicatefrom: pg02    # replicate from specific node
```

## Pause Mode

Disables auto-failover globally for maintenance (etcd maintenance, PG upgrade). Replica creation and manual switchover still possible.

## Other HA Solutions

| Solution | Key Feature |
|----------|-------------|
| pg_auto_failover | Simple automated failover, 3-node setup |
| repmgr | Replication management + failover, split-brain prevention |
| Stolon | K8s native, any partition resilient, etcd/consul |
| ClusterControl | Commercial, UI-based management, monitoring |
| Pgpool-II | Built-in replication, connection pooling, read LB |

## Kubernetes Operators

**Zalando PostgreSQL Operator:** Manages PostgreSQL clusters as K8s custom resources. Patroni-based. PgBouncer sidecar.

**Crunchy PGO:** Production-grade, pgBackRest integration, monitoring.

```yaml
apiVersion: acid.zalan.do/v1
kind: postgresql
metadata:
  name: myapp-db
spec:
  teamId: myteam
  numberOfInstances: 3
  postgresql:
    version: "15"
  volume:
    size: 50Gi
```

## Gotchas

- Automatic failover default TTL is 30s - during this window writes fail
- etcd requires odd number of nodes (3, 5) for consensus
- Config priority: ALTER SYSTEM SET > patroni.yml > postgresql.base.conf
- Patroni manages certain params (max_connections, wal_level, etc.) - cannot override locally
- keepalived provides VIP floating between HAProxy instances (eliminates proxy SPOF)
- Split-brain: different segments elect separate masters. DCS consensus prevents this.

## See Also

- [[replication-fundamentals]] - streaming replication setup
- [[connection-pooling]] - PgBouncer with Patroni
- [[backup-and-recovery]] - replica creation from backup
- [[postgresql-configuration-tuning]] - parameters managed by Patroni
