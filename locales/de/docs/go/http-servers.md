---
title: "HTTP-Server"
category: patterns
tags: [go, http, net-http, middleware, routing, context, handlers, rest-api]
level: 3
source_sha256: 962f6dad7313dd53332bfb7cef0646495cff5f521cd867cb1db115be788a0f78
translation: machine
translated_at: '2026-10-24'
---
# HTTP-Server {#http-servers}

Das `net/http`-Paket von Go bietet einen produktionstauglichen HTTP/2-Server mit TLS-Unterstützung von Haus aus. Das Design basiert auf dem `http.Handler`-Interface und kombinierbarer Middleware; für die meisten Anwendungsfälle ist kein externes Framework nötig.

## Wichtige Fakten {#key-facts}

- Das `http.Handler`-Interface hat genau eine Methode: `ServeHTTP(http.ResponseWriter, *http.Request)`
- `http.HandlerFunc` ist ein Funktionstyp, der `http.Handler` implementiert – Funktionen als Handler
- `http.ServeMux` ist der eingebaute Request-Multiplexer (Router), der in Go 1.22 deutlich verbessert wurde
- Go 1.22 ergänzt den Standard-Mux um Methodenabgleich (`GET /users/{id}`) und Pfadparameter
- Methoden von `http.ResponseWriter` müssen in fester Reihenfolge aufgerufen werden: `Header()` -> `WriteHeader()` -> `Write()`
- Jeder Request läuft in einer eigenen Goroutine – Handler müssen für die nebenläufige Nutzung sicher sein
- `context.Context` wird über `req.Context()` und `req.WithContext(ctx)` an `*http.Request` übergeben

## Einfacher Server {#basic-server}

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

## Routing (Go 1.22+) {#routing-go-122}

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

### Vor Go 1.22 {#before-go-122}

Ohne Methodenabgleich musste man manuell verzweigen oder einen Drittanbieter-Router verwenden:

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

## Middleware {#middleware}

Middleware umschließt einen Handler, um querschnittliches Verhalten hinzuzufügen (Logging, Authentifizierung, CORS usw.).

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

### Hilfsfunktion für Middleware-Ketten {#middleware-chain-helper}

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

## JSON-API-Muster {#json-api-patterns}

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

### Hilfsfunktion für Antworten {#response-helper}

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

## Context in HTTP {#context-in-http}

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

## HTTP-Client {#http-client}

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

## Fallstricke {#gotchas}

- **`WriteHeader` darf nur einmal aufgerufen werden** – ein zweiter Aufruf von `WriteHeader` wird stillschweigend ignoriert. Ruft man `Write()` vor `WriteHeader()` auf, sendet Go implizit den Status 200. Wird also nach dem Start einer 200-Antwort noch eine Fehlermeldung geschrieben, erscheint eine Warnung im Log und der Client erhält eine verwirrende Antwort
- **Der Standard-ServeMux ist global** – `http.HandleFunc` (ohne eigenen Mux) registriert auf `http.DefaultServeMux`, einer globalen Variable auf Paketebene. Jedes importierte Paket kann dort Handler registrieren. In produktivem Code immer eigenes `http.NewServeMux()` erzeugen
- **`http.DefaultClient` hat kein Timeout** – `http.Get()` und `http.Post()` verwenden `http.DefaultClient`, der keinen Timeout besitzt. Ein langsamer oder nicht antwortender Server blockiert die Goroutine dauerhaft. Immer einen eigenen Client mit expliziten Timeouts anlegen
- **Der Request-Body muss geschlossen werden** – unterbleibt der Aufruf von `resp.Body.Close()`, leckt die TCP-Verbindung. Unmittelbar nach der Prüfung von `err` `defer resp.Body.Close()` verwenden

## Siehe auch {#see-also}

- [[goroutines-channels]] – jeder HTTP-Request läuft in einer eigenen Goroutine
- [[interfaces-composition]] – `http.Handler`-Interface und Middleware-Muster
- [Fehlerbehandlung](error-handling.md) – Fehlerbehandlung in HTTP-Handlern und Clients
- [[modules-packages]] – Organisation von HTTP-Handlern über Pakete hinweg
