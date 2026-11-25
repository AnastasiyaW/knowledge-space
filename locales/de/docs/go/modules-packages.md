---
title: "Module und Pakete"
category: reference
tags: [go, modules, packages, go-mod, versioning, workspace, dependencies, imports]
level: 3
source_sha256: e0320f5be016513855e3cd6b476abd81c74c258960bb5dd134d1880bbb6b0a27
translation: machine
translated_at: '2026-10-24'
---
# Module und Pakete {#modules-and-packages}

Go-Module sind die Einheit der Abhängigkeitsverwaltung, und Pakete sind die Einheit der Code-Organisation. Ein Modul ist eine Sammlung von Paketen mit einer `go.mod`-Datei im Wurzelverzeichnis. Pakete gruppieren zusammengehörigen Code innerhalb eines Verzeichnisses – ein Paket pro Verzeichnis, ein Verzeichnis pro Paket.

## Key Facts {#key-facts}

- Ein Modul wird durch `go.mod` im Wurzelverzeichnis definiert, die den Modulpfad und die Go-Version enthält
- Der Modulpfad ist typischerweise die Repository-URL: `module github.com/user/project`
- Jedes Verzeichnis ist ein Paket; der Paketname entspricht dem Verzeichnisnamen (außer bei `main`)
- Exportierte Bezeichner beginnen mit einem Großbuchstaben: `MyFunc`, `MyType` (nicht exportiert: `myFunc`)
- `go get` lädt Abhängigkeiten herunter und aktualisiert `go.mod`
- `go.sum` enthält kryptografische Hashes zur Sicherstellung der Integrität von Abhängigkeiten – in die VCS committen
- `go mod tidy` entfernt nicht verwendete Abhängigkeiten und ergänzt fehlende
- Der Go-Workspace-Modus (`go.work`) ermöglicht es, mehrere Module gleichzeitig zu entwickeln

## Modulinitialisierung {#module-initialization}

```bash
# Create a new module
mkdir myproject && cd myproject
go mod init github.com/user/myproject

# go.mod contents:
# module github.com/user/myproject
# go 1.22
```

### Aufbau von go.mod {#gomod-structure}

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

## Paketorganisation {#package-organization}

### Verzeichnisstruktur {#directory-structure}

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

### Paketbenennung {#package-naming}

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

### Interne Pakete {#internal-packages}

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

## Abhängigkeitsverwaltung {#dependency-management}

### Abhängigkeiten hinzufügen {#adding-dependencies}

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

### Importieren und verwenden {#import-and-use}

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

### Konvention für die Gruppierung von Imports {#import-grouping-convention}

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

### Umgang mit Namenskonflikten {#handling-name-collisions}

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

## Versionierung {#versioning}

### Semantische Versionierung {#semantic-versioning}

```text
Go modules use semver: vMAJOR.MINOR.PATCH
  v1.2.3
  - MAJOR: breaking changes (different import path for v2+)
  - MINOR: new features, backward compatible
  - PATCH: bug fixes

Pre-v1 (v0.x.y): no stability guarantees
v1+: backward compatibility expected within major version
```

### Upgrades auf Major-Versionen {#major-version-upgrades}

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

### Replace und Exclude {#replace-and-exclude}

```text
// go.mod: use local copy during development
replace github.com/user/other => ../other

// go.mod: use a fork
replace github.com/original/pkg => github.com/myfork/pkg v1.2.3

// go.mod: exclude a broken version
exclude github.com/broken/pkg v1.0.1
```

## Workspace-Modus (Go 1.18+) {#workspace-mode-go-118}

Mehrere Module gleichzeitig entwickeln, ohne `replace`-Direktiven.

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

## Build und Installation {#build-and-install}

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

## Stolperfallen {#gotchas}

- **Zirkuläre Imports sind Kompilierfehler** – importiert Paket A das Paket B und B das Paket A, weigert sich Go zu kompilieren. Umstrukturieren, indem gemeinsame Typen in ein drittes Paket ausgelagert werden, oder Interfaces verwenden, um die Abhängigkeit aufzulösen
- **go.sum muss committet werden** – es ist kein Lockfile (go.mod schon). Es enthält die erwarteten Hashes zur Überprüfung der Abhängigkeiten. Wenn Sie es in `.gitignore` aufnehmen, werden Builds nicht reproduzierbar und anfällig für Supply-Chain-Angriffe
- **Modulpfad muss mit dem Repository übereinstimmen** – wenn Ihre `go.mod` `module github.com/user/project` angibt, der Code aber unter `gitlab.com/user/project` liegt, schlägt `go get` fehl. Der Modulpfad ist der Download-Pfad
- **`replace`-Direktiven werden nicht weitergegeben** – verweist Ihr Modul mit `replace` auf einen lokalen Pfad, sehen Konsumenten Ihres Moduls diese Ersetzung nicht und versuchen, das Original herunterzuladen. `replace` nur während der Entwicklung verwenden und vor der Veröffentlichung entfernen

## Siehe auch {#see-also}

- [[interfaces-composition]] - Organisation von Interfaces über Pakete hinweg
- [[http-servers]] - Paketstruktur für HTTP-Anwendungen
- [Fehlerbehandlung](error-handling.md) - Fehlerkonventionen über Paketgrenzen hinweg
