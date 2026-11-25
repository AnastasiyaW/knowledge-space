---
title: "Topics et partitions"
category: concepts
tags: [kafka, topics, partitions, keys, ordering, segments]
level: 5
source_sha256: 3cac388b22e48a9441a3ae868066c45d8b1fe4db5d78b8a230b2cce84345d0c8
translation: machine
translated_at: '2026-10-24'
---
# Topics et partitions {#topics-and-partitions}

Un **topic** est le canal logique de Kafka pour organiser les enregistrements. Physiquement, chaque topic est découpé en une ou plusieurs **partitions** -- des segments de journal ordonnés, en ajout seul (append-only), immuables, stockés sur les disques des brokers. Les partitions sont l'unité fondamentale de parallélisme, de stockage et de réplication dans Kafka. Chaque décision de conception d'un déploiement Kafka -- débit, garanties d'ordonnancement, mise à l'échelle des consommateurs, rétention des données -- dépend de la manière dont les topics et les partitions sont configurés.

## Concepts fondamentaux {#core-concepts}

### Topic comme canal logique {#topic-as-logical-channel}

Un topic est un flux nommé d'enregistrements. Les producteurs écrivent dans les topics ; les consommateurs les lisent. Les topics sont identifiés par leur nom et existent à l'échelle du cluster -- ils ne sont pas liés à un broker unique.

- Un topic peut avoir un nombre quelconque de producteurs et de consommateurs simultanément
- Plusieurs [[consumer-groups|groupes de consommateurs]] peuvent lire le même topic de façon indépendante, chacun suivant ses propres offsets
- Les topics sont créés explicitement (`kafka-topics.sh --create`) ou automatiquement lorsqu'un producteur y écrit pour la première fois (si `auto.create.topics.enable=true` sur le broker)
- Les noms de topics acceptent `[a-zA-Z0-9._-]`, avec un maximum de 249 caractères. Évitez `.` et `_` dans un même cluster -- Kafka utilise les deux comme séparateurs internes dans les noms de métriques

### Partition comme unité de parallélisme {#partition-as-unit-of-parallelism}

Chaque partition est un journal indépendant et ordonné. Le parallélisme dans Kafka croît avec le nombre de partitions :

```yaml
Topic: user-events (4 partitions)

Partition 0:  [msg0] [msg1] [msg2] [msg3] ...
Partition 1:  [msg0] [msg1] [msg2] ...
Partition 2:  [msg0] [msg1] [msg2] [msg3] [msg4] ...
Partition 3:  [msg0] [msg1] ...
```

- Chaque partition a sa propre séquence d'offsets, commençant à 0
- Un [[consumer-groups|groupe de consommateurs]] peut compter au plus un consommateur par partition -- le nombre de partitions constitue donc la borne supérieure du parallélisme des consommateurs
- Chaque partition possède un réplica **leader** (qui gère toutes les lectures et écritures) et zéro ou plusieurs réplicas **followers** (réplication passive)
- Les partitions sont réparties entre les brokers du cluster -- voir [[broker-architecture]]

### Garanties d'ordonnancement des messages {#message-ordering-guarantees}

**Kafka ne garantit l'ordre qu'au sein d'une même partition.** Il n'existe aucun ordre global entre les partitions.

```yaml
Partition 0:  A -> B -> C        (order guaranteed: A before B before C)
Partition 1:  D -> E -> F        (order guaranteed: D before E before F)

Cross-partition: no guarantee on relative order of A vs D
```

