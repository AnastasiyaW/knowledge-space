---
title: Borrowing and References
category: concepts
tags: [borrowing, references, borrow-checker, slices]
---
# Borrowing and References

Borrowing allows accessing data without taking [[ownership-and-move-semantics]] by using references.

## Key Facts

- `&T` is a shared (immutable) reference; `&mut T` is an exclusive (mutable) reference
- Borrowing rules enforced at compile time by the borrow checker:
  - Any number of `&T` references OR exactly one `&mut T` at a time (never both)
  - References must always be valid (no dangling references)
- References are non-owning pointers; the original owner retains responsibility for dropping
- Slices (`&[T]`, `&str`) are fat pointers: pointer + length
- Reborrowing: `&mut T` can be temporarily narrowed to `&T`
- NLL (Non-Lexical Lifetimes) - references are valid until their last use, not until end of scope

## Patterns

```rust
// Shared references
fn calculate_length(s: &String) -> usize {
    s.len()
}
let s = String::from("hello");
let len = calculate_length(&s);  // borrow s
println!("{s} has length {len}"); // s still valid

// Mutable references
fn push_world(s: &mut String) {
    s.push_str(" world");
}
let mut s = String::from("hello");
push_world(&mut s);

// Borrowing rules in action
let mut s = String::from("hello");
let r1 = &s;      // OK: first shared ref
let r2 = &s;      // OK: second shared ref
println!("{r1}, {r2}");
// r1, r2 no longer used after this point (NLL)
let r3 = &mut s;  // OK: no active shared refs
r3.push_str("!");

// Slices
let v = vec![1, 2, 3, 4, 5];
let slice: &[i32] = &v[1..3];  // [2, 3]

// String slices
let s = String::from("hello world");
let hello: &str = &s[0..5];
let world: &str = &s[6..11];

// Slice patterns
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &b) in bytes.iter().enumerate() {
        if b == b' ' {
            return &s[..i];
        }
    }
    s
}
```

```rust
// Reborrowing
fn read(r: &i32) { println!("{r}"); }

let mut x = 42;
let r = &mut x;
read(r);       // implicit reborrow: &*r
*r += 1;       // still usable as &mut
```

## Gotchas

- **Symptom**: "cannot borrow as mutable because it is also borrowed as immutable" - **Cause**: overlapping shared and mutable borrows - **Fix**: ensure shared refs are no longer used before creating `&mut`
- **Symptom**: "cannot borrow as mutable more than once" - **Cause**: two `&mut` references alive simultaneously - **Fix**: scope the first `&mut` or restructure
- **Symptom**: indexing a `String` by byte range panics - **Cause**: slicing at non-UTF-8 boundary - **Fix**: use `.chars()`, `.char_indices()`, or validate boundaries
- **Symptom**: returning a reference to a local variable - **Cause**: local is dropped, reference would dangle - **Fix**: return owned value or use [[lifetimes]]

## See Also

- [[ownership-and-move-semantics]] - ownership fundamentals
- [[lifetimes]] - explicit annotation of reference validity
- [[collections]] - `Vec`, `String`, `HashMap` and their slice views
- [The Rust Book - References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)
- [The Rust Book - Slices](https://doc.rust-lang.org/book/ch04-03-slices.html)
