---
title: "Interfaces et composition"
category: patterns
tags: [go, interfaces, embedding, composition, duck-typing, dependency-injection, type-assertions]
level: 3
source_sha256: 9754844c266f3f5a2fb5a05146e0b250fc0fe18fa0f04549aa7635ccd4cb0482
translation: machine
translated_at: '2026-10-24'
---
# Interfaces et composition {#interfaces-and-composition}

Go utilise les interfaces pour le polymorphisme et l'embedding pour la composition. Les interfaces sont satisfaites de manière implicite (duck typing) : un type implémente une interface dès qu'il possède les méthodes requises, sans déclaration explicite. Go privilégie la composition à l'héritage et utilise l'embedding de struct pour réutiliser du comportement.

## Points clés {#key-facts}

- Les interfaces sont implicites : pas de mot-clé `implements`, seulement la correspondance des signatures de méthodes
- Les petites interfaces sont idiomatiques : `io.Reader` ne possède qu'une méthode, `io.ReadWriteCloser` en possède trois
- Une valeur d'interface est nil si son type et sa valeur sont tous deux nil ; une interface non nil peut contenir un pointeur nil
- `any` (alias de `interface{}`) représente n'importe quel type ; son usage doit rester modéré en Go idiomatique
- L'embedding de struct promeut les champs et méthodes du type embarqué vers la struct englobante
- L'embedding n'est PAS de l'héritage : on ne peut pas affecter un type englobant à une variable du type interne
- Accepter des interfaces, retourner des structs : principe de conception standard en Go

## Bases des interfaces {#interface-basics}

### Définition et implémentation {#defining-and-implementing}

```go
// Define an interface - typically small (1-3 methods)
type Stringer interface {
    String() string
}

// Implement by having matching methods - no explicit declaration
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

func (p Person) String() string {
    return fmt.Sprintf("%s %s, age %d", p.FirstName, p.LastName, p.Age)
}
// Person now satisfies Stringer - automatically, implicitly
```

### Interfaces de la bibliothèque standard {#standard-library-interfaces}

```go
// io.Reader - the most important interface in Go
type Reader interface {
    Read(p []byte) (n int, err error)
}

// io.Writer
type Writer interface {
    Write(p []byte) (n int, err error)
}

// io.Closer
type Closer interface {
    Close() error
}

// Composed from smaller interfaces
type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

// fmt.Stringer
type Stringer interface {
    String() string
}

// error - the most pervasive interface
type error interface {
    Error() string
}
```

## Principes de conception des interfaces {#interface-design-principles}

### Accepter des interfaces, retourner des structs {#accept-interfaces-return-structs}

```go
// Good: accept interface, return concrete type
func ProcessData(r io.Reader) (*Result, error) {
    data, err := io.ReadAll(r)
    if err != nil {
        return nil, err
    }
    return &Result{Data: data}, nil
}

// Callers can pass any Reader: file, network, buffer, string
ProcessData(os.Stdin)
ProcessData(strings.NewReader("hello"))
ProcessData(bytes.NewBuffer(data))
```

### Garder les interfaces petites {#keep-interfaces-small}

```go
// Good: focused interface
type Logger interface {
    Log(msg string)
}

// Avoid: kitchen sink interface
// type Logger interface {
//     Log(msg string)
//     LogWithLevel(level int, msg string)
//     LogJSON(data any)
//     SetOutput(w io.Writer)
//     Flush()
// }
```

### Définir les interfaces là où elles sont utilisées {#define-interfaces-where-theyre-used}

```go
// Package "service" defines the interface it needs
package service

type Store interface {
    Get(id string) (Item, error)
    Put(item Item) error
}

type Service struct {
    store Store
}

// Package "postgres" implements it without importing "service"
package postgres

type DB struct { /* ... */ }

func (db *DB) Get(id string) (Item, error) { /* ... */ }
func (db *DB) Put(item Item) error { /* ... */ }
// postgres.DB satisfies service.Store implicitly
```

## Embedding de struct (composition) {#struct-embedding-composition}

### Embedding de base {#basic-embedding}

