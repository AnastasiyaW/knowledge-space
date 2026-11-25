---
title: "Goroutines et canaux"
category: patterns
tags: [go, concurrency, goroutines, channels, select, context, waitgroup, pipeline]
level: 3
source_sha256: f0b038f9166da16e1b4b8b409dbc307e6ea2ac6f5159b3df87fa095cb44b66a8
translation: machine
translated_at: '2026-10-24'
---
# Goroutines et canaux {#goroutines-and-channels}

Le modèle de concurrence de Go repose sur les goroutines (threads légers gérés par le runtime Go) et les canaux (conduits typés pour la communication entre goroutines). La philosophie : « Ne communiquez pas en partageant la mémoire ; partagez la mémoire en communiquant. »

## Faits clés {#key-facts}

- Une goroutine est une fonction exécutée de manière concurrente, gérée par l'ordonnanceur du runtime Go et non par le système d'exploitation
- La création d'une goroutine coûte une pile initiale d'environ 2 Ko (qui croît selon les besoins), contre environ 1 Mo pour les threads du système d'exploitation
- Les programmes Go exécutent couramment de quelques milliers à plusieurs centaines de milliers de goroutines concurrentes
- Les canaux sont typés : `chan int`, `chan string`, `chan MyStruct`
- Les canaux non bufferisés bloquent l'émetteur tant que le récepteur n'est pas prêt (point de synchronisation)
- Les canaux bufferisés (`make(chan int, 10)`) ne bloquent l'émetteur que lorsque le tampon est plein
- L'instruction `select` multiplexe plusieurs opérations sur des canaux
- Le paquet `context` fournit l'annulation, les échéances et la propagation de valeurs entre goroutines

## Goroutines {#goroutines}

### Lancement {#launching}

```go
// Launch a goroutine with the go keyword
go func() {
    fmt.Println("running concurrently")
}()

// Named function
go processItem(item)

// Method call
go server.HandleRequest(req)
```

### WaitGroup pour la synchronisation {#waitgroup-for-synchronization}

```go
var wg sync.WaitGroup

for _, item := range items {
    wg.Add(1)
    go func() {
        defer wg.Done()
        process(item)
    }()
}

wg.Wait() // blocks until all goroutines call Done()
```

Depuis Go 1.22, la variable de boucle `item` est propre à chaque itération (plus de bug de capture). Avant la version 1.22, il fallait écrire `item := item` à l'intérieur de la boucle.

## Canaux {#channels}

### Opérations de base {#basic-operations}

```go
// Create channels
ch := make(chan int)       // unbuffered
bch := make(chan int, 10)  // buffered, capacity 10

// Send and receive
ch <- 42       // send (blocks on unbuffered until receiver ready)
val := <-ch    // receive (blocks until value available)

// Close a channel - signals no more values
close(ch)

// Range over channel - receives until closed
for val := range ch {
    fmt.Println(val)
}
```

### Canaux directionnels {#directional-channels}

```go
// Read-only channel (receive only)
func consumer(ch <-chan int) {
    for val := range ch {
        process(val)
    }
}

// Write-only channel (send only)
func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
}

// Bidirectional chan converts implicitly to directional
ch := make(chan int)
go producer(ch) // chan int -> chan<- int (implicit)
consumer(ch)    // chan int -> <-chan int (implicit)
```

### Motif générateur {#generator-pattern}

```go
func countTo(max int) <-chan int {
    ch := make(chan int)
    go func() {
        for i := 0; i < max; i++ {
            ch <- i
        }
        close(ch)
    }()
    return ch
}

for val := range countTo(10) {
    fmt.Println(val)
}
```

## Instruction select {#select-statement}

Multiplexe plusieurs opérations sur des canaux. Bloque jusqu'à ce qu'un cas soit prêt. Si plusieurs cas sont prêts, l'un d'eux est choisi au hasard.

```go
select {
case val := <-ch1:
    fmt.Println("received from ch1:", val)
case ch2 <- outVal:
    fmt.Println("sent to ch2")
case <-time.After(5 * time.Second):
    fmt.Println("timeout")
default:
    fmt.Println("no channel ready, non-blocking")
}
```

