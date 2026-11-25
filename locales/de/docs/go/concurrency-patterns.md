---
title: "Go-Concurrency – Goroutines, Channels und Sync"
category: concepts
tags: [go, golang, concurrency, goroutines, channels, mutex, scheduler]
level: 4
source_sha256: cae9d37fbb1021f273215e1fa2b588862c19a34c4f22eac0fafe5de781704ba1
translation: machine
translated_at: '2026-10-24'
---
# Go-Concurrency – Goroutines, Channels und Sync {#go-concurrency-goroutines-channels-and-sync}

Go-Nebenläufigkeitsmodell: der GMP-Scheduler, Channels, select, Synchronisationsprimitive und Produktionsmuster für nebenläufige Go-Programme.

## Key Facts {#key-facts}

- Der Goroutine-Stack beginnt bei 2-8KB und wächst dynamisch – ~1 Million Goroutines sind machbar
- GMP-Scheduler: G (Goroutine), M (OS-Thread), P (Prozessor/Run-Queue), Anzahl = GOMAXPROCS
- Das Scheduling ist kooperativ-präemptiv: Es gibt die Kontrolle bei Funktionsaufrufen ab, seit Go 1.14 zusätzlich asynchrone Präemption
- Ein ungepufferter Channel synchronisiert Sender und Empfänger; ein gepufferter Channel blockiert nur, wenn er voll ist
- Nur der Sender sollte einen Channel schließen; das Senden auf einen geschlossenen Channel löst einen Panic aus
- `go run -race` oder `go test -race` zur Erkennung von Data Races

## Patterns {#patterns}

### Channels {#channels}

```go
ch := make(chan int)        // unbuffered: synchronizes sender and receiver
ch := make(chan int, 100)   // buffered: sender blocks only when full

ch <- value                 // send (blocks if full/no receiver)
value := <-ch               // receive (blocks if empty/no sender)
value, ok := <-ch           // ok=false if channel closed and empty

close(ch)                   // only sender should close
for v := range ch { ... }  // reads until closed
```

### Channel-Regeln {#channel-rules}

| Operation | nil-Channel | geschlossener Channel |
|-----------|-------------|----------------------|
| Senden | blockiert für immer | panic |
| Empfangen | blockiert für immer | gibt Zero-Value zurück (ok=false) |

### Semaphore mit gepuffertem Channel {#semaphore-via-buffered-channel}

```go
sem := make(chan struct{}, 10) // max 10 concurrent
for _, item := range items {
    sem <- struct{}{}           // acquire
    go func(x Item) {
        defer func() { <-sem }() // release
        process(x)
    }(item)
}
```

**Signal-Channel**: `done := make(chan struct{})` – die Struct ohne Größe belegt keinen Speicher.

### Select-Anweisung {#select-statement}

```go
select {
case v := <-ch1:  ...
case ch2 <- val:  ...
case <-time.After(timeout): ...
default:          // non-blocking
}
```

Nicht deterministisch – sind mehrere Fälle bereit, wird einer zufällig gewählt.

### Synchronisationsprimitive {#synchronization-primitives}

```go
var mu sync.Mutex
mu.Lock(); defer mu.Unlock()

var rw sync.RWMutex
rw.RLock(); defer rw.RUnlock()  // multiple concurrent readers
rw.Lock(); defer rw.Unlock()    // exclusive write

var wg sync.WaitGroup
wg.Add(n)
go func() { defer wg.Done(); ... }()
wg.Wait()

var once sync.Once
once.Do(func() { /* init */ }) // runs exactly once

var count int64
atomic.AddInt64(&count, 1)     // atomic increment
atomic.LoadInt64(&count)       // atomic read
```

### Geordnetes Herunterfahren {#graceful-shutdown}

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
<-ctx.Done()
// shutdown logic: close listeners, drain connections, flush buffers
```

### Interna des GMP-Schedulers {#gmp-scheduler-internals}

- **G** (Goroutine): User-Space-Green-Thread mit wachsendem Stack
- **M** (Machine): OS-Thread, begrenzt durch GOMAXPROCS
- **P** (Processor): lokale Run-Queue + Kontext, Anzahl = GOMAXPROCS

Work-Stealing-Scheduler: Ein untätiger P stiehlt Goroutines aus den Run-Queues anderer P.

`runtime.Gosched()` – gibt die Kontrolle explizit ab; selten nötig. `runtime.GOMAXPROCS(n)` – legt die Anzahl der OS-Threads fest.

## Gotchas {#gotchas}

- Das Senden auf einen geschlossenen Channel löst einen Panic aus – die Verantwortung für das Schließen muss eindeutig geregelt sein
- Das Empfangen von einem nil-Channel blockiert für immer (nützlich, um einen select-Fall zu deaktivieren)
- `sync.Map` ist kein allgemeiner Ersatz für `map + mutex` – optimiert für leselastige Workloads oder disjunkte Schlüsselmengen
- Der Race Detector liefert falsch negative Ergebnisse, findet aber die meisten Races – Tests immer mit `-race` ausführen
- Eine hohe Goroutine-Anzahl wird nur dann zum Problem, wenn alle gleichzeitig um dieselben Ressourcen konkurrieren
- `wg.Add(n)` muss vor dem Start der Goroutines aufgerufen werden, nicht innerhalb davon

## See Also {#see-also}

- [[go/fundamentals]] – Typen, Slices, Maps, Interfaces, Fehlerbehandlung
- [[microservices]] – gRPC-Services, Testing, Projektstruktur
- [[javascript-async-event-loop]] – Vergleich: Event-Loop vs. Goroutines
- [[kafka-messaging-fundamentals]] – Consumer-Gruppen, häufig mit Goroutines umgesetzt
