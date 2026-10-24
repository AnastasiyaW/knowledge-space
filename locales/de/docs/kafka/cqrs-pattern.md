---
title: "CQRS-Muster"
category: patterns
tags: [kafka, cqrs, command, query, event-sourcing, aggregate, read-model, spring-kafka]
level: 3
source_sha256: 597618022276937c9ae7f15a77bc6cc6e3501dc02d4b3362ab6f3ea4bc089f74
translation: machine
translated_at: '2026-10-24'
---
# CQRS-Muster {#cqrs-pattern}

CQRS (Command Query Responsibility Segregation) trennt den Schreibpfad (Command API mit Event Store) vom Lesepfad (Query API mit optimierten Projektionen) und verbindet beide über Kafka-Topics zur asynchronen Ereignisweitergabe.

## Wichtige Fakten {#key-facts}

- **Command API** (Schreibseite): validiert Commands gegen den Aggregatzustand, erzeugt Events und veröffentlicht sie in Kafka
- **Query API** (Leseseite): konsumiert Events aus Kafka und baut leseoptimierte Projektionen auf
- Schreib- und Leseseite können unterschiedliche Datenbanken verwenden, die auf ihre Zugriffsmuster optimiert sind
- **Aggregate**: minimaler Zustand auf der Schreibseite, der für die Validierung von Commands benötigt wird und durch Wiedergabe von Events aufgebaut wird
- **Event Store** (MongoDB, PostgreSQL, EventStoreDB): speichert ALLE Events als unveränderliche Fakten und ist die Quelle der Wahrheit (Source of Truth)
- **Read Model** (MySQL, ElasticSearch, Redis): für bestimmte Abfragemuster optimiert
- Dasselbe Kafka-Topic kann mehrere unabhängige Query APIs speisen, die jeweils ihr eigenes Read Model aufbauen
- Idempotente Event-Verarbeitung: Die zuletzt verarbeitete Event-ID wird gespeichert, damit Duplikate beim Neustart des Consumers übersprungen werden

## Muster {#patterns}

### Architekturablauf {#architecture-flow}

```sql
1. User sends command (create account, deposit, withdraw)
2. Command API validates command against aggregate state
3. Command API creates event, applies to aggregate, saves to Event Store
4. Command API publishes event to Kafka topic
5. Query API consumes events, builds read-optimized projections
6. Users read data from Query API (different DB)
```

### Spring-Kafka-Implementierung {#spring-kafka-implementation}

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

### Mehrere Read Models {#multiple-read-models}

```php
Kafka Topic "order-events"
  -> Consumer Group A -> MySQL (operational queries)
  -> Consumer Group B -> ElasticSearch (full-text search)
  -> Consumer Group C -> Redis (real-time dashboard)
  -> Consumer Group D -> ML Service (fraud detection)
```

## Fallstricke {#gotchas}

- **Eventual Consistency ist by design** - das Read Model hinkt dem Write Model hinterher; Benutzern sollten Zustände wie „wird verarbeitet" angezeigt werden, anstatt auf den Abschluss zu warten
- **Replay blockiert eingehende Commands** - während der Event-Wiedergabe müssen neue Commands blockiert werden, um die Konsistenz zu wahren
- **Kafka direkt als Event Store nutzen** - möglich mit unbegrenzter Aufbewahrung und Log Compaction, Kafka löscht Daten standardmäßig jedoch irgendwann; für dauerhafte Speicherung sind dedizierte Event Stores besser geeignet
- **Nebenläufige Verarbeitung und Reihenfolge** - bei unabhängigen Entitäten nach Entitätsschlüssel partitionieren; bei abhängigen Entitäten, die eine globale Reihenfolge erfordern, kann sequentielle Verarbeitung notwendig sein

## Siehe auch {#see-also}

- [[event-sourcing]] - unveränderlicher Event-Log, Zustandsrekonstruktion, Replay
- [[saga-pattern]] - verteilte Transaktionen über CQRS-Microservices hinweg
- [[transactional-outbox]] - atomare Ereignisveröffentlichung zusammen mit Datenbankschreibvorgängen
- [[kafka-streams]] - Aufbau materialisierter Sichten aus Event-Streams
