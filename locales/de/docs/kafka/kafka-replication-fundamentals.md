---
level: 3
source_sha256: 0b7ac6a1c24d3df59145a7d158cb0f7219d4cadd106e594cc10e0aff591c470f
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Replikationsgrundlagen {#kafka-replication-fundamentals}

Leader-Follower-Replikationsmodell, Empfehlungen zum Replikationsfaktor, ISR-Mechanik, High Watermark (HW) vs. Log End Offset (LEO), Leader Epoch, committete vs. nicht committete Nachrichten sowie das Zusammenspiel von acks und min.insync.replicas.

## Leader-Follower-Replikationsmodell {#leader-follower-replication-model}

### Funktionsweise {#how-it-works}

```text
Producer --produce--> Broker 0 (Leader, Partition 0)
                         |
                    fetch request
                    (follower pull)
                         |
                   +-----+-----+
                   v           v
              Broker 1      Broker 2
             (Follower)    (Follower)
```

- Follower senden `Fetch`-Anfragen an den Leader. Diese entsprechen den Consumer-Fetches, laufen aber über einen separaten Replikationskanal.
- Follower schreiben die abgerufenen Daten in der gleichen Reihenfolge in ihren eigenen lokalen Log.
- Es gibt **kein Push** vom Leader zu den Followern. Die Follower pullen in ihrem eigenen Tempo.
- Die Leadership wird pro Partition vergeben. Ein Broker ist in der Regel für einige Partitionen Leader und für andere Follower.
- Der Controller (ZooKeeper oder KRaft-Quorum) weist die Leadership zu; siehe [[broker-architecture]].

### Replikationsfaktor {#replication-factor}

Wird beim Erstellen des Topics festgelegt. Er kann nicht über die Anzahl der Broker hinaus erhöht werden.

```bash
# Create topic with replication factor 3
kafka-topics.sh --create --topic orders \
  --partitions 12 --replication-factor 3 \
  --bootstrap-server localhost:9092

# Verify replica assignment
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Output:
# Topic: orders  Partition: 0  Leader: 1  Replicas: 1,2,3  Isr: 1,2,3
```

**Empfehlungen nach Anwendungsfall:**

| Anwendungsfall | Replikationsfaktor | min.insync.replicas | Begründung |
|----------------|-------------------|---------------------|------------|
| Entwicklung/Test | 1 | 1 | Keine Dauerhaftigkeit erforderlich |
| Standard-Produktion | 3 | 2 | Toleriert den Ausfall eines Brokers, kein Datenverlust |
| Kritische Finanzdaten | 3 | 2 | Wie oben, aber mit erzwungenem `acks=all` |
| Großer Cluster (>10 Broker) | 3 | 2 | RF=3 ist ausreichend; RF=5 verschwendet Plattenplatz |
| Multi-AZ (3 AZs) | 3 | 2 | Eine Replik pro AZ, übersteht den Totalausfall einer AZ |
| Stretch-Cluster über zwei Rechenzentren | 4 | 3 | 2 Repliken pro RZ, übersteht den Totalausfall eines RZ |

RF=2 ist ein häufiger Fehler. Bei `min.insync.replicas=2` macht der Ausfall eines einzigen Followers die Partition schreibgeschützt. Bei `min.insync.replicas=1` riskiert der Verlust eines einzigen Brokers Datenverlust. **In der Produktion immer RF >= 3 verwenden.**

## In-Sync Replicas (ISR) {#in-sync-replicas-isr}

Die ISR-Menge ist die Teilmenge der Repliken, die als „aufgeholt“ mit dem Leader gelten. Nur ISR-Mitglieder kommen für die Leader-Wahl infrage (sofern nicht `unclean.leader.election.enable=true` gesetzt ist).

### Kriterien für die ISR-Mitgliedschaft {#isr-membership-criteria}

Eine Replik bleibt in der ISR, solange sie:
1. innerhalb von `replica.lag.time.max.ms` (Standard: 30000 ms = 30 s) bis zum Log End Offset (LEO) des Leaders aufgeholt hat und
2. eine aktive Sitzung mit dem Controller unterhält (Heartbeats).

```properties
# Key broker configs controlling ISR behavior
replica.lag.time.max.ms=30000        # Max time before follower is removed from ISR
```

**Ablauf beim Schrumpfen und Wachsen der ISR:**

```text
t=0:  ISR = {0, 1, 2}     # All replicas caught up
t=5:  Broker 2 goes slow (GC pause, disk I/O, network)
t=35: Broker 2 hasn't fetched within 30s
      Leader removes Broker 2 from ISR
      ISR = {0, 1}         # Shrunk ISR
t=40: Broker 2 catches up, fetches to leader's LEO
      Leader adds Broker 2 back to ISR
      ISR = {0, 1, 2}     # Expanded ISR
```

**Die Überwachung von ISR-Schrumpfungen** ist entscheidend, denn sie zeigt Probleme mit dem Zustand der Broker an, bevor es zu Ausfällen kommt.

```bash
# Check under-replicated partitions (ISR < replication factor)
kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server localhost:9092

# JMX metrics to monitor
# kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions  (should be 0)
# kafka.server:type=ReplicaManager,name=IsrShrinksPerSec
# kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
```

## High Watermark (HW) vs. Log End Offset (LEO) {#high-watermark-hw-vs-log-end-offset-leo}

Zwei Offset-Marker bestimmen, welche Daten sichtbar sind und welche repliziert werden:

```yaml
Partition Log (Leader):

Offset:  0   1   2   3   4   5   6   7   8
         [A] [B] [C] [D] [E] [F] [G] [H] [I]
                           ^               ^
                           HW              LEO
                           (committed)     (latest written)

Messages 0-4: committed (replicated to all ISR members)
Messages 5-8: uncommitted (only on leader, not yet fully replicated)
```

| Konzept | Definition | Wer pflegt es? |
|---------|-----------|----------------|
| **LEO (Log End Offset)** | Offset der nächsten zu schreibenden Nachricht. Jede Replik hat ihren eigenen LEO. | Jede Replik unabhängig |
| **HW (High Watermark)** | Der höchste Offset, der auf **alle** ISR-Mitglieder repliziert wurde. Nur Nachrichten unterhalb der HW sind für Consumer sichtbar. | Der Leader berechnet ihn und verteilt ihn über Fetch-Antworten an die Follower |

### So rückt die HW vor {#how-hw-advances}

1. Der Producer schreibt die Nachricht mit Offset 8 auf den Leader. LEO des Leaders = 9.
2. Follower 1 holt Daten bis Offset 8. LEO von Follower 1 = 9.
3. Follower 2 holt Daten bis Offset 8. LEO von Follower 2 = 9.
4. Der Leader stellt fest, dass alle ISR-Mitglieder einen LEO >= 9 haben, und setzt die HW auf 9.
5. Die nächsten Fetch-Antworten übermitteln den neuen HW-Wert an die Follower.

**Sichtbarkeit für Consumer**: Consumer können nur bis `HW - 1` lesen. So wird verhindert, dass sie Daten lesen, die verloren gehen könnten, falls der Leader abstürzt, bevor die Follower sie repliziert haben.

### Leader Epoch (KIP-101) {#leader-epoch-kip-101}

Die **Leader Epoch** ist eine streng monoton steigende Ganzzahl, die sich jedes Mal erhöht, wenn für eine Partition ein neuer Leader gewählt wird. Sie löst das Problem der **Log-Divergenz**:

```text
Scenario without leader epoch:
1. Leader (Broker 0) writes offset 5, HW=4 (follower hasn't fetched yet)
2. Leader crashes
3. Follower (Broker 1) becomes leader, HW=4, LEO=5
4. New leader writes a DIFFERENT message at offset 5
5. Old leader comes back -- its offset 5 conflicts

With leader epoch:
- Each leader election bumps epoch: epoch 0 -> epoch 1
- Recovering broker asks new leader: "What was the LEO at end of epoch 0?"
- New leader responds: "LEO was 5 at epoch 0"
- Recovering broker truncates its log to offset 5, then fetches from new leader
- No divergence
```

```properties
# Leader epoch checkpoint file on each broker (automatic, no config needed)
# $LOG_DIR/leader-epoch-checkpoint
# Format: leader_epoch start_offset
# 0  0
# 1  5
# 2  12
```

## Committete vs. nicht committete Nachrichten {#committed-vs-uncommitted-messages}

Eine Nachricht gilt als **committet**, wenn sie auf alle ISR-Repliken repliziert wurde. Nur committete Nachrichten können konsumiert werden.

### Interaktionsmatrix von acks und min.insync.replicas {#acks-mininsyncreplicas-interaction-matrix}

Dies ist die wichtigste Konfigurationsmatrix für die Dauerhaftigkeit in Kafka:

```properties
# Producer config
acks=all                  # -1 is equivalent
# Broker/topic config
min.insync.replicas=2     # Minimum ISR members to accept a write
```

| acks | min.insync.replicas | RF | Verhalten |
|------|--------------------|----|-----------|
| `0` | beliebig | beliebig | Der Producer wartet nicht auf ein ACK. Maximaler Durchsatz, keine Garantie für Dauerhaftigkeit. |
| `1` | beliebig | beliebig | Der Producer wartet nur auf das ACK des Leaders. Datenverlust, wenn der Leader ausfällt, bevor repliziert wurde. |
| `all` | `1` | 3 | Die ISR kann auf den Leader allein schrumpfen. Dann ist `acks=all` gleich `acks=1`. **Trügerische Sicherheit.** |
| `all` | `2` | 3 | Die ISR muss mindestens 2 Mitglieder haben, sonst werden Schreibvorgänge abgelehnt. **Empfohlene Produktionseinstellung.** |
| `all` | `3` | 3 | Der Ausfall eines beliebigen Brokers blockiert Schreibvorgänge. **Für die meisten Anwendungsfälle zu strikt.** |

**Die goldene Regel**: `acks=all` + `min.insync.replicas=2` + `replication.factor=3`.

### Was passiert, wenn die ISR unter min.insync.replicas fällt {#what-happens-when-isr-shrinks-below-mininsyncreplicas}

```yaml
Scenario: RF=3, min.insync.replicas=2, acks=all

1. Normal: ISR={0,1,2}, writes succeed
2. Broker 2 dies: ISR={0,1}, writes succeed (2 >= min.insync)
3. Broker 1 dies: ISR={0}, writes FAIL with NotEnoughReplicasException
   - Partition is READABLE but NOT WRITABLE
   - Consumers continue reading committed data
4. Broker 1 returns: ISR={0,1}, writes resume
```

## Konfigurationsreferenz {#configuration-reference}

### Replikationskonfiguration auf Broker-Ebene {#broker-level-replication-configs}

```properties
# --- ISR ---
replica.lag.time.max.ms=30000           # Follower removed from ISR after this lag
min.insync.replicas=2                    # Cluster-wide default (override per topic)

# --- Replication threads ---
num.replica.fetchers=1                   # Threads per broker for fetching from leaders
replica.fetch.max.bytes=1048576          # 1MB max fetch per partition per request
replica.fetch.wait.max.ms=500            # Max wait before fetch returns
replica.socket.timeout.ms=30000          # Socket timeout for replication fetches
replica.socket.receive.buffer.bytes=65536

# --- Leader election ---
unclean.leader.election.enable=false     # NEVER set true for critical topics
auto.leader.rebalance.enable=true        # Periodic preferred leader election
leader.imbalance.check.interval.seconds=300
leader.imbalance.per.broker.percentage=10

# --- Log recovery ---
log.recovery.threads.per.data.dir=1
unclean.shutdown.recovery.enable=true
```

### Überschreibungen auf Topic-Ebene {#topic-level-overrides}

```bash
# Set replication configs per topic
kafka-configs.sh --alter --topic payments \
  --add-config min.insync.replicas=2,unclean.leader.election.enable=false \
  --bootstrap-server localhost:9092

# Increase replication factor of existing topic (reassignment)
cat > reassignment.json << 'EOF'
{
  "version": 1,
  "partitions": [
    {"topic": "orders", "partition": 0, "replicas": [1, 2, 3]},
    {"topic": "orders", "partition": 1, "replicas": [2, 3, 1]},
    {"topic": "orders", "partition": 2, "replicas": [3, 1, 2]}
  ]
}
EOF

kafka-reassign-partitions.sh --reassignment-json-file reassignment.json \
  --execute --bootstrap-server localhost:9092
```

## Stolperfallen {#gotchas}

- **RF=2 ist eine Falle.** Bei `min.insync.replicas=2` macht der Ausfall eines einzigen Followers die Partition schreibgeschützt. Bei `min.insync.replicas=1` genügt ein Absturz eines Brokers für Datenverlust. Immer RF >= 3 verwenden.
- **`acks=all` mit `min.insync.replicas=1` ist trügerische Sicherheit.** Wenn die ISR auf den Leader allein schrumpft, wird `acks=all` zu `acks=1`, also ohne Bestätigung der Replikation.
- **ISR-Schrumpfungen werden oft durch GC-Pausen verursacht, nicht durch Broker-Ausfälle.** Prüfen Sie GC-Logs und `replica.lag.time.max.ms`, bevor Sie ein Hardwareproblem annehmen.
- **Die Weitergabe der HW erfolgt verzögert.** Der Leader aktualisiert die HW, die Follower erfahren davon aber erst mit der nächsten Fetch-Antwort. Es gibt kurze Zeitfenster, in denen Follower Daten oberhalb ihrer lokalen HW haben.

## Siehe auch {#see-also}

- [[kafka-fault-tolerance]] – Ausfallszenarien, Unclean Leader Election, rack-bewusste Replikation, Multi-DC-Muster
- [[broker-architecture]] – Controller-Wahl, KRaft, Broker-Interna
- [[topics-and-partitions]] – Partitionszuweisung, Log-Segmente, Compaction
- [[kafka-cluster-management]] – Rolling Upgrades, Reassignment, Monitoring
- [[kafka-producer-fundamentals]] – acks-Modi aus Sicht des Producers
