---
title: Schema Registry
category: concepts
tags: [kafka, schema, avro, protobuf, json-schema, compatibility, serialization]
---

# Schema Registry

Confluent Schema Registry is a serving layer for schema metadata. It stores versioned schemas in the `_schemas` compacted topic in Kafka, exposes a REST API for registration, retrieval, and compatibility checks, and integrates with Kafka clients via serializers/deserializers that embed a 4-byte schema ID in each message. Supports Avro, Protobuf, and JSON Schema. Critical dependency for [[kafka-connect]] converters, [[kafka-streams]] serdes, and any producer/consumer pipeline that needs schema evolution guarantees.

## Architecture

```
Producer / Consumer          Schema Registry (port 8081)         Kafka Cluster
   |                              |                                  |
   |--- register schema --------->|                                  |
   |<-- schema id (int32) --------|--- store in _schemas topic ----->|
   |                              |                                  |
   |--- serialize: [0][id][data]->|                                  |
   |                              |                                  |
   |--- GET /schemas/ids/{id} --->|--- read from _schemas cache ---->|
   |<-- full schema definition ---|                                  |
```

### Wire Format (Confluent framing)

Every message serialized through the Schema Registry serializer follows this binary layout:

```
| magic byte (0x0) | schema ID (4 bytes, big-endian) | payload (Avro/Protobuf/JSON) |
```

Total overhead: 5 bytes per message. The deserializer reads the schema ID, fetches the writer schema from the registry (cached locally), and deserializes the payload using that schema.

### `_schemas` Topic

- Compacted topic, single partition, RF = 3 (production)
- Stores all registered schemas, subjects, compatibility configs, and schema references
- Schema Registry instances are **stateless** - all state lives in this topic
- On startup, each instance reads `_schemas` from the beginning to rebuild its in-memory cache
- Leader election: one instance becomes the "primary" (writes), others are read-only followers
- `kafkastore.connection.url` (ZooKeeper) or `kafkastore.bootstrap.servers` (KRaft) for cluster connection

## Subjects and Naming Strategies

A **subject** is the unit of schema versioning and compatibility enforcement. Subject naming strategy determines how schemas map to subjects.

### TopicNameStrategy (default)

```
subject = "{topic}-key" | "{topic}-value"
```

One schema per topic (per key/value). Simple. Breaks when you need multiple event types in a single topic.

```properties
# Producer config
value.subject.name.strategy=io.confluent.kafka.serializers.subject.TopicNameStrategy
```

### RecordNameStrategy

```
subject = "{fully.qualified.record.name}"
```

Schema is scoped by the record's full name (namespace + name). Topic-independent. Enables multiple event types per topic. Compatibility is checked per record type, not per topic.

```properties
value.subject.name.strategy=io.confluent.kafka.serializers.subject.RecordNameStrategy
```

Use case: event sourcing topic with `OrderCreated`, `OrderShipped`, `OrderCancelled` - each evolves independently.

### TopicRecordNameStrategy

```
subject = "{topic}-{fully.qualified.record.name}"
```

Combines both: same record type can have different schemas on different topics.

```properties
value.subject.name.strategy=io.confluent.kafka.serializers.subject.TopicRecordNameStrategy
```

Use case: same `User` record on `users-v1` and `users-v2` topics with different evolution paths.

### Custom Naming Strategy

Implement `SubjectNameStrategy` interface:

```java
public class CustomStrategy implements SubjectNameStrategy {
    @Override
    public String subjectName(String topic, boolean isKey, ParsedSchema schema) {
        return "custom-" + topic + "-" + schema.name();
    }
}
```

## Compatibility Modes

Compatibility is enforced **per subject** on schema registration. The registry rejects schemas that violate the configured compatibility level.

### Compatibility Matrix

