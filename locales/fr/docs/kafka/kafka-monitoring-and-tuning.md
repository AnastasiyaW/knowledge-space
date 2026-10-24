---
level: 4
source_sha256: 42d16cd0bbfc06a526b4dd0ef00e2559319ca11c002e1b32bb4163f22333d854
translation: machine
translated_at: '2026-10-24'
---
# Supervision et réglage de Kafka {#kafka-monitoring-and-tuning}

Métriques JMX critiques, mise en place de Prometheus et Grafana, règles d'alerte, et réglage des performances au niveau de l'OS, de la JVM et du broker pour les clusters Kafka en production.

## Métriques JMX critiques {#critical-jmx-metrics}

### Santé du cluster {#cluster-health}

| MBean | Métrique | Seuil d'alerte |
|---|---|---|
| `kafka.controller:type=KafkaController,name=ActiveControllerCount` | Doit valoir exactement 1 sur l'ensemble du cluster | != 1 |
| `kafka.controller:type=KafkaController,name=OfflinePartitionsCount` | Partitions sans leader actif | > 0 |
| `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions` | Partitions en dessous du facteur de réplication | > 0 pendant plus de 5 min |
| `kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount` | Partitions en dessous de `min.insync.replicas` | > 0 |

### Débit {#throughput}

| MBean | Métrique | Utilisation |
|---|---|---|
| `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec` | Octets entrants/s | Planification de la capacité |
| `kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec` | Octets sortants/s | Saturation réseau |
| `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec` | Messages/s | Suivi de la tendance du débit |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=Produce` | Requêtes Produce/s | Profilage de la charge |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=FetchConsumer` | Requêtes Fetch des consommateurs/s | Charge des consommateurs |

### Latence {#latency}

| MBean | Métrique | Seuil d'alerte |
|---|---|---|
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce` | Latence Produce de bout en bout (p99) | > 100 ms |
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer` | Latence Fetch des consommateurs (p99) | > 500 ms |
| `kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Produce` | Temps d'attente dans la file de requêtes | > 50 ms (broker surchargé) |
| `kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent` | Taux d'inactivité des threads de traitement des requêtes | < 0,3 (plus de 70 % d'occupation = surcharge) |

### Réplication {#replication}

| MBean | Métrique | Seuil d'alerte |
|---|---|---|
| `kafka.server:type=ReplicaManager,name=IsrShrinksPerSec` | Taux de réduction de l'ISR | > 0 de façon soutenue |
| `kafka.server:type=ReplicaManager,name=IsrExpandsPerSec` | Taux d'extension de l'ISR | Doit suivre les réductions |
| `kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica` | Retard de réplication maximal (messages) | > 10000 |
| `kafka.server:type=ReplicaManager,name=PartitionCount` | Partitions sur le broker | > 4000 |

### Retard des consommateurs (consumer lag) {#consumer-lag}

```bash
# CLI method
kafka-consumer-groups.sh --bootstrap-server broker1:9092 \
  --describe --group my-consumer-group

# Output columns: TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
```

Pour une supervision du retard en temps réel, utilisez Burrow (LinkedIn) ou exportez les données via JMX :

```properties
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,
  name=records-lag-max
```

## Mise en place de Prometheus + Grafana {#prometheus-grafana-setup}

### 1. Agent JMX Exporter {#1-jmx-exporter-agent}

```bash
# Download
curl -LO https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/1.0.1/jmx_prometheus_javaagent-1.0.1.jar
```

```yaml
# kafka-jmx-config.yml
lowercaseOutputName: true
lowercaseOutputLabelNames: true
whitelistObjectNames:
  - "kafka.controller:*"
  - "kafka.server:type=BrokerTopicMetrics,*"
  - "kafka.server:type=ReplicaManager,*"
  - "kafka.server:type=ReplicaFetcherManager,*"
  - "kafka.server:type=KafkaRequestHandlerPool,*"
  - "kafka.network:type=RequestMetrics,*"
  - "kafka.network:type=RequestChannel,*"
  - "kafka.network:type=SocketServer,*"
  - "kafka.log:type=LogFlushStats,*"
  - "kafka.log:type=Log,name=Size,*"
  - "java.lang:type=GarbageCollector,*"
  - "java.lang:type=Memory"
rules:
  - pattern: "kafka.server<type=(.+), name=(.+), topic=(.+)><>(.+):"
    name: kafka_server_$1_$2
    labels:
      topic: $3
    type: GAUGE
  - pattern: "kafka.server<type=(.+), name=(.+)><>(.+):"
    name: kafka_server_$1_$2
    type: GAUGE
```

