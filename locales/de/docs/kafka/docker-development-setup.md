---
title: "Docker-Entwicklungsumgebung"
category: reference
tags: [kafka, docker, docker-compose, kraft, development, local]
level: 3
source_sha256: ccedacfb89514af94bf9944d3a8850f6a3ca9b157cf19a0fe184d18281e663ea
translation: machine
translated_at: '2026-10-24'
---
# Docker-Entwicklungsumgebung {#docker-development-setup}

Minimale Docker-Compose-Konfigurationen für die lokale Kafka-Entwicklung im KRaft-Modus (ohne ZooKeeper), mit Single-Broker- und Multi-Broker-Setups.

## Kernfakten {#key-facts}

- Ein Single-Broker-KRaft-Setup reicht für Entwicklung und Tests aus
- Produktivbetrieb erfordert 3 oder mehr Broker mit Replikation
- `confluentinc/cp-kafka:latest` ist das am häufigsten verwendete Docker-Image
- Der KRaft-Modus erfordert: `KAFKA_PROCESS_ROLES`, `KAFKA_CONTROLLER_QUORUM_VOTERS`, `CLUSTER_ID`
- Der kombinierte Modus (`broker,controller`) eignet sich für die Entwicklung, wird für Produktivumgebungen mit mehr als 10 Knoten nicht empfohlen
- CLI-Tools befinden sich im Container unter `/usr/bin/kafka-*`

## Muster {#patterns}

### Single Broker (KRaft, minimal) {#single-broker-kraft-minimal}

```yaml
version: '3'
services:
  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LOG_DIRS: /var/lib/kafka/data
      CLUSTER_ID: "MkU3OEVBNTcwNTJENDM2Qg"
```

### Mit Schema Registry und ksqlDB {#with-schema-registry-and-ksqldb}

```yaml
version: '3'
services:
  kafka:
    image: confluentinc/cp-kafka:latest
    ports: ["9092:9092"]
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      CLUSTER_ID: "MkU3OEVBNTcwNTJENDM2Qg"

  schema-registry:
    image: confluentinc/cp-schema-registry:latest
    ports: ["8081:8081"]
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka:9092
    depends_on: [kafka]

  ksqldb:
    image: confluentinc/ksqldb-server:latest
    ports: ["8088:8088"]
    environment:
      KSQL_BOOTSTRAP_SERVERS: kafka:9092
      KSQL_KSQL_SCHEMA_REGISTRY_URL: http://schema-registry:8081
    depends_on: [kafka, schema-registry]
```

### Verwendung der CLI-Tools {#cli-tools-usage}

```bash
# Create topic
docker exec -it kafka kafka-topics --create \
  --topic test --partitions 3 --replication-factor 1 \
  --bootstrap-server localhost:9092

# Produce
docker exec -it kafka kafka-console-producer \
  --topic test --bootstrap-server localhost:9092

# Consume
docker exec -it kafka kafka-console-consumer \
  --topic test --from-beginning --bootstrap-server localhost:9092

# Describe consumer group
docker exec -it kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 --group my-group --describe
```

### Schnellstart (ohne Docker) {#quick-start-no-docker}

```bash
# 1. Download Kafka from kafka.apache.org
# 2. Generate cluster UUID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# 3. Format storage
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

# 4. Start broker
bin/kafka-server-start.sh config/kraft/server.properties
```

## Stolperfallen {#gotchas}

- **`KAFKA_ADVERTISED_LISTENERS` muss von Clients erreichbar sein** - für die lokale Entwicklung `localhost` verwenden, für Docker-Networking den Container-Hostnamen
- **Ein Multi-Broker-Setup erfordert eindeutige `KAFKA_NODE_ID`s und Port-Mappings** für jeden Broker-Service
- **Ein Single Broker hat keine Replikation** - `replication-factor` muss 1 sein; Produktivbetrieb erfordert 3 oder mehr Broker

## Siehe auch {#see-also}

- [[broker-architecture]] - KRaft-Konfiguration, Produktionseinstellungen
- [[kafka-cluster-management]] - Überlegungen zum Produktivbetrieb
- [[topics-and-partitions]] - Erstellung und Konfiguration von Topics
