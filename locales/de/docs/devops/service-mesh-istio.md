---
title: "Service Mesh und Istio"
category: concepts
tags: [devops, kubernetes, istio, service-mesh, envoy, mtls, traffic-management]
level: 3
source_sha256: 655bc1a38933539d44d508232d8a8ba0d925ae0dd596901ffed9f23c89993a5c
translation: machine
translated_at: '2026-10-24'
---
# Service Mesh und Istio {#service-mesh-and-istio}

Ein Service Mesh fügt eine eigene Infrastrukturschicht für die Kommunikation zwischen Services hinzu. Es bietet Traffic-Management, Observability, Sicherheit (mTLS) und Zuverlässigkeit (Circuit Breaker, Retries) ohne Änderungen am Anwendungscode.

## Architektur {#architecture}

### Data Plane {#data-plane}

Envoy-Sidecar-Proxys, die in jeden Pod injiziert werden. Sie verarbeiten sämtlichen Netzwerkverkehr ein- und ausgehend für jeden Service.

### Control Plane (istiod) {#control-plane-istiod}

| Komponente | Funktion |
|-----------|----------|
| **Pilot** | Wandelt Routing-Regeln (VirtualService, DestinationRule) in Envoy-Konfiguration um. Verwaltet dynamisches Routing für Canary- und A/B-Tests |
| **Citadel** | Verwaltet Zertifikate für gegenseitiges TLS zwischen Services |
| **Galley** | Validiert Konfigurationen und synchronisiert sich mit der K8s-API |

## Installation {#installation}

```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
# All new pods automatically get Envoy sidecar
```

## Traffic-Flow {#traffic-flow}

1. Externe Anfrage -> LoadBalancer
2. -> Istio-Ingress-Gateway-Pods
3. -> Gateway- und VirtualService-Regeln bestimmen das Ziel
4. -> Envoy-Sidecar im Zielpod empfängt den Traffic
5. -> Die Antwort folgt dem umgekehrten Pfad

## Traffic-Management {#traffic-management}

### VirtualService (Routing-Regeln) {#virtualservice-routing-rules}

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

### DestinationRule (Richtlinien nach dem Routing) {#destinationrule-post-routing-policies}

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

### Gateway (Einstiegspunkt für externen Traffic) {#gateway-external-traffic-entry}

Ersetzt Kubernetes Ingress. Unterstützt TLS-Terminierung und hostbasiertes Routing.

## Mutual TLS (mTLS) {#mutual-tls-mtls}

Automatisches mTLS zwischen allen Services im Mesh:

| Modus | Verhalten |
|------|----------|
| STRICT | Nur mTLS-Traffic erlaubt |
| PERMISSIVE | Sowohl Klartext als auch mTLS werden akzeptiert |
| DISABLE | Keine mTLS-Durchsetzung |

## Observability {#observability}

Automatisch konfiguriert mit Istio-Addons:

- **Kiali** - Dashboard für das Service Mesh, Topologie-Visualisierung
- **Jaeger** - verteiltes Tracing
- **Prometheus + Grafana** - Metriken

## Gotchas {#gotchas}

- Sidecar-Injection erhöht den Cold Start um ca. 100 ms und belegt zusätzlichen Speicher pro Pod
- mTLS im STRICT-Modus unterbricht die Kommunikation mit Services außerhalb des Mesh
- VirtualService und DestinationRule müssen die Service-Namen exakt übereinstimmen lassen
- Debugging mit `istioctl analyze` und `istioctl proxy-status`
- Ressourcenaufwand: istiod plus Sidecar pro Pod erhöht den Ressourcenverbrauch des Clusters

## Siehe auch {#see-also}

- [[kubernetes-services-and-networking]] - K8s-Networking ohne Mesh
- [[deployment-strategies]] - Canary über Istio-Traffic-Splitting
- [[monitoring-and-observability]] - Observability auf Mesh-Ebene
- [[chaos-engineering-and-testing]] - Circuit Breaking, Resilienz
