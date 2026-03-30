---
title: Ownership and Move Semantics
category: concepts
tags: [ownership, move, memory, RAII, drop]
---
# Ownership and Move Semantics

Rust's ownership system is a set of compile-time rules that governs how memory is managed without a garbage collector.

## Key Facts

- Every value in Rust has exactly one owner variable
- When the owner goes out of scope, the value is dropped (RAII pattern)
- Assignment of non-[[closures#Copy]] types **moves** the value - the original binding becomes invalid
- Move is a bitwise copy of the stack representation; no deep copy occurs
- Types implementing `Copy` are implicitly copied instead of moved (integers, `bool`, `char`, tuples/arrays of `Copy` types)
- `Clone` trait provides explicit deep-copy via `.clone()`
- `Drop` trait provides custom destructor logic; called automatically when owner goes out of scope
- You cannot implement both `Copy` and `Drop` on the same type

## Patterns

```rust
// Move semantics
let s1 = String::from("hello");
let s2 = s1;          // s1 is moved into s2
// println!("{s1}");   // ERROR: value used after move

// Clone for explicit copy
let s1 = String::from("hello");
let s2 = s1.clone();  // deep copy
println!("{s1}");      // OK

// Copy types are implicitly copied
let x: i32 = 42;
let y = x;             // x is still valid (i32 is Copy)
println!("{x}");        // OK

// Move in function calls
fn take_ownership(s: String) {
    println!("{s}");
}   // s is dropped here

let s = String::from("hello");
take_ownership(s);
// println!("{s}");     // ERROR: s was moved

// Returning ownership
fn give_back(s: String) -> String {
    s   // ownership transferred to caller
}

// Custom Drop
struct Resource { name: String }
impl Drop for Resource {
    fn drop(&mut self) {
        println!("Dropping {}", self.name);
    }
}
// drop order: reverse declaration order
```

```rust
// Partial moves from structs
struct Person { name: String, age: u32 }

let p = Person { name: String::from("Alice"), age: 30 };
let name = p.name;     // partial move
// println!("{}", p.name);  // ERROR: partially moved
println!("{}", p.age);      // OK: age is Copy
```

## Gotchas

- **Symptom**: "value used here after move" - **Cause**: variable was moved by assignment or function call - **Fix**: use `.clone()`, pass by reference, or restructure to avoid the move
- **Symptom**: "cannot move out of index" on `Vec<String>` - **Cause**: indexing gives a reference, not ownership - **Fix**: use `.remove()`, `.swap_remove()`, or `std::mem::replace()`
- **Symptom**: `let _ = val` does NOT extend lifetime; `let _x = val` does - **Cause**: `_` is not a binding, it drops immediately; `_x` is a named binding
- **Symptom**: Drop order surprise in structs - **Cause**: struct fields are dropped in declaration order, local variables in reverse declaration order

## See Also

- [[borrowing-and-references]] - using values without taking ownership
- [[smart-pointers]] - `Box`, `Rc`, `Arc` for heap allocation and shared ownership
- [[closures]] - `Copy` and `Clone` trait details
- [The Rust Book - Ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)
- [std::ops::Drop](https://doc.rust-lang.org/std/ops/trait.Drop.html)
