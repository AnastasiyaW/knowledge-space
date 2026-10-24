---
title: "Modules et visibilité"
category: reference
tags: [rust, modules, pub, crate, visibility, use, cargo, workspaces, testing, documentation]
level: 3
source_sha256: f101800047e319c75f660356f3b910032b8fc45b1750703f11c20483262f6215
translation: machine
translated_at: '2026-10-24'
---
# Modules et visibilité {#modules-and-visibility}

Le système de modules de Rust contrôle l'organisation du code et sa visibilité. Les modules peuvent être en ligne ou basés sur des fichiers. Tout est privé par défaut ; `pub` expose des éléments au-delà des frontières des modules. Cargo gère les compilations, les dépendances, les workspaces et les tests. Le système de modules et Cargo forment ensemble l'approche de Rust en matière d'encapsulation et de structure de projet.

## Points clés {#key-facts}

- `mod my_module;` recherche `my_module.rs` ou `my_module/mod.rs`
- Tous les éléments sont **privés par défaut** : ils ne sont accessibles que dans leur module et ses sous-modules
- `pub` = public partout, `pub(crate)` = visible uniquement dans le crate, `pub(super)` = module parent, `pub(in path)` = chemin spécifique
- `use` importe des éléments dans la portée ; `pub use` réexporte (motif de façade)
- Les workspaces regroupent plusieurs crates : `Cargo.lock` et répertoire `target/` partagés
- Les éditions (2015, 2018, 2021, 2024) sont activées par crate sur option et sont interopérables

## Motifs {#patterns}

### Déclaration de module {#module-declaration}

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

### Modificateurs de visibilité {#visibility-modifiers}

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

### Réexportations (pub use) {#re-exports-pub-use}

```rust
// Flatten deep module hierarchy for users
mod internal {
    pub mod engine {
        pub fn process() {}
    }
}

pub use internal::engine::process;  // users call crate::process()
```

### L'essentiel de Cargo.toml {#cargotoml-essentials}

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

### Tests {#testing}

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

### Documentation {#documentation}

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

### Commandes Cargo {#cargo-commands}

| Commande | Rôle |
|---------|---------|
| `cargo build` | Compiler |
| `cargo run` | Compiler + exécuter |
| `cargo test` | Exécuter tous les tests |
| `cargo clippy` | Analyse statique (lint) |
| `cargo fmt` | Formatage |
| `cargo doc --open` | Générer et ouvrir la documentation |
| `cargo bench` | Benchmarks |
| `cargo expand` | Afficher le code après expansion des macros |

## Pièges {#gotchas}

- Au sein d'un même module, tous les éléments peuvent accéder les uns aux autres (y compris les éléments privés) : la confidentialité est une notion liée aux frontières des modules
- La convention `mod.rs` est plus ancienne ; `module_name.rs` au même niveau est préférée dans le Rust moderne
- `#[cfg(test)]` garantit que le code de test n'est pas compilé dans les builds de release
- Les exemples de code des tests de documentation doivent utiliser l'API publique du crate (ils s'exécutent comme des tests externes)

## Voir aussi {#see-also}

- [[structs-and-methods]] - visibilité `pub` sur les champs de structures
- [[macros]] - export et portée des macros
- [[rust-tooling]] - commandes cargo, clippy, rustfmt