| Mode | New schema must... | Who updates first | Use case |
|------|-------------------|-------------------|----------|
| `BACKWARD` (default) | Read data written with the previous version | Consumer (deploy new consumer, then new producer) | Add optional fields, remove fields |
| `BACKWARD_TRANSITIVE` | Read data written with ALL previous versions | Consumer | Long-lived data in storage (S3, HDFS) |
| `FORWARD` | Be readable by consumers using the previous schema | Producer (deploy new producer, then new consumer) | Add fields, remove optional fields |
| `FORWARD_TRANSITIVE` | Be readable by consumers using ANY previous version | Producer | Rolling deploys where old consumers linger |
| `FULL` | Both BACKWARD and FORWARD compatible | Either | Maximum safety, strictest evolution rules |
| `FULL_TRANSITIVE` | FULL compatibility with ALL previous versions | Either | Regulated environments, critical data |
| `NONE` | No check | Either | Development, prototyping only |

### Transitive vs Non-Transitive

- **Non-transitive** (default): compatibility checked only against the **last registered** version
- **Transitive**: compatibility checked against **every** previously registered version

Example where transitive matters:
- v1: `{name: string}`
- v2: `{name: string, age: int (default 0)}` - BACKWARD compatible with v1
- v3: `{name: string}` (remove age) - BACKWARD compatible with v2 but NOT with v1 if v1 data still exists
- `BACKWARD_TRANSITIVE` would reject v3 because old v1-era data cannot be read with v3

## Schema Evolution Rules by Format

### Avro Evolution

| Change | BACKWARD | FORWARD | FULL |
|--------|----------|---------|------|
| Add field with default | Yes | Yes | Yes |
| Add field without default | No | Yes | No |
| Remove field with default | Yes | No | No |
| Remove field without default | Yes | No | No |
| Rename field (via alias) | Yes | Yes | Yes |
| Widen type (int -> long) | Yes | No | No |
| Narrow type (long -> int) | No | Yes | No |

```json
{
  "type": "record",
  "name": "UserEvent",
  "namespace": "com.example.events",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null},
    {"name": "age", "type": "int", "default": 0},
    {"name": "tags", "type": {"type": "array", "items": "string"}, "default": []}
  ]
}
```

Key rule: **always provide defaults for new fields** in Avro. This ensures both BACKWARD and FORWARD compatibility.

### Protobuf Evolution

| Change | BACKWARD | FORWARD | FULL |
|--------|----------|---------|------|
| Add optional field | Yes | Yes | Yes |
| Remove optional field | Yes | Yes | Yes |
| Add required field | No | No | No |
| Remove required field | No | No | No |
| Rename field (same number) | Yes | Yes | Yes |
| Change field number | No | No | No |
| Add enum value | Yes (with `reserved`) | Yes | Yes |
| Reorder fields | Yes | Yes | Yes |

```protobuf
syntax = "proto3";
package com.example.events;

message UserEvent {
  int64 id = 1;
  string name = 2;
  optional string email = 3;
  int32 age = 4;
  repeated string tags = 5;
  // reserved 6; // field removed in v3, reserve to prevent reuse
}
```

Proto3: all fields are implicitly optional (have defaults). Proto2 `required` fields break evolution.

### JSON Schema Evolution

| Change | BACKWARD | FORWARD | FULL |
|--------|----------|---------|------|
| Add optional property | Yes | Yes | Yes |
| Add required property | No | Yes | No |
| Remove optional property | Yes | No | No |
| Remove required property | Yes | No | No |
| Make required -> optional | Yes | No | No |
| Make optional -> required | No | Yes | No |
| Widen type (integer -> number) | Yes | No | No |

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "email": {"type": "string"},
    "age": {"type": "integer", "default": 0}
  },
  "required": ["id", "name"],
  "additionalProperties": false
}
```

Warning: `"additionalProperties": false` blocks FORWARD compatibility (old consumer rejects unknown fields from new producer).

## Schema References

Schema references enable schema composition - one schema can reference another registered schema. Critical for Protobuf imports and Avro named types shared across schemas.

### Protobuf References

```protobuf
// address.proto - registered as subject "Address"
syntax = "proto3";
message Address {
  string street = 1;
  string city = 2;
  string country = 3;
}
```

```protobuf
// user.proto - references address.proto
syntax = "proto3";
import "address.proto";
message User {
  string name = 1;
  Address home_address = 2;
}
```

Register with references via REST API:

```bash
# Register Address first
curl -X POST http://localhost:8081/subjects/Address/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schemaType": "PROTOBUF",
    "schema": "syntax = \"proto3\"; message Address { string street = 1; string city = 2; string country = 3; }"
  }'

