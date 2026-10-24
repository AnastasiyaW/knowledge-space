---
title: "MySQL InnoDB et moteurs de stockage"
category: concepts
tags: [sql-databases, mysql, innodb, myisam, storage-engine, clustered-index, redo-log]
level: 3
source_sha256: 6302494354580e21ad689052eaf28c2dff0566bd0a62f2f7caead441a5d69b56
translation: machine
translated_at: '2026-10-24'
---
# MySQL InnoDB et moteurs de stockage {#mysql-innodb-and-storage-engines}

MySQL prend en charge des moteurs de stockage enfichables. InnoDB (par défaut depuis la 5.5) fournit des transactions ACID, un verrouillage au niveau des lignes et la récupération après incident. Comprendre les différences entre moteurs est indispensable pour administrer MySQL.

## Comparaison des moteurs de stockage {#storage-engine-comparison}

| Moteur | Transactions | Verrouillage | Récupération après incident | Remarques |
|--------|-------------|--------------|-----------------------------|-----------|
| **InnoDB** | Oui (ACID) | Au niveau des lignes | Redo log | Par défaut depuis la 5.5. MVCC, prise en charge des clés étrangères |
| **MyISAM** | Non | Au niveau de la table | REPAIR TABLE | Hérité. Lectures rapides, pas de récupération après incident |
| **MEMORY/HEAP** | Non | Au niveau de la table | N/A (RAM uniquement) | Données perdues au redémarrage. Tables temporaires |
| **Archive** | Non | Au niveau des lignes | N/A | INSERT + SELECT uniquement. Forte compression |

## Architecture d'InnoDB {#innodb-architecture}

- **Index clusterisé sur la PK :** les données sont physiquement triées selon la clé primaire. Chaque table en possède un.
- **Index secondaires :** les feuilles stockent la valeur de la PK (et non un pointeur vers la ligne). Une recherche nécessite un double saut : index secondaire -> recherche de la PK -> index clusterisé -> données de la ligne.
- **Redo log :** équivalent du WAL. Journal circulaire pour la récupération après incident.
- **Buffer pool :** cache en mémoire pour les pages de données et d'index.
- **MVCC :** lecture *read-committed* et *repeatable-read* grâce aux undo logs (gestion des versions de lignes).

### Comportement en écriture : InnoDB vs PostgreSQL {#innodb-vs-postgresql-write-behavior}

| Opération | InnoDB | PostgreSQL |
|-----------|--------|------------|
| UPDATE | Sur place si la ligne tient dans la page | Crée un nouveau tuple (copie complète de la ligne) |
| Index secondaire lors d'un UPDATE | Mis à jour uniquement si la colonne indexée change | Tous les index sont mis à jour (sauf HOT) |
| Verrouillage des lignes | En mémoire (gestionnaire de verrous) | Dans l'en-tête du tuple (champ xmax) |

InnoDB présente une amplification d'écriture nettement plus faible pour les charges dominées par les UPDATE, en présence de nombreux index secondaires.

## Types de verrous spécifiques à MySQL {#mysql-specific-lock-types}

- **Gap lock :** verrouille l'intervalle entre les enregistrements d'un index en REPEATABLE READ. Empêche les lectures fantômes.
- **Next-key lock :** combinaison d'un gap lock et d'un record lock. Mode par défaut pour RR dans InnoDB.
- **Insert intention lock :** permet des insertions concurrentes à des positions différentes au sein d'un même intervalle.
- **MDL (Metadata Lock) :** une opération DDL acquiert un MDL exclusif et attend que toutes les opérations DML soient terminées.
- **SX Lock (8.0.20+) :** verrou partagé-exclusif pour le DDL en ligne. Autorise les lectures ET les écritures concurrentes pendant certaines opérations ALTER TABLE.

## Moteurs à arbres LSM {#lsm-tree-engines}

**RocksDB (MyRocks) :** moteur à arbre LSM optimisé pour l'écriture, destiné à MySQL. Toutes les écritures sont séquentielles (ajout au WAL + memtable). Une compaction en arrière-plan fusionne les SSTables. Meilleur débit d'écriture que InnoDB pour les charges à forte proportion d'écritures. Utilisé par Facebook.

**B+Tree vs LSM-Tree :**
- B+Tree (InnoDB) : optimisé pour la lecture, mises à jour sur place, E/S aléatoires pour les écritures
- LSM-Tree (RocksDB) : optimisé pour l'écriture, écritures séquentielles, amplification de lecture due à la présence de plusieurs SSTables

## Points clés {#key-facts}

- InnoDB crée automatiquement un index clusterisé sur la PK. Sans PK explicite, il utilise le premier index UNIQUE NOT NULL ou un `row_id` caché de 6 octets
- `utf8` dans MySQL ne couvre que 3 octets (pas les emoji) : utilisez systématiquement `utf8mb4`
- `SERIAL` = `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`
- Guillemets inversés pour les identifiants : `` `table` ``, `` `column` ``
- `SHOW ENGINES;` liste les moteurs de stockage disponibles
- MyISAM n'est pas recommandé pour les nouvelles applications

## Supervision de MySQL {#mysql-monitoring}

```sql
SHOW DATABASES;
SHOW TABLES;
DESCRIBE table_name;
SHOW TABLE STATUS;              -- engine, rows, data/index size
SHOW ENGINE INNODB STATUS\G     -- detailed InnoDB metrics
SELECT VERSION();
```

## Pièges à éviter {#gotchas}

- UUID aléatoire comme PK InnoDB : pire cas, l'index clusterisé ET tous les index secondaires héritent de cette aléatoire
- Effet en cascade des MDL : ALTER TABLE attend un SELECT long, puis les nouveaux SELECT se mettent en file derrière l'ALTER
- L'isolation par défaut d'InnoDB est REPEATABLE READ (les gap locks peuvent provoquer des blocages inattendus)
- Coût des connexions : un thread par connexion. Utilisez ProxySQL ou un pool côté application pour monter en charge
- `TRUNCATE TABLE` réinitialise AUTO_INCREMENT dans MySQL (contrairement à PostgreSQL)
- `REPAIR TABLE` de MyISAM n'est pas automatique : des données peuvent être perdues sans intervention

## Voir aussi {#see-also}

- [[btree-and-index-internals]] - index clusterisés vs non clusterisés
- [[concurrency-and-locking]] - types de verrous InnoDB
- [[transactions-and-acid]] - niveaux d'isolation dans MySQL vs PostgreSQL
- [[connection-pooling]] - ProxySQL pour la gestion des connexions MySQL
