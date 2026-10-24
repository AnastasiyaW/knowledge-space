---
title: "Architecture du broker"
category: concepts
tags: [kafka, broker, cluster, zookeeper, kraft, replication]
level: 5
source_sha256: c51494aca14f0a4f8d0f5b5fa2a1b9eeea50f931ba5656af8347e167e776acd9
translation: machine
translated_at: '2026-10-24'
---
# Architecture du broker {#broker-architecture}

Un broker Kafka est un processus serveur unique qui reçoit les messages des producteurs, attribue les offsets, persiste les données sur disque et sert les requêtes de fetch des consommateurs. Un **cluster** est un groupe de brokers qui se coordonnent via une couche de métadonnées (ZooKeeper ou KRaft). Cette entrée couvre les mécanismes internes des brokers, l'élection du contrôleur, le leadership des partitions, les mécanismes de réplication, le stockage des logs, les politiques de rétention et le chemin de migration vers KRaft.

## Rôle du broker dans un cluster {#broker-role-in-a-cluster}

Chaque broker d'un cluster :
- Est identifié par un entier unique `broker.id`
- Possède un sous-ensemble des partitions (en tant que leader ou follower)
- Accepte les connexions TCP sur les `listeners` (PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL)
- Stocke les données de partition sous `log.dirs` sous forme de fichiers de segments en ajout seul
- Remonte ses métadonnées au contrôleur et reçoit les affectations de partitions

Un cluster de production minimal nécessite **3 brokers** (pour tolérer 1 panne avec `replication.factor=3` et `min.insync.replicas=2`).

```php
Producer --> Broker 0 (leader P0)  --> Broker 1 (follower P0, leader P1)
                                   --> Broker 2 (follower P0, follower P1)
```

Les brokers sont **sans état vis-à-vis des consommateurs** : ils ne suivent pas en interne les offsets des consommateurs (les offsets sont stockés dans le topic `__consumer_offsets`). Voir [[consumer-groups]].

## Élection du contrôleur {#controller-election}

### Mode ZooKeeper (historique, déprécié depuis Kafka 3.3) {#zookeeper-mode-legacy-deprecated-since-kafka-33}

