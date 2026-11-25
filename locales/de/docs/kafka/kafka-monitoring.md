---
title: "Kafka-Überwachung"
category: reference
tags: [kafka, monitoring, jmx, prometheus, grafana, metrics, alerting, consumer-lag]
level: 4
source_sha256: 2eac4de176bdf6e91dcf6b2771e902344762680dc37e9a37423d4f4300bb53dd
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Überwachung {#kafka-monitoring}

Kafka stellt Metriken über JMX bereit; ein produktiver Betrieb erfordert die Überwachung des Broker-Zustands, des Replikationsstatus, des Consumer-Lags und der Request-Latenz, jeweils mit Alarmierung bei kritischen Schwellenwerten.

## Kernfakten {#key-facts}

- Kafka-Metriken werden über JMX (Java Management Extensions) bereitgestellt
- Empfohlener Stack: Prometheus + Grafana mit vorgefertigten Kafka-Dashboards
- Der Consumer-Lag ist die wichtigste Metrik für den Zustand der Anwendung
- Die Festplattenüberwachung hat höchste Priorität – erschöpfter Festplattenspeicher ist die häufigste Ursache für Kafka-Ausfälle
- Confluent Control Center bietet eine Web-Oberfläche zur Überwachung (Port 9021), ist jedoch ein kommerzielles Produkt

## Muster {#patterns}

### Kritische Broker-Metriken {#critical-broker-metrics}

```markdown
# Cluster-level (MUST alert on these)
kafka.controller:type=KafkaController,name=ActiveControllerCount   # MUST be exactly 1
kafka.controller:type=KafkaController,name=OfflinePartitionsCount   # MUST be 0
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions     # should be 0
kafka.controller:type=KafkaController,name=UncleanLeaderElectionsPerSec  # MUST be 0

# Broker throughput
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec

# Replication health
kafka.server:type=ReplicaManager,name=IsrShrinksPerSec     # spikes = trouble
kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount  # ISR < minIsr

# Request latency
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce   # p99 latency
kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Fetch

# Disk
kafka.log:type=LogFlushRateAndTimeMs   # disk flush latency

# Thread utilization
kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent
kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent
```

### Alarmschwellenwerte {#alert-thresholds}

| Metrik | Alarmschwellenwert | Schweregrad |
|--------|----------------|----------|
| `ActiveControllerCount` | != 1 (Summe über den Cluster) | Kritisch |
| `OfflinePartitionsCount` | > 0 | Kritisch |
| `UnderReplicatedPartitions` | > 0 für > 5 Min | Warnung |
| `UncleanLeaderElectionsPerSec` | > 0 | Kritisch (potenzieller Datenverlust) |
| `UnderMinIsrPartitionCount` | > 0 | Warnung (für acks=all nicht verfügbar) |
| `IsrShrinksPerSec` | anhaltende Spitzen | Warnung |
| Consumer-Lag | über die Zeit wachsend | Warnung |
| Festplattenbelegung | > 80 % | Warnung |
| Request-Latenz p99 | > 1 s | Warnung |

### Überwachung des Consumer-Lags {#consumer-lag-monitoring}

```bash
# CLI monitoring
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe

# Output columns:
# GROUP  TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG  CONSUMER-ID
```

Consumer-Lag = `LOG-END-OFFSET - CURRENT-OFFSET`. Ein wachsender Lag bedeutet, dass die Consumer nicht mithalten können.

### Tuning der Broker-Threads {#broker-thread-tuning}

```properties
# Network threads: handle incoming connections
num.network.threads=3     # Monitor idle%; if < 30%, increase
# 10,000 connections sufficient for most deployments

# I/O threads: handle disk operations
num.io.threads=8          # Monitor idle%; more = better disk utilization

# Total request capacity = network threads + I/O threads
```

### Zu erfassende Consumer-Metriken {#consumer-metrics-to-track}

```markdown
# Java producer/consumer metrics
record-send-rate           # messages sent per second
record-error-rate          # send failures per second
batch-size-avg             # average batch size
buffer-available-bytes     # producer buffer remaining
request-latency-avg        # average request latency
produce-throttle-time-avg  # broker-side throttling time
```

## Fallstricke {#gotchas}

- **`OfflinePartitionsCount > 0` erfordert sofortige Untersuchung** – Partitionen ohne aktiven Leader sind weder schreib- noch lesbar
- **`UnderReplicatedPartitions > 0` über einen längeren Zeitraum** – E/A der Festplatte, Netzwerk und GC-Pausen auf den zurückliegenden Brokern prüfen
- **Das Zusammenspiel von Segmenten und Retention verursacht unerwarteten Festplattenverbrauch** – die tatsächliche Datenlebensdauer kann die konfigurierte Retention überschreiten, da die Retention nur für geschlossene Segmente gilt
- **Unclean Leader Election** – Kafka wählt einen nicht synchronisierten Replica als Leader; das führt zum Abschneiden des Logs und damit zu Datenverlust; ausgelöst durch Quorum-Ausfälle, Netzwerkpartitionen, langsame Festplatten oder GC-Pausen
- **Wachsender Consumer-Lag = Verarbeitungsproblem, nicht Kafka-Problem** – Partitionen und Consumer erhöhen, die Verarbeitungslogik optimieren oder die Batch-Größen vergrößern

## Siehe auch {#see-also}

- [[broker-architecture]] – Interna des Brokers, Referenz der JMX-Metriken
- [[kafka-replication-fundamentals]] – ISR-Mechanik, Bedeutung von UnderReplicated
- [[kafka-cluster-management]] – Betriebsprozesse, Kapazitätsplanung
- [[kafka-monitoring-and-tuning]] – Referenz der JMX-Metriken, Prometheus-Einrichtung, Performance-Tuning
- [[kafka-troubleshooting]] – Zuordnung von Symptomen zu Lösungen
- [Apache Kafka Monitoring](https://kafka.apache.org/documentation/#monitoring)
