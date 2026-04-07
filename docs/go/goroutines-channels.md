---
title: Goroutines and Channels
category: patterns
tags: [go, concurrency, goroutines, channels, select, context, waitgroup, pipeline]
---

# Goroutines and Channels

Go's concurrency model is built on goroutines (lightweight threads managed by the Go runtime) and channels (typed conduits for communication between goroutines). The philosophy: "Don't communicate by sharing memory; share memory by communicating."

## Key Facts

- A goroutine is a function executing concurrently, managed by the Go runtime scheduler, not the OS
- Goroutine creation is ~2KB initial stack (grows as needed) vs ~1MB for OS threads
- Go programs routinely run thousands to hundreds of thousands of concurrent goroutines
- Channels are typed: `chan int`, `chan string`, `chan MyStruct`
- Unbuffered channels block sender until receiver is ready (synchronization point)
- Buffered channels (`make(chan int, 10)`) block sender only when buffer is full
- `select` statement multiplexes across multiple channel operations
- The `context` package provides cancellation, deadlines, and value propagation across goroutines

## Goroutines

### Launching

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

### WaitGroup for Synchronization

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

Since Go 1.22, the loop variable `item` is per-iteration (no capture bug). Before 1.22, you needed `item := item` inside the loop.

## Channels

### Basic Operations

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

### Directional Channels

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

### Generator Pattern

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

## Select Statement

Multiplexes across multiple channel operations. Blocks until one case is ready. If multiple are ready, one is chosen at random.

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

### For-Select Loop (Common Pattern)

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

## Context for Cancellation

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

### Context with Timeout

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

## Concurrency Patterns

### Fan-Out / Fan-In

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

### Pipeline

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

### Semaphore (Limit Concurrency)

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

## When to Use Channels vs Mutexes

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

## Gotchas

- **Goroutine leaks are silent memory leaks** - a goroutine blocked forever on a channel send/receive is never garbage collected. Always provide a cancellation path (context) for every goroutine, and close channels when done producing
- **Sending on a closed channel panics** - only the producer (sender) should close a channel, never the consumer. If multiple producers write to one channel, use a WaitGroup to close after all producers finish
- **Nil channels block forever** - a send or receive on a `nil` channel blocks permanently. This is actually useful in `select` to disable a case, but accidentally using an uninitialized channel causes silent deadlocks
- **Buffered channels hide bugs** - buffered channels mask timing issues during development that surface under load. Start with unbuffered channels, add buffering only when you have a measured performance reason

## See Also

- [[error-handling]] - propagating errors through channels and goroutines
- [[interfaces-composition]] - defining behavior contracts for concurrent components
- [[http-servers]] - concurrency patterns in HTTP request handling