Si vous avez besoin d'un ordre strict pour un ensemble d'enregistrements liés (par exemple, tous les événements d'un même utilisateur), vous devez les router vers la même partition à l'aide d'une clé cohérente.

Avec `max.in.flight.requests.per.connection > 1` (valeur par défaut : 5), une livraison désordonnée est possible même au sein d'une partition si des tentatives de réémission ont lieu. Pour garantir l'ordre par partition avec des réémissions :
- Utilisez un producteur idempotent (`enable.idempotence=true`, activé par défaut depuis Kafka 3.0) -- cela gère le réordonnancement en interne
- Ou définissez `max.in.flight.requests.per.connection=1` (réduit le débit)

Voir [[kafka-producer-fundamentals]] pour la configuration du producteur idempotent et transactionnel.

### Partitionnement par clé {#key-based-partitioning}

Le producteur détermine la partition cible de chaque enregistrement :

**1. Messages avec clé (DefaultPartitioner)** :

```python
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

# All records with key="user-42" go to the same partition
# Partition = murmur2(key_bytes) % num_partitions
producer.produce("user-events", key="user-42", value="login")
producer.produce("user-events", key="user-42", value="purchase")  # Same partition
producer.flush()
```

Le partitionneur par défaut applique un hachage `murmur2` aux octets sérialisés de la clé, puis prend le modulo du nombre de partitions. Ce mécanisme est déterministe : une même clé correspond toujours à la même partition (tant que le nombre de partitions ne change pas).

**2. Clés nulles = round-robin / sticky** :

```python
# No key -> round-robin distribution (pre-2.4) or sticky partitioner (2.4+)
producer.produce("metrics", value="cpu=80%")
producer.produce("metrics", value="mem=60%")  # May go to a different partition
```

Depuis Kafka 2.4, le **sticky partitioner** est le comportement par défaut pour les enregistrements à clé nulle : le producteur reste attaché à une partition jusqu'à ce que le lot courant soit plein ou que `linger.ms` expire, puis change de partition. Cela améliore l'efficacité du regroupement par rapport à un round-robin pur.

**3. Partitionneur personnalisé** :

```python
from confluent_kafka import Producer

def region_partitioner(key, partitions, _):
    """Route by region prefix in key: 'us-east:user-42' -> hash only region."""
    if key is None:
        return None  # Fall back to default
    region = key.split(b":")[0]
    return hash(region) % len(partitions)

# confluent-kafka doesn't directly support custom partitioner callbacks
# in Python -- use the Java client or implement key prefixing with
# default partitioner. For Python, a common workaround:
# encode routing info into the key itself.
```

En Java :

```java
public class RegionPartitioner implements Partitioner {
    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        int numPartitions = partitions.size();
        if (keyBytes == null) return ThreadLocalRandom.current().nextInt(numPartitions);
        String region = new String(keyBytes).split(":")[0];
        return Utils.toPositive(Utils.murmur2(region.getBytes())) % numPartitions;
    }
}
```

### Stockage des partitions : segments {#partition-storage-segments}

Chaque partition est stockée sous forme de répertoire dans le répertoire de journaux du broker. À l'intérieur, les données sont découpées en **segments** :

```php
/kafka-logs/user-events-0/
    00000000000000000000.log        # Segment file (records)
    00000000000000000000.index      # Offset -> file position index
    00000000000000000000.timeindex  # Timestamp -> offset index
    00000000000000523417.log        # Next segment (starts at offset 523417)
    00000000000000523417.index
    00000000000000523417.timeindex
    leader-epoch-checkpoint
    partition.metadata
```

- Le **segment actif** est celui dans lequel on écrit actuellement
- La rotation des segments intervient lorsque `segment.bytes` (valeur par défaut : 1 Go) est atteint ou lorsque `segment.ms` (valeur par défaut : 7 jours) est écoulé
- Seuls les **segments fermés (inactifs)** sont éligibles à la suppression ou à la compaction
- Des segments plus petits signifient un nettoyage plus fréquent mais davantage de descripteurs de fichiers ; des segments plus grands signifient un nettoyage retardé

### Réaffectation des partitions {#partition-reassignment}

Les partitions peuvent être déplacées entre brokers pour équilibrer la charge ou lors du retrait d'un broker.

**Générer un plan de réaffectation** :
```bash
# Create a JSON file listing topics to reassign
cat > topics.json << 'EOF'
{"topics": [{"topic": "user-events"}], "version": 1}
EOF

# Generate a reassignment plan (move to brokers 1, 2, 3)
kafka-reassign-partitions.sh --generate \
  --topics-to-move-json-file topics.json \
  --broker-list "1,2,3" \
  --bootstrap-server localhost:9092
```

**Exécuter la réaffectation** :
```bash
# Save the generated plan to reassignment.json, then execute
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file reassignment.json \
  --bootstrap-server localhost:9092

# Monitor progress
kafka-reassign-partitions.sh --verify \
  --reassignment-json-file reassignment.json \
  --bootstrap-server localhost:9092
```

**Limiter le débit de réaffectation** pour borner la bande passante de réplication :
```bash
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file reassignment.json \
  --throttle 50000000 \
  --bootstrap-server localhost:9092
# 50 MB/s throttle -- prevents reassignment from saturating network
```

### Élection du leader préféré {#preferred-leader-election}

Chaque partition possède un **leader préféré** -- le premier broker de la liste des réplicas. Au fil du temps, les leaders peuvent changer (redémarrages de brokers, pannes). Pour rééquilibrer le leadership :

```bash
# Trigger preferred leader election for all partitions
kafka-leader-election.sh --election-type PREFERRED --all-topic-partitions \
  --bootstrap-server localhost:9092

# For a specific topic
kafka-leader-election.sh --election-type PREFERRED \
  --topic user-events \
  --bootstrap-server localhost:9092

# Unclean leader election (risk of data loss -- only for non-critical topics)
kafka-leader-election.sh --election-type UNCLEAN \
  --topic user-events --partition 0 \
  --bootstrap-server localhost:9092
```

`auto.leader.rebalance.enable=true` (valeur par défaut) déclenche une élection automatique du leader préféré lorsque le déséquilibre des leaders dépasse `leader.imbalance.percentage.per.broker` (valeur par défaut : 10 %).

## Configuration des topics {#topic-configuration}

### cleanup.policy {#cleanuppolicy}

Contrôle la manière dont les données anciennes sont supprimées d'un topic.

| Politique | Comportement | Cas d'usage |
|--------|----------|----------|
| `delete` (par défaut) | Supprime les segments plus anciens que `retention.ms` ou dépassant `retention.bytes` | Flux d'événements, journaux, métriques |
| `compact` | Ne conserve que la dernière valeur par clé ; un tombstone (valeur nulle) supprime la clé | Snapshots d'état, changelogs, caches |
| `compact,delete` | Compacte d'abord, puis supprime les segments plus anciens que la rétention | Topics compactés avec un plafond de rétention |

**Fonctionnement interne de la compaction** :
- Le thread de nettoyage du log parcourt les segments « sales » (non compactés)
- Pour chaque clé, seul l'enregistrement d'offset le plus élevé survit
- Un **tombstone** (clé avec valeur nulle) marque une clé pour suppression ; il est retiré après `delete.retention.ms` (valeur par défaut : 24 h)
- `min.compaction.lag.ms` -- délai minimal avant qu'un enregistrement devienne éligible à la compaction (évite de compacter des enregistrements que les consommateurs n'ont pas encore traités)
- `max.compaction.lag.ms` -- délai maximal avant que la compaction soit garantie de s'exécuter
- `min.cleanable.dirty.ratio` (valeur par défaut : 0.5) -- la compaction démarre lorsque 50 % ou plus du log est sale