# Register User with reference to Address
curl -X POST http://localhost:8081/subjects/User/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schemaType": "PROTOBUF",
    "schema": "syntax = \"proto3\"; import \"address.proto\"; message User { string name = 1; Address home_address = 2; }",
    "references": [
      {
        "name": "address.proto",
        "subject": "Address",
        "version": 1
      }
    ]
  }'
```

### Avro References

```json
{
  "schema": "{\"type\":\"record\",\"name\":\"Order\",\"fields\":[{\"name\":\"customer\",\"type\":\"com.example.Customer\"}]}",
  "references": [
    {
      "name": "com.example.Customer",
      "subject": "Customer",
      "version": 1
    }
  ]
}
```

### JSON Schema References

Uses standard `$ref` syntax:

```json
{
  "schema": "{\"type\":\"object\",\"properties\":{\"address\":{\"$ref\":\"address.json\"}}}",
  "schemaType": "JSON",
  "references": [
    {
      "name": "address.json",
      "subject": "Address",
      "version": 1
    }
  ]
}
```

## Serializer/Deserializer Configuration

### Java Producer/Consumer

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");

// Schema Registry connection
props.put("schema.registry.url", "http://schema-registry:8081");

// Avro
props.put("key.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("key.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
props.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");

// Protobuf
props.put("value.serializer", "io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer");
props.put("value.deserializer", "io.confluent.kafka.serializers.protobuf.KafkaProtobufDeserializer");

// JSON Schema
props.put("value.serializer", "io.confluent.kafka.serializers.json.KafkaJsonSchemaSerializer");
props.put("value.deserializer", "io.confluent.kafka.serializers.json.KafkaJsonSchemaDeserializer");

// Key config options
props.put("auto.register.schemas", "true");       // auto-register on produce (default: true)
props.put("use.latest.version", "false");          // use latest registered version instead of exact match
props.put("latest.compatibility.strict", "true");  // fail if schema is not compatible with latest
props.put("normalize.schemas", "false");           // normalize before registration
props.put("value.subject.name.strategy",
    "io.confluent.kafka.serializers.subject.TopicNameStrategy");

// Specific record (code-gen) vs GenericRecord
props.put("specific.avro.reader", "true");  // deserialize to generated class, not GenericRecord
```

### Python (confluent-kafka)

```python
from confluent_kafka import SerializingProducer, DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer

sr_client = SchemaRegistryClient({"url": "http://schema-registry:8081"})

avro_schema = """{
    "type": "record",
    "name": "User",
    "namespace": "com.example",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "int", "default": 0}
    ]
}"""

# Serialize dict -> Avro bytes with schema ID prefix
avro_ser = AvroSerializer(sr_client, avro_schema)
avro_deser = AvroDeserializer(sr_client)

producer = SerializingProducer({
    "bootstrap.servers": "localhost:9092",
    "value.serializer": avro_ser,
})

consumer = DeserializingConsumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "value.deserializer": avro_deser,
    "auto.offset.reset": "earliest",
})

producer.produce("users", value={"name": "Alice", "age": 30})
producer.flush()
```

### Python Protobuf and JSON Schema

```python
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer

# Protobuf: pass generated pb2 class
from user_pb2 import User
pb_ser = ProtobufSerializer(User, sr_client, {"auto.register.schemas": True})
pb_deser = ProtobufDeserializer(User)

# JSON Schema
json_schema_str = '{"type":"object","properties":{"name":{"type":"string"}}}'
json_ser = JSONSerializer(json_schema_str, sr_client)
json_deser = JSONDeserializer(json_schema_str)
```