```go
type Employee struct {
    Name string
    ID   string
}

func (e Employee) Description() string {
    return fmt.Sprintf("%s (%s)", e.Name, e.ID)
}

type Manager struct {
    Employee        // embedded field - no field name
    Reports []Employee
}

m := Manager{
    Employee: Employee{Name: "Bob", ID: "12345"},
    Reports:  []Employee{},
}

// Promoted fields and methods
fmt.Println(m.Name)          // "Bob" - accessed directly
fmt.Println(m.Description()) // "Bob (12345)" - method promoted
fmt.Println(m.ID)            // "12345"
```

### L'embedding n'est pas de l'héritage {#embedding-is-not-inheritance}

```go
var e Employee = m           // COMPILE ERROR - not assignable
var e Employee = m.Employee  // OK - explicit access

// The outer type does NOT satisfy interfaces requiring the inner type
// Manager is NOT an Employee, it HAS an Employee
```

### Masquage des champs embarqués {#shadowing-embedded-fields}

```go
type Inner struct {
    X int
}

type Outer struct {
    Inner
    X int // shadows Inner.X
}

o := Outer{Inner: Inner{X: 10}, X: 20}
fmt.Println(o.X)       // 20 (Outer.X)
fmt.Println(o.Inner.X) // 10 (must qualify)
```

### Embedding d'interfaces {#embedding-interfaces}

```go
// Embed an interface in a struct - useful for partial implementation
type MyReader struct {
    io.Reader // embed the interface
    count int
}

func (r *MyReader) Read(p []byte) (int, error) {
    n, err := r.Reader.Read(p) // delegate to embedded Reader
    r.count += n
    return n, err
}
```

## Assertions de type et switch de type {#type-assertions-and-type-switches}

```go
// Type assertion: extract concrete type from interface
var w io.Writer = os.Stdout
f, ok := w.(*os.File)
if ok {
    fmt.Println("is a file:", f.Name())
}

// Type switch: dispatch based on concrete type
func describe(i any) string {
    switch v := i.(type) {
    case int:
        return fmt.Sprintf("integer: %d", v)
    case string:
        return fmt.Sprintf("string: %q", v)
    case io.Reader:
        return "implements io.Reader"
    default:
        return fmt.Sprintf("unknown: %T", v)
    }
}
```

## Injection de dépendances {#dependency-injection}

```go
// Define what you need as an interface
type UserStore interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

type UserService struct {
    store  UserStore
    logger Logger
}

func NewUserService(store UserStore, logger Logger) *UserService {
    return &UserService{store: store, logger: logger}
}

// In production: pass real implementation
svc := NewUserService(postgres.NewUserDB(conn), slog.Default())

// In tests: pass mock
svc := NewUserService(&mockStore{}, &mockLogger{})
```

## Pièges à éviter {#gotchas}

- **Interface non nil contenant une valeur nil** - une interface contenant un pointeur nil n'est PAS nil. `var p *MyStruct = nil; var i MyInterface = p; i != nil` vaut TRUE. Cela provoque des bugs subtils lorsqu'on retourne des types concrets `nil` sous forme de valeurs d'interface. Retourner explicitement la valeur nil du type interface : `return nil`, et non `return p`
- **L'embedding promeut toutes les méthodes, y compris celles qu'on ne souhaite pas** - si l'on embarque `sync.Mutex`, les méthodes `Lock()` et `Unlock()` deviennent partie de l'API du type. Utiliser un champ nommé si l'on ne veut pas de promotion : `mu sync.Mutex` au lieu de `sync.Mutex`
- **Pollution par les interfaces** - définir des interfaces avant d'en avoir besoin, ou définir de grosses interfaces que la plupart des implémentations n'utilisent pas entièrement. Suivre le proverbe Go : plus l'interface est grosse, plus l'abstraction est faible. Définir les interfaces côté consommateur, et non côté producteur

## Voir aussi {#see-also}

- [Gestion des erreurs](error-handling.md) - l'interface `error` et les types d'erreur personnalisés
- [[goroutines-channels]] - interfaces pour les contrats de composants concurrents
- [[http-servers]] - l'interface `http.Handler` et la composition de middlewares
