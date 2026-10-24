---
title: "Structure interne du stockage des bases de données"
category: concepts
tags: [sql-databases, storage, pages, heap, row-store, column-store, toast, io, disk]
level: 4
source_sha256: dd406d6a2f24242c6f4b97fa010998f2d1a4ec750021f8c7fb6ea2cc5dae3c18
translation: machine
translated_at: '2026-10-24'
---
# Structure interne du stockage des bases de données {#database-storage-internals}

Comprendre comment les bases de données stockent et récupèrent les données sur disque est fondamental pour l'optimisation des performances. Chaque requête se traduit finalement par des opérations d'E/S disque sur des pages.

## Architecture de stockage {#storage-architecture}

### Pages {#pages}
La plus petite unité d'E/S. Lire une ligne = lire la page entière. Toutes les lignes de cette page deviennent disponibles dans le buffer pool.

| SGBD | Taille de page |
|-------|-----------|
| PostgreSQL | 8 Ko |
| MySQL InnoDB | 16 Ko |
| SQL Server | 8 Ko |

Avec 1000 lignes à raison de 3 lignes par page, on obtient environ 334 pages. Un parcours complet de table lit les 334 pages.

### Heap {#heap}
Collection non ordonnée de pages où résident les données de la table. Les nouvelles lignes sont ajoutées à la fin (sans ordre intrinsèque). Un parcours séquentiel complet du heap lit chaque page, ce qui est coûteux pour les requêtes sélectives.

### Row_ID / Tuple_ID {#row_id-tuple_id}
Identifiant système interne de chaque ligne :
- **MySQL InnoDB :** row_id = clé primaire (index clusterisé)
- **PostgreSQL :** `ctid` = (numéro_de_page, décalage) pointant vers l'emplacement physique

### Opérations d'E/S {#io-operations}
Une E/S lit une ou plusieurs pages. Objectif : minimiser le nombre d'E/S. Certaines E/S sont servies par le cache du système d'exploitation (sans accès disque). L'E/S est la principale métrique de coût pour les performances des requêtes.

**SSD vs HDD :** les lectures aléatoires sur SSD prennent environ 0,1 ms contre environ 10 ms sur HDD (100 fois plus rapide). Les lectures séquentielles sur SSD ne sont qu'environ 4 fois plus rapides que les lectures aléatoires (contre 100 fois sur HDD). Cela modifie les stratégies d'optimisation : les E/S aléatoires coûtent moins cher sur SSD.

## Stockage par ligne vs par colonne {#row-vs-column-store}

**Orienté ligne (OLTP par défaut) :** la ligne entière est stockée ensemble, sur la même page.
- Adapté pour : `SELECT * FROM emp WHERE id = 1` (toutes les colonnes, une seule ligne)
- Inadapté pour : `SELECT SUM(salary) FROM emp` (lit toutes les colonnes pour accéder à une seule)
- Exemples : PostgreSQL, MySQL, Oracle, SQL Server

**Orienté colonne (OLAP / analytique) :** chaque colonne est stockée séparément.
- Adapté pour : `SUM(salary)` (ne lit que la colonne salary et ignore le reste)
- Inadapté pour : `SELECT * WHERE id = 1` (doit lire dans chaque fichier de colonne)
- Exemples : ClickHouse, Redshift, BigQuery, fichiers Parquet
- Meilleure compression (les données de même type se compressent bien)

## TOAST (PostgreSQL) {#toast-postgresql}

Le sigle désigne *The Oversized-Attribute Storage Technique*, c'est-à-dire la technique de stockage des attributs surdimensionnés. La version d'une ligne doit tenir dans une seule page de 8 Ko.

- Les grandes valeurs sont automatiquement compressées et/ou déplacées vers une table TOAST séparée
- La table TOAST possède son propre index
- Lue uniquement lorsqu'un attribut volumineux est accédé
- Les parties TOAST non modifiées ne sont pas dupliquées lors d'un UPDATE de la ligne
- `SELECT *` force la récupération et la décompression de toutes les colonnes TOAST

## Amplification d'écriture {#write-amplification}

Une seule écriture logique provoque plusieurs écritures physiques.

**PostgreSQL :** la mise à jour de n'importe quelle colonne réécrit le tuple entier (nouvelle version dans le heap). Tous les index pointant vers l'ancien tuple doivent créer de nouvelles entrées. Une mise à jour HOT (Heap-Only Tuple) évite la mise à jour des index si : (1) les colonnes modifiées ne sont pas indexées ET (2) le nouveau tuple tient sur la même page.

**MySQL InnoDB :** UPDATE modifie le tuple sur place (si cela tient sur la page). Les index secondaires ne sont mis à jour que si la colonne indexée change. L'amplification d'écriture est nettement plus faible pour les charges à forte proportion d'UPDATE.

**Migration d'Uber (2016) :** la motivation principale était l'amplification d'écriture de Postgres avec de nombreux index secondaires. Les mises à jour sur place de MySQL réduisaient les E/S d'écriture. Postgres a depuis été amélioré avec les mises à jour HOT.

## Faits essentiels {#key-facts}

- La taille de page détermine le facteur de branchement de l'arbre B+ : des pages plus grandes = plus de clés par nœud = arbre moins profond
- PostgreSQL stocke les verrous de ligne dans l'en-tête du tuple, et non en mémoire
- Les écritures complètes de pages (`full_page_writes = on`) préviennent le problème des pages partiellement écrites (torn page), mais doublent la taille du WAL
- Le cache de pages du système d'exploitation peut servir les lectures sans E/S disque ; `effective_cache_size` informe le planificateur à ce sujet
- `O_DIRECT` contourne le cache du système d'exploitation pour un cache géré par la base de données

## Détails sur le stockage disque {#disk-storage-details}

- Les données sont stockées dans des fichiers gérés par le système de fichiers (ext4, XFS, NTFS)
- Le SSD modifie les optimisations : `random_page_cost` devrait être compris entre 1,1 et 2,0 (contre 4,0 pour un HDD)
- NVMe : `effective_io_concurrency = 500-1000` ; SSD SATA : 200 ; HDD : nombre de disques (spindles)

## Pièges {#gotchas}

- `SELECT *` dégrade les performances en récupérant les colonnes TOAST et en empêchant les parcours index-only
- Ajouter des colonnes à une table dégrade silencieusement les requêtes `SELECT *` existantes
- E/S mappées en mémoire (mmap) vs E/S tamponnées : PostgreSQL utilise des E/S tamponnées via shared_buffers
- Le système d'exploitation peut mettre les écritures en cache en mémoire ; `fsync()` force l'écriture physique sur disque

## Voir aussi {#see-also}

- [[btree-and-index-internals]] - structures de données d'index et divisions de pages
- [[postgresql-mvcc-vacuum]] - tuples morts et récupération d'espace
- [[postgresql-wal-durability]] - journal d'écriture anticipée pour la reprise après incident
- [[query-optimization-explain]] - comprendre les coûts d'E/S dans les plans de requête
