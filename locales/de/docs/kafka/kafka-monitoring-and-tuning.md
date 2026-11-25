---
level: 4
source_sha256: 42d16cd0bbfc06a526b4dd0ef00e2559319ca11c002e1b32bb4163f22333d854
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Monitoring und Tuning {#kafka-monitoring-and-tuning}

Kritische JMX-Metriken, Prometheus- und Grafana-Setup, Alert-Regeln sowie Performance-Tuning auf Betriebssystem-, JVM- und Broker-Ebene für produktive Kafka-Cluster.

## Kritische JMX-Metriken {#critical-jmx-metrics}

### Cluster-Zustand {#cluster-health}

| MBean | Metrik | Alert-Schwellenwert |
|---|---|---|
| `kafka.controller:type=KafkaController,name=ActiveControllerCount` | Muss im gesamten Cluster genau 1 sein | != 1 |
| `kafka.controller:type=KafkaController,name=OfflinePartitionsCount` | Partitionen ohne aktiven Leader | > 0 |
| `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions` | Partitionen unterhalb des Replikationsfaktors | > 0 für > 5 min |
| `kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount` | Partitionen unterhalb von `min.insync.replicas` | > 0 |

### Durchsatz {#throughput}

| MBean | Metrik | Verwendung |
|---|---|---|
| `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec` | Eingehende Bytes/s | Kapazitätsplanung |
| `kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec` | Ausgehende Bytes/s | Netzwerksättigung |
| `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec` | Nachrichten/s | Durchsatztrends |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=Produce` | Produce-Requests/s | Lastprofilierung |
| `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=FetchConsumer` | Consumer-Fetch-Requests/s | Consumer-Last |

### Latenz {#latency}

| MBean | Metrik | Alert-Schwellenwert |
|---|---|---|
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce` | End-to-End-Produce-Latenz (p99) | > 100ms |
| `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer` | Consumer-Fetch-Latenz (p99) | > 500ms |
| `kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Produce` | Wartezeit in der Request-Queue | > 50ms (Broker überlastet) |
| `kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent` | Leerlaufanteil der Request-Handler-Threads | < 0.3 (mehr als 70 % ausgelastet = überlastet) |

### Replikation {#replication}

| MBean | Metrik | Alert-Schwellenwert |
|---|---|---|
| `kafka.server:type=ReplicaManager,name=IsrShrinksPerSec` | ISR-Schrumpfungsrate | Anhaltend > 0 |
| `kafka.server:type=ReplicaManager,name=IsrExpandsPerSec` | ISR-Erweiterungsrate | Sollte auf Schrumpfungen folgen |
| `kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica` | Maximaler Replikationsrückstand (Nachrichten) | > 10000 |
| `kafka.server:type=ReplicaManager,name=PartitionCount` | Partitionen auf dem Broker | > 4000 |

### Consumer-Lag {#consumer-lag}

```bash
# CLI method
kafka-consumer-groups.sh --bootstrap-server broker1:9092 \
  --describe --group my-consumer-group

# Output columns: TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
```

Für die Echtzeitüberwachung des Lags kann Burrow (LinkedIn) verwendet oder per JMX exportiert werden:

```properties
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,
  name=records-lag-max
```

## Prometheus- und Grafana-Setup {#prometheus-grafana-setup}

### 1. JMX-Exporter-Agent {#1-jmx-exporter-agent}

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

### 2. Broker-Start mit Agent {#2-broker-startup-with-agent}

```bash
# In systemd unit Environment or kafka-server-start.sh
export KAFKA_OPTS="-javaagent:/opt/kafka/libs/jmx_prometheus_javaagent-1.0.1.jar=7071:/opt/kafka/config/kafka-jmx-config.yml"
```

### 3. Prometheus-Scrape-Konfiguration {#3-prometheus-scrape-config}

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

### 4. Alert-Regeln {#4-alert-rules}

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

### 5. Grafana-Dashboards {#5-grafana-dashboards}

Import-IDs `721` (Broker-Übersicht), `7589` (Topic-Details) verwenden oder die Open-Source-Dashboards von Confluent nutzen. Wichtige Panels: BytesIn/Out pro Broker, Heatmap der Request-Latenz, Verteilung der Partitionsanzahl, Consumer-Lag nach Consumer-Group.

## Performance-Tuning {#performance-tuning}

### Betriebssystemebene {#os-level}

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

### JVM-Tuning (G1GC) {#jvm-tuning-g1gc}

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

Wichtige GC-Grundsätze:
- **6 GB Heap** ist für die meisten Workloads der optimale Wert. Größer bedeutet längere GC-Pausen.
- **G1GC** mit `MaxGCPauseMillis=20` hält die Tail-Latenz niedrig.
- `InitiatingHeapOccupancyPercent=35` startet die nebenläufige GC früh und verhindert so Full GCs.
- Überwachen Sie `java.lang:type=GarbageCollector,name=G1 Young Generation` und `G1 Old Generation` in JMX. Alarm auslösen, wenn Old-Gen-Collections mit > 0/min auftreten.

### Tuning auf Broker-Ebene {#broker-level-tuning}

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

## Stolperfallen {#gotchas}

- **Page-Cache-Thrashing.** Lesen Consumer sehr alte Daten (Catch-up-Reads), verdrängen sie aktuelle Daten aus dem Page Cache und verschlechtern die Echtzeit-Consumer. Verwenden Sie für historische Reads Tiered Storage oder separate Read-only-Follower.
- **Heap > 8 GB verursacht lange GC-Pausen.** Kafka hält nur wenig Zustand im Heap. Zusätzlicher RAM ist im Page Cache besser aufgehoben.
- **`UnderReplicatedPartitions > 0` bedeutet nicht zwingend einen Broker-Ausfall.** Ursachen können langsame Festplatten, Netzwerksättigung oder GC-Pausen sein. Prüfen Sie die Korrelation von `IsrShrinksPerSec` mit den GC-Logs.
- **Die `whitelistObjectNames` des JMX-Exporters sind wichtig.** Das Scrapen aller MBeans erzeugt Tausende Metriken und kann beim Exporter zu einem OOM führen. Setzen Sie nur die Metriken auf die Whitelist, für die Sie Alarme definieren.

## Siehe auch {#see-also}

- [[kafka-cluster-management]] - Sizing, Upgrades, Disk-Ausfälle, Partition-Reassignment
- [[kafka-backup-and-dr]] - MirrorMaker 2, Backup-Strategien, Disaster Recovery
- [[kafka-replication-fundamentals]] - ISR-Mechanik, Semantik des Replikationsrückstands
- [[consumer-groups]] - Rebalance-Protokolle, Offset-Management, Semantik des Consumer-Lags
- [[kafka-monitoring]] - weitere Monitoring-Muster und Tooling
