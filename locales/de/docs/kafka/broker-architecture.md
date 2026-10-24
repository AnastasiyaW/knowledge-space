---
title: "Broker-Architektur"
category: concepts
tags: [kafka, broker, cluster, zookeeper, kraft, replication]
level: 5
source_sha256: c51494aca14f0a4f8d0f5b5fa2a1b9eeea50f931ba5656af8347e167e776acd9
translation: machine
translated_at: '2026-10-24'
---
# Broker-Architektur {#broker-architecture}

Ein Kafka-Broker ist ein einzelner Serverprozess, der Nachrichten von Producern empfängt, Offsets vergibt, Daten auf die Festplatte schreibt und Fetch-Anfragen von Consumern beantwortet. Ein **Cluster** ist eine Gruppe von Brokern, die sich über eine Metadatenschicht (ZooKeeper oder KRaft) koordinieren. Dieser Eintrag behandelt die internen Abläufe der Broker, die Controller-Wahl, die Partition-Leadership, die Replikationsmechanik, die Log-Speicherung, Aufbewahrungsrichtlinien und den Migrationspfad zu KRaft.

## Rolle des Brokers im Cluster {#broker-role-in-a-cluster}

Jeder Broker in einem Cluster:
- wird durch eine eindeutige Ganzzahl `broker.id` identifiziert
- besitzt eine Teilmenge der Partitionen (als Leader oder Follower)
- nimmt TCP-Verbindungen auf den `listeners` an (PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL)
- speichert Partitionsdaten unter `log.dirs` als Segmentdateien mit reinem Anhängen (append-only)
- meldet Metadaten an den Controller und empfängt Partitionszuweisungen

Ein minimaler Produktiv-Cluster benötigt **3 Broker** (um einen Ausfall mit `replication.factor=3` und `min.insync.replicas=2` zu tolerieren).

```php
Producer --> Broker 0 (leader P0)  --> Broker 1 (follower P0, leader P1)
                                   --> Broker 2 (follower P0, follower P1)
```

Broker sind **bezüglich der Consumer zustandslos** -- sie verwalten keine Consumer-Offsets intern (Offsets werden im Topic `__consumer_offsets` gespeichert). Siehe [[consumer-groups]].

## Controller-Wahl {#controller-election}

### ZooKeeper-Modus (veraltet, seit Kafka 3.3 als deprecated markiert) {#zookeeper-mode-legacy-deprecated-since-kafka-33}

Ein Broker im Cluster wird als **Controller** gewählt. Er ist verantwortlich für:
- die Erkennung von Broker-Ausfällen (über das Ablaufen der ZooKeeper-Session)
- die Neuzuweisung der Partition-Leadership, wenn ein Leader-Broker ausfällt
- die Weitergabe von Metadatenänderungen (neue Topics, Neuzuweisung von Partitionen) an alle Broker

Wahlmechanismus:
1. Jeder Broker versucht beim Start, einen **ephemeren ZNode** `/controller` in ZooKeeper anzulegen
2. Der erste Broker, dem dies gelingt, wird Controller
3. Die übrigen Broker setzen einen **Watch** auf den ZNode `/controller`
4. Wenn der Controller ausfällt, löscht ZooKeeper den ephemeren Knoten, was ein Watch-Ereignis auslöst
5. Die verbleibenden Broker konkurrieren erneut um das Anlegen des Knotens -- der Gewinner wird neuer Controller

```bash
# ZooKeeper znodes used by Kafka
/brokers/ids/[broker_id]      # ephemeral - broker registration
/controller                    # ephemeral - current controller
/brokers/topics/[topic]        # persistent - topic metadata
/admin/reassign_partitions     # persistent - reassignment state
```

**Einschränkungen**: ZooKeeper wird bei großer Skalierung zum Engpass (>200k Partitionen). Die Verbreitung von Metadaten ist asynchron, was während eines Controller-Failovers Zeitfenster mit Split-Brain-Verhalten verursacht.

