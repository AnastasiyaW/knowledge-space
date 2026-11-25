---
title: "Rust-Werkzeuge und Ökosystem"
category: reference
tags: [rust, cargo, clippy, rustfmt, serde, tokio, rayon, ffi, profiling, wasm, web-frameworks]
level: 4
source_sha256: 751a2c7d7a31530fad21ebeb13f4fe80de7698ea2dc2452e58a147f5c4e165b6
translation: machine
translated_at: '2026-10-24'
---
# Rust-Werkzeuge und Ökosystem {#rust-tooling-and-ecosystem}

Rust bringt eine einheitliche Toolchain mit: cargo (Build/Abhängigkeiten/Tests), clippy (Linting), rustfmt (Formatierung), rustdoc (Dokumentation). Das Ökosystem stellt bewährte Crates für Serialisierung (serde), Async (tokio), Parallelität (rayon), Web (actix-web, axum) und FFI bereit. Rust kann außerdem nach WebAssembly kompiliert werden, für den Einsatz im Browser bzw. im Frontend.

## Wichtige Fakten {#key-facts}

- **cargo** = Build-System + Paketmanager + Testrunner + Benchmark-Runner
- **clippy** = Linter mit über 500 Lints, erkennt häufige Fehler und unidiomatischen Code
- **rustfmt** = meinungsstarker Formatter, erzwingt einen einheitlichen Stil
- **serde** = meistgenutztes Crate, Serialisierungs-Framework (JSON, TOML, YAML, MessagePack usw.)
- **tokio** = dominierende Async-Runtime; **rayon** = Datenparallelität mit parallelen Iteratoren
- **FFI**: `extern "C"` + `#[no_mangle]`, um Rust für C verfügbar zu machen; `extern "C" { }`, um aus Rust C-Funktionen aufzurufen
- Editionen (2015, 2018, 2021, 2024) sind abwärtskompatibel und miteinander interoperabel

## Wesentliche Crates {#essential-crates}

### Serialisierung - serde {#serialization-serde}

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

### Datenparallelität - rayon {#data-parallelism-rayon}

```rust
use rayon::prelude::*;

let sum: i32 = (0..1_000_000)
    .into_par_iter()
    .map(|x| x * x)
    .sum();
// Automatically distributes across CPU cores (work-stealing)
```

### Strukturiertes Logging - tracing {#structured-logging-tracing}

```rust
use tracing::{info, warn, span, Level};

#[tracing::instrument]
fn process_request(id: u64) {
    info!(id, "Processing request");
    // Auto-creates span with function name + args
}
```

### Weitere wichtige Crates {#other-key-crates}

| Crate | Zweck |
|-------|-------|
| `tokio` | Async-Runtime |
| `reqwest` | HTTP-Client |
| `sqlx` | Async SQL (zur Compile-Zeit geprüfte Abfragen) |
| `clap` | Parsen von CLI-Argumenten |
| `regex` | Reguläre Ausdrücke |
| `chrono` | Datum/Uhrzeit |
| `uuid` | UUID-Erzeugung |
| `itertools` | Zusätzliche Iterator-Adaptoren |
| `anyhow` / `thiserror` | Fehlerbehandlung (Anwendung / Bibliothek) |

## FFI (Foreign Function Interface) {#ffi-foreign-function-interface}

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

Bibliothekstypen in Cargo.toml:
- `cdylib`: C-kompatible dynamische Bibliothek (.so/.dll)
- `staticlib`: statische Bibliothek (.a/.lib)
- `rlib`: Rust-Bibliothek (Standard)

## Webentwicklung {#web-development}

### Backend-Frameworks {#backend-frameworks}

| Framework | Stil | Hinweise |
|-----------|------|----------|
| **actix-web** | Service-basiert | Schnellstes, an der Spitze von TechEmpower, höhere Einstiegshürde |
| **axum** | Tower-basiert | Vom offiziellen Tokio-Team, einfacher, typsichere Extraktoren |
| **tonic** | gRPC | HTTP/2 + Protobuf, Service-zu-Service-Kommunikation |
| **async-graphql** | GraphQL | Client wählt Felder aus, N+1-Problem erfordert Batching |

### Frontend (WebAssembly) {#frontend-webassembly}

| Framework | Stil |
|-----------|------|
| **Leptos** | Reaktiv, SSR-Unterstützung, feingranulare Reaktivität |
| **Dioxus** | React-ähnlich, Web/Desktop/Mobil |
| **Yew** | Komponentenbasiert, ähnlich wie React |

Werkzeuge: `wasm-pack` (Build), `trunk` (Entwicklungsserver), `wasm-bindgen` (JS-Interop)

## Debugging und Profiling {#debugging-and-profiling}

```rust
// dbg! macro - prints file:line, expression, value
let x = dbg!(5 * 2);  // [src/main.rs:1] 5 * 2 = 10

// Pretty-print debug
println!("{:#?}", complex_struct);
```

- **flamegraph**: `cargo flamegraph --bin my_app` - SVG-Flamegraph der Ausführungszeit
- **CodeLLDB** / GDB für schrittweises Debugging

## Fallstricke {#gotchas}

- Alle FFI-Aufrufe sind `unsafe` - Rust kann die Sicherheit von C-Code nicht überprüfen
- `#[repr(C)]` ist erforderlich für Structs, die über eine FFI-Grenze übergeben werden (das Speicherlayout von Rust-Structs ist nicht spezifiziert)
- Für die FFI-Stringkonvertierung `CString`/`CStr` verwenden, nicht `String`/`&str` (C-Strings sind null-terminiert)
- `bindgen` erzeugt Rust-Bindings automatisch aus C-Headern: `bindgen wrapper.h -o bindings.rs`

## Siehe auch {#see-also}

- [[modules-and-visibility]] - cargo-Projektstruktur, Workspaces, Tests
- [[async-await]] - Details zur tokio-Runtime
- [Concurrency](concurrency.md) - rayon vs. Threads vs. Async
- [[macros]] - cargo expand zum Debuggen von Makros
