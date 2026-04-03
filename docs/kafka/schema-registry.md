---
title: Schema Registry
category: concepts
tags: [kafka, schema-registry, avro, protobuf, json-schema, compatibility, serialization, confluent]
---

# Schema Registry

Confluent Schema Registry is a separate service (not part of Apache Kafka core) that stores, manages, and validates message schemas (Avro, Protobuf, JSON Schema) with versioning and compatibility enforcement, using a 5-byte header in each message to reference the schema ID.

## Key Facts

- Runs as standalone service, default port 8081
- Stores schemas in a special Kafka topic (`_schemas`)
- Schema is NOT sent with every message - only a 4-byte ID (5-byte header: 1 magic byte + 4-byte schema ID)
- Both producer and consumer cache schemas locally
- **Subject** = scope under which schemas are registered; default strategy: `{topic-name}-key` and `{topic-name}-value`
- Producer registers schema on first send; Schema Registry assigns unique integer schema ID
- Consumer reads schema ID from message header, fetches schema from Registry, deserializes
- Subject naming strategies: `TopicNameStrategy` (default), `RecordNameStrategy`, `TopicRecordNameStrategy`

## Patterns

### Schema Formats

**Avro** (most common in Kafka ecosystem):
```json
{
  "type": "record",
  "name": "Student",
  "namespace": "com.example",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "age", "type": ["null", "int"], "default": null}
  ]
}
```

Three methods of creating Avro objects:
1. **Generic** - parse JSON schema, build `GenericRecord` at runtime
2. **Specific** - generate Java classes from schema via Maven/Gradle plugin
3. **Reflection** - generate schema from existing Java class

**Protobuf**:
```protobuf
message Student {
  int32 id = 1;
  string name = 2;
  optional int32 age = 3;
}
```

### Compatibility Modes

| Mode | Description | Adding Fields | Removing Fields |
|------|-------------|---------------|-----------------|
| **BACKWARD** (default) | New schema reads old data | Only with defaults | OK |
| **FORWARD** | Old schema reads new data | OK | Only with defaults |
| **FULL** | Both directions | Only with defaults | Only with defaults |
| **NONE** | No compatibility checking | Any | Any |

- BACKWARD = consumer upgrade first, then producer
- FORWARD = producer upgrade first, then consumer
- FULL = safest, both directions

### REST API

```bash
# List subjects
curl http://localhost:8081/subjects

# Get schema versions
curl http://localhost:8081/subjects/orders-value/versions

# Get specific / latest version
curl http://localhost:8081/subjects/orders-value/versions/1
curl http://localhost:8081/subjects/orders-value/versions/latest

# Register new schema
curl -X POST http://localhost:8081/subjects/orders-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{\"type\":\"record\",\"name\":\"Order\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"}]}"}'

# Check compatibility
curl -X POST http://localhost:8081/compatibility/subjects/orders-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "..."}'

# Get / Set compatibility level
curl http://localhost:8081/config
curl -X PUT http://localhost:8081/config/orders-value \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"compatibility": "FULL"}'
```

### Java Producer with Avro + Schema Registry

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", "http://localhost:8081");

KafkaProducer<String, GenericRecord> producer = new KafkaProducer<>(props);
GenericRecord record = new GenericData.Record(schema);
record.put("id", 1);
producer.send(new ProducerRecord<>("topic", "key", record));
```

### Python Producer with Avro + Schema Registry

```python
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

sr = SchemaRegistryClient({"url": "http://localhost:8081"})
serializer = AvroSerializer(sr, schema_str)

producer = SerializingProducer({
    "bootstrap.servers": "localhost:9092",
    "key.serializer": lambda k, ctx: k.encode(),
    "value.serializer": serializer,
})
producer.produce("topic", key="key", value={"id": 1})
producer.flush()
```

### Confluent Serializer/Deserializer Classes

```
io.confluent.kafka.serializers.KafkaAvroSerializer
io.confluent.kafka.serializers.KafkaAvroDeserializer
io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer
io.confluent.kafka.serializers.json.KafkaJsonSchemaSerializer
```

## Gotchas

- **Schema changes can break consumers** - removing a field without default crashes consumers with old schema; always use FULL compatibility in production
- **JSON is human-readable but inefficient** - text takes more space than binary formats (Avro/Protobuf); field names repeated in every message; no type enforcement
- **Binary protocols require schema known by both sides** - adding a field: consumer ignores unknown (usually OK); removing a field: consumer expects it and crashes
- **User-Agent strings crashed JSON parser** in production - solution: Dead Letter Queue for unparseable messages + manual analysis + fix + re-process
- **`specific.avro.reader=true`** must be set on consumer to use generated classes instead of `GenericRecord`
- **Schema Registry is a Confluent product** - not part of Apache Kafka; open-source alternatives exist (Apicurio, Karapace)

## See Also

- [[producer-patterns]] - serialization in the producer pipeline
- [[kafka-connect]] - converters for Connect data format
- [[ksqldb]] - automatic Schema Registry integration for AVRO/PROTOBUF
- [Confluent Schema Registry Documentation](https://docs.confluent.io/platform/current/schema-registry/)
