---
title: Docker Development Setup
category: reference
tags: [kafka, docker, docker-compose, kraft, development, local]
---

# Docker Development Setup

Minimal Docker Compose configurations for local Kafka development using KRaft mode (no ZooKeeper), with single-broker and multi-broker setups.

## Key Facts

- Single-broker KRaft setup is sufficient for development and testing
- Production requires 3+ brokers with replication
- `confluentinc/cp-kafka:latest` is the most common Docker image
- KRaft mode requires: `KAFKA_PROCESS_ROLES`, `KAFKA_CONTROLLER_QUORUM_VOTERS`, `CLUSTER_ID`
- Combined mode (`broker,controller`) suitable for development, not recommended for production >10 nodes
- CLI tools are inside the container at `/usr/bin/kafka-*`

## Patterns

### Single Broker (KRaft, Minimal)

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

### With Schema Registry and ksqlDB

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

### CLI Tools Usage

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

### Quick Start (No Docker)

```bash
# 1. Download Kafka from kafka.apache.org
# 2. Generate cluster UUID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# 3. Format storage
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

# 4. Start broker
bin/kafka-server-start.sh config/kraft/server.properties
```

## Gotchas

- **`KAFKA_ADVERTISED_LISTENERS` must be reachable by clients** - use `localhost` for local dev, container hostname for Docker networking
- **Multi-broker setup requires unique `KAFKA_NODE_ID` and port mappings** for each broker service
- **Single broker has no replication** - `replication-factor` must be 1; production needs 3+ brokers

## See Also

- [[broker-architecture]] - KRaft configuration, production settings
- [[kafka-cluster-operations]] - production deployment considerations
- [[topics-and-partitions]] - topic creation and configuration
