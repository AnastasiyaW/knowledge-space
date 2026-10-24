---
title: "Go-Microservices - gRPC, Architektur und Testing"
category: concepts
tags: [go, golang, grpc, protobuf, clean-architecture, microservices, testing]
level: 3
source_sha256: 0e8a086fbde9a42e73be1b83ac120a995d0001986034bf52ec56c6d188fe9d13
translation: machine
translated_at: '2026-10-24'
---
# Go-Microservices - gRPC, Architektur und Testing {#go-microservices-grpc-architecture-and-testing}

Produktionsreife Muster für Go-Microservices: gRPC mit protobuf, Schichten der Clean Architecture, Dependency Injection, Tests mit Mocks sowie Deployment mit Docker und Kubernetes.

## Kernfakten {#key-facts}

- Die buf-Toolchain ersetzt manuelles protoc: Linting, Erkennung von Breaking Changes, Code-Generierung mit mehreren Plugins
- gRPC Gateway stellt denselben Proto-Service sowohl als gRPC (50051) als auch als REST/JSON (8081) über einen Reverse Proxy bereit
- Clean Architecture: drei Modellebenen (Proto, Domain, Repository) mit Konvertern an den Grenzen
- Repository-Interfaces in der konsumierenden Schicht (Service) definieren, nicht in der Implementierungsschicht
- `protoc-gen-validate` validiert Felder in .proto-Dateien über gRPC-Interceptoren
- Go-Workspaces (`go.work`) ermöglichen modulübergreifende Entwicklung ohne Veröffentlichung

## Muster {#patterns}

### gRPC-Service-Design {#grpc-service-design}

```yaml
# buf.gen.yaml - code generation config
plugins:
  - plugin: go
    out: pkg/proto
  - plugin: go-grpc
    out: pkg/proto
  - plugin: grpc-gateway
    out: pkg/proto
  - plugin: validate
    out: pkg/proto
```

**Interceptor-Kette**:
```go
server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        loggingInterceptor,
        recoveryInterceptor,
        validationInterceptor,
    ),
)
```

**Nullable Felder**: `google.protobuf.wrappers` verwenden (StringValue, BoolValue, Int32Value) für Felder, die zwischen fehlend und Nullwert unterscheiden müssen.

**Partielle Updates**:
```proto
message UpdateRequest {
  string uuid = 1;
  UpdateInfo update_info = 2;
}
message UpdateInfo {
  google.protobuf.StringValue description = 1;
  google.protobuf.StringValue color = 2;
}
```

### Schichten der Clean Architecture {#clean-architecture-layers}

```go
cmd/main.go              - entry point
internal/
  api/                   - controllers (HTTP/gRPC handlers)
  service/               - use cases, business logic
    interfaces.go        - repository interfaces defined here
  repository/            - data access implementations
    model/               - DB-specific models
    converter/           - domain <-> repo model conversion
  model/                 - domain entities
  converter/             - proto/API <-> domain model conversion
```

**Abhängigkeitsrichtung**: api -> service -> repository (Abhängigkeiten zeigen nach innen).

**Drei Modellebenen**:
- **Proto-Modelle**: versionierter API-Vertrag, generierter Code
- **Domain-Modelle**: stabile Geschäftsentitäten, unabhängig von externen Belangen
- **Repository-Modelle**: optimiert für die Datenbankrepräsentation (DB-Tags, nullable Typen)

Konverter an jeder Grenze erlauben es, dass sich jede Schicht unabhängig voneinander ändern kann.

### Dependency Injection {#dependency-injection}

```go
// service/interfaces.go
type UserRepository interface {
    Get(ctx context.Context, id uuid.UUID) (*model.User, error)
    Create(ctx context.Context, user *model.User) (uuid.UUID, error)
}

type UserService struct {
    repo UserRepository // depends on interface, not implementation
}
```

Für komplexe Abhängigkeitsgraphen: `wire` (Google) oder `dig` (Uber). Manuelle DI in `app/di.go` ist oft am übersichtlichsten.

### Testing {#testing}

```go
// Table-driven tests
tests := []struct{ name string; input int; want int }{
    {"zero", 0, 0},
    {"positive", 5, 25},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        assert.Equal(t, tt.want, square(tt.input))
    })
}

// Benchmarks (Go 1.24+)
func BenchmarkMyFunc(b *testing.B) {
    for b.Loop() {
        myFunc()
    }
}
```

`mockery` generiert Mocks aus Interface-Definitionen. API- und Service-Schicht mit Mocks testen; die Repository-Schicht mit Integrationstests (testcontainers).

### Docker Multi-Stage Build {#docker-multi-stage-build}

```dockerfile
FROM golang:1.24 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app ./cmd/main.go

FROM alpine:3.21
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/app .
USER appuser
CMD ["./app"]
```

**Layer-Caching**: `go.mod`/`go.sum` zuerst kopieren, damit der Modul-Download gecacht werden kann.

### Go-Monorepo mit Workspaces {#go-monorepo-with-workspaces}

```bash
go work init
go work use ./service-a ./service-b ./shared
```

`go.work` ermöglicht modulübergreifende Entwicklung ohne Veröffentlichung. `buf.work.yaml` für gemeinsam genutzte Proto-Dateien.

### Standard-Stack für Microservices {#microservice-standard-stack}

- **HTTP**: `net/http` (Routing ab Go 1.22), chi oder ogen (Code-Generierung aus OpenAPI)
- **gRPC**: google.golang.org/grpc + protobuf + buf
- **DB PostgreSQL**: pgx, goqu SQL-Builder, goose-Migrationen
- **DB MongoDB**: offizieller mongo-driver, bson
- **Kafka**: segmentio/kafka-go oder confluent-kafka-go
- **Redis**: go-redis
- **Mocking**: mockery (aus Interfaces)
- **Testing**: testify, testify/suite
- **Linting**: golangci-lint
- **Build**: Taskfile.yml oder Makefile

## Stolperfallen {#gotchas}

- gRPC nutzt HTTP/2-Multiplexing - Load Balancer auf Verbindungsebene reichen nicht aus; client-seitiges LB oder ein Service Mesh verwenden
- `protoc-gen-validate` liefert für Validierungsfehler den gRPC-Statuscode 3 (INVALID_ARGUMENT)
- Docker `depends_on` mit `condition: service_healthy` wartet auf den Healthcheck, nicht nur auf den Start des Containers
- `go test -coverprofile=coverage.out ./...` und anschließend `go tool cover -html=coverage.out` zur Visualisierung
- Soft-Delete-Muster: Feld `deleted_at *time.Time`, Filter `WHERE deleted_at IS NULL`

## Siehe auch {#see-also}

- [[go/fundamentals]] - Typen, Slices, Maps, Interfaces
- [Go-Concurrency - Goroutinen, Channels und Sync](concurrency-patterns.md) - Goroutinen, Channels, Sync
- [[database-patterns]] - PostgreSQL, MongoDB, Redis, transactional outbox
- [[observability-query-languages]] - PromQL, LogQL, TraceQL für das Monitoring von Go-Services
- [[kafka-messaging-fundamentals]] - Zustellungssemantik, Consumer Groups
