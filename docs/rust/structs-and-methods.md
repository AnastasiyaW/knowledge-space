---
title: Structs and Methods
category: concepts
tags: [rust, structs, methods, impl, encapsulation, tuple-struct, newtype, self, visibility]
---

# Structs and Methods

Structs are Rust's primary way to create custom data types. Three kinds exist: classic (named fields), tuple (positional fields), and unit (no fields). Methods are defined in `impl` blocks with three receiver types (`&self`, `&mut self`, `self`) controlling access. Visibility defaults to private - use `pub` to expose across module boundaries.

## Key Facts

- Three struct kinds: classic (`struct Point { x: f64, y: f64 }`), tuple (`struct Color(u8, u8, u8)`), unit (`struct Marker;`)
- All fields and methods are **private by default** - privacy enforced at module boundary
- `impl` blocks define methods (take `self`) and associated functions (no `self`, like constructors)
- Struct update syntax: `User { name: "Tom".into(), ..old_user }` copies remaining fields
- `#[derive(Debug, Clone, PartialEq)]` auto-implements common traits
- Multiple `impl` blocks allowed per type (useful for conditional trait implementations)

## Patterns

### Three Struct Kinds

```rust
// Classic struct - named fields
struct User {
    name: String,
    email: String,
    active: bool,
}

// Tuple struct - positional fields (newtype pattern)
struct Meters(f64);
struct Color(u8, u8, u8);

// Unit struct - no fields (markers, type-level tags)
struct EndOfStream;
```

### Creating and Destructuring

```rust
let user = User {
    name: "Alice".to_string(),
    email: "alice@example.com".to_string(),
    active: true,
};

// Struct update syntax (spread)
let user2 = User { name: "Bob".to_string(), ..user };

// Destructuring
let User { name, email, .. } = user2;

// Tuple struct access and destructuring
let color = Color(255, 128, 0);
let r = color.0;
let Color(_, g, _) = color;
```

### Methods and Associated Functions

```rust
struct Point { x: f64, y: f64 }

impl Point {
    // Associated function (constructor) - no self
    fn origin() -> Point {
        Point { x: 0.0, y: 0.0 }
    }

    // Immutable borrow - read-only access
    fn distance(&self, other: &Point) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }

    // Mutable borrow - can modify
    fn translate(&mut self, dx: f64, dy: f64) {
        self.x += dx;
        self.y += dy;
    }

    // Takes ownership - consumes the value
    fn into_tuple(self) -> (f64, f64) {
        (self.x, self.y)
    }
}

let p = Point::origin();          // associated function call
let d = p.distance(&Point { x: 3.0, y: 4.0 });  // method call
```

### Visibility Modifiers

```rust
pub struct Config {
    pub name: String,         // public everywhere
    pub(crate) port: u16,     // public within crate only
    pub(super) debug: bool,   // public in parent module
    secret: String,           // private (default)
}

// Re-export to flatten module hierarchy
pub use self::inner::PublicApi;
```

### Newtype Pattern

```rust
// Wrap a type to add type safety without runtime cost
struct Meters(f64);
struct Seconds(f64);

fn speed(distance: Meters, time: Seconds) -> f64 {
    distance.0 / time.0
}

// Compiler prevents: speed(Seconds(10.0), Meters(100.0))
```

## Gotchas

- Struct update syntax (`..old`) moves non-Copy fields - `old` may become partially moved
- Cannot have both `&self` method and `&mut self` method called on same value simultaneously (borrow rules)
- Unit structs are zero-sized types (ZST) - take no memory at runtime
- `self` receiver (by value) consumes the struct - it cannot be used after the method call

## See Also

- [[traits]] - implementing traits for structs
- [[enums-and-pattern-matching]] - enums as the other main custom type
- [[modules-and-visibility]] - module system and pub visibility rules
- [[ownership-and-move-semantics]] - ownership implications of self receivers
