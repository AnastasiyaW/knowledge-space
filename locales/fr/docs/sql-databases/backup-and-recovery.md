---
title: "Sauvegarde et restauration"
category: reference
tags: [sql-databases, postgresql, backup, pg-dump, pg-basebackup, pg-probackup, wal-g, pitr, point-in-time-recovery]
level: 3
source_sha256: af582d28fe5ae61281ad0b1050a09ceb3b03a558e111f0eb1c0e0da1ee391aa2
translation: machine
translated_at: '2026-10-24'
---
# Sauvegarde et restauration {#backup-and-recovery}

PostgreSQL propose plusieurs stratégies de sauvegarde, des dumps logiques à l'archivage continu des WAL. Le choix dépend de la taille de la base, des exigences en RPO/RTO et de la complexité opérationnelle acceptable.

## Comparaison des outils de sauvegarde {#backup-tools-comparison}

| Outil | Type | Incrémentale | Parallèle | Cloud-natif |
|-------|------|--------------|-----------|-------------|
| pg_dump | Logique | Non | Restauration uniquement | Non |
| pg_basebackup | Physique | Non | Non | Non |
| pg_probackup | Physique | Oui (FULL/PAGE/DELTA) | Oui | S3 via Ceph |
| WAL-G | Physique | Oui (delta) | Oui | S3/GCS/Azure |

## pg_dump / pg_dumpall {#pg_dump-pg_dumpall}

Sauvegarde logique : exporte les instructions SQL. Fonctionne entre les versions de PostgreSQL.

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

Sauvegarde physique : copie l'intégralité du répertoire de données. Sert de base à la réplication en flux.

```bash
pg_basebackup -h PRIMARY_IP -p 5432 -U repuser -R -D /path/to/data
# -R creates standby.signal + connection info
# --no-slot avoids replication slot creation
```

## pg_probackup {#pg_probackup}

Utilitaire de sauvegarde avancé : sauvegardes incrémentales, validation, opérations multi-threads.

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

**À grande échelle (1500+ instances) :** stratégie DELTA uniquement (pas de FULL périodique), `--no-validate` et `--no-sync` pendant la sauvegarde, fusion selon la rétention. Ratio incrémental d'environ 0,12 (12 % de la taille d'une sauvegarde complète).

## WAL-G {#wal-g}

Sauvegarde cloud-native avec prise en charge de S3/GCS/Azure.

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

Utilise l'archivage des WAL pour restaurer la base à n'importe quel instant.

```bash
# Enable WAL archiving (postgresql.conf)
archive_mode = on
archive_command = 'cp %p /archive/%f'

# Restore to specific time
recovery_target_time = '2024-06-15 14:30:00'
```

Chaque restauration crée une nouvelle timeline. `pg_rewind` resynchronise les réplicas divergents sans nouvelle copie complète.

## Optimisations avant chargement (Bulk Load) {#pre-loading-optimizations-bulk-load}

Avant de charger en masse de grands jeux de données :
1. Désactiver l'autocommit
2. Supprimer les index (les recréer après le chargement)
3. Supprimer les clés étrangères (les recréer après)
4. Augmenter `maintenance_work_mem`
5. Augmenter `max_wal_size`

## Sommes de contrôle des données {#data-checksums}

```bash
# Enable at initdb or via utility (requires shutdown)
pg_checksums --enable -D /var/lib/postgresql/15/main
```

Détecte la corruption silencieuse des données (bitrot). Surcoût d'environ 1 à 2 % en lecture. Validée pendant la sauvegarde (détecte la corruption de blocs). Vérification : `SHOW data_checksums;`

## Liste de contrôle pour la production {#production-backup-checklist}

- Effectuer les sauvegardes depuis un réplica (pour éviter l'impact sur les performances du primaire)
- Tester régulièrement les restaurations (tests de restauration automatisés)
- Surveiller le succès de `archive_command`
- Politique de rétention : 7 à 30 jours selon les exigences
- Séparer le stockage des sauvegardes du stockage de la base
- RPO (Recovery Point Objective) : perte de données acceptable
- RTO (Recovery Time Objective) : délai maximal de reprise après incident

## Pièges courants {#gotchas}

- pg_dump est logique : il ne conserve pas les optimisations physiques (ordre des tables, TOAST)
- pg_basebackup copie l'intégralité du répertoire de données : lent pour les grandes bases
- La perte de segments WAL rompt la chaîne de sauvegarde pour le PITR
- Les slots de réplication empêchent le nettoyage des WAL mais peuvent saturer le disque
- Le parallélisme de `pg_restore -j` ne fonctionne qu'avec le format personnalisé (`-Fc`)
- Timelines PostgreSQL : les fichiers WAL incluent l'identifiant de timeline ; ne pas rejouer un WAL issu d'une mauvaise branche de restauration

## Voir aussi {#see-also}

- [[postgresql-wal-durability]] - configuration de l'archivage des WAL
- [[replication-fundamentals]] - pg_basebackup pour la mise en place d'un réplica
- [[postgresql-ha-patroni]] - création de réplicas à partir d'une sauvegarde avec Patroni
- [[postgresql-data-loading]] - optimisation du chargement de données en masse
