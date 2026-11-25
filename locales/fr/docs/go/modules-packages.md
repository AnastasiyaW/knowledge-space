---
title: "Modules et packages"
category: reference
tags: [go, modules, packages, go-mod, versioning, workspace, dependencies, imports]
level: 3
source_sha256: e0320f5be016513855e3cd6b476abd81c74c258960bb5dd134d1880bbb6b0a27
translation: machine
translated_at: '2026-10-24'
---
# Modules et packages {#modules-and-packages}

Les modules Go sont l'unité de gestion des dépendances, et les packages sont l'unité d'organisation du code. Un module est une collection de packages dont la racine contient un fichier `go.mod`. Les packages regroupent du code lié au sein d'un répertoire : un package par répertoire, un répertoire par package.

## Points clés {#key-facts}

- Un module est défini par `go.mod` à la racine, qui contient le chemin du module et la version de Go
- Le chemin du module correspond généralement à l'URL du dépôt : `module github.com/user/project`
- Chaque répertoire constitue un package, et le nom du package correspond au nom du répertoire (sauf `main`)
- Les identifiants exportés commencent par une majuscule : `MyFunc`, `MyType` (non exportés : `myFunc`)
- `go get` télécharge les dépendances et met à jour `go.mod`
- `go.sum` contient les empreintes cryptographiques garantissant l'intégrité des dépendances : à versionner dans le VCS
- `go mod tidy` supprime les dépendances inutilisées et ajoute celles qui manquent
- Le mode workspace de Go (`go.work`) permet de développer plusieurs modules simultanément

## Initialisation du module {#module-initialization}

```bash
# Create a new module
mkdir myproject && cd myproject
go mod init github.com/user/myproject

# go.mod contents:
# module github.com/user/myproject
# go 1.22
```

### Structure de go.mod {#gomod-structure}

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

## Organisation des packages {#package-organization}

### Structure des répertoires {#directory-structure}

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

### Nommage des packages {#package-naming}

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

### Packages internes {#internal-packages}

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

## Gestion des dépendances {#dependency-management}

### Ajout de dépendances {#adding-dependencies}

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

### Import et utilisation {#import-and-use}

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

### Convention de regroupement des imports {#import-grouping-convention}

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

### Gestion des collisions de noms {#handling-name-collisions}

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

## Versionnement {#versioning}

### Versionnement sémantique {#semantic-versioning}

```text
Go modules use semver: vMAJOR.MINOR.PATCH
  v1.2.3
  - MAJOR: breaking changes (different import path for v2+)
  - MINOR: new features, backward compatible
  - PATCH: bug fixes

Pre-v1 (v0.x.y): no stability guarantees
v1+: backward compatibility expected within major version
```

### Mises à niveau de version majeure {#major-version-upgrades}

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

### Replace et Exclude {#replace-and-exclude}

```text
// go.mod: use local copy during development
replace github.com/user/other => ../other

// go.mod: use a fork
replace github.com/original/pkg => github.com/myfork/pkg v1.2.3

// go.mod: exclude a broken version
exclude github.com/broken/pkg v1.0.1
```

## Mode workspace (Go 1.18+) {#workspace-mode-go-118}

Développez plusieurs modules simultanément sans directives `replace`.

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

## Compilation et installation {#build-and-install}

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

## Pièges courants {#gotchas}

- **Les imports circulaires sont des erreurs de compilation** : si le package A importe B et que B importe A, Go refuse de compiler. Restructurez le code en extrayant les types partagés dans un troisième package, ou utilisez des interfaces pour rompre la dépendance
- **go.sum doit être versionné** : ce n'est pas un fichier de verrouillage (c'est go.mod qui joue ce rôle). Il contient les empreintes attendues pour la vérification des dépendances. Si vous l'ajoutez à `.gitignore`, les builds deviennent non reproductibles et vulnérables aux attaques de la chaîne d'approvisionnement
- **Le chemin du module doit correspondre au dépôt** : si votre `go.mod` indique `module github.com/user/project` alors que le code se trouve à `gitlab.com/user/project`, `go get` échouera. Le chemin du module EST le chemin de téléchargement
- **Les directives `replace` ne se propagent pas** : si votre module utilise `replace` pour pointer vers un chemin local, les consommateurs de votre module ne verront pas ce remplacement et tenteront de télécharger la version d'origine. Utilisez `replace` uniquement pendant le développement, et supprimez-le avant la publication

## Voir aussi {#see-also}

- [[interfaces-composition]] - organisation des interfaces entre packages
- [[http-servers]] - structure des packages pour les applications HTTP
- [Gestion des erreurs](error-handling.md) - conventions d'erreurs aux frontières des packages
