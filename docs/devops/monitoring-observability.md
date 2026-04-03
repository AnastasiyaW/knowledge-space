---
title: Monitoring & Observability
category: operations
tags: [monitoring, observability, prometheus, grafana, metrics, logs, traces, alerting]
---
# Monitoring & Observability

Three pillars of observability: metrics, logs, traces. Prometheus + Grafana stack, alerting strategies.

## Key Facts

- **Monitoring** answers "what is broken?"; **Observability** answers "why is it broken?"
- Three pillars: **Metrics** (numerical time-series), **Logs** (event records), **Traces** (request flow)
- **Prometheus** = pull-based metrics collection; scrapes `/metrics` endpoints; PromQL for queries
- **Grafana** = visualization dashboards; supports Prometheus, Loki, Elasticsearch, CloudWatch data sources
- **Loki** = log aggregation (Grafana's log solution); uses same label concept as Prometheus
- **Jaeger/Tempo** = distributed tracing; follows requests across microservices
- **USE method** (Brendan Gregg): for resources - Utilization, Saturation, Errors
- **RED method**: for services - Rate, Errors, Duration
- **Four Golden Signals** (Google SRE): Latency, Traffic, Errors, Saturation
- [[sre-sli-slo-sla]] define what metrics to track and threshold values
- [[kubernetes-pods]] expose metrics via sidecar or application instrumentation
- [[ci-cd-pipelines]] can gate deployments on monitoring signals
- **Alert fatigue** = too many alerts; prioritize actionable alerts with clear runbooks

## Patterns

```yaml
# Prometheus scrape config (prometheus.yml)
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

```yaml
# Prometheus alerting rules (alerts.yml)
groups:
- name: application
  rules:
  - alert: HighErrorRate
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m])) /
      sum(rate(http_requests_total[5m])) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate ({{ $value | humanizePercentage }})"
      runbook_url: "https://wiki.example.com/runbook/high-error-rate"

  - alert: HighLatency
    expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 10m
    labels:
      severity: warning

  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 5m
    labels:
      severity: warning
```

```promql
# PromQL examples
rate(http_requests_total[5m])                              # requests per second
histogram_quantile(0.99, rate(http_duration_bucket[5m]))   # p99 latency
sum by (status) (rate(http_requests_total[5m]))            # grouped by status
increase(errors_total[1h])                                 # total errors in last hour
avg_over_time(cpu_usage[1h])                               # average CPU over 1h
```

```bash
# Prometheus / Grafana on K8s via Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# Port forward Grafana
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
# Default creds: admin/prom-operator
```

## Gotchas

- Prometheus stores data locally by default; for long-term storage use Thanos or Cortex
- High cardinality labels (user_id, request_id) cause Prometheus memory explosion; use logs for high-cardinality data
- `rate()` requires counter metric type; `increase()` is syntactic sugar for `rate() * seconds`
- Alert `for:` duration = how long condition must be true before firing; too short = flapping alerts
- Grafana dashboards as code: export as JSON, store in version control, provision via ConfigMaps
- Scrape interval vs evaluation interval: scrape = how often data is collected; evaluation = how often alerts are checked
- [[sre-sli-slo-sla]] error budgets should drive alert thresholds, not arbitrary percentages

## See Also

- [[sre-sli-slo-sla]] - defining what and when to alert
- [[kubernetes-pods]] - pod-level metrics and probes
- [[incident-management]] - responding to alerts
- [[microservices-architecture]] - distributed tracing across services
- Prometheus docs: https://prometheus.io/docs/
- Grafana docs: https://grafana.com/docs/grafana/latest/
