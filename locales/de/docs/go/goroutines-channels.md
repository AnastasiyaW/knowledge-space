---
title: "Goroutinen und Channels"
category: patterns
tags: [go, concurrency, goroutines, channels, select, context, waitgroup, pipeline]
level: 3
source_sha256: f0b038f9166da16e1b4b8b409dbc307e6ea2ac6f5159b3df87fa095cb44b66a8
translation: machine
translated_at: '2026-10-24'
---
# Goroutinen und Channels {#goroutines-and-channels}

Das Nebenläufigkeitsmodell von Go basiert auf Goroutinen (leichtgewichtige Threads, die von der Go-Laufzeitumgebung verwaltet werden) und Channels (typisierte Kanäle für die Kommunikation zwischen Goroutinen). Die Philosophie lautet: „Don't communicate by sharing memory; share memory by communicating."

## Kernfakten {#key-facts}

- Eine Goroutine ist eine Funktion, die nebenläufig ausgeführt wird, vom Go-Laufzeit-Scheduler und nicht vom Betriebssystem verwaltet wird
- Eine Goroutine beginnt mit einem Stack von ~2KB (wächst bei Bedarf) gegenüber ~1MB bei OS-Threads
- Go-Programme betreiben routinemäßig Tausende bis Hunderttausende nebenläufige Goroutinen
- Channels sind typisiert: `chan int`, `chan string`, `chan MyStruct`
- Unbuffered Channels blockieren den Sender, bis der Empfänger bereit ist (Synchronisationspunkt)
- Buffered Channels (`make(chan int, 10)`) blockieren den Sender nur, wenn der Puffer voll ist
- Die `select`-Anweisung multiplext über mehrere Channel-Operationen
- Das `context`-Paket stellt Abbruch, Deadlines und die Weitergabe von Werten über Goroutinen hinweg bereit

## Goroutinen {#goroutines}

### Starten {#launching}

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

### WaitGroup zur Synchronisation {#waitgroup-for-synchronization}

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

Seit Go 1.22 ist die Schleifenvariable `item` pro Iteration eigenständig (kein Capture-Fehler mehr). Vor Go 1.22 war innerhalb der Schleife `item := item` nötig.

## Channels {#channels}

### Grundlegende Operationen {#basic-operations}

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

### Gerichtete Channels {#directional-channels}

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

### Generator-Muster {#generator-pattern}

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

## Select-Anweisung {#select-statement}

Multiplext über mehrere Channel-Operationen. Blockiert, bis ein Fall bereit ist. Sind mehrere bereit, wird einer zufällig ausgewählt.

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

### For-Select-Schleife (häufiges Muster) {#for-select-loop-common-pattern}

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

## Context für Abbruch {#context-for-cancellation}

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

### Context mit Timeout {#context-with-timeout}

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

## Nebenläufigkeitsmuster {#concurrency-patterns}

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

### Semaphore (Nebenläufigkeit begrenzen) {#semaphore-limit-concurrency}

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

## Wann Channels und wann Mutexe verwenden {#when-to-use-channels-vs-mutexes}

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

## Fallstricke {#gotchas}

- **Goroutine-Lecks sind stille Speicherlecks** - eine Goroutine, die dauerhaft auf einem Channel-Senden oder -Empfangen blockiert, wird nie vom Garbage Collector freigegeben. Stelle für jede Goroutine einen Abbruchpfad (context) bereit und schließe Channels, sobald die Produktion abgeschlossen ist
- **Senden auf einen geschlossenen Channel löst eine Panic aus** - nur der Produzent (Sender) sollte einen Channel schließen, niemals der Konsument. Schreiben mehrere Produzenten in einen Channel, verwende eine WaitGroup, um ihn erst nach Abschluss aller Produzenten zu schließen
- **Nil-Channels blockieren dauerhaft** - ein Senden oder Empfangen auf einem `nil`-Channel blockiert unbegrenzt. Das ist in `select` nützlich, um einen Fall zu deaktivieren, führt aber bei versehentlicher Verwendung eines nicht initialisierten Channels zu stillen Deadlocks
- **Buffered Channels verbergen Fehler** - gepufferte Channels maskieren während der Entwicklung Timing-Probleme, die erst unter Last auftreten. Beginne mit unbuffered Channels und füge Puffer nur hinzu, wenn ein gemessener Performance-Grund vorliegt

## Siehe auch {#see-also}

- [Fehlerbehandlung](error-handling.md) - Weitergabe von Fehlern über Channels und Goroutinen
- [[interfaces-composition]] - Definition von Verhaltensverträgen für nebenläufige Komponenten
- [[http-servers]] - Nebenläufigkeitsmuster bei der Verarbeitung von HTTP-Anfragen
