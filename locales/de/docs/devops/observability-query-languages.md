---
title: "Observability-Abfragesprachen - PromQL, LogQL, TraceQL"
category: concepts
tags: [observability, prometheus, grafana, loki, tempo, promql, logql, traceql, opentelemetry]
level: 3
source_sha256: 1ace9b2b01472ec33b69d46fb080b36207ddd0a6a1e82d2bdff7ceae9e92d05f
translation: machine
translated_at: '2026-10-24'
---
# Observability-Abfragesprachen - PromQL, LogQL, TraceQL {#observability-query-languages-promql-logql-traceql}

Referenz für die drei wichtigsten Abfragesprachen der Observability: Prometheus PromQL für Metriken, Grafana Loki LogQL für Logs und Grafana Tempo TraceQL für Traces. Enthält die OpenTelemetry-Integration und die SRE Golden Signals.

## Key Facts {#key-facts}

- Drei Säulen der Observability: Metriken (Prometheus), Logs (Loki), Traces (Tempo/Jaeger)
- Golden Signals (SRE): Latency, Traffic, Errors, Saturation
- PromQL arbeitet auf Zeitreihen mit Labels; `rate()` berechnet die Rate pro Sekunde über ein Zeitfenster
- LogQL verwendet Label-Selektoren, String- und Regex-Filter sowie eine JSON-Parsing-Pipeline
- TraceQL fragt verteilte Traces nach Dauer, Servicename und Span-Attributen ab
- Das OpenTelemetry SDK bietet eine einheitliche Instrumentierung für alle drei Säulen

## Patterns {#patterns}

### PromQL (Prometheus) {#promql-prometheus}

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

### LogQL (Grafana Loki) {#logql-grafana-loki}

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

### TraceQL (Grafana Tempo) {#traceql-grafana-tempo}

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

### OpenTelemetry in Go {#opentelemetry-in-go}

```go
// Trace context propagation through gRPC metadata
type metadataCarrier struct { md metadata.MD }
func (m *metadataCarrier) Get(key string) string { ... }
func (m *metadataCarrier) Set(key, value string) { ... }
func (m *metadataCarrier) Keys() []string { ... }

// In interceptor:
ctx = otel.GetTextMapPropagator().Extract(ctx, &metadataCarrier{md: incomingMD})
```

HTTP und gRPC mit Middleware bzw. Interceptors instrumentieren. Export nach Jaeger, Tempo oder an einen beliebigen OTLP-Collector.

### Golden Signals {#golden-signals}

| Signal | Was gemessen wird | Beispielmetrik |
|--------|-----------------|----------------|
| Latency | Wie lange Anfragen dauern | `histogram_quantile(0.99, ...)` |
| Traffic | Nachfrage (RPS) | `sum(rate(http_requests_total[1m]))` |
| Errors | Rate fehlgeschlagener Anfragen | `rate(http_requests_total{status!="200"}[1m])` |
| Saturation | Wie „ausgelastet" der Dienst ist | CPU, Speicher, Queue-Tiefe |

### Structured Logging {#structured-logging}

`slog` (Go 1.21 Standardbibliothek) oder `zap`/`zerolog` verwenden. Logs immer mit Kontext schreiben: Request-ID, User-ID, Trace-ID. Für Produktion JSON-Format, für Entwicklung Textformat.

## Gotchas {#gotchas}

- `rate()` in PromQL erfordert einen Counter (monoton steigend); auf einem Gauge angewendet liefert es unsinnige Ergebnisse
- `histogram_quantile` arbeitet auf Histogramm-Buckets - decken die Bucket-Grenzen den Datenbereich nicht ab, sind die Ergebnisse ungenau
- LogQL `unwrap` funktioniert nur auf geparsten numerischen Feldern - sicherstellen, dass das JSON-Parsing das Feld korrekt extrahiert
- TraceQL `duration` bezieht sich auf einzelne Spans; für die Gesamtdauer eines Traces den Root-Span oder Abfragen auf Trace-Ebene verwenden
- Das OpenTelemetry SDK verursacht Overhead - bei Services mit hohem Durchsatz die Sampling-Rate anpassen

## See Also {#see-also}

- [[microservices]] - gRPC-Interceptors für die Injektion von Telemetrie
- [[kafka-messaging-fundamentals]] - Überwachung des Consumer-Lags mit Metriken
