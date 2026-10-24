---
title: "Microservices Go - gRPC, architecture et tests"
category: concepts
tags: [go, golang, grpc, protobuf, clean-architecture, microservices, testing]
level: 3
source_sha256: 0e8a086fbde9a42e73be1b83ac120a995d0001986034bf52ec56c6d188fe9d13
translation: machine
translated_at: '2026-10-24'
---
# Microservices Go - gRPC, architecture et tests {#go-microservices-grpc-architecture-and-testing}

Patrons de microservices Go en production : gRPC avec protobuf, couches de clean architecture, injection de dépendances, tests avec mocks, et déploiement Docker/Kubernetes.

## Points clés {#key-facts}

- La chaîne d'outils buf remplace protoc manuel : lint, détection des changements incompatibles, génération de code multi-plugins
- gRPC Gateway expose le même service proto en gRPC (50051) et en REST/JSON (8081) via un reverse proxy
- Clean architecture : trois niveaux de modèles (proto, domaine, repository) avec des convertisseurs aux frontières
- Définir les interfaces de repository dans la couche consommatrice (service), et non dans la couche d'implémentation
- `protoc-gen-validate` valide les champs des fichiers .proto via des intercepteurs gRPC
- Les workspaces Go (`go.work`) permettent le développement inter-modules sans publication

## Patrons {#patterns}

### Conception de services gRPC {#grpc-service-design}

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

**Chaîne d'intercepteurs** :
```go
server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        loggingInterceptor,
        recoveryInterceptor,
        validationInterceptor,
    ),
)
```

**Champs nullables** : utiliser `google.protobuf.wrappers` (StringValue, BoolValue, Int32Value) pour les champs qui doivent distinguer l'absence de la valeur zéro.

**Mises à jour partielles** :
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

### Couches de clean architecture {#clean-architecture-layers}

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

**Sens des dépendances** : api -> service -> repository (les dépendances pointent vers l'intérieur).

**Trois niveaux de modèles** :
- **Modèles proto** : contrat d'API versionné, code généré
- **Modèles domaine** : entités métier stables, indépendantes des préoccupations externes
- **Modèles repository** : optimisés pour la représentation en base (tags DB, types nullables)

Les convertisseurs à chaque frontière permettent à chaque couche d'évoluer indépendamment.

### Injection de dépendances {#dependency-injection}

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

Pour les graphes complexes : `wire` (Google) ou `dig` (Uber). L'injection manuelle dans `app/di.go` est souvent la plus claire.

### Tests {#testing}

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

`mockery` génère des mocks à partir des définitions d'interfaces. Tester les couches API et service avec des mocks ; la couche repository avec des tests d'intégration (testcontainers).

### Build Docker multi-étapes {#docker-multi-stage-build}

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

**Cache des couches** : copier `go.mod`/`go.sum` en premier pour mettre en cache le téléchargement des modules.

### Monorepo Go avec workspaces {#go-monorepo-with-workspaces}

```bash
go work init
go work use ./service-a ./service-b ./shared
```

`go.work` permet le développement inter-modules sans publication. `buf.work.yaml` sert aux fichiers proto partagés.

### Pile standard pour microservices {#microservice-standard-stack}

- **HTTP** : `net/http` (routage Go 1.22+), chi, ou ogen (génération de code depuis OpenAPI)
- **gRPC** : google.golang.org/grpc + protobuf + buf
- **DB PostgreSQL** : pgx, générateur SQL goqu, migrations goose
- **DB MongoDB** : mongo-driver officiel, bson
- **Kafka** : segmentio/kafka-go ou confluent-kafka-go
- **Redis** : go-redis
- **Mocking** : mockery (à partir des interfaces)
- **Tests** : testify, testify/suite
- **Linting** : golangci-lint
- **Build** : Taskfile.yml ou Makefile

## Pièges {#gotchas}

- gRPC utilise le multiplexage HTTP/2 - les load balancers au niveau connexion sont insuffisants ; utiliser un LB côté client ou un service mesh
- `protoc-gen-validate` renvoie le code de statut gRPC 3 (INVALID_ARGUMENT) en cas d'échec de validation
- `depends_on` de Docker avec `condition: service_healthy` attend le healthcheck, et pas seulement le démarrage du conteneur
- `go test -coverprofile=coverage.out ./...` puis `go tool cover -html=coverage.out` pour la visualisation
- Patron de soft delete : champ `deleted_at *time.Time`, filtrer avec `WHERE deleted_at IS NULL`

## Voir aussi {#see-also}

- [[go/fundamentals]] - types, slices, maps, interfaces
- [Concurrence en Go - goroutines, canaux et sync](concurrency-patterns.md) - goroutines, canaux, sync
- [[database-patterns]] - PostgreSQL, MongoDB, Redis, outbox transactionnel
- [[observability-query-languages]] - PromQL, LogQL, TraceQL pour la supervision des services Go
- [[kafka-messaging-fundamentals]] - sémantiques de livraison, groupes de consommateurs