### KRaft-Modus (Kafka Raft -- produktionsreif seit Kafka 3.6) {#kraft-mode-kafka-raft-production-ready-since-kafka-36}

KRaft ersetzt ZooKeeper durch ein internes, auf Raft basierendes Konsensprotokoll. Controller-Knoten bilden ein **Quorum**, das die Cluster-Metadaten als replizierten Log (Topic `__cluster_metadata`) verwaltet.

Wesentliche Unterschiede zum ZooKeeper-Modus:

| Aspekt | ZooKeeper | KRaft |
|--------|-----------|-------|
| Externe Abhängigkeit | ZooKeeper-Ensemble (3-5 Knoten) | Keine |
| Metadatenspeicherung | ZooKeeper-znodes | Internes Topic `__cluster_metadata` |
| Controller-Wahl | Wettlauf um ephemeren znode | Raft-Leader-Wahl |
| Max. Partitionen pro Cluster | praktische Grenze von ~200k | Millionen (getestet mit 2M+) |
| Herunterfahren/Starten | Langsam (vollständiges Neuladen der Metadaten aus ZK) | Schnell (Log-Replay) |
| Konfiguration | `zookeeper.connect` | `controller.quorum.voters` |

KRaft-Knotenrollen:
- **Nur Controller** (`process.roles=controller`): nimmt am Metadaten-Quorum teil, bedient keine Client-Daten
- **Nur Broker** (`process.roles=broker`): bedient Produce/Fetch, empfängt Metadaten von den Controllern
- **Kombiniert** (`process.roles=broker,controller`): beide Rollen in einer JVM (geeignet für kleine Cluster, für Produktivbetrieb mit mehr als 10 Knoten nicht empfohlen)

```properties
# KRaft controller configuration
process.roles=controller
node.id=1
controller.quorum.voters=1@controller1:9093,2@controller2:9093,3@controller3:9093
controller.listener.names=CONTROLLER
listeners=CONTROLLER://controller1:9093
log.dirs=/var/kafka/controller-logs
```

```properties
# KRaft broker configuration
process.roles=broker
node.id=101
controller.quorum.voters=1@controller1:9093,2@controller2:9093,3@controller3:9093
listeners=PLAINTEXT://broker1:9092
log.dirs=/var/kafka/data
```

Referenz: [KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)

## Partition-Leadership und ISR {#partition-leadership-and-isr}

### Leader und Follower {#leader-and-followers}

Jede Partition hat genau **einen Leader** und null oder mehr **Follower**. Der Leader:
- bearbeitet alle Produce- und Fetch-Anfragen für diese Partition
- vergibt streng monoton steigende Offsets an eingehende Records
- pflegt das **High Watermark (HW)** -- den Offset, bis zu dem alle ISR-Mitglieder repliziert haben

Follower:
- senden Fetch-Anfragen an den Leader (dasselbe Protokoll wie Consumer)
- replizieren Records in der richtigen Reihenfolge
- bedienen **keine** Client-Lesezugriffe (im Standardmodus; siehe KIP-392 für Follower Fetching)

### In-Sync Replicas (ISR) {#in-sync-replicas-isr}

Die ISR ist die dynamische Menge der Replicas, die mit dem Leader „aufgeholt“ sind. Eine Replica fällt aus der ISR, wenn sie innerhalb von `replica.lag.time.max.ms` (Standard: 30s) keine Daten mehr vom Leader abgerufen hat.

```sql
Partition P0:
  Leader: Broker 0  (offset 1000, HW=998)
  ISR: [0, 1, 2]
  Broker 1: offset 998 (in sync)
  Broker 2: offset 998 (in sync)
  Broker 3: offset 950 (OUT of sync -- lagging, removed from ISR)
```

**Committed Record**: Ein Record ist committed (für Consumer sichtbar), erst wenn **alle ISR-Mitglieder** ihn bestätigt haben. Das High Watermark rückt entsprechend vor.

