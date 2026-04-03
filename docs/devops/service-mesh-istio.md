---
title: Service Mesh and Istio
category: concepts
tags: [devops, kubernetes, istio, service-mesh, envoy, mtls, traffic-management]
---

# Service Mesh and Istio

A service mesh adds a dedicated infrastructure layer for service-to-service communication. It provides traffic management, observability, security (mTLS), and reliability (circuit breakers, retries) without application code changes.

## Architecture

### Data Plane

Envoy sidecar proxies injected into every pod. Handle all network traffic in/out of each service.

### Control Plane (istiod)

| Component | Function |
|-----------|----------|
| **Pilot** | Converts routing rules (VirtualService, DestinationRule) to Envoy config. Manages dynamic routing for canary, A/B testing |
| **Citadel** | Manages certificates for mutual TLS between services |
| **Galley** | Validates configurations, syncs with K8s API |

## Installation

```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
# All new pods automatically get Envoy sidecar
```

## Traffic Flow

1. External request -> LoadBalancer
2. -> Istio Ingress Gateway pods
3. -> Gateway + VirtualService rules determine target
4. -> Envoy sidecar in target pod receives traffic
5. -> Response follows reverse path

## Traffic Management

### VirtualService (Routing Rules)

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: accounts
spec:
  hosts: [accounts]
  http:
  - route:
    - destination:
        host: accounts
        subset: v1
      weight: 90
    - destination:
        host: accounts
        subset: v2
      weight: 10    # 10% canary traffic
```

### DestinationRule (Post-Routing Policies)

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: accounts
spec:
  host: accounts
  trafficPolicy:
    connectionPool:
      http:
        h2UpgradePolicy: DEFAULT
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: v1
    labels: {version: v1}
  - name: v2
    labels: {version: v2}
```

### Gateway (External Traffic Entry)

Replaces Kubernetes Ingress. Supports TLS termination, host-based routing.

## Mutual TLS (mTLS)

Automatic mTLS between all services in mesh:

| Mode | Behavior |
|------|----------|
| STRICT | Only mTLS traffic allowed |
| PERMISSIVE | Both plain and mTLS accepted |
| DISABLE | No mTLS enforcement |

## Observability

Auto-configured with Istio addons:

- **Kiali** - service mesh dashboard, topology visualization
- **Jaeger** - distributed tracing
- **Prometheus + Grafana** - metrics

## Gotchas

- Sidecar injection adds ~100ms to cold start and memory overhead per pod
- mTLS in STRICT mode breaks communication with non-mesh services
- VirtualService and DestinationRule must match service names exactly
- Debug with `istioctl analyze` and `istioctl proxy-status`
- Resource overhead: istiod + sidecar per pod increases cluster resource usage

## See Also

- [[kubernetes-services-and-networking]] - K8s networking without mesh
- [[deployment-strategies]] - canary via Istio traffic splitting
- [[monitoring-and-observability]] - mesh-level observability
- [[chaos-engineering-and-testing]] - circuit breaking, resilience
