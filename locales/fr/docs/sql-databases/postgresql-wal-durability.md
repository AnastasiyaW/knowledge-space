---
title: "WAL et durabilité dans PostgreSQL"
category: concepts
tags: [sql-databases, postgresql, wal, write-ahead-log, durability, checkpoint, fsync, crash-recovery]
level: 3
source_sha256: 3f36bded270f4892db07d3b6d615ad6bcbe2aa477a11cf8685d89984720c9110
translation: machine
translated_at: '2026-10-24'
---
# WAL et durabilité dans PostgreSQL {#postgresql-wal-and-durability}

Le Write-Ahead Log (WAL) est le fondement de la récupération après panne et de la réplication dans PostgreSQL. Il garantit que les transactions validées survivent à toute défaillance en écrivant les modifications dans un journal séquentiel avant de modifier les pages de données.

## Fonctionnement du WAL {#how-wal-works}

1. La transaction modifie les données dans shared_buffers (mémoire)
2. L'enregistrement WAL est écrit dans les tampons WAL
3. Lors d'un COMMIT, le WAL est vidé sur disque (écriture séquentielle - rapide)
4. Les pages de données réelles sont écrites de manière différée par le background writer ou le checkpointer
5. En cas de crash : rejouer le WAL depuis le dernier checkpoint pour reconstruire l'état validé

Les segments WAL sont des fichiers de 16 Mo par défaut. Équivalent MySQL InnoDB : « redo log ».

## Paramètres clés {#key-parameters}

```sql
-- WAL detail level
wal_level = replica    -- minimal | replica | logical
-- 'minimal' = crash recovery only
-- 'replica' = streaming replication support
-- 'logical' = logical replication/decoding

-- Durability vs performance
synchronous_commit = on
-- 'on' (default): WAL flushed to disk on each commit (safest)
-- 'off': buffered, async flush. 3x faster, risk ~600ms of lost commits on crash
-- 'remote_apply': WAL applied on replica before confirming

-- Full page writes (torn page protection)
full_page_writes = on  -- write full page to WAL on first modification after checkpoint

-- WAL compression
wal_compression = on   -- reduces WAL size, slight CPU overhead
```

## Checkpoints {#checkpoints}

Checkpoint : processus en arrière-plan qui écrit sur disque toutes les pages sales et inscrit un enregistrement de checkpoint dans le WAL. Après un checkpoint, les anciens fichiers WAL peuvent être recyclés.

```sql
-- Checkpoint frequency controls
max_wal_size = '4GB'          -- trigger checkpoint when WAL reaches this size
checkpoint_timeout = '5min'    -- max time between checkpoints
checkpoint_completion_target = 0.9  -- spread I/O over 90% of interval
```

## Cache du système d'exploitation et fsync {#os-cache-and-fsync}

Le système d'exploitation met en cache les opérations d'écriture en mémoire (page cache). Une coupure de courant avant le vidage du cache entraîne une perte de données, même si la base de données a « écrit » les données.

- `fsync()` force l'écriture physique sur disque - coûteux
- Le cache d'écriture protégé par batterie (BBWC) des contrôleurs RAID rend fsync rapide
- `wal_sync_method = fdatasync` (valeur par défaut sous Linux) ou `open_datasync`

## Compromis durabilité / performance {#durability-vs-performance-trade-offs}

| Réglage | Comportement | Risque |
|---------|--------------|--------|
| `synchronous_commit = on` | WAL vidé à chaque validation | Aucun - durabilité complète |
| `synchronous_commit = off` | WAL bufferisé, vidage asynchrone | Perte des ~600 ms de validations les plus récentes |
| Validations groupées | Regrouper plusieurs validations en un seul fsync | Débit plus élevé, léger risque par transaction |
| Disque WAL dédié | Disque séparé pour les fichiers WAL | Amélioration des écritures de 2 à 30 fois |

## Le WAL pour la réplication {#wal-for-replication}

```sql
-- Required for streaming replication
wal_level = replica
max_wal_senders = 10
```

Les segments WAL sont diffusés vers les réplicas pour une réplication continue. L'archivage du WAL permet la PITR (Point-in-Time Recovery, récupération à un instant donné).

## Comparaison avec d'autres bases de données {#comparison-with-other-databases}

| Base de données | Mécanisme | Remarques |
|-----------------|-----------|-----------|
| PostgreSQL | WAL (segments de 16 Mo) | Journal séquentiel + écritures différées des données |
| MySQL InnoDB | Redo log | Similaire au WAL, journal circulaire de taille fixe |
| Redis | RDB + AOF (optionnel) | Conçu pour la mémoire, durabilité à activer explicitement |
| MongoDB | Journal (WiredTiger) | Checkpoint toutes les 60 s ou tous les 2 Go |
| Cassandra | Commit log + memtable | Équivalent du WAL + vidage en SSTable |

## Pièges à éviter {#gotchas}

- `synchronous_commit = off` risque de perdre seulement les ~600 ms de transactions validées les plus récentes, et NON de corrompre les données
- `full_page_writes = on` double à peu près la taille du WAL mais prévient la corruption de pages partiellement écrites
- Les échecs d'archivage du WAL rompent les chaînes de sauvegarde - surveillez le succès de `archive_command`
- Un `max_wal_size` élevé réduit la fréquence des checkpoints mais augmente le temps de récupération après un crash
- Les sommes de contrôle des données (`initdb -k` ou `pg_checksums`) détectent la corruption silencieuse mais ajoutent environ 1 à 2 % de surcharge en lecture

## Voir aussi {#see-also}

- [[transactions-and-acid]] - propriété de durabilité ACID
- [[backup-and-recovery]] - archivage WAL pour la PITR
- [[replication-fundamentals]] - réplication en flux basée sur le WAL
- [[postgresql-configuration-tuning]] - réglage des paramètres WAL
