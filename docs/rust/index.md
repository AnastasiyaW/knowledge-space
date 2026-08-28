---
title: Rust Knowledge Base
category: index
tags: [rust, systems-programming, memory-safety]
---

# Rust

Systems programming language with compile-time memory safety, zero-cost abstractions, and fearless concurrency. No garbage collector - ownership and borrowing enforce safety at compile time.

## Ownership and Memory

- [[ownership-and-move-semantics]] - ownership rules, RAII, move semantics, Copy/Clone
- [[borrowing-and-references]] - borrow rules, shared/mutable refs, slices, NLL
- [[lifetimes]] - lifetime annotations, elision rules, 'static, interior mutability
- [Smart Pointers](smart-pointers.md) - Box, Rc, Arc, RefCell, Cow, interior mutability

## Type System

- [[structs-and-methods]] - three struct kinds, impl blocks, visibility, newtype pattern
- [[enums-and-pattern-matching]] - algebraic types, match, if let, destructuring
- [[traits]] - trait bounds, default impls, operator overloading, orphan rule
- [[generics-and-monomorphization]] - type parameters, impl Trait, turbofish, static dispatch
- [[dynamic-dispatch]] - dyn Trait, vtables, object safety, dyn Any

## Functional Patterns

- [[closures]] - Fn/FnMut/FnOnce, captures, move, returning closures
- [[iterators]] - Iterator trait, lazy evaluation, adaptors, custom iterators
- [[collections]] - Vec, HashMap, BTreeMap, String, Big O complexity

## Concurrency and Async

- [Concurrency](concurrency.md) - threads, Send/Sync, Arc+Mutex, channels, RwLock
- [[async-await]] - tokio, futures, select, streams, Pin

## Error Handling

- [Error Handling](error-handling.md) - Result, Option, ? operator, anyhow/thiserror, custom errors

## Language Features

- [[macros]] - declarative (macro_rules!) and procedural macros, derive, syn/quote
- [[modules-and-visibility]] - mod, pub, use, Cargo.toml, workspaces, testing, docs

## Tooling and Ecosystem

- [[rust-tooling]] - cargo, clippy, serde, rayon, FFI, web frameworks, WebAssembly, profiling

## Additional References

- [[interior-mutability]] - Pattern allowing mutation of data behind shared references (&T)
- [[rust-gui]] - Landscape of GUI development in Rust: native frameworks, bindings to established toolkits, and
- [[send-sync]] - Marker traits that encode thread-safety guarantees at the type level
- [[sized-and-dst]] - Rust types divide into Sized (known size at compile time) and Dynamically Sized Types (DSTs, size
