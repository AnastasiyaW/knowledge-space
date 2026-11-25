---
title: "Modèles d'architecture microservices"
category: patterns
tags: [devops, microservices, spring-cloud, api-gateway, service-discovery, resilience]
level: 3
source_sha256: eae706a46c073665e72427f15956314aa1a32ac7aa9d2897a1e47ef4de796eba
translation: machine
translated_at: '2026-10-24'
---
# Modèles d'architecture microservices {#microservices-architecture-patterns}

Les microservices décomposent les applications en services déployables de façon indépendante, chacun possédant sa propre base de données et communiquant via des API ou une messagerie. Couvre les principaux modèles, de la découverte de services à la communication orientée événements.

## Évolution {#evolution}

Monolithe -> SOA (ESB partagé) -> Microservices (totalement indépendants, base de données propre, communication légère)

## Principaux défis {#key-challenges}

1. **Gestion de la configuration** sur N services
2. **Découverte de services** (emplacements dynamiques)
3. **Répartition de charge**
4. **Coupe-circuit** (défaillances en cascade)
5. **Passerelle API** (point d'entrée unique, préoccupations transversales)
6. **Observabilité** (traçage distribué, journalisation)
7. **Sécurité** (OAuth2, propagation des jetons)

## Spring Cloud Config Server {#spring-cloud-config-server}

Configuration centralisée depuis un dépôt Git :

```yaml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/org/config-repo
          default-label: main
```

Client : `spring.config.import=optional:configserver:http://configserver:8071`

Rechargement sans redémarrage : `POST /actuator/busrefresh` via Spring Cloud Bus + RabbitMQ.

## Découverte de services (Eureka) {#service-discovery-eureka}

```java
@EnableEurekaServer  // server
@EnableEurekaClient  // implicit with dependency
```

Les services s'enregistrent au démarrage et envoient un signal de vie (heartbeat) toutes les 30 s. Répartition de charge côté client via Spring Cloud LoadBalancer.

**Sur Kubernetes** : le DNS de K8s remplace Eureka. `<service-name>.<namespace>.svc.cluster.local`

## Passerelle API (Spring Cloud Gateway) {#api-gateway-spring-cloud-gateway}

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

Préoccupations transversales : authentification, limitation de débit (adossée à Redis), CORS, journalisation.

## Modèles de résilience (Resilience4j) {#resilience-patterns-resilience4j}

### Coupe-circuit {#circuit-breaker}

FERMÉ (normal) -> OUVERT (échec immédiat) -> SEMI-OUVERT (sonde) :

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

## Architecture orientée événements {#event-driven-architecture}

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

Publication : `streamBridge.send("destination", event)`

### RabbitMQ vs Kafka {#rabbitmq-vs-kafka}

| Caractéristique | RabbitMQ | Kafka |
|---------|----------|-------|
| Modèle | File de messages, push | Journal distribué, pull |
| Rétention | Supprimé après consommation | Conservé (configurable) |
| Idéal pour | Distribution de tâches | Event sourcing, rejeu, haut débit |

## Sécurité (OAuth2 + KeyCloak) {#security-oauth2-keycloak}

- **Client Credentials** - service à service, sans utilisateur
- **Authorization Code + PKCE** - applications destinées aux utilisateurs
- La passerelle, en tant que client OAuth2, gère la connexion et propage le JWT
- Les services valident le JWT sans état via le point de terminaison JWK Set

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated()
).oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
```

## Équivalents natifs Kubernetes {#kubernetes-native-replacements}

| Spring Cloud | Kubernetes natif |
|-------------|-------------------|
| Eureka (découverte) | DNS de K8s |
| Config Server | ConfigMaps + Secrets |
| Ribbon (répartition de charge) | kube-proxy / Service |
| Spring Cloud Gateway | Ingress / Istio Gateway |

## Pièges à éviter {#gotchas}

- Une base de données par service est indispensable pour une véritable indépendance : les bases partagées créent du couplage
- `depends_on: { condition: service_healthy }` dans Compose garantit un ordre de démarrage correct
- La communication inter-services passe par les noms de service, et non par localhost
- Les coupe-circuits doivent être configurés par dépendance, et non globalement
- Les images natives GraalVM démarrent instantanément mais la compilation est plus longue ; une configuration de la réflexion est nécessaire

## Voir aussi {#see-also}

- [[kubernetes-workloads]] - déploiement de microservices sur K8s
- [[service-mesh-istio]] - résilience au niveau de l'infrastructure
- [[monitoring-and-observability]] - traçage distribué entre services
- [[docker-compose]] - développement local de microservices
- [[deployment-strategies]] - canary/blue-green pour les microservices
