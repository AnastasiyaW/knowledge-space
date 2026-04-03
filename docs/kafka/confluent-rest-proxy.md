---
title: Confluent REST Proxy
category: reference
tags: [kafka, rest-proxy, http, confluent, api, producer, consumer]
---

# Confluent REST Proxy

The Confluent REST Proxy provides an HTTP-based interface to Kafka (default port 8082), enabling produce, consume, and metadata operations for environments without native Kafka clients.

## Key Facts

- Enables Kafka interaction via standard HTTP/REST - useful for languages without Kafka client libraries or firewall-restricted environments
- Supports JSON, Avro, Protobuf, JSON Schema, and binary (base64) message formats
- Consumer API is **stateful** - requires creating an instance, subscribing, then polling
- Consumer instances have timeout (`consumer.instance.timeout.ms`, default 5 min) - auto-deleted if no poll
- Part of Confluent Platform (not Apache Kafka core)
- Integrates with [[schema-registry]] for Avro/Protobuf serialization

## Patterns

### Produce Messages

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

### Consume Messages

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

### Metadata

```bash
curl http://localhost:8082/topics            # List topics
curl http://localhost:8082/topics/test       # Topic details
curl http://localhost:8082/topics/test/partitions  # Partitions
curl http://localhost:8082/brokers           # Broker list
curl http://localhost:8082/v3/clusters       # Cluster metadata
```

### Content Types

| Format | Content-Type |
|--------|-------------|
| JSON | `application/vnd.kafka.json.v2+json` |
| Avro | `application/vnd.kafka.avro.v2+json` |
| Protobuf | `application/vnd.kafka.protobuf.v2+json` |
| Binary | `application/vnd.kafka.binary.v2+json` |

## Gotchas

- **Consumer instances auto-expire** - if no poll within timeout (default 5 min), instance deleted; must recreate
- **REST Proxy adds latency** - HTTP overhead vs native binary protocol; not suitable for ultra-low-latency use cases
- **Not a replacement for native clients** - use for admin tasks, non-JVM environments, or when HTTP is the only allowed protocol

## See Also

- [[admin-api]] - programmatic cluster management (native Java)
- [[schema-registry]] - schema management for Avro/Protobuf via REST Proxy
- [Confluent REST Proxy Documentation](https://docs.confluent.io/platform/current/kafka-rest/)
