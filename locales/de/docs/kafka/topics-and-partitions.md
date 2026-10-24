---
title: "Topics und Partitionen"
category: concepts
tags: [kafka, topics, partitions, keys, ordering, segments]
level: 5
source_sha256: 3cac388b22e48a9441a3ae868066c45d8b1fe4db5d78b8a230b2cce84345d0c8
translation: machine
translated_at: '2026-10-24'
---
# Topics und Partitionen {#topics-and-partitions}

Ein **Topic** ist Kafkas logischer Kanal zur Organisation von Records. Physisch wird jedes Topic in eine oder mehrere **Partitionen** aufgeteilt – geordnete, nur anfügbare, unveränderliche Log-Segmente, die auf den Festplatten der Broker gespeichert werden. Partitionen sind die grundlegende Einheit für Parallelität, Speicherung und Replikation in Kafka. Jede Designentscheidung in einem Kafka-Deployment – Durchsatz, Ordnungsgarantien, Skalierung der Consumer, Datenaufbewahrung – geht darauf zurück, wie Topics und Partitionen konfiguriert sind.

## Kernkonzepte {#core-concepts}

### Topic als logischer Kanal {#topic-as-logical-channel}

Ein Topic ist ein benannter Datenstrom von Records. Producer schreiben in Topics; Consumer lesen aus Topics. Topics werden über ihren Namen identifiziert und existieren clusterweit – sie sind nicht an einen einzelnen Broker gebunden.

- Topics können gleichzeitig beliebig viele Producer und Consumer haben
- Mehrere [[consumer-groups]] können dasselbe Topic unabhängig voneinander lesen und jeweils ihre eigenen Offsets verwalten
- Topics werden explizit erstellt (`kafka-topics.sh --create`) oder automatisch, sobald ein Producer erstmals in sie schreibt (sofern `auto.create.topics.enable=true` auf dem Broker gesetzt ist)
- Topic-Namen unterstützen `[a-zA-Z0-9._-]`, maximal 249 Zeichen. Verwende `.` und `_` nicht im selben Cluster – Kafka nutzt beide als interne Trennzeichen in Metriknamen

### Partition als Einheit der Parallelität {#partition-as-unit-of-parallelism}

Jede Partition ist ein unabhängiges, geordnetes Log. Die Parallelität in Kafka skaliert mit der Anzahl der Partitionen:

```yaml
Topic: user-events (4 partitions)

Partition 0:  [msg0] [msg1] [msg2] [msg3] ...
Partition 1:  [msg0] [msg1] [msg2] ...
Partition 2:  [msg0] [msg1] [msg2] [msg3] [msg4] ...
Partition 3:  [msg0] [msg1] ...
```

- Jede Partition hat eine eigene Offset-Sequenz, die bei 0 beginnt
- Eine [[consumer-groups|Consumer-Gruppe]] kann höchstens einen Consumer pro Partition haben – die Partitionsanzahl ist also die obere Grenze für die Parallelität der Consumer
- Jede Partition hat eine **Leader**-Replik (verarbeitet alle Lese- und Schreibzugriffe) und keine oder mehrere **Follower**-Repliken (passive Replikation)
- Partitionen sind über die Broker im Cluster verteilt – siehe [[broker-architecture]]

### Ordnungsgarantien für Nachrichten {#message-ordering-guarantees}

**Kafka garantiert Ordnung nur innerhalb einer einzelnen Partition.** Es gibt keine globale Ordnung über Partitionen hinweg.

```yaml
Partition 0:  A -> B -> C        (order guaranteed: A before B before C)
Partition 1:  D -> E -> F        (order guaranteed: D before E before F)

Cross-partition: no guarantee on relative order of A vs D
```

Wenn du eine strikte Reihenfolge für eine Gruppe zusammengehöriger Records benötigst (z. B. alle Ereignisse eines einzelnen Benutzers), musst du sie mithilfe eines konsistenten Schlüssels in dieselbe Partition leiten.

Bei `max.in.flight.requests.per.connection > 1` (Standard: 5) kann es auch innerhalb einer Partition zu Out-of-Order-Auslieferung kommen, wenn Wiederholungsversuche stattfinden. Um die Reihenfolge pro Partition auch mit Wiederholungen zu garantieren:
- Verwende einen idempotenten Producer (`enable.idempotence=true`, seit Kafka 3.0 Standard) – dieser behandelt Umordnungen intern
- Oder setze `max.in.flight.requests.per.connection=1` (verringert den Durchsatz)

Siehe [[kafka-producer-fundamentals]] für die Konfiguration des idempotenten und transaktionalen Producers.

### Schlüsselbasiertes Partitionieren {#key-based-partitioning}

Der Producer bestimmt die Zielpartition für jeden Record:

**1. Nachrichten mit Schlüssel (DefaultPartitioner)**:

