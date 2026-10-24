---
title: "Configuration Docker pour le développement"
category: reference
tags: [kafka, docker, docker-compose, kraft, development, local]
level: 3
source_sha256: ccedacfb89514af94bf9944d3a8850f6a3ca9b157cf19a0fe184d18281e663ea
translation: machine
translated_at: '2026-10-24'
---
# Configuration Docker pour le développement {#docker-development-setup}

Configurations Docker Compose minimales pour le développement local de Kafka en mode KRaft (sans ZooKeeper), avec des configurations à un seul broker et à plusieurs brokers.

## Points clés {#key-facts}

- Une configuration KRaft à un seul broker suffit pour le développement et les tests
- La production nécessite 3 brokers ou plus avec réplication
- `confluentinc/cp-kafka:latest` est l'image Docker la plus courante
- Le mode KRaft nécessite : `KAFKA_PROCESS_ROLES`, `KAFKA_CONTROLLER_QUORUM_VOTERS`, `CLUSTER_ID`
- Le mode combiné (`broker,controller`) convient au développement, mais n'est pas recommandé en production au-delà de 10 nœuds
- Les outils en ligne de commande se trouvent dans le conteneur, à l'emplacement `/usr/bin/kafka-*`

## Schémas d'utilisation {#patterns}

### Broker unique (KRaft, minimal) {#single-broker-kraft-minimal}

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

### Avec Schema Registry et ksqlDB {#with-schema-registry-and-ksqldb}

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

### Utilisation des outils en ligne de commande {#cli-tools-usage}

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

### Démarrage rapide (sans Docker) {#quick-start-no-docker}

```bash
# 1. Download Kafka from kafka.apache.org
# 2. Generate cluster UUID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# 3. Format storage
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

# 4. Start broker
bin/kafka-server-start.sh config/kraft/server.properties
```

## Pièges à éviter {#gotchas}

- **`KAFKA_ADVERTISED_LISTENERS` doit être accessible par les clients** - utilisez `localhost` pour le développement local, et le nom d'hôte du conteneur pour le réseau Docker
- **La configuration multi-brokers nécessite un `KAFKA_NODE_ID` unique et des correspondances de ports distinctes** pour chaque service broker
- **Un broker unique n'offre aucune réplication** - `replication-factor` doit valoir 1 ; la production nécessite 3 brokers ou plus

## Voir aussi {#see-also}

- [[broker-architecture]] - configuration KRaft, paramètres de production
- [[kafka-cluster-management]] - considérations relatives au déploiement en production
- [[topics-and-partitions]] - création et configuration des topics
