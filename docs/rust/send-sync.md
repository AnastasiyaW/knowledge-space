---
title: Send and Sync Traits
category: concepts
tags: [concurrency, thread-safety, marker-traits, auto-traits]
---

# Send and Sync Traits

Marker traits that encode thread-safety guarantees at the type level. The compiler uses them to prevent data races at compile time - Rust's key concurrency safety mechanism.

## Key Facts

- `Send`: type can be transferred to another thread (ownership move across thread boundary)
- `Sync`: type can be shared between threads via shared reference (`&T` is `Send` iff `T` is `Sync`)
- Both are auto-traits: compiler implements them automatically when all fields are Send/Sync
- Both are marker traits: no methods, purely compile-time information
- Almost all types are Send + Sync. Notable exceptions: `Rc<T>`, `RefCell<T>`, raw pointers
- Manually implementing Send/Sync is `unsafe` - you assert the invariants hold

## Rules

| T is... | Meaning |
|---------|---------|
| `Send` | Safe to move `T` to another thread |
| `!Send` | Must stay on creating thread |
| `Sync` | Safe for multiple threads to hold `&T` simultaneously |
| `!Sync` | Only one thread can reference at a time |

Derived rule: `T: Sync` iff `&T: Send`

## Common Types

| Type | Send | Sync | Why |
|------|------|------|-----|
| `i32`, `String`, `Vec<T>` | Yes | Yes | No shared mutable state |
| `Rc<T>` | No | No | Non-atomic reference count |
| `Arc<T>` | Yes | Yes | Atomic reference count |
| `RefCell<T>` | Yes | No | Runtime borrow checking not thread-safe |
| `Mutex<T>` | Yes | Yes | Lock serializes access |
| `Cell<T>` | Yes | No | Non-atomic interior mutation |
| `*const T`, `*mut T` | No | No | Raw pointers: no guarantees |
| `MutexGuard<T>` | No | Yes | Must unlock on same thread |

## Patterns

### Thread Spawn Requires Send

```rust
use std::thread;

let data = vec![1, 2, 3];
// Vec is Send, so this works:
thread::spawn(move || {
    println!("{:?}", data);
});

// Rc is !Send, so this fails:
// use std::rc::Rc;
// let rc = Rc::new(42);
// thread::spawn(move || {
//     println!("{}", rc);  // ERROR: Rc<i32> cannot be sent between threads
// });
```

### Shared State Requires Sync

```rust
use std::sync::Arc;
use std::thread;

// Arc<T> is Send + Sync when T: Send + Sync
let shared = Arc::new(vec![1, 2, 3]);

let handles: Vec<_> = (0..3).map(|_| {
    let data = Arc::clone(&shared);
    thread::spawn(move || {
        println!("{:?}", data);  // &Vec is Send because Vec is Sync
    })
}).collect();
```

### Move Closure and Send

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));

let handles: Vec<_> = (0..10).map(|_| {
    let counter = Arc::clone(&counter);
    thread::spawn(move || {
        // Mutex makes interior mutation Sync
        let mut num = counter.lock().unwrap();
        *num += 1;
    })
}).collect();

for h in handles { h.join().unwrap(); }
println!("{}", *counter.lock().unwrap()); // 10
```

### Unsafe Send/Sync Implementation

```rust
struct MyWrapper(*mut u8);

// UNSAFE: you guarantee thread-safety invariants
unsafe impl Send for MyWrapper {}
unsafe impl Sync for MyWrapper {}
```

## Negative Implementations

```rust
// How Rc opts out of Send/Sync (in std):
// impl<T> !Send for Rc<T> {}
// impl<T> !Sync for Rc<T> {}

// You can't write negative impls in stable Rust.
// Use PhantomData to opt out:
use std::marker::PhantomData;
use std::cell::Cell;

struct NotSync {
    _marker: PhantomData<Cell<()>>,  // Cell is !Sync
}
```

## Decision Table

| Need | Use |
|------|-----|
| Shared read-only data across threads | `Arc<T>` where `T: Sync` |
| Shared mutable data across threads | `Arc<Mutex<T>>` or `Arc<RwLock<T>>` |
| Single-thread shared ownership | `Rc<T>` |
| Single-thread interior mutability | `RefCell<T>` or `Cell<T>` |
| Transfer ownership to thread | Anything `Send` via `move` closure |

## Gotchas

- **Issue:** `Rc<T>` inside `thread::spawn` closure fails to compile -> **Fix:** Replace `Rc` with `Arc`. `Arc` is the thread-safe version with atomic reference counting.
- **Issue:** `RefCell<T>` shared via `Arc` fails (RefCell is `!Sync`) -> **Fix:** Use `Arc<Mutex<T>>` or `Arc<RwLock<T>>` instead. Mutex provides thread-safe interior mutability.
- **Issue:** `MutexGuard` held across `.await` point in async code -> **Fix:** `MutexGuard` is `!Send`, which blocks async tasks from moving between threads. Drop the guard before `.await`, or use `tokio::sync::Mutex`.

## See Also

- [[concurrency]] - threads, channels, shared state
- [[interior-mutability]] - Cell, RefCell, Mutex
- [[smart-pointers]] - Rc vs Arc
- [[async-await]] - Send bounds in async contexts
