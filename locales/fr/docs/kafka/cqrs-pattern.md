---
title: "Patron CQRS"
category: patterns
tags: [kafka, cqrs, command, query, event-sourcing, aggregate, read-model, spring-kafka]
level: 3
source_sha256: 597618022276937c9ae7f15a77bc6cc6e3501dc02d4b3362ab6f3ea4bc089f74
translation: machine
translated_at: '2026-10-24'
---
# Patron CQRS {#cqrs-pattern}

CQRS (Command Query Responsibility Segregation) sépare le chemin d'écriture (Command API avec event store) du chemin de lecture (Query API avec projections optimisées), reliés par des topics Kafka pour la propagation asynchrone des événements.

## Points clés {#key-facts}

- **Command API** (côté écriture) : valide les commandes par rapport à l'état de l'agrégat, crée les événements et les publie sur Kafka
- **Query API** (côté lecture) : consomme les événements depuis Kafka et construit des projections optimisées pour la lecture
- Les côtés écriture et lecture peuvent utiliser des bases de données différentes, optimisées pour leurs schémas d'accès
- **Agrégat** : état minimal côté écriture, nécessaire à la validation des commandes, reconstruit en rejouant les événements
- **Event Store** (MongoDB, PostgreSQL, EventStoreDB) : stocke TOUS les événements comme faits immuables, source de vérité
- **Modèle de lecture** (MySQL, ElasticSearch, Redis) : optimisé pour des schémas de requêtes spécifiques
- Un même topic Kafka peut alimenter plusieurs Query API indépendantes, chacune construisant son propre modèle de lecture
- Traitement d'événements idempotent : mémoriser l'identifiant du dernier événement traité pour ignorer les doublons au redémarrage du consommateur

## Patrons {#patterns}

### Flux d'architecture {#architecture-flow}

```sql
1. User sends command (create account, deposit, withdraw)
2. Command API validates command against aggregate state
3. Command API creates event, applies to aggregate, saves to Event Store
4. Command API publishes event to Kafka topic
5. Query API consumes events, builds read-optimized projections
6. Users read data from Query API (different DB)
```

### Implémentation avec Spring Kafka {#spring-kafka-implementation}

```yaml
# application.yml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
    consumer:
      group-id: query-service
      auto-offset-reset: earliest
```

```java
// Command API - Producer
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void handleCommand(CreateAccountCommand cmd) {
    Account account = Account.create(cmd);
    eventStore.save(new AccountCreatedEvent(account));
    kafkaTemplate.send("account-events", account.getId(), serialize(event));
}

// Query API - Consumer
@KafkaListener(topics = "account-events", groupId = "${spring.kafka.consumer.group-id}")
public void handleEvent(String event, Acknowledgment ack) {
    AccountEvent parsed = deserialize(event);
    if (alreadyProcessed(parsed.getId())) { return; }  // Idempotency
    readModelRepository.apply(parsed);
    ack.acknowledge();
}
```

### Plusieurs modèles de lecture {#multiple-read-models}

```php
Kafka Topic "order-events"
  -> Consumer Group A -> MySQL (operational queries)
  -> Consumer Group B -> ElasticSearch (full-text search)
  -> Consumer Group C -> Redis (real-time dashboard)
  -> Consumer Group D -> ML Service (fraud detection)
```

## Pièges {#gotchas}

- **Cohérence éventuelle par conception** - le modèle de lecture accuse un retard sur le modèle d'écriture ; afficher des états « en cours de traitement » aux utilisateurs plutôt que de les faire attendre la fin du traitement
- **Le rejeu bloque les commandes entrantes** - pendant le rejeu des événements, les nouvelles commandes doivent être bloquées pour préserver la cohérence
- **Utiliser Kafka directement comme Event Store** - possible avec une rétention infinie et la compaction de logs, mais Kafka supprime les données par défaut ; un event store dédié convient mieux à un stockage illimité dans le temps
- **Traitement concurrent et ordre** - pour des entités indépendantes, partitionner par clé d'entité ; pour des entités dépendantes qui exigent un ordre global, un traitement séquentiel peut être nécessaire

## Voir aussi {#see-also}

- [[event-sourcing]] - journal d'événements immuable, reconstruction d'état, rejeu
- [[saga-pattern]] - transactions distribuées entre microservices CQRS
- [[transactional-outbox]] - publication atomique d'événements avec les écritures en base
- [[kafka-streams]] - construction de vues matérialisées à partir de flux d'événements
