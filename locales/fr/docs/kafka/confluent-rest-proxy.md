---
title: "Proxy REST Confluent"
category: reference
tags: [kafka, rest-proxy, http, confluent, api, producer, consumer]
level: 3
source_sha256: dd5c0cc69fbc9868076a0a2e2b76664d9e8b309437d9bfb92459a225b202fc4f
translation: machine
translated_at: '2026-10-24'
---
# Proxy REST Confluent {#confluent-rest-proxy}

Le proxy REST Confluent fournit une interface HTTP vers Kafka (port par défaut 8082), permettant les opérations de production, de consommation et de métadonnées dans des environnements sans client Kafka natif.

## Points clés {#key-facts}

- Permet d'interagir avec Kafka via HTTP/REST standard, utile pour les langages sans bibliothèque cliente Kafka ou dans les environnements soumis à des restrictions de pare-feu
- Prend en charge les formats de messages JSON, Avro, Protobuf, JSON Schema et binaire (base64)
- L'API consommateur est **avec état** : il faut créer une instance, s'abonner, puis interroger (poll)
- Les instances consommateur ont un délai d'expiration (`consumer.instance.timeout.ms`, 5 min par défaut) : elles sont supprimées automatiquement si aucune interrogation n'a lieu
- Fait partie de Confluent Platform (et non du cœur d'Apache Kafka)
- S'intègre à [[schema-registry]] pour la sérialisation Avro/Protobuf

## Schémas d'utilisation {#patterns}

### Produire des messages {#produce-messages}

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

### Consommer des messages {#consume-messages}

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

### Métadonnées {#metadata}

```bash
curl http://localhost:8082/topics            # List topics
curl http://localhost:8082/topics/test       # Topic details
curl http://localhost:8082/topics/test/partitions  # Partitions
curl http://localhost:8082/brokers           # Broker list
curl http://localhost:8082/v3/clusters       # Cluster metadata
```

### Types de contenu {#content-types}

| Format | Content-Type |
|--------|-------------|
| JSON | `application/vnd.kafka.json.v2+json` |
| Avro | `application/vnd.kafka.avro.v2+json` |
| Protobuf | `application/vnd.kafka.protobuf.v2+json` |
| Binaire | `application/vnd.kafka.binary.v2+json` |

## Pièges courants {#gotchas}

- **Les instances consommateur expirent automatiquement** : si aucune interrogation n'a lieu dans le délai imparti (5 min par défaut), l'instance est supprimée et doit être recréée
- **Le proxy REST ajoute de la latence** : surcoût HTTP par rapport au protocole binaire natif ; peu adapté aux cas d'usage à latence ultra-faible
- **Ce n'est pas un remplacement des clients natifs** : à utiliser pour les tâches d'administration, les environnements non JVM, ou lorsque HTTP est le seul protocole autorisé

## Voir aussi {#see-also}

- [[admin-api]] - gestion programmatique du cluster (Java natif)
- [[schema-registry]] - gestion des schémas Avro/Protobuf via le proxy REST
- [Documentation du proxy REST Confluent](https://docs.confluent.io/platform/current/kafka-rest/)
