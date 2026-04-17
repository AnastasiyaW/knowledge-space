---
title: Go Microservices - gRPC, Architecture, and Testing
category: concepts
tags: [misc, go, golang, grpc, protobuf, clean-architecture, microservices, testing]
---

# Go Microservices - gRPC, Architecture, and Testing

Production Go microservice patterns - gRPC with protobuf, clean architecture layers, dependency injection, testing with mocks, and Docker/Kubernetes deployment.

## Key Facts

- buf toolchain replaces manual protoc: lint, breaking change detection, multi-plugin code generation
- gRPC Gateway exposes same proto service as both gRPC (50051) and REST/JSON (8081) via reverse proxy
- Clean architecture: three model levels (proto, domain, repository) with converters at boundaries
- Define repository interfaces in the consuming layer (service), not the implementation layer
- `protoc-gen-validate` validates fields in .proto files via gRPC interceptors
- Go workspaces (`go.work`) enable cross-module development without publishing

## Patterns

### gRPC Service Design

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

**Interceptor chain**:
```go
server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        loggingInterceptor,
        recoveryInterceptor,
        validationInterceptor,
    ),
)
```

**Nullable fields**: use `google.protobuf.wrappers` (StringValue, BoolValue, Int32Value) for fields that must distinguish absent vs zero.

**Partial updates**:
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

### Clean Architecture Layers

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

**Dependency direction**: api -> service -> repository (dependencies point inward).

**Three model levels**:
- **Proto models**: versioned API contract, generated code
- **Domain models**: stable business entities, independent of external concerns
- **Repository models**: optimized for DB representation (DB tags, nullable types)

Converters at each boundary allow each layer to change independently.

### Dependency Injection

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

For complex graphs: `wire` (Google) or `dig` (Uber). Manual DI in `app/di.go` is often clearest.

### Testing

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

`mockery` generates mocks from interface definitions. Test API and service layers with mocks; repository layer with integration tests (testcontainers).

### Docker Multi-Stage Build

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

**Layer caching**: copy `go.mod`/`go.sum` first for module download caching.

### Go Monorepo with Workspaces

```bash
go work init
go work use ./service-a ./service-b ./shared
```

`go.work` enables cross-module development without publishing. `buf.work.yaml` for shared proto files.

### Microservice Standard Stack

- **HTTP**: `net/http` (Go 1.22+ routing), chi, or ogen (code-gen from OpenAPI)
- **gRPC**: google.golang.org/grpc + protobuf + buf
- **DB PostgreSQL**: pgx, goqu SQL builder, goose migrations
- **DB MongoDB**: official mongo-driver, bson
- **Kafka**: segmentio/kafka-go or confluent-kafka-go
- **Redis**: go-redis
- **Mocking**: mockery (from interfaces)
- **Testing**: testify, testify/suite
- **Linting**: golangci-lint
- **Build**: Taskfile.yml or Makefile

## Gotchas

- gRPC uses HTTP/2 multiplexing - connection-level load balancers are insufficient; use client-side LB or service mesh
- `protoc-gen-validate` returns gRPC status code 3 (INVALID_ARGUMENT) for validation failures
- Docker `depends_on` with `condition: service_healthy` waits for healthcheck, not just container start
- `go test -coverprofile=coverage.out ./...` then `go tool cover -html=coverage.out` for visualization
- Soft delete pattern: `deleted_at *time.Time` field, filter `WHERE deleted_at IS NULL`

## See Also

- [[go/fundamentals]] - types, slices, maps, interfaces
- [[go/concurrency-patterns]] - goroutines, channels, sync
- [[database-patterns]] - PostgreSQL, MongoDB, Redis, transactional outbox
- [[observability-query-languages]] - PromQL, LogQL, TraceQL for monitoring Go services
- [[kafka-messaging-fundamentals]] - delivery semantics, consumer groups
