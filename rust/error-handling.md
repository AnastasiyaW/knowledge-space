---
title: Error Handling
category: patterns
tags: [result, option, error, question-mark, panic, thiserror, anyhow]
---
# Error Handling

Rust uses `Result<T, E>` and `Option<T>` for recoverable errors, and `panic!` for unrecoverable ones - no exceptions.

## Key Facts

- `Result<T, E>` = `Ok(T)` | `Err(E)` for operations that can fail
- `Option<T>` = `Some(T)` | `None` for values that may be absent
- `?` operator: early-returns `Err` (or `None`), unwraps on success; works in functions returning `Result`/`Option`
- `unwrap()` / `expect("msg")` - panic on `Err`/`None`; use only in prototypes/tests
- `map`, `and_then`, `unwrap_or`, `unwrap_or_else` for functional chaining
- Custom errors: implement `std::error::Error` + `Display` + `Debug`
- Crates: `thiserror` for library errors (derive macro), `anyhow` for application errors (type-erased)
- `From` trait enables automatic error conversion with `?`
- `panic!` is for bugs, not expected errors; unwinds by default, can be set to abort

## Patterns

```rust
// Basic Result usage
use std::fs;
use std::io;

fn read_username() -> Result<String, io::Error> {
    let s = fs::read_to_string("username.txt")?;
    Ok(s.trim().to_string())
}

// Chaining with combinators
fn first_line(filename: &str) -> Option<String> {
    fs::read_to_string(filename)
        .ok()?                          // Result -> Option
        .lines()
        .next()
        .map(String::from)
}

// Option combinators
let port: u16 = std::env::var("PORT")
    .ok()                               // Result -> Option
    .and_then(|s| s.parse().ok())       // parse, convert error
    .unwrap_or(8080);                   // default

// Custom error type
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    NotFound(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::Io(e) => write!(f, "IO error: {e}"),
            AppError::Parse(e) => write!(f, "Parse error: {e}"),
            AppError::NotFound(s) => write!(f, "Not found: {s}"),
        }
    }
}

impl std::error::Error for AppError {}

// From implementations enable ? conversion
impl From<io::Error> for AppError {
    fn from(e: io::Error) -> Self { AppError::Io(e) }
}
impl From<std::num::ParseIntError> for AppError {
    fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }
}

fn process() -> Result<i32, AppError> {
    let content = fs::read_to_string("data.txt")?;  // io::Error -> AppError
    let value: i32 = content.trim().parse()?;        // ParseIntError -> AppError
    Ok(value * 2)
}

// With thiserror crate
// use thiserror::Error;
// #[derive(Error, Debug)]
// enum AppError {
//     #[error("IO error: {0}")]
//     Io(#[from] io::Error),
//     #[error("Parse error: {0}")]
//     Parse(#[from] std::num::ParseIntError),
//     #[error("Not found: {0}")]
//     NotFound(String),
// }

// With anyhow crate
// use anyhow::{Context, Result};
// fn load_config() -> Result<Config> {
//     let s = fs::read_to_string("config.toml")
//         .context("Failed to read config file")?;
//     toml::from_str(&s)
//         .context("Failed to parse config")
// }

// Result methods summary
let r: Result<i32, &str> = Ok(42);
r.unwrap();                    // 42 or panic
r.expect("must work");         // 42 or panic with message
r.unwrap_or(0);                // 42 or default
r.unwrap_or_else(|_| 0);      // 42 or compute default
r.map(|v| v * 2);             // Ok(84)
r.and_then(|v| Ok(v + 1));    // Ok(43)
r.is_ok();                     // true
r.is_err();                    // false
r.ok();                        // Some(42)
```

## Gotchas

- **Symptom**: "the `?` operator can only be used in a function that returns `Result` or `Option`" - **Cause**: `main()` or closure doesn't return `Result` - **Fix**: change return type to `Result<(), Box<dyn std::error::Error>>` or use `anyhow::Result<()>`
- **Symptom**: can't use `?` to convert between `Option` and `Result` - **Cause**: they are different types - **Fix**: use `.ok_or("error msg")?` to convert `Option` to `Result`, `.ok()?` for the reverse
- **Symptom**: `unwrap()` panics in production - **Cause**: used `unwrap()` on a path that can fail - **Fix**: replace with `?`, `match`, or `.unwrap_or_default()`
- **Symptom**: error types don't compose with `?` - **Cause**: no `From` impl between error types - **Fix**: implement `From`, use `thiserror`'s `#[from]`, or `anyhow`

## See Also

- [[enums-and-pattern-matching]] - `match` on `Result`/`Option`
- [[traits]] - `Error`, `Display`, `From` traits
- [[closures]] - combinators like `map`, `and_then`
- [The Rust Book - Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [thiserror crate](https://docs.rs/thiserror)
- [anyhow crate](https://docs.rs/anyhow)
