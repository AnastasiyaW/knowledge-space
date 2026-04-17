---
title: Dynamic Dispatch
category: concepts
tags: [rust, dyn, trait-objects, vtable, polymorphism, object-safety, any, downcasting]
---

# Dynamic Dispatch

Dynamic dispatch uses trait objects (`dyn Trait`) to call methods through a vtable at runtime. A `dyn Trait` reference is a fat pointer: data pointer + vtable pointer. This enables heterogeneous collections and runtime polymorphism, at the cost of indirect call overhead and inability to inline. Not all traits are object-safe.

## Key Facts

- `&dyn Trait` / `Box<dyn Trait>` = fat pointer (2 words): pointer to data + pointer to vtable
- **vtable** = table of function pointers for the trait's methods (one per concrete type)
- Runtime overhead: one indirect function call per method dispatch (prevents inlining)
- **Object safety** required: no `Self` in return types, no generic methods, no associated constants with `Self` bounds
- `dyn Any` enables runtime type checking and downcasting
- Use when: types unknown at compile time, heterogeneous collections, plugin systems

## Patterns

### Trait Objects

```rust
trait Animal {
    fn speak(&self) -> &str;
}

struct Dog;
struct Cat;
impl Animal for Dog { fn speak(&self) -> &str { "Woof" } }
impl Animal for Cat { fn speak(&self) -> &str { "Meow" } }

// Heterogeneous collection - impossible with generics alone
let animals: Vec<Box<dyn Animal>> = vec![
    Box::new(Dog),
    Box::new(Cat)];

for animal in &animals {
    println!("{}", animal.speak());  // vtable dispatch
}
```

### Object Safety Rules

A trait is object-safe if all methods:
- Have `self`, `&self`, or `&mut self` as first parameter
- Do not return `Self`
- Have no generic type parameters

```rust
// Object-safe
trait Draw { fn draw(&self); }

// NOT object-safe (returns Self)
trait Clone { fn clone(&self) -> Self; }

// NOT object-safe (generic method)
trait Serialize { fn serialize<W: Write>(&self, w: &mut W); }
```

### dyn Any (Runtime Type Checking)

```rust
use std::any::Any;

fn process(value: &dyn Any) {
    if let Some(s) = value.downcast_ref::<String>() {
        println!("String: {}", s);
    } else if let Some(n) = value.downcast_ref::<i32>() {
        println!("i32: {}", n);
    }
}
```

### When to Use Which

| Scenario | Use |
|----------|-----|
| All types known at compile time | Generics (`impl Trait`) |
| Heterogeneous collection | `Vec<Box<dyn Trait>>` |
| Plugin/extension system | `dyn Trait` |
| Performance-critical hot path | Generics (enables inlining) |
| Minimizing binary size | `dyn Trait` (no code duplication) |

## Gotchas

- Cannot call non-object-safe methods through `dyn Trait` - must restructure or use workarounds
- `Box<dyn Trait>` requires heap allocation for each object
- Cannot combine multiple trait objects: `dyn TraitA + TraitB` requires a supertrait or separate handling
- Trait objects have no type information at compile time - downcasting needs `dyn Any`

## See Also

- [[traits]] - trait definition, bounds, and implementations
- [[generics-and-monomorphization]] - static dispatch alternative
- [[smart-pointers]] - Box<T> for heap allocation of trait objects
