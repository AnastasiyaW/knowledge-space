---
title: Spring Kafka
category: reference
tags: [kafka, spring, spring-boot, kafka-template, kafka-listener, spring-cloud-stream]
---

# Spring Kafka

Spring Kafka provides declarative, annotation-based Kafka integration with `KafkaTemplate` for producing and `@KafkaListener` for consuming, plus Spring Cloud Stream for middleware-agnostic event-driven microservices.

## Key Facts

- `KafkaTemplate` wraps KafkaProducer with Spring conventions
- `@KafkaListener` auto-manages consumer lifecycle, deserialization, offset commits
- `@Component` annotation enables automatic bean discovery and dependency injection
- Spring Boot auto-configures Kafka with `application.properties` or `application.yml`
- Manual acknowledge via `Acknowledgment.acknowledge()` for at-least-once processing
- Spring Cloud Stream: middleware-agnostic abstraction with binders for Kafka, RabbitMQ, Kinesis, etc.
- Spring Cloud Data Flow: orchestration platform for composing streaming/batch pipelines

## Patterns

### Producer

```java
@Component
public class OrderProducer {
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public void send(String orderId, String orderJson) {
        kafkaTemplate.send("orders", orderId, orderJson);
    }
}
```

### Consumer

```java
@Component
public class OrderConsumer {
    @KafkaListener(topics = "orders", groupId = "order-service")
    public void consume(String message, Acknowledgment ack) {
        processOrder(message);
        ack.acknowledge();  // Manual commit
    }
}
```

### Configuration

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
    consumer:
      group-id: my-group
      auto-offset-reset: earliest
      enable-auto-commit: false
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
```

### Spring Cloud Stream (Functional)

```java
@Bean
public Function<String, String> uppercase() {
    return value -> value.toUpperCase();
}
// Auto-binds to input/output channels; no explicit Kafka API calls
```

## Gotchas

- **Default settings are adequate for many use cases** - don't over-configure
- **Spring approach is more declarative than Alpakka** - no manual stream management, Spring handles lifecycle
- **Less control over topology** - for complex stream processing, use [[kafka-streams]] instead

## See Also

- [[cqrs-pattern]] - Spring Kafka for CQRS implementation
- [[kafka-streams]] - more powerful stream processing
- [[alpakka-kafka]] - Akka Streams alternative
- [Spring for Apache Kafka Documentation](https://docs.spring.io/spring-kafka/reference/)
