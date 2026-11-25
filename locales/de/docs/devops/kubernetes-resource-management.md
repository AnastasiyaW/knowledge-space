---
title: "Kubernetes-Ressourcenverwaltung"
category: concepts
tags: [devops, kubernetes, resources, limits, quotas, autoscaling, hpa, namespaces]
level: 3
source_sha256: e692cdccb21ec87b00b0770a5e49f7b756a03aeecefd5985bc8b1abfa648535c
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes-Ressourcenverwaltung {#kubernetes-resource-management}

Die Ressourcenverwaltung steuert, wie CPU und Speicher im Cluster zugewiesen, verbraucht und begrenzt werden. Eine korrekte Konfiguration verhindert Noisy Neighbors und sorgt für eine faire Ressourcenverteilung.

## Requests und Limits {#requests-and-limits}

Pro Container definiert, nicht pro Pod:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "200m"
    memory: "256Mi"
```

- **Requests** - garantiertes Minimum. Der Scheduler verwendet diesen Wert für Platzierungsentscheidungen
- **Limits** - maximal erlaubter Verbrauch
- CPU in Millicores: 1000m = 1 vCPU
- Speicher in Mi/Gi

### Überschreiten von Limits {#exceeding-limits}

| Ressource | Verhalten | Typ |
|-----------|-----------|-----|
| CPU | Gedrosselt (nicht beendet) | Komprimierbar - kann umverteilt werden |
| Speicher | OOMKilled | Nicht komprimierbar - wird nur durch Beenden zurückgewonnen |

## QoS-Klassen {#qos-classes}

Werden automatisch anhand der Konfiguration von Requests und Limits zugewiesen. Sie bestimmen die Eviction-Priorität (BestEffort zuerst, Guaranteed zuletzt):

| Klasse | Bedingung | Anwendungsfall |
|--------|-----------|----------------|
| **Guaranteed** | Alle Container: Limits == Requests für CPU und Speicher | Datenbanken, kritische Dienste |
| **Burstable** | Mindestens ein Container: Requests < Limits | Webdienste, Apps mit variabler Last |
| **BestEffort** | Keine Requests oder Limits gesetzt | Nur Testumgebungen |

## Namespaces {#namespaces}

Virtuelle Cluster innerhalb eines physischen Clusters. Sie bieten eine Isolationsgrenze und eine Ressourcensteuerung pro Namespace.

```bash
kubectl create namespace dev
kubectl apply -f manifest.yaml -n dev
kubectl get pods -n dev
kubectl delete ns dev           # deletes namespace + ALL contents
```

**Standard-Namespaces**: `default`, `kube-system` (CoreDNS, kube-proxy, metrics-server), `kube-public`, `kube-node-lease`.

Dasselbe Manifest lässt sich ohne Namensänderung in mehrere Namespaces deployen - einfach `-n <namespace>` verwenden.

## LimitRange {#limitrange}

Richtlinie pro Container innerhalb eines Namespace. Weist Standardwerte zu und erzwingt Minimal- und Maximalwerte:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-mem-limit-range
  namespace: dev
spec:
  limits:
  - type: Container
    default:            # default limits
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:     # default requests
      cpu: "300m"
      memory: "256Mi"
    min:
      cpu: "100m"
      memory: "64Mi"
    max:
      cpu: "2"
      memory: "2Gi"
```

Pods, die eine LimitRange verletzen, werden bei der Erstellung abgelehnt.

## ResourceQuota {#resourcequota}

Namespace-weites Budget für den aggregierten Ressourcenverbrauch:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ns-resource-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "4Gi"
    limits.cpu: "8"
    limits.memory: "8Gi"
    pods: "20"
    configmaps: "10"
    persistentvolumeclaims: "10"
    secrets: "10"
    services: "10"
```

Neue Pods schlagen mit "exceeded quota" fehl, sobald die Summen im Namespace erreicht sind.

**Wichtige Unterscheidung**: LimitRange = Richtlinie pro Container. ResourceQuota = namespace-weites Budget. Beide wirken zusammen.

## Horizontal Pod Autoscaler (HPA) {#horizontal-pod-autoscaler-hpa}

Skaliert Pod-Replikate anhand der CPU- bzw. Speicherauslastung. Benötigt den Metrics Server.

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-demo
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```

```bash
kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10
kubectl get hpa
```

- Scale-up: sofort, sobald das Ziel überschritten wird
- Scale-down: 5-minütige Abkühlphase
- Erfordert gesetzte Ressourcen-Requests auf den Containern

## Cluster Autoscaler {#cluster-autoscaler}

Skaliert Worker-Nodes anhand der ausstehenden Pod-Anforderungen:

```bash
az aks create --enable-cluster-autoscaler --min-count 1 --max-count 5
```

- Stellt neue Nodes bereit, wenn Pods nicht geplant werden können (1-3 Minuten)
- Entfernt unterausgelastete Nodes nach einer Abkühlphase
- Requests und Limits bestimmen die Entscheidung - große Requests erzwingen eine schnellere Bereitstellung neuer Nodes

### HPA und Cluster Autoscaler gemeinsam {#hpa-cluster-autoscaler-together}

HPA erhöht die Pods -> unzureichende Node-Ressourcen -> Cluster Autoscaler fügt Nodes hinzu -> Pods werden geplant. Beim Scale-down läuft der Vorgang umgekehrt.

## Node Selectors {#node-selectors}

Pods gezielt auf bestimmte Node-Pools planen:

```yaml
spec:
  nodeSelector:
    nodepoolos: linux           # Linux user pool
    # OR
    kubernetes.io/os: windows   # Windows pool
    # OR
    type: virtual-kubelet       # Virtual nodes (ACI/Fargate)
```

## Fallstricke {#gotchas}

- Ohne Requests hat der Scheduler keine Informationen für die Platzierung - Pods landen zufällig
- Ohne Speicherlimits kann ein einzelner Container den gesamten Node per OOMKill beenden
- Wenn kein CPU-`default` in der LimitRange angegeben ist, weist das System jedem Container 1 vCPU (1000m) zu
- ResourceQuota blockiert die Skalierung, sobald das Quota erreicht ist - neue Pods bleiben im Status Pending
- Der Metrics Server muss laufen, damit der HPA funktioniert (Standard in verwalteten Kubernetes-Diensten)
- Den `default`-Namespace niemals löschen

## Siehe auch {#see-also}

- [[kubernetes-architecture]] - Cluster-Komponenten
- [[kubernetes-workloads]] - Pods, Deployments
- [[kubernetes-on-aks]] - AKS-spezifische Ressourcenverwaltung
- [[kubernetes-on-eks]] - EKS-spezifische Autoskalierung