```bash
# Create a compacted topic
kafka-topics.sh --create --topic user-profiles \
  --partitions 6 --replication-factor 3 \
  --config cleanup.policy=compact \
  --config min.compaction.lag.ms=3600000 \
  --config delete.retention.ms=86400000 \
  --bootstrap-server localhost:9092
```

### Configuration de la rétention {#retention-configuration}

| Paramètre | Valeur par défaut | Description |
|-----------|---------|-------------|
| `retention.ms` | 604800000 (7 jours) | Rétention basée sur le temps ; `-1` = infinie |
| `retention.bytes` | -1 (illimitée) | Rétention basée sur la taille, par partition |
| `segment.bytes` | 1073741824 (1 Go) | Taille maximale d'un fichier segment |
| `segment.ms` | 604800000 (7 jours) | Durée maximale avant la rotation du segment actif |
| `min.compaction.lag.ms` | 0 | Délai minimal avant qu'un enregistrement soit compactable |
| `max.compaction.lag.ms` | 9223372036854775807 | Délai maximal avant l'exécution de la compaction |
| `delete.retention.ms` | 86400000 (24 h) | Durée de conservation des tombstones après compaction |
| `message.timestamp.type` | `CreateTime` | `CreateTime` (défini par le producteur) ou `LogAppendTime` (défini par le broker) |

La rétention est évaluée par segment, et non par enregistrement. Un segment est supprimé lorsque **tous** les enregistrements qu'il contient dépassent le seuil de rétention.

## Modèles pratiques {#practical-patterns}

### Commandes kafka-topics.sh {#kafka-topicssh-commands}

**Créer un topic** :
```bash
kafka-topics.sh --create --topic orders \
  --partitions 12 --replication-factor 3 \
  --config retention.ms=259200000 \
  --config cleanup.policy=delete \
  --bootstrap-server kafka1:9092
```

**Décrire un topic** (partitions, réplicas, ISR, configurations) :
```bash
kafka-topics.sh --describe --topic orders \
  --bootstrap-server kafka1:9092

# Output:
# Topic: orders  PartitionCount: 12  ReplicationFactor: 3  Configs: retention.ms=259200000
#   Topic: orders  Partition: 0  Leader: 1  Replicas: 1,2,3  Isr: 1,2,3
#   Topic: orders  Partition: 1  Leader: 2  Replicas: 2,3,1  Isr: 2,3,1
#   ...
```

