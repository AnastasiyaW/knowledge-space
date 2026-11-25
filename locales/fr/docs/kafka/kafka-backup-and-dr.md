---
level: 4
source_sha256: 58a6ebde2d41cbe66a9b6f55d3ceaf26c462a1e22d715acdee7bbadf14463ba0
translation: machine
translated_at: '2026-10-24'
---
# Sauvegarde Kafka et reprise après sinistre {#kafka-backup-and-disaster-recovery}

MirrorMaker 2 pour la réplication multi-datacenter, stratégies de sauvegarde (au niveau des topics, du système de fichiers, des métadonnées) et schémas de reprise après sinistre (actif-passif, actif-actif, stretch cluster, tiered storage).

## MirrorMaker 2 - Réplication multi-DC {#mirrormaker-2-multi-dc-replication}

MM2 est construit sur Kafka Connect. Il prend en charge les topologies actif-actif, actif-passif et en éventail (fan-out).

### Configuration {#configuration}

```properties
# mm2.properties
clusters = dc-east, dc-west
dc-east.bootstrap.servers = east-broker1:9092,east-broker2:9092,east-broker3:9092
dc-west.bootstrap.servers = west-broker1:9092,west-broker2:9092,west-broker3:9092

# Replicate east -> west
dc-east->dc-west.enabled = true
dc-east->dc-west.topics = orders, events, users
# Or regex: dc-east->dc-west.topics = .*

# Replicate west -> east (active-active)
dc-west->dc-east.enabled = true
dc-west->dc-east.topics = orders, events, users

# Prevent infinite replication loops
# MM2 prefixes remote topics: "dc-east.orders" on dc-west cluster
dc-west->dc-east.topics.exclude = dc-east\..*
dc-east->dc-west.topics.exclude = dc-west\..*

# Offset sync (consumers can failover with correct offsets)
emit.checkpoints.enabled = true
emit.checkpoints.interval.seconds = 60
sync.group.offsets.enabled = true
sync.group.offsets.interval.seconds = 60

# Replication tuning
replication.factor = 3
tasks.max = 4
offset-syncs.topic.replication.factor = 3
heartbeats.topic.replication.factor = 3
checkpoints.topic.replication.factor = 3
```

### Lancement {#launch}

```bash
# Standalone mode
bin/connect-mirror-maker.sh config/mm2.properties

# Distributed mode (via Kafka Connect cluster)
curl -X POST http://connect:8083/connectors -H "Content-Type: application/json" -d '{
  "name": "mm2-dc-east-to-dc-west",
  "config": {
    "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "source.cluster.alias": "dc-east",
    "target.cluster.alias": "dc-west",
    "source.cluster.bootstrap.servers": "east-broker1:9092",
    "target.cluster.bootstrap.servers": "west-broker1:9092",
    "topics": "orders,events,users",
    "replication.factor": "3",
    "tasks.max": "4"
  }
}'
```

### Bascule des consommateurs avec traduction des offsets {#consumer-failover-with-offset-translation}

```bash
# On dc-west, after dc-east failure:
# MM2 checkpoints store translated offsets in dc-west's
# "dc-east.checkpoints.internal" topic

kafka-console-consumer.sh --topic dc-east.checkpoints.internal \
  --from-beginning --bootstrap-server west-broker1:9092 \
  --property print.key=true | head

# Automated offset translation for consumer group failover:
kafka-consumer-groups.sh --bootstrap-server west-broker1:9092 \
  --group my-app --reset-offsets --to-latest \
  --topic dc-east.orders --execute
```

### Supervision de MM2 {#mm2-monitoring}

Métriques clés (via JMX sur les workers Connect) :
- `kafka.connect.mirror:type=MirrorSourceConnector,target=*,topic=*,partition=*` - `record-count`, `byte-rate`, `replication-latency-ms`
- Alerter sur `replication-latency-ms-avg > 5000` (retard de réplication de 5 s)

## Stratégies de sauvegarde {#backup-strategies}

Kafka n'est pas une base de données, mais des scénarios de perte de données existent.

### 1. Sauvegarde au niveau des topics avec kafka-consumer {#1-topic-level-backup-with-kafka-consumer}

```bash
# Dump topic to file (for smaller topics / config topics)
kafka-console-consumer.sh --bootstrap-server broker1:9092 \
  --topic __consumer_offsets --from-beginning \
  --timeout-ms 30000 \
  --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" \
  > consumer_offsets_backup_$(date +%Y%m%d).txt
```

### 2. Sauvegarde au niveau du système de fichiers {#2-filesystem-level-backup}

```bash
# Stop broker, snapshot log.dirs
sudo systemctl stop kafka

# Rsync partition data (preserves segment files, indexes, snapshots)
rsync -avz --progress /data/kafka-logs/ backup-server:/backup/kafka/broker1/

sudo systemctl start kafka
```

Pour une sauvegarde en ligne : créer un snapshot du système de fichiers sous-jacent (LVM, ZFS ou snapshots EBS dans le cloud).

```bash
# LVM snapshot (online, consistent if broker is not leader for partitions)
lvcreate -L 50G -s -n kafka-snap /dev/vg0/kafka-data
mount /dev/vg0/kafka-snap /mnt/kafka-snap
rsync -avz /mnt/kafka-snap/ backup-server:/backup/kafka/broker1/
umount /mnt/kafka-snap
lvremove -f /dev/vg0/kafka-snap
```

### 3. Réplication inter-clusters (à privilégier) {#3-cross-cluster-replication-preferred}

MirrorMaker 2 vers un cluster de secours est la « sauvegarde » recommandée pour les données de production. Il gère la traduction des offsets, les configurations des topics et les ACL.

