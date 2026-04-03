---
title: Go Concurrency - Goroutines, Channels, and Sync
category: concepts
tags: [misc, go, golang, concurrency, goroutines, channels, mutex, scheduler]
---

# Go Concurrency - Goroutines, Channels, and Sync

Go's concurrency model - the GMP scheduler, channels, select, synchronization primitives, and production patterns for concurrent Go programs.

## Key Facts

- Goroutine stack starts at 2-8KB, grows dynamically - ~1 million goroutines feasible
- GMP scheduler: G (goroutine), M (OS thread), P (processor/run queue), count = GOMAXPROCS
- Scheduling is cooperative-preemptive: yields at function calls + async preemption since Go 1.14
- Unbuffered channel synchronizes sender and receiver; buffered blocks only when full
- Only the sender should close a channel; sending to closed channel panics
- `go run -race` or `go test -race` for data race detection

## Patterns

### Channels

```go
ch := make(chan int)        // unbuffered: synchronizes sender and receiver
ch := make(chan int, 100)   // buffered: sender blocks only when full

ch <- value                 // send (blocks if full/no receiver)
value := <-ch               // receive (blocks if empty/no sender)
value, ok := <-ch           // ok=false if channel closed and empty

close(ch)                   // only sender should close
for v := range ch { ... }  // reads until closed
```

### Channel Rules

| Operation | nil channel | closed channel |
|-----------|-------------|----------------|
| Send | blocks forever | panics |
| Receive | blocks forever | returns zero value (ok=false) |

### Semaphore via Buffered Channel

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

**Signal channel**: `done := make(chan struct{})` - zero-size struct uses no memory.

### Select Statement

```go
select {
case v := <-ch1:  ...
case ch2 <- val:  ...
case <-time.After(timeout): ...
default:          // non-blocking
}
```

Non-deterministic - if multiple cases are ready, one is chosen at random.

### Synchronization Primitives

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

### Graceful Shutdown

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
<-ctx.Done()
// shutdown logic: close listeners, drain connections, flush buffers
```

### GMP Scheduler Internals

- **G** (Goroutine): user-space green thread with growable stack
- **M** (Machine): OS thread, bounded by GOMAXPROCS
- **P** (Processor): local run queue + context, count = GOMAXPROCS

Work-stealing scheduler: idle P steals goroutines from other P's run queues.

`runtime.Gosched()` - explicitly yield; rarely needed. `runtime.GOMAXPROCS(n)` - set number of OS threads.

## Gotchas

- Sending to a closed channel panics - always have a clear ownership model for who closes
- Receiving from nil channel blocks forever (useful for disabling a select case)
- `sync.Map` is not a general replacement for `map + mutex` - optimized for read-heavy or disjoint key sets
- Race detector has false negatives but catches most races - always run tests with `-race`
- High goroutine count only degrades when they all compete for the same resources simultaneously
- `wg.Add(n)` must be called before launching goroutines, not inside them

## See Also

- [[go-fundamentals]] - types, slices, maps, interfaces, error handling
- [[go-microservices]] - gRPC services, testing, project layout
- [[javascript-async-patterns]] - comparison: event loop vs goroutines
- [[kafka-messaging]] - consumer groups often implemented with goroutines
