---
title: Async/Await
category: concepts
tags: [async, await, future, tokio, runtime, event-loop, concurrency]
---
# Async/Await

Rust's async system provides cooperative concurrency for I/O-bound workloads using `async`/`await` syntax, `Future` trait, and runtime executors like Tokio.

## Key Facts

- `async fn` returns a `Future` - a lazy computation that does nothing until polled
- `await` yields control until the future completes; can only be used inside `async` context
- The `Future` trait: `fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Output>`
- `Poll::Ready(value)` - future is done; `Poll::Pending` - not yet, wake me later
- Rust has NO built-in async runtime; you choose one: `tokio`, `async-std`, `smol`
- Async is zero-cost: futures are state machines compiled to enums, no heap allocation for the state machine itself
- `async` blocks capture variables like closures; `async move { }` takes ownership
- `tokio::spawn` for concurrent task execution (like `thread::spawn` but cooperative)
- `join!` / `select!` for concurrent/racing futures
- Pin is required because self-referential state machines can't be moved

## Patterns

```rust
// Basic async function
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let body = reqwest::get(url).await?.text().await?;
    Ok(body)
}

// Tokio runtime setup
#[tokio::main]
async fn main() {
    let result = fetch_data("https://example.com").await;
    println!("{:?}", result);
}

// Manual runtime creation
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        println!("Hello from async!");
    });
}

// Concurrent tasks with spawn
async fn process_urls(urls: Vec<String>) {
    let mut handles = vec![];
    for url in urls {
        handles.push(tokio::spawn(async move {
            fetch_data(&url).await
        }));
    }
    for handle in handles {
        match handle.await.unwrap() {
            Ok(data) => println!("Got {} bytes", data.len()),
            Err(e) => eprintln!("Error: {e}"),
        }
    }
}

// join! - run concurrently, wait for all
use tokio::join;
async fn fetch_both() {
    let (a, b) = join!(
        fetch_data("https://a.com"),
        fetch_data("https://b.com"),
    );
    println!("{:?} {:?}", a, b);
}

// select! - race futures, take first result
use tokio::select;
async fn fetch_with_timeout() {
    select! {
        result = fetch_data("https://slow.com") => {
            println!("Got data: {:?}", result);
        }
        _ = tokio::time::sleep(std::time::Duration::from_secs(5)) => {
            println!("Timeout!");
        }
    }
}

// Async channels
use tokio::sync::mpsc;
async fn channel_example() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
        }
    });

    while let Some(value) = rx.recv().await {
        println!("received: {value}");
    }
}

// Async streams
use tokio_stream::StreamExt;
async fn stream_example() {
    let mut interval = tokio::time::interval(
        std::time::Duration::from_millis(100)
    );
    for _ in 0..5 {
        interval.tick().await;
        println!("tick");
    }
}

// Shared state in async (Arc + Mutex)
use std::sync::Arc;
use tokio::sync::Mutex;  // use tokio::sync::Mutex, not std::sync::Mutex
async fn shared_state() {
    let data = Arc::new(Mutex::new(0));
    let mut handles = vec![];
    for _ in 0..10 {
        let data = Arc::clone(&data);
        handles.push(tokio::spawn(async move {
            let mut lock = data.lock().await;
            *lock += 1;
        }));
    }
    for h in handles { h.await.unwrap(); }
}
```

## Gotchas

- **Symptom**: "future cannot be sent between threads safely" - **Cause**: future holds a non-`Send` type (e.g., `Rc`, `MutexGuard` across `.await`) - **Fix**: scope the guard before `.await`, or use `tokio::sync::Mutex`
- **Symptom**: using `std::sync::Mutex` in async causes deadlocks - **Cause**: holding a blocking lock across `.await` blocks the executor thread - **Fix**: use `tokio::sync::Mutex`, or scope the std lock to not span `.await` points
- **Symptom**: async function does nothing - **Cause**: futures are lazy, must be `.await`ed or spawned - **Fix**: always `await` or `tokio::spawn()` the future
- **Symptom**: "cannot use `await` outside of `async` context" - **Cause**: calling `.await` in synchronous code - **Fix**: wrap in `async` block or make the function `async`; use `block_on()` at the boundary
- **Symptom**: task not making progress - **Cause**: blocking operation (CPU-heavy or blocking I/O) on the async executor - **Fix**: use `tokio::task::spawn_blocking()` for blocking work

## See Also

- [[concurrency]] - OS thread-based concurrency
- [[closures]] - `async move` captures
- [[rust/error-handling]] - `?` operator works inside async functions
- [[traits]] - `Future` trait internals
- [The Rust Book - Async (edition 2024)](https://doc.rust-lang.org/book/ch17-00-async-await.html)
- [Tokio tutorial](https://tokio.rs/tokio/tutorial)
- [Async Book](https://rust-lang.github.io/async-book/)
