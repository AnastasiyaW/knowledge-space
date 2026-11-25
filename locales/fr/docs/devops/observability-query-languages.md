---
title: "Langages de requête d'observabilité - PromQL, LogQL, TraceQL"
category: concepts
tags: [observability, prometheus, grafana, loki, tempo, promql, logql, traceql, opentelemetry]
level: 3
source_sha256: 1ace9b2b01472ec33b69d46fb080b36207ddd0a6a1e82d2bdff7ceae9e92d05f
translation: machine
translated_at: '2026-10-24'
---
# Langages de requête d'observabilité - PromQL, LogQL, TraceQL {#observability-query-languages-promql-logql-traceql}

Référence des trois principaux langages de requête d'observabilité : Prometheus PromQL pour les métriques, Grafana Loki LogQL pour les journaux, et Grafana Tempo TraceQL pour les traces. Inclut l'intégration OpenTelemetry et les golden signals SRE.

## Points clés {#key-facts}

- Trois piliers de l'observabilité : Métriques (Prometheus), Journaux (Loki), Traces (Tempo/Jaeger)
- Golden signals (SRE) : Latence, Trafic, Erreurs, Saturation
- PromQL opère sur des séries temporelles avec des labels ; `rate()` calcule le taux par seconde sur une fenêtre
- LogQL utilise des sélecteurs de labels + des filtres chaîne/regex + un pipeline d'analyse JSON
- TraceQL interroge les traces distribuées par durée, nom de service et attributs de span
- Le SDK OpenTelemetry fournit une instrumentation unifiée pour les trois piliers

## Patrons {#patterns}

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

### OpenTelemetry en Go {#opentelemetry-in-go}

```go
// Trace context propagation through gRPC metadata
type metadataCarrier struct { md metadata.MD }
func (m *metadataCarrier) Get(key string) string { ... }
func (m *metadataCarrier) Set(key, value string) { ... }
func (m *metadataCarrier) Keys() []string { ... }

// In interceptor:
ctx = otel.GetTextMapPropagator().Extract(ctx, &metadataCarrier{md: incomingMD})
```

Instrumentez HTTP et gRPC avec des middlewares/intercepteurs. Exportez vers Jaeger, Tempo ou tout collecteur OTLP.

### Golden Signals {#golden-signals}

| Signal | Ce qu'il mesure | Exemple de métrique |
|--------|-----------------|----------------|
| Latence | Durée des requêtes | `histogram_quantile(0.99, ...)` |
| Trafic | Demande (RPS) | `sum(rate(http_requests_total[1m]))` |
| Erreurs | Taux de requêtes échouées | `rate(http_requests_total{status!="200"}[1m])` |
| Saturation | Niveau de « remplissage » du service | CPU, mémoire, profondeur de file d'attente |

### Journalisation structurée {#structured-logging}

Utilisez `slog` (stdlib de Go 1.21) ou `zap`/`zerolog`. Journalisez toujours avec le contexte : identifiant de requête, identifiant utilisateur, identifiant de trace. Format JSON en production, texte en développement.

## Pièges courants {#gotchas}

- `rate()` en PromQL nécessite un compteur (croissant de manière monotone) ; l'utiliser sur une jauge produit des résultats absurdes
- `histogram_quantile` opère sur les buckets d'un histogramme : si les bornes des buckets ne couvrent pas la plage de vos données, les résultats sont inexacts
- `unwrap` en LogQL ne fonctionne que sur des champs numériques analysés : assurez-vous que l'analyse JSON extrait correctement le champ
- La `duration` en TraceQL est au niveau du span ; pour la durée totale d'une trace, utilisez le span racine ou des requêtes au niveau de la trace
- Le SDK OpenTelemetry ajoute un surcoût : ajustez le taux d'échantillonnage pour les services à fort débit

## Voir aussi {#see-also}

- [[microservices]] - intercepteurs gRPC pour l'injection de télémétrie
- [[kafka-messaging-fundamentals]] - surveillance du retard des consommateurs avec des métriques
