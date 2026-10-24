---
title: "Fondamentaux du langage Go"
category: concepts
tags: [go, golang, types, slices, maps, interfaces, pointers]
level: 3
source_sha256: a86a21b3d482515a3b52182abab9dd3a98a7d943feeb96c88549f8e5304b59a1
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux du langage Go {#go-language-fundamentals}

Fonctionnalités essentielles du langage Go : système de types, slices, maps, pointeurs, interfaces, fermetures et gestion des erreurs. Couvre les mécanismes internes du runtime et les patterns courants pour le code Go en production.

## Faits clés {#key-facts}

- `string` est un slice d'octets immuable en lecture seule : `struct { data *byte; len int }`
- Un slice est une vue sur un tableau sous-jacent : `struct { data *T; len int; cap int }`
- Les maps de Go 1.24 utilisent Swiss Table et une recherche accélérée par SIMD (auparavant, un hachage fermé avec des buckets)
- Les maps ne sont PAS sûres en accès concurrent : utilisez `sync.Map` ou un mutex externe
- Les interfaces sont implémentées implicitement : pas de mot-clé `implements` (typage structurel)
- `any` = `interface{}` depuis Go 1.18

## Patterns {#patterns}

### Slices {#slices}

```go
s := make([]int, 3, 10)     // len=3, cap=10
s = append(s, 4)             // uses existing array if cap allows
s2 := s[1:3]                 // shares underlying array!
s3 := s[1:3:5]               // three-index slice: limits cap
```

Comportements clés :
- `append` double la capacité jusqu'à environ 256 éléments, puis croît d'environ 1,25x (Go 1.18+)
- Les sous-slices partagent le tableau sous-jacent : une modification dans l'un affecte l'autre
- Utilisez `copy(dst, src)` ou `append(nil, src...)` pour obtenir des copies indépendantes
- La comparaison de slices nécessite `slices.Equal()` : l'opérateur `==` direct n'est pas autorisé

### Maps {#maps}

```go
m := make(map[string]int, 100) // preallocate hint - reduces rehashing
delete(m, "key")
val, ok := m["key"]            // safe lookup - ok=false if absent
```

### Pointeurs {#pointers}

N'utilisez des pointeurs que dans les cas suivants :
1. Modification d'une struct dans une fonction
2. Struct volumineuse (règle empirique : au-delà de 1 Ko)
3. Sémantique nullable nécessaire

Un pointeur vers un slice, une map ou un channel est presque jamais nécessaire : ce sont déjà des types référence en interne.

**Analyse d'échappement** : le compilateur décide entre pile et tas. Profilez avec `go build -gcflags="-m"`.

### Interfaces {#interfaces}

```go
type ReadWriter interface { Reader; Writer } // interface composition
type MyService struct { BaseService }        // struct embedding
```

**Piège du nil typé** :
```go
var p *MyError = nil
var err error = p   // err is NOT nil! type info is non-nil
if err != nil { ... } // this branch EXECUTES
```

Retournez toujours l'interface `error`, et non des types d'erreur concrets.

Assertion de type : `val.(ConcreteType)` panique si le type est incorrect. Version sûre : `val, ok := v.(T)`.
Switch de type : `switch v := x.(type) { case *T: ... case *S: ... }`.

### Fermetures {#closures}

Piège courant : capture de la variable de boucle :
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

### Gestion des erreurs {#error-handling}

Les erreurs sont des valeurs : retournez-les, n'utilisez pas d'exceptions pour le contrôle de flux.

```go
if err != nil {
    return fmt.Errorf("context: %w", err) // wrap with %w for unwrapping
}

var myErr *MyError
if errors.As(err, &myErr) { ... }    // checks chain
if errors.Is(err, io.EOF) { ... }    // checks chain for specific value
```

`panic/recover` : utilisez `panic` pour les erreurs de programmation non récupérables. Les serveurs HTTP utilisent couramment `recover` dans le middleware des handlers. Une `fatal error` (dépassement de pile) ne peut pas être récupérée.

### Context {#context}

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()

ctx = context.WithValue(ctx, key, value) // request-scoped data only
```

Règles :
- Passez `ctx` en premier argument à toutes les fonctions d'E/S
- Ne stockez jamais `ctx` dans une struct
- Appelez `cancel()` dès que le travail est terminé
- Les valeurs du context ne servent qu'aux données propres à la requête (ID utilisateur, ID de trace), et non aux paramètres optionnels

### Options fonctionnelles {#functional-options}

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

## Pièges {#gotchas}

- Les sous-slices partagent le tableau sous-jacent : modifier un sous-slice modifie l'original
- Les maps ne sont pas sûres en concurrence ; `sync.Map` est optimisé pour les charges à forte proportion de lectures, et ne remplace pas une map classique dans le cas général
- Une interface contenant un nil typé n'est PAS nil (l'interface conserve les informations de type même lorsque la valeur est nil)
- `unsafe.Pointer` contourne le système de types : réservé aux bindings C et aux E/S mappées en mémoire
- Go 1.22 corrige la capture de la variable de boucle pour les goroutines ; dans les versions antérieures, chaque closure partage la même variable

## Voir aussi {#see-also}

- [Concurrence en Go : goroutines, canaux et synchronisation](concurrency-patterns.md) : planificateur GMP, canaux, primitives de synchronisation
- [[microservices]] : gRPC, architecture propre, organisation du projet
- [[database-patterns]] : PostgreSQL/pgx, MongoDB, Redis
