---
level: 3
source_sha256: 643161c87218e252c764ab1a0d39d3d19d8647ca0465e53976050c2c88b19986
translation: machine
translated_at: '2026-10-24'
---
# Tolérance aux pannes dans Kafka {#kafka-fault-tolerance}

Élection de leader « unclean », élection du réplica préféré, réplicas observateurs, réplication consciente des racks, schémas multi-datacenters, scénarios de panne avec procédures de reprise et métriques de santé de la réplication.

Pour le modèle de réplication, l'ISR, HW/LEO et l'interaction avec `acks`, voir [[kafka-replication-fundamentals]].

## Élection de leader « unclean » {#unclean-leader-election}

Lorsque tous les réplicas de l'ISR sont en panne, Kafka doit choisir entre **disponibilité et intégrité des données**.

```properties
# Broker config (default: false since Kafka 0.11.0.0)
unclean.leader.election.enable=false
```

| Paramètre | Comportement | Compromis |
|-----------|--------------|-----------|
| `false` (par défaut) | La partition reste hors ligne jusqu'au retour d'un membre de l'ISR | **Aucune perte de données**, mais indisponibilité |
| `true` | Un réplica désynchronisé peut devenir leader | **Perte de données** (les messages non répliqués sont perdus), mais disponibilité |

**Quand activer l'élection « unclean » :**
- Métriques, logs et flux de clics, lorsque la disponibilité prime sur la durabilité
- Topics reconstructibles depuis les systèmes sources
- **Jamais** pour les transactions financières, les commandes ou les journaux d'audit

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

### Mécanique de perte de données avec l'élection « unclean » {#data-loss-mechanics-with-unclean-election}

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

## Élection du réplica préféré {#preferred-replica-election}

Kafka attribue un **leader préféré** à chaque partition (le premier broker de la liste des réplicas). Après des pannes et des reprises, le leadership peut se déséquilibrer, certains brokers portant alors davantage de charge de leader que d'autres.

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

**Fonctionnement du rééquilibrage automatique :**
1. Toutes les `leader.imbalance.check.interval.seconds`, le contrôleur vérifie chaque broker.
2. Si le déséquilibre de leadership d'un broker dépasse `leader.imbalance.per.broker.percentage`, le contrôleur déclenche des élections de leader préféré.
3. Cela ne fonctionne que si le leader préféré est dans l'ISR.

## Réplicas observateurs (KIP-392) {#observer-replicas-kip-392}

Les réplicas observateurs sont des réplicas **sans droit de vote** : ils répliquent les données, mais ne sont **jamais ajoutés à l'ISR** et **ne peuvent jamais être élus leader**. Ils servent uniquement aux lectures des consommateurs, en lecture seule.

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

Cas d'usage :
- **Lectures inter-datacenters** : les consommateurs du DC-West lisent depuis l'observateur local.
- **Déchargement du trafic de lecture** : l'observateur traite les lectures des consommateurs sans affecter l'ISR ni la latence d'écriture.
- **Charges analytiques** : les consommateurs gourmands n'impactent pas les réplicas de production.

```properties
# Consumer config to fetch from closest replica (including observers)
client.rack=dc-west
# Broker config
broker.rack=dc-east

# Replica placement (topic config)
replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector
```

**Limite** : les réplicas observateurs peuvent accuser un retard par rapport au leader. Les consommateurs qui lisent depuis les observateurs obtiennent des données **à cohérence éventuelle**.

## Réplication consciente des racks {#rack-aware-replication}

`broker.rack` indique à Kafka le domaine de défaillance (rack, AZ, datacenter) auquel appartient chaque broker. L'algorithme d'affectation des partitions veille à répartir les réplicas entre les racks.

```properties
# Broker configs
# Broker 0 (AZ-a)
broker.rack=us-east-1a
# Broker 1 (AZ-b)
broker.rack=us-east-1b
# Broker 2 (AZ-c)
broker.rack=us-east-1c
```

Avec la conscience des racks activée, un topic avec RF=3 sur un cluster de 6 brokers répartis sur 3 AZ :

```text
Partition 0: Broker 0 (AZ-a), Broker 3 (AZ-b), Broker 5 (AZ-c)
Partition 1: Broker 1 (AZ-b), Broker 4 (AZ-c), Broker 2 (AZ-a)

Each partition has one replica per AZ -- survives full AZ failure.
```

Sans `broker.rack`, Kafka peut placer tous les réplicas dans la même AZ, rendant la panne d'une seule AZ fatale.

```bash
# Verify rack-aware placement
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
# Cross-reference broker IDs with their broker.rack setting
```

## Schémas multi-datacenters {#multi-datacenter-patterns}

### Schéma 1 : cluster étendu (stretch cluster) {#pattern-1-stretch-cluster}

Un unique cluster Kafka couvrant 2 ou 3 datacenters reliés par un réseau à faible latence.

```text
DC-East                         DC-West
+----------+                    +----------+
| Broker 0 |<--- replication -->| Broker 3 |
| Broker 1 |      (sync)       | Broker 4 |
| Broker 2 |                    | Broker 5 |
+----------+                    +----------+
```