### Replikationsfaktor {#replication-factor}

Wird pro Topic bei der Erstellung gesetzt:

```bash
kafka-topics.sh --create \
  --topic orders \
  --partitions 12 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092
```

Faustregeln:
- `replication.factor=3` ist der Standard für den Produktivbetrieb
- **Muss kleiner oder gleich der Anzahl der Broker** im Cluster sein
- Ein höherer RF erhöht die Haltbarkeit, kostet aber Plattenplatz und Netzwerkkapazität

### min.insync.replicas {#mininsyncreplicas}

Steuert die minimale Anzahl von Replicas, die einen Schreibvorgang bestätigen müssen, bevor der Producer eine Erfolgsmeldung erhält (bei `acks=all`):

```properties
# Topic-level or broker-level config
min.insync.replicas=2
```

Bei `replication.factor=3` und `min.insync.replicas=2`:
- Schreibvorgänge gelingen, solange mindestens 2 Replicas (einschließlich des Leaders) in-sync sind
- Schrumpft die ISR auf 1, erhalten Produce-Anfragen mit `acks=all` eine `NotEnoughReplicasException`
- Dies garantiert **keinen Datenverlust**, solange mindestens eine der 2 bestätigenden Replicas überlebt

**Stolperfalle**: `min.insync.replicas` hat keine Wirkung, wenn der Producer nicht `acks=all` (oder `acks=-1`) setzt. Bei `acks=1` bestätigt nur der Leader.

Siehe [[kafka-fault-tolerance]] für Leader-Wahl, unclean Leader Election und Fehlerszenarien.

## Log-Segmente und Speicherung {#log-segments-and-storage}

### Layout auf dem Datenträger {#on-disk-layout}

Jede Partition wird als Verzeichnis im Dateisystem des Brokers gespeichert:

```text
/var/kafka/data/
  orders-0/                          # topic "orders", partition 0
    00000000000000000000.log         # segment file (records)
    00000000000000000000.index        # offset index
    00000000000000000000.timeindex    # timestamp index
    00000000000000123456.log         # next segment (starts at offset 123456)
    00000000000000123456.index
    00000000000000123456.timeindex
    leader-epoch-checkpoint
    partition.metadata
```

- **.log**: die eigentlichen Nachrichtendaten (batchweise komprimiert mit dem konfigurierten `compression.type`)
- **.index**: spärlicher Index von Offset zu Position (bildet logische Offsets auf Byte-Positionen in `.log` ab)
- **.timeindex**: spärlicher Index von Zeitstempel zu Offset (ermöglicht zeitbasierte Suche)

### Segment-Rotation {#segment-rolling}

Ein neues Segment wird angelegt, sobald eine dieser Bedingungen erfüllt ist:

| Konfiguration | Standard | Löst ein neues Segment aus, wenn ... |
|--------------|----------|--------------------------------------|
| `log.segment.bytes` | 1 GB (`1073741824`) | das aktuelle Segment diese Größe erreicht |
| `log.roll.ms` / `log.roll.hours` | 7 Tage (`168` Stunden) | die Zeit seit Erstellung des Segments diesen Wert überschreitet |
| `log.index.size.max.bytes` | 10 MB | die Indexdatei diese Größe erreicht |

Nur das **aktive Segment** (das jüngste) wird beschrieben. Ältere Segmente sind unveränderlich und für Aufbewahrung bzw. Compaction geeignet.

```properties
# Smaller segments = more frequent rolling, finer retention granularity
log.segment.bytes=536870912    # 512 MB
log.roll.hours=24              # roll daily
```

### Zero-Copy-Übertragung {#zero-copy-transfer}

Kafka verwendet `sendfile()` (Zero-Copy), um Daten von der Festplatte in den Netzwerk-Socket zu übertragen, wobei Puffer im Userspace umgangen werden. Deshalb erreicht Kafka einen hohen Durchsatz bei geringem CPU-Aufwand. Zero-Copy funktioniert nur, wenn auf dem Broker-Listener **kein** SSL aktiviert ist.

