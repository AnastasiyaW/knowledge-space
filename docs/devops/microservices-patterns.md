---
title: Microservices Architecture Patterns
category: patterns
tags: [devops, microservices, spring-cloud, api-gateway, service-discovery, resilience]
---

# Microservices Architecture Patterns

Microservices decompose applications into independently deployable services, each owning its database and communicating via APIs or messaging. Covers key patterns from service discovery through event-driven communication.

## Evolution

Monolith -> SOA (shared ESB) -> Microservices (fully independent, own database, lightweight communication)

## Key Challenges

1. **Configuration management** across N services
2. **Service discovery** (dynamic locations)
3. **Load balancing**
4. **Circuit breaking** (cascading failures)
5. **API Gateway** (single entry, cross-cutting concerns)
6. **Observability** (distributed tracing, logging)
7. **Security** (OAuth2, token propagation)

## Spring Cloud Config Server

Centralized configuration from Git repo:

```yaml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/org/config-repo
          default-label: main
```

Client: `spring.config.import=optional:configserver:http://configserver:8071`

Refresh without restart: `POST /actuator/busrefresh` via Spring Cloud Bus + RabbitMQ.

## Service Discovery (Eureka)

```java
@EnableEurekaServer  // server
@EnableEurekaClient  // implicit with dependency
```

Services register on startup, heartbeat every 30s. Client-side load balancing via Spring Cloud LoadBalancer.

**On Kubernetes**: K8s DNS replaces Eureka. `<service-name>.<namespace>.svc.cluster.local`

## API Gateway (Spring Cloud Gateway)

```yaml
spring:
  cloud:
    gateway:
      routes:
      - id: accounts-route
        uri: lb://ACCOUNTS       # load-balanced via Eureka
        predicates:
        - Path=/api/accounts/**
        filters:
        - RewritePath=/api/accounts/(?<segment>.*), /${segment}
```

Cross-cutting: authentication, rate limiting (Redis-backed), CORS, logging.

## Resilience Patterns (Resilience4j)

### Circuit Breaker

CLOSED (normal) -> OPEN (fail fast) -> HALF-OPEN (probe):

```java
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() { ... }
```

### Retry, Rate Limiter, Bulkhead

```java
@Retry(name = "service", fallbackMethod = "fallback")
@RateLimiter(name = "service")
@Bulkhead(name = "service")   // limits concurrent calls
```

## Event-Driven Architecture

### Spring Cloud Stream

```yaml
spring:
  cloud:
    stream:
      bindings:
        sendNotification-in-0:
          destination: send-notification
          group: notification-group
    function:
      definition: sendNotification
```

Publish: `streamBridge.send("destination", event)`

### RabbitMQ vs Kafka

| Feature | RabbitMQ | Kafka |
|---------|----------|-------|
| Model | Message queue, push | Distributed log, pull |
| Retention | Deleted after consumption | Retained (configurable) |
| Best for | Task distribution | Event sourcing, replay, high throughput |

## Security (OAuth2 + KeyCloak)

- **Client Credentials** - service-to-service, no user
- **Authorization Code + PKCE** - user-facing apps
- Gateway as OAuth2 client handles login, propagates JWT
- Services validate JWT stateless via JWK Set endpoint

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated()
).oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
```

## Kubernetes-Native Replacements

| Spring Cloud | Kubernetes Native |
|-------------|-------------------|
| Eureka (discovery) | K8s DNS |
| Config Server | ConfigMaps + Secrets |
| Ribbon (load balancing) | kube-proxy / Service |
| Spring Cloud Gateway | Ingress / Istio Gateway |

## Gotchas

- Database per service is mandatory for true independence - shared databases create coupling
- `depends_on: { condition: service_healthy }` in Compose ensures proper startup ordering
- Inter-service communication via service names, not localhost
- Circuit breakers should be configured per-dependency, not globally
- GraalVM native images: instant startup but longer build, reflection config needed

## See Also

- [[kubernetes-workloads]] - deploying microservices on K8s
- [[service-mesh-istio]] - infrastructure-level resilience
- [[monitoring-and-observability]] - distributed tracing across services
- [[docker-compose]] - local microservice development
- [[deployment-strategies]] - canary/blue-green for microservices
