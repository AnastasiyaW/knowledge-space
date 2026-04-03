---
title: Monitoring and Observability
category: concepts
tags: [devops, monitoring, observability, prometheus, grafana, alerting, sli, golden-signals]
---

# Monitoring and Observability

Monitoring answers "what is broken?" (symptoms) and "why?" (causes). Observability means building a system you can ask any questions about and discover new correlations. Goal: maximize signal, minimize noise.

## Four Golden Signals

1. **Latency** - time to serve requests. Distinguish successful vs failed request latency
2. **Traffic** - demand on system (requests/sec, transactions/sec)
3. **Errors** - rate of failed requests (explicit 5xx + implicit slow responses)
4. **Saturation** - how "full" the service is (CPU, memory, I/O, queue depth)

### Measuring Saturation

- Determine acceptable latency threshold (e.g., 200ms)
- Saturation can be caused by equipment degradation, not just load
- Sawtooth pattern: periodic saturation (e.g., Elasticsearch index merging) causes throughput drops then spikes

## Three Pillars of Observability

| Pillar | What | Tools |
|--------|------|-------|
| **Logging** | What happened | Loki, ELK, CloudWatch Logs |
| **Metrics** | How system performs | Prometheus, CloudWatch, Datadog |
| **Tracing** | Request flow across services | Jaeger, Tempo, Zipkin |

## Prometheus

Pull-based time-series metrics collection:

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

PromQL queries: `rate(http_server_requests_seconds_count[5m])`, `jvm_memory_used_bytes{area="heap"}`

Service discovery: Kubernetes, Consul, file-based. Alertmanager handles alert routing, grouping, silencing.

## Grafana

Visualization platform for Prometheus, Loki, Tempo, Elasticsearch data:

- Import pre-built dashboards (e.g., Node Exporter Full: ID 1860)
- Panels: graph, stat, gauge, table
- Dashboard variables for filtering
- Alerting rules with contact points (email, Slack, PagerDuty)

### Grafana + Loki (Centralized Logging)

Loki indexes labels only (not content) - much lighter than ELK:

```
LogQL: {container_name="accounts"} |= "error"
Rate:  rate({container_name="accounts"}[5m])
```

Promtail agent tails log files on each node, sends to Loki.

### Grafana Tempo (Distributed Tracing)

Receives traces via OTLP. Visualizes request flow as waterfall diagram. Link from Loki logs to Tempo traces via traceId correlation.

## OpenTelemetry

Vendor-neutral instrumentation standard for traces, metrics, logs. Each request gets:
- **traceId** - unique per request chain
- **spanId** - unique per service hop

W3C Trace Context header propagated across services automatically.

## SLI, SLO, SLA

### SLI (Service Level Indicator)
Quantitative measure: latency p95/p99, availability %, error rate, throughput. Measured at user-facing boundary.

### SLO (Service Level Objective)
Target for SLI: "99.9% of requests in < 200ms over 30 days." Internal engineering target.

### SLA (Service Level Agreement)
SLO + consequences (refunds, credits). Typically more lenient than SLO.

### Error Budget
`100% - SLO = error budget`. SLO 99.9% = 0.1% budget = 43.2 min/month. Budget exhausted -> freeze releases, focus on reliability. Budget remaining -> deploy faster.

## Problem Lifecycle

`OK -> Soft -> Hard -> Notify -> Escalate -> Acknowledge -> Resolve`

- Every notification must lead to an action
- Alerts via various transports: email, SMS, IM (offband delivery)
- Context must be attached to every alert

## Alerting Philosophy

- Alert on **symptoms**, not causes (user impact, not CPU usage)
- Every alert should be **actionable**
- Every page should require **human intelligence** to resolve
- Distinguish ticket-worthy vs page-worthy
- Multi-window, multi-burn-rate: fast burn = page, slow burn = ticket

## Data Sources for SLI

- **Application metrics**: implemented in code. Competes with main tasks for resources
- **Infrastructure APIs**: cloud, WAF, network equipment. Great detail, historical data. Knows nothing about app logic
- **Third-party monitoring**: external perspective. Useful for SLA validation
- **Synthetic probes**: black-box checks simulating user behavior

## Cloud-Specific Monitoring

### AWS CloudWatch

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

### Azure Monitor (Container Insights)

KQL queries on container logs, metrics, performance data. OMS Agent as DaemonSet on each node.

## Gotchas

- Monitoring != Observability. Monitoring checks known issues; observability discovers unknowns
- Percentiles (p50, p95, p99) over averages for latency - averages hide outliers
- APDEX (Application Performance Index) standardizes user satisfaction: Satisfied (<T), Tolerating (T-4T), Frustrated (>4T)
- Spring Boot: `spring-boot-starter-actuator` + `micrometer-registry-prometheus` for `/actuator/prometheus`
- Error budget burn rate tracks how fast budget is consumed - a single incident can consume minutes of budget

## See Also

- [[sre-principles]] - SRE philosophy driving monitoring decisions
- [[sre-incident-management]] - on-call, escalation, postmortems
- [[kubernetes-resource-management]] - metrics server for HPA
- [[service-mesh-istio]] - mesh-level observability
