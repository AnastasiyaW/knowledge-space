---
title: "Fehlerbehandlung"
category: patterns
tags: [go, errors, wrapping, sentinel, custom-errors, panic, recover, error-types]
level: 3
source_sha256: 8def333876d3f21fcf5d1c75da157d78e28570eba92a2821925a75a3b549f23e
translation: machine
translated_at: '2026-10-24'
---
# Fehlerbehandlung {#error-handling}

Go verwendet explizite Fehlerrückgaben anstelle von Exceptions. Funktionen, die fehlschlagen können, geben einen `error` als letzten Rückgabewert zurück. Der Aufrufer muss ihn prüfen. Dadurch sind Fehlerpfade sichtbar, und Entwickler müssen Fehler an der Stelle behandeln, an der sie auftreten.

## Wichtige Fakten {#key-facts}

- `error` ist ein Interface: `type error interface { Error() string }`
- Idiomatisches Go gibt `(result, error)` zurück. Prüfe immer `err != nil`, bevor das Ergebnis verwendet wird.
- `errors.New("message")` und `fmt.Errorf("format %v", val)` erzeugen einfache Fehler
- Error Wrapping mit dem Verb `%w` erhält die Fehlerkette: `fmt.Errorf("context: %w", err)`
- `errors.Is()` prüft in der Kette auf bestimmte Fehler (ersetzt den Vergleich mit `==`)
- `errors.As()` extrahiert einen bestimmten Fehlertyp aus der Kette (ersetzt die Typzusicherung)
- `panic` ist für wirklich nicht behebbare Situationen gedacht, nicht für die normale Fehlerbehandlung
- Sentinel-Fehler sind Variablen auf Paketebene, die bestimmte Zustände signalisieren (z. B. `io.EOF`)

## Grundlegende Fehlerbehandlung {#basic-error-handling}

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

### Formatierte Fehler {#formatted-errors}

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide %f by zero", a)
    }
    return a / b, nil
}
```

## Sentinel-Fehler {#sentinel-errors}

Werte für Fehler auf Paketebene, die bestimmte Zustände signalisieren. Per Konvention beginnen die Namen mit `Err` (außer `io.EOF`).

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

## Error Wrapping {#error-wrapping}

Wrapping fügt Kontext hinzu und erhält gleichzeitig den ursprünglichen Fehler für die Prüfung.

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

### errors.Is vs. errors.As {#errorsis-vs-errorsas}

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

## Eigene Fehlertypen {#custom-error-types}

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

### Eigener Fehler mit Wrapping {#custom-error-with-wrapping}

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

## Muster der Fehlerbehandlung {#error-handling-patterns}

### defer für konsistentes Wrapping {#defer-for-consistent-wrapping}

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

### Muster mit mehreren Rückgabewerten {#multiple-returns-pattern}

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

## Panic und Recover {#panic-and-recover}

`panic` beendet die Goroutine mit einem Stack Trace. `recover` fängt einen Panic innerhalb einer deferred Funktion ab. Verwende es sparsam.

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

## Fallstricke {#gotchas}

- **Wiederverwendete err-Variable verdeckt ungeprüfte Fehler** - Go verlangt, dass jede Variable mindestens einmal gelesen wird, aber nicht, dass jede Zuweisung gelesen wird. Wenn du `err` über mehrere Zuweisungen hinweg wiederverwendest, verlangt der Compiler nur eine Prüfung. Mit dem Linter `staticcheck` lassen sich ungeprüfte Fehlerzuweisungen erkennen.
- **%w vs. %v in fmt.Errorf ist wichtig** - Die Verwendung von `%v` statt `%w` erzeugt zwar einen neuen Fehlerstring, wickelt den ursprünglichen Fehler aber NICHT ein. `errors.Is` und `errors.As` finden den ursprünglichen Fehler dann nicht. Verwende immer `%w`, wenn die Fehlerkette prüfbar sein soll.
- **Sentinel-Fehler sind veränderbar** - Sie sind Variablen auf Paketebene, und nichts verhindert eine Änderung. Ändere einen Sentinel-Fehler niemals. Go kennt für Fehler kein `const`. Die Community verlässt sich daher auf die Konvention, sie als schreibgeschützt zu behandeln.
- **Panic in einer Goroutine bringt das gesamte Programm zum Absturz** - Wenn eine Goroutine ohne `recover` in Panic gerät, wird das gesamte Programm beendet, nicht nur diese Goroutine. Füge in Goroutinen, die unvertrauenswürdige Eingaben verarbeiten, immer `recover` hinzu.

## Siehe auch {#see-also}

- [[goroutines-channels]] - Weitergabe von Fehlern über Channels in nebenläufigem Code
- [[interfaces-composition]] - das error-Interface und eigene Fehlertypen
- [[http-servers]] - Muster zur HTTP-Fehlerbehandlung und Middleware
