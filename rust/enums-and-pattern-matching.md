---
title: Enums and Pattern Matching
category: concepts
tags: [enums, match, pattern-matching, option, if-let, destructuring]
---
# Enums and Pattern Matching

Rust enums are algebraic data types (sum types) where each variant can hold different data; `match` provides exhaustive pattern matching.

## Key Facts

- Enum variants can be: unit (no data), tuple (unnamed fields), struct (named fields)
- `match` must be exhaustive - every possible value must be handled
- `match` is an expression - every arm returns the same type
- Pattern types: literal, variable binding, wildcard `_`, range `1..=5`, OR `|`, guard `if`
- `if let` / `while let` for single-pattern matching without exhaustiveness
- `let` is itself a pattern: `let (x, y) = (1, 2);`
- `Option<T>` = `Some(T) | None` - Rust's null replacement
- `@` bindings: `val @ 3..=5` captures the value while matching a pattern
- Slice patterns: `[first, .., last]`, `[a, rest @ ..]`
- Empty enum `enum Never {}` is uninhabited (like `!` type)

## Patterns

```rust
// Enum with data variants
enum Message {
    Quit,                          // unit variant
    Move { x: i32, y: i32 },      // struct variant
    Write(String),                 // tuple variant
    ChangeColor(u8, u8, u8),       // multi-field tuple
}

// Exhaustive match
fn process(msg: Message) {
    match msg {
        Message::Quit => println!("quit"),
        Message::Move { x, y } => println!("move to ({x}, {y})"),
        Message::Write(text) => println!("text: {text}"),
        Message::ChangeColor(r, g, b) => {
            println!("color: ({r}, {g}, {b})");
        }
    }
}

// Match as expression
fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(r) => std::f64::consts::PI * r * r,
        Shape::Rectangle(w, h) => w * h,
    }
}

// OR patterns and ranges
fn classify(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1 | 2 | 3 => "small",
        4..=10 => "medium",
        _ => "large",
    }
}

// Guards
fn describe(point: (i32, i32)) {
    match point {
        (0, 0) => println!("origin"),
        (x, y) if x == y => println!("on diagonal"),
        (x, 0) => println!("on x-axis at {x}"),
        (0, y) => println!("on y-axis at {y}"),
        (x, y) => println!("({x}, {y})"),
    }
}

// if let (single pattern)
let config_max: Option<u8> = Some(3);
if let Some(max) = config_max {
    println!("max is {max}");
}

// while let
let mut stack = vec![1, 2, 3];
while let Some(top) = stack.pop() {
    println!("{top}");
}

// @ bindings
match value {
    n @ 1..=12 => println!("month: {n}"),
    n => println!("invalid: {n}"),
}

// Slice patterns
match slice {
    [] => println!("empty"),
    [x] => println!("single: {x}"),
    [first, .., last] => println!("first={first}, last={last}"),
}

// Nested destructuring
struct Customer {
    name: String,
    contact: ContactMethod,
}
enum ContactMethod {
    Email(String),
    Phone(String),
}

fn notify(c: Customer) {
    match c {
        Customer { name, contact: ContactMethod::Email(email) } => {
            println!("Email {name} at {email}");
        }
        Customer { name, contact: ContactMethod::Phone(phone) } => {
            println!("Call {name} at {phone}");
        }
    }
}
```

## Gotchas

- **Symptom**: "non-exhaustive patterns" error - **Cause**: `match` missing a variant - **Fix**: add missing arms or use `_` wildcard (but prefer explicit handling)
- **Symptom**: `if let` with `else` branch - more readable with `match` when handling 2+ variants
- **Symptom**: `let _ = expr` drops immediately, `let _x = expr` binds until end of scope - **Cause**: `_` is not a binding - **Fix**: use named `_x` if you need the value to live longer (e.g., for RAII guards)
- **Symptom**: can't match on `String` directly in patterns - **Cause**: patterns require constants - **Fix**: match on `s.as_str()` or use guards

## See Also

- [[structs-and-methods]] - struct types used with enums
- [[rust/error-handling]] - `Result<T, E>` and `Option<T>` patterns
- [[traits]] - deriving traits for enums
- [The Rust Book - Enums](https://doc.rust-lang.org/book/ch06-00-enums.html)
- [The Rust Book - Patterns](https://doc.rust-lang.org/book/ch18-00-patterns.html)
- [Rust Reference - Patterns](https://doc.rust-lang.org/reference/patterns.html)