## Aufbewahrungsrichtlinien {#retention-policies}

Kafka unterstützt drei Aufbewahrungsstrategien, konfigurierbar pro Topic oder auf Broker-Ebene.

### Zeitbasierte Aufbewahrung (Standard) {#time-based-retention-default}

Segmente löschen, die älter als die Aufbewahrungsdauer sind:

```properties
log.retention.hours=168         # 7 days (default)
log.retention.minutes=10080     # equivalent, finer granularity
log.retention.ms=604800000      # equivalent, finest granularity
# Precedence: ms > minutes > hours
```

Der Log-Cleaner-Thread des Brokers prüft regelmäßig (`log.retention.check.interval.ms`, Standard 5 Minuten), ob abgeschlossene Segmente einen maximalen Zeitstempel haben, der älter als die Aufbewahrungsdauer ist. Ist das der Fall, wird das Segment gelöscht.

**Wichtig**: Die Aufbewahrung gilt für ganze Segmente, nicht für einzelne Records. Ein Record kann länger bestehen als `log.retention.hours`, wenn er sich im aktiven Segment befindet, das noch nicht rotiert wurde.

### Größenbasierte Aufbewahrung {#size-based-retention}

Älteste Segmente löschen, wenn das Partitions-Log eine bestimmte Gesamtgröße überschreitet:

```properties
log.retention.bytes=10737418240  # 10 GB per partition
# -1 = no size limit (default)
```

Kann mit der zeitbasierten Aufbewahrung kombiniert werden -- welche Bedingung zuerst eintritt, gewinnt.

### Log Compaction {#log-compaction}

Behält nur den **jeweils neuesten Wert pro Schlüssel** innerhalb einer Partition. Wird für Changelog- und Snapshot-Topics verwendet (z. B. `__consumer_offsets`, Zustandsspeicher von KTables).

```properties
log.cleanup.policy=compact       # or "delete,compact" for both
log.cleaner.min.compaction.lag.ms=0
log.cleaner.min.cleanable.ratio=0.5
```

Ablauf der Compaction:
1. Der Log-Cleaner-Thread erstellt eine Offset-Map im Speicher (Schlüssel-Hash -> neuester Offset)
2. Er liest den „schmutzigen“ (noch nicht kompaktierten) Teil des Logs
3. Er kopiert Records und überspringt jeden Schlüssel, dessen neuester Offset in einem neueren Segment liegt
4. Records mit `null`-Wert (Tombstones) werden für `delete.retention.ms` (Standard 24h) aufbewahrt und danach entfernt

```text
Before compaction:        After compaction:
offset  key  value        offset  key  value
0       A    v1           2       A    v3
1       B    v1           3       B    v2
2       A    v3           (tombstone B removed after delete.retention.ms)
3       B    v2
4       B    null (tombstone)
```

**Stolperfalle**: Kompaktierte Topics müssen Schlüssel ungleich null haben. Records ohne Schlüssel werden abgelehnt, wenn `log.cleanup.policy=compact` gesetzt ist.

Siehe [[topics-and-partitions]] für Topic-spezifische Konfigurationsüberschreibungen.

## Wichtige Broker-Konfigurationen {#key-broker-configurations}

### Kritische Einstellungen für den Produktivbetrieb {#critical-production-settings}

