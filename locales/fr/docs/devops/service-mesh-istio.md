---
title: "Service Mesh et Istio"
category: concepts
tags: [devops, kubernetes, istio, service-mesh, envoy, mtls, traffic-management]
level: 3
source_sha256: 655bc1a38933539d44d508232d8a8ba0d925ae0dd596901ffed9f23c89993a5c
translation: machine
translated_at: '2026-10-24'
---
# Service Mesh et Istio {#service-mesh-and-istio}

Un service mesh ajoute une couche d'infrastructure dédiée à la communication entre services. Il fournit la gestion du trafic, l'observabilité, la sécurité (mTLS) et la fiabilité (circuit breakers, retries) sans modification du code applicatif.

## Architecture {#architecture}

### Plan de données {#data-plane}

Des proxys sidecar Envoy sont injectés dans chaque pod. Ils gèrent l'ensemble du trafic réseau entrant et sortant de chaque service.

### Plan de contrôle (istiod) {#control-plane-istiod}

| Composant | Fonction |
|-----------|----------|
| **Pilot** | Convertit les règles de routage (VirtualService, DestinationRule) en configuration Envoy. Gère le routage dynamique pour le canary, les tests A/B |
| **Citadel** | Gère les certificats pour le mutual TLS entre services |
| **Galley** | Valide les configurations, se synchronise avec l'API K8s |

## Installation {#installation}

```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
# All new pods automatically get Envoy sidecar
```

## Flux de trafic {#traffic-flow}

1. Requête externe -> LoadBalancer
2. -> Pods Istio Ingress Gateway
3. -> Les règles Gateway + VirtualService déterminent la cible
4. -> Le sidecar Envoy du pod cible reçoit le trafic
5. -> La réponse emprunte le chemin inverse

## Gestion du trafic {#traffic-management}

### VirtualService (règles de routage) {#virtualservice-routing-rules}

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

### DestinationRule (politiques post-routage) {#destinationrule-post-routing-policies}

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

### Gateway (point d'entrée du trafic externe) {#gateway-external-traffic-entry}

Remplace Kubernetes Ingress. Prend en charge la terminaison TLS et le routage basé sur l'hôte.

## Mutual TLS (mTLS) {#mutual-tls-mtls}

mTLS automatique entre tous les services du mesh :

| Mode | Comportement |
|------|--------------|
| STRICT | Seul le trafic mTLS est autorisé |
| PERMISSIVE | Le trafic en clair et mTLS sont acceptés |
| DISABLE | Aucune application du mTLS |

## Observabilité {#observability}

Configurée automatiquement avec les addons Istio :

- **Kiali** - tableau de bord du service mesh, visualisation de la topologie
- **Jaeger** - traçage distribué
- **Prometheus + Grafana** - métriques

## Points de vigilance {#gotchas}

- L'injection du sidecar ajoute environ 100 ms au démarrage à froid et une surcharge mémoire par pod
- Le mTLS en mode STRICT interrompt la communication avec les services hors du mesh
- VirtualService et DestinationRule doivent correspondre exactement aux noms de services
- Déboguer avec `istioctl analyze` et `istioctl proxy-status`
- Surcharge de ressources : istiod et un sidecar par pod augmentent la consommation de ressources du cluster

## Voir aussi {#see-also}

- [[kubernetes-services-and-networking]] - réseau K8s sans mesh
- [[deployment-strategies]] - canary via le découpage de trafic Istio
- [[monitoring-and-observability]] - observabilité au niveau du mesh
- [[chaos-engineering-and-testing]] - circuit breaking, résilience
