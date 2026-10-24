---
level: 3
source_sha256: 3811069d625702688d7fbedc2ebe08fa532155b11350c3913e41e8cc2ea9861e
translation: machine
translated_at: '2026-10-24'
---
# Gestion du cluster Kafka {#kafka-cluster-management}

Dimensionnement du cluster, mises à niveau progressives, migration de ZooKeeper vers KRaft, gestion des pannes de disque, réaffectation des partitions et élection du leader préféré.

## Dimensionnement du cluster {#cluster-sizing}

### Nombre de brokers {#broker-count}

Au minimum 3 brokers en production (`replication.factor=3`, `min.insync.replicas=2`, ce qui tolère la panne d'un broker). Pour monter en charge horizontalement, ajoutez des brokers puis réaffectez les partitions.

**Formule de dimensionnement :**

```toml
brokers_needed = max(
    total_disk_needed / disk_per_broker,
    total_throughput_needed / throughput_per_broker,
    total_partitions / max_partitions_per_broker
)
```

Règles empiriques :
- ~4000 partitions par broker (leaders et followers) avant que les performances ne se dégradent
- ~200K partitions par cluster (KRaft ; la limite avec ZooKeeper était d'environ 100K)
- Chaque réplica de partition utilise 1 descripteur de fichier par segment, plus 1 descripteur pour l'index
- Un seul broker peut absorber environ 100 Mo/s en écriture avec du NVMe, environ 30 Mo/s avec des disques mécaniques

### Disque {#disk}

```properties
# Multiple log.dirs across disks = parallel I/O
log.dirs=/data/kafka-logs-1,/data/kafka-logs-2,/data/kafka-logs-3
```

**Calcul de la capacité :**

```toml
disk_per_broker = (write_throughput_MB_s * retention_seconds * replication_factor) / broker_count
                  + 20% overhead (compaction, index, snapshots)
```

XFS est préférable à ext4 pour les charges Kafka. Montez avec `noatime,nodiratime`. Utilisez du RAID-10 avec des disques mécaniques ; avec des SSD, privilégiez le JBOD avec plusieurs `log.dirs` (Kafka gère le placement des réplicas).

### Mémoire {#memory}

Kafka s'appuie sur le page cache du système d'exploitation, et non sur le tas de la JVM, pour les performances de lecture.

```toml
total_RAM = JVM_heap + page_cache_for_active_segments
```

- Tas JVM : 6 Go en général, 8 Go au maximum (des tas plus grands allongent les pauses du ramasse-miettes)
- Page cache : assez grand pour contenir les segments actifs de toutes les partitions. Le segment actif d'une partition correspond à `log.segment.bytes` (1 Go par défaut). Pour 1000 partitions, visez environ 32 à 64 Go de page cache
- Total par broker : 64 à 128 Go de RAM sont courants

### Réseau {#network}

```toml
network_per_broker = write_throughput * (replication_factor - 1) + read_throughput * consumer_count
```

10 GbE minimum en production. Agrégez plusieurs cartes réseau si nécessaire. Réglez `socket.send.buffer.bytes` et `socket.receive.buffer.bytes` sur le BDP (produit débit × délai) pour la réplication inter-datacenters.

### Quorum de contrôleurs (KRaft) {#controller-quorum-kraft}

3 contrôleurs pour la plupart des déploiements, 5 pour les grands clusters (tolère 2 pannes). Les contrôleurs peuvent être colocalisés avec les brokers (mode combiné) ou dédiés (mode séparé).

```properties
# Dedicated controller (separate mode)
process.roles=controller
node.id=100
controller.quorum.voters=100@ctrl1:9093,101@ctrl2:9093,102@ctrl3:9093
listeners=CONTROLLER://ctrl1:9093
controller.listener.names=CONTROLLER
```

## Procédure de mise à niveau progressive {#rolling-upgrade-procedure}

### Avant la mise à niveau {#pre-upgrade}

```bash
# 1. Check current versions
kafka-broker-api-versions.sh --bootstrap-server broker1:9092 | head -1

# 2. Verify cluster health
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --status  # KRaft
kafka-topics.sh --describe --under-replicated-partitions --bootstrap-server broker1:9092

# 3. Ensure no under-replicated partitions
# UnderReplicatedPartitions must be 0 before starting
```

### Étapes de mise à niveau {#upgrade-steps}

```bash
# For each broker, one at a time:

# Step 1: Set inter.broker.protocol.version to CURRENT version
# in server.properties BEFORE upgrading binary
echo "inter.broker.protocol.version=3.6" >> /opt/kafka/config/server.properties
echo "log.message.format.version=3.6" >> /opt/kafka/config/server.properties

# Step 2: Stop broker gracefully
sudo systemctl stop kafka
# Wait for "controlled shutdown complete" in logs

# Step 3: Replace binaries
mv /opt/kafka /opt/kafka-old
tar xzf kafka_2.13-3.7.0.tgz -C /opt/
mv /opt/kafka_2.13-3.7.0 /opt/kafka
cp /opt/kafka-old/config/server.properties /opt/kafka/config/

# Step 4: Start broker with new binary
sudo systemctl start kafka

# Step 5: Wait for ISR to recover before moving to next broker
watch -n 5 "kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server broker1:9092 | wc -l"
# Proceed only when output is 0
```

### Après la mise à niveau (une fois tous les brokers mis à jour) {#post-upgrade-after-all-brokers}

```bash
# Remove protocol version pins to enable new features
# Edit server.properties on all brokers, remove:
#   inter.broker.protocol.version
#   log.message.format.version
# Then rolling restart again

# Verify new version
kafka-broker-api-versions.sh --bootstrap-server broker1:9092
```

### Migration de ZooKeeper vers KRaft {#zookeeper-to-kraft-migration}

```bash
# 1. Generate migration metadata
kafka-metadata-migration.sh --zk-connect zk1:2181 --dry-run

# 2. Start KRaft controllers with migration flag
# In controller server.properties:
#   zookeeper.metadata.migration.enable=true
#   zookeeper.connect=zk1:2181,zk2:2181,zk3:2181

# 3. Rolling restart brokers with KRaft config
# 4. Verify all brokers registered with KRaft controllers
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --replication

# 5. Finalize migration (irreversible)
kafka-metadata-migration.sh --finalize
```

## Gestion des pannes de disque {#disk-failure-handling}

### Configuration JBOD {#jbod-configuration}

```properties
# Multiple independent disks (JBOD)
log.dirs=/data1/kafka-logs,/data2/kafka-logs,/data3/kafka-logs
```

Depuis Kafka 1.1, une panne de disque en JBOD est gérée de façon gracieuse :

```properties
# Broker stays online when a disk fails (default since 2.0)
log.dir.failure.handler=kafka.server.LogDirFailureHandler
# Broker marks failed log dir as offline, stops partitions on that disk
# Other disks continue serving
```

### Réponse à une panne de disque {#disk-failure-response}

```bash
# 1. Identify failed disk
kafka-log-dirs.sh --describe --bootstrap-server broker1:9092 | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for broker in data['brokers']:
    for ld in broker['logDirs']:
        if ld['error']:
            print(f\"Broker {broker['broker']}: {ld['logDir']} - {ld['error']}\")
"

# 2. Partitions on failed disk lose their replicas on this broker.
# ISR shrinks. If this was the leader, leadership moves to another ISR member.
# No data loss if replication.factor >= 2.

# 3. Replace disk, recreate mount, restart broker
sudo systemctl stop kafka
# ... replace disk, mkfs.xfs, mount ...
sudo systemctl start kafka

# 4. Verify recovery
watch -n 10 "kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server broker1:9092 | wc -l"
```

### Surveillance de la santé des disques {#monitoring-disk-health}

```bash
# Include in cron or monitoring agent
smartctl -a /dev/sdb | grep -E "Reallocated_Sector|Current_Pending|Offline_Uncorrectable"
iostat -x 5 | grep -E "sdb|sdc|sdd"  # watch await, %util
```

Déclenchez une alerte sur : `await > 50 ms`, `%util > 90 %` de façon soutenue, erreurs SMART.

## Réaffectation des partitions {#partition-reassignment}

### Quand réaffecter {#when-to-reassign}

- Un nouveau broker est ajouté au cluster (il ne porte aucune partition)
- Un broker est mis hors service (il faut retirer toutes ses partitions)
- Répartition inégale des partitions (brokers surchargés)
- Rééquilibrage des disques au sein d'un broker (déplacement entre `log.dirs`)

### Réaffectation manuelle {#manual-reassignment}

```bash
# Step 1: Generate reassignment plan
cat > topics-to-move.json << 'EOF'
{
  "version": 1,
  "topics": [
    {"topic": "orders"},
    {"topic": "events"}
  ]
}
EOF

# Generate proposal (target brokers: 1,2,3,4 - including new broker 4)
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --topics-to-move-json-file topics-to-move.json \
  --broker-list "1,2,3,4" \
  --generate

# Step 2: Save proposed assignment to file
cat > reassignment.json << 'EOF'
{
  "version": 1,
  "partitions": [
    {"topic": "orders", "partition": 0, "replicas": [4,2,3], "log_dirs": ["any","any","any"]},
    {"topic": "orders", "partition": 1, "replicas": [1,4,2], "log_dirs": ["any","any","any"]},
    {"topic": "orders", "partition": 2, "replicas": [2,3,4], "log_dirs": ["any","any","any"]}
  ]
}
EOF

# Step 3: Execute (throttled to avoid saturating network)
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassignment.json \
  --execute \
  --throttle 50000000  # 50 MB/s replication throttle

# Step 4: Monitor progress
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassignment.json \
  --verify

# Step 5: After completion, remove throttle
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassignment.json \
  --verify  # automatically removes throttle on completion
```

### Élection du leader préféré {#preferred-leader-election}

```bash
# After reassignment, new preferred leaders may not be active leaders.
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type PREFERRED \
  --all-topic-partitions

# Or for specific topic:
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type PREFERRED \
  --topic orders
```

### Rééquilibrage automatisé avec Cruise Control {#automated-rebalancing-with-cruise-control}

Pour les grands clusters, Cruise Control, développé par LinkedIn, automatise le rééquilibrage :

```bash
# Key endpoints:
# GET  /kafkacruisecontrol/state          - cluster state
# POST /kafkacruisecontrol/rebalance      - trigger rebalance
# POST /kafkacruisecontrol/add_broker     - integrate new broker
# POST /kafkacruisecontrol/remove_broker  - decommission broker

# Example: add broker 4 and rebalance
curl -X POST "http://cruise-control:9090/kafkacruisecontrol/add_broker?brokerid=4&dryrun=false"
```

## Aide-mémoire {#quick-reference}

```bash
# --- Cluster health ---
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --status
kafka-topics.sh --describe --under-replicated-partitions --bootstrap-server broker1:9092
kafka-topics.sh --describe --unavailable-partitions --bootstrap-server broker1:9092

# --- Broker API versions ---
kafka-broker-api-versions.sh --bootstrap-server broker1:9092

# --- Partition reassignment ---
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --topics-to-move-json-file topics.json --broker-list "1,2,3,4" --generate
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassign.json --execute --throttle 50000000
kafka-reassign-partitions.sh --bootstrap-server broker1:9092 \
  --reassignment-json-file reassign.json --verify

# --- Leader election ---
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type PREFERRED --all-topic-partitions

# --- Log dirs (disk usage per partition) ---
kafka-log-dirs.sh --describe --bootstrap-server broker1:9092 --topic-list orders

# --- Consumer lag ---
kafka-consumer-groups.sh --bootstrap-server broker1:9092 --describe --group my-group

# --- Config dump ---
kafka-configs.sh --describe --all --entity-type brokers --entity-name 1 \
  --bootstrap-server broker1:9092
```

## Pièges courants {#gotchas}

- **L'ordre de la mise à niveau progressive compte.** Mettez à niveau les brokers un par un, en attendant la récupération des ISR entre chaque opération. Ne mettez jamais tout à niveau en même temps.
- **`inter.broker.protocol.version` doit rester à l'ANCIENNE version** avant la mise à niveau des binaires. La supprimer une fois tous les brokers mis à jour active les nouvelles fonctionnalités.
- **Le throttle de réaffectation n'est pas retiré automatiquement en cas d'échec.** Si `--verify` affiche « in progress » alors que rien ne bouge, vérifiez `leader.replication.throttled.rate` et `follower.replication.throttled.rate` sur les brokers.
- **Une réaffectation de partitions sature le réseau** si elle n'est pas limitée. Utilisez toujours l'option `--throttle`. Commencez à 50 Mo/s et augmentez progressivement.
- **Ne réduisez pas le nombre de partitions.** Kafka ne permet pas de diminuer le nombre de partitions, seulement de l'augmenter. Planifiez soigneusement ce nombre dès le départ. Voir [[topics-and-partitions]].

## Voir aussi {#see-also}

- [[kafka-monitoring-and-tuning]] - métriques JMX, configuration de Prometheus, réglage du système d'exploitation, de la JVM et des brokers
- [[kafka-backup-and-dr]] - stratégies de sauvegarde, MirrorMaker 2, schémas de reprise après sinistre
- [[broker-architecture]] - fonctionnement interne, élection du contrôleur, stockage des logs, cycle de vie des segments
- [[topics-and-partitions]] - planification du nombre de partitions, routage par clé, compaction
- [[kafka-replication-fundamentals]] - fonctionnement des ISR, sémantique d'acks, élection de leader non propre