### Go (confluent-kafka-go)

```go
import (
    "github.com/confluentinc/confluent-kafka-go/v2/schemaregistry"
    "github.com/confluentinc/confluent-kafka-go/v2/schemaregistry/serde"
    "github.com/confluentinc/confluent-kafka-go/v2/schemaregistry/serde/avro"
    "github.com/confluentinc/confluent-kafka-go/v2/schemaregistry/serde/protobuf"
    "github.com/confluentinc/confluent-kafka-go/v2/schemaregistry/serde/jsonschema"
)

client, _ := schemaregistry.NewClient(schemaregistry.NewConfig("http://schema-registry:8081"))

// Avro
ser, _ := avro.NewGenericSerializer(client, serde.ValueSerde, avro.NewSerializerConfig())
deser, _ := avro.NewGenericDeserializer(client, serde.ValueSerde, avro.NewDeserializerConfig())

// Protobuf
pbSer, _ := protobuf.NewSerializer(client, serde.ValueSerde, protobuf.NewSerializerConfig())

// JSON Schema
jsonSer, _ := jsonschema.NewSerializer(client, serde.ValueSerde, jsonschema.NewSerializerConfig())
```

### Critical Serializer Flags

| Property | Default | Description |
|----------|---------|-------------|
| `auto.register.schemas` | `true` | Automatically register new schemas on produce. **Set to `false` in production** - use CI/CD pipeline to register schemas |
| `use.latest.version` | `false` | Use the latest registered schema version instead of the exact schema. Use with `auto.register.schemas=false` for consumer-driven schema evolution |
| `latest.compatibility.strict` | `true` | Fail if the schema is not compatible with the latest version |
| `normalize.schemas` | `false` | Normalize schemas before registration (canonicalize field order) |
| `schema.registry.url` | -- | Comma-separated list of Schema Registry URLs |
| `basic.auth.credentials.source` | `URL` | Auth source: `URL`, `USER_INFO`, `SASL_INHERIT` |
| `basic.auth.user.info` | -- | `user:password` for basic auth |

## REST API Reference

Default port: 8081. Content type: `application/vnd.schemaregistry.v1+json`.

### Subjects

```bash
# List all subjects
GET /subjects
curl http://localhost:8081/subjects
# ["users-value", "orders-value", "payments-key"]

# List versions under a subject
GET /subjects/{subject}/versions
curl http://localhost:8081/subjects/users-value/versions
# [1, 2, 3]

# Get schema by version
GET /subjects/{subject}/versions/{version}
curl http://localhost:8081/subjects/users-value/versions/latest
# {"subject":"users-value","version":3,"id":42,"schema":"...","schemaType":"AVRO"}

# Register a new schema version
POST /subjects/{subject}/versions
curl -X POST http://localhost:8081/subjects/users-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{\"type\":\"record\",\"name\":\"User\",\"fields\":[{\"name\":\"name\",\"type\":\"string\"},{\"name\":\"age\",\"type\":\"int\",\"default\":0}]}"}'
# {"id": 43}

# Check if schema exists under subject (without registering)
POST /subjects/{subject}
curl -X POST http://localhost:8081/subjects/users-value \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "..."}'
# Returns version and ID if exists, 404 if not

# Delete subject (soft delete)
DELETE /subjects/{subject}
# Delete subject (hard delete, requires prior soft delete)
DELETE /subjects/{subject}?permanent=true

# Delete specific version
DELETE /subjects/{subject}/versions/{version}
```

### Schemas by ID

```bash
# Get schema by global ID
GET /schemas/ids/{id}
curl http://localhost:8081/schemas/ids/42
# {"schema": "..."}

# Get schema string only
GET /schemas/ids/{id}/schema

# List all schema types
GET /schemas/types
# ["AVRO", "PROTOBUF", "JSON"]

# Get all versions referencing this schema
GET /schemas/ids/{id}/versions
```

