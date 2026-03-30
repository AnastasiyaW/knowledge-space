---
title: Traits
category: concepts
tags: [traits, polymorphism, derive, orphan-rule, associated-types, supertraits]
---
# Traits

Traits define shared behavior (like interfaces) that types can implement, enabling [[generics-and-monomorphization]] and [[dynamic-dispatch]].

## Key Facts

- Traits declare method signatures, associated constants, and associated types
- Default implementations can be provided; implementors may override
- Orphan rule: you can only implement a trait if you own the trait OR the type (not both foreign)
- Newtype pattern circumvents orphan rule: `struct MyWrapper(ForeignType);`
- Supertraits: `trait Bar: Foo {}` means any `Bar` implementor must also implement `Foo`
- Associated types vs generics: associated types = one implementation per type, generics = many
- Marker traits: `Copy`, `Send`, `Sync`, `Sized`, `Unpin` - no methods, convey compiler guarantees
- Auto traits: `Send`, `Sync` are automatically implemented when all fields satisfy them
- Must `use` a trait to call its methods on a type
- Fully qualified syntax for disambiguation: `<Type as Trait>::method()`

## Patterns

```rust
// Define a trait
pub trait Summary {
    fn summarize_author(&self) -> String;

    // Default implementation
    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}

// Implement for a type
struct Article { author: String, content: String }

impl Summary for Article {
    fn summarize_author(&self) -> String {
        self.author.clone()
    }
    // summarize() uses default implementation
}

// Associated types
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}

struct Counter { count: u32 }
impl Iterator for Counter {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        self.count += 1;
        if self.count <= 5 { Some(self.count) } else { None }
    }
}

// Associated constants
trait HasId {
    const ID: usize;
}
impl HasId for Article {
    const ID: usize = 1;
}

// Supertraits
trait PrettyPrint: std::fmt::Display {
    fn pretty(&self) -> String {
        format!("[[ {} ]]", self)  // can use Display methods
    }
}

// Orphan rule workaround with newtype
struct Wrapper(Vec<String>);
impl std::fmt::Display for Wrapper {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

// Common derivable traits
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
struct Config {
    name: String,
    value: i32,
}

// Disambiguation with fully qualified syntax
trait A { fn do_it(&self) -> &str; }
trait B { fn do_it(&self) -> &str; }
struct S;
impl A for S { fn do_it(&self) -> &str { "A" } }
impl B for S { fn do_it(&self) -> &str { "B" } }

let s = S;
println!("{}", <S as A>::do_it(&s));  // "A"
println!("{}", <S as B>::do_it(&s));  // "B"

// Operator overloading via traits
use std::ops::Add;
#[derive(Debug, Copy, Clone)]
struct Point { x: f64, y: f64 }

impl Add for Point {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self { x: self.x + other.x, y: self.y + other.y }
    }
}
```

## Gotchas

- **Symptom**: "method not found" even though trait is implemented - **Cause**: trait not imported in scope - **Fix**: `use path::to::Trait;`
- **Symptom**: "only traits defined in current crate can be implemented" - **Cause**: orphan rule violation - **Fix**: wrap with newtype or define your own trait
- **Symptom**: "the trait bound is not satisfied" - **Cause**: type doesn't implement required trait - **Fix**: add `#[derive()]` or manual `impl`
- **Symptom**: confusion between `Display` and `Debug` - `Debug` (`{:?}`) is for developers, derivable; `Display` (`{}`) is for users, must be manually implemented

## See Also

- [[generics-and-monomorphization]] - static polymorphism using trait bounds
- [[dynamic-dispatch]] - `dyn Trait` for runtime polymorphism
- [[closures]] - `Fn`, `FnMut`, `FnOnce` traits
- [The Rust Book - Traits](https://doc.rust-lang.org/book/ch10-02-traits.html)
- [std::ops](https://doc.rust-lang.org/std/ops/index.html) - operator overloading traits
