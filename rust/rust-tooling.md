---
title: Rust Tooling and Project Setup
category: reference
tags: [cargo, rustup, clippy, rustfmt, toolchain, testing, documentation]
---
# Rust Tooling and Project Setup

Core tools for Rust development: `rustup` for toolchain management, `cargo` for build/test/dependency management, plus linters, formatters, and testing infrastructure.

## Key Facts

- `rustup` manages Rust installations: stable/beta/nightly channels, components, targets
- `cargo` is the build system AND package manager: build, test, run, publish, manage dependencies
- Toolchain components: `rustc` (compiler), `cargo`, `rustfmt` (formatter), `clippy` (linter), `rust-analyzer` (LSP), `rust-docs`
- Editions: 2015, 2018, 2021, 2024 - opt-in language evolution without breaking compatibility
- Cargo commands: `new`, `build`, `run`, `test`, `bench`, `doc`, `clippy`, `fmt`, `add`, `update`
- `Cargo.toml` - project manifest (dependencies, features, profiles)
- `Cargo.lock` - exact dependency versions (committed for binaries, not for libraries)
- Testing: `#[test]` for unit tests, `tests/` for integration, doc tests in `///` comments
- `cargo doc --open` generates and opens HTML documentation

## Patterns

```bash
# Installation
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Verify installation
rustup --version
rustc --version
cargo --version

# Add components
rustup component add rustfmt clippy rust-analyzer

# Create project
cargo new my_project        # binary
cargo new my_lib --lib       # library
cd my_project
cargo run                    # build and run

# Build modes
cargo build                  # debug (fast compile, slow runtime)
cargo build --release        # optimized (slow compile, fast runtime)

# Testing
cargo test                   # run all tests
cargo test test_name         # run specific test
cargo test -- --nocapture    # show println output
cargo test --lib             # unit tests only
cargo test --test integration_test  # specific integration test

# Linting and formatting
cargo fmt                    # format code
cargo fmt --check            # check without modifying
cargo clippy                 # lint with suggestions
cargo clippy -- -W clippy::pedantic  # stricter lints

# Documentation
cargo doc --open             # generate and open docs
```

```toml
# Cargo.toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2024"
authors = ["Name <email>"]
description = "Short description"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1.0"
thiserror = "2.0"

[dev-dependencies]
criterion = "0.5"
tempfile = "3"

[features]
default = ["logging"]
logging = ["dep:tracing"]
full = ["logging", "metrics"]

[profile.release]
opt-level = 3
lto = true
```

```rust
// Unit tests (alongside code)
pub fn add(a: i32, b: i32) -> i32 { a + b }

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
        panic!("overflow");
    }

    #[test]
    fn test_result() -> Result<(), String> {
        if add(2, 2) == 4 {
            Ok(())
        } else {
            Err("math is broken".to_string())
        }
    }

    #[ignore]
    #[test]
    fn expensive_test() {
        // run with: cargo test -- --ignored
    }
}

// Doc tests (in documentation comments)
/// Multiplies two numbers.
///
/// # Examples
///
/// ```
/// assert_eq!(my_crate::multiply(3, 4), 12);
/// ```
///
/// # Panics
///
/// Panics if overflow occurs in debug mode.
pub fn multiply(a: i32, b: i32) -> i32 { a * b }

// Integration tests (tests/integration_test.rs)
// use my_crate::add;
// #[test]
// fn integration_add() {
//     assert_eq!(add(10, 20), 30);
// }
```

## Gotchas

- **Symptom**: "found incompatible edition" - **Cause**: crate uses features from newer edition - **Fix**: update `edition` in `Cargo.toml`
- **Symptom**: `cargo clippy` and `cargo fmt --check` produce warnings - **Cause**: style/correctness issues - **Fix**: run `cargo fmt` to fix formatting; address clippy suggestions (they're usually right)
- **Symptom**: dependency conflict / duplicate versions - **Cause**: transitive dependencies require different versions - **Fix**: `cargo update`, check `Cargo.lock`, use `cargo tree` to inspect dependency graph
- **Symptom**: tests can't access private functions - **Cause**: integration tests are external - **Fix**: unit tests in `#[cfg(test)]` mod inside the file can access private items; integration tests can only test public API

## See Also

- [[modules-and-visibility]] - project structure and `mod` system
- [[macros]] - `#[cfg(test)]` and `#[derive()]`
- [[rust/error-handling]] - `Result`-returning tests
- [The Rust Book - Getting Started](https://doc.rust-lang.org/book/ch01-00-getting-started.html)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
- [Clippy Lints](https://rust-lang.github.io/rust-clippy/master/)
