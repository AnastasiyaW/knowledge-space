---
title: Concurrency
category: concepts
tags: [rust, concurrency, threads, send, sync, arc, mutex, channels, c10k]
---

# Concurrency

Rust's type system prevents data races at compile time through the `Send` and `Sync` marker traits. Combined with `Arc<Mutex<T>>` for shared state and channels for message passing, Rust provides fearless concurrency - if it compiles, it's free of data races.

## Key Facts

- **Thread overhead:** 2-8 MB stack, ~10-20 KB kernel structures, ~100 us creation, ~1-10 us context switch
- With 16 GB RAM and 2 MB stack: max ~8,000 threads
- **C10K problem** (Dan Kegel, 1999): 10K connections = 20 GB stack + 50 ms/sec context switching
- Typical HTTP request: 94% time spent WAITING on I/O (DB queries, file reads)
- **Send** = type can be transferred between threads (most types)
- **Sync** = type can be shared via `&T` between threads (most types)
- `Rc<T>` is neither Send nor Sync (use `Arc<T>`)
- `Cell<T>`, `RefCell<T>` are Send but NOT Sync

## Concurrency Problems

- **Race conditions:** result depends on unpredictable execution order
- **Inconsistent state:** read during incomplete modification
- **Lost updates:** two threads read-modify-write, one gets overwritten

## Patterns

### Thread Spawning

```rust
use std::thread;

let handle = thread::spawn(|| {
    println!("Hello from a thread!");
});
handle.join().unwrap();
```

### Arc + Mutex (Shared State)

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));
}

for handle in handles { handle.join().unwrap(); }
println!("Count: {}", *counter.lock().unwrap());
```

### Channels (Message Passing)

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();
let tx2 = tx.clone();

thread::spawn(move || { tx.send("from thread 1").unwrap(); });
thread::spawn(move || { tx2.send("from thread 2").unwrap(); });

for msg in rx { println!("{msg}"); }
```

### RwLock (Many Readers, One Writer)

```rust
use std::sync::RwLock;

let lock = RwLock::new(5);
{
    let r1 = lock.read().unwrap();
    let r2 = lock.read().unwrap(); // multiple readers OK
}
{
    let mut w = lock.write().unwrap(); // exclusive writer
    *w += 1;
}
```

## Gotchas

- `Mutex::lock()` can deadlock if you hold multiple locks in different order across threads
- `Arc::clone()` is cheap (atomic counter increment), but `Mutex::lock()` has overhead
- Raw pointers (`*const T`, `*mut T`) are neither Send nor Sync - use `unsafe` to override if you know it's safe
- Poisoned mutex: if a thread panics while holding a lock, the mutex is poisoned - subsequent `lock()` returns `Err`

## See Also

- [[async-await]] - async alternative to threads for I/O-bound workloads
- [[smart-pointers]] - Arc, Rc, and reference counting
- [[ownership-and-move-semantics]] - `move` closures for thread spawning
