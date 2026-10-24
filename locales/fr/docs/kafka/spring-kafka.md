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

Spring Kafka fournit une intégration Kafka déclarative, basée sur les annotations, avec `KafkaTemplate` pour la production de messages et `@KafkaListener` pour leur consommation, ainsi que Spring Cloud Stream pour des microservices orientés événements indépendants du middleware.

## Points clés {#key-facts}

- `KafkaTemplate` encapsule KafkaProducer avec les conventions de Spring
- `@KafkaListener` gère automatiquement le cycle de vie du consommateur, la désérialisation et la validation des offsets (commits d'offsets)
- L'annotation `@Component` active la découverte automatique des beans et l'injection de dépendances
- Spring Boot configure automatiquement Kafka à partir de `application.properties` ou `application.yml`
- Acquittement manuel via `Acknowledgment.acknowledge()` pour un traitement au moins une fois (at-least-once)
- Spring Cloud Stream : abstraction indépendante du middleware, avec des binders pour Kafka, RabbitMQ, Kinesis, etc.
- Spring Cloud Data Flow : plateforme d'orchestration permettant de composer des pipelines de streaming et de traitement par lots

## Modèles {#patterns}

### Producteur {#producer}

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

### Consommateur {#consumer}

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

### Spring Cloud Stream (fonctionnel) {#spring-cloud-stream-functional}

```java
@Bean
public Function<String, String> uppercase() {
    return value -> value.toUpperCase();
}
// Auto-binds to input/output channels; no explicit Kafka API calls
```

## Pièges à éviter {#gotchas}

- **Les paramètres par défaut suffisent pour de nombreux cas d'usage** - inutile de trop configurer
- **L'approche Spring est plus déclarative que celle d'Alpakka** - pas de gestion manuelle des flux, Spring gère le cycle de vie
- **Moins de contrôle sur la topologie** - pour un traitement de flux complexe, utilisez plutôt [[kafka-streams]]

## Voir aussi {#see-also}

- [[cqrs-pattern]] - Spring Kafka pour l'implémentation de CQRS
- [[kafka-streams]] - traitement de flux plus puissant
- [[alpakka-kafka]] - alternative basée sur Akka Streams
- [Documentation Spring for Apache Kafka](https://docs.spring.io/spring-kafka/reference/)
