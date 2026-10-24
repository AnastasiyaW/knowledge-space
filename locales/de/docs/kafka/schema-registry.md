---
title: "Schema Registry"
category: concepts
tags: [kafka, schema-registry, avro, protobuf, json-schema, compatibility, serialization, confluent]
level: 3
source_sha256: bcfd0e1e7770ecbde694ba9776862a92df9e8ff83a4655aa17d5b3968db461cc
translation: machine
translated_at: '2026-10-24'
---
# Schema Registry {#schema-registry}

Die Confluent Schema Registry ist ein eigenständiger Dienst (nicht Teil des Apache-Kafka-Kerns), der Nachrichtenschemas (Avro, Protobuf, JSON Schema) speichert, verwaltet und validiert. Dabei unterstützt er Versionierung und Kompatibilitätsprüfungen. Jede Nachricht enthält einen 5-Byte-Header, der auf die Schema-ID verweist.

## Key Facts {#key-facts}

- Läuft als eigenständiger Dienst, Standardport 8081
- Speichert Schemas in einem speziellen Kafka-Topic (`_schemas`)
- Das Schema wird NICHT mit jeder Nachricht gesendet – nur eine 4-Byte-ID (5-Byte-Header: 1 Magic Byte + 4-Byte-Schema-ID)
- Producer und Consumer cachen Schemas lokal
- **Subject** = Geltungsbereich, unter dem Schemas registriert werden; Standardstrategie: `{topic-name}-key` und `{topic-name}-value`
- Der Producer registriert das Schema beim ersten Senden; die Schema Registry vergibt eine eindeutige Integer-Schema-ID
- Der Consumer liest die Schema-ID aus dem Nachrichten-Header, ruft das Schema von der Registry ab und deserialisiert die Nachricht
- Namensstrategien für Subjects: `TopicNameStrategy` (Standard), `RecordNameStrategy`, `TopicRecordNameStrategy`

## Patterns {#patterns}

### Schema Formats {#schema-formats}

**Avro** (am häufigsten im Kafka-Ökosystem):
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

Drei Methoden, Avro-Objekte zu erzeugen:
1. **Generic** – JSON-Schema parsen, zur Laufzeit einen `GenericRecord` aufbauen
2. **Specific** – Java-Klassen aus dem Schema über ein Maven/Gradle-Plugin generieren
3. **Reflection** – Schema aus einer bestehenden Java-Klasse generieren

**Protobuf**:
```protobuf
message Student {
  int32 id = 1;
  string name = 2;
  optional int32 age = 3;
}
```

### Compatibility Modes {#compatibility-modes}

| Mode | Description | Adding Fields | Removing Fields |
|------|-------------|---------------|-----------------|
| **BACKWARD** (Standard) | Neues Schema liest alte Daten | Nur mit Defaults | OK |
| **FORWARD** | Altes Schema liest neue Daten | OK | Nur mit Defaults |
| **FULL** | Beide Richtungen | Nur mit Defaults | Nur mit Defaults |
| **NONE** | Keine Kompatibilitätsprüfung | Beliebig | Beliebig |

- BACKWARD = zuerst Consumer aktualisieren, dann Producer
- FORWARD = zuerst Producer aktualisieren, dann Consumer
- FULL = am sichersten, beide Richtungen

### REST API {#rest-api}

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

### Java Producer with Avro + Schema Registry {#java-producer-with-avro-schema-registry}

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

### Python Producer with Avro + Schema Registry {#python-producer-with-avro-schema-registry}

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

### Confluent Serializer/Deserializer Classes {#confluent-serializerdeserializer-classes}

```text
io.confluent.kafka.serializers.KafkaAvroSerializer
io.confluent.kafka.serializers.KafkaAvroDeserializer
io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer
io.confluent.kafka.serializers.json.KafkaJsonSchemaSerializer
```

## Gotchas {#gotchas}

- **Schemaänderungen können Consumer brechen** – das Entfernen eines Feldes ohne Default lässt Consumer mit dem alten Schema abstürzen; in Produktion immer FULL-Kompatibilität verwenden
- **JSON ist menschenlesbar, aber ineffizient** – Text benötigt mehr Platz als Binärformate (Avro/Protobuf); Feldnamen werden in jeder Nachricht wiederholt; keine Typprüfung
- **Binärprotokolle setzen voraus, dass das Schema beiden Seiten bekannt ist** – beim Hinzufügen eines Feldes ignoriert der Consumer das unbekannte Feld (meist unproblematisch); beim Entfernen eines Feldes erwartet der Consumer es und stürzt ab
- **User-Agent-Strings haben den JSON-Parser in Produktion zum Absturz gebracht** – Lösung: Dead Letter Queue für nicht parsbare Nachrichten + manuelle Analyse + Fix + erneute Verarbeitung
- **`specific.avro.reader=true`** muss im Consumer gesetzt sein, damit generierte Klassen statt `GenericRecord` verwendet werden
- **Die Schema Registry ist ein Confluent-Produkt** – nicht Teil von Apache Kafka; es gibt Open-Source-Alternativen (Apicurio, Karapace)

## See Also {#see-also}

- [[kafka-producer-fundamentals]] – Serialisierung in der Producer-Pipeline
- [[kafka-connect]] – Converter für das Datenformat von Connect
- [[ksqldb]] – automatische Schema-Registry-Integration für AVRO/PROTOBUF
- [Confluent Schema Registry Dokumentation](https://docs.confluent.io/platform/current/schema-registry/)
