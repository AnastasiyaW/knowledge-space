---
title: "Gestion des erreurs"
category: patterns
tags: [go, errors, wrapping, sentinel, custom-errors, panic, recover, error-types]
level: 3
source_sha256: 8def333876d3f21fcf5d1c75da157d78e28570eba92a2821925a75a3b549f23e
translation: machine
translated_at: '2026-10-24'
---
# Gestion des erreurs {#error-handling}

Go utilise des retours d'erreur explicites au lieu des exceptions. Les fonctions qui peuvent échouer renvoient une `error` comme dernière valeur de retour. L'appelant doit la vérifier. Cela rend les chemins d'erreur visibles et oblige les développeurs à traiter les échecs à l'endroit où ils surviennent.

## Points clés {#key-facts}

- `error` est une interface : `type error interface { Error() string }`
- Le style idiomatique en Go renvoie `(result, error)` : vérifiez toujours `err != nil` avant d'utiliser le résultat
- `errors.New("message")` et `fmt.Errorf("format %v", val)` créent des erreurs simples
- Le wrapping d'erreur avec le verbe `%w` préserve la chaîne d'erreurs : `fmt.Errorf("context: %w", err)`
- `errors.Is()` recherche une erreur spécifique dans la chaîne (remplace la comparaison `==`)
- `errors.As()` extrait un type d'erreur spécifique de la chaîne (remplace l'assertion de type)
- `panic` est réservé aux situations réellement irrécupérables, et non à la gestion d'erreurs courante
- Les erreurs sentinelles sont des variables au niveau du package signalant des conditions précises (par exemple `io.EOF`)

## Gestion de base des erreurs {#basic-error-handling}

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

### Erreurs formatées {#formatted-errors}

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide %f by zero", a)
    }
    return a / b, nil
}
```

## Erreurs sentinelles {#sentinel-errors}

Valeurs d'erreur au niveau du package qui signalent des conditions précises. Par convention, leurs noms commencent par `Err` (sauf `io.EOF`).

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

## Wrapping d'erreurs {#error-wrapping}

Le wrapping ajoute du contexte tout en préservant l'erreur d'origine pour inspection.

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

### errors.Is ou errors.As {#errorsis-vs-errorsas}

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

## Types d'erreur personnalisés {#custom-error-types}

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

### Erreur personnalisée avec wrapping {#custom-error-with-wrapping}

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

## Motifs de gestion des erreurs {#error-handling-patterns}

### Defer pour un wrapping cohérent {#defer-for-consistent-wrapping}

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

### Motif des retours multiples {#multiple-returns-pattern}

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

## Panic et recover {#panic-and-recover}

`panic` interrompt la goroutine avec une trace de pile. `recover` intercepte un panic à l'intérieur d'une fonction différée. À utiliser avec parcimonie.

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

## Pièges à éviter {#gotchas}

- **Une variable err réutilisée masque les erreurs non vérifiées** : Go exige que chaque variable soit lue au moins une fois, mais pas que chaque écriture soit lue. Si vous réutilisez `err` pour plusieurs affectations, le compilateur n'exige qu'une seule vérification. Utilisez le linter `staticcheck` pour détecter les écritures d'erreurs non vérifiées
- **La différence entre %w et %v dans fmt.Errorf est importante** : utiliser `%v` au lieu de `%w` crée une nouvelle chaîne d'erreur mais n'encapsule PAS l'erreur d'origine. `errors.Is` et `errors.As` ne retrouveront pas l'erreur d'origine. Utilisez toujours `%w` lorsque la chaîne d'erreurs doit pouvoir être inspectée
- **Les erreurs sentinelles sont modifiables** : ce sont des variables au niveau du package, rien n'empêche leur modification. Ne modifiez jamais une erreur sentinelle. Go n'a pas de `const` pour les erreurs ; la communauté s'appuie sur une convention pour les traiter comme en lecture seule
- **Un panic dans une goroutine fait planter tout le programme** : si une goroutine panique sans `recover`, c'est l'ensemble du programme qui se termine, et non seulement cette goroutine. Ajoutez toujours un `recover` dans les goroutines qui traitent des entrées non fiables

## Voir aussi {#see-also}

- [[goroutines-channels]] - propagation des erreurs à travers les canaux dans le code concurrent
- [[interfaces-composition]] - l'interface error et les types d'erreur personnalisés
- [[http-servers]] - motifs de gestion des erreurs HTTP et middlewares
