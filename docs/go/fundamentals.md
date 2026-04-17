---
title: Go Language Fundamentals
category: concepts
tags: [go, golang, types, slices, maps, interfaces, pointers]
---

# Go Language Fundamentals

Core Go language features - type system, slices, maps, pointers, interfaces, closures, and error handling. Covers runtime internals and common patterns for production Go code.

## Key Facts

- `string` is an immutable read-only byte slice: `struct { data *byte; len int }`
- Slice is a view over an underlying array: `struct { data *T; len int; cap int }`
- Go 1.24 maps use Swiss Table + SIMD-accelerated lookup (previously closed hashing with buckets)
- Maps are NOT safe for concurrent access - use `sync.Map` or external mutex
- Interfaces are implicitly implemented - no `implements` keyword (structural typing)
- `any` = `interface{}` since Go 1.18

## Patterns

### Slices

```go
s := make([]int, 3, 10)     // len=3, cap=10
s = append(s, 4)             // uses existing array if cap allows
s2 := s[1:3]                 // shares underlying array!
s3 := s[1:3:5]               // three-index slice: limits cap
```

Key behaviors:
- `append` doubles capacity up to ~256 elements, then grows by ~1.25x (Go 1.18+)
- Sub-slices share the underlying array - mutations in one affect the other
- Use `copy(dst, src)` or `append(nil, src...)` for independent copies
- Comparing slices requires `slices.Equal()` - direct `==` is not allowed

### Maps

```go
m := make(map[string]int, 100) // preallocate hint - reduces rehashing
delete(m, "key")
val, ok := m["key"]            // safe lookup - ok=false if absent
```

### Pointers

Only use pointers when:
1. Mutating struct in a function
2. Struct is large (>1 KB rule of thumb)
3. Nullable semantics needed

Pointer to slice/map/channel is almost never needed - they are already reference types internally.

**Escape analysis**: compiler decides stack vs heap. Profile with `go build -gcflags="-m"`.

### Interfaces

```go
type ReadWriter interface { Reader; Writer } // interface composition
type MyService struct { BaseService }        // struct embedding
```

**Typed nil gotcha**:
```go
var p *MyError = nil
var err error = p   // err is NOT nil! type info is non-nil
if err != nil { ... } // this branch EXECUTES
```

Always return `error` interface, not concrete error types.

Type assertion: `val.(ConcreteType)` panics if wrong. Safe: `val, ok := v.(T)`.
Type switch: `switch v := x.(type) { case *T: ... case *S: ... }`.

### Closures

Common gotcha - loop variable capture:
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

### Error Handling

Errors are values - return them, don't use exceptions for control flow.

```go
if err != nil {
    return fmt.Errorf("context: %w", err) // wrap with %w for unwrapping
}

var myErr *MyError
if errors.As(err, &myErr) { ... }    // checks chain
if errors.Is(err, io.EOF) { ... }    // checks chain for specific value
```

`panic/recover`: panic for unrecoverable programmer errors. HTTP servers commonly use recover in handler middleware. `fatal error` (stack overflow) cannot be recovered.

### Context

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()

ctx = context.WithValue(ctx, key, value) // request-scoped data only
```

Rules:
- Pass `ctx` as first argument to all I/O functions
- Never store ctx in struct
- Call `cancel()` as soon as work is done
- Context values for request-scoped data only (user ID, trace ID), not optional parameters

### Functional Options

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

## Gotchas

- Sub-slices share underlying array - modifying a sub-slice mutates the original
- Maps are not concurrent-safe; `sync.Map` is optimized for read-heavy workloads, not a general replacement
- Typed nil interface is NOT nil (interface holds type info even when value is nil)
- `unsafe.Pointer` bypasses type system - only for C bindings and memory-mapped I/O
- Go 1.22 fixed loop variable capture for goroutines - in older versions each closure shares the same variable

## See Also

- [[go/concurrency-patterns]] - GMP scheduler, channels, sync primitives
- [[microservices]] - gRPC, clean architecture, project layout
- [[database-patterns]] - PostgreSQL/pgx, MongoDB, Redis
