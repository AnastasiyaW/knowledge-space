---
title: "Principes fondamentaux de la réplication"
category: concepts
tags: [sql-databases, replication, streaming-replication, logical-replication, synchronous, asynchronous, postgresql, read-replica]
level: 2
source_sha256: c6cef0ffc7132560bdd9f514061e0d3410a5c08afb115b4df146584c08ca07c5
translation: machine
translated_at: '2026-10-24'
---
# Principes fondamentaux de la réplication {#replication-fundamentals}

La réplication de base de données copie les données d'un primaire vers une ou plusieurs répliques, pour la montée en charge en lecture, la haute disponibilité et la distribution géographique. PostgreSQL prend en charge à la fois la réplication physique (streaming de WAL) et la réplication logique.

## Types de réplication {#replication-types}

| Type | Mécanisme | Périmètre | Cas d'usage |
|------|-----------|-------|----------|
| Physique (streaming) | Copie au niveau octet des WAL | Cluster entier | HA, répliques de lecture |
| Logique | Modifications au niveau des lignes | Tables/bases sélectionnées | Inter-versions, synchronisation sélective |
| Synchrone | Attente de l'ACK de la réplique | Configurable | Aucune perte de données |
| Asynchrone | Streaming sans attente | Par défaut | Latence plus faible, risque de perte de données |

## Mise en place de la réplication par streaming {#streaming-replication-setup}

### Configuration du primaire {#primary-configuration}
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

### Mise en place de la réplique {#replica-setup}
```bash
# Clone primary data
pg_basebackup -h PRIMARY_IP -p 5432 -U repuser -R -D /var/lib/postgresql/15/main
# -R creates standby.signal and writes connection info to postgresql.auto.conf

# Start replica - it auto-connects as streaming standby
systemctl start postgresql
```

### Surveillance de la réplication {#monitoring-replication}
```sql
-- On primary: connected replicas and lag
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
  pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replay_lag_bytes
FROM pg_stat_replication;

-- On replica: lag check
SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(),
  pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn()) AS lag_bytes;
```

## pg_rewind - Resynchronisation rapide d'une réplique {#pg_rewind-fast-replica-re-sync}

Lorsqu'une réplique diverge (par exemple après un split-brain), `pg_rewind` la resynchronise sans passer par un pg_basebackup complet :

```bash
pg_rewind --target-pgdata=/var/lib/postgresql/15/main \
          --source-server="host=primary port=5432 user=rewind_user"
```

Compare l'historique des WAL et ne copie que les blocs modifiés. Nécessite `wal_log_hints = on` ou les sommes de contrôle des données.

## Problèmes de retard de réplication {#replication-lag-issues}

- **Lectures obsolètes :** un utilisateur écrit des données, lit immédiatement depuis la réplique et obtient d'anciennes données
- **Solutions :** cohérence lecture-après-écriture (router les écritures récentes vers le primaire), cohérence causale, sessions persistantes (sticky sessions)

## Points clés {#key-facts}

- Les répliques peuvent servir des requêtes de lecture (hot standby) : diriger les lectures vers les répliques et les écritures vers le primaire
- Réplication synchrone : attendre l'ACK d'au moins une réplique. Cohérence plus forte, latence d'écriture plus élevée
- Semi-synchrone : attendre au moins une réplique (compromis entre cohérence et performance)
- `pg_promote()` ou `pg_ctl promote` pour promouvoir un standby en primaire
- Réplication en cascade : une réplique se réplique depuis une autre réplique (réduit la charge du primaire)
- Prendre les sauvegardes depuis une réplique pour éviter l'impact sur les performances du primaire

## Pièges {#gotchas}

- Réplication synchrone : si la réplique synchrone tombe, le débit d'écriture du primaire tombe à zéro jusqu'à expiration du délai
- La réplication logique ne réplique pas les modifications DDL : le schéma doit être géré séparément
- Les segments WAL du primaire doivent être conservés jusqu'à ce que toutes les répliques les aient consommés
- Les slots de réplication empêchent le nettoyage des WAL mais peuvent saturer le disque si une réplique se déconnecte pendant longtemps
- `max_wal_senders` limite le nombre de connexions de réplication simultanées

## Voir aussi {#see-also}

- [[postgresql-ha-patroni]] - bascule automatique avec Patroni
- [[postgresql-wal-durability]] - fonctionnement interne des WAL
- [[backup-and-recovery]] - archivage des WAL pour la PITR
- [[distributed-databases]] - alternatives de réplication multi-maîtres