### Compatibility

```bash
# Check compatibility of new schema against specific version
POST /compatibility/subjects/{subject}/versions/{version}
curl -X POST http://localhost:8081/compatibility/subjects/users-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "..."}'
# {"is_compatible": true}

# Check against all versions (for transitive checks)
POST /compatibility/subjects/{subject}/versions?verbose=true

# Get compatibility level for a subject
GET /config/{subject}
curl http://localhost:8081/config/users-value
# {"compatibilityLevel": "BACKWARD"}

# Set compatibility level for a subject
PUT /config/{subject}
curl -X PUT http://localhost:8081/config/users-value \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"compatibility": "FULL"}'

# Get global default compatibility level
GET /config
# {"compatibilityLevel": "BACKWARD"}

# Set global default
PUT /config
curl -X PUT http://localhost:8081/config \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"compatibility": "FULL_TRANSITIVE"}'

# Delete subject-level config (revert to global)
DELETE /config/{subject}
```

### Mode

```bash
# Get mode (READWRITE, READONLY, IMPORT)
GET /mode
GET /mode/{subject}

# Set mode
PUT /mode/{subject}
curl -X PUT http://localhost:8081/mode/users-value \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"mode": "READONLY"}'
```

## Integration with Kafka Connect

[[kafka-connect]] uses converters that delegate to Schema Registry for serialization.

```properties
# Worker-level converter config
key.converter=io.confluent.connect.avro.AvroConverter
key.converter.schema.registry.url=http://schema-registry:8081

value.converter=io.confluent.connect.avro.AvroConverter
value.converter.schema.registry.url=http://schema-registry:8081

# Per-connector override
"value.converter": "io.confluent.connect.protobuf.ProtobufConverter",
"value.converter.schema.registry.url": "http://schema-registry:8081",
"value.converter.auto.register.schemas": "false",
"value.converter.use.latest.version": "true"
```

Available converters:
- `AvroConverter` - binary Avro + schema ID wire format
- `ProtobufConverter` - binary Protobuf + schema ID
- `JsonSchemaConverter` - JSON payload + schema ID
- `JsonConverter` (built-in, NO schema registry) - JSON with optional inline schema

Gotcha: `JsonConverter` with `schemas.enable=true` embeds the full schema in every message (bloated). Use `JsonSchemaConverter` with Schema Registry instead.

## Integration with Kafka Streams

```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "my-streams-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put("schema.registry.url", "http://schema-registry:8081");

// Default serdes
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,
    Serdes.StringSerde.class);
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,
    SpecificAvroSerde.class);

// Per-stream serde override
StreamsBuilder builder = new StreamsBuilder();
Serde<User> userSerde = new SpecificAvroSerde<>();
userSerde.configure(
    Map.of("schema.registry.url", "http://schema-registry:8081"),
    false  // isKey = false
);

KStream<String, User> users = builder.stream(
    "users",
    Consumed.with(Serdes.String(), userSerde)
);
```

Available serdes: `SpecificAvroSerde`, `GenericAvroSerde`, `KafkaProtobufSerde`, `KafkaJsonSchemaSerde`.

## Deployment and HA

```yaml
# docker-compose snippet
schema-registry:
  image: confluentinc/cp-schema-registry:7.7.0
  ports:
    - "8081:8081"
  environment:
    SCHEMA_REGISTRY_HOST_NAME: schema-registry
    SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: broker:29092
    SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081
    SCHEMA_REGISTRY_SCHEMA_REGISTRY_GROUP_ID: schema-registry-cluster
    # HA: leader election
    SCHEMA_REGISTRY_LEADER_ELIGIBILITY: "true"
    # Security
    SCHEMA_REGISTRY_AUTHENTICATION_METHOD: BASIC
    SCHEMA_REGISTRY_AUTHENTICATION_ROLES: admin,developer,readonly
    SCHEMA_REGISTRY_AUTHENTICATION_REALM: SchemaRegistryProps
```

