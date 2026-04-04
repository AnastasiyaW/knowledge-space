---
title: Interior Mutability
category: concepts
tags: [refcell, cell, mutex, unsafe, borrowing]
---

# Interior Mutability

Pattern allowing mutation of data behind shared references (`&T`). Bypasses compile-time borrow checking in favor of runtime checks. Used when the compiler cannot prove borrowing safety but the programmer can.

## Key Facts

- Normal Rust: shared ref `&T` = read-only, exclusive ref `&mut T` = mutable
- Interior mutability: mutate through `&T` via runtime-checked wrappers
- `Cell<T>`: copy-based, no borrowing. Only for `T: Copy` types
- `RefCell<T>`: runtime borrow checking. Panics on violation
- `Mutex<T>`: thread-safe interior mutability via locking
- `RwLock<T>`: multiple readers OR one writer, thread-safe
- `AtomicT`: lock-free interior mutability for primitive types
- `UnsafeCell<T>`: foundation of all interior mutability. Raw, no safety guarantees

## Cell - Copy Semantics

```rust
use std::cell::Cell;

let x = Cell::new(42);
// x is not mut, but we can change the inner value
x.set(100);
println!("{}", x.get()); // 100

// Useful in structs behind shared references
struct Counter {
    count: Cell<u32>,
}

impl Counter {
    fn increment(&self) {  // &self, not &mut self
        self.count.set(self.count.get() + 1);
    }
}
```

## RefCell - Runtime Borrow Checking

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// Borrow immutably
{
    let borrowed = data.borrow();
    println!("{:?}", *borrowed);
}

// Borrow mutably
{
    let mut borrowed = data.borrow_mut();
    borrowed.push(4);
}

// PANIC: simultaneous mutable + immutable borrow
// let r1 = data.borrow();
// let r2 = data.borrow_mut();  // panics at runtime!
```

## Common Pattern: Rc + RefCell

```rust
use std::cell::RefCell;
use std::rc::Rc;

// Shared ownership + interior mutability
let shared = Rc::new(RefCell::new(vec![1, 2, 3]));

let clone1 = Rc::clone(&shared);
let clone2 = Rc::clone(&shared);

clone1.borrow_mut().push(4);
clone2.borrow_mut().push(5);

println!("{:?}", shared.borrow()); // [1, 2, 3, 4, 5]
```

## Thread-Safe: Arc + Mutex

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let data = Arc::new(Mutex::new(vec![1, 2, 3]));

let handles: Vec<_> = (0..3).map(|i| {
    let data = Arc::clone(&data);
    thread::spawn(move || {
        let mut lock = data.lock().unwrap();
        lock.push(i);
    })
}).collect();

for h in handles { h.join().unwrap(); }
println!("{:?}", data.lock().unwrap());
```

## Comparison

| Type | Thread-safe | Overhead | Panics | Use case |
|------|------------|----------|--------|----------|
| `Cell<T>` | No | Minimal (copy) | Never | Simple values, counters |
| `RefCell<T>` | No | Runtime borrow check | On violation | Complex single-thread mutation |
| `Mutex<T>` | Yes | Lock acquisition | On poisoning | Multi-thread shared state |
| `RwLock<T>` | Yes | Lock acquisition | On poisoning | Read-heavy multi-thread |
| `Atomic*` | Yes | Lock-free | Never | Counters, flags |

## When to Use

- **Cell**: simple `Copy` values you need to mutate through `&self`
- **RefCell**: complex types in single-threaded code where compiler cannot prove safety
- **Rc<RefCell<T>>**: shared ownership + mutation in single-threaded code (graph nodes, caches)
- **Arc<Mutex<T>>**: shared ownership + mutation across threads
- **OnceCell/LazyCell**: one-time initialization (stable since Rust 1.80)

## Gotchas

- **Issue:** `RefCell::borrow_mut()` called while `borrow()` is active -> panics at runtime -> **Fix:** Keep borrow scopes short. Use blocks `{}` to drop borrows early. Consider `try_borrow_mut()` for non-panicking variant.
- **Issue:** `Mutex` poisoning after a thread panics while holding lock -> **Fix:** Handle with `lock().unwrap_or_else(|e| e.into_inner())` to recover, or let it propagate. Consider `parking_lot::Mutex` which has no poisoning.
- **Issue:** Using `RefCell` in multi-threaded code -> compile error (RefCell is `!Sync`) -> **Fix:** Use `Mutex` or `RwLock` for thread-safe interior mutability.

## See Also

- [[borrowing-and-references]] - compile-time borrow rules that interior mutability relaxes
- [[smart-pointers]] - Rc, Arc, Box
- [[concurrency]] - Mutex, RwLock, atomics
