---
title: Generics and Monomorphization
category: concepts
tags: [rust, generics, monomorphization, type-parameters, where-clause, turbofish, impl-trait, static-dispatch]
---

# Generics and Monomorphization

Generics enable writing code that works with any type satisfying trait bounds. The compiler generates specialized versions for each concrete type used - this is monomorphization. The result is zero runtime overhead (static dispatch) at the cost of larger binary size and longer compile times.

## Key Facts

- Generic functions/structs use type parameters: `fn max<T: PartialOrd>(a: T, b: T) -> T`
- **Monomorphization**: compiler generates `max_i32`, `max_f64`, `max_String` etc. - zero-cost abstraction
- `impl Trait` in argument position = syntactic sugar for generics
- `impl Trait` in return position = opaque type (hides concrete type from caller)
- **Turbofish** syntax `::<Type>` for explicit type annotation: `"42".parse::<i32>()`
- Trade-off: static dispatch (generics) = fast but larger binary; dynamic dispatch (`dyn Trait`) = smaller binary but vtable overhead

## Patterns

### Generic Functions

```rust
// Three equivalent ways to write trait bounds
fn print_it<T: Display>(item: T) { println!("{}", item); }
fn print_it(item: impl Display) { println!("{}", item); }
fn print_it<T>(item: T) where T: Display { println!("{}", item); }

// Multiple bounds
fn process<T: Display + Clone + Debug>(item: T) { /* ... */ }

// Multiple type parameters with where clause (cleaner)
fn merge<A, B, C>(a: A, b: B) -> C
where
    A: IntoIterator<Item = C>,
    B: IntoIterator<Item = C>,
    C: FromIterator<C>,
{ /* ... */ }
```

### Generic Structs and Enums

```rust
struct Point<T> { x: T, y: T }

impl<T: Add<Output = T> + Copy> Point<T> {
    fn add(&self, other: &Point<T>) -> Point<T> {
        Point { x: self.x + other.x, y: self.y + other.y }
    }
}

// Conditional impl: only for specific types
impl Point<f64> {
    fn distance(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

### impl Trait in Return Position

```rust
fn make_greeting() -> impl Display {
    "Hello, world!"  // concrete type hidden from caller
}

// Common use: returning iterators without exposing complex types
fn even_numbers(v: &[i32]) -> impl Iterator<Item = &i32> {
    v.iter().filter(|&&x| x % 2 == 0)
}
```

### Static vs Dynamic Dispatch

| Feature | Static (generics / `impl Trait`) | Dynamic (`dyn Trait`) |
|---------|------|---------|
| Dispatch | Compile-time (monomorphization) | Runtime (vtable) |
| Performance | Fastest, enables inlining | Indirect call overhead |
| Binary size | Larger (code duplication) | Smaller |
| Heterogeneous collections | Not possible | Yes: `Vec<Box<dyn Trait>>` |
| Type known at compile time | Yes | No |

### Turbofish Syntax

```rust
let x = "42".parse::<i32>().unwrap();
let v = Vec::<u8>::new();
let sum = [1, 2, 3].iter().sum::<i32>();
```

## Gotchas

- `impl Trait` in return position can only return ONE concrete type - cannot return different types conditionally (use `Box<dyn Trait>` instead)
- Monomorphization increases compile time and binary size - each unique type creates new code
- `Sized` trait is implicitly bound on all generics - use `?Sized` to accept unsized types like `str` or `dyn Trait`
- Generic type inference sometimes fails - turbofish (`::<Type>`) or let-binding with type annotation resolves it

## See Also

- [[traits]] - trait bounds and trait implementations
- [[dynamic-dispatch]] - dyn Trait, vtables, object safety
- [[closures]] - returning closures via impl Fn
- [[iterators]] - generic iterator adaptors