### Boucle for-select (motif courant) {#for-select-loop-common-pattern}

```go
for {
    select {
    case val, ok := <-dataCh:
        if !ok {
            return // channel closed
        }
        process(val)
    case <-ctx.Done():
        return // cancellation
    }
}
```

## Context pour l'annulation {#context-for-cancellation}

```go
func countTo(ctx context.Context, max int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; i < max; i++ {
            select {
            case <-ctx.Done():
                return
            case ch <- i:
            }
        }
    }()
    return ch
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    
    ch := countTo(ctx, 100)
    for val := range ch {
        if val > 5 {
            break // cancel() called by defer, goroutine cleans up
        }
        fmt.Println(val)
    }
}
```

### Context avec délai d'expiration {#context-with-timeout}

```go
ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
defer cancel()

select {
case result := <-doWork(ctx):
    fmt.Println("result:", result)
case <-ctx.Done():
    fmt.Println("timed out:", ctx.Err())
}
```

## Motifs de concurrence {#concurrency-patterns}

### Fan-Out / Fan-In {#fan-out-fan-in}

```go
// Fan-out: distribute work to N goroutines
func fanOut(input <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        channels[i] = worker(input)
    }
    return channels
}

// Fan-in: merge multiple channels into one
func fanIn(channels ...<-chan int) <-chan int {
    merged := make(chan int)
    var wg sync.WaitGroup
    for _, ch := range channels {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for val := range ch {
                merged <- val
            }
        }()
    }
    go func() {
        wg.Wait()
        close(merged)
    }()
    return merged
}
```

### Pipeline {#pipeline}

```go
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// Usage: pipeline composition
ch := square(square(generate(2, 3, 4)))
for val := range ch {
    fmt.Println(val) // 16, 81, 256
}
```

### Sémaphore (limiter la concurrence) {#semaphore-limit-concurrency}

```go
sem := make(chan struct{}, 10) // max 10 concurrent

for _, item := range items {
    sem <- struct{}{} // acquire
    go func() {
        defer func() { <-sem }() // release
        process(item)
    }()
}
```

## Quand utiliser les canaux plutôt que les mutex {#when-to-use-channels-vs-mutexes}

```text
Use channels when:
  - Passing ownership of data between goroutines
  - Coordinating multiple pieces of logic  
  - Distributing units of work

Use sync.Mutex when:
  - Protecting a shared cache or state
  - Simple counter increments (or use sync/atomic)
  - Guard an internal struct field
```

## Pièges {#gotchas}

- **Les fuites de goroutines sont des fuites de mémoire silencieuses** - une goroutine bloquée indéfiniment sur un envoi ou une réception de canal n'est jamais libérée par le ramasse-miettes. Prévoyez toujours un chemin d'annulation (context) pour chaque goroutine, et fermez les canaux lorsque la production est terminée
- **Envoyer sur un canal fermé provoque un panic** - seul le producteur (l'émetteur) doit fermer un canal, jamais le consommateur. Si plusieurs producteurs écrivent dans un même canal, utilisez un WaitGroup pour le fermer après la fin de tous les producteurs
- **Les canaux nil bloquent indéfiniment** - un envoi ou une réception sur un canal `nil` bloque de façon permanente. Cela est utile dans un `select` pour désactiver un cas, mais utiliser accidentellement un canal non initialisé provoque des deadlocks silencieux
- **Les canaux bufferisés masquent les bugs** - les canaux bufferisés dissimulent pendant le développement des problèmes de timing qui n'apparaissent qu'en charge. Commencez avec des canaux non bufferisés et n'ajoutez un tampon que pour une raison de performance mesurée

## Voir aussi {#see-also}

- [Gestion des erreurs](error-handling.md) - propagation des erreurs à travers les canaux et les goroutines
- [[interfaces-composition]] - définir des contrats de comportement pour les composants concurrents
- [[http-servers]] - motifs de concurrence dans le traitement des requêtes HTTP
