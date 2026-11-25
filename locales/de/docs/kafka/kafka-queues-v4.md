---
title: "Kafka Queues (v4.0)"
category: concepts
tags: [kafka, queues, kafka-4, work-queue, virtual-partitions]
level: 2
source_sha256: 3f8a61706dbc8c5ca005f4ac245d5b0f3dfc01042d160c9a76d7c0de2f801eed
translation: machine
translated_at: '2026-10-24'
---
# Kafka Queues (v4.0) {#kafka-queues-v40}

Kafka 4.0 führt Work-Queue-Semantik ein, bei der jede Nachricht von nur einem Consumer innerhalb einer Gruppe verarbeitet wird. Die Skalierung erfolgt automatisch und ohne Rebalancing, intern werden virtuelle Partitionen verwendet.

## Wichtige Fakten {#key-facts}

- Aktiviert über `queue.topic.enable=true` am Topic
- Jede Nachricht wird von nur EINEM Consumer in der Gruppe verarbeitet (Competing-Consumers-Muster)
- Automatische Skalierung ohne Rebalancing (im Gegensatz zu klassischen Consumer-Gruppen)
- Partitionierung ist für den Client verborgen: Die Verteilung erfolgt intern über virtuelle Partitionen
- Schließt die Lücke zwischen Kafkas Log-Modell und dem Verhalten klassischer Message Queues
- Teil des Kafka-4.0-Releases zusammen mit dem reinen KRaft-Betrieb (ZooKeeper vollständig entfernt) und Tiered Storage

## Muster {#patterns}

### Zusammenfassung der Funktionen in Kafka 4.0 {#kafka-40-feature-summary}

| Funktion | Status |
|---------|--------|
| KRaft (ZooKeeper entfernt) | Standard in Produktion |
| Kafka Queues | Neu in 4.0 |
| Tiered Storage | GA in 4.0 |

### Tiered Storage {#tiered-storage}

```properties
# Enable tiered storage
remote.log.enabled=true
# Recent data on local disk, older segments on remote tier (S3, HDFS)
# Extended retention without overwhelming local storage
```

## Stolperfallen {#gotchas}

- **Kafka Queues ist neu in v4.0** - die Unterstützung im Ökosystem kann zunächst eingeschränkt sein
- **Kein Ersatz für RabbitMQ** - Kafka Queues ergänzt Queue-Semantik, Kafkas Architektur bleibt jedoch log-basiert
- **Virtuelle Partitionen sind intern** - Du konfigurierst sie nicht und siehst sie nicht; die Verteilung erfolgt automatisch

## Siehe auch {#see-also}

- [[messaging-models]] - Queue- vs. Pub-Sub- vs. Log-basierte Modelle
- [[consumer-groups]] - klassische Consumer-Gruppen-Semantik in Kafka
- [[broker-architecture]] - KRaft-Modus, Änderungen in Kafka 4.0
- [KIP-932: Queues für Kafka](https://cwiki.apache.org/confluence/display/KAFKA/KIP-932)