```python
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

# All records with key="user-42" go to the same partition
# Partition = murmur2(key_bytes) % num_partitions
producer.produce("user-events", key="user-42", value="login")
producer.produce("user-events", key="user-42", value="purchase")  # Same partition
producer.flush()
```

Der Standard-Partitioner wendet einen `murmur2`-Hash auf die serialisierten Schlüssel-Bytes an und bildet anschließend den Modulo mit der Partitionsanzahl. Das ist deterministisch: Derselbe Schlüssel wird immer auf dieselbe Partition abgebildet (solange sich die Partitionsanzahl nicht ändert).

**2. Null-Schlüssel = Round-Robin / Sticky**:

```python
# No key -> round-robin distribution (pre-2.4) or sticky partitioner (2.4+)
producer.produce("metrics", value="cpu=80%")
producer.produce("metrics", value="mem=60%")  # May go to a different partition
```

Seit Kafka 2.4 ist der **Sticky Partitioner** der Standard für Records ohne Schlüssel: Der Producer bleibt bei einer Partition, bis der aktuelle Batch voll ist oder `linger.ms` abläuft, und wechselt dann. Das verbessert die Batching-Effizienz gegenüber reinem Round-Robin.

**3. Eigener Partitioner**:

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

In Java:

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

### Partitionsspeicherung: Segmente {#partition-storage-segments}

Jede Partition wird als Verzeichnis im Log-Verzeichnis des Brokers gespeichert. Darin sind die Daten in **Segmente** aufgeteilt:

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

- Das **aktive Segment** ist dasjenige, in das gerade geschrieben wird
- Eine Segment-Rotation erfolgt, sobald `segment.bytes` (Standard: 1 GB) erreicht ist oder `segment.ms` (Standard: 7 Tage) verstrichen ist
- Nur **geschlossene (inaktive) Segmente** kommen für Löschung oder Komprimierung in Frage
- Kleinere Segmente = häufigere Bereinigung, aber mehr Dateihandles; größere Segmente = verzögerte Bereinigung

### Partitionsneuzuweisung {#partition-reassignment}

Partitionen können zwischen Brokern verschoben werden, etwa zum Lastausgleich oder bei der Außerbetriebnahme eines Brokers.

**Neuzuweisungsplan erzeugen**:
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

**Neuzuweisung ausführen**:
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

**Neuzuweisung drosseln**, um die Replikationsbandbreite zu begrenzen:
```bash
kafka-reassign-partitions.sh --execute \
  --reassignment-json-file reassignment.json \
  --throttle 50000000 \
  --bootstrap-server localhost:9092
# 50 MB/s throttle -- prevents reassignment from saturating network
```

### Wahl des bevorzugten Leaders {#preferred-leader-election}

Jede Partition hat einen **bevorzugten Leader** – den ersten Broker in der Replik-Liste. Im Laufe der Zeit können sich Leader verschieben (Broker-Neustarts, Ausfälle). Um die Leader-Verteilung neu auszugleichen:

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

`auto.leader.rebalance.enable=true` (Standard) löst eine automatische Wahl des bevorzugten Leaders aus, sobald das Leader-Ungleichgewicht `leader.imbalance.percentage.per.broker` (Standard: 10 %) überschreitet.

## Topic-Konfiguration {#topic-configuration}

### cleanup.policy {#cleanuppolicy}

Steuert, wie alte Daten aus einem Topic entfernt werden.

| Policy | Verhalten | Anwendungsfall |
|--------|-----------|----------------|
| `delete` (Standard) | Entfernt Segmente, die älter als `retention.ms` sind oder `retention.bytes` überschreiten | Ereignisströme, Logs, Metriken |
| `compact` | Behält nur den neuesten Wert pro Schlüssel; ein Tombstone (Null-Wert) entfernt den Schlüssel | Zustandssnapshots, Changelogs, Caches |
| `compact,delete` | Zuerst komprimieren, dann Segmente löschen, die älter als die Aufbewahrungszeit sind | Komprimierte Topics mit oberer Aufbewahrungsgrenze |

**Interna der Komprimierung**:
- Der Log-Cleaner-Thread durchsucht „dirty" (nicht komprimierte) Segmente
- Pro Schlüssel überlebt nur der Record mit dem höchsten Offset
- Ein **Tombstone** (Schlüssel mit Null-Wert) markiert einen Schlüssel zur Löschung; er wird nach `delete.retention.ms` (Standard: 24 h) entfernt
- `min.compaction.lag.ms` – Mindestzeit, bevor ein Record für die Komprimierung infrage kommt (verhindert, dass Records komprimiert werden, die Consumer noch nicht verarbeitet haben)
- `max.compaction.lag.ms` – maximale Zeit, nach der die Komprimierung garantiert ausgeführt wird
- `min.cleanable.dirty.ratio` (Standard: 0,5) – die Komprimierung startet, wenn 50 % oder mehr des Logs „dirty" sind

