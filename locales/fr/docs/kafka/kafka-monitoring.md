---
title: "Surveillance de Kafka"
category: reference
tags: [kafka, monitoring, jmx, prometheus, grafana, metrics, alerting, consumer-lag]
level: 4
source_sha256: 2eac4de176bdf6e91dcf6b2771e902344762680dc37e9a37423d4f4300bb53dd
translation: machine
translated_at: '2026-10-24'
---
# Surveillance de Kafka {#kafka-monitoring}

Kafka expose ses métriques via JMX ; la surveillance en production exige de suivre la santé des brokers, l'état de réplication, le retard des consommateurs (consumer lag) et la latence des requêtes, avec des alertes sur les seuils critiques.

## Points clés {#key-facts}

- Métriques Kafka exposées via JMX (Java Management Extensions)
- Stack recommandée : Prometheus + Grafana avec des tableaux de bord Kafka préconfigurés
- Le consumer lag est la métrique de santé applicative la plus critique
- La surveillance du disque est la priorité n° 1 : l'épuisement du disque est la cause de panne la plus fréquente de Kafka
- Confluent Control Center fournit une interface web de surveillance (port 9021) mais est un produit commercial

## Modèles {#patterns}

### Métriques critiques des brokers {#critical-broker-metrics}

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

### Seuils d'alerte {#alert-thresholds}

| Métrique | Seuil d'alerte | Gravité |
|--------|----------------|----------|
| `ActiveControllerCount` | != 1 (somme sur le cluster) | Critique |
| `OfflinePartitionsCount` | > 0 | Critique |
| `UnderReplicatedPartitions` | > 0 pendant > 5 min | Avertissement |
| `UncleanLeaderElectionsPerSec` | > 0 | Critique (perte de données potentielle) |
| `UnderMinIsrPartitionCount` | > 0 | Avertissement (indisponible pour acks=all) |
| `IsrShrinksPerSec` | pics soutenus | Avertissement |
| Consumer lag | en croissance dans le temps | Avertissement |
| Utilisation du disque | > 80 % | Avertissement |
| Latence des requêtes p99 | > 1 s | Avertissement |

### Surveillance du consumer lag {#consumer-lag-monitoring}

```bash
# CLI monitoring
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe

# Output columns:
# GROUP  TOPIC  PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG  CONSUMER-ID
```

Consumer lag = `LOG-END-OFFSET - CURRENT-OFFSET`. Un lag croissant signifie que les consommateurs ne parviennent pas à suivre le rythme.

### Réglage des threads du broker {#broker-thread-tuning}

```properties
# Network threads: handle incoming connections
num.network.threads=3     # Monitor idle%; if < 30%, increase
# 10,000 connections sufficient for most deployments

# I/O threads: handle disk operations
num.io.threads=8          # Monitor idle%; more = better disk utilization

# Total request capacity = network threads + I/O threads
```

### Métriques des consommateurs à suivre {#consumer-metrics-to-track}

```markdown
# Java producer/consumer metrics
record-send-rate           # messages sent per second
record-error-rate          # send failures per second
batch-size-avg             # average batch size
buffer-available-bytes     # producer buffer remaining
request-latency-avg        # average request latency
produce-throttle-time-avg  # broker-side throttling time
```

## Pièges {#gotchas}

- **`OfflinePartitionsCount > 0` nécessite une investigation immédiate** : les partitions sans leader actif ne sont ni inscriptibles ni lisibles
- **`UnderReplicatedPartitions > 0` pendant une période prolongée** : vérifier les E/S disque, le réseau et les pauses GC sur les brokers en retard
- **L'interaction entre segments et rétention provoque une utilisation disque inattendue** : la durée de vie réelle des données peut dépasser la rétention configurée, car la rétention ne s'applique qu'aux segments fermés
- **Élection de leader non propre (Unclean Leader Election)** : Kafka sélectionne un réplica désynchronisé comme leader ; cela entraîne une troncature du journal, donc une perte de données ; déclenchée par des pannes de quorum, des partitions réseau, des disques lents ou des pauses GC
- **Un consumer lag croissant relève d'un problème de traitement, pas d'un problème Kafka** : ajouter des partitions et des consommateurs, optimiser la logique de traitement ou augmenter la taille des lots

## Voir aussi {#see-also}

- [[broker-architecture]] - fonctionnement interne des brokers, référence des métriques JMX
- [[kafka-replication-fundamentals]] - mécanismes ISR, signification de UnderReplicated
- [[kafka-cluster-management]] - procédures opérationnelles, planification de la capacité
- [[kafka-monitoring-and-tuning]] - référence des métriques JMX, mise en place de Prometheus, réglage des performances
- [[kafka-troubleshooting]] - correspondance symptômes-solutions
- [Apache Kafka Monitoring](https://kafka.apache.org/documentation/#monitoring)
