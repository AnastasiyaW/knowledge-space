---
title: "Monitoring und Observability"
category: concepts
tags: [devops, monitoring, observability, prometheus, grafana, alerting, sli, golden-signals]
level: 3
source_sha256: 18d9986c7530f89ac571c3b66ccac62fd667ae124127a2f1532e217d118ad469
translation: machine
translated_at: '2026-10-24'
---
# Monitoring und Observability {#monitoring-and-observability}

Monitoring beantwortet die Fragen „Was ist kaputt?“ (Symptome) und „Warum?“ (Ursachen). Observability bedeutet, ein System zu bauen, das man zu beliebigen Fragen befragen kann und in dem sich neue Zusammenhänge entdecken lassen. Ziel: Signal maximieren, Rauschen minimieren.

## Vier Golden Signals {#four-golden-signals}

1. **Latenz** - Zeit, die zur Beantwortung von Anfragen benötigt wird. Erfolgreiche und fehlgeschlagene Anfrage-Latenzen getrennt betrachten
2. **Traffic** - Last auf dem System (Anfragen/s, Transaktionen/s)
3. **Fehler** - Rate fehlgeschlagener Anfragen (explizite 5xx sowie implizite langsame Antworten)
4. **Sättigung** - wie „voll“ der Dienst ist (CPU, Speicher, I/O, Queue-Tiefe)

### Sättigung messen {#measuring-saturation}

- Akzeptablen Latenz-Schwellenwert festlegen (z. B. 200 ms)
- Sättigung kann durch Verschleiß der Hardware entstehen, nicht nur durch Last
- Sägezahnmuster: periodische Sättigung (z. B. Elasticsearch-Index-Merging) führt zu Einbrüchen und anschließenden Spitzen beim Durchsatz

## Drei Säulen der Observability {#three-pillars-of-observability}

| Säule | Was | Werkzeuge |
|-------|-----|-----------|
| **Logging** | Was ist passiert | Loki, ELK, CloudWatch Logs |
| **Metriken** | Wie performt das System | Prometheus, CloudWatch, Datadog |
| **Tracing** | Anfragefluss über Dienste hinweg | Jaeger, Tempo, Zipkin |

## Prometheus {#prometheus}

