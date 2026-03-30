---
title: Concurrency
category: concepts
tags: [threads, send, sync, mutex, atomic, channels, rwlock, threadpool]
---
# Concurrency

Rust's type system guarantees thread safety at compile time through `Send`/`Sync` marker traits and [[ownership-and-move-semantics]].

## Key Facts

- `std::thread::spawn` creates OS threads; requires `'static` lifetime for captured data
- `Send` - type can be transferred to another thread (most types are `Send`)
- `Sync` - type can be shared between threads via `&T` (equivalent to `&T: Send`)
- Not `Send`: `Rc`, raw pointers. Not `Sync`: `Cell`, `RefCell`, `Rc`
- `Mutex<T>` - mutual exclusion lock; `lock()` returns `MutexGuard` (RAII)
- `RwLock<T>` - reader-writer lock; multiple readers OR one writer
- `Arc<Mutex<T>>` - standard pattern for shared mutable state across threads
- Channels (`mpsc`): multiple producers, single consumer; `send()`/`recv()`
- `Atomic*` types (AtomicBool, AtomicUsize, etc.) - lock-free thread-safe primitives
- `thread::spawn` returns `JoinHandle`; `.join()` waits for completion

## Patterns

```rust
use std::thread;
use std::sync::{Arc, Mutex, mpsc};
use std::time::Duration;

// Basic thread spawning
let handle = thread::spawn(|| {
    println!("Hello from thread!");
    42
});
let result = handle.join().unwrap();  // 42

// Move closure for data transfer
let data = vec![1, 2, 3];
let handle = thread::spawn(move || {
    println!("{data:?}");  // data moved into thread
});
handle.join().unwrap();

// Shared state with Arc + Mutex
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));  // MutexGuard dropped here, lock released
}

for h in handles {
    h.join().unwrap();
}
println!("count = {}", *counter.lock().unwrap());

// Channels
let (tx, rx) = mpsc::channel();

// Multiple producers
for i in 0..5 {
    let tx = tx.clone();
    thread::spawn(move || {
        tx.send(format!("msg {i}")).unwrap();
    });
}
drop(tx);  // drop original sender so rx iterator ends

for received in rx {
    println!("Got: {received}");
}

// Sync channel (bounded buffer)
let (tx, rx) = mpsc::sync_channel(3);  // buffer size 3
tx.send(1).unwrap();
tx.send(2).unwrap();
// tx.send() blocks if buffer full

// RwLock
use std::sync::RwLock;
let lock = Arc::new(RwLock::new(vec![1, 2, 3]));

// Multiple readers
let lock_clone = Arc::clone(&lock);
let reader = thread::spawn(move || {
    let data = lock_clone.read().unwrap();
    println!("{data:?}");
});

// Single writer
{
    let mut data = lock.write().unwrap();
    data.push(4);
}

// Atomic types
use std::sync::atomic::{AtomicUsize, Ordering};
let counter = Arc::new(AtomicUsize::new(0));
let handles: Vec<_> = (0..10).map(|_| {
    let c = Arc::clone(&counter);
    thread::spawn(move || {
        c.fetch_add(1, Ordering::SeqCst);
    })
}).collect();
for h in handles { h.join().unwrap(); }
println!("{}", counter.load(Ordering::SeqCst));

// Scoped threads (no 'static requirement)
let mut data = vec![1, 2, 3];
thread::scope(|s| {
    s.spawn(|| {
        println!("{data:?}");  // borrows data, no move needed
    });
    s.spawn(|| {
        println!("len = {}", data.len());
    });
});
// all spawned threads joined automatically here
```

## Gotchas

- **Symptom**: "`Rc<T>` cannot be sent between threads safely" - **Cause**: `Rc` is not `Send`/`Sync` (non-atomic ref count) - **Fix**: use `Arc` instead
- **Symptom**: Mutex lock poisoned - **Cause**: a thread panicked while holding the lock - **Fix**: use `.lock().unwrap_or_else(|e| e.into_inner())` to recover, or let it propagate
- **Symptom**: deadlock - **Cause**: two threads waiting for each other's locks - **Fix**: always acquire locks in consistent order; use channels instead of shared state when possible
- **Symptom**: "closure may outlive borrowed value" with `thread::spawn` - **Cause**: spawned thread requires `'static` lifetime - **Fix**: use `move` closure, or use `thread::scope()` for non-`'static` borrows
- **Symptom**: `Cell`/`RefCell` are not `Sync` - **Cause**: they lack internal synchronization - **Fix**: use `Mutex` or `RwLock` for multi-threaded interior mutability

## See Also

- [[smart-pointers]] - `Arc`, `Mutex`, `Cell`, `RefCell`
- [[closures]] - `move` closures for thread spawning
- [[async-await]] - async concurrency alternative
- [[ownership-and-move-semantics]] - Send/Sync and ownership transfer
- [The Rust Book - Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)
- [std::sync](https://doc.rust-lang.org/std/sync/index.html)
- [std::thread::scope](https://doc.rust-lang.org/std/thread/fn.scope.html)
