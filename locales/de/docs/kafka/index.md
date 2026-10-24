---
title: "Kafka & Message Queues"
type: MOC
level: 3
source_sha256: 435a580e2d2b0365545772cdef275bf6602a1ab2c83732d14cc5fb0cf5403b2b
translation: machine
translated_at: '2026-10-24'
---
# Kafka & Message Queues {#kafka-message-queues}

## Kernkonzepte {#core-concepts}
- [[broker-architecture]] - Broker-Cluster, Controller-Wahl (ZooKeeper/KRaft), Log-Segmente, Retention
- [[topics-and-partitions]] - Topics, Partitionen, Reihenfolge, schlüsselbasiertes Routing, Cleanup-Policies
- [[consumer-groups]] - Gruppenprotokoll, Partitionszuweisung, Offset-Verwaltung, Rebalancing
- [[kafka-replication-fundamentals]] - ISR, HW/LEO, acks + min.insync.replicas
- [[kafka-fault-tolerance]] - Unclean Leader Election, Rack-aware Replikation, Multi-DC-Muster

## Stream Processing {#stream-processing}
- [[kafka-streams]] - KStream/KTable, zustandsbehaftete Operationen, Windowing, Joins, Exactly-once, interaktive Abfragen
- [[ksqldb]] - SQL über Streams, Push-/Pull-Abfragen, fensterbasierte Aggregationen, persistente Abfragen

## Integration {#integration}
- [[kafka-connect]] - Source- und Sink-Connectors, SMTs, REST-API, DLQ, Fehlerbehandlung
- [[schema-registry]] - Schema-Evolution, Kompatibilitätsmodi, Avro/Protobuf/JSON Schema, Subject-Strategien

## Muster & Best Practices {#patterns-best-practices}
- [[kafka-producer-fundamentals]] - Acks-Modi, Batching, Komprimierung, Retries, Sendemuster
- [[kafka-producer-advanced-patterns]] - Eigene Partitioner, Header, Interceptors, Backpressure, idempotenter Producer
- [[kafka-transactions]] - Idempotenter Producer, transaktionale API, Exactly-once-Semantik, Zombie-Fencing

## Betrieb & Sicherheit {#operations-security}
- [[kafka-cluster-management]] - Dimensionierung, Rolling Upgrades, Plattenausfälle, Partition-Reassignment
- [[kafka-monitoring-and-tuning]] - JMX-Metriken, Prometheus/Grafana, OS-/JVM-/Broker-Tuning
- [[kafka-backup-and-dr]] - MirrorMaker 2, Backup-Strategien, Muster für Disaster Recovery
- [[kafka-security]] - SSL/TLS, SASL, ACLs, Listener, RBAC, Audit-Logging

## Weiterführende Referenzen {#additional-references}

- [[admin-api]] - Die Admin API (kafka-clients-Bibliothek) bietet programmatische Cluster-Verwaltung für Topics, Consumer
- [[alpakka-kafka]] - Alpakka Kafka verbindet Kafka-Topics mit Akka-Streams-Pipelines und bietet reaktives Backpressure
- [[confluent-rest-proxy]] - Der Confluent REST Proxy bietet eine HTTP-basierte Schnittstelle zu Kafka (Standardport 8082) und ermöglicht
- [[consumer-configuration]] - Vollständige Referenz der Kafka-Consumer-Konfigurationsparameter mit Standardwerten und Tuning-Richtlinien
- [[cqrs-pattern]] - CQRS (Command Query Responsibility Segregation) trennt den Schreibpfad (Command API mit Event
- [[delivery-semantics]] - Kafka unterstützt drei Delivery-Semantiken – at-most-once, at-least-once und exactly-once – jeweils mit
- [[docker-development-setup]] - Minimale Docker-Compose-Konfigurationen für die lokale Kafka-Entwicklung im KRaft-Modus (ohne ZooKeeper)
- [[event-sourcing]] - Event Sourcing speichert jede Zustandsänderung als unveränderliches Event in Kafka, statt Daten zu überschreiben
- [[idempotent-producer]] - Der idempotente Producer weist jeder Nachricht eine PID (Producer ID) und Sequenznummern zu, wodurch ermöglicht wird
- [[kafka-messaging-fundamentals]] - Kafka-Zustellungsgarantien, Mechanik von Consumer-Gruppen, Rebalancing-Strategien und Integration
- [[kafka-monitoring]] - Kafka stellt Metriken über JMX bereit
- [[kafka-queues-v4]] - Kafka 4.0 führt Work-Queue-Semantik ein, bei der jede Nachricht von nur einem Consumer in einer
- [[kafka-streams-state-stores]] - State Stores bieten lokalen Key-Value-Speicher pro Kafka-Streams-Task, gestützt auf RocksDB auf der Festplatte und
- [[kafka-streams-time-semantics]] - Zeitsemantik für Stream Processing auf Basis des Google-Dataflow-Modells legt fest, wie Events gruppiert werden
- [[kafka-streams-windowing]] - Fensteroperationen gruppieren Stream-Records in endliche Zeitintervalle für Aggregationen und unterstützen
- [[kafka-troubleshooting]] - Häufige Kafka-Probleme, zugeordnet zu Symptomen, Ursachen und Behebungen sowohl auf Producer- als auch auf
- [[messaging-models]] - In verteilten Systemen existieren drei grundlegende Messaging-Modelle
- [[mirrormaker]] - MirrorMaker 2 (MM2) repliziert Topics zwischen Kafka-Clustern für Disaster Recovery und
- [[nats-comparison]] - NATS ist ein leichtgewichtiges Messaging-System mit drei Schichten (Core, JetStream, Clustering) und bietet
- [[offsets-and-commits]] - Ein Offset ist eine fortlaufende Nachrichtennummer innerhalb einer Partition, die beim Schreiben vergeben wird
- [[partitioning-strategies]] - Das Partitionieren in Kafka bestimmt, wie Nachrichten über Partitionen verteilt werden, mittels Key-Hashing
- [[rebalancing-deep-dive]] - Rebalancing ist der Prozess der Neuverteilung von Partitionszuweisungen auf die Consumer einer Gruppe
- [[saga-pattern]] - Das Saga-Pattern verwaltet verteilte Transaktionen über Microservices hinweg via Kafka, entweder
- [[spring-kafka]] - Spring Kafka bietet deklarative, annotationsbasierte Kafka-Integration mit KafkaTemplate für
- [[transactional-outbox]] - Das Transactional-Outbox-Pattern schreibt Events in eine Outbox-Tabelle innerhalb derselben Datenbank
- [[zero-copy-and-disk-io]] - Kafka erreicht hohen Durchsatz durch sequenzielle Festplatten-I/O, Nutzung des OS-Page-Caches und
- [[zio-kafka]] - ZIO Kafka bietet rein funktionale Kafka-Integration mit ZIO Streams und umhüllt die Standard-
