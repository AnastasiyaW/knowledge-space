---
title: Smart Pointers
category: concepts
tags: [box, rc, arc, deref, drop, heap, RAII, interior-mutability]
---
# Smart Pointers

Smart pointers are structs that act like pointers but provide additional semantics: `Box` for heap allocation, `Rc`/`Arc` for shared ownership, `Cell`/`RefCell` for interior mutability.

## Key Facts

- `Box<T>` - heap allocation with single ownership; implements `Deref<Target=T>` for transparent access
- `Rc<T>` - reference-counted shared ownership (single-threaded); clone increments count, drop decrements; no mutable access
- `Arc<T>` - atomic reference-counted shared ownership (thread-safe [[concurrency]])
- `Cell<T>` - interior mutability for `Copy` types; get/set without `&mut`
- `RefCell<T>` - interior mutability with runtime borrow checking; `borrow()` / `borrow_mut()` panic on violation
- `Cow<'a, B>` - clone-on-write: `Borrowed(&'a B)` or `Owned(<B as ToOwned>::Owned)`
- RAII: all smart pointers drop their contents when they go out of scope
- `Deref` coercion: `&Box<T>` auto-deferences to `&T`, `&String` to `&str`, `&Vec<T>` to `&[T]`
- Common pattern: `Arc<Mutex<T>>` for shared mutable state across threads

## Patterns

```rust
// Box - heap allocation
let b = Box::new(5);
println!("{b}");  // Deref coercion: prints "5"

// Box for recursive types
enum List {
    Cons(i32, Box<List>),
    Nil,
}
let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Nil))));

// Box for trait objects
let animal: Box<dyn std::fmt::Display> = Box::new("hello");

// Rc - shared ownership (single-threaded)
use std::rc::Rc;
let shared = Rc::new(vec![1, 2, 3]);
let clone1 = Rc::clone(&shared);  // increment count
let clone2 = shared.clone();      // same thing
println!("refs: {}", Rc::strong_count(&shared)); // 3

// Arc - thread-safe shared ownership
use std::sync::Arc;
let data = Arc::new(vec![1, 2, 3]);
let data_clone = Arc::clone(&data);
std::thread::spawn(move || {
    println!("{:?}", data_clone);
});

// Cell - interior mutability for Copy types
use std::cell::Cell;
struct Counter {
    value: Cell<i32>,
}
impl Counter {
    fn increment(&self) {  // note: &self, not &mut self
        self.value.set(self.value.get() + 1);
    }
}

// RefCell - runtime borrow checking
use std::cell::RefCell;
let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4);         // mutable borrow at runtime
println!("{:?}", data.borrow());   // shared borrow at runtime
// data.borrow_mut() while borrow() is alive -> PANIC!

// Rc + RefCell pattern (shared mutable data, single-threaded)
let shared_data = Rc::new(RefCell::new(vec![1, 2, 3]));
let ref1 = Rc::clone(&shared_data);
let ref2 = Rc::clone(&shared_data);
ref1.borrow_mut().push(4);
ref2.borrow_mut().push(5);
println!("{:?}", shared_data.borrow()); // [1, 2, 3, 4, 5]

// Arc + Mutex pattern (shared mutable data, multi-threaded)
use std::sync::Mutex;
let counter = Arc::new(Mutex::new(0));
let handles: Vec<_> = (0..10).map(|_| {
    let counter = Arc::clone(&counter);
    std::thread::spawn(move || {
        *counter.lock().unwrap() += 1;
    })
}).collect();
for h in handles { h.join().unwrap(); }
println!("{}", *counter.lock().unwrap()); // 10

// Cow - clone on write
use std::borrow::Cow;
fn normalize(s: &str) -> Cow<'_, str> {
    if s.contains(' ') {
        Cow::Owned(s.replace(' ', "_"))
    } else {
        Cow::Borrowed(s)  // no allocation
    }
}
```

## Gotchas

- **Symptom**: `RefCell::borrow_mut()` panics at runtime - **Cause**: another borrow (shared or mutable) is still active - **Fix**: scope borrows tightly, use `try_borrow_mut()` for safe fallback
- **Symptom**: `Rc` is not `Send` - can't use across threads - **Cause**: reference count is not atomic - **Fix**: use `Arc` for multi-threaded scenarios
- **Symptom**: memory leak with `Rc` cycles - **Cause**: circular references prevent ref count from reaching zero - **Fix**: use `Weak` for back-references: `Rc::downgrade(&rc)`
- **Symptom**: `Box<dyn Trait>` vs `&dyn Trait` - **Cause**: `Box` owns the data (heap-allocated), `&dyn` borrows it - **Fix**: use `Box` when you need ownership, `&dyn` when borrowing suffices

## See Also

- [[ownership-and-move-semantics]] - single ownership with Box
- [[concurrency]] - `Arc<Mutex<T>>` pattern
- [[dynamic-dispatch]] - `Box<dyn Trait>` for trait objects
- [[borrowing-and-references]] - compile-time vs runtime borrow checking
- [The Rust Book - Smart Pointers](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)
- [std::rc::Rc](https://doc.rust-lang.org/std/rc/struct.Rc.html)
- [std::sync::Arc](https://doc.rust-lang.org/std/sync/struct.Arc.html)
