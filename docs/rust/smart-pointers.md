---
title: Smart Pointers
category: concepts
tags: [rust, smart-pointers, box, rc, arc, refcell, interior-mutability, heap]
---

# Smart Pointers

Smart pointers are data structures that act like pointers but have additional metadata and capabilities. They implement `Deref` (for transparent dereferencing) and `Drop` (for automatic cleanup). The main smart pointers are `Box<T>`, `Rc<T>`, `Arc<T>`, `RefCell<T>`, and `Cow<T>`.

## Key Facts

- **Box<T>** = heap allocation with single ownership, zero-cost abstraction (just a pointer)
- **Rc<T>** = reference counting, multiple owners, single-threaded only
- **Arc<T>** = atomic reference counting, multiple owners, thread-safe
- **RefCell<T>** = interior mutability with runtime borrow checking
- **Cow<T>** = clone-on-write, avoids allocation when data doesn't need modification
- `Box<T>` is the most common - used for recursive types, trait objects, and large stack-to-heap moves

## Patterns

### Box<T> - Heap Allocation

```rust
// Recursive type (requires known size)
enum List {
    Cons(i32, Box<List>),
    Nil,
}

// Trait objects
let animal: Box<dyn Animal> = Box::new(Dog { name: "Rex".into() });

// Large data on heap
let big_array = Box::new([0u8; 1_000_000]);
```

### Rc<T> - Reference Counting

```rust
use std::rc::Rc;

let a = Rc::new(vec![1, 2, 3]);
let b = Rc::clone(&a);  // increment reference count (cheap)
let c = Rc::clone(&a);

println!("References: {}", Rc::strong_count(&a)); // 3
// Data dropped when last Rc goes out of scope
```

### RefCell<T> - Interior Mutability

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// Runtime borrow checking
let borrowed = data.borrow();      // immutable borrow
// data.borrow_mut();              // PANIC: already borrowed immutably
drop(borrowed);

data.borrow_mut().push(4);         // OK: no active borrows
```

### Common Combinations

```rust
// Multiple owners with mutability (single-threaded)
let shared = Rc::new(RefCell::new(HashMap::new()));

// Multiple owners with mutability (multi-threaded)
let shared = Arc::new(Mutex::new(HashMap::new()));
```

## Gotchas

- `Rc<T>` can create reference cycles → memory leaks; use `Weak<T>` to break cycles
- `RefCell<T>` panics at runtime if borrow rules violated - compile-time safety traded for flexibility
- `Rc<T>` is NOT thread-safe (use `Arc<T>` for multithreading)
- `Box<T>` moves data to heap but the Box itself lives on stack (pointer-sized)

## See Also

- [[ownership-and-move-semantics]] - ownership model that smart pointers extend
- [[concurrency]] - Arc + Mutex for thread-safe shared state
- [[traits]] - Deref and Drop traits that power smart pointers
