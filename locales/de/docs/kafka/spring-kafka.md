---
title: "Spring Kafka"
category: reference
tags: [kafka, spring, spring-boot, kafka-template, kafka-listener, spring-cloud-stream]
level: 3
source_sha256: 5310aae42f914bef41e917fba4c2fa387979c7868e931b5db5221fc45abf3c81
translation: machine
translated_at: '2026-10-24'
---
# Spring Kafka {#spring-kafka}

Spring Kafka bietet deklarative, annotationsbasierte Kafka-Integration mit `KafkaTemplate` zum Produzieren und `@KafkaListener` zum Konsumieren sowie Spring Cloud Stream für middleware-agnostische, ereignisgesteuerte Microservices.

## Key Facts {#key-facts}

- `KafkaTemplate` kapselt den KafkaProducer mit Spring-Konventionen
- `@KafkaListener` verwaltet den Lebenszyklus des Consumers, die Deserialisierung und Offset-Commits automatisch
- Die `@Component`-Annotation ermöglicht automatische Bean-Erkennung und Dependency Injection
- Spring Boot konfiguriert Kafka automatisch über `application.properties` oder `application.yml`
- Manuelle Bestätigung über `Acknowledgment.acknowledge()` für Verarbeitung mit mindestens einmaliger Zustellung (At-least-once)
- Spring Cloud Stream: middleware-agnostische Abstraktion mit Bindern für Kafka, RabbitMQ, Kinesis usw.
- Spring Cloud Data Flow: Orchestrierungsplattform zum Zusammenstellen von Streaming- und Batch-Pipelines

## Patterns {#patterns}

### Producer {#producer}

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

### Consumer {#consumer}

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

### Configuration {#configuration}

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

### Spring Cloud Stream (Functional) {#spring-cloud-stream-functional}

```java
@Bean
public Function<String, String> uppercase() {
    return value -> value.toUpperCase();
}
// Auto-binds to input/output channels; no explicit Kafka API calls
```

## Gotchas {#gotchas}

- **Die Standardeinstellungen reichen für viele Anwendungsfälle aus** - nicht unnötig überkonfigurieren
- **Der Spring-Ansatz ist deklarativer als Alpakka** - kein manuelles Stream-Management, Spring übernimmt den Lebenszyklus
- **Weniger Kontrolle über die Topologie** - für komplexe Stream-Verarbeitung stattdessen [[kafka-streams]] verwenden

## See Also {#see-also}

- [[cqrs-pattern]] - Spring Kafka zur CQRS-Implementierung
- [[kafka-streams]] - leistungsfähigere Stream-Verarbeitung
- [[alpakka-kafka]] - Alternative mit Akka Streams
- [Spring for Apache Kafka Documentation](https://docs.spring.io/spring-kafka/reference/)
