---
title: Modules and Visibility
category: reference
tags: [rust, modules, pub, crate, visibility, use, cargo, workspaces, testing, documentation]
---

# Modules and Visibility

Rust's module system controls code organization and visibility. Modules can be inline or file-based. Everything is private by default; `pub` exposes items across module boundaries. Cargo manages builds, dependencies, workspaces, and testing. The module system + Cargo together form Rust's approach to encapsulation and project structure.

## Key Facts

- `mod my_module;` looks for `my_module.rs` or `my_module/mod.rs`
- All items are **private by default** - only accessible within their module and its children
- `pub` = public everywhere, `pub(crate)` = crate-only, `pub(super)` = parent module, `pub(in path)` = specific path
- `use` imports items into scope; `pub use` re-exports (facade pattern)
- Workspaces group multiple crates: shared `Cargo.lock`, shared `target/` directory
- Editions (2015, 2018, 2021, 2024) are opt-in per crate and interoperable

## Patterns

### Module Declaration

```rust
// Inline module
mod math {
    pub fn add(a: i32, b: i32) -> i32 { a + b }
    fn helper() { /* private */ }
}

// File-based module (two conventions)
// Option A: src/math.rs
// Option B: src/math/mod.rs (for modules with submodules)
mod math;  // in main.rs or lib.rs
```

### Visibility Modifiers

```rust
pub mod outer {
    pub mod inner {
        pub(in crate::outer) fn outer_visible() {}   // visible in outer
        pub(crate) fn crate_visible() {}               // visible in crate
        pub(super) fn parent_visible() {}              // visible in outer
        fn private() {}                                 // visible in inner only
    }
}
```

### Re-exports (pub use)

```rust
// Flatten deep module hierarchy for users
mod internal {
    pub mod engine {
        pub fn process() {}
    }
}

pub use internal::engine::process;  // users call crate::process()
```

### Cargo.toml Essentials

```toml
[package]
name = "my_project"
version = "0.1.0"
edition = "2024"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
criterion = "0.5"

[workspace]
members = ["library", "cli", "server"]
```

### Testing

```rust
// Unit tests: inline, next to code
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn test_overflow() {
        add(i32::MAX, 1);
    }
}

// Integration tests: tests/ directory (separate crate)
// Doc tests: code in /// comments runs as tests
```

### Documentation

```rust
/// Adds two numbers.
///
/// # Examples
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 { a + b }

//! Module-level documentation (at top of file)
```

### Cargo Commands

| Command | Purpose |
|---------|---------|
| `cargo build` | Compile |
| `cargo run` | Build + run |
| `cargo test` | Run all tests |
| `cargo clippy` | Lint |
| `cargo fmt` | Format |
| `cargo doc --open` | Generate + open docs |
| `cargo bench` | Benchmarks |
| `cargo expand` | Show macro-expanded code |

## Gotchas

- Within the same module, all items can access each other (even private ones) - privacy is a module-boundary concept
- `mod.rs` convention is older; `module_name.rs` at the same level is preferred in modern Rust
- `#[cfg(test)]` ensures test code is not compiled in release builds
- Doc test code examples must use the crate's public API (they run as external tests)

## See Also

- [[structs-and-methods]] - pub visibility on struct fields
- [[macros]] - macro export and scoping
- [[rust-tooling]] - cargo commands, clippy, rustfmt