```bash
# Create a compacted topic
kafka-topics.sh --create --topic user-profiles \
  --partitions 6 --replication-factor 3 \
  --config cleanup.policy=compact \
  --config min.compaction.lag.ms=3600000 \
  --config delete.retention.ms=86400000 \
  --bootstrap-server localhost:9092
```

### Aufbewahrungskonfiguration {#retention-configuration}

| Parameter | Standard | Beschreibung |
|-----------|----------|--------------|
| `retention.ms` | 604800000 (7 Tage) | Zeitbasierte Aufbewahrung; `-1` = unbegrenzt |
| `retention.bytes` | -1 (unbegrenzt) | Größenbasierte Aufbewahrung pro Partition |
| `segment.bytes` | 1073741824 (1 GB) | Maximale Größe einer einzelnen Segmentdatei |
| `segment.ms` | 604800000 (7 Tage) | Maximale Zeit, bevor das aktive Segment rotiert wird |
| `min.compaction.lag.ms` | 0 | Mindestverzögerung, bevor ein Record komprimierbar ist |
| `max.compaction.lag.ms` | 9223372036854775807 | Maximale Verzögerung, bevor die Komprimierung läuft |
| `delete.retention.ms` | 86400000 (24 h) | Wie lange Tombstones nach der Komprimierung erhalten bleiben |
| `message.timestamp.type` | `CreateTime` | `CreateTime` (vom Producer gesetzt) oder `LogAppendTime` (vom Broker gesetzt) |

Die Aufbewahrung wird pro Segment ausgewertet, nicht pro Record. Ein Segment wird gelöscht, wenn **alle** Records darin die Aufbewahrungsgrenze überschreiten.

## Praxismuster {#practical-patterns}

### kafka-topics.sh-Befehle {#kafka-topicssh-commands}

**Topic erstellen**:
```bash
kafka-topics.sh --create --topic orders \
  --partitions 12 --replication-factor 3 \
  --config retention.ms=259200000 \
  --config cleanup.policy=delete \
  --bootstrap-server kafka1:9092
```

**Topic beschreiben** (Partitionen, Replikate, ISR, Konfigurationen):
```bash
kafka-topics.sh --describe --topic orders \
  --bootstrap-server kafka1:9092

# Output:
# Topic: orders  PartitionCount: 12  ReplicationFactor: 3  Configs: retention.ms=259200000
#   Topic: orders  Partition: 0  Leader: 1  Replicas: 1,2,3  Isr: 1,2,3
#   Topic: orders  Partition: 1  Leader: 2  Replicas: 2,3,1  Isr: 2,3,1
#   ...
```

**Alle Topics auflisten**:
```bash
kafka-topics.sh --list --bootstrap-server kafka1:9092

# Exclude internal topics
kafka-topics.sh --list --exclude-internal --bootstrap-server kafka1:9092
```

**Partitionsanzahl ändern** (nur erhöhen):
```bash
kafka-topics.sh --alter --topic orders --partitions 24 \
  --bootstrap-server kafka1:9092
# WARNING: breaks key-based partition assignment for existing keys
```

**Topic-Konfigurationen ändern**:
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

**Topic löschen**:
```bash
kafka-topics.sh --delete --topic orders \
  --bootstrap-server kafka1:9092
# Requires delete.topic.enable=true on broker (default: true since Kafka 1.0)
# Deletion is asynchronous -- data is removed in the background
```

### Programmatische Topic-Verwaltung (Python) {#programmatic-topic-management-python}

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

### Heuristik zur Wahl der Partitionsanzahl {#partition-count-selection-heuristic}

```yaml
Target throughput:    100 MB/s
Per-partition write:  ~10 MB/s (single partition, single producer)
Consumer instances:   8 (in one consumer group)

Minimum partitions = max(100/10, 8) = 10
Recommended:         12 (round up, leave room for growth)
```

Beginne mit wenigen Partitionen und erhöhe sie später. Du kannst die Partitionsanzahl nicht verringern, ohne das Topic neu anzulegen.

## Stolperfallen {#gotchas}

