---
title: "Hadoop et HDFS"
category: tools
tags: [data-engineering, hadoop, hdfs, distributed-storage, big-data]
level: 4
source_sha256: 09548d32acaf410387f7bbee7e5e0f758b3329875c366ac623633336e92e9cd4
translation: machine
translated_at: '2026-10-24'
---
# Hadoop et HDFS {#hadoop-and-hdfs}

Hadoop est un framework de stockage et de traitement distribués de grands jeux de données. HDFS (Hadoop Distributed File System) fournit un stockage tolérant aux pannes sur du matériel standard.

## Architecture de Hadoop {#hadoop-architecture}

```bash
Application Layer: MapReduce | Spark | Tez | Hive | Pig
Resource Layer:    YARN (Resource Management)
Storage Layer:     HDFS (Distributed File System)
```

**Outils de l'écosystème :** Ambari (interface de gestion), ZooKeeper (coordination), Sqoop/Flume (ingestion), Oozie (ordonnancement), HBase (NoSQL), Mahout (ML).

## Architecture de HDFS {#hdfs-architecture}

```javascript
Client -> NameNode (Active) -- Standby NameNode (HA)
              |                 Secondary NameNode (checkpoints)
    +---------+---------+
    DN1     DN2     DN3     (DataNodes)
```

| Composant | Rôle |
|-----------|------|
| **NameNode** | Stocke les métadonnées : emplacements des fichiers, emplacements des blocs, permissions. Ne stocke PAS les données |
| **DataNode** | Stocke les blocs de données sur le disque local |
| **Secondary NameNode** | Fusionne les journaux d'édition avec le point de contrôle. N'est PAS un basculement (failover) |
| **Standby NameNode** | Basculement HA pour le NameNode actif |

**Critique :** si tous les NameNodes sont perdus, les données HDFS deviennent inaccessibles (métadonnées perdues).

## Stockage par blocs {#block-storage}

- Taille de bloc par défaut : **128 Mo** (configurable par fichier)
- Facteur de réplication par défaut : **3** (chaque bloc sur 3 DataNodes)
- Utilisation disque : un fichier de 2 Go avec une réplication de 3 = **6 Go** physiques
- **Conscience de rack (rack awareness) :** répliquer sur des racks différents pour la tolérance aux pannes

## Propriétés de HDFS {#hdfs-properties}

| Propriété | Détail |
|-----------|--------|
| Ajout seul (append-only) | Les fichiers ne peuvent pas être modifiés après écriture |
| Optimisé pour le débit | Au détriment de la latence |
| Non conforme POSIX | Sémantique différente du système de fichiers local |
| Configurable par fichier | Taille de bloc et facteur de réplication |

## Problème des petits fichiers {#small-files-problem}

10 M de fichiers totalisant 1 Go : chaque fichier = 1 bloc. Le NameNode stocke ~150 octets de métadonnées par bloc. 10 M × 150 octets = ~1,5 Go de métadonnées > données réelles.

**Solutions :** regrouper dans des fichiers plus volumineux (SequenceFiles, archives HAR).

## Commandes HDFS {#hdfs-commands}

```bash
hadoop fs -ls /path                # list files
hadoop fs -put local.txt /hdfs/    # upload
hadoop fs -get /hdfs/file.txt ./   # download
hadoop fs -cat /hdfs/file.txt      # view content
hadoop fs -text /hdfs/file.txt     # view (handles compression)
hadoop fs -mkdir /hdfs/dir         # create directory
hadoop fs -rm -r /hdfs/output/     # delete recursively
hdfs dfsadmin -report              # cluster health
hdfs fsck file -files -blocks -locations  # check blocks

# Custom block size and replication
hadoop fs -D dfs.blocksize=67108864 -D dfs.replication=2 -put file.txt /hdfs/
```

## Heartbeats des DataNodes {#datanode-heartbeats}
- Les DataNodes envoient périodiquement des heartbeats AU NameNode (et non l'inverse)
- L'absence de heartbeats déclenche une vérification par le NameNode, puis une re-réplication
- Un DataNode connaît ses blocs et leurs sommes de contrôle, mais PAS les fichiers auxquels ils appartiennent

## Principe de localité des données {#data-locality-principle}
Déplacer le calcul vers les données, et non les données vers le calcul. Évite le goulot d'étranglement réseau. C'est pourquoi les patterns fonctionnels (map, reduce, filter) dominent dans le big data.

## Big Data 5V {#big-data-5v}

| V | Signification |
|---|---------------|
| **Volume** | Taille des données (To, Po) |
| **Velocity** | Exigence de vitesse de traitement |
| **Value** | Importance pour l'activité |
| **Veracity** | Fiabilité des données |
| **Variety** | Diversité des types de données |

## Pièges à éviter {#gotchas}
- Splits HDFS != blocs HDFS : les splits sont logiques (MapReduce), les blocs sont physiques
- Les petits fichiers sont problématiques : surcharge mémoire du NameNode
- `hadoop distcp` pour la copie S3 vers HDFS (copie distribuée via MR)
- S3 est 5 à 10 fois moins cher que HDFS et pratiquement illimité

## Voir aussi {#see-also}
- [[mapreduce]] - paradigme de traitement
- [[yarn-resource-management]] - gestion des ressources du cluster
- [[apache-hive]] - SQL sur Hadoop
- [[hbase]] - NoSQL sur HDFS
- [[file-formats]] - Parquet, ORC, Avro
