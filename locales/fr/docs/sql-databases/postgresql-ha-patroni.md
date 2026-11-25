---
title: "PostgreSQL HA avec Patroni"
category: reference
tags: [sql-databases, postgresql, patroni, etcd, haproxy, high-availability, failover, switchover, ha-cluster]
level: 4
source_sha256: 48af499f0077c660611ac9534845ce8ca35c43d374f2dcaa537a3f0157caf173
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL HA avec Patroni {#postgresql-ha-with-patroni}

Patroni est un démon Python qui s'exécute aux côtés de PostgreSQL et gère la bascule automatique, l'élection du leader et la configuration du cluster via un magasin de configuration distribué (DCS).

## Architecture {#architecture}

Composants : 3 instances PostgreSQL ou plus + Patroni, 3 nœuds etcd ou plus (ou colocalisés), HAProxy/PgBouncer pour le routage.

Patroni fait le lien entre PostgreSQL et etcd : PostgreSQL ne peut pas interagir directement avec etcd. Depuis la v2.0, le protocole Raft natif est disponible (aucun etcd/consul externe n'est nécessaire).

## Configuration YAML de Patroni {#patroni-yaml-configuration}

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

## Paramètres clés {#key-parameters}

- `loop_wait` : nombre de secondes entre les tentatives de mise à jour de la clé du leader
- `retry_timeout` : intervalle de nouvelle tentative pour les mises à jour de clé
- `ttl` : durée de vie de la clé du leader. Recommandation : >= loop_wait + retry_timeout
- `maximum_lag_on_failover` : retard maximal (en octets) d'un réplica pour participer aux élections
- `synchronous_mode` : active le réplica synchrone
- `synchronous_mode_strict` : le primaire s'arrête si le réplica synchrone tombe

## Gestion du cluster (patronictl) {#cluster-management-patronictl}

```bash
patronictl -c /etc/patroni.yml list            # cluster status
patronictl -c /etc/patroni.yml edit-config      # edit DCS configuration
patronictl -c /etc/patroni.yml switchover       # planned manual role switch
patronictl -c /etc/patroni.yml failover         # forced failover
patronictl -c /etc/patroni.yml restart postgres pg02  # restart specific node
patronictl -c /etc/patroni.yml reinit postgres pg03   # wipe + pg_basebackup
patronictl -c /etc/patroni.yml pause|resume     # disable/enable auto-failover
```

## Configuration HAProxy {#haproxy-configuration}

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

## API REST pour la supervision {#rest-api-for-monitoring}

- `GET /master` : renvoie 200 uniquement pour le leader, 503 pour les autres
- `GET /replica` : renvoie 200 pour les réplicas
- `GET /patroni` : renvoie l'état, le statut de la réplication et la position WAL

## Tags de nœud {#node-tags}

```yaml
tags:
  nofailover: true       # never becomes master
  noloadbalance: true    # /replica always returns 503
  clonefrom: true        # preferred source for pg_basebackup
  nosync: true           # never becomes synchronous replica
  replicatefrom: pg02    # replicate from specific node
```

## Mode pause {#pause-mode}

Désactive globalement la bascule automatique pour la maintenance (maintenance d'etcd, mise à niveau de PG). La création de réplicas et la bascule manuelle (switchover) restent possibles.

## Autres solutions de haute disponibilité {#other-ha-solutions}

| Solution | Fonctionnalité clé |
|----------|-------------------|
| pg_auto_failover | Bascule automatique simple, configuration à 3 nœuds |
| repmgr | Gestion de la réplication + bascule, prévention du split-brain |
| Stolon | Natif K8s, résistant à tout partitionnement, etcd/consul |
| ClusterControl | Commercial, gestion par interface graphique, supervision |
| Pgpool-II | Réplication intégrée, pooling de connexions, répartition de charge en lecture |

## Opérateurs Kubernetes {#kubernetes-operators}

**Zalando PostgreSQL Operator :** gère les clusters PostgreSQL sous forme de ressources personnalisées K8s. Basé sur Patroni. Sidecar PgBouncer.

**Crunchy PGO :** qualité production, intégration pgBackRest, supervision.

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

## Pièges courants {#gotchas}

- Le TTL de bascule automatique par défaut est de 30 s : pendant cette fenêtre, les écritures échouent
- etcd exige un nombre impair de nœuds (3, 5) pour le consensus
- Priorité de configuration : ALTER SYSTEM SET > patroni.yml > postgresql.base.conf
- Patroni gère certains paramètres (max_connections, wal_level, etc.) : ils ne peuvent pas être surchargés localement
- keepalived fournit une VIP flottante entre les instances HAProxy (supprime le SPOF du proxy)
- Split-brain : des segments différents élisent des primaires distincts. Le consensus du DCS empêche ce cas.

## Voir aussi {#see-also}

- [[replication-fundamentals]] - mise en place de la réplication en streaming
- [[connection-pooling]] - PgBouncer avec Patroni
- [[backup-and-recovery]] - création de réplicas à partir d'une sauvegarde
- [[postgresql-configuration-tuning]] - paramètres gérés par Patroni
