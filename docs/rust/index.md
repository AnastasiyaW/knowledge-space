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
- [[smart-pointers]] - Box, Rc, Arc, RefCell, Cow, interior mutability

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

- [[concurrency]] - threads, Send/Sync, Arc+Mutex, channels, RwLock
- [[async-await]] - tokio, futures, select, streams, Pin

## Error Handling

- [[error-handling]] - Result, Option, ? operator, anyhow/thiserror, custom errors

## Language Features

- [[macros]] - declarative (macro_rules!) and procedural macros, derive, syn/quote
- [[modules-and-visibility]] - mod, pub, use, Cargo.toml, workspaces, testing, docs

## Tooling and Ecosystem

- [[rust-tooling]] - cargo, clippy, serde, rayon, FFI, web frameworks, WebAssembly, profiling
