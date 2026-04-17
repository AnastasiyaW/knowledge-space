---
title: Observability Query Languages - PromQL, LogQL, TraceQL
category: concepts
tags: [observability, prometheus, grafana, loki, tempo, promql, logql, traceql, opentelemetry]
---

# Observability Query Languages - PromQL, LogQL, TraceQL

Reference for the three main observability query languages - Prometheus PromQL for metrics, Grafana Loki LogQL for logs, and Grafana Tempo TraceQL for traces. Includes OpenTelemetry integration and SRE golden signals.

## Key Facts

- Three pillars of observability: Metrics (Prometheus), Logs (Loki), Traces (Tempo/Jaeger)
- Golden signals (SRE): Latency, Traffic, Errors, Saturation
- PromQL operates on time series with labels; `rate()` calculates per-second rate over a window
- LogQL uses label selectors + string/regex filters + JSON parsing pipeline
- TraceQL queries distributed traces by duration, service name, span attributes
- OpenTelemetry SDK provides unified instrumentation across all three pillars

## Patterns

### PromQL (Prometheus)

```promql
# Request rate (per second, 1-min window)
sum(rate(http_server_requests_total[1m]))

# Error rate by endpoint
sum(rate(http_server_requests_total{status!="200"}[1m])) by (method)

# Error percentage
(
  sum(rate(http_server_requests_total{status!="200"}[1m]))
  /
  sum(rate(http_server_requests_total[1m]))
) * 100

# Latency percentiles (histogram)
histogram_quantile(0.50, sum(rate(http_server_request_duration_seconds_bucket[1m])) by (le, method))
histogram_quantile(0.90, sum(rate(http_server_request_duration_seconds_bucket[1m])) by (le, method))
histogram_quantile(0.95, sum(rate(http_server_request_duration_seconds_bucket[1m])) by (le, method))
histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket[1m])) by (le, method))

# Average latency
sum(rate(http_server_request_duration_seconds_sum[1m])
  / rate(http_server_request_duration_seconds_count[1m])) by (method)
```

### LogQL (Grafana Loki)

```logql
# Basic label selector
{compose_service="app", level="info"}

# String filter operators
{..} |= "server"    # contains
{..} != "debug"     # not contains
{..} |~ "err.*500"  # regex match
{..} !~ "health"    # regex not match

# JSON log parsing pipeline
{app_name="my-app"} | json | method = "GET" and status != "200"

# Rate of error log lines
sum(rate({app_name="my-app"} | json | level = "error" [1m])) by (method)

# Latency quantile from logs
quantile_over_time(0.9,
  {app_name="my-app"} | json | code=~"400|500"
  | unwrap duration[1m]) by (method)
```

### TraceQL (Grafana Tempo)

```traceql
# Find slow traces
{duration > 5s}

# By service and status
{resource.service.name="order-service" && span.http.response.status_code >= 400}

# Rate of spans
{resource.service.name="order-service"} | rate() by (span.http.response.status_code)

# Latency quantiles
{span.http.response.status_code = 200} | quantile_over_time(duration, .999, .99, .9)
```

### OpenTelemetry in Go

```go
// Trace context propagation through gRPC metadata
type metadataCarrier struct { md metadata.MD }
func (m *metadataCarrier) Get(key string) string { ... }
func (m *metadataCarrier) Set(key, value string) { ... }
func (m *metadataCarrier) Keys() []string { ... }

// In interceptor:
ctx = otel.GetTextMapPropagator().Extract(ctx, &metadataCarrier{md: incomingMD})
```

Instrument HTTP and gRPC with middleware/interceptors. Export to Jaeger, Tempo, or any OTLP collector.

### Golden Signals

| Signal | What it measures | Example metric |
|--------|-----------------|----------------|
| Latency | How long requests take | `histogram_quantile(0.99, ...)` |
| Traffic | Demand (RPS) | `sum(rate(http_requests_total[1m]))` |
| Errors | Rate of failed requests | `rate(http_requests_total{status!="200"}[1m])` |
| Saturation | How "full" the service is | CPU, memory, queue depth |

### Structured Logging

Use `slog` (Go 1.21 stdlib) or `zap`/`zerolog`. Always log with context: request ID, user ID, trace ID. JSON format for production, text for development.

## Gotchas

- `rate()` in PromQL requires a counter (monotonically increasing); using it on a gauge produces nonsense
- `histogram_quantile` operates on histogram buckets - if bucket boundaries don't cover your data range, results are inaccurate
- LogQL `unwrap` only works on parsed numeric fields - ensure JSON parsing extracts the field correctly
- TraceQL `duration` is span-level; for total trace duration use root span or trace-level queries
- OpenTelemetry SDK adds overhead - tune sampling rate for high-throughput services

## See Also

- [[microservices]] - gRPC interceptors for telemetry injection
- [[kafka-messaging-fundamentals]] - monitoring consumer lag with metrics
