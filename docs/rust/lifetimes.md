---
title: Lifetimes
category: concepts
tags: [rust, lifetimes, borrow-checker, references, annotations, elision, static, nll]
---

# Lifetimes

Lifetimes are the compiler's way of tracking how long references remain valid. They prevent dangling references at compile time - no garbage collector needed. Most lifetimes are inferred automatically through elision rules; explicit annotations (`'a`) are needed when the compiler cannot determine the relationship between input and output references.

## Key Facts

- Lifetime annotations don't change how long data lives - they describe relationships between references
- `'a` reads as "lifetime a" - a named region of code where a reference is valid
- **Elision rules** handle most cases automatically (single input ref, `&self` methods)
- `'static` = reference valid for entire program (string literals, leaked data)
- **NLL (Non-Lexical Lifetimes)**: borrow checker analyzes actual usage, not just lexical scopes
- Structs holding references must declare lifetime parameters: `struct Foo<'a> { data: &'a str }`

## Patterns

### Explicit Lifetime Annotations

```rust
// Return reference must live as long as BOTH inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Multiple lifetimes when they're independent
fn first_word<'a, 'b>(s: &'a str, _prefix: &'b str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}
```

### Lifetime Elision Rules

The compiler infers lifetimes in three cases:
1. Each input reference gets its own lifetime parameter
2. If exactly one input lifetime, it's assigned to all outputs
3. If one input is `&self` or `&mut self`, its lifetime is assigned to all outputs

```rust
// These are equivalent (rule 2):
fn first(s: &str) -> &str { &s[..1] }
fn first<'a>(s: &'a str) -> &'a str { &s[..1] }

// Method: self's lifetime used for output (rule 3):
impl MyStruct {
    fn name(&self) -> &str { &self.name }
}
```

### Struct Lifetimes

```rust
struct Important<'a> {
    content: &'a str,
}

// Struct cannot outlive the reference it holds
let novel = String::from("Call me Ishmael...");
let i = Important { content: &novel };
// novel must live at least as long as i
```

### 'static Lifetime

```rust
// String literals are always 'static
let s: &'static str = "I live forever";

// 'static as trait bound: type contains no non-static references
fn spawn_thread<T: Send + 'static>(data: T) { /* ... */ }

// Leaking to get 'static (rare, use carefully)
let leaked: &'static str = Box::leak(String::from("leaked").into_boxed_str());
```

### Interior Mutability (Bypassing Borrow Checker at Runtime)

```rust
use std::cell::{Cell, RefCell};

// Cell<T> for Copy types - get/set, no references
let cell = Cell::new(5);
cell.set(10);
let val = cell.get();  // 10

// RefCell<T> for any type - runtime borrow checking
let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4);     // runtime-checked mutable borrow
let r = data.borrow();          // runtime-checked immutable borrow
// data.borrow_mut();            // PANIC: already borrowed immutably
```

## Gotchas

- The compiler cannot analyze control flow for borrows: even `if true { &mut x } else { &y }` may confuse it - restructure code instead
- HashMap Entry API exists specifically because the borrow checker couldn't handle "lookup then insert" patterns
- `Cell`/`RefCell` are Send but NOT Sync - single-threaded only (use `Mutex`/`RwLock` for multi-threaded)
- `'static` doesn't mean "lives forever" as a bound - it means "contains no non-static references" (owned types like `String` are `'static`)

## See Also

- [[borrowing-and-references]] - borrow rules that lifetimes enforce
- [[smart-pointers]] - RefCell for interior mutability, Rc/Arc for shared ownership
- [[concurrency]] - 'static bound on spawned threads
- [[generics-and-monomorphization]] - lifetime parameters in generic code
