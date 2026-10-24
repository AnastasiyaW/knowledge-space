---
title: "Confluent REST Proxy"
category: reference
tags: [kafka, rest-proxy, http, confluent, api, producer, consumer]
level: 3
source_sha256: dd5c0cc69fbc9868076a0a2e2b76664d9e8b309437d9bfb92459a225b202fc4f
translation: machine
translated_at: '2026-10-24'
---
# Confluent REST Proxy {#confluent-rest-proxy}

Der Confluent REST Proxy stellt eine HTTP-basierte Schnittstelle zu Kafka bereit (Standardport 8082) und ermöglicht Produce-, Consume- und Metadaten-Operationen in Umgebungen ohne native Kafka-Clients.

## Key Facts {#key-facts}

- Ermöglicht die Interaktion mit Kafka über standardmäßiges HTTP/REST – nützlich für Sprachen ohne Kafka-Client-Bibliotheken oder firewallbeschränkte Umgebungen
- Unterstützt die Nachrichtenformate JSON, Avro, Protobuf, JSON Schema und Binary (Base64)
- Die Consumer-API ist **zustandsbehaftet** – man muss zuerst eine Instanz erstellen, sie abonnieren und anschließend Polling betreiben
- Consumer-Instanzen haben ein Timeout (`consumer.instance.timeout.ms`, Standard 5 Min.) – sie werden automatisch gelöscht, wenn kein Poll erfolgt
- Teil der Confluent Platform (nicht des Apache-Kafka-Kerns)
- Integriert sich mit [[schema-registry]] für die Avro-/Protobuf-Serialisierung

## Patterns {#patterns}

### Produce Messages {#produce-messages}

```bash
# JSON
curl -X POST http://localhost:8082/topics/test \
  -H "Content-Type: application/vnd.kafka.json.v2+json" \
  -d '{"records": [{"key": "k1", "value": {"name": "John"}}]}'

# Avro (requires Schema Registry)
curl -X POST http://localhost:8082/topics/test-avro \
  -H "Content-Type: application/vnd.kafka.avro.v2+json" \
  -d '{"value_schema": "...", "records": [{"value": {"name": "John"}}]}'

# Binary (base64)
curl -X POST http://localhost:8082/topics/test-bin \
  -H "Content-Type: application/vnd.kafka.binary.v2+json" \
  -d '{"records": [{"value": "aGVsbG8="}]}'
```

### Consume Messages {#consume-messages}

```bash
# 1. Create consumer instance
curl -X POST http://localhost:8082/consumers/my-group \
  -H "Content-Type: application/vnd.kafka.v2+json" \
  -d '{"name": "my-consumer", "format": "json", "auto.offset.reset": "earliest"}'

# 2. Subscribe
curl -X POST http://localhost:8082/consumers/my-group/instances/my-consumer/subscription \
  -H "Content-Type: application/vnd.kafka.v2+json" \
  -d '{"topics": ["test"]}'

# 3. Poll
curl http://localhost:8082/consumers/my-group/instances/my-consumer/records \
  -H "Accept: application/vnd.kafka.json.v2+json"

# 4. Commit offsets
curl -X POST http://localhost:8082/consumers/my-group/instances/my-consumer/offsets

# 5. Delete instance
curl -X DELETE http://localhost:8082/consumers/my-group/instances/my-consumer
```

### Metadata {#metadata}

```bash
curl http://localhost:8082/topics            # List topics
curl http://localhost:8082/topics/test       # Topic details
curl http://localhost:8082/topics/test/partitions  # Partitions
curl http://localhost:8082/brokers           # Broker list
curl http://localhost:8082/v3/clusters       # Cluster metadata
```

### Content Types {#content-types}

| Format | Content-Type |
|--------|-------------|
| JSON | `application/vnd.kafka.json.v2+json` |
| Avro | `application/vnd.kafka.avro.v2+json` |
| Protobuf | `application/vnd.kafka.protobuf.v2+json` |
| Binary | `application/vnd.kafka.binary.v2+json` |

## Gotchas {#gotchas}

- **Consumer-Instanzen laufen automatisch ab** – erfolgt innerhalb des Timeouts (Standard 5 Min.) kein Poll, wird die Instanz gelöscht und muss neu erstellt werden
- **REST Proxy erhöht die Latenz** – HTTP-Overhead gegenüber dem binären Protokoll nativer Clients; nicht geeignet für Anwendungsfälle mit extrem niedriger Latenz
- **Kein Ersatz für native Clients** – verwenden für Administrationsaufgaben, Nicht-JVM-Umgebungen oder wenn HTTP das einzig erlaubte Protokoll ist

## See Also {#see-also}

- [[admin-api]] – programmatische Clusterverwaltung (native Java-API)
- [[schema-registry]] – Schemaverwaltung für Avro/Protobuf über den REST Proxy
- [Confluent REST Proxy Documentation](https://docs.confluent.io/platform/current/kafka-rest/)
