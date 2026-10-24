---
title: "Rust-Wissensdatenbank"
category: index
tags: [rust, systems-programming, memory-safety]
level: 3
source_sha256: bbe81ad18e40ac6f1a776110a2f3072b57b9bdaf5926b303080913979b166596
translation: machine
translated_at: '2026-10-24'
---
# Rust {#rust}

Systemprogrammiersprache mit Speichersicherheit zur Kompilierzeit, Zero-Cost-Abstraktionen und furchtloser Nebenläufigkeit. Kein Garbage Collector - Ownership und Borrowing erzwingen Sicherheit zur Kompilierzeit.

## Ownership und Speicher {#ownership-and-memory}

- [[ownership-and-move-semantics]] - Ownership-Regeln, RAII, Move-Semantik, Copy/Clone
- [[borrowing-and-references]] - Borrow-Regeln, gemeinsame/mutable Referenzen, Slices, NLL
- [[lifetimes]] - Lifetime-Annotationen, Elision-Regeln, 'static, Interior Mutability
- [Smart Pointers](smart-pointers.md) - Box, Rc, Arc, RefCell, Cow, Interior Mutability

## Typsystem {#type-system}

- [[structs-and-methods]] - drei Struct-Arten, impl-Blöcke, Sichtbarkeit, Newtype-Muster
- [[enums-and-pattern-matching]] - algebraische Typen, match, if let, Destrukturierung
- [[traits]] - Trait-Bounds, Default-Implementierungen, Operator-Overloading, Orphan Rule
- [[generics-and-monomorphization]] - Typparameter, impl Trait, Turbofish, statische Dispatch
- [[dynamic-dispatch]] - dyn Trait, Vtables, Object Safety, dyn Any

## Funktionale Muster {#functional-patterns}

- [[closures]] - Fn/FnMut/FnOnce, Captures, move, Rückgabe von Closures
- [[iterators]] - Iterator-Trait, Lazy Evaluation, Adaptoren, eigene Iteratoren
- [[collections]] - Vec, HashMap, BTreeMap, String, Big-O-Komplexität

## Nebenläufigkeit und Async {#concurrency-and-async}

- [Concurrency](concurrency.md) - Threads, Send/Sync, Arc+Mutex, Channels, RwLock
- [[async-await]] - tokio, futures, select, Streams, Pin

## Fehlerbehandlung {#error-handling}

- [Error Handling](error-handling.md) - Result, Option, ?-Operator, anyhow/thiserror, eigene Fehlertypen

## Sprachmerkmale {#language-features}

- [[macros]] - deklarative (macro_rules!) und prozedurale Makros, Derive, syn/quote
- [[modules-and-visibility]] - mod, pub, use, Cargo.toml, Workspaces, Testing, Dokumentation

## Werkzeuge und Ökosystem {#tooling-and-ecosystem}

- [[rust-tooling]] - cargo, clippy, serde, rayon, FFI, Web-Frameworks, WebAssembly, Profiling

## Weitere Referenzen {#additional-references}

- [[interior-mutability]] - Muster, das die Mutation von Daten hinter gemeinsamen Referenzen (&T) erlaubt
- [[rust-gui]] - Überblick über die GUI-Entwicklung in Rust: native Frameworks, Bindings zu etablierten Toolkits und
- [[send-sync]] - Marker-Traits, die Thread-Sicherheitsgarantien auf Typebene kodieren
- [[sized-and-dst]] - Rust-Typen teilen sich in Sized (zur Kompilierzeit bekannte Größe) und Dynamically Sized Types (DSTs, Größe