HA setup: run 2+ instances. One becomes primary (leader), others serve reads. On leader failure, another instance takes over via leader election.

## Gotchas

- **`auto.register.schemas=true` in production is a footgun.** Any producer can register arbitrary schemas. Use CI/CD to register schemas and set `auto.register.schemas=false` on all producers.

- **BACKWARD compatibility is the default but not always correct.** If producers deploy before consumers (common in microservices), you need FORWARD. If deployment order varies, use FULL. Think about who deploys first.

- **Adding a field without a default breaks BACKWARD in Avro.** New consumer cannot deserialize old messages missing the field. Always provide defaults.

- **`additionalProperties: false` in JSON Schema blocks FORWARD compatibility.** Old consumer rejects new fields it does not recognize. Either set to `true` or omit (defaults to `true`).

- **Subject naming strategy mismatch between producer and consumer causes schema not found errors.** Both sides must use the same strategy. Changing strategy mid-stream orphans existing subjects.

- **Schema Registry uses Kafka as its backing store.** If the Kafka cluster is down, Schema Registry cannot serve schemas (even cached schemas expire). Deploy Schema Registry close to the brokers.

- **Deleting a schema version is a soft delete by default.** The schema ID is still resolvable. Use `?permanent=true` for hard delete, but only after soft-deleting first.

- **Schema IDs are globally unique across all subjects.** Two subjects registering the exact same schema get the same ID. This is by design - it enables cross-subject schema sharing.

- **Protobuf field numbers are the contract, not field names.** Renaming a field is safe. Changing or reusing a field number is a breaking change. Use `reserved` for removed fields.

- **Schema Registry caches schemas in-memory.** First deserialization of a new schema ID triggers a REST call. Subsequent deserializations use the cache. Schema cache size is controlled by `schema.registry.cache.max.size` (default: 1000 for Java client).

- **`use.latest.version=true` without `auto.register.schemas=false` is contradictory.** If auto-register is on, the serializer registers its own schema - `use.latest.version` has no effect. The intended pattern is: register schemas in CI/CD, set `auto.register.schemas=false` + `use.latest.version=true` on the producer.

## Quick Reference

### REST API Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/subjects` | List all subjects |
| `GET` | `/subjects/{subject}/versions` | List versions |
| `GET` | `/subjects/{subject}/versions/{version}` | Get schema by version (`latest` supported) |
| `POST` | `/subjects/{subject}/versions` | Register new schema |
| `POST` | `/subjects/{subject}` | Check if schema exists (lookup) |
| `DELETE` | `/subjects/{subject}` | Soft-delete subject |
| `DELETE` | `/subjects/{subject}?permanent=true` | Hard-delete subject |
| `GET` | `/schemas/ids/{id}` | Get schema by global ID |
| `POST` | `/compatibility/subjects/{subject}/versions/{version}` | Test compatibility |
| `GET` | `/config` | Get global compatibility |
| `PUT` | `/config` | Set global compatibility |
| `GET` | `/config/{subject}` | Get subject compatibility |
| `PUT` | `/config/{subject}` | Set subject compatibility |
| `GET` | `/mode` | Get global mode |

### Client Library Packages

| Language | Package |
|----------|---------|
| Python | `confluent_kafka.schema_registry` (client), `.avro`, `.protobuf`, `.json_schema` (serdes) |
| Java | `io.confluent:kafka-avro-serializer`, `kafka-protobuf-serializer`, `kafka-json-schema-serializer` |
| Go | `github.com/confluentinc/confluent-kafka-go/v2/schemaregistry` |
| .NET | `Confluent.SchemaRegistry`, `Confluent.SchemaRegistry.Serdes.Avro` |

## See Also

- [[kafka-connect]] - uses Schema Registry converters for data format transformation
- [[producer-patterns]] - producer-side serialization configuration
- [[consumer-groups]] - consumer-side deserialization and schema compatibility concerns