**Lister tous les topics** :
```bash
kafka-topics.sh --list --bootstrap-server kafka1:9092

# Exclude internal topics
kafka-topics.sh --list --exclude-internal --bootstrap-server kafka1:9092
```

**Modifier le nombre de partitions** (augmentation uniquement) :
```bash
kafka-topics.sh --alter --topic orders --partitions 24 \
  --bootstrap-server kafka1:9092
# WARNING: breaks key-based partition assignment for existing keys
```

**Modifier les configurations d'un topic** :
```bash
# Using kafka-configs.sh (preferred for config changes)
kafka-configs.sh --alter --entity-type topics --entity-name orders \
  --add-config retention.ms=86400000,segment.bytes=536870912 \
  --bootstrap-server kafka1:9092

# Remove a config override (revert to broker default)
kafka-configs.sh --alter --entity-type topics --entity-name orders \
  --delete-config retention.ms \
  --bootstrap-server kafka1:9092

# Describe current configs
kafka-configs.sh --describe --entity-type topics --entity-name orders \
  --bootstrap-server kafka1:9092
```

**Supprimer un topic** :
```bash
kafka-topics.sh --delete --topic orders \
  --bootstrap-server kafka1:9092
# Requires delete.topic.enable=true on broker (default: true since Kafka 1.0)
# Deletion is asynchronous -- data is removed in the background
```

### Gestion programmatique des topics (Python) {#programmatic-topic-management-python}

```python
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource

admin = AdminClient({"bootstrap.servers": "localhost:9092"})

# Create topic
topic = NewTopic(
    "user-events",
    num_partitions=12,
    replication_factor=3,
    config={
        "cleanup.policy": "compact,delete",
        "retention.ms": "604800000",
        "min.compaction.lag.ms": "3600000",
        "segment.bytes": "536870912",
    },
)
futures = admin.create_topics([topic])
for topic_name, future in futures.items():
    try:
        future.result()  # Block until complete
        print(f"Created topic: {topic_name}")
    except Exception as e:
        print(f"Failed to create {topic_name}: {e}")

# Describe topic config
resource = ConfigResource("TOPIC", "user-events")
futures = admin.describe_configs([resource])
for res, future in futures.items():
    configs = future.result()
    for key, config in configs.items():
        print(f"  {key} = {config.value}")

# List topics
metadata = admin.list_topics(timeout=10)
for topic_name in metadata.topics:
    print(f"Topic: {topic_name}, Partitions: {len(metadata.topics[topic_name].partitions)}")
```

### Heuristique de choix du nombre de partitions {#partition-count-selection-heuristic}

```yaml
Target throughput:    100 MB/s
Per-partition write:  ~10 MB/s (single partition, single producer)
Consumer instances:   8 (in one consumer group)

Minimum partitions = max(100/10, 8) = 10
Recommended:         12 (round up, leave room for growth)
```

Commencez avec un nombre réduit de partitions et augmentez-le ensuite. Vous ne pouvez pas diminuer le nombre de partitions sans recréer le topic.

## Pièges courants {#gotchas}

- **Augmenter le nombre de partitions casse l'affinité des clés.** `murmur2(key) % 12` != `murmur2(key) % 24`. Après une augmentation du nombre de partitions, des enregistrements ayant la même clé peuvent atterrir dans des partitions différentes. Si l'ordre compte, planifiez le nombre de partitions dès le départ ou utilisez un partitionneur personnalisé qui gère cette croissance.
- **Le nombre de partitions ne peut pas être diminué.** La seule façon de le réduire consiste à créer un nouveau topic avec moins de partitions et à migrer les données à l'aide de MirrorMaker, de Kafka Connect ou d'un pont consommateur-producteur.
- **La compaction exige des clés non nulles.** Si `cleanup.policy=compact`, chaque enregistrement doit avoir une clé. Les enregistrements à clé nulle entraîneront le contournement complet de ces enregistrements par la compaction.
- **Le segment actif n'est jamais supprimé ni compacté.** La rétention et la compaction ne s'appliquent qu'aux segments fermés. Si `segment.bytes=1GB` et que vous produisez 500 Mo/jour, le segment actif ne sera pas renouvelé avant environ 2 jours, ce qui retarde le nettoyage.
- **La suppression d'un topic est asynchrone et peut laisser des traces.** Après `--delete`, les partitions sont marquées pour suppression, mais la suppression effective des données s'effectue en arrière-plan. Le nom du topic devient immédiatement indisponible, mais l'espace disque n'est récupéré que plus tard.
- **`retention.bytes` s'applique par partition, et non par topic.** Un topic de 12 partitions avec `retention.bytes=1GB` peut conserver jusqu'à 12 Go au total.
- **L'élection de leader non propre risque une perte de données.** Si `unclean.leader.election.enable=true` (valeur par défaut : false depuis Kafka 0.11), un réplica désynchronisé peut devenir leader, ce qui fait perdre les messages non répliqués.
- **Les jointures entre partitions nécessitent un co-partitionnement.** Si vous devez joindre deux topics par clé, ils doivent avoir le même nombre de partitions et utiliser le même partitionneur. Voir [[consumer-groups]] pour les exigences de `RangeAssignor`.