### 4. Sauvegarde des métadonnées {#4-metadata-backup}

```bash
# Export topic configs
kafka-topics.sh --describe --bootstrap-server broker1:9092 | \
  tee topics_describe_$(date +%Y%m%d).txt

# Export all topic configurations
for topic in $(kafka-topics.sh --list --bootstrap-server broker1:9092); do
  echo "=== $topic ==="
  kafka-configs.sh --describe --all --topic "$topic" --bootstrap-server broker1:9092
done > topic_configs_$(date +%Y%m%d).txt

# Export consumer group offsets
kafka-consumer-groups.sh --bootstrap-server broker1:9092 --all-groups --describe \
  > consumer_groups_$(date +%Y%m%d).txt

# Export ACLs
kafka-acls.sh --bootstrap-server broker1:9092 --list \
  > acls_$(date +%Y%m%d).txt

# KRaft metadata snapshot (already in log.dirs/__cluster_metadata-0/)
# Automatically maintained by controller quorum
```

## Schémas de reprise après sinistre {#disaster-recovery-patterns}

### Schéma 1 : Actif-passif avec MM2 {#pattern-1-active-passive-with-mm2}

```text
DC-East (Primary)  ----MM2---->  DC-West (Standby)
   producers                       idle consumers
   consumers                       ready to activate
```

**Procédure de bascule :**

```bash
# 1. Detect primary failure (automated or manual)
# 2. Stop MM2 replication
# 3. Translate consumer offsets on standby
kafka-consumer-groups.sh --bootstrap-server west-broker1:9092 \
  --group my-app --reset-offsets --to-latest \
  --topic dc-east.orders --execute

# 4. Redirect producers to standby cluster (DNS failover or config push)
# 5. Start consumers on standby cluster pointing to dc-east.* prefixed topics

# RTO: 5-15 min (mostly DNS propagation + consumer group stabilization)
# RPO: seconds to minutes (depends on MM2 replication lag)
```

### Schéma 2 : Actif-actif avec MM2 {#pattern-2-active-active-with-mm2}

```text
DC-East  <----MM2---->  DC-West
   producers write locally         producers write locally
   consumers read local + remote   consumers read local + remote
```

Les consommateurs s'abonnent à la fois aux topics locaux et aux topics préfixés du site distant :

```java
consumer.subscribe(Arrays.asList("orders", "dc-west.orders"));
// Application must handle deduplication if needed
```

**Résolution des conflits :** au niveau applicatif. Utiliser des clés d'enregistrement préfixées par le DC ou des horodatages d'événements pour un mécanisme last-writer-wins.

### Schéma 3 : Stretch cluster (un seul cluster, plusieurs DC) {#pattern-3-stretch-cluster-single-cluster-multiple-dcs}

```properties
# Broker rack awareness
broker.rack=dc-east-rack1

# Topic with rack-aware replica placement
kafka-topics.sh --create --topic orders \
  --partitions 6 --replication-factor 3 \
  --config min.insync.replicas=2 \
  --bootstrap-server broker1:9092
```

Avantages : un seul cluster, pas de traduction d'offsets, forte cohérence.
Inconvénients : latence inter-DC à chaque écriture (acks=all), nécessite une interconnexion à faible latence (RTT < 10 ms).

### Schéma 4 : Tiered storage pour une rétention économique {#pattern-4-tiered-storage-for-cost-effective-retention}

```properties
# Kafka 3.6+ tiered storage (early access)
remote.log.storage.system.enable=true
remote.log.storage.manager.class.name=org.apache.kafka.server.log.remote.storage.RemoteLogManagerConfig

# Move old segments to S3/GCS/Azure Blob
remote.log.storage.manager.impl.prefix=rsm.config.
rsm.config.s3.bucket.name=kafka-tiered-storage
rsm.config.s3.region=us-east-1

# Topic-level config
kafka-configs.sh --alter --topic orders \
  --add-config "remote.storage.enable=true,local.retention.ms=86400000,retention.ms=2592000000" \
  --bootstrap-server broker1:9092
# Local: 1 day, Total: 30 days (29 days on remote storage)
```

## Pièges courants {#gotchas}

- **Nommage des topics dans MM2.** Les topics distants sont préfixés (`dc-east.orders`). Les consommateurs doivent s'abonner aux noms de topics préfixés sur le cluster de secours. Ce comportement n'est pas transparent.
- **Retard des consommateurs après bascule.** Même avec la synchronisation des checkpoints MM2, les offsets des consommateurs peuvent être légèrement en retard. Concevoir les consommateurs pour être idempotents.
- **Les snapshots LVM sur les partitions leaders ne sont pas garantis cohérents.** Le broker peut être en pleine écriture. Préférer le snapshot de brokers followers, ou utiliser `controlled.shutdown` au préalable.
- **La sauvegarde des métadonnées ne capture pas l'état en cours.** Les offsets des groupes de consommateurs exportés via la CLI sont ponctuels ; les consommateurs actifs peuvent avoir des offsets non validés au-delà de ce qui a été exporté.

## Voir aussi {#see-also}

- [[kafka-cluster-management]] - dimensionnement, mises à niveau, réaffectation des partitions
- [[kafka-monitoring-and-tuning]] - métriques JMX, alertes, optimisation des performances
- [[kafka-replication-fundamentals]] - ISR, HW/LEO, modèle de réplication
- [[kafka-fault-tolerance]] - scénarios de panne, schémas multi-DC, réplication tenant compte des racks
- [[mirrormaker]] - approfondissement dédié à MirrorMaker
