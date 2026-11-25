---
level: 3
source_sha256: 0b7ac6a1c24d3df59145a7d158cb0f7219d4cadd106e594cc10e0aff591c470f
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de la réplication Kafka {#kafka-replication-fundamentals}

Modèle de réplication leader-follower, recommandations sur le facteur de réplication, mécanique de l'ISR, High Watermark (HW) et Log End Offset (LEO), epoch de leader, messages committed et uncommitted, et interaction entre `acks` et `min.insync.replicas`.

## Modèle de réplication leader-follower {#leader-follower-replication-model}

### Fonctionnement {#how-it-works}

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

- Les followers émettent des requêtes `Fetch` vers le leader, identiques aux fetches des consommateurs mais sur un canal de réplication distinct
- Les followers écrivent les données récupérées dans leur propre log local, dans le même ordre
- Il n'y a **aucun push** du leader vers les followers : les followers tirent les données à leur propre rythme
- Le leadership est défini par partition : un même broker est généralement leader pour certaines partitions et follower pour d'autres
- Le controller (ZooKeeper ou quorum KRaft) attribue le leadership ; voir [[broker-architecture]]

### Facteur de réplication {#replication-factor}

Défini à la création du topic. Ne peut pas être augmenté au-delà du nombre de brokers.

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

**Recommandations par cas d'usage :**

| Cas d'usage | Facteur de réplication | min.insync.replicas | Justification |
|----------|-------------------|---------------------|-----------|
| Dev/test | 1 | 1 | Pas de durabilité requise |
| Production standard | 3 | 2 | Tolère la panne d'un broker, aucune perte de données |
| Données financières critiques | 3 | 2 | Identique, mais avec `acks=all` imposé |
| Grand cluster (>10 brokers) | 3 | 2 | RF=3 suffit ; RF=5 gaspille du disque |
| Multi-AZ (3 AZ) | 3 | 2 | Une réplique par AZ, survit à la perte complète d'une AZ |
| Stretch sur deux datacenters | 4 | 3 | 2 répliques par DC, survit à la perte complète d'un DC |

RF=2 est une erreur fréquente. Avec `min.insync.replicas=2`, la panne d'un seul follower rend la partition en lecture seule. Avec `min.insync.replicas=1`, la perte d'un seul broker risque de provoquer une perte de données. **Utilisez toujours RF >= 3 en production.**

## In-Sync Replicas (ISR) {#in-sync-replicas-isr}

L'ISR est le sous-ensemble des répliques considérées comme « à jour » par rapport au leader. Seuls les membres de l'ISR peuvent être élus leader (sauf si `unclean.leader.election.enable=true`).

### Critères d'appartenance à l'ISR {#isr-membership-criteria}

Une réplique reste dans l'ISR tant que :
1. Elle a récupéré jusqu'au **Log End Offset (LEO)** du leader dans un délai de `replica.lag.time.max.ms` (par défaut : 30000 ms, soit 30 s)
2. Elle maintient une session active avec le controller (heartbeats)

```properties
# Key broker configs controlling ISR behavior
replica.lag.time.max.ms=30000        # Max time before follower is removed from ISR
```

**Flux de réduction et d'extension de l'ISR :**

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

**La surveillance des réductions de l'ISR** est essentielle : elle signale des problèmes de santé des brokers avant que les pannes ne surviennent.

```bash
# Check under-replicated partitions (ISR < replication factor)
kafka-topics.sh --describe --under-replicated-partitions \
  --bootstrap-server localhost:9092

# JMX metrics to monitor
# kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions  (should be 0)
# kafka.server:type=ReplicaManager,name=IsrShrinksPerSec
# kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
```

## High Watermark (HW) et Log End Offset (LEO) {#high-watermark-hw-vs-log-end-offset-leo}

Deux marqueurs d'offset déterminent les données visibles et celles qui sont répliquées :

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

| Concept | Définition | Qui le maintient |
|---------|-----------|-----------------|
| **LEO (Log End Offset)** | Offset du prochain message à écrire. Chaque réplique a son propre LEO. | Chaque réplique, de manière indépendante |
| **HW (High Watermark)** | Le plus haut offset répliqué sur **tous** les membres de l'ISR. Seuls les messages situés sous le HW sont visibles par les consommateurs. | Le leader le calcule et le propage aux followers via les réponses de fetch |

### Comment le HW progresse {#how-hw-advances}

1. Le producteur écrit le message à l'offset 8 sur le leader. LEO du leader = 9.
2. Le follower 1 récupère jusqu'à l'offset 8. LEO du follower 1 = 9.
3. Le follower 2 récupère jusqu'à l'offset 8. LEO du follower 2 = 9.
4. Le leader constate que tous les membres de l'ISR ont un LEO >= 9. Il fait progresser le HW à 9.
5. Les réponses de fetch suivantes transmettent le nouveau HW aux followers.

**Visibilité pour les consommateurs** : les consommateurs ne peuvent lire que jusqu'à `HW - 1`. Cela les empêche de lire des données susceptibles d'être perdues si le leader tombe avant que les followers ne les aient répliquées.

### Leader Epoch (KIP-101) {#leader-epoch-kip-101}

Le **leader epoch** est un entier strictement croissant, incrémenté à chaque élection d'un nouveau leader pour une partition. Il résout le **problème de divergence des logs** :

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

## Messages committed et uncommitted {#committed-vs-uncommitted-messages}

Un message est **committed** lorsqu'il a été répliqué sur toutes les répliques de l'ISR. Seuls les messages committed sont consommables.

### Matrice d'interaction acks + min.insync.replicas {#acks-mininsyncreplicas-interaction-matrix}

C'est la matrice de configuration la plus critique pour la durabilité dans Kafka :

```properties
# Producer config
acks=all                  # -1 is equivalent
# Broker/topic config
min.insync.replicas=2     # Minimum ISR members to accept a write
```

| acks | min.insync.replicas | RF | Comportement |
|------|--------------------|----|----------|
| `0` | indifférent | indifférent | Le producteur n'attend aucun ACK. Débit maximal, aucune garantie de durabilité. |
| `1` | indifférent | indifférent | Le producteur attend uniquement l'ACK du leader. Perte de données si le leader tombe avant la réplication. |
| `all` | `1` | 3 | L'ISR peut se réduire au seul leader, auquel cas `acks=all` équivaut à `acks=1`. **Fausse impression de sécurité.** |
| `all` | `2` | 3 | L'ISR doit compter au moins 2 membres, sinon les écritures sont rejetées. **Paramétrage de production recommandé.** |
| `all` | `3` | 3 | La panne d'un seul broker bloque les écritures. **Trop strict pour la plupart des cas d'usage.** |

**La règle d'or** : `acks=all` + `min.insync.replicas=2` + `replication.factor=3`.

### Ce qui se passe lorsque l'ISR descend sous min.insync.replicas {#what-happens-when-isr-shrinks-below-mininsyncreplicas}

```yaml
Scenario: RF=3, min.insync.replicas=2, acks=all

1. Normal: ISR={0,1,2}, writes succeed
2. Broker 2 dies: ISR={0,1}, writes succeed (2 >= min.insync)
3. Broker 1 dies: ISR={0}, writes FAIL with NotEnoughReplicasException
   - Partition is READABLE but NOT WRITABLE
   - Consumers continue reading committed data
4. Broker 1 returns: ISR={0,1}, writes resume
```

## Référence de configuration {#configuration-reference}

### Configurations de réplication au niveau du broker {#broker-level-replication-configs}

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

### Surcharges au niveau du topic {#topic-level-overrides}

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

## Pièges courants {#gotchas}

- **RF=2 est un piège.** Avec `min.insync.replicas=2`, la panne d'un seul follower rend la partition en lecture seule. Avec `min.insync.replicas=1`, un seul crash de broker suffit pour provoquer une perte de données. Toujours RF >= 3.
- **`acks=all` avec `min.insync.replicas=1` donne une fausse sécurité.** Si l'ISR se réduit au seul leader, `acks=all` se dégrade en `acks=1` : plus aucune confirmation de réplication.
- **Les réductions de l'ISR sont souvent causées par des pauses GC, et non par des pannes de brokers.** Vérifiez les logs GC et `replica.lag.time.max.ms` avant de supposer un problème matériel.
- **La propagation du HW est différée.** Le leader met à jour le HW, mais les followers ne le apprennent qu'à la réponse de fetch suivante. Il existe de brèves fenêtres pendant lesquelles les followers possèdent des données au-delà de leur HW local.

## Voir aussi {#see-also}

- [[kafka-fault-tolerance]] - scénarios de panne, élection de leader unclean, réplication rack-aware, schémas multi-DC
- [[broker-architecture]] - élection du controller, KRaft, fonctionnement interne des brokers
- [[topics-and-partitions]] - affectation des partitions, segments de log, compaction
- [[kafka-cluster-management]] - mises à jour progressives, réaffectation, supervision
- [[kafka-producer-fundamentals]] - modes acks du point de vue du producteur
