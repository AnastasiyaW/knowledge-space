---
title: Modules and Packages
category: reference
tags: [go, modules, packages, go-mod, versioning, workspace, dependencies, imports]
---

# Modules and Packages

Go modules are the unit of dependency management, and packages are the unit of code organization. A module is a collection of packages with a `go.mod` file at the root. Packages group related code within a directory - one package per directory, one directory per package.

## Key Facts

- A module is defined by `go.mod` in the root directory, containing the module path and Go version
- Module path is typically the repository URL: `module github.com/user/project`
- Each directory is one package, package name matches directory name (except `main`)
- Exported identifiers start with uppercase: `MyFunc`, `MyType` (unexported: `myFunc`)
- `go get` downloads dependencies and updates `go.mod`
- `go.sum` contains cryptographic hashes for dependency integrity - commit to VCS
- `go mod tidy` removes unused dependencies and adds missing ones
- Go workspace mode (`go.work`) lets you develop multiple modules simultaneously

## Module Initialization

```bash
# Create a new module
mkdir myproject && cd myproject
go mod init github.com/user/myproject

# go.mod contents:
# module github.com/user/myproject
# go 1.22
```

### go.mod Structure

```text
module github.com/user/myproject

go 1.22

require (
    github.com/shopspring/decimal v1.3.1
    golang.org/x/sync v0.6.0
)

require (
    // indirect dependencies (used by your dependencies)
    golang.org/x/text v0.14.0 // indirect
)
```

## Package Organization

### Directory Structure

```text
myproject/
  go.mod
  main.go            # package main - entry point
  internal/           # private packages, cannot be imported from outside module
    config/
      config.go       # package config
    database/
      database.go     # package database
  pkg/                # optional, public reusable packages
    auth/
      auth.go         # package auth
  handler/
    user.go           # package handler
    order.go          # package handler (same directory = same package)
```

### Package Naming

```go
// Package name = directory name, used as import qualifier
import "github.com/user/myproject/handler"

// Usage: handler.CreateUser, handler.GetOrder
// Good: package name is a noun, functions are verbs
```

```text
Naming conventions:
  - Package names: short, lowercase, no underscores (names, extract, auth)
  - Don't repeat package name in exports: names.Extract, NOT names.ExtractNames
  - Don't use generic names: util, common, helpers (what does util.Process do?)
  - One exception: when identifier IS the package: sort.Sort, context.Context
```

### Internal Packages

```text
Packages under internal/ are only importable by code in the parent directory:

myproject/
  internal/
    secret/         # only importable by myproject/* code
      secret.go
  cmd/
    server/
      internal/     # only importable by cmd/server/* code
        config.go
```

## Dependency Management

### Adding Dependencies

```bash
# Add a specific dependency
go get github.com/shopspring/decimal@v1.3.1

# Add latest version
go get github.com/shopspring/decimal@latest

# Update all dependencies
go get -u ./...

# Remove unused, add missing
go mod tidy
```

### Import and Use

```go
package main

import (
    "fmt"                                    // standard library
    "github.com/shopspring/decimal"         // third-party
    "github.com/user/myproject/internal/db" // internal package
)

func main() {
    price := decimal.NewFromFloat(19.99)
    fmt.Println(price)
}
```

### Import Grouping Convention

```go
import (
    // Standard library
    "context"
    "fmt"
    "net/http"

    // Third-party
    "github.com/gorilla/mux"
    "go.uber.org/zap"

    // Internal/project packages
    "github.com/user/myproject/handler"
    "github.com/user/myproject/model"
)
```

### Handling Name Collisions

```go
import (
    crand "crypto/rand"  // renamed to avoid collision
    "math/rand"
)

func main() {
    // Use crand for crypto, rand for math
    seed, _ := crand.Int(crand.Reader, big.NewInt(1000))
    r := rand.New(rand.NewSource(seed.Int64()))
}
```

## Versioning

### Semantic Versioning

```text
Go modules use semver: vMAJOR.MINOR.PATCH
  v1.2.3
  - MAJOR: breaking changes (different import path for v2+)
  - MINOR: new features, backward compatible
  - PATCH: bug fixes

Pre-v1 (v0.x.y): no stability guarantees
v1+: backward compatibility expected within major version
```

### Major Version Upgrades

```go
// v1 import
import "github.com/user/module"

// v2+ requires version suffix in import path
import "github.com/user/module/v2"

// Both can coexist in the same project
import (
    v1 "github.com/user/module"
    "github.com/user/module/v2"
)
```

### Replace and Exclude

```text
// go.mod: use local copy during development
replace github.com/user/other => ../other

// go.mod: use a fork
replace github.com/original/pkg => github.com/myfork/pkg v1.2.3

// go.mod: exclude a broken version
exclude github.com/broken/pkg v1.0.1
```

## Workspace Mode (Go 1.18+)

Develop multiple modules simultaneously without `replace` directives.

```bash
# Create a workspace
go work init ./module-a ./module-b

# go.work file:
# go 1.22
# use (
#     ./module-a
#     ./module-b
# )
```

```text
Workspace benefits:
  - Edit module-a and module-b, changes visible to each other immediately
  - No need for replace directives in go.mod
  - go.work should NOT be committed to VCS (local development only)
  - go.work.sum tracks hashes (also local only)
```

## Build and Install

```bash
# Build current module
go build ./...

# Install a binary (goes to $GOPATH/bin or $GOBIN)
go install ./cmd/server

# Install a third-party tool
go install github.com/rakyll/hey@latest

# Cross-compile
GOOS=linux GOARCH=amd64 go build -o server-linux ./cmd/server
GOOS=windows GOARCH=amd64 go build -o server.exe ./cmd/server
```

## Gotchas

- **Circular imports are compile errors** - if package A imports B and B imports A, Go refuses to compile. Restructure by extracting shared types into a third package, or use interfaces to break the dependency
- **go.sum must be committed** - it's not a lockfile (go.mod is). It contains expected hashes for dependency verification. If you .gitignore it, builds become non-reproducible and vulnerable to supply chain attacks
- **Module path must match repository** - if your `go.mod` says `module github.com/user/project` but the code lives at `gitlab.com/user/project`, `go get` will fail. The module path IS the download path
- **`replace` directives don't propagate** - if your module uses `replace` to point to a local path, consumers of your module won't see that replace. They'll try to download the original. Use `replace` only during development, remove before publishing

## See Also

- [[interfaces-composition]] - organizing interfaces across packages
- [[http-servers]] - package structure for HTTP applications
- [[error-handling]] - error conventions across package boundaries
