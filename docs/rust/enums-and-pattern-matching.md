---
title: Enums and Pattern Matching
category: concepts
tags: [rust, enums, match, pattern-matching, option, result, if-let, destructuring, algebraic-types]
---

# Enums and Pattern Matching

Rust enums are algebraic data types - each variant can hold different data (unit, tuple, or struct-like). Combined with exhaustive `match` expressions, they enable compile-time checked branching that catches missing cases. `Option<T>` and `Result<T, E>` are the most important enums in the standard library.

## Key Facts

- Enums define a type that can be one of several variants, each potentially carrying data
- `match` must be **exhaustive** - all variants must be handled (or use `_` wildcard)
- `match` is an **expression** - returns a value, all arms must return the same type
- `if let` / `while let` for single-variant matching without exhaustiveness
- Pattern matching works in: `match`, `if let`, `while let`, `let` bindings, function params
- Enums replace the need for null pointers, error codes, and tagged unions from C

## Patterns

### Enum Definition

```rust
// Simple C-like enum
enum Direction { North, South, East, West }

// Enum with data (algebraic data type)
enum Message {
    Quit,                         // unit variant
    Move { x: i32, y: i32 },     // struct variant
    Write(String),                // tuple variant
    ChangeColor(i32, i32, i32),   // multi-value tuple variant
}
```

### Match Expression

```rust
fn process(msg: Message) -> String {
    match msg {
        Message::Quit => "Quitting".to_string(),
        Message::Move { x, y } => format!("Moving to ({}, {})", x, y),
        Message::Write(text) => format!("Message: {}", text),
        Message::ChangeColor(r, g, b) => format!("RGB({}, {}, {})", r, g, b),
    }
}
```

### Pattern Matching Features

```rust
// Alternatives with |
Weather::Rainy | Weather::Snowy => true,

// Ranges
4..=10 => println!("Medium number"),

// Guards
x if x > 0 => println!("positive"),

// Tuple destructuring
match point {
    (0, 0) => println!("Origin"),
    (0, y) => println!("On Y axis: {}", y),
    (x, 0) => println!("On X axis: {}", x),
    (x, y) if x == y => println!("On diagonal"),
    (x, y) => println!("({}, {})", x, y),
}

// Struct destructuring in match
match person {
    Person { name, age: 0 } => println!("{} - newborn", name),
    Person { name, age } if age < 18 => println!("{} - minor", name),
    Person { name, .. } => println!("{} - adult", name),
}

// Nested enum + struct matching
match customer {
    Customer { contact: ContactMethod::Email(email), vip: true, .. } =>
        println!("VIP email: {}", email),
    Customer { contact: ContactMethod::Phone(phone), .. } =>
        println!("Calling {}", phone),
    _ => {}
}
```

### if let / while let (Single-Variant Matching)

```rust
// Instead of full match for one variant
if let Some(x) = some_value {
    println!("Value: {}", x);
}

// Loop until pattern fails
let mut stack = vec![1, 2, 3];
while let Some(value) = stack.pop() {
    println!("Popped: {}", value);
}
```

### Advanced Patterns

```rust
// Slice patterns with binding
match slice {
    [.., "!"] => println!("exclamation"),
    [start @ .., "z"] => println!("starts with: {:?}", start),
    ["a", end @ ..] => println!("ends with: {:?}", end),
    all @ [.., last] => println!("last of {:?} is {}", all, last),
    _ => {}
}

// FizzBuzz with tuple match
let s = match (x % 3, x % 5) {
    (0, 0) => String::from("FizzBuzz"),
    (0, _) => String::from("Fizz"),
    (_, 0) => String::from("Buzz"),
    _ => x.to_string(),
};

// Destructuring in function params
fn distance((x1, y1): (f64, f64), (x2, y2): (f64, f64)) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2)).sqrt()
}
```

## Gotchas

- Forgetting to handle a variant is a compile error - this is intentional and catches bugs early
- `let _ = expr` does NOT bind/move the value (unlike `let _x = expr` which does)
- Using constants instead of enums (`const STATUS: i32 = 0`) loses type safety - prefer enums
- Enum variants are namespaced: `Message::Quit`, not just `Quit` (unless you `use Message::*`)

## See Also

- [[error-handling]] - Result<T, E> and Option<T> as enum-based error handling
- [[structs-and-methods]] - struct variants inside enums
- [[traits]] - implementing traits for enums
