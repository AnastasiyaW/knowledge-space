---
title: "Microservices-Architekturmuster"
category: patterns
tags: [devops, microservices, spring-cloud, api-gateway, service-discovery, resilience]
level: 3
source_sha256: eae706a46c073665e72427f15956314aa1a32ac7aa9d2897a1e47ef4de796eba
translation: machine
translated_at: '2026-10-24'
---
# Microservices-Architekturmuster {#microservices-architecture-patterns}

Microservices zerlegen Anwendungen in unabhängig deploybare Services, von denen jeder seine eigene Datenbank besitzt und über APIs oder Messaging kommuniziert. Behandelt werden zentrale Muster von Service Discovery bis zur ereignisgesteuerten Kommunikation.

## Evolution {#evolution}

Monolith -> SOA (gemeinsamer ESB) -> Microservices (vollständig unabhängig, eigene Datenbank, leichtgewichtige Kommunikation)

## Zentrale Herausforderungen {#key-challenges}

1. **Konfigurationsmanagement** über N Services
2. **Service Discovery** (dynamische Standorte)
3. **Lastverteilung**
4. **Circuit Breaking** (kaskadierende Fehler)
5. **API Gateway** (einzelner Einstiegspunkt, querschnittliche Belange)
6. **Observability** (verteiltes Tracing, Logging)
7. **Sicherheit** (OAuth2, Token-Propagation)

## Spring Cloud Config Server {#spring-cloud-config-server}

Zentrale Konfiguration aus einem Git-Repository:

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

Aktualisierung ohne Neustart: `POST /actuator/busrefresh` über Spring Cloud Bus + RabbitMQ.

## Service Discovery (Eureka) {#service-discovery-eureka}

```java
@EnableEurekaServer  // server
@EnableEurekaClient  // implicit with dependency
```

Services registrieren sich beim Start und senden alle 30 s einen Heartbeat. Clientseitige Lastverteilung erfolgt über Spring Cloud LoadBalancer.

**Auf Kubernetes**: K8s-DNS ersetzt Eureka. `<service-name>.<namespace>.svc.cluster.local`

## API Gateway (Spring Cloud Gateway) {#api-gateway-spring-cloud-gateway}

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

Querschnittlich: Authentifizierung, Rate Limiting (Redis-basiert), CORS, Logging.

## Resilienz-Muster (Resilience4j) {#resilience-patterns-resilience4j}

### Circuit Breaker {#circuit-breaker}

CLOSED (normal) -> OPEN (Fail Fast) -> HALF-OPEN (Probe):

```java
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() { ... }
```

### Retry, Rate Limiter, Bulkhead {#retry-rate-limiter-bulkhead}

```java
@Retry(name = "service", fallbackMethod = "fallback")
@RateLimiter(name = "service")
@Bulkhead(name = "service")   // limits concurrent calls
```

## Ereignisgesteuerte Architektur {#event-driven-architecture}

### Spring Cloud Stream {#spring-cloud-stream}

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

Veröffentlichen: `streamBridge.send("destination", event)`

### RabbitMQ vs. Kafka {#rabbitmq-vs-kafka}

| Merkmal | RabbitMQ | Kafka |
|---------|----------|-------|
| Modell | Message Queue, Push | Verteiltes Log, Pull |
| Aufbewahrung | Nach Konsum gelöscht | Aufbewahrt (konfigurierbar) |
| Geeignet für | Aufgabenverteilung | Event Sourcing, Replay, hoher Durchsatz |

## Sicherheit (OAuth2 + KeyCloak) {#security-oauth2-keycloak}

- **Client Credentials** - Service-zu-Service, ohne Benutzer
- **Authorization Code + PKCE** - benutzerseitige Anwendungen
- Gateway als OAuth2-Client übernimmt den Login und propagiert das JWT
- Services validieren JWTs zustandslos über den JWK-Set-Endpoint

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated()
).oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
```

## Kubernetes-native Alternativen {#kubernetes-native-replacements}

| Spring Cloud | Kubernetes Native |
|-------------|-------------------|
| Eureka (Discovery) | K8s-DNS |
| Config Server | ConfigMaps + Secrets |
| Ribbon (Lastverteilung) | kube-proxy / Service |
| Spring Cloud Gateway | Ingress / Istio Gateway |

## Stolperfallen {#gotchas}

- Eine Datenbank pro Service ist für echte Unabhängigkeit zwingend - gemeinsam genutzte Datenbanken erzeugen Kopplung
- `depends_on: { condition: service_healthy }` in Compose sorgt für die richtige Startreihenfolge
- Kommunikation zwischen Services über Servicenamen, nicht über localhost
- Circuit Breaker sollten pro Abhängigkeit konfiguriert werden, nicht global
- GraalVM Native Images: sofortiger Start, aber längerer Build; Reflection-Konfiguration erforderlich

## Siehe auch {#see-also}

- [[kubernetes-workloads]] - Deployment von Microservices auf K8s
- [[service-mesh-istio]] - Resilienz auf Infrastrukturebene
- [[monitoring-and-observability]] - verteiltes Tracing über Services hinweg
- [[docker-compose]] - lokale Microservice-Entwicklung
- [[deployment-strategies]] - Canary/Blue-Green für Microservices
