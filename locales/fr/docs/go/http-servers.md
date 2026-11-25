---
title: "Serveurs HTTP"
category: patterns
tags: [go, http, net-http, middleware, routing, context, handlers, rest-api]
level: 3
source_sha256: 962f6dad7313dd53332bfb7cef0646495cff5f521cd867cb1db115be788a0f78
translation: machine
translated_at: '2026-10-24'
---
# Serveurs HTTP {#http-servers}

Le package `net/http` de Go fournit un serveur HTTP/2 de qualité production avec prise en charge de TLS dès l'installation. La conception repose sur l'interface `http.Handler` et sur des middlewares composables, ce qui évite de recourir à un framework externe pour la plupart des cas d'usage.

## Points clés {#key-facts}

- L'interface `http.Handler` ne comporte qu'une seule méthode : `ServeHTTP(http.ResponseWriter, *http.Request)`
- `http.HandlerFunc` est un type de fonction qui implémente `http.Handler` - les fonctions peuvent servir de handlers
- `http.ServeMux` est le multiplexeur de requêtes (routeur) intégré, considérablement amélioré dans Go 1.22
- Go 1.22 a ajouté la correspondance par méthode (`GET /users/{id}`) et les paramètres de chemin au mux par défaut
- Les méthodes de `http.ResponseWriter` doivent être appelées dans l'ordre : `Header()` -> `WriteHeader()` -> `Write()`
- Chaque requête s'exécute dans sa propre goroutine - les handlers doivent être sûrs pour un usage concurrent
- `context.Context` est transporté sur `*http.Request` via `req.Context()` et `req.WithContext(ctx)`

## Serveur de base {#basic-server}

```go
package main

import (
    "fmt"
    "log"
    "net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /hello/{name}", func(w http.ResponseWriter, r *http.Request) {
        name := r.PathValue("name") // Go 1.22+ path parameter
        fmt.Fprintf(w, "Hello, %s!", name)
    })

    server := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 30 * time.Second,
        IdleTimeout:  120 * time.Second,
    }
    log.Fatal(server.ListenAndServe())
}
```

## Routage (Go 1.22+) {#routing-go-122}

```go
mux := http.NewServeMux()

// Method + path matching
mux.HandleFunc("GET /users", listUsers)
mux.HandleFunc("POST /users", createUser)
mux.HandleFunc("GET /users/{id}", getUser)
mux.HandleFunc("PUT /users/{id}", updateUser)
mux.HandleFunc("DELETE /users/{id}", deleteUser)

// Wildcard - matches remaining path
mux.HandleFunc("GET /files/{path...}", serveFile)

// Extract path parameters
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
}
```

### Avant Go 1.22 {#before-go-122}

Sans correspondance par méthode, il fallait répartir les requêtes manuellement ou utiliser un routeur tiers :

```go
// Manual method dispatch (pre-1.22 pattern)
mux.HandleFunc("/users/", func(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        getUser(w, r)
    case http.MethodPut:
        updateUser(w, r)
    default:
        http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
    }
})
```

## Middlewares {#middleware}

Un middleware encapsule un handler pour ajouter un comportement transversal (journalisation, authentification, CORS, etc.).

```go
// Middleware signature: takes Handler, returns Handler
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return
        }
        // Validate token, add user to context
        ctx := context.WithValue(r.Context(), userKey, user)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Chain middleware
handler := loggingMiddleware(authMiddleware(mux))
server := &http.Server{Handler: handler}
```

### Utilitaire de chaînage de middlewares {#middleware-chain-helper}

```go
type Middleware func(http.Handler) http.Handler

func chain(h http.Handler, middlewares ...Middleware) http.Handler {
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}

// Usage: request flows through logging -> auth -> recovery -> handler
handler := chain(mux, loggingMiddleware, authMiddleware, recoveryMiddleware)
```

## Patterns pour API JSON {#json-api-patterns}

```go
func createUser(w http.ResponseWriter, r *http.Request) {
    // Decode request body
    var input struct {
        Name  string `json:"name"`
        Email string `json:"email"`
    }
    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, "invalid JSON", http.StatusBadRequest)
        return
    }

    user, err := db.CreateUser(r.Context(), input.Name, input.Email)
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    // Encode response
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```

### Utilitaire de réponse {#response-helper}

```go
func writeJSON(w http.ResponseWriter, status int, data any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(data); err != nil {
        log.Printf("failed to encode response: %v", err)
    }
}

func writeError(w http.ResponseWriter, status int, msg string) {
    writeJSON(w, status, map[string]string{"error": msg})
}
```

## Contexte dans HTTP {#context-in-http}

```go
// Extract context from request
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // Pass context to downstream calls (DB, external APIs)
    result, err := db.Query(ctx, "SELECT ...")
    if err != nil {
        // If context was cancelled (client disconnected), ctx.Err() != nil
        if ctx.Err() != nil {
            return // client gone, no point responding
        }
        http.Error(w, "db error", 500)
        return
    }
}

// Add values to context in middleware
type contextKey string

const userKey contextKey = "user"

func getUserFromContext(ctx context.Context) (*User, bool) {
    user, ok := ctx.Value(userKey).(*User)
    return user, ok
}
```

## Client HTTP {#http-client}

```go
// Always create a client with timeouts - never use http.DefaultClient
client := &http.Client{
    Timeout: 10 * time.Second,
}

resp, err := client.Get("https://api.example.com/data")
if err != nil {
    return fmt.Errorf("request failed: %w", err)
}
defer resp.Body.Close()

if resp.StatusCode != http.StatusOK {
    return fmt.Errorf("unexpected status: %s", resp.Status)
}

var data MyResponse
if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
    return fmt.Errorf("decode response: %w", err)
}
```

## Pièges {#gotchas}

- **WriteHeader ne peut être appelé qu'une seule fois** - un second appel à `WriteHeader` est silencieusement ignoré. Si `Write()` est appelé avant `WriteHeader()`, Go envoie implicitement un 200. Cela signifie qu'écrire un message d'erreur après le démarrage d'une réponse 200 produit un avertissement dans les logs et une réponse déroutante pour le client
- **Le ServeMux par défaut est global** - `http.HandleFunc` (sans mux explicite) enregistre sur `http.DefaultServeMux`, une variable globale au niveau du package. N'importe quel package importé peut y enregistrer des handlers. Créez toujours votre propre `http.NewServeMux()` en production
- **http.DefaultClient n'a pas de timeout** - `http.Get()` et `http.Post()` utilisent `http.DefaultClient`, dont le timeout est nul. Un serveur lent ou non réactif bloquera votre goroutine indéfiniment. Créez toujours un client personnalisé avec des timeouts explicites
- **Le corps de la requête doit être fermé** - ne pas appeler `resp.Body.Close()` provoque une fuite de la connexion TCP. Utilisez `defer resp.Body.Close()` immédiatement après avoir vérifié `err`

## Voir aussi {#see-also}

- [[goroutines-channels]] - chaque requête HTTP s'exécute dans sa propre goroutine
- [[interfaces-composition]] - l'interface `http.Handler` et le pattern middleware
- [Gestion des erreurs](error-handling.md) - gestion des erreurs dans les handlers et clients HTTP
- [[modules-packages]] - organisation des handlers HTTP entre packages