```properties
# --- Identity & Networking ---
broker.id=1                              # unique per broker
listeners=PLAINTEXT://0.0.0.0:9092       # bind address
advertised.listeners=PLAINTEXT://broker1.example.com:9092  # client-facing address

# --- Storage ---
log.dirs=/data/kafka1,/data/kafka2       # comma-separated for JBOD
num.partitions=6                         # default partitions for auto-created topics
default.replication.factor=3             # default RF for auto-created topics

# --- Replication ---
min.insync.replicas=2                    # require 2 ISR acks with acks=all
replica.lag.time.max.ms=30000            # ISR eviction threshold
replica.fetch.max.bytes=1048576          # max bytes per replica fetch

# --- Retention ---
log.retention.hours=168                  # 7 days
log.retention.bytes=-1                   # unlimited size
log.segment.bytes=1073741824             # 1 GB segments
log.retention.check.interval.ms=300000   # check every 5 min

# --- Performance ---
num.io.threads=8                         # threads for disk I/O
num.network.threads=3                    # threads for network requests
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
num.replica.fetchers=1                   # increase for high-partition counts

# --- Topic Management ---
auto.create.topics.enable=false          # ALWAYS disable in production
delete.topic.enable=true                 # allow topic deletion
```

### Konfigurationshierarchie {#config-hierarchy}

Kafka-Konfigurationen können auf mehreren Ebenen gesetzt werden. Spezifischere Einstellungen überschreiben allgemeinere:

1. **Dynamische Konfiguration pro Topic** (höchste Priorität): `kafka-configs.sh --alter --topic X`
2. **Dynamische Konfiguration pro Broker**: `kafka-configs.sh --alter --entity-type brokers --entity-name 0`
3. **Dynamische clusterweite Konfiguration**: `kafka-configs.sh --alter --entity-type brokers --entity-default`
4. **Statische Broker-Konfiguration** (`server.properties`): erfordert einen Neustart des Brokers

```bash
# Set topic-level retention to 3 days (overrides broker default)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --entity-type topics --entity-name orders \
  --add-config retention.ms=259200000

# Set broker-level default partitions dynamically (no restart)
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --entity-type brokers --entity-default \
  --add-config num.partitions=12
```

## Migration von ZooKeeper zu KRaft {#kraft-migration-from-zookeeper}

Migrationspfad für bestehende, ZooKeeper-basierte Cluster (unterstützt seit Kafka 3.6, ZooKeeper vollständig entfernt in Kafka 4.0):

### Schrittweise Migration {#step-by-step-migration}

```hcl
Phase 1: Deploy KRaft controllers alongside existing ZK cluster
Phase 2: Migrate metadata (brokers dual-write to ZK and KRaft)
Phase 3: Switch brokers to KRaft mode
Phase 4: Decommission ZooKeeper
```

**1. KRaft-Controller-Knoten bereitstellen**

```properties
# New controller nodes (do NOT run on existing broker machines if possible)
process.roles=controller
node.id=3000    # use IDs that don't conflict with existing broker.id values
controller.quorum.voters=3000@ctrl1:9093,3001@ctrl2:9093,3002@ctrl3:9093
controller.listener.names=CONTROLLER
listeners=CONTROLLER://ctrl1:9093
```

**2. Speicher der Controller formatieren**

```bash
# Generate a cluster ID from the existing ZK cluster
CLUSTER_ID=$(kafka-metadata.sh --snapshot /var/kafka/data/__cluster_metadata-0/00000000000000000000.log --cluster-id)
# Or from ZooKeeper directly:
CLUSTER_ID=$(zookeeper-shell.sh localhost:2181 get /cluster/id | grep version | jq -r .id)

# Format each controller's log directory
kafka-storage.sh format \
  --config /etc/kafka/kraft-controller.properties \
  --cluster-id $CLUSTER_ID
```

**3. Controller starten und Migration beginnen**

```bash
# Start controller quorum
kafka-server-start.sh /etc/kafka/kraft-controller.properties

# Initiate migration on the ZK-based cluster -- enable dual-write
kafka-metadata.sh --bootstrap-controller ctrl1:9093 \
  --command-config admin.properties \
  migrate --start
```

**4. Broker auf den KRaft-Modus umstellen**

Für jeden Broker (rollierender Neustart):

