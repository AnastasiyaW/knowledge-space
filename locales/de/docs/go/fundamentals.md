---
title: "Go-Sprachgrundlagen"
category: concepts
tags: [go, golang, types, slices, maps, interfaces, pointers]
level: 3
source_sha256: a86a21b3d482515a3b52182abab9dd3a98a7d943feeb96c88549f8e5304b59a1
translation: machine
translated_at: '2026-10-24'
---
# Go-Sprachgrundlagen {#go-language-fundamentals}

Zentrale Sprachmerkmale von Go - Typsystem, Slices, Maps, Pointer, Interfaces, Closures und Fehlerbehandlung. Behandelt Laufzeitinterna und gängige Muster für produktiven Go-Code.

## Key Facts {#key-facts}

- `string` ist eine unveränderliche, schreibgeschützte Byte-Slice: `struct { data *byte; len int }`
- Ein Slice ist eine Sicht auf ein zugrunde liegendes Array: `struct { data *T; len int; cap int }`
- Go 1.24 Maps verwenden Swiss Table mit SIMD-beschleunigter Suche (zuvor geschlossenes Hashing mit Buckets)
- Maps sind NICHT nebenläufigkeitssicher - `sync.Map` oder einen externen Mutex verwenden
- Interfaces werden implizit implementiert - kein `implements`-Schlüsselwort (strukturelle Typisierung)
- `any` = `interface{}` seit Go 1.18

## Patterns {#patterns}

### Slices {#slices}

```go
s := make([]int, 3, 10)     // len=3, cap=10
s = append(s, 4)             // uses existing array if cap allows
s2 := s[1:3]                 // shares underlying array!
s3 := s[1:3:5]               // three-index slice: limits cap
```

Wichtige Verhaltensweisen:
- `append` verdoppelt die Kapazität bis ~256 Elemente und wächst danach um ~1,25x (Go 1.18+)
- Sub-Slices teilen sich das zugrunde liegende Array - Änderungen an einem wirken sich auf das andere aus
- `copy(dst, src)` oder `append(nil, src...)` für unabhängige Kopien verwenden
- Der Vergleich von Slices erfordert `slices.Equal()` - direktes `==` ist nicht erlaubt

### Maps {#maps}

```go
m := make(map[string]int, 100) // preallocate hint - reduces rehashing
delete(m, "key")
val, ok := m["key"]            // safe lookup - ok=false if absent
```

### Pointer {#pointers}

Pointer nur verwenden, wenn:
1. ein Struct innerhalb einer Funktion verändert wird
2. das Struct groß ist (Faustregel: >1 KB)
3. Nullable-Semantik benötigt wird

Ein Pointer auf Slice/Map/Channel ist fast nie nötig - diese sind intern bereits Referenztypen.

**Escape-Analyse**: Der Compiler entscheidet zwischen Stack und Heap. Mit `go build -gcflags="-m"` profilieren.

### Interfaces {#interfaces}

```go
type ReadWriter interface { Reader; Writer } // interface composition
type MyService struct { BaseService }        // struct embedding
```

**Typed-nil-Falle**:
```go
var p *MyError = nil
var err error = p   // err is NOT nil! type info is non-nil
if err != nil { ... } // this branch EXECUTES
```

Immer das `error`-Interface zurückgeben, nicht konkrete Fehlertypen.

Typassertion: `val.(ConcreteType)` panics bei falschem Typ. Sicher: `val, ok := v.(T)`.
Type Switch: `switch v := x.(type) { case *T: ... case *S: ... }`.

### Closures {#closures}

Häufige Falle - Erfassung der Schleifenvariable:
```go
// Wrong: all goroutines capture same 'i'
for i := 0; i < 5; i++ {
    go func() { fmt.Println(i) }()
}

// Correct: pass as argument
for i := 0; i < 5; i++ {
    go func(n int) { fmt.Println(n) }(i)
}
// In Go 1.22+: loop variable is per-iteration (fixed)
```

### Fehlerbehandlung {#error-handling}

Fehler sind Werte - sie werden zurückgegeben, Exceptions werden nicht zur Steuerung des Kontrollflusses verwendet.

```go
if err != nil {
    return fmt.Errorf("context: %w", err) // wrap with %w for unwrapping
}

var myErr *MyError
if errors.As(err, &myErr) { ... }    // checks chain
if errors.Is(err, io.EOF) { ... }    // checks chain for specific value
```

`panic/recover`: panic für nicht behebbare Programmierfehler. HTTP-Server verwenden recover häufig in Handler-Middleware. `fatal error` (Stack-Overflow) kann nicht abgefangen werden.

### Context {#context}

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()

ctx = context.WithValue(ctx, key, value) // request-scoped data only
```

Regeln:
- `ctx` als erstes Argument an alle I/O-Funktionen übergeben
- `ctx` niemals in einem Struct speichern
- `cancel()` aufrufen, sobald die Arbeit erledigt ist
- Context-Werte nur für anfragebezogene Daten (Benutzer-ID, Trace-ID) verwenden, nicht für optionale Parameter

### Functional Options {#functional-options}

```go
type Option func(*Server)
func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}
func NewServer(opts ...Option) *Server {
    s := &Server{timeout: 5*time.Second}
    for _, opt := range opts { opt(s) }
    return s
}
```

## Gotchas {#gotchas}

- Sub-Slices teilen sich das zugrunde liegende Array - das Ändern eines Sub-Slices verändert das Original
- Maps sind nicht nebenläufigkeitssicher; `sync.Map` ist für leselastige Workloads optimiert und kein allgemeiner Ersatz
- Ein Typed-nil-Interface ist NICHT nil (das Interface enthält Typinformationen, auch wenn der Wert nil ist)
- `unsafe.Pointer` umgeht das Typsystem - nur für C-Bindings und speicherabgebildete I/O verwenden
- Go 1.22 hat die Erfassung der Schleifenvariable für Goroutinen behoben - in älteren Versionen teilen sich alle Closures dieselbe Variable

## Siehe auch {#see-also}

- [Go Concurrency - Goroutines, Channels und Sync](concurrency-patterns.md) - GMP-Scheduler, Channels, Sync-Primitive
- [[microservices]] - gRPC, Clean Architecture, Projektstruktur
- [[database-patterns]] - PostgreSQL/pgx, MongoDB, Redis
