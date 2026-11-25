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

Confluent Schema Registry est un service distinct (qui ne fait pas partie du cœur d'Apache Kafka) qui stocke, gère et valide les schémas de messages (Avro, Protobuf, JSON Schema) avec gestion des versions et application de la compatibilité, en utilisant un en-tête de 5 octets dans chaque message pour référencer l'ID du schéma.

## Faits clés {#key-facts}

- Fonctionne comme service autonome, port par défaut 8081
- Stocke les schémas dans un topic Kafka spécifique (`_schemas`)
- Le schéma n'est PAS envoyé avec chaque message : seulement un ID de 4 octets (en-tête de 5 octets : 1 octet magique + ID de schéma de 4 octets)
- Le producteur et le consommateur mettent en cache les schémas localement
- **Subject** = périmètre sous lequel les schémas sont enregistrés ; stratégie par défaut : `{topic-name}-key` et `{topic-name}-value`
- Le producteur enregistre le schéma lors du premier envoi ; Schema Registry attribue un ID entier unique au schéma
- Le consommateur lit l'ID du schéma dans l'en-tête du message, récupère le schéma auprès du Registry et désérialise le message
- Stratégies de nommage des subjects : `TopicNameStrategy` (par défaut), `RecordNameStrategy`, `TopicRecordNameStrategy`

## Modèles {#patterns}

### Formats de schéma {#schema-formats}

**Avro** (le plus courant dans l'écosystème Kafka) :
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

Trois méthodes de création d'objets Avro :
1. **Generic** : analyser le schéma JSON et construire un `GenericRecord` à l'exécution
2. **Specific** : générer des classes Java à partir du schéma via un plugin Maven/Gradle
3. **Reflection** : générer le schéma à partir d'une classe Java existante

**Protobuf** :
```protobuf
message Student {
  int32 id = 1;
  string name = 2;
  optional int32 age = 3;
}
```

### Modes de compatibilité {#compatibility-modes}

| Mode | Description | Ajout de champs | Suppression de champs |
|------|-------------|-----------------|-----------------------|
| **BACKWARD** (par défaut) | Le nouveau schéma lit les anciennes données | Uniquement avec valeurs par défaut | OK |
| **FORWARD** | L'ancien schéma lit les nouvelles données | OK | Uniquement avec valeurs par défaut |
| **FULL** | Les deux sens | Uniquement avec valeurs par défaut | Uniquement avec valeurs par défaut |
| **NONE** | Aucune vérification de compatibilité | Tous | Tous |

- BACKWARD = mettre à jour d'abord le consommateur, puis le producteur
- FORWARD = mettre à jour d'abord le producteur, puis le consommateur
- FULL = le plus sûr, dans les deux sens

### API REST {#rest-api}

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

### Producteur Java avec Avro + Schema Registry {#java-producer-with-avro-schema-registry}

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

### Producteur Python avec Avro + Schema Registry {#python-producer-with-avro-schema-registry}

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

### Classes de sérialiseur/désérialiseur Confluent {#confluent-serializerdeserializer-classes}

```text
io.confluent.kafka.serializers.KafkaAvroSerializer
io.confluent.kafka.serializers.KafkaAvroDeserializer
io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer
io.confluent.kafka.serializers.json.KafkaJsonSchemaSerializer
```

## Pièges à éviter {#gotchas}

- **Les modifications de schéma peuvent casser les consommateurs** : supprimer un champ sans valeur par défaut fait planter les consommateurs utilisant l'ancien schéma ; utilisez toujours la compatibilité FULL en production
- **JSON est lisible par un humain mais peu efficace** : le texte occupe plus de place que les formats binaires (Avro/Protobuf) ; les noms de champs sont répétés dans chaque message ; aucune vérification de type
- **Les protocoles binaires exigent que le schéma soit connu des deux côtés** : ajout d'un champ : le consommateur ignore le champ inconnu (généralement OK) ; suppression d'un champ : le consommateur l'attend et plante
- **Des chaînes User-Agent ont fait planter le parseur JSON** en production : solution : Dead Letter Queue pour les messages non analysables + analyse manuelle + correction + retraitement
- **`specific.avro.reader=true`** doit être défini sur le consommateur pour utiliser les classes générées au lieu de `GenericRecord`
- **Schema Registry est un produit Confluent** : il ne fait pas partie d'Apache Kafka ; des alternatives open source existent (Apicurio, Karapace)

## Voir aussi {#see-also}

- [[kafka-producer-fundamentals]] - sérialisation dans le pipeline du producteur
- [[kafka-connect]] - convertisseurs pour le format de données de Connect
- [[ksqldb]] - intégration automatique de Schema Registry pour AVRO/PROTOBUF
- [Documentation de Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/)
