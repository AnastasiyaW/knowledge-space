---
title: "Outils Rust et écosystème"
category: reference
tags: [rust, cargo, clippy, rustfmt, serde, tokio, rayon, ffi, profiling, wasm, web-frameworks]
level: 4
source_sha256: 751a2c7d7a31530fad21ebeb13f4fe80de7698ea2dc2452e58a147f5c4e165b6
translation: machine
translated_at: '2026-10-24'
---
# Outils Rust et écosystème {#rust-tooling-and-ecosystem}

Rust est livré avec une chaîne d'outils unifiée : cargo (compilation, dépendances, tests), clippy (lint), rustfmt (formatage), rustdoc (documentation). L'écosystème fournit des crates éprouvées pour la sérialisation (serde), l'asynchrone (tokio), le parallélisme (rayon), le web (actix-web, axum) et le FFI. Rust se compile également en WebAssembly pour un usage dans le navigateur et le frontend.

## Points clés {#key-facts}

- **cargo** = système de build + gestionnaire de paquets + exécuteur de tests + exécuteur de benchmarks
- **clippy** = linter avec plus de 500 lints, détecte les erreurs courantes et le code non idiomatique
- **rustfmt** = formateur à parti pris, impose un style cohérent
- **serde** = crate la plus utilisée, framework de sérialisation (JSON, TOML, YAML, MessagePack, etc.)
- **tokio** = runtime asynchrone dominant ; **rayon** = parallélisme de données avec des itérateurs parallèles
- **FFI** : `extern "C"` + `#[no_mangle]` pour exposer Rust au C ; `extern "C" { }` pour appeler du C depuis Rust
- Les éditions (2015, 2018, 2021, 2024) sont rétrocompatibles et interopérables

## Crates essentielles {#essential-crates}

### Sérialisation - serde {#serialization-serde}

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

### Parallélisme de données - rayon {#data-parallelism-rayon}

```rust
use rayon::prelude::*;

let sum: i32 = (0..1_000_000)
    .into_par_iter()
    .map(|x| x * x)
    .sum();
// Automatically distributes across CPU cores (work-stealing)
```

### Journalisation structurée - tracing {#structured-logging-tracing}

```rust
use tracing::{info, warn, span, Level};

#[tracing::instrument]
fn process_request(id: u64) {
    info!(id, "Processing request");
    // Auto-creates span with function name + args
}
```

### Autres crates clés {#other-key-crates}

| Crate | Rôle |
|-------|---------|
| `tokio` | Runtime asynchrone |
| `reqwest` | Client HTTP |
| `sqlx` | SQL asynchrone (requêtes vérifiées à la compilation) |
| `clap` | Analyse des arguments de la CLI |
| `regex` | Expressions régulières |
| `chrono` | Date/heure |
| `uuid` | Génération d'UUID |
| `itertools` | Adaptateurs d'itérateurs supplémentaires |
| `anyhow` / `thiserror` | Gestion des erreurs (application / bibliothèque) |

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

Types de bibliothèques dans Cargo.toml :
- `cdylib` : bibliothèque dynamique compatible C (.so/.dll)
- `staticlib` : bibliothèque statique (.a/.lib)
- `rlib` : bibliothèque Rust (par défaut)

## Développement web {#web-development}

### Frameworks backend {#backend-frameworks}

| Framework | Style | Remarques |
|-----------|-------|-------|
| **actix-web** | Basé sur des services | Le plus rapide, en tête de TechEmpower, courbe d'apprentissage plus raide |
| **axum** | Basé sur Tower | Développé par l'équipe officielle de Tokio, plus simple, extracteurs typés |
| **tonic** | gRPC | HTTP/2 + Protobuf, communication entre services |
| **async-graphql** | GraphQL | Le client sélectionne les champs, le problème N+1 nécessite du batching |

### Frontend (WebAssembly) {#frontend-webassembly}

| Framework | Style |
|-----------|-------|
| **Leptos** | Réactif, prise en charge du SSR, réactivité fine |
| **Dioxus** | Proche de React, web/bureau/mobile |
| **Yew** | Basé sur des composants, similaire à React |

Outillage : `wasm-pack` (build), `trunk` (serveur de développement), `wasm-bindgen` (interopérabilité avec JS)

## Débogage et profilage {#debugging-and-profiling}

```rust
// dbg! macro - prints file:line, expression, value
let x = dbg!(5 * 2);  // [src/main.rs:1] 5 * 2 = 10

// Pretty-print debug
println!("{:#?}", complex_struct);
```

- **flamegraph** : `cargo flamegraph --bin my_app` - flamegraph SVG du temps d'exécution
- **CodeLLDB** / GDB pour le débogage pas à pas

## Pièges à éviter {#gotchas}

- Tous les appels FFI sont `unsafe` : Rust ne peut pas vérifier la sûreté du code C
- `#[repr(C)]` est requis sur les structures passées à travers la frontière FFI (la disposition en mémoire d'une struct Rust n'est pas spécifiée)
- Utiliser `CString`/`CStr` pour la conversion de chaînes avec le FFI, et non `String`/`&str` (les chaînes C sont terminées par un caractère nul)
- `bindgen` génère automatiquement des liaisons Rust à partir d'en-têtes C : `bindgen wrapper.h -o bindings.rs`

## Voir aussi {#see-also}

- [[modules-and-visibility]] - structure de projet cargo, workspaces, tests
- [[async-await]] - détails du runtime tokio
- [Concurrence](concurrency.md) - rayon vs threads vs asynchrone
- [[macros]] - cargo expand pour le débogage des macros
