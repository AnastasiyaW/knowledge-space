---
title: Rust Tooling and Ecosystem
category: reference
tags: [rust, cargo, clippy, rustfmt, serde, tokio, rayon, ffi, profiling, wasm, web-frameworks]
---

# Rust Tooling and Ecosystem

Rust ships with a unified toolchain: cargo (build/deps/test), clippy (lint), rustfmt (format), rustdoc (docs). The ecosystem provides battle-tested crates for serialization (serde), async (tokio), parallelism (rayon), web (actix-web, axum), and FFI. Rust also compiles to WebAssembly for browser/frontend use.

## Key Facts

- **cargo** = build system + package manager + test runner + benchmark runner
- **clippy** = linter with 500+ lints, catches common mistakes and unidiomatic code
- **rustfmt** = opinionated formatter, enforces consistent style
- **serde** = most-used crate, serialization framework (JSON, TOML, YAML, MessagePack, etc.)
- **tokio** = dominant async runtime; **rayon** = data parallelism with parallel iterators
- **FFI**: `extern "C"` + `#[no_mangle]` to expose Rust to C; `extern "C" { }` to call C from Rust
- Editions (2015, 2018, 2021, 2024) are backward-compatible and interoperable

## Essential Crates

### Serialization - serde

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Config {
    name: String,
    port: u16,
    #[serde(default)]
    debug: bool,
}

let json = serde_json::to_string(&config)?;
let config: Config = serde_json::from_str(&json)?;
```

### Data Parallelism - rayon

```rust
use rayon::prelude::*;

let sum: i32 = (0..1_000_000)
    .into_par_iter()
    .map(|x| x * x)
    .sum();
// Automatically distributes across CPU cores (work-stealing)
```

### Structured Logging - tracing

```rust
use tracing::{info, warn, span, Level};

#[tracing::instrument]
fn process_request(id: u64) {
    info!(id, "Processing request");
    // Auto-creates span with function name + args
}
```

### Other Key Crates

| Crate | Purpose |
|-------|---------|
| `tokio` | Async runtime |
| `reqwest` | HTTP client |
| `sqlx` | Async SQL (compile-time checked queries) |
| `clap` | CLI argument parsing |
| `regex` | Regular expressions |
| `chrono` | Date/time |
| `uuid` | UUID generation |
| `itertools` | Extra iterator adaptors |
| `anyhow` / `thiserror` | Error handling (app / library) |

## FFI (Foreign Function Interface)

```rust
// Calling C from Rust
extern "C" {
    fn abs(input: i32) -> i32;
}
unsafe { abs(-5); }  // all FFI calls are unsafe

// Exposing Rust to C
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 { a + b }

// Struct compatibility
#[repr(C)]
struct Point { x: f64, y: f64 }
```

Library types in Cargo.toml:
- `cdylib`: C-compatible dynamic library (.so/.dll)
- `staticlib`: static library (.a/.lib)
- `rlib`: Rust library (default)

## Web Development

### Backend Frameworks

| Framework | Style | Notes |
|-----------|-------|-------|
| **actix-web** | Service-based | Fastest, TechEmpower top, higher learning curve |
| **axum** | Tower-based | Official Tokio team, simpler, type-safe extractors |
| **tonic** | gRPC | HTTP/2 + Protobuf, service-to-service |
| **async-graphql** | GraphQL | Client selects fields, N+1 problem needs batching |

### Frontend (WebAssembly)

| Framework | Style |
|-----------|-------|
| **Leptos** | Reactive, SSR support, fine-grained reactivity |
| **Dioxus** | React-like, web/desktop/mobile |
| **Yew** | Component-based, similar to React |

Tooling: `wasm-pack` (build), `trunk` (dev server), `wasm-bindgen` (JS interop)

## Debugging and Profiling

```rust
// dbg! macro - prints file:line, expression, value
let x = dbg!(5 * 2);  // [src/main.rs:1] 5 * 2 = 10

// Pretty-print debug
println!("{:#?}", complex_struct);
```

- **flamegraph**: `cargo flamegraph --bin my_app` - SVG flamegraph of execution time
- **CodeLLDB** / GDB for step-by-step debugging

## Gotchas

- All FFI calls are `unsafe` - Rust cannot verify C code's safety
- `#[repr(C)]` required on structs passed across FFI boundary (Rust struct layout is unspecified)
- `CString`/`CStr` for FFI string conversion, not `String`/`&str` (C strings are null-terminated)
- `bindgen` auto-generates Rust bindings from C headers: `bindgen wrapper.h -o bindings.rs`

## See Also

- [[modules-and-visibility]] - cargo project structure, workspaces, testing
- [[async-await]] - tokio runtime details
- [[concurrency]] - rayon vs threads vs async
- [[macros]] - cargo expand for macro debugging
