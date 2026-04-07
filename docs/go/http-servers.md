---
title: HTTP Servers
category: patterns
tags: [go, http, net-http, middleware, routing, context, handlers, rest-api]
---

# HTTP Servers

Go's `net/http` package provides a production-grade HTTP/2 server with TLS support out of the box. The design centers on the `http.Handler` interface and composable middleware, requiring no external framework for most use cases.

## Key Facts

- `http.Handler` interface has one method: `ServeHTTP(http.ResponseWriter, *http.Request)`
- `http.HandlerFunc` is a function type that implements `http.Handler` - functions as handlers
- `http.ServeMux` is the built-in request multiplexer (router), improved significantly in Go 1.22
- Go 1.22 added method matching (`GET /users/{id}`) and path parameters to the default mux
- `http.ResponseWriter` methods must be called in order: `Header()` -> `WriteHeader()` -> `Write()`
- Every request runs in its own goroutine - handlers must be safe for concurrent use
- `context.Context` is carried on `*http.Request` via `req.Context()` and `req.WithContext(ctx)`

## Basic Server

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

## Routing (Go 1.22+)

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

### Before Go 1.22

Without method matching, you had to dispatch manually or use a third-party router:

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

## Middleware

Middleware wraps a handler to add cross-cutting behavior (logging, auth, CORS, etc.).

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

### Middleware Chain Helper

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

## JSON API Patterns

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

### Response Helper

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

## Context in HTTP

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

## HTTP Client

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

## Gotchas

- **WriteHeader can only be called once** - calling `WriteHeader` a second time is silently ignored. If you call `Write()` before `WriteHeader()`, Go implicitly sends 200. This means writing an error message after already starting a 200 response produces a warning in logs and a confusing response to the client
- **Default ServeMux is a global** - `http.HandleFunc` (without a mux) registers on `http.DefaultServeMux`, a package-level global. Any imported package can register handlers on it. Always create your own `http.NewServeMux()` in production
- **http.DefaultClient has no timeout** - `http.Get()` and `http.Post()` use `http.DefaultClient` which has zero timeout. A slow/unresponsive server will block your goroutine forever. Always create a custom client with explicit timeouts
- **Request body must be closed** - failing to call `resp.Body.Close()` leaks the TCP connection. Use `defer resp.Body.Close()` immediately after checking `err`

## See Also

- [[goroutines-channels]] - each HTTP request runs in its own goroutine
- [[interfaces-composition]] - `http.Handler` interface and middleware pattern
- [[error-handling]] - error handling in HTTP handlers and clients
- [[modules-packages]] - organizing HTTP handlers across packages
