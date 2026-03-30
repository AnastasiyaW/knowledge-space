---
title: Rust Knowledge Base
category: index
tags: [rust, systems-programming, memory-safety]
---
# Rust Knowledge Base

Reference knowledge base for Rust systems programming language - ownership, type system, concurrency, and ecosystem.

## Core Concepts

### Memory Model
- [[ownership-and-move-semantics]] - ownership rules, move/copy semantics, RAII, Drop
- [[borrowing-and-references]] - shared/mutable references, borrow checker, slices
- [[lifetimes]] - lifetime annotations, elision rules, 'static

### Type System
- [[structs-and-methods]] - struct kinds, impl blocks, encapsulation, newtype pattern
- [[enums-and-pattern-matching]] - algebraic types, match, if let, destructuring
- [[traits]] - trait definitions, orphan rules, derive, supertraits, associated types
- [[generics-and-monomorphization]] - type parameters, trait bounds, where clauses, const generics
- [[dynamic-dispatch]] - dyn Trait, vtable, object safety, trait objects

## Patterns & Practices

- [[rust/error-handling]] - Result/Option, ? operator, thiserror/anyhow, custom errors
- [[closures]] - Fn/FnMut/FnOnce, capture modes, move, returning closures
- [[iterators]] - lazy evaluation, adapter/consumer chain, custom Iterator impl
- [[collections]] - Vec, HashMap, String, slices, Entry API

## Advanced Topics

### Concurrency
- [[concurrency]] - threads, Send/Sync, Mutex, channels, atomics, scoped threads
- [[async-await]] - futures, tokio, spawn, join/select, async channels

### Pointers & Indirection
- [[smart-pointers]] - Box, Rc, Arc, Cell, RefCell, Cow, interior mutability

### Metaprogramming
- [[macros]] - macro_rules!, procedural macros, derive, cfg

## Tooling & Project Setup
- [[rust-tooling]] - cargo, rustup, clippy, rustfmt, testing, documentation

## External References

- [The Rust Programming Language (Book)](https://doc.rust-lang.org/book/)
- [Rust By Example](https://doc.rust-lang.org/rust-by-example/)
- [Rust Standard Library](https://doc.rust-lang.org/std/)
- [The Rust Reference](https://doc.rust-lang.org/reference/)
- [Rustonomicon (Unsafe Rust)](https://doc.rust-lang.org/nomicon/)
- [Async Book](https://rust-lang.github.io/async-book/)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