## Référence rapide {#quick-reference}

### Configuration essentielle au niveau du topic {#key-topic-level-configuration}

| Paramètre | Valeur par défaut | Description |
|-----------|---------|-------------|
| `cleanup.policy` | `delete` | `delete`, `compact` ou `compact,delete` |
| `retention.ms` | 604800000 (7j) | Rétention basée sur le temps |
| `retention.bytes` | -1 | Rétention basée sur la taille, par partition |
| `segment.bytes` | 1073741824 (1GB) | Taille du fichier segment |
| `segment.ms` | 604800000 (7j) | Âge maximal du segment actif |
| `min.compaction.lag.ms` | 0 | Délai minimal avant l'éligibilité à la compaction |
| `max.compaction.lag.ms` | MAX_LONG | Délai maximal avant une compaction forcée |
| `delete.retention.ms` | 86400000 (24h) | Durée de vie des tombstones après compaction |
| `min.cleanable.dirty.ratio` | 0.5 | Ratio de log sale déclenchant la compaction |
| `max.message.bytes` | 1048588 (~1MB) | Taille maximale d'un enregistrement pour ce topic |
| `min.insync.replicas` | 1 | Nombre d'ISR requis pour `acks=all` |
| `unclean.leader.election.enable` | false | Autorise un réplica désynchronisé à devenir leader |
| `message.timestamp.type` | `CreateTime` | `CreateTime` ou `LogAppendTime` |

### Commandes CLI essentielles {#essential-cli-commands}

```bash
# Create
kafka-topics.sh --create --topic T --partitions N --replication-factor R \
  --bootstrap-server HOST:9092

# Describe
kafka-topics.sh --describe --topic T --bootstrap-server HOST:9092

# List
kafka-topics.sh --list --bootstrap-server HOST:9092

# Alter partitions (increase only)
kafka-topics.sh --alter --topic T --partitions N --bootstrap-server HOST:9092

# Alter configs
kafka-configs.sh --alter --entity-type topics --entity-name T \
  --add-config KEY=VALUE --bootstrap-server HOST:9092

# Delete
kafka-topics.sh --delete --topic T --bootstrap-server HOST:9092

# Preferred leader election
kafka-leader-election.sh --election-type PREFERRED --all-topic-partitions \
  --bootstrap-server HOST:9092

# Reassign partitions
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file plan.json --bootstrap-server HOST:9092
```

## Documentation officielle {#official-documentation}

- [Topics and Logs](https://kafka.apache.org/documentation/#intro_topics) - modèle topic/partition de base
- [Topic-Level Configs](https://kafka.apache.org/documentation/#topicconfigs) - référence complète de la configuration
- [Log Compaction](https://kafka.apache.org/documentation/#compaction) - sémantique et garanties de la compaction
- [Operations: Adding/Removing Topics](https://kafka.apache.org/documentation/#basic_ops_add_topic) - gestion en CLI
- [Partition Reassignment](https://kafka.apache.org/documentation/#basic_ops_partitionassignment) - rééquilibrage des partitions entre brokers

## Voir aussi {#see-also}

- [[broker-architecture]] - répartition des partitions sur les brokers, ISR, élection du contrôleur
- [[consumer-groups]] - stratégies d'attribution des partitions, rééquilibrage, gestion des offsets
- [[kafka-producer-fundamentals]] - sérialisation des clés, regroupement par lots, acks
- [[kafka-producer-advanced-patterns]] - producteur idempotent, partitionneurs personnalisés
- [[kafka-cluster-management]] - gestion quotidienne des topics et du cluster