- **Das Erhöhen der Partitionen bricht die Schlüsselzuordnung.** `murmur2(key) % 12` != `murmur2(key) % 24`. Nach einer Erhöhung der Partitionen können Records mit demselben Schlüssel in unterschiedlichen Partitionen landen. Wenn die Reihenfolge wichtig ist, plane die Partitionsanzahl von Anfang an oder verwende einen eigenen Partitioner, der das Wachstum berücksichtigt.
- **Die Partitionsanzahl kann nicht verringert werden.** Die einzige Möglichkeit ist, ein neues Topic mit weniger Partitionen anzulegen und die Daten mit MirrorMaker, Kafka Connect oder einer Consumer-Producer-Brücke zu migrieren.
- **Komprimierung erfordert Schlüssel ungleich null.** Wenn `cleanup.policy=compact` gesetzt ist, muss jeder Record einen Schlüssel haben. Records ohne Schlüssel führen dazu, dass die Komprimierung diese Records vollständig überspringt.
- **Das aktive Segment wird nie gelöscht oder komprimiert.** Aufbewahrung und Komprimierung gelten nur für geschlossene Segmente. Bei `segment.bytes=1GB` und 500 MB Schreibvolumen pro Tag rotiert das aktive Segment erst nach etwa 2 Tagen, wodurch sich die Bereinigung verzögert.
- **Das Löschen von Topics ist asynchron und kann Zustand hinterlassen.** Nach `--delete` werden Partitionen zur Löschung markiert, die eigentliche Datenentfernung erfolgt im Hintergrund. Der Topic-Name ist sofort nicht mehr verfügbar, der Festplattenspeicher wird jedoch erst später freigegeben.
- **`retention.bytes` gilt pro Partition, nicht pro Topic.** Ein Topic mit 12 Partitionen und `retention.bytes=1GB` kann insgesamt bis zu 12 GB behalten.
- **Unsaubere Leader-Wahl birgt Datenverlustrisiken.** Ist `unclean.leader.election.enable=true` gesetzt (Standard: false seit Kafka 0.11), kann eine nicht synchronisierte Replik zum Leader werden und dabei nicht replizierte Nachrichten verlieren.
- **Partitionsübergreifende Joins erfordern Ko-Partitionierung.** Wenn du zwei Topics anhand des Schlüssels joinen möchtest, müssen beide dieselbe Partitionsanzahl haben und denselben Partitioner verwenden. Die Anforderungen an `RangeAssignor` findest du unter [[consumer-groups]].

## Kurzreferenz {#quick-reference}

### Wichtige Konfiguration auf Topic-Ebene {#key-topic-level-configuration}

| Parameter | Standard | Beschreibung |
|-----------|----------|--------------|
| `cleanup.policy` | `delete` | `delete`, `compact` oder `compact,delete` |
| `retention.ms` | 604800000 (7d) | Zeitbasierte Aufbewahrung |
| `retention.bytes` | -1 | Größenbasierte Aufbewahrung pro Partition |
| `segment.bytes` | 1073741824 (1GB) | Größe der Segmentdatei |
| `segment.ms` | 604800000 (7d) | Maximales Alter des aktiven Segments |
| `min.compaction.lag.ms` | 0 | Mindestverzögerung bis zur Komprimierbarkeit |
| `max.compaction.lag.ms` | MAX_LONG | Maximale Verzögerung bis zur erzwungenen Komprimierung |
| `delete.retention.ms` | 86400000 (24h) | TTL von Tombstones nach der Komprimierung |
| `min.cleanable.dirty.ratio` | 0.5 | Anteil dirty Log, der die Komprimierung auslöst |
| `max.message.bytes` | 1048588 (~1MB) | Maximale Record-Größe für dieses Topic |
| `min.insync.replicas` | 1 | ISR-Anzahl, die für `acks=all` erforderlich ist |
| `unclean.leader.election.enable` | false | Nicht synchronisierte Replik als Leader erlauben |
| `message.timestamp.type` | `CreateTime` | `CreateTime` oder `LogAppendTime` |

### Wichtige CLI-Befehle {#essential-cli-commands}

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

## Offizielle Dokumentation {#official-documentation}

- [Topics and Logs](https://kafka.apache.org/documentation/#intro_topics) – Kernmodell von Topics und Partitionen
- [Topic-Level Configs](https://kafka.apache.org/documentation/#topicconfigs) – vollständige Konfigurationsreferenz
- [Log Compaction](https://kafka.apache.org/documentation/#compaction) – Semantik und Garantien der Komprimierung
- [Operations: Adding/Removing Topics](https://kafka.apache.org/documentation/#basic_ops_add_topic) – Verwaltung über die CLI
- [Partition Reassignment](https://kafka.apache.org/documentation/#basic_ops_partitionassignment) – Neuverteilung von Partitionen über Broker

## Siehe auch {#see-also}

- [[broker-architecture]] – wie Partitionen auf Broker abgebildet werden, ISR, Controller-Wahl
- [[consumer-groups]] – Strategien zur Partitionszuweisung, Rebalancing, Offset-Verwaltung
- [[kafka-producer-fundamentals]] – Schlüsselserialisierung, Batching, acks
- [[kafka-producer-advanced-patterns]] – idempotenter Producer, eigene Partitioner
- [[kafka-cluster-management]] – tägliche Verwaltung von Topics und Cluster