```properties
# Remove ZK config, add KRaft config
# REMOVE: zookeeper.connect=zk1:2181,zk2:2181,zk3:2181
# ADD:
controller.quorum.voters=3000@ctrl1:9093,3001@ctrl2:9093,3002@ctrl3:9093
controller.listener.names=CONTROLLER
```

```bash
# Restart each broker one at a time
kafka-server-stop.sh
kafka-server-start.sh /etc/kafka/server.properties
```

**5. Migration abschließen**

```bash
# After all brokers are on KRaft, finalize (stops dual-write to ZK)
kafka-metadata.sh --bootstrap-controller ctrl1:9093 \
  --command-config admin.properties \
  migrate --finalize
```

**6. ZooKeeper außer Betrieb nehmen**

Nach dem Abschluss wird ZooKeeper nicht mehr benötigt. ZK-Knoten stoppen und aus der Infrastruktur entfernen.

### Stolperfallen bei der Migration {#migration-gotchas}

- **Keine Kafka-Versionen überspringen**: Bei einer älteren Version zuerst auf 3.6+ aktualisieren, danach von ZK zu KRaft migrieren
- **Anzahl der Controller-Knoten**: Immer ungerade (3 oder 5), entsprechend der Dimensionierung eines ZooKeeper-Ensembles
- **Konflikte bei `node.id`**: Die IDs der Controller-Knoten dürfen sich nicht mit bestehenden Broker-IDs überschneiden
- **ACLs**: Bei Verwendung von ZK-basierten ACLs (`kafka.security.auth.SimpleAclAuthorizer`) vor der Migration auf `kafka.security.authorizer.AclAuthorizer` (KRaft-kompatibel) umstellen
- **Rollback**: Nur vor `--finalize` möglich. Nach dem Abschluss wird kein Rollback zu ZK unterstützt
- **Monitoring**: `kafka.controller:type=KafkaController,name=ActiveControllerCount` beobachten -- der Wert muss jederzeit genau 1 sein

Referenz: [Apache Kafka ZooKeeper to KRaft Migration Guide](https://kafka.apache.org/documentation/#kraft_zk_migration)

## Monitoring der Broker-Gesundheit {#monitoring-broker-health}

Wichtige JMX-Metriken zur Überwachung:

```markdown
# Cluster-level
kafka.controller:type=KafkaController,name=ActiveControllerCount  # must be 1
kafka.controller:type=KafkaController,name=OfflinePartitionsCount  # must be 0

# Broker-level
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions    # should be 0
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec             # spikes = trouble
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce  # p99 latency
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Fetch
kafka.log:type=LogFlushRateAndTimeMs                                # disk flush latency
```

**Alarmschwellen**:
- `OfflinePartitionsCount > 0` -- sofortige Untersuchung
- `UnderReplicatedPartitions > 0` für mehr als 5 Minuten -- Broker ist wahrscheinlich überlastet oder fällt aus
- Anhaltend hohe `IsrShrinksPerSec` -- Festplatten-I/O, Netzwerk und GC-Pausen prüfen

## Querverweise {#cross-references}

- [[topics-and-partitions]] -- Strategien zur Partitionszuweisung, schlüsselbasiertes Routing, Dimensionierung der Partitionsanzahl
- [[consumer-groups]] -- Verwaltung der Consumer-Offsets, Rebalancing, Group Coordinator
- [[kafka-replication-fundamentals]] -- ISR, HW/LEO, acks + min.insync.replicas
- [[kafka-fault-tolerance]] -- unclean Leader Election, rack-aware Replikation, Preferred Leader Election

## Externe Referenzen {#external-references}

- [Apache Kafka Broker Configuration](https://kafka.apache.org/documentation/#brokerconfigs)
- [KIP-500: Replace ZooKeeper with KRaft](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)
- [KRaft Migration Guide](https://kafka.apache.org/documentation/#kraft_zk_migration)
- [Kafka Design: Log Storage](https://kafka.apache.org/documentation/#design_filesystem)
- [Kafka Design: Replication](https://kafka.apache.org/documentation/#replication)
