---
level: 3
source_sha256: 3811069d625702688d7fbedc2ebe08fa532155b11350c3913e41e8cc2ea9861e
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Cluster-Verwaltung {#kafka-cluster-management}

Clustergröße, Rolling Upgrades, Migration von ZooKeeper zu KRaft, Behandlung von Festplattenausfällen, Partitionsneuzuweisung und Election des bevorzugten Leaders.

## Clustergröße {#cluster-sizing}

### Anzahl der Broker {#broker-count}

Für den Produktivbetrieb mindestens 3 Broker (`replication.factor=3`, `min.insync.replicas=2` – toleriert den Ausfall eines Brokers). Horizontal skalieren durch Hinzufügen von Brokern und Neuzuweisung der Partitionen.

**Formel zur Dimensionierung:**

```toml
brokers_needed = max(
    total_disk_needed / disk_per_broker,
    total_throughput_needed / throughput_per_broker,
    total_partitions / max_partitions_per_broker
)
```

Faustregeln:
- Etwa 4000 Partitionen pro Broker (Leader + Follower), danach lässt die Performance nach
- Etwa 200.000 Partitionen pro Cluster (KRaft; das ZooKeeper-Limit lag bei etwa 100.000)
- Jede Partitionsreplik belegt pro Segment einen File Descriptor plus einen Index-fd
- Ein einzelner Broker kann mit NVMe etwa 100 MB/s Schreiblast verarbeiten, mit rotierenden Festplatten etwa 30 MB/s

### Festplatten {#disk}

```properties
# Multiple log.dirs across disks = parallel I/O
log.dirs=/data/kafka-logs-1,/data/kafka-logs-2,/data/kafka-logs-3
```

**Berechnung der Kapazität:**

```toml
disk_per_broker = (write_throughput_MB_s * retention_seconds * replication_factor) / broker_count
                  + 20% overhead (compaction, index, snapshots)
```

Für Kafka-Workloads ist XFS besser geeignet als ext4. Mit `noatime,nodiratime` einhängen. Bei rotierenden Festplatten RAID-10 verwenden; bei SSDs sind JBOD mit mehreren `log.dirs` zu bevorzugen (Kafka übernimmt die Platzierung der Replikate).

### Arbeitsspeicher {#memory}

Für die Lesleistung stützt sich Kafka auf den Page Cache des Betriebssystems, nicht auf den JVM-Heap.

```toml
total_RAM = JVM_heap + page_cache_for_active_segments
```

- JVM-Heap: typischerweise 6 GB, maximal 8 GB (größere Heaps bedeuten längere GC-Pausen)
- Page Cache: genug, um die aktiven Segmente aller Partitionen zu halten. Das aktive Segment einer Partition entspricht `log.segment.bytes` (Standard 1 GB). Bei 1000 Partitionen sollten etwa 32–64 GB Page Cache angestrebt werden
- Gesamt pro Broker: 64–128 GB RAM sind üblich

### Netzwerk {#network}

```toml
network_per_broker = write_throughput * (replication_factor - 1) + read_throughput * consumer_count
```

Für den Produktivbetrieb mindestens 10 GbE. Bei Bedarf mehrere NICs bündeln (Bonding). `socket.send.buffer.bytes` und `socket.receive.buffer.bytes` so setzen, dass sie an das BDP (Bandbreite-Verzögerungs-Produkt) für die Replikation über Rechenzentren angepasst sind.

### Controller-Quorum (KRaft) {#controller-quorum-kraft}

In den meisten Deployments 3 Controller, bei großen Clustern 5 (toleriert 2 Ausfälle). Controller können gemeinsam mit Brokern betrieben werden (kombinierter Modus) oder dediziert (getrennter Modus).

```properties
# Dedicated controller (separate mode)
process.roles=controller
node.id=100
controller.quorum.voters=100@ctrl1:9093,101@ctrl2:9093,102@ctrl3:9093
listeners=CONTROLLER://ctrl1:9093
controller.listener.names=CONTROLLER
```

## Rolling-Upgrade-Verfahren {#rolling-upgrade-procedure}

### Vor dem Upgrade {#pre-upgrade}

```bash
# 1. Check current versions
kafka-broker-api-versions.sh --bootstrap-server broker1:9092 | head -1

# 2. Verify cluster health
kafka-metadata-quorum.sh --bootstrap-server broker1:9092 describe --status  # KRaft
kafka-topics.sh --describe --under-replicated-partitions --bootstrap-server broker1:9092

# 3. Ensure no under-replicated partitions
# UnderReplicatedPartitions must be 0 before starting
```

### Upgrade-Schritte {#upgrade-steps}

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

### Nach dem Upgrade (nachdem alle Broker aktualisiert wurden) {#post-upgrade-after-all-brokers}

```bash
# Remove protocol version pins to enable new features
# Edit server.properties on all brokers, remove:
#   inter.broker.protocol.version
#   log.message.format.version
# Then rolling restart again

# Verify new version
kafka-broker-api-versions.sh --bootstrap-server broker1:9092
```

### Migration von ZooKeeper zu KRaft {#zookeeper-to-kraft-migration}

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

## Behandlung von Festplattenausfällen {#disk-failure-handling}

### JBOD-Konfiguration {#jbod-configuration}

```properties
# Multiple independent disks (JBOD)
log.dirs=/data1/kafka-logs,/data2/kafka-logs,/data3/kafka-logs
```

Seit Kafka 1.1 wird der Ausfall einer JBOD-Festplatte kontrolliert behandelt:

```properties
# Broker stays online when a disk fails (default since 2.0)
log.dir.failure.handler=kafka.server.LogDirFailureHandler
# Broker marks failed log dir as offline, stops partitions on that disk
# Other disks continue serving
```

### Reaktion auf Festplattenausfälle {#disk-failure-response}

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

### Überwachung des Festplattenzustands {#monitoring-disk-health}

```bash
# Include in cron or monitoring agent
smartctl -a /dev/sdb | grep -E "Reallocated_Sector|Current_Pending|Offline_Uncorrectable"
iostat -x 5 | grep -E "sdb|sdc|sdd"  # watch await, %util
```

Alarm auslösen bei: `await > 50ms`, anhaltend `%util > 90%`, SMART-Fehlern.

## Partitionsneuzuweisung {#partition-reassignment}

### Wann neu zuweisen {#when-to-reassign}

- Neuer Broker dem Cluster hinzugefügt (der neue Broker hat 0 Partitionen)
- Broker außer Betrieb genommen (alle Partitionen verschieben)
- Ungleichmäßige Partitionsverteilung (überlastete Broker)
- Festplatten-Rebalancing innerhalb eines Brokers (Verschieben zwischen `log.dirs`)

### Manuelle Neuzuweisung {#manual-reassignment}

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

### Election des bevorzugten Leaders {#preferred-leader-election}

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

### Automatisches Rebalancing mit Cruise Control {#automated-rebalancing-with-cruise-control}

Für große Cluster automatisiert LinkedIns Cruise Control das Rebalancing:

```bash
# Key endpoints:
# GET  /kafkacruisecontrol/state          - cluster state
# POST /kafkacruisecontrol/rebalance      - trigger rebalance
# POST /kafkacruisecontrol/add_broker     - integrate new broker
# POST /kafkacruisecontrol/remove_broker  - decommission broker

# Example: add broker 4 and rebalance
curl -X POST "http://cruise-control:9090/kafkacruisecontrol/add_broker?brokerid=4&dryrun=false"
```

## Kurzreferenz {#quick-reference}

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

## Stolperfallen {#gotchas}

- **Die Reihenfolge beim Rolling Upgrade ist entscheidend.** Broker immer einzeln aktualisieren und zwischen den Schritten auf die Wiederherstellung der ISR warten. Niemals alle gleichzeitig aktualisieren.
- **`inter.broker.protocol.version` muss vor dem Binär-Upgrade auf die ALTE Version gesetzt sein.** Wird es entfernt, nachdem alle Broker aktualisiert wurden, werden neue Features aktiviert.
- **Das Throttle der Neuzuweisung wird bei einem Fehler nicht automatisch entfernt.** Wenn `--verify` „in progress" anzeigt, aber sich nichts bewegt, `leader.replication.throttled.rate` und `follower.replication.throttled.rate` auf den Brokern prüfen.
- **Ohne Throttling sättigt die Partitionsneuzuweisung das Netzwerk.** Immer das Flag `--throttle` verwenden. Mit 50 MB/s beginnen und schrittweise erhöhen.
- **Die Partitionsanzahl nicht verringern.** Kafka unterstützt kein Reduzieren von Partitionen, nur Erhöhen. Die Partitionsanzahl daher von Anfang an sorgfältig planen. Siehe [[topics-and-partitions]].

## Siehe auch {#see-also}

- [[kafka-monitoring-and-tuning]] - JMX-Metriken, Prometheus-Einrichtung, Tuning von Betriebssystem, JVM und Broker
- [[kafka-backup-and-dr]] - Backup-Strategien, MirrorMaker 2, Muster für Disaster Recovery
- [[broker-architecture]] - Interna, Controller-Election, Log-Speicherung, Segment-Lebenszyklus
- [[topics-and-partitions]] - Planung der Partitionsanzahl, schlüsselbasiertes Routing, Compaction
- [[kafka-replication-fundamentals]] - ISR-Mechanik, acks-Semantik, Unclean Leader Election