### 2. Démarrage du broker avec l'agent {#2-broker-startup-with-agent}

```bash
# In systemd unit Environment or kafka-server-start.sh
export KAFKA_OPTS="-javaagent:/opt/kafka/libs/jmx_prometheus_javaagent-1.0.1.jar=7071:/opt/kafka/config/kafka-jmx-config.yml"
```

### 3. Configuration de scrape Prometheus {#3-prometheus-scrape-config}

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kafka-brokers'
    static_configs:
      - targets:
        - broker1:7071
        - broker2:7071
        - broker3:7071
    relabel_configs:
      - source_labels: [__address__]
        regex: '(.+):7071'
        target_label: broker
        replacement: '$1'

  - job_name: 'kafka-consumer-lag'
    static_configs:
      - targets: ['burrow:8000']  # or kafka-lag-exporter
```

### 4. Règles d'alerte {#4-alert-rules}

```yaml
# kafka-alerts.yml
groups:
  - name: kafka
    rules:
      - alert: KafkaUnderReplicatedPartitions
        expr: kafka_server_replicamanager_underreplicatedpartitions > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.broker }} has {{ $value }} under-replicated partitions"

      - alert: KafkaNoActiveController
        expr: sum(kafka_controller_kafkacontroller_activecontrollercount) != 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "No active Kafka controller in the cluster"

      - alert: KafkaRequestHandlerSaturated
        expr: kafka_server_kafkarequesthandlerpool_requesthandleravgidlepercent < 0.3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.broker }} request handlers >70% busy"

      - alert: KafkaHighConsumerLag
        expr: kafka_consumer_consumer_fetch_manager_metrics_records_lag_max > 100000
        for: 10m
        labels:
          severity: warning
```

### 5. Tableaux de bord Grafana {#5-grafana-dashboards}

Importez les identifiants `721` (vue d'ensemble des brokers) ou `7589` (détail par topic), ou utilisez les tableaux de bord open source de Confluent. Panneaux clés : BytesIn/Out par broker, carte de chaleur de latence des requêtes, répartition du nombre de partitions, retard des consommateurs par groupe.

## Réglage des performances {#performance-tuning}

### Niveau OS {#os-level}

```bash
# --- Page cache ---
# Kafka reads/writes through page cache. More free RAM = more cache hits.
echo 1 > /proc/sys/vm/swappiness          # near-zero swap preference
echo "vm.swappiness=1" >> /etc/sysctl.conf

# Dirty page flush tuning (aggressive flush to avoid I/O bursts)
echo "vm.dirty_ratio=60" >> /etc/sysctl.conf
echo "vm.dirty_background_ratio=5" >> /etc/sysctl.conf

# --- File descriptors ---
# Each partition segment = 2 fds (log + index). 10K partitions = 20K fds minimum.
echo "kafka soft nofile 128000" >> /etc/security/limits.conf
echo "kafka hard nofile 128000" >> /etc/security/limits.conf
# Or in systemd unit: LimitNOFILE=128000

# --- TCP settings (critical for high-throughput and cross-DC) ---
echo "net.core.wmem_max=2097152" >> /etc/sysctl.conf         # 2 MB send buffer max
echo "net.core.rmem_max=2097152" >> /etc/sysctl.conf         # 2 MB receive buffer max
echo "net.ipv4.tcp_wmem=4096 65536 2097152" >> /etc/sysctl.conf
echo "net.ipv4.tcp_rmem=4096 65536 2097152" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog=50000" >> /etc/sysctl.conf  # packet queue before kernel
echo "net.ipv4.tcp_max_syn_backlog=8192" >> /etc/sysctl.conf

