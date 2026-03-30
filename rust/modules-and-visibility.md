---
title: Modules and Visibility
category: reference
tags: [modules, pub, crate, visibility, use, re-export, cargo]
---
# Modules and Visibility

Modules organize code into namespaces with fine-grained visibility control; Cargo manages project structure and dependencies.

## Key Facts

- `mod name { }` declares an inline module; `mod name;` loads from `name.rs` or `name/mod.rs`
- Everything is private by default; `pub` makes items accessible to parent modules
- Visibility modifiers: `pub` (public), `pub(crate)` (crate-wide), `pub(super)` (parent module), `pub(in path)` (specific module)
- `use` imports items into scope; `pub use` re-exports for external consumers
- Crate root: `src/lib.rs` (library) or `src/main.rs` (binary)
- `crate::` prefix for absolute paths within the crate; `self::` for current module; `super::` for parent
- `Cargo.toml` defines package metadata, dependencies, features, build profiles
- Workspace: multiple related packages in one repo via `[workspace]` in root `Cargo.toml`
- `tests/` directory for integration tests; `examples/` for example binaries; `benches/` for benchmarks

## Patterns

```rust
// Module declaration
mod math {
    pub fn add(a: i32, b: i32) -> i32 { a + b }
    fn internal_helper() -> i32 { 42 } // private

    pub mod advanced {
        pub fn factorial(n: u64) -> u64 {
            (1..=n).product()
        }
    }
}

// Using modules
use math::add;
use math::advanced::factorial;
let sum = add(1, 2);
let fact = factorial(5);

// Visibility modifiers
pub mod outer {
    pub mod inner {
        pub(in crate::outer) fn outer_visible() {}
        pub(crate) fn crate_visible() {}
        pub(super) fn parent_visible() {}
        pub(self) fn self_visible() {}  // same as private
    }

    pub fn demo() {
        inner::outer_visible();  // OK
        inner::crate_visible();  // OK
        inner::parent_visible(); // OK
        // inner::self_visible(); // ERROR
    }
}

// Re-exporting
pub mod api {
    mod implementation {
        pub fn process() -> String {
            "done".to_string()
        }
    }
    pub use implementation::process;  // flatten the API
}
// Users call: api::process() instead of api::implementation::process()

// File structure
// src/
//   main.rs          or lib.rs
//   config.rs        -> mod config;
//   network/
//     mod.rs          -> mod network;
//     tcp.rs          -> mod tcp; (inside network/mod.rs)
//     udp.rs          -> mod udp;

// Cargo.toml essentials
// [package]
// name = "my-project"
// version = "0.1.0"
// edition = "2024"
//
// [dependencies]
// serde = { version = "1.0", features = ["derive"] }
// tokio = { version = "1", features = ["full"] }
//
// [dev-dependencies]
// criterion = "0.5"
//
// [[bin]]
// name = "server"
// path = "src/bin/server.rs"

// Tests alongside code
#[cfg(test)]
mod tests {
    use super::*;  // import parent module items

    #[test]
    fn test_add() {
        assert_eq!(math::add(2, 3), 5);
    }
}

// Doc comments (generate with cargo doc)
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 { a + b }
```

```toml
# Cargo workspace
# root Cargo.toml
[workspace]
members = ["core", "cli", "web"]
```

## Gotchas

- **Symptom**: "unresolved import" - **Cause**: module not declared with `mod` or wrong path - **Fix**: ensure `mod name;` appears in parent module, file exists at correct path
- **Symptom**: "function is private" - **Cause**: missing `pub` on item or enclosing module - **Fix**: add `pub` at each level in the path that needs to be accessible
- **Symptom**: struct is `pub` but fields are still private - **Cause**: struct visibility doesn't imply field visibility - **Fix**: mark individual fields as `pub`, or provide constructor
- **Symptom**: confusion between `mod.rs` and `name.rs` - **Cause**: two file layout conventions - **Fix**: Rust 2018+ prefers `name.rs` + `name/` directory over `name/mod.rs`

## See Also

- [[structs-and-methods]] - visibility of struct fields
- [[traits]] - trait visibility and orphan rules
- [[rust/error-handling]] - organizing error types across modules
- [The Rust Book - Modules](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
