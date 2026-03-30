---
title: Service Mesh
category: patterns
tags: [service-mesh, istio, envoy, sidecar, infrastructure]
---
# Service Mesh

A dedicated infrastructure layer for managing, monitoring, and securing service-to-service communication in microservices architectures, separating business logic from network concerns.

## Key Facts

- Core principle: separate business logic from infrastructure concerns (routing, retries, TLS, observability)
- Implemented via sidecar proxy pattern: each service instance gets a companion proxy (e.g., Envoy) handling all network traffic
- Control plane (Istio, Linkerd) manages configuration; data plane (Envoy sidecars) handles actual traffic
- Provides: mutual TLS, circuit breaking, retries, load balancing, traffic splitting, observability - without changing application code
- Adds latency (extra hop through sidecar) and operational complexity
- Only justified for large microservices deployments (50+ services). For smaller systems, libraries or [[load-balancing]] are sufficient
- See [[microservices-vs-monolith]] for architecture context
- See [[distributed-system-patterns]] for patterns that service mesh implements

## Patterns

### Sidecar proxy architecture

```
Without service mesh:
  [Service A] --HTTP/gRPC--> [Service B]
  (App handles retries, TLS, tracing)

With service mesh:
  [Service A] --> [Envoy A] --mTLS--> [Envoy B] --> [Service B]
  (App sends plain HTTP to localhost, sidecar handles everything)

                    [Control Plane (Istio/Linkerd)]
                         |           |
                    config push  config push
                         |           |
  [Service A]-->[Envoy A]---mTLS---[Envoy B]-->[Service B]
  [Service C]-->[Envoy C]---mTLS---[Envoy D]-->[Service D]
```

### Key capabilities

```
Traffic Management:
  - Load balancing (client-side, per-request)
  - Traffic splitting (canary: 95% v1, 5% v2)
  - Circuit breaking (stop calling failing service)
  - Retries with exponential backoff
  - Timeouts per route

Security:
  - Mutual TLS (mTLS) between all services
  - Certificate rotation (automatic)
  - Authorization policies (service A can call B, not C)
  - No changes to application code

Observability:
  - Distributed tracing (automatic span injection)
  - Metrics (latency, error rate, throughput per service pair)
  - Access logging
  - Service topology visualization
```

### Traffic splitting (canary deployment)

```yaml
# Istio VirtualService: canary deployment
apiVersion: networking.istio.io/v1alpha3
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
        subset: v1
      weight: 95
    - destination:
        host: order-service
        subset: v2
      weight: 5
```

### Circuit breaker

```yaml
# Istio DestinationRule: circuit breaker
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
```

### When to use vs alternatives

| Solution | Complexity | Best for |
|----------|-----------|----------|
| Client library (e.g., Resilience4j) | Low | < 10 services |
| API Gateway only | Medium | External traffic mgmt |
| Service mesh (Linkerd) | High | 20-50 services, simplicity |
| Service mesh (Istio) | Very high | 50+ services, full features |
| eBPF-based (Cilium) | High | Performance-sensitive |

## Gotchas

- **Symptom**: Latency increased 2-5ms per service hop after mesh adoption -> **Cause**: Sidecar proxy adds overhead for every request -> **Fix**: Accept the tradeoff for features gained, or use eBPF-based mesh (Cilium) for lower overhead. Avoid mesh for latency-critical internal paths
- **Symptom**: Debugging harder with service mesh than without -> **Cause**: Failures can be in app, sidecar, or control plane -> **Fix**: Use mesh's built-in observability first (Kiali for Istio). Check sidecar logs alongside app logs. Ensure distributed tracing is enabled
- **Symptom**: Service mesh configuration conflicts with app-level retry logic -> **Cause**: Both app and sidecar retrying = retry amplification -> **Fix**: Disable app-level retries, let mesh handle them. Or disable mesh retries and keep app-level. Never both
- **Symptom**: Massive resource overhead (CPU/memory) from sidecars -> **Cause**: Each pod gets a sidecar consuming 50-100MB RAM -> **Fix**: Right-size sidecar resources per workload. Consider ambient mesh (Istio ambient) which uses per-node proxies instead of per-pod

## See Also

- [[microservices-vs-monolith]] - Service mesh is only for microservices at scale
- [[load-balancing]] - Service mesh includes client-side load balancing
- [[distributed-system-patterns]] - Circuit breaker, retry patterns
- [[orchestration-vs-choreography]] - Service mesh is orthogonal to communication patterns
- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2/overview/)
- [Envoy Proxy](https://www.envoyproxy.io/)
