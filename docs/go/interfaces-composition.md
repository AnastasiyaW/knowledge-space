---
title: Interfaces and Composition
category: patterns
tags: [go, interfaces, embedding, composition, duck-typing, dependency-injection, type-assertions]
---

# Interfaces and Composition

Go uses interfaces for polymorphism and embedding for composition. Interfaces are satisfied implicitly (duck typing) - a type implements an interface by having the right methods, with no explicit declaration. Go favors composition over inheritance, using struct embedding to reuse behavior.

## Key Facts

- Interfaces are implicit: no `implements` keyword, just matching method signatures
- Small interfaces are idiomatic: `io.Reader` has one method, `io.ReadWriteCloser` has three
- Interface values are nil if both the type and value are nil - a non-nil interface can hold a nil pointer
- `any` (alias for `interface{}`) represents any type, used sparingly in idiomatic Go
- Struct embedding promotes fields and methods of the embedded type to the containing struct
- Embedding is NOT inheritance: you cannot assign an outer type to the inner type's variable
- Accept interfaces, return structs - standard Go design principle

## Interface Basics

### Defining and Implementing

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

### Standard Library Interfaces

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

## Interface Design Principles

### Accept Interfaces, Return Structs

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

### Keep Interfaces Small

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

### Define Interfaces Where They're Used

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

## Struct Embedding (Composition)

### Basic Embedding

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

### Embedding Is Not Inheritance

```go
var e Employee = m           // COMPILE ERROR - not assignable
var e Employee = m.Employee  // OK - explicit access

// The outer type does NOT satisfy interfaces requiring the inner type
// Manager is NOT an Employee, it HAS an Employee
```

### Shadowing Embedded Fields

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

### Embedding Interfaces

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

## Type Assertions and Type Switches

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

## Dependency Injection

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

## Gotchas

- **Non-nil interface with nil value** - an interface holding a nil pointer is NOT nil. `var p *MyStruct = nil; var i MyInterface = p; i != nil` is TRUE. This causes subtle bugs when returning `nil` concrete types as interface values. Always return the interface type explicitly: `return nil`, not `return p`
- **Embedding promotes all methods, including unwanted ones** - if you embed `sync.Mutex`, the `Lock()` and `Unlock()` methods become part of your type's API. Use a named field instead if you don't want promotion: `mu sync.Mutex` instead of `sync.Mutex`
- **Interface pollution** - defining interfaces before you need them, or defining large interfaces that most implementations don't fully use. Follow the Go proverb: the bigger the interface, the weaker the abstraction. Define interfaces at the consumer side, not the producer side

## See Also

- [[error-handling]] - the `error` interface and custom error types
- [[goroutines-channels]] - interfaces for concurrent component contracts
- [[http-servers]] - `http.Handler` interface and middleware composition
