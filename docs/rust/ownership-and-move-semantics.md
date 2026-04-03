---
title: Ownership and Move Semantics
category: concepts
tags: [rust, ownership, move, raii, memory, stack, heap, drop]
---

# Ownership and Move Semantics

Rust's ownership system is its defining feature - a compile-time mechanism for memory safety without garbage collection. Three rules govern how values are created, transferred, and destroyed, eliminating use-after-free, double-free, and data races at compile time.

## Key Facts

- **Three ownership rules:** (1) every value has an owner, (2) one owner at a time, (3) when owner goes out of scope, value is destroyed (`Drop::drop` called)
- Move is a bitwise copy from old to new location (may be elided by compiler); old value becomes inaccessible
- **Clone** = explicit deep copy via `.clone()`, can be expensive
- **Copy** = implicit bitwise copy, only for stack-only types (no heap allocations)
- RAII: resource acquisition tied to initialization, release tied to destruction

## Memory Types

| | Stack | Heap |
|---|---|---|
| Contents | Local variables | Program data |
| Size | Limited (2-8 MB/thread) | Unlimited |
| Allocation speed | Fast | Slow |
| Size knowledge | Must know at compile time | Can be dynamic |
| Per-thread | One per thread | One per process |

## Patterns

### Move Semantics

```rust
let s1 = String::from("hello");
let s2 = s1;          // s1 is MOVED to s2, s1 is now invalid
// println!("{}", s1); // ERROR: value used after move

let s1 = String::from("hello");
let s2 = s1.clone();  // deep copy, both valid
```

Move happens on: variable reassignment, passing by value to function, returning from function.

### RAII

```rust
{
    let string = String::from("Hello"); // allocation
    println!("{}", string);              // use
}                                        // automatic deallocation (drop)
```

Resource management approaches: explicit (C), automatic (GC languages), semi-automatic (Rust RAII, Go `defer`, Python `with`).

### Copy vs Clone

```rust
// Copy types: integers, floats, bool, char, tuples of Copy types
let x = 5;
let y = x;  // Copy - both valid
println!("{} {}", x, y);

// Non-Copy types: String, Vec, Box - must use .clone() or move
let v1 = vec![1, 2, 3];
let v2 = v1.clone();  // explicit deep copy
```

## Gotchas

- Integer overflow: debug mode panics, release mode wraps (two's complement); use `checked_add()`, `wrapping_add()`, `saturating_add()` for explicit behavior
- `let x = 5; let x = 5;` is shadowing (new variable), not reassignment - different memory addresses
- `usize` is the only valid type for array/slice indexing

## See Also

- [[borrowing-and-references]] - non-owning access to data
- [[smart-pointers]] - Box, Rc, Arc for heap management
- [[lifetimes]] - compile-time tracking of reference validity
