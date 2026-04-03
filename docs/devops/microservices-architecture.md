---
title: Microservices Architecture
category: architecture
tags: [microservices, service-mesh, api-gateway, distributed-systems, spring-boot, istio]
---
# Microservices Architecture

Designing, deploying, and operating distributed microservice systems.

## Key Facts

- **Microservice** = independently deployable service responsible for a single business capability
- Each service owns its data (database per service); NO shared databases between services
- Communication: **synchronous** (REST, gRPC) vs **asynchronous** (message queues, event streaming)
- **API Gateway** = single entry point; routing, auth, rate limiting (Kong, NGINX, AWS API Gateway)
- **Service Mesh** = infrastructure layer handling service-to-service communication (Istio, Linkerd)
- **Service discovery** = how services find each other; client-side (Eureka) or server-side (K8s DNS)
- **Circuit breaker** = prevent cascade failures; states: closed (OK), open (failing), half-open (testing)
- **Saga pattern** = distributed transactions across services; choreography (events) or orchestration (coordinator)
- **Sidecar pattern** = helper container alongside main container (Envoy proxy in Istio)
- [[kubernetes-services]] provide built-in service discovery and load balancing
- [[monitoring-observability]] is critical - distributed tracing ties requests across services
- [[docker-images-containers]] package each microservice independently
- 12-Factor App principles: config in env vars, stateless processes, port binding, disposability

## Patterns

```yaml
# Spring Boot microservice - Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: order-service
        image: myorg/order-service:2.1.0
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "kubernetes"
        - name: PAYMENT_SERVICE_URL
          value: "http://payment-service:8080"
        - name: KAFKA_BOOTSTRAP_SERVERS
          value: "kafka:9092"
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
```

```
# Communication patterns

Synchronous (REST/gRPC):
  Client -> API Gateway -> Service A -> Service B
  + Simple, familiar
  - Tight coupling, cascading failures, latency chains

Asynchronous (Events/Messages):
  Service A -> Message Broker (Kafka/RabbitMQ) -> Service B
  + Loose coupling, resilience, scalability
  - Eventual consistency, debugging complexity

# Circuit Breaker states
CLOSED  --[failures > threshold]--> OPEN
OPEN    --[timeout expires]-------> HALF-OPEN
HALF-OPEN --[test succeeds]-------> CLOSED
HALF-OPEN --[test fails]----------> OPEN
```

```yaml
# Istio VirtualService (traffic management)
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - route:
    - destination:
        host: order-service
        subset: v2
      weight: 90
    - destination:
        host: order-service
        subset: v1
      weight: 10
    timeout: 3s
    retries:
      attempts: 3
      perTryTimeout: 1s
```

## Gotchas

- "Distributed monolith" = microservices that are tightly coupled and must deploy together; worse than a monolith
- Network IS the problem: latency, partial failures, message ordering are constant concerns
- Database per service means no JOINs across services; use API composition or CQRS pattern
- Start with a monolith, extract services when boundaries are clear ("monolith first" - Martin Fowler)
- Service mesh adds latency (~1-2ms per hop) and operational complexity; evaluate if you need it
- Distributed tracing is NOT optional for microservices; instrument from day one
- Event-driven architecture requires idempotent consumers (same message processed twice = same result)
- Testing microservices: contract testing (Pact) + integration testing + chaos engineering

## See Also

- [[kubernetes-services]] - service discovery and load balancing
- [[monitoring-observability]] - distributed tracing
- [[deployment-strategies]] - canary and blue-green for services
- [[docker-images-containers]] - containerizing microservices
- 12-Factor App: https://12factor.net/
- Microservices patterns: https://microservices.io/patterns/
