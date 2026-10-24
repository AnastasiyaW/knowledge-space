---
title: "PostgreSQL HA mit Patroni"
category: reference
tags: [sql-databases, postgresql, patroni, etcd, haproxy, high-availability, failover, switchover, ha-cluster]
level: 4
source_sha256: 48af499f0077c660611ac9534845ce8ca35c43d374f2dcaa537a3f0157caf173
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL HA mit Patroni {#postgresql-ha-with-patroni}

Patroni ist ein Python-Daemon, der neben PostgreSQL läuft und automatisches Failover, Leader-Wahl sowie die Cluster-Konfiguration über einen verteilten Konfigurationsspeicher (DCS) verwaltet.

## Architektur {#architecture}

Komponenten: 3+ PostgreSQL-Instanzen + Patroni, 3+ etcd-Knoten (oder gemeinsam auf denselben Hosts betrieben), HAProxy/PgBouncer für das Routing.

Patroni verbindet PostgreSQL und etcd, denn PostgreSQL kann nicht direkt mit etcd interagieren. Seit v2.0 steht zusätzlich das native Raft-Protokoll zur Verfügung (kein externes etcd/Consul erforderlich).

## Patroni-YAML-Konfiguration {#patroni-yaml-configuration}

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

## Wichtige Parameter {#key-parameters}

- `loop_wait`: Sekunden zwischen den Versuchen, den Leader-Schlüssel zu aktualisieren
- `retry_timeout`: Wiederholungsintervall für Schlüsselaktualisierungen
- `ttl`: Lebensdauer des Leader-Schlüssels. Empfehlung: >= loop_wait + retry_timeout
- `maximum_lag_on_failover`: maximaler Replikations-Lag (in Bytes), um an Wahlen teilnehmen zu dürfen
- `synchronous_mode`: aktiviert die synchrone Replik
- `synchronous_mode_strict`: der Primary stoppt, wenn die synchrone Replik ausfällt

## Cluster-Verwaltung (patronictl) {#cluster-management-patronictl}

```bash
patronictl -c /etc/patroni.yml list            # cluster status
patronictl -c /etc/patroni.yml edit-config      # edit DCS configuration
patronictl -c /etc/patroni.yml switchover       # planned manual role switch
patronictl -c /etc/patroni.yml failover         # forced failover
patronictl -c /etc/patroni.yml restart postgres pg02  # restart specific node
patronictl -c /etc/patroni.yml reinit postgres pg03   # wipe + pg_basebackup
patronictl -c /etc/patroni.yml pause|resume     # disable/enable auto-failover
```

## HAProxy-Konfiguration {#haproxy-configuration}

```text
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

## REST-API für Monitoring {#rest-api-for-monitoring}

- `GET /master`: liefert nur für den Leader 200, für alle anderen 503
- `GET /replica`: liefert 200 für Replicas
- `GET /patroni`: liefert Status, Replikationsstatus und WAL-Position

## Node-Tags {#node-tags}

```yaml
tags:
  nofailover: true       # never becomes master
  noloadbalance: true    # /replica always returns 503
  clonefrom: true        # preferred source for pg_basebackup
  nosync: true           # never becomes synchronous replica
  replicatefrom: pg02    # replicate from specific node
```

## Pause-Modus {#pause-mode}

Deaktiviert das automatische Failover clusterweit für Wartungsarbeiten (etcd-Wartung, PG-Upgrade). Das Erstellen von Replicas und ein manuelles Switchover sind weiterhin möglich.

## Weitere HA-Lösungen {#other-ha-solutions}

| Lösung | Hauptmerkmal |
|----------|-------------|
| pg_auto_failover | Einfaches automatisiertes Failover, Setup mit 3 Knoten |
| repmgr | Replikationsverwaltung + Failover, Verhinderung von Split-Brain |
| Stolon | K8s-nativ, resistent gegen beliebige Partitionierung, etcd/Consul |
| ClusterControl | Kommerziell, UI-basierte Verwaltung, Monitoring |
| Pgpool-II | Integrierte Replikation, Connection-Pooling, Read-Load-Balancing |

## Kubernetes-Operatoren {#kubernetes-operators}

**Zalando PostgreSQL Operator:** Verwaltet PostgreSQL-Cluster als K8s-Custom-Resources. Basiert auf Patroni. PgBouncer als Sidecar.

**Crunchy PGO:** Produktionsreif, Integration mit pgBackRest, Monitoring.

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

## Stolperfallen {#gotchas}

- Der Standard-TTL für automatisches Failover beträgt 30 s. In diesem Zeitfenster schlagen Schreibvorgänge fehl.
- etcd benötigt für den Konsens eine ungerade Anzahl von Knoten (3, 5).
- Priorität der Konfiguration: ALTER SYSTEM SET > patroni.yml > postgresql.base.conf
- Patroni verwaltet bestimmte Parameter (max_connections, wal_level usw.). Sie können lokal nicht überschrieben werden.
- keepalived stellt eine VIP bereit, die zwischen HAProxy-Instanzen wandert (beseitigt den Single Point of Failure beim Proxy).
- Split-Brain: Verschiedene Segmente wählen eigene Primaries. Der DCS-Konsens verhindert dies.

## Siehe auch {#see-also}

- [[replication-fundamentals]] - Einrichtung der Streaming-Replikation
- [[connection-pooling]] - PgBouncer mit Patroni
- [[backup-and-recovery]] - Erstellung von Replicas aus einem Backup
- [[postgresql-configuration-tuning]] - von Patroni verwaltete Parameter