Pull-basierte Erfassung von Zeitreihen-Metriken:

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
```

PromQL-Abfragen: `rate(http_server_requests_seconds_count[5m])`, `jvm_memory_used_bytes{area="heap"}`

Service Discovery: Kubernetes, Consul, dateibasiert. Alertmanager übernimmt Alert-Routing, Gruppierung und Stummschaltung.

## Grafana {#grafana}

Visualisierungsplattform für Daten aus Prometheus, Loki, Tempo und Elasticsearch:

- Vorgefertigte Dashboards importieren (z. B. Node Exporter Full: ID 1860)
- Panels: Graph, Stat, Gauge, Tabelle
- Dashboard-Variablen zum Filtern
- Alerting-Regeln mit Kontaktpunkten (E-Mail, Slack, PagerDuty)

### Grafana + Loki (zentralisiertes Logging) {#grafana-loki-centralized-logging}

Loki indiziert nur Labels (nicht den Inhalt) - deutlich leichtgewichtiger als ELK:

```yaml
LogQL: {container_name="accounts"} |= "error"
Rate:  rate({container_name="accounts"}[5m])
```

Der Promtail-Agent liest Logdateien auf jedem Node mit und sendet sie an Loki.

### Grafana Tempo (verteiltes Tracing) {#grafana-tempo-distributed-tracing}

Empfängt Traces über OTLP. Visualisiert den Anfragefluss als Wasserfalldiagramm. Über die traceId-Korrelation lässt sich von Loki-Logs zu Tempo-Traces springen.

## OpenTelemetry {#opentelemetry}

Herstellerneutraler Instrumentierungsstandard für Traces, Metriken und Logs. Jede Anfrage erhält:
- **traceId** - eindeutig pro Anfragekette
- **spanId** - eindeutig pro Dienst-Hop

Der W3C-Trace-Context-Header wird automatisch über Dienste hinweg weitergegeben.

## SLI, SLO, SLA {#sli-slo-sla}

### SLI (Service Level Indicator) {#sli-service-level-indicator}
Quantitatives Maß: Latenz p95/p99, Verfügbarkeit in %, Fehlerrate, Durchsatz. Wird an der nutzerseitigen Grenze gemessen.

### SLO (Service Level Objective) {#slo-service-level-objective}
Zielwert für einen SLI: „99,9 % der Anfragen in < 200 ms über 30 Tage.“ Internes technisches Ziel.

### SLA (Service Level Agreement) {#sla-service-level-agreement}
SLO plus Konsequenzen (Erstattungen, Gutschriften). Üblicherweise weniger streng als das SLO.

### Error Budget {#error-budget}
`100% - SLO = error budget`. SLO 99,9 % = 0,1 % Budget = 43,2 Minuten/Monat. Budget aufgebraucht -> Releases einfrieren, Fokus auf Zuverlässigkeit. Budget vorhanden -> schneller ausliefern.

## Lebenszyklus eines Problems {#problem-lifecycle}

`OK -> Soft -> Hard -> Notify -> Escalate -> Acknowledge -> Resolve`

- Jede Benachrichtigung muss zu einer Handlung führen
- Alarme über verschiedene Kanäle: E-Mail, SMS, IM (Offband-Zustellung)
- Jedem Alarm muss Kontext beigefügt sein

## Alerting-Philosophie {#alerting-philosophy}

- Auf **Symptome** alarmieren, nicht auf Ursachen (Auswirkung auf Nutzer, nicht CPU-Auslastung)
- Jeder Alarm sollte **umsetzbar** sein
- Jede Page sollte **menschliches Urteilsvermögen** zur Lösung erfordern
- Unterscheiden, was ein Ticket und was eine Page auslösen sollte
- Multi-Window, Multi-Burn-Rate: schneller Verbrauch = Page, langsamer Verbrauch = Ticket

## Datenquellen für SLIs {#data-sources-for-sli}

- **Anwendungsmetriken**: im Code implementiert. Konkurrieren mit den Hauptaufgaben um Ressourcen
- **Infrastruktur-APIs**: Cloud, WAF, Netzwerkgeräte. Hohe Detailtiefe, historische Daten. Kennen die Anwendungslogik nicht
- **Drittanbieter-Monitoring**: externe Sicht. Nützlich zur SLA-Validierung
- **Synthetische Probes**: Black-Box-Prüfungen, die Nutzerverhalten simulieren

## Cloud-spezifisches Monitoring {#cloud-specific-monitoring}

### AWS CloudWatch {#aws-cloudwatch}

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "HighCPU" \
  --metric-name "CPUUtilization" \
  --namespace "AWS/EC2" \
  --statistic "Average" \
  --period 300 --threshold 80 \
  --comparison-operator "GreaterThanThreshold" \
  --alarm-actions arn:aws:sns:us-east-1:123456:alert-topic
```

### Azure Monitor (Container Insights) {#azure-monitor-container-insights}

KQL-Abfragen auf Container-Logs, Metriken und Performancedaten. OMS-Agent als DaemonSet auf jedem Node.

## Stolperfallen {#gotchas}

- Monitoring != Observability. Monitoring prüft bekannte Probleme; Observability entdeckt Unbekanntes
- Für Latenzen Perzentile (p50, p95, p99) statt Durchschnittswerten verwenden - Durchschnitte verbergen Ausreißer
- Der APDEX (Application Performance Index) standardisiert die Nutzerzufriedenheit: Zufrieden (<T), Toleriert (T-4T), Frustriert (>4T)
- Spring Boot: `spring-boot-starter-actuator` + `micrometer-registry-prometheus` für `/actuator/prometheus`
- Die Burn Rate des Error Budgets zeigt, wie schnell das Budget verbraucht wird - ein einziger Vorfall kann Minuten an Budget kosten

## Siehe auch {#see-also}

- [[sre-principles]] - SRE-Philosophie, die Monitoring-Entscheidungen prägt
- [[sre-incident-management]] - Bereitschaft, Eskalation, Postmortems
- [[kubernetes-resource-management]] - Metrics Server für HPA
- [[service-mesh-istio]] - Observability auf Mesh-Ebene
