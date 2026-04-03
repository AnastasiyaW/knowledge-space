---
title: CQRS Pattern
category: patterns
tags: [kafka, cqrs, command, query, event-sourcing, aggregate, read-model, spring-kafka]
---

# CQRS Pattern

CQRS (Command Query Responsibility Segregation) separates the write path (Command API with event store) from the read path (Query API with optimized projections), connected via Kafka topics for asynchronous event propagation.

## Key Facts

- **Command API** (write side): validates commands against aggregate state, creates events, publishes to Kafka
- **Query API** (read side): consumes events from Kafka, builds read-optimized projections
- Write and read sides can use different databases optimized for their access patterns
- **Aggregate**: minimal state on write side needed for command validation, built by replaying events
- **Event Store** (MongoDB, PostgreSQL, EventStoreDB): stores ALL events as immutable facts, source of truth
- **Read Model** (MySQL, ElasticSearch, Redis): optimized for specific query patterns
- Same Kafka topic can feed multiple independent Query APIs, each building its own read model
- Idempotent event processing: track last processed event ID to skip duplicates on consumer restart

## Patterns

### Architecture Flow

```
1. User sends command (create account, deposit, withdraw)
2. Command API validates command against aggregate state
3. Command API creates event, applies to aggregate, saves to Event Store
4. Command API publishes event to Kafka topic
5. Query API consumes events, builds read-optimized projections
6. Users read data from Query API (different DB)
```

### Spring Kafka Implementation

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

### Multiple Read Models

```
Kafka Topic "order-events"
  -> Consumer Group A -> MySQL (operational queries)
  -> Consumer Group B -> ElasticSearch (full-text search)
  -> Consumer Group C -> Redis (real-time dashboard)
  -> Consumer Group D -> ML Service (fraud detection)
```

## Gotchas

- **Eventual consistency by design** - read model lags behind write model; display "processing" states to users instead of waiting for completion
- **Replay blocks incoming commands** - during event replay, new commands must be blocked to maintain consistency
- **Using Kafka as Event Store directly** - possible with infinite retention + log compaction, but Kafka eventually deletes data by default; dedicated event stores are more appropriate for indefinite storage
- **Concurrent processing and ordering** - for independent entities, partition by entity key; for dependent entities requiring global ordering, sequential processing may be necessary

## See Also

- [[event-sourcing]] - immutable event log, state reconstruction, replay
- [[saga-pattern]] - distributed transactions across CQRS microservices
- [[transactional-outbox]] - atomic event publishing with database writes
- [[kafka-streams]] - building materialized views from event streams
