---
title: "Zero-Copy et E/S disque"
category: concepts
tags: [kafka, zero-copy, sendfile, page-cache, sequential-io, performance]
level: 3
source_sha256: 88aae180d3b60f3350c6e41b2c22164c302bdbb2c5bbc96b700bfa5f84135a48
translation: machine
translated_at: '2026-10-24'
---
# Zero-Copy et E/S disque {#zero-copy-and-disk-io}

Kafka atteint un débit élevé grâce aux E/S disque séquentielles, à l'utilisation du cache de pages du système d'exploitation et au transfert zero-copy via `sendfile()`, ce qui fait que le CPU n'est presque jamais le goulot d'étranglement.

## Points clés {#key-facts}

- Kafka utilise l'appel système `sendfile()` (zero-copy) pour transférer les données du disque vers la socket réseau, en contournant les tampons de l'espace utilisateur
- Les données sur disque sont déjà au format exact du protocole réseau : aucune transformation CPU n'est nécessaire
- Les E/S disque séquentielles sont plus rapides que les accès mémoire aléatoires à grande échelle
- Le flux de données est : disque -> cache de pages du noyau -> NIC (carte réseau) via DMA, sans intervention du CPU
- Cascade typique de défaillances : le réseau tombe en premier, puis le disque, le CPU presque jamais
- Les réseaux de datacenter modernes en 10 Gbit/s peuvent gérer des dizaines de lecteurs indépendants par topic
- Les consommateurs multiples sont très peu coûteux, car les données sont servies depuis le cache de pages
- Le zero-copy ne fonctionne QUE lorsque SSL n'est PAS activé sur le listener du broker
- Les messages sont regroupés en lots et compressés au niveau du lot, stockés compressés sur disque, et décompressés par les consommateurs
- Les en-têtes de lot stockent le `CreateTime` le plus récent des messages qu'ils contiennent

## Patterns {#patterns}

### Fonctionnement du zero-copy {#how-zero-copy-works}

```php
Traditional (without zero-copy):
  Disk -> Kernel Buffer -> User Space Buffer -> Socket Buffer -> NIC
  (4 copies, 4 context switches)

Kafka (with zero-copy / sendfile):
  Disk -> Kernel Page Cache -> NIC (via DMA)
  (2 copies, 0 context switches, CPU uninvolved)
```

### Pourquoi Kafka est rapide {#why-kafka-is-fast}

```sql
1. Sequential I/O:
   - Append-only writes (no random seeks)
   - Sequential reads (consumers read in order)
   - HDD sequential: 200-300 MB/s vs random: 0.1-1 MB/s

2. Page Cache:
   - OS caches recently written/read data
   - Hot data served from memory without Kafka knowing
   - JVM heap stays clean (no GC pressure from data)

3. Batching:
   - Producer accumulates messages into batches
   - One batch = one disk write, one network send
   - 100 messages = 1 Kafka write

4. Compression:
   - Batch-level compression (lz4/zstd/snappy/gzip)
   - Stored compressed, transferred compressed
   - Consumer decompresses on read
```

### Structure des fichiers de segment {#segment-file-structure}

```text
/var/kafka/data/
  orders-0/                          # topic "orders", partition 0
    00000000000000000000.log         # segment file (records)
    00000000000000000000.index       # offset-to-position index
    00000000000000000000.timeindex   # timestamp-to-offset index
    00000000000000123456.log         # next segment (starts at offset 123456)
    leader-epoch-checkpoint
```

- `.log` - données de messages réelles (compressées par lot)
- `.index` - correspondance clairsemée entre offset et position en octets
- `.timeindex` - correspondance clairsemée entre horodatage et offset

## Pièges courants {#gotchas}

- **SSL désactive le zero-copy** - avec SSL activé, les données doivent être chiffrées dans l'espace utilisateur, ce qui ajoute une surcharge CPU et supprime l'optimisation `sendfile()`
- **Le GC de la JVM ne concerne PAS le chemin des données** - Kafka stocke les données dans le cache de pages (en dehors du tas de la JVM) ; la pression sur le GC provient de la gestion des connexions et des métadonnées, pas des données
- **Thrashing du cache de pages** - si le broker sert trop de partitions différentes qui ne tiennent pas en RAM, les évictions du cache provoquent des lectures disque ; surveillez le taux de succès du cache
- **Un segment reste ouvert longtemps avec des écrivains lents** - la durée de rétention réelle peut être bien plus longue que la valeur configurée, car la rétention ne s'applique qu'aux segments fermés

## Voir aussi {#see-also}

- [[broker-architecture]] - segments de journal, politiques de rétention, rotation des segments
- [[topics-and-partitions]] - disposition sur disque, configuration des segments
- [[kafka-producer-fundamentals]] - regroupement et compression au niveau du producteur
- [Kafka Design : Efficacité](https://kafka.apache.org/documentation/#maximizingefficiency)
