---
level: 4
source_sha256: 58a6ebde2d41cbe66a9b6f55d3ceaf26c462a1e22d715acdee7bbadf14463ba0
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Backup und Disaster Recovery {#kafka-backup-and-disaster-recovery}

MirrorMaker 2 für Replikation über mehrere Rechenzentren, Backup-Strategien (auf Topic-Ebene, Dateisystem, Metadaten) und Disaster-Recovery-Muster (Active-Passive, Active-Active, Stretch Cluster, Tiered Storage).

## MirrorMaker 2 - Replikation über mehrere Rechenzentren {#mirrormaker-2-multi-dc-replication}

MM2 basiert auf Kafka Connect. Unterstützt werden Active-Active-, Active-Passive- und Fan-out-Topologien.

### Konfiguration {#configuration}

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

### Start {#launch}

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

### Consumer-Failover mit Offset-Übersetzung {#consumer-failover-with-offset-translation}

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

### Monitoring von MM2 {#mm2-monitoring}

Wichtige Metriken (über JMX auf den Connect-Workern):
- `kafka.connect.mirror:type=MirrorSourceConnector,target=*,topic=*,partition=*` - `record-count`, `byte-rate`, `replication-latency-ms`
- Alarm bei `replication-latency-ms-avg > 5000` (5 s Replikationsverzögerung)

## Backup-Strategien {#backup-strategies}

Kafka ist keine Datenbank, dennoch existieren Szenarien mit Datenverlust.

### 1. Backup auf Topic-Ebene mit kafka-consumer {#1-topic-level-backup-with-kafka-consumer}

```bash
# Dump topic to file (for smaller topics / config topics)
kafka-console-consumer.sh --bootstrap-server broker1:9092 \
  --topic __consumer_offsets --from-beginning \
  --timeout-ms 30000 \
  --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" \
  > consumer_offsets_backup_$(date +%Y%m%d).txt
```

### 2. Backup auf Dateisystemebene {#2-filesystem-level-backup}

```bash
# Stop broker, snapshot log.dirs
sudo systemctl stop kafka

# Rsync partition data (preserves segment files, indexes, snapshots)
rsync -avz --progress /data/kafka-logs/ backup-server:/backup/kafka/broker1/

sudo systemctl start kafka
```

Für Online-Backups das darunterliegende Dateisystem snapshotten (LVM, ZFS oder EBS-Snapshots in der Cloud).

```bash
# LVM snapshot (online, consistent if broker is not leader for partitions)
lvcreate -L 50G -s -n kafka-snap /dev/vg0/kafka-data
mount /dev/vg0/kafka-snap /mnt/kafka-snap
rsync -avz /mnt/kafka-snap/ backup-server:/backup/kafka/broker1/
umount /mnt/kafka-snap
lvremove -f /dev/vg0/kafka-snap
```

### 3. Replikation zwischen Clustern (bevorzugt) {#3-cross-cluster-replication-preferred}

Ein MirrorMaker-2-Replikat auf einen Standby-Cluster ist das empfohlene „Backup“ für Produktionsdaten. Es übernimmt Offset-Übersetzung, Topic-Konfigurationen und ACLs.

### 4. Backup der Metadaten {#4-metadata-backup}

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

## Disaster-Recovery-Muster {#disaster-recovery-patterns}

### Muster 1: Active-Passive mit MM2 {#pattern-1-active-passive-with-mm2}

```text
DC-East (Primary)  ----MM2---->  DC-West (Standby)
   producers                       idle consumers
   consumers                       ready to activate
```

**Failover-Ablauf:**

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

### Muster 2: Active-Active mit MM2 {#pattern-2-active-active-with-mm2}

```text
DC-East  <----MM2---->  DC-West
   producers write locally         producers write locally
   consumers read local + remote   consumers read local + remote
```

Consumer abonnieren sowohl lokale als auch remote-präfixierte Topics:

```java
consumer.subscribe(Arrays.asList("orders", "dc-west.orders"));
// Application must handle deduplication if needed
```

**Konfliktauflösung:** auf Anwendungsebene. Dazu Record-Keys mit DC-Präfix oder Event-Zeitstempel für Last-Writer-Wins verwenden.

### Muster 3: Stretch Cluster (ein Cluster, mehrere Rechenzentren) {#pattern-3-stretch-cluster-single-cluster-multiple-dcs}

```properties
# Broker rack awareness
broker.rack=dc-east-rack1

# Topic with rack-aware replica placement
kafka-topics.sh --create --topic orders \
  --partitions 6 --replication-factor 3 \
  --config min.insync.replicas=2 \
  --bootstrap-server broker1:9092
```

Vorteile: ein einziger Cluster, keine Offset-Übersetzung, starke Konsistenz.
Nachteile: Latenz zwischen den Rechenzentren bei jedem Schreibvorgang (acks=all), erfordert eine Verbindung mit niedriger Latenz (<10 ms RTT).

### Muster 4: Tiered Storage für kosteneffiziente Aufbewahrung {#pattern-4-tiered-storage-for-cost-effective-retention}

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

## Stolpersteine {#gotchas}

- **Benennung der MM2-Topics.** Remote-Topics erhalten ein Präfix (`dc-east.orders`). Consumer müssen auf dem Standby-Cluster die präfixierten Topic-Namen abonnieren. Das geschieht nicht transparent.
- **Consumer-Lag nach einem Failover.** Auch mit MM2-Checkpoint-Synchronisation können Consumer-Offsets leicht zurückliegen. Consumer sollten daher idempotent entworfen werden.
- **LVM-Snapshots auf Leader-Partitionen sind nicht garantiert konsistent.** Der Broker könnte sich mitten in einem Schreibvorgang befinden. Besser Follower-Broker snapshotten oder vorher `controlled.shutdown` verwenden.
- **Die Metadatensicherung erfasst keinen laufenden Zustand.** Über die CLI exportierte Consumer-Group-Offsets sind eine Momentaufnahme; aktive Consumer können nicht committete Offsets haben, die über den Export hinausgehen.

## Siehe auch {#see-also}

- [[kafka-cluster-management]] - Dimensionierung, Upgrades, Partition-Reassignment
- [[kafka-monitoring-and-tuning]] - JMX-Metriken, Alarmierung, Performance-Tuning
- [[kafka-replication-fundamentals]] - ISR, HW/LEO, Replikationsmodell
- [[kafka-fault-tolerance]] - Fehlerszenarien, Muster für mehrere Rechenzentren, rack-aware Replikation
- [[mirrormaker]] - vertiefende Behandlung von MirrorMaker
