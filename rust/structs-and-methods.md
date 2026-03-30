---
title: Structs and Methods
category: concepts
tags: [structs, methods, impl, encapsulation, newtype]
---
# Structs and Methods

Structs are custom data types that group related fields; methods are functions associated with a type via `impl` blocks.

## Key Facts

- Three struct kinds: classic (named fields), tuple struct (indexed fields), unit struct (no fields)
- `impl` blocks define methods (take `self`) and associated functions (no `self`)
- Method receivers: `self` (consume), `&self` (borrow), `&mut self` (mutable borrow)
- Struct update syntax: `MyStruct { field: val, ..other }` copies remaining fields
- Destructuring: `let MyStruct { field1, field2, .. } = instance;`
- All fields private by default; use `pub` per-field for visibility from other [[modules-and-visibility]]
- `#[derive(...)]` auto-implements common [[traits]]: `Debug`, `Clone`, `Copy`, `PartialEq`, `Eq`, `Hash`, `Default`
- Newtype pattern: `struct Wrapper(pub InnerType);` - enables implementing foreign traits on foreign types (orphan rule workaround)

## Patterns

```rust
// Classic struct
#[derive(Debug, Clone)]
struct User {
    name: String,
    email: String,
    active: bool,
}

// Construction
let user = User {
    name: String::from("Alice"),
    email: String::from("alice@example.com"),
    active: true,
};

// Struct update syntax
let user2 = User {
    name: String::from("Bob"),
    ..user  // moves non-Copy fields from user
};

// Destructuring
let User { name, email, .. } = user2;

// Tuple struct
struct Point(f64, f64);
struct Color(u8, u8, u8);

let origin = Point(0.0, 0.0);
let x = origin.0;

// Unit struct (marker/placeholder)
struct EndOfStream;

// Methods and associated functions
impl User {
    // Associated function (constructor pattern)
    fn new(name: String, email: String) -> Self {
        Self { name, email, active: true }
    }

    // Immutable method
    fn full_info(&self) -> String {
        format!("{} <{}>", self.name, self.email)
    }

    // Mutable method
    fn deactivate(&mut self) {
        self.active = false;
    }

    // Consuming method
    fn into_name(self) -> String {
        self.name
    }
}

// Multiple impl blocks allowed
impl std::fmt::Display for User {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.full_info())
    }
}

// Newtype pattern
struct Meters(f64);
struct Kilometers(f64);

impl From<Kilometers> for Meters {
    fn from(km: Kilometers) -> Self {
        Meters(km.0 * 1000.0)
    }
}
```

## Gotchas

- **Symptom**: "field is private" when constructing struct from another module - **Cause**: fields are private by default - **Fix**: add `pub` to fields, or provide a constructor function
- **Symptom**: struct update syntax moves non-Copy fields - **Cause**: `..other` moves fields, making `other` partially moved - **Fix**: clone before update or only spread Copy fields
- **Symptom**: can't implement Display for Vec<MyType> - **Cause**: orphan rule prevents implementing foreign traits for foreign types - **Fix**: use newtype pattern: `struct MyVec(Vec<MyType>)`

## See Also

- [[enums-and-pattern-matching]] - algebraic data types and match
- [[traits]] - implementing behavior for structs
- [[modules-and-visibility]] - `pub` modifiers and encapsulation
- [The Rust Book - Structs](https://doc.rust-lang.org/book/ch05-00-structs.html)
- [The Rust Book - Method Syntax](https://doc.rust-lang.org/book/ch05-03-method-syntax.html)
