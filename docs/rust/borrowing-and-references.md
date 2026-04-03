---
title: Borrowing and References
category: concepts
tags: [rust, borrowing, references, mutable, immutable, slices]
---

# Borrowing and References

Borrowing allows access to data without taking ownership. References (`&T` and `&mut T`) are non-owning pointers that the borrow checker validates at compile time, preventing data races and dangling references.

## Key Facts

- `&T` = immutable (shared) reference - multiple allowed simultaneously
- `&mut T` = mutable (exclusive) reference - only one at a time
- Cannot have `&T` and `&mut T` to same data simultaneously
- References must always be valid (no null, no dangling)
- Borrowing rules enforced at compile time by the borrow checker
- Slices (`&[T]`, `&str`) are fat pointers: pointer + length

## Borrowing Rules

1. At any given time, you can have **either** one mutable reference **or** any number of immutable references
2. References must always be valid (no dangling pointers)

```rust
let mut s = String::from("hello");

let r1 = &s;     // OK: immutable borrow
let r2 = &s;     // OK: second immutable borrow
// let r3 = &mut s; // ERROR: cannot borrow mutably while immutable borrows exist

println!("{} {}", r1, r2);
// r1, r2 no longer used after this point (NLL)

let r3 = &mut s;  // OK: immutable borrows are done
r3.push_str(" world");
```

## Patterns

### Slices

```rust
let s = String::from("hello world");
let hello = &s[0..5];    // &str slice
let world = &s[6..11];

let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];    // &[i32] = [2, 3]
```

### Function Borrowing

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return &s[0..i]; }
    }
    &s[..]
}
```

## Gotchas

- NLL (Non-Lexical Lifetimes): borrows end at last use, not at scope end - makes borrow checker more ergonomic
- String literals (`"hello"`) are `&'static str` - references to data baked into the binary
- `&String` auto-coerces to `&str` via `Deref` trait

## See Also

- [[ownership-and-move-semantics]] - ownership transfer vs borrowing
- [[lifetimes]] - explicit lifetime annotations for complex borrowing
- [[collections]] - borrowing patterns with Vec, HashMap, String
