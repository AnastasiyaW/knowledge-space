---
title: Error Handling
category: patterns
tags: [go, errors, wrapping, sentinel, custom-errors, panic, recover, error-types]
---

# Error Handling

Go uses explicit error returns instead of exceptions. Functions that can fail return an `error` as the last return value. The caller must check it. This makes error paths visible and forces developers to handle failures at the point they occur.

## Key Facts

- `error` is an interface: `type error interface { Error() string }`
- Idiomatic Go returns `(result, error)` - always check `err != nil` before using result
- `errors.New("message")` and `fmt.Errorf("format %v", val)` create simple errors
- Error wrapping with `%w` verb preserves the error chain: `fmt.Errorf("context: %w", err)`
- `errors.Is()` checks for specific errors in the chain (replaces `==` comparison)
- `errors.As()` extracts a specific error type from the chain (replaces type assertion)
- `panic` is for truly unrecoverable situations, not for normal error handling
- Sentinel errors are package-level variables signaling specific conditions (e.g., `io.EOF`)

## Basic Error Handling

```go
func doubleEven(i int) (int, error) {
    if i%2 != 0 {
        return 0, errors.New("only even numbers are processed")
    }
    return i * 2, nil
}

result, err := doubleEven(3)
if err != nil {
    log.Fatal(err) // or return err, or handle specifically
}
fmt.Println(result)
```

### Formatted Errors

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide %f by zero", a)
    }
    return a / b, nil
}
```

## Sentinel Errors

Package-level error values that signal specific conditions. By convention, names start with `Err` (except `io.EOF`).

```go
// Defining sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrRateLimited  = errors.New("rate limited")
)

// Checking sentinel errors
if errors.Is(err, ErrNotFound) {
    // handle not found
}

// Standard library sentinels
if errors.Is(err, io.EOF) {
    // end of input
}
if errors.Is(err, sql.ErrNoRows) {
    // no results from query
}
```

## Error Wrapping

Wrapping adds context while preserving the original error for inspection.

```go
// Wrap with %w verb
func readConfig(path string) (Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return Config{}, fmt.Errorf("reading config %s: %w", path, err)
    }
    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return Config{}, fmt.Errorf("parsing config %s: %w", path, err)
    }
    return cfg, nil
}

// Unwrapping chain
err := readConfig("missing.json")
// err.Error() = "reading config missing.json: open missing.json: no such file or directory"

// Check for specific error in chain
if errors.Is(err, os.ErrNotExist) {
    fmt.Println("config file missing, using defaults")
}
```

### errors.Is vs errors.As

```go
// errors.Is: check if specific error value is in chain
if errors.Is(err, os.ErrPermission) {
    // somewhere in the error chain, os.ErrPermission exists
}

// errors.As: extract typed error from chain
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println("failed path:", pathErr.Path)
    fmt.Println("operation:", pathErr.Op)
}
```

## Custom Error Types

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}

// Usage
func validateAge(age int) error {
    if age < 0 || age > 150 {
        return &ValidationError{
            Field:   "age",
            Message: fmt.Sprintf("must be 0-150, got %d", age),
        }
    }
    return nil
}

// Extracting custom error
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Printf("field %s: %s\n", valErr.Field, valErr.Message)
}
```

### Custom Error with Wrapping

```go
type QueryError struct {
    Query string
    Err   error // wrapped error
}

func (e *QueryError) Error() string {
    return fmt.Sprintf("query %s: %v", e.Query, e.Err)
}

func (e *QueryError) Unwrap() error {
    return e.Err // enables errors.Is/As to traverse the chain
}
```

## Error Handling Patterns

### Defer for Consistent Wrapping

```go
func process() (err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("process failed: %w", err)
        }
    }()
    
    val, err := step1()
    if err != nil {
        return err
    }
    return step2(val)
}
```

### Multiple Returns Pattern

```go
// Standard multi-step with early return
func createUser(name, email string) (*User, error) {
    if err := validateName(name); err != nil {
        return nil, fmt.Errorf("invalid name: %w", err)
    }
    if err := validateEmail(email); err != nil {
        return nil, fmt.Errorf("invalid email: %w", err)
    }
    user, err := db.Insert(name, email)
    if err != nil {
        return nil, fmt.Errorf("db insert: %w", err)
    }
    return user, nil
}
```

## Panic and Recover

`panic` terminates the goroutine with a stack trace. `recover` catches a panic inside a deferred function. Use sparingly.

```go
// Panic for truly unrecoverable situations
func mustParseURL(rawURL string) *url.URL {
    u, err := url.Parse(rawURL)
    if err != nil {
        panic(fmt.Sprintf("invalid URL %q: %v", rawURL, err))
    }
    return u
}

// Recover in a deferred function
func safeHandler(w http.ResponseWriter, r *http.Request) {
    defer func() {
        if rec := recover(); rec != nil {
            log.Printf("panic recovered: %v\n%s", rec, debug.Stack())
            http.Error(w, "internal error", http.StatusInternalServerError)
        }
    }()
    handleRequest(w, r) // might panic
}
```

```text
When to panic:
  - Program initialization that absolutely must succeed (parse config, open DB)
  - Convention: functions prefixed with Must (MustCompile, MustParse)
  - Programmer error: impossible state that indicates a bug

When NOT to panic:
  - Network errors, file not found, invalid user input
  - Anything that can happen in normal operation
  - Library code (return errors, let caller decide)
```

## Gotchas

- **Reused err variable hides unchecked errors** - Go requires each variable to be read at least once, but not every write. If you reuse `err` across multiple assignments, the compiler only requires one check. Use `staticcheck` linter to detect unchecked error writes
- **%w vs %v in fmt.Errorf matters** - using `%v` instead of `%w` creates a new error string but does NOT wrap the original. `errors.Is` and `errors.As` will not find the original error. Always use `%w` when you want the error chain to be inspectable
- **Sentinel errors are mutable** - they're package-level variables, nothing prevents mutation. Never modify a sentinel error. Go has no `const` for errors; the community relies on convention to treat them as read-only
- **Panic in a goroutine crashes the entire program** - if a goroutine panics without `recover`, the whole program exits, not just that goroutine. Always add `recover` in goroutines that handle untrusted input

## See Also

- [[goroutines-channels]] - propagating errors through channels in concurrent code
- [[interfaces-composition]] - the error interface and custom error types
- [[http-servers]] - HTTP error handling patterns and middleware