**Prérequis :**
- Latence aller-retour inférieure à 50 ms entre les DC (idéalement inférieure à 10 ms)
- `broker.rack` défini au nom du DC
- RF=4, min.insync.replicas=3 pour 2 DC ; RF=3, min.insync.replicas=2 pour 3 DC

### Schéma 2 : MM2 actif-passif {#pattern-2-mm2-active-passive}

Clusters Kafka distincts par DC. MM2 réplique les topics de manière asynchrone.

### Schéma 3 : MM2 actif-actif {#pattern-3-mm2-active-active}

Les deux clusters acceptent les écritures. MM2 réplique dans les deux sens. L'espace de noms des topics empêche les boucles.

### Comparaison des schémas {#pattern-comparison}

| Critère | Cluster étendu | MM2 actif-passif | MM2 actif-actif |
|---------|----------------|------------------|-----------------|
| Latence inter-DC | < 50 ms requise | Quelconque | Quelconque |
| Latence d'écriture | Plus élevée (inter-DC) | Locale | Locale |
| Bascule | Automatique (ISR) | Manuelle | Manuelle |
| Exactly-once | Oui | Non (écart asynchrone) | Non |
| Complexité | Faible | Moyenne | Élevée |
| Perte de données en cas de panne de DC | Aucune (si l'ISR s'étend sur les DC) | Possible | Possible |

Pour la configuration détaillée de MM2 et les procédures de bascule, voir [[kafka-backup-and-dr]].

## Scénarios de panne et reprise {#failure-scenarios-and-recovery}

### Scénario 1 : panne d'un broker (RF=3, min.insync.replicas=2) {#scenario-1-single-broker-failure-rf3-mininsyncreplicas2}

```yaml
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 crashes
After:  Controller elects Broker 1 as leader (next in ISR)
        ISR={1,2}, writes continue normally
        When Broker 0 recovers, it joins as follower, catches up, rejoins ISR
```

Aucune perte de données. Aucune interruption. Reprise automatique.

### Scénario 2 : deux pannes de brokers (RF=3, min.insync.replicas=2) {#scenario-2-two-broker-failures-rf3-mininsyncreplicas2}

```yaml
Before: Leader=Broker0, ISR={0,1,2}
Event:  Broker 0 and Broker 1 crash
After:  Controller elects Broker 2 as leader
        ISR={2} -- below min.insync.replicas=2
        Reads work. Writes FAIL with NotEnoughReplicasException.
        Writes resume when any other broker recovers and joins ISR.
```

Aucune perte de données. Les écritures sont bloquées jusqu'à la reprise.

### Scénario 3 : crash du leader avec données non répliquées {#scenario-3-leader-crash-with-unreplicated-data}

```yaml
Before: Leader LEO=100, HW=95, Follower LEO=95
Event:  Leader crashes (offsets 95-99 not replicated)
After:  Follower becomes leader with LEO=95
        Offsets 95-99 LOST (were uncommitted)
        Producers with acks=all never received ACK for 95-99
        Producers with acks=1 DID receive ACK -- DATA LOSS for those messages
```

C'est pourquoi `acks=all` est indispensable à la durabilité.

### Scénario 4 : redémarrage complet du cluster {#scenario-4-full-cluster-restart}

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

## Métriques clés de la santé de la réplication {#key-metrics-for-replication-health}

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

**Seuils d'alerte :**
- `UnderReplicatedPartitions > 0` pendant plus de 5 minutes : problème de santé d'un broker
- `OfflinePartitionsCount > 0` : alerte immédiate, partitions indisponibles
- `IsrShrinksPerSec` soutenu : vérifier les E/S disque, le réseau et le GC sur les brokers concernés
- `UnderMinIsrPartitionCount > 0` : les écritures échouent pour les partitions concernées

## Pièges courants {#gotchas}

- **L'élection de leader « unclean » peut faire perdre des données validées.** Des messages entièrement répliqués dans l'ISR peuvent être perdus si le seul réplica survivant était désynchronisé. Il ne s'agit pas seulement d'une perte de données « non validées ».
- **Le rééquilibrage automatique du leader ne fonctionne que si le leader préféré est dans l'ISR.** S'il a pris du retard, le rééquilibrage attend qu'il rattrape son retard. Aucune élection forcée n'est effectuée.
- **Les réplicas observateurs ajoutent de la charge de réplication sans apporter de durabilité.** Ils tirent leurs données du leader comme les followers classiques, ce qui consomme de la bande passante réseau. Dimensionnez le réseau en conséquence.
- **La réplication consciente des racks exige `broker.rack` sur TOUS les brokers.** Si certains brokers ne l'ont pas, Kafka ignore complètement la conscience des racks pour les topics concernés.

## Voir aussi {#see-also}

- [[kafka-replication-fundamentals]] - ISR, HW/LEO, matrice acks + min.insync.replicas
- [[kafka-backup-and-dr]] - configuration de MirrorMaker 2, procédures de reprise après sinistre
- [[broker-architecture]] - élection du contrôleur, KRaft, fonctionnement interne des brokers
- [[topics-and-partitions]] - affectation des partitions, segments de log
- [[kafka-cluster-management]] - mises à niveau progressives, réaffectation des partitions
