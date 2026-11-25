---
title: "Chaos Engineering und Reliability-Tests"
category: concepts
tags: [devops, sre, chaos-engineering, testing, load-testing, resilience]
level: 3
source_sha256: e87b42779c733a99bb68a5f0a86859d5f484f3f473dced37d66ae4448341d48a
translation: machine
translated_at: '2026-10-24'
---
# Chaos Engineering und Reliability-Tests {#chaos-engineering-and-reliability-testing}

Reliability-Tests überprüfen das Systemverhalten unter Last und bei Ausfällen. Chaos Engineering injiziert gezielt Fehler, um Schwachstellen zu finden, bevor sie zu Ausfällen führen.

## Infrastructure Testing Pyramid {#infrastructure-testing-pyramid}

1. **Konfigurationsvalidierung** (Unit) - Syntaxprüfungen, Schema-Validierung
2. **Infrastruktur-Integration** - Tests der Dienstinteraktion
3. **System-Ebene** - Validierung des gesamten Stacks
4. **Chaos** - Fehlerinjektion

## Arten von Reliability-Tests {#reliability-testing-types}

| Typ | Zweck | Tools |
|-----|-------|-------|
| **Load Testing** | Anhaltende erwartete Last, Überprüfung der SLOs | k6, Locust, JMeter |
| **Stress Testing** | Last über das Erwartete hinaus, Ermittlung des Breaking Points | k6, Gatling |
| **Soak Testing** | Lange Laufzeit, Erkennung von Leaks/Erschöpfung | k6, eigene Lösung |
| **Chaos Engineering** | Fehler injizieren, Resilienz überprüfen | Chaos Monkey, Litmus, Gremlin |

## Chaos Engineering {#chaos-engineering}

### Voraussetzungen {#prerequisites}

1. Funktionierender Incident-Management-Prozess
2. Kultur des Lernens aus Fehlern (schuldzuweisungsfrei)
3. Vertrauen innerhalb der Organisation
4. Gute Observability/Monitoring

### Prinzipien {#principles}

1. Steady State definieren (normale SLI-Werte)
2. Hypothese aufstellen, dass der Steady State während des Experiments bestehen bleibt
3. Realistische Ereignisse einführen (Pod beenden, Netzwerkpartition, volle Festplatte)
4. Versuchen, die Hypothese zu widerlegen
5. Blast Radius minimieren (klein beginnen, automatischer Kill Switch)

### Tools {#tools}

- **Chaos Monkey** (Netflix) - beendet Instanzen zufällig
- **Litmus** - Chaos-Engineering-Lösung für Kubernetes
- **Gremlin** - SaaS-Chaos-Plattform
- **PowerfulSeal** - Fehlerinjektion für K8s-Pods/-Nodes

## Game Days {#game-days}

Geplante Reliability-Übungen, die reale Incidents simulieren:

1. Szenario und Umfang definieren
2. Betroffene Teams benachrichtigen
3. Simulierten Ausfall ausführen
4. Reaktion des Teams beobachten
5. Nachbesprechung durchführen und Erkenntnisse dokumentieren

Regelmäßiger Rhythmus (monatlich/quartalsweise). Testet Runbooks, Alerting und Kommunikation.

## Infrastructure-Testing-Tools {#infrastructure-testing-tools}

### InSpec (Compliance) {#inspec-compliance}

```ruby
control 'sshd-8' do
  impact 0.6
  title 'Server: Configure the service port'
  describe sshd_config do
    its('Port') { should cmp 22 }
  end
end
```

### Testinfra (Python + Pytest) {#testinfra-python-pytest}

```python
def test_access(host):
    addr = host.addr("google.com")
    assert addr.is_resolvable
    assert addr.port(443).is_reachable
```

### Konfigurationsvalidierung {#configuration-validation}

```bash
nginx -t -c nginx.conf
terraform validate
ansible --check
kubectl apply --dry-run=client -f deploy.yml
yamllint file.yaml
python -m json.tool sample.json
```

## Resilienzmuster {#resilience-patterns}

### Circuit Breaker {#circuit-breaker}

Drei Zustände: CLOSED (normal) -> OPEN (Fail Fast) -> HALF-OPEN (Erholung prüfen).

```java
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() { ... }
```

### Load Shedding {#load-shedding}

Anfragen bei voller Auslastung ablehnen. 503 zurückgeben. Besser 80 % der Anfragen erfolgreich bedienen als 100 % langsam.

### Rate Limiting {#rate-limiting}

- Pro Client (Token Bucket, Sliding Window)
- Global (verteilter Zähler in Redis)
- Adaptiv (Anpassung an die aktuelle Last)
- Back-Pressure-Weitergabe

### Graceful Degradation {#graceful-degradation}

- Zwischengespeicherte/veraltete Daten zurückgeben, wenn das Backend nicht verfügbar ist
- Nicht kritische Funktionen unter Last deaktivieren
- Prioritätswarteschlangen für die Anfragenverarbeitung

## Performance-Metriken {#performance-metrics}

### APDEX (Application Performance Index) {#apdex-application-performance-index}

Standardisierte Nutzerzufriedenheit: Zufrieden (<T), Toleriert (T-4T), Frustriert (>4T).

Score = (Zufrieden + Toleriert/2) / Gesamt. Wertebereich 0-1.

### Perzentile statt Durchschnittswerte {#percentiles-over-averages}

p50, p95, p99 für Latenz. Durchschnittswerte verbergen Ausreißer und Tail Latency.

## Stolperfallen {#gotchas}

- Chaos Engineering ohne funktionierende Incident-Response ist verantwortungslos
- Zu großer Blast Radius = echter Ausfall, kein Experiment
- Lasttests sollten realistische Daten und Zugriffsmuster enthalten
- Soak-Tests werden oft übersprungen, erkennen aber Memory Leaks, die kurze Tests übersehen
- `siege -c 50 -t 30s http://localhost:80` für schnelle Lasttests

## Siehe auch {#see-also}

- [[sre-principles]] - Error Budgets und Reliability-Ziele
- [[sre-incident-management]] - durch Chaos getestete Incident-Response
- [[monitoring-and-observability]] - Erkennung der Auswirkungen von Chaos-Experimenten
- [[service-mesh-istio]] - Circuit Breaking, Retries, Timeouts
