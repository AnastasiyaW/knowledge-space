---
title: Traits
category: concepts
tags: [rust, traits, polymorphism, trait-objects, dyn, impl, derive, trait-bounds]
---

# Traits

Traits define shared behavior - similar to interfaces in other languages but with default implementations, associated types, and the ability to implement for foreign types. Traits are the foundation of Rust's polymorphism, used for operator overloading, generic bounds, and dynamic dispatch.

## Key Facts

- Traits define method signatures that types must implement
- Default implementations allow optional overriding
- **Orphan rule:** can only implement a trait for a type if either the trait OR the type is defined in your crate
- **Derive macros:** `#[derive(Debug, Clone, PartialEq)]` auto-implement common traits
- **Trait objects** (`dyn Trait`) enable dynamic dispatch via vtable
- **Blanket implementations:** `impl<T: Display> ToString for T` - implement for all types matching a bound
- Auto-traits: `Send`, `Sync`, `Sized`, `Unpin` are implemented automatically by the compiler

## Patterns

### Defining and Implementing Traits

```rust
trait Summary {
    fn summarize_author(&self) -> String;

    // Default implementation
    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}

struct Article { author: String, content: String }

impl Summary for Article {
    fn summarize_author(&self) -> String { self.author.clone() }
    // summarize() uses default
}
```

### Trait Bounds

```rust
// Syntax options (equivalent):
fn notify(item: &impl Summary) { }
fn notify<T: Summary>(item: &T) { }
fn notify<T>(item: &T) where T: Summary { }

// Multiple bounds
fn process<T: Summary + Display>(item: &T) { }
```

### Returning Impl Trait

```rust
fn create_summarizable() -> impl Summary {
    Article { author: "Alice".into(), content: "...".into() }
}
// Caller doesn't know the concrete type
```

### Supertraits

```rust
trait PrettyPrint: Display {
    fn pretty_print(&self) {
        println!("=== {} ===", self); // can use Display methods
    }
}
```

### Operator Overloading

```rust
use std::ops::Add;

#[derive(Debug)]
struct Point { x: f64, y: f64 }

impl Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        Point { x: self.x + other.x, y: self.y + other.y }
    }
}
```

## Gotchas

- Cannot return different concrete types from `impl Trait` functions (e.g., Article or Tweet based on condition) - use `Box<dyn Trait>` instead
- Trait objects have a small runtime cost (vtable indirection) vs monomorphized generics (zero-cost)
- `Sized` trait is implicitly bound on all generic parameters - use `?Sized` to accept unsized types

## See Also

- [[generics-and-monomorphization]] - compile-time polymorphism with generics
- [[dynamic-dispatch]] - trait objects, vtables, dyn Trait
- [[error-handling]] - Error trait and From for error type conversion