# --- Filesystem ---
# XFS is preferred. Mount options:
# /dev/sdb /data/kafka xfs noatime,nodiratime,nobarrier 0 2
# nobarrier: safe with battery-backed RAID or NVMe with PLP

sysctl -p  # apply all
```

### Réglage de la JVM (G1GC) {#jvm-tuning-g1gc}

```bash
# kafka-server-start.sh or systemd Environment
export KAFKA_HEAP_OPTS="-Xms6g -Xmx6g"
export KAFKA_JVM_PERFORMANCE_OPTS="\
  -server \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=20 \
  -XX:InitiatingHeapOccupancyPercent=35 \
  -XX:+ExplicitGCInvokesConcurrent \
  -XX:MaxInlineLevel=15 \
  -XX:+ParallelRefProcEnabled \
  -XX:+UnlockExperimentalVMOptions \
  -XX:G1NewSizePercent=10 \
  -XX:G1MaxNewSizePercent=25 \
  -Djava.awt.headless=true"
```

Principes clés pour le GC :
- Un **tas de 6 Go** constitue le meilleur compromis pour la plupart des charges. Au-delà, les pauses GC s'allongent.
- **G1GC** avec `MaxGCPauseMillis=20` maintient une faible latence en queue de distribution.
- `InitiatingHeapOccupancyPercent=35` déclenche le GC concurrent plus tôt, ce qui évite les GC complets.
- Surveillez `java.lang:type=GarbageCollector,name=G1 Young Generation` et `G1 Old Generation` dans JMX. Alertez si les collections de l'ancienne génération sont > 0/min.

### Réglage au niveau du broker {#broker-level-tuning}

```properties
# --- Threading ---
num.network.threads=8              # network I/O threads (default 3, increase for 10GbE+)
num.io.threads=16                  # disk I/O threads (default 8, increase for JBOD)
num.replica.fetchers=4             # parallel replica fetch threads (default 1)
num.recovery.threads.per.data.dir=2  # log recovery threads at startup

# --- Socket buffers ---
socket.send.buffer.bytes=1048576   # 1 MB (default 100 KB)
socket.receive.buffer.bytes=1048576

# --- Replication ---
replica.fetch.max.bytes=10485760   # 10 MB (match message.max.bytes)
replica.fetch.wait.max.ms=500      # max wait before fetch response

# --- Log flush (usually leave to OS page cache) ---
# log.flush.interval.messages=10000  # uncomment only for durability-critical
# log.flush.interval.ms=1000

# --- Compression ---
compression.type=producer          # let producer decide (lz4 recommended)
```

## Pièges à éviter {#gotchas}

- **Thrashing du page cache.** Si les consommateurs lisent d'anciennes données (lectures de rattrapage), ils évincent les données récentes du page cache, ce qui dégrade les consommateurs temps réel. Utilisez le stockage tiered ou des followers dédiés en lecture seule pour les lectures historiques.
- **Un tas supérieur à 8 Go provoque de longues pauses GC.** Kafka conserve un état minimal dans le tas. La RAM supplémentaire est mieux utilisée pour le page cache.
- **`UnderReplicatedPartitions > 0` ne signifie pas toujours une panne du broker.** Cela peut être causé par des disques lents, une saturation réseau ou des pauses GC. Vérifiez la corrélation de `IsrShrinksPerSec` avec les journaux GC.
- **`whitelistObjectNames` du JMX exporter est important.** Scruter tous les MBeans génère des milliers de métriques et peut provoquer un OOM sur l'exporter. Ne whitelistez que les métriques sur lesquelles vous alertez.

## Voir aussi {#see-also}

- [[kafka-cluster-management]] - dimensionnement, mises à niveau, défaillance de disque, réaffectation des partitions
- [[kafka-backup-and-dr]] - MirrorMaker 2, stratégies de sauvegarde, reprise après sinistre
- [[kafka-replication-fundamentals]] - mécanique de l'ISR, sémantique du retard de réplication
- [[consumer-groups]] - protocoles de rééquilibrage, gestion des offsets, sémantique du retard des consommateurs
- [[kafka-monitoring]] - autres modèles et outils de supervision