L'un des brokers du cluster est élu **contrôleur**. Il est chargé de :
- Détecter les pannes de brokers (via l'expiration de session ZooKeeper)
- Réaffecter le leadership des partitions lorsqu'un broker leader tombe
- Propager les changements de métadonnées (nouveaux topics, réaffectations de partitions) à tous les brokers

Mécanisme d'élection :
1. Chaque broker tente de créer un **ZNode éphémère** `/controller` dans ZooKeeper au démarrage
2. Le premier broker qui réussit devient le contrôleur
3. Les autres brokers posent un **watch** sur le ZNode `/controller`
4. Lorsque le contrôleur meurt, ZooKeeper supprime le nœud éphémère, ce qui déclenche un événement de watch
5. Les brokers restants se disputent la recréation du nœud : le gagnant devient le nouveau contrôleur

```bash
# ZooKeeper znodes used by Kafka
/brokers/ids/[broker_id]      # ephemeral - broker registration
/controller                    # ephemeral - current controller
/brokers/topics/[topic]        # persistent - topic metadata
/admin/reassign_partitions     # persistent - reassignment state
```

**Limites** : ZooKeeper devient un goulot d'étranglement à grande échelle (>200k partitions). La propagation des métadonnées est asynchrone, ce qui crée des fenêtres de split-brain pendant le basculement du contrôleur.

### Mode KRaft (Kafka Raft, prêt pour la production depuis Kafka 3.6) {#kraft-mode-kafka-raft-production-ready-since-kafka-36}

KRaft remplace ZooKeeper par un protocole de consensus interne basé sur Raft. Les nœuds contrôleurs forment un **quorum** qui gère les métadonnées du cluster sous forme de log répliqué (topic `__cluster_metadata`).

Différences clés avec le mode ZooKeeper :

| Aspect | ZooKeeper | KRaft |
|--------|-----------|-------|
| Dépendance externe | Ensemble ZooKeeper (3-5 nœuds) | Aucune |
| Stockage des métadonnées | ZNodes ZooKeeper | Topic interne `__cluster_metadata` |
| Élection du contrôleur | Course sur ZNode éphémère | Élection de leader Raft |
| Partitions max par cluster | ~200k en limite pratique | Millions (testé à 2M+) |
| Arrêt/démarrage | Lent (rechargement complet des métadonnées depuis ZK) | Rapide (rejeu du log) |
| Configuration | `zookeeper.connect` | `controller.quorum.voters` |

Rôles des nœuds KRaft :
- **Contrôleur seul** (`process.roles=controller`) : participe au quorum de métadonnées, ne sert pas les données clients
- **Broker seul** (`process.roles=broker`) : sert les requêtes produce/fetch, reçoit les métadonnées des contrôleurs
- **Combiné** (`process.roles=broker,controller`) : les deux rôles sur une même JVM (adapté aux petits clusters, non recommandé en production au-delà de 10 nœuds)

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

Réf. : [KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)

## Leadership des partitions et ISR {#partition-leadership-and-isr}

### Leader et followers {#leader-and-followers}

Chaque partition possède exactement **un leader** et zéro ou plusieurs **followers**. Le leader :
- Traite toutes les requêtes produce et fetch pour cette partition
- Attribue des offsets croissants de manière monotone aux enregistrements entrants
- Maintient le **High Watermark (HW)**, c'est-à-dire l'offset jusqu'auquel tous les membres de l'ISR ont répliqué

Les followers :
- Envoient des requêtes de fetch au leader (même protocole que les consommateurs)
- Répliquent les enregistrements dans l'ordre
- **Ne** servent **pas** les lectures clients (en mode standard ; voir KIP-392 pour le fetch depuis les followers)

### Réplicas synchronisés (ISR) {#in-sync-replicas-isr}

L'ISR est l'ensemble dynamique des réplicas qui sont « à jour » par rapport au leader. Un réplica sort de l'ISR s'il n'a pas effectué de fetch depuis le leader pendant `replica.lag.time.max.ms` (par défaut : 30 s).

```sql
Partition P0:
  Leader: Broker 0  (offset 1000, HW=998)
  ISR: [0, 1, 2]
  Broker 1: offset 998 (in sync)
  Broker 2: offset 998 (in sync)
  Broker 3: offset 950 (OUT of sync -- lagging, removed from ISR)
```

**Enregistrement validé** : un enregistrement est validé (visible par les consommateurs) uniquement lorsque **tous les membres de l'ISR** l'ont acquitté. Le High Watermark avance en conséquence.

### Facteur de réplication {#replication-factor}

Défini par topic à la création :

```bash
kafka-topics.sh --create \
  --topic orders \
  --partitions 12 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092
```

Règles empiriques :
- `replication.factor=3` est le standard en production
- **Doit être <= nombre de brokers** du cluster
- Un RF plus élevé augmente la durabilité mais coûte en disque et en réseau

### min.insync.replicas {#mininsyncreplicas}

Contrôle le nombre minimal de réplicas qui doivent acquitter une écriture avant que le producteur reçoive un succès (lorsque `acks=all`) :

```properties
# Topic-level or broker-level config
min.insync.replicas=2
```

Avec `replication.factor=3` et `min.insync.replicas=2` :
- Les écritures réussissent si au moins 2 réplicas (leader inclus) sont synchronisés
- Si l'ISR descend à 1, les produce avec `acks=all` reçoivent une `NotEnoughReplicasException`
- Cela garantit **l'absence de perte de données** tant qu'au moins 1 des 2 réplicas ayant acquitté survit

**Piège** : `min.insync.replicas` n'a aucun effet si le producteur n'utilise pas `acks=all` (ou `acks=-1`). Avec `acks=1`, seul le leader acquitte.

Voir [[kafka-fault-tolerance]] pour l'élection de leader, l'élection de leader non propre et les scénarios de panne.

## Segments de log et stockage {#log-segments-and-storage}

### Organisation sur disque {#on-disk-layout}

Chaque partition est stockée sous forme de répertoire dans le système de fichiers du broker :

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

- **.log** : les données des messages proprement dites (compressées par batch avec le `compression.type` configuré)
- **.index** : index clairsemé offset-vers-position (associe les offsets logiques aux positions en octets dans `.log`)
- **.timeindex** : index clairsemé timestamp-vers-offset (permet les recherches par temps)

### Rotation des segments {#segment-rolling}

Un nouveau segment est créé lorsque l'une de ces conditions est remplie :

| Configuration | Valeur par défaut | Déclenche un nouveau segment lorsque... |
|---------------|-------------------|------------------------------------------|
| `log.segment.bytes` | 1 Go (`1073741824`) | Le segment courant atteint cette taille |
| `log.roll.ms` / `log.roll.hours` | 7 jours (`168` heures) | Le temps écoulé depuis la création du segment dépasse cette valeur |
| `log.index.size.max.bytes` | 10 Mo | Le fichier d'index atteint cette taille |

Seul le **segment actif** (le plus récent) est en cours d'écriture. Les segments plus anciens sont immuables et éligibles à la rétention ou à la compaction.

```properties
# Smaller segments = more frequent rolling, finer retention granularity
log.segment.bytes=536870912    # 512 MB
log.roll.hours=24              # roll daily
```

### Transfert zero-copy {#zero-copy-transfer}

Kafka utilise `sendfile()` (zero-copy) pour transférer les données du disque vers le socket réseau, en contournant les buffers de l'espace utilisateur. C'est pour cette raison que Kafka atteint un débit élevé avec une faible consommation de CPU. Le zero-copy ne fonctionne que lorsque SSL n'est **pas** activé sur le listener du broker.

## Politiques de rétention {#retention-policies}

Kafka prend en charge trois stratégies de rétention, configurables par topic ou au niveau du broker.

### Rétention basée sur le temps (par défaut) {#time-based-retention-default}

Supprime les segments plus anciens que la période de rétention :

```properties
log.retention.hours=168         # 7 days (default)
log.retention.minutes=10080     # equivalent, finer granularity
log.retention.ms=604800000      # equivalent, finest granularity
# Precedence: ms > minutes > hours
```

Le thread de nettoyage du broker vérifie périodiquement (`log.retention.check.interval.ms`, par défaut 5 min) si des **segments fermés** ont un timestamp maximal plus ancien que la période de rétention. Si c'est le cas, le segment est supprimé.

**Important** : la rétention s'applique à des segments entiers, et non à des enregistrements individuels. Un enregistrement peut vivre plus longtemps que `log.retention.hours` s'il se trouve dans le segment actif, qui n'a pas encore été tourné.

### Rétention basée sur la taille {#size-based-retention}

Supprime les segments les plus anciens lorsque le log de la partition dépasse une taille totale :

```properties
log.retention.bytes=10737418240  # 10 GB per partition
# -1 = no size limit (default)
```

Peut être combinée à la rétention temporelle : la première condition atteinte déclenche la suppression.

### Compaction de log {#log-compaction}

Ne conserve que la **dernière valeur pour chaque clé** au sein d'une partition. Utilisée pour les topics de changelog et de snapshot (par exemple `__consumer_offsets`, les state stores de KTable).

```properties
log.cleanup.policy=compact       # or "delete,compact" for both
log.cleaner.min.compaction.lag.ms=0
log.cleaner.min.cleanable.ratio=0.5
```

Processus de compaction :
1. Le thread **log cleaner** construit une map d'offsets en mémoire (hash de clé -> dernier offset)
2. Il lit la partie « sale » (non compactée) du log
3. Il copie les enregistrements en ignorant toute clé dont le dernier offset se trouve dans un segment plus récent
4. Les enregistrements dont la valeur est `null` (tombstones) sont conservés pendant `delete.retention.ms` (par défaut 24 h), puis supprimés

```text
Before compaction:        After compaction:
offset  key  value        offset  key  value
0       A    v1           2       A    v3
1       B    v1           3       B    v2
2       A    v3           (tombstone B removed after delete.retention.ms)
3       B    v2
4       B    null (tombstone)
```

**Piège** : les topics compactés doivent avoir des clés non nulles. Les enregistrements sans clé sont rejetés si `log.cleanup.policy=compact`.

Voir [[topics-and-partitions]] pour les surcharges de configuration au niveau du topic.

## Configurations clés du broker {#key-broker-configurations}

### Paramètres critiques en production {#critical-production-settings}

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

### Hiérarchie de configuration {#config-hierarchy}

Les configurations Kafka peuvent être définies à plusieurs niveaux. Les paramètres plus spécifiques priment sur les moins spécifiques :

1. **Configuration dynamique par topic** (priorité la plus élevée) : `kafka-configs.sh --alter --topic X`
2. **Configuration dynamique par broker** : `kafka-configs.sh --alter --entity-type brokers --entity-name 0`
3. **Configuration dynamique à l'échelle du cluster** : `kafka-configs.sh --alter --entity-type brokers --entity-default`
4. **Configuration statique du broker** (`server.properties`) : nécessite un redémarrage du broker

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

## Migration de ZooKeeper vers KRaft {#kraft-migration-from-zookeeper}

Chemin de migration pour les clusters existants basés sur ZooKeeper (pris en charge depuis Kafka 3.6, ZooKeeper entièrement supprimé dans Kafka 4.0) :

### Migration étape par étape {#step-by-step-migration}

```hcl
Phase 1: Deploy KRaft controllers alongside existing ZK cluster
Phase 2: Migrate metadata (brokers dual-write to ZK and KRaft)
Phase 3: Switch brokers to KRaft mode
Phase 4: Decommission ZooKeeper
```

**1. Provisionner les nœuds contrôleurs KRaft**

```properties
# New controller nodes (do NOT run on existing broker machines if possible)
process.roles=controller
node.id=3000    # use IDs that don't conflict with existing broker.id values
controller.quorum.voters=3000@ctrl1:9093,3001@ctrl2:9093,3002@ctrl3:9093
controller.listener.names=CONTROLLER
listeners=CONTROLLER://ctrl1:9093
```

**2. Formater le stockage des contrôleurs**

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

**3. Démarrer les contrôleurs et lancer la migration**

```bash
# Start controller quorum
kafka-server-start.sh /etc/kafka/kraft-controller.properties

# Initiate migration on the ZK-based cluster -- enable dual-write
kafka-metadata.sh --bootstrap-controller ctrl1:9093 \
  --command-config admin.properties \
  migrate --start
```

**4. Basculer les brokers en mode KRaft**

Pour chaque broker (redémarrage progressif) :

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

**5. Finaliser la migration**

```bash
# After all brokers are on KRaft, finalize (stops dual-write to ZK)
kafka-metadata.sh --bootstrap-controller ctrl1:9093 \
  --command-config admin.properties \
  migrate --finalize
```

**6. Mettre hors service ZooKeeper**

Après la finalisation, ZooKeeper n'est plus nécessaire. Arrêtez les nœuds ZK et retirez-les de l'infrastructure.

### Pièges de la migration {#migration-gotchas}

- **Ne pas sauter de versions de Kafka** : migrer d'abord vers 3.6+ si vous êtes sur une version plus ancienne, puis migrer de ZK vers KRaft
- **Nombre de nœuds contrôleurs** : toujours impair (3 ou 5), comme pour le dimensionnement de l'ensemble ZooKeeper
- **Conflits de `node.id`** : les identifiants des nœuds contrôleurs ne doivent pas chevaucher les identifiants de brokers existants
- **ACL** : si vous utilisez des ACL basées sur ZK (`kafka.security.auth.SimpleAclAuthorizer`), passez à `kafka.security.authorizer.AclAuthorizer` (compatible KRaft) avant la migration
- **Retour arrière** : possible uniquement avant `--finalize`. Après la finalisation, le retour à ZK n'est pas pris en charge
- **Supervision** : surveillez `kafka.controller:type=KafkaController,name=ActiveControllerCount`, qui doit valoir exactement 1 en permanence

Réf. : [Apache Kafka ZooKeeper to KRaft Migration Guide](https://kafka.apache.org/documentation/#kraft_zk_migration)

## Surveillance de la santé des brokers {#monitoring-broker-health}

Principales métriques JMX à surveiller :

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

**Seuils d'alerte** :
- `OfflinePartitionsCount > 0` : investigation immédiate
- `UnderReplicatedPartitions > 0` pendant plus de 5 min : broker probablement surchargé ou en panne
- `IsrShrinksPerSec` soutenu : vérifier les E/S disque, le réseau, les pauses du GC

## Références croisées {#cross-references}

- [[topics-and-partitions]] -- stratégies d'affectation des partitions, routage par clé, dimensionnement du nombre de partitions
- [[consumer-groups]] -- gestion des offsets des consommateurs, rééquilibrage, coordinateur de groupe
- [[kafka-replication-fundamentals]] -- ISR, HW/LEO, acks + min.insync.replicas
- [[kafka-fault-tolerance]] -- élection de leader non propre, réplication tenant compte des racks, élection du leader préféré

## Références externes {#external-references}

- [Apache Kafka Broker Configuration](https://kafka.apache.org/documentation/#brokerconfigs)
- [KIP-500: Replace ZooKeeper with KRaft](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)
- [KRaft Migration Guide](https://kafka.apache.org/documentation/#kraft_zk_migration)
- [Kafka Design: Log Storage](https://kafka.apache.org/documentation/#design_filesystem)
- [Kafka Design: Replication](https://kafka.apache.org/documentation/#replication)
