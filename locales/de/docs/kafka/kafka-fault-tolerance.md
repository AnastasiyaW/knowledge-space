---
level: 3
source_sha256: 643161c87218e252c764ab1a0d39d3d19d8647ca0465e53976050c2c88b19986
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Fehlertoleranz {#kafka-fault-tolerance}

Unclean Leader Election, Preferred Replica Election, Observer Replicas, rack-aware Replikation, Multi-Datacenter-Muster, Fehlerszenarien mit Wiederherstellungsverfahren sowie Metriken zum Replikationszustand.

Zum Replikationsmodell, ISR, HW/LEO und dem Zusammenspiel von acks siehe [[kafka-replication-fundamentals]].

## Unclean Leader Election {#unclean-leader-election}

Wenn alle ISR-Replikate ausgefallen sind, steht Kafka vor einer Wahl: **Verfügbarkeit gegen Datenintegrität**.

```properties
# Broker config (default: false since Kafka 0.11.0.0)
unclean.leader.election.enable=false
```

| Einstellung | Verhalten | Abwägung |
|-------------|-----------|----------|
| `false` (Standard) | Die Partition bleibt offline, bis ein ISR-Mitglied wieder verfügbar ist | **Kein Datenverlust**, aber Nichtverfügbarkeit |
| `true` | Ein nicht synchronisiertes Replikat kann Leader werden | **Datenverlust** (nicht replizierte Nachrichten sind verloren), aber Verfügbarkeit |

**Wann Unclean Leader Election aktiviert werden sollte:**
- Metriken, Logs und Clickstream-Daten, bei denen Verfügbarkeit wichtiger ist als Dauerhaftigkeit
- Topics, die sich aus Quellsystemen neu aufbauen lassen
- **Niemals** für Finanztransaktionen, Bestellungen oder Audit-Logs

```bash
# Set per-topic for granular control
kafka-configs.sh --alter --topic clickstream \
  --add-config unclean.leader.election.enable=true \
  --bootstrap-server localhost:9092

# Keep default (false) for critical topics
kafka-configs.sh --alter --topic payments \
  --add-config unclean.leader.election.enable=false \
  --bootstrap-server localhost:9092
```

### Mechanik des Datenverlusts bei Unclean Election {#data-loss-mechanics-with-unclean-election}

```text
Leader (Broker 0):    [0] [1] [2] [3] [4] [5] [6] [7]   LEO=8, HW=6
Follower (Broker 1):  [0] [1] [2] [3] [4] [5]            LEO=6  (in ISR)
Follower (Broker 2):  [0] [1] [2] [3]                     LEO=4  (out of ISR)

Broker 0 and Broker 1 crash simultaneously.

unclean.leader.election.enable=false:
  Partition offline. Wait for Broker 0 or 1 to recover.

unclean.leader.election.enable=true:
  Broker 2 becomes leader with LEO=4.
  Messages at offsets 4,5 (committed!) are LOST.
  Messages at offsets 6,7 (uncommitted) are LOST.
  New writes start at offset 4.
```

## Preferred Replica Election {#preferred-replica-election}

Kafka weist jeder Partition einen **bevorzugten Leader** zu (den ersten Broker in der Replikatliste). Nach Ausfällen und Wiederherstellungen kann die Leadership jedoch so verschoben sein, dass einige Broker deutlich mehr Leader-Last tragen als andere.

```bash
# Check current vs preferred leaders
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Replicas: 1,2,3  <-- first in list (1) is preferred leader
# Leader: 2        <-- actual leader is 2 (leadership drifted)

# Trigger preferred replica election
kafka-leader-election.sh --election-type PREFERRED \
  --topic orders --partition 0 \
  --bootstrap-server localhost:9092

# Auto-balance (broker config)
auto.leader.rebalance.enable=true           # default: true
leader.imbalance.check.interval.seconds=300 # default: 300 (5 min)
leader.imbalance.per.broker.percentage=10   # default: 10%
```

**So funktioniert das automatische Rebalancing:**
1. In jedem Intervall `leader.imbalance.check.interval.seconds` prüft der Controller jeden Broker.
2. Übersteigt das Leader-Ungleichgewicht eines Brokers `leader.imbalance.per.broker.percentage`, löst der Controller Preferred-Leader-Elections aus.
3. Dies funktioniert nur, wenn der bevorzugte Leader in der ISR ist.

## Observer Replicas (KIP-392) {#observer-replicas-kip-392}

Observer Replicas sind **nicht stimmberechtigte** Replikate. Sie repliziere Daten, werden aber **nie in die ISR aufgenommen** und sind **nie für eine Leader-Wahl berechtigt**. Sie bedienen ausschließlich lesende Consumer-Fetches.

```text
Producer --> Leader (Broker 0, DC-East)
                |
         +------+------+
         v             v
    Follower       Observer
    (Broker 1,     (Broker 3,
     DC-East)      DC-West)
     [ISR]         [NOT in ISR, never votes]
```

Anwendungsfälle:
- **Cross-DC-Lesezugriffe**: Consumer in DC-West lesen vom lokalen Observer.
- **Entlastung des Lesetraffics**: Der Observer übernimmt Consumer-Fetches, ohne ISR oder Schreiblatenz zu beeinflussen.
- **Analyse-Workloads**: Lastintensive Consumer wirken sich nicht auf die produktiven Replikate aus.

```properties
# Consumer config to fetch from closest replica (including observers)
client.rack=dc-west
# Broker config
broker.rack=dc-east

# Replica placement (topic config)
replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector
```

**Einschränkung**: Observer Replicas können dem Leader hinterherhinken. Consumer, die von Observern lesen, erhalten **eventuell konsistente** Daten.

## Rack-Aware Replikation {#rack-aware-replication}

`broker.rack` teilt Kafka mit, zu welcher Fehlerdomäne (Rack, AZ, Datacenter) ein Broker gehört. Der Algorithmus zur Partitionszuweisung sorgt dafür, dass Replikate über Racks verteilt werden.

```properties
# Broker configs
# Broker 0 (AZ-a)
broker.rack=us-east-1a
# Broker 1 (AZ-b)
broker.rack=us-east-1b
# Broker 2 (AZ-c)
broker.rack=us-east-1c
```

Mit aktivierter Rack-Awareness verteilt sich ein Topic mit RF=3 auf einem 6-Broker-Cluster über 3 AZs so:

```text
Partition 0: Broker 0 (AZ-a), Broker 3 (AZ-b), Broker 5 (AZ-c)
Partition 1: Broker 1 (AZ-b), Broker 4 (AZ-c), Broker 2 (AZ-a)

Each partition has one replica per AZ -- survives full AZ failure.
```

Ohne `broker.rack` kann Kafka alle Replikate in derselben AZ platzieren. Fällt diese AZ aus, ist das fatal.

```bash
# Verify rack-aware placement
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Cross-reference broker IDs with their broker.rack setting
```

## Multi-Datacenter-Muster {#multi-datacenter-patterns}

### Muster 1: Stretch Cluster {#pattern-1-stretch-cluster}

Ein einzelner Kafka-Cluster erstreckt sich über 2 bis 3 Datacenter, verbunden über ein Netzwerk mit niedriger Latenz.

```text
DC-East                         DC-West
+----------+                    +----------+
| Broker 0 |<--- replication -->| Broker 3 |
| Broker 1 |      (sync)       | Broker 4 |
| Broker 2 |                    | Broker 5 |
+----------+                    +----------+
```

**Voraussetzungen:**
- Round-Trip-Latenz < 50 ms zwischen den DCs (idealerweise < 10 ms)
- `broker.rack` auf den DC-Namen gesetzt
- RF=4, min.insync.replicas=3 bei 2 DCs; RF=3, min.insync.replicas=2 bei 3 DCs

### Muster 2: MM2 Active-Passive {#pattern-2-mm2-active-passive}

Separate Kafka-Cluster pro DC. MM2 repliziert Topics asynchron.

### Muster 3: MM2 Active-Active {#pattern-3-mm2-active-active}

Beide Cluster nehmen Schreibzugriffe an. MM2 repliziert bidirektional. Ein Topic-Namespace verhindert Schleifen.

### Vergleich der Muster {#pattern-comparison}

| Kriterium | Stretch Cluster | MM2 Active-Passive | MM2 Active-Active |
|-----------|-----------------|--------------------|-------------------|
| DC-Latenz | < 50 ms erforderlich | Beliebig | Beliebig |
| Schreiblatenz | Höher (DC-übergreifend) | Lokal | Lokal |
| Failover | Automatisch (ISR) | Manuell | Manuell |
| Exactly-once | Ja | Nein (asynchrone Lücke) | Nein |
| Komplexität | Gering | Mittel | Hoch |
| Datenverlust bei DC-Ausfall | Keiner (wenn die ISR DCs umspannt) | Möglich | Möglich |

Für die detaillierte MM2-Konfiguration und die Failover-Verfahren siehe [[kafka-backup-and-dr]].

## Fehlerszenarien und Wiederherstellung {#failure-scenarios-and-recovery}

### Szenario 1: Ausfall eines einzelnen Brokers (RF=3, min.insync.replicas=2) {#scenario-1-single-broker-failure-rf3-mininsyncreplicas2}

```yaml
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 crashes
After:  Controller elects Broker 1 as leader (next in ISR)
        ISR={1,2}, writes continue normally
        When Broker 0 recovers, it joins as follower, catches up, rejoins ISR
```

Kein Datenverlust. Keine Ausfallzeit. Automatische Wiederherstellung.

### Szenario 2: Ausfall zweier Broker (RF=3, min.insync.replicas=2) {#scenario-2-two-broker-failures-rf3-mininsyncreplicas2}

```yaml
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 and Broker 1 crash
After:  Controller elects Broker 2 as leader
        ISR={2} -- below min.insync.replicas=2
        Reads work. Writes FAIL with NotEnoughReplicasException.
        Writes resume when any other broker recovers and joins ISR.
```

Kein Datenverlust. Schreibzugriffe sind bis zur Wiederherstellung blockiert.

### Szenario 3: Leader-Absturz mit nicht replizierten Daten {#scenario-3-leader-crash-with-unreplicated-data}

```yaml
Before: Leader LEO=100, HW=95, Follower LEO=95
Event:  Leader crashes (offsets 95-99 not replicated)
After:  Follower becomes leader with LEO=95
        Offsets 95-99 LOST (were uncommitted)
        Producers with acks=all never received ACK for 95-99
        Producers with acks=1 DID receive ACK -- DATA LOSS for those messages
```

Deshalb ist `acks=all` für Dauerhaftigkeit unverzichtbar.

### Szenario 4: Vollständiger Cluster-Neustart {#scenario-4-full-cluster-restart}

```bash
# Rolling restart procedure (zero downtime):
# 1. Stop broker (leadership migrates to ISR members)
# 2. Upgrade/config change
# 3. Start broker (rejoins cluster, catches up, rejoins ISR)
# 4. Wait for under-replicated partitions to reach 0
# 5. Repeat for next broker

kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server localhost:9092
# Wait until output is empty before proceeding to next broker
```

```properties
# Controlled shutdown config
controlled.shutdown.enable=true          # default: true
controlled.shutdown.max.retries=3
controlled.shutdown.retry.backoff.ms=5000
```

## Zentrale Metriken für den Replikationszustand {#key-metrics-for-replication-health}

```text
# Broker level
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions     # TARGET: 0
kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount      # TARGET: 0
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec               # Alert on sustained > 0
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
kafka.server:type=ReplicaManager,name=FailedIsrUpdatesPerSec         # TARGET: 0
kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec

# Partition level
kafka.cluster:type=Partition,name=UnderReplicated,topic=*,partition=*
kafka.log:type=Log,name=LogEndOffset,topic=*,partition=*

# Controller
kafka.controller:type=KafkaController,name=OfflinePartitionsCount    # TARGET: 0
kafka.controller:type=KafkaController,name=ActiveControllerCount     # TARGET: 1
kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs
```

**Alarmschwellen:**
- `UnderReplicatedPartitions > 0` länger als 5 Minuten: Problem mit der Broker-Gesundheit
- `OfflinePartitionsCount > 0`: sofortiger Alarm, Partitionen sind nicht verfügbar
- Anhaltend erhöhtes `IsrShrinksPerSec`: Plattenes I/O, Netzwerk und GC auf den betroffenen Brokern prüfen
- `UnderMinIsrPartitionCount > 0`: Schreibvorgänge für die betroffenen Partitionen schlagen fehl

## Stolperfallen {#gotchas}

- **Unclean Leader Election kann bestätigte Daten verlieren.** Nachrichten, die vollständig in die ISR repliziert wurden, können verloren gehen, wenn das einzige verbliebene Replikat nicht synchron war. Dabei geht es nicht nur um "nicht bestätigte" Daten.
- **Automatisches Leader-Rebalancing funktioniert nur, wenn der bevorzugte Leader in der ISR ist.** Ist er zurückgefallen, wartet das Rebalancing, bis er aufgeholt hat. Eine erzwungene Election findet nicht statt.
- **Observer Replicas erhöhen die Replikationslast, bieten aber keine zusätzliche Dauerhaftigkeit.** Sie holen Daten wie reguläre Follower vom Leader und belegen Netzwerkbandbreite. Dimensionieren Sie das Netzwerk entsprechend.
- **Rack-Aware-Platzierung erfordert `broker.rack` auf ALLEN Brokern.** Fehlt es auf einigen Brokern, ignoriert Kafka die Rack-Awareness für die betroffenen Topics vollständig.

## Siehe auch {#see-also}

- [[kafka-replication-fundamentals]] - ISR, HW/LEO, Matrix aus acks und min.insync.replicas
- [[kafka-backup-and-dr]] - MirrorMaker-2-Konfiguration, Verfahren zur Disaster Recovery
- [[broker-architecture]] - Controller-Wahl, KRaft, Broker-Interna
- [[topics-and-partitions]] - Partitionszuweisung, Log-Segmente
- [[kafka-cluster-management]] - Rolling Upgrades, Partition Reassignment
