---
title: Error Handling
category: patterns
tags: [rust, error-handling, result, option, panic, question-mark, thiserror, anyhow]
---

# Error Handling

Rust uses `Result<T, E>` and `Option<T>` for recoverable errors and absent values, with `panic!` for unrecoverable situations. The `?` operator enables ergonomic error propagation, and the type system ensures all error paths are handled at compile time.

## Key Facts

- `Option<T>` = value either exists (`Some(T)`) or doesn't (`None`)
- `Result<T, E>` = either success (`Ok(T)`) or error (`Err(E)`)
- `?` operator = early return on `None`/`Err`, unwrap on `Some`/`Ok`
- `panic!` terminates the thread (unwind or abort depending on config)
- `unwrap()` panics on `None`/`Err` - avoid in production, useful in tests/prototypes
- `thiserror` crate for library error types, `anyhow` for application error handling

## Patterns

### Option Combinators

```rust
let name: Option<String> = Some("Alice".to_string());

// map: transform inner value
let upper = name.as_ref().map(|n| n.to_uppercase());

// and_then: chain operations that return Option
let first_char = name.as_ref().and_then(|n| n.chars().next());

// unwrap_or: provide default
let display = name.unwrap_or_else(|| "Anonymous".to_string());

// Sum two Options
let sum = a.and_then(|x| b.map(|y| x + y));
```

### Result and ? Operator

```rust
use std::fs;
use std::io;

fn read_username() -> Result<String, io::Error> {
    let content = fs::read_to_string("username.txt")?;  // ? = early return on Err
    Ok(content.trim().to_string())
}

// Chaining with ?
fn process() -> Result<i32, String> {
    let num: i32 = "42".parse().map_err(|e| format!("Parse error: {e}"))?;
    Ok(num * 2)
}
```

### Custom Error Types

```rust
#[derive(Debug)]
enum AppError {
    NotFound(String),
    PermissionDenied,
    DatabaseError(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "Not found: {msg}"),
            AppError::PermissionDenied => write!(f, "Permission denied"),
            AppError::DatabaseError(msg) => write!(f, "DB error: {msg}"),
        }
    }
}

impl std::error::Error for AppError {}
```

### Pattern Matching on Results

```rust
match fs::read_to_string("config.toml") {
    Ok(content) => println!("Config: {content}"),
    Err(e) if e.kind() == io::ErrorKind::NotFound => {
        println!("Using defaults");
    }
    Err(e) => return Err(e.into()),
}
```

## Gotchas

- `unwrap()` in library code is a code smell - always propagate errors with `?` or handle explicitly
- `?` requires the function to return `Result` or `Option` - cannot use in `main()` without `-> Result<(), Box<dyn Error>>`
- Converting between error types: implement `From<OriginalError> for YourError` to enable `?` across error types

## See Also

- [[enums-and-pattern-matching]] - enum-based error types, exhaustive matching
- [[traits]] - Error trait, From trait for error conversion
- [[closures]] - closures with Result/Option combinators
