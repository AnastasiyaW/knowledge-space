---
title: Dynamic Dispatch
category: concepts
tags: [dyn, trait-objects, vtable, polymorphism, object-safety]
---
# Dynamic Dispatch

Dynamic dispatch uses trait objects (`dyn Trait`) to resolve method calls at runtime via vtable, enabling heterogeneous collections and runtime polymorphism.

## Key Facts

- `dyn Trait` is a trait object - a fat pointer: data pointer + vtable pointer
- Trait objects must be behind a pointer: `&dyn Trait`, `Box<dyn Trait>`, `Arc<dyn Trait>`
- Object safety rules - a trait is object-safe if:
  - No methods return `Self` (except with `where Self: Sized` bound)
  - No generic type parameters on methods
  - No associated functions without `self` (unless bounded with `Self: Sized`)
- Runtime cost: indirect function call through vtable (no inlining possible)
- Advantage over [[generics-and-monomorphization]]: smaller binary, heterogeneous collections, runtime flexibility
- `dyn Any` enables runtime type checking and downcasting
- Multiple trait bounds: `dyn TraitA + TraitB` (limited, usually use supertraits)

## Patterns

```rust
// Trait object behind Box
trait Animal {
    fn name(&self) -> &str;
    fn sound(&self) -> &str;
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn name(&self) -> &str { "Dog" }
    fn sound(&self) -> &str { "Woof" }
}
impl Animal for Cat {
    fn name(&self) -> &str { "Cat" }
    fn sound(&self) -> &str { "Meow" }
}

// Heterogeneous collection
let animals: Vec<Box<dyn Animal>> = vec![
    Box::new(Dog),
    Box::new(Cat),
];
for animal in &animals {
    println!("{}: {}", animal.name(), animal.sound());
}

// Function accepting trait object
fn describe(animal: &dyn Animal) {
    println!("{} says {}", animal.name(), animal.sound());
}

// Returning trait objects
fn make_animal(kind: &str) -> Box<dyn Animal> {
    match kind {
        "dog" => Box::new(Dog),
        "cat" => Box::new(Cat),
        _ => panic!("unknown animal"),
    }
}

// dyn Any for runtime type checking
use std::any::Any;

fn print_if_string(val: &dyn Any) {
    if let Some(s) = val.downcast_ref::<String>() {
        println!("String: {s}");
    } else {
        println!("Not a string");
    }
}

// Object-safe trait design
trait Drawable {
    fn draw(&self);
    fn bounds(&self) -> (f64, f64, f64, f64);
}

struct Canvas {
    elements: Vec<Box<dyn Drawable>>,
}

impl Canvas {
    fn render(&self) {
        for element in &self.elements {
            element.draw();
        }
    }
}

// Trait object with lifetime
fn longest_name<'a>(animals: &'a [Box<dyn Animal>]) -> &'a str {
    animals.iter()
        .map(|a| a.name())
        .max_by_key(|n| n.len())
        .unwrap_or("")
}
```

## Gotchas

- **Symptom**: "the trait `X` cannot be made into an object" - **Cause**: trait is not object-safe (has `Self` returns, generic methods, or associated functions) - **Fix**: add `where Self: Sized` to non-object-safe methods, or redesign
- **Symptom**: can't call `clone()` on `Box<dyn Trait>` - **Cause**: `Clone` is not object-safe (returns `Self`) - **Fix**: add a `fn clone_box(&self) -> Box<dyn Trait>` method to your trait
- **Symptom**: dynamic dispatch is slower than generics - **Cause**: vtable indirection prevents inlining - **Fix**: use generics for hot paths, `dyn` for cold paths or heterogeneous storage
- **Symptom**: `dyn Trait + Send + Sync` required for thread-safe trait objects - **Cause**: trait objects don't automatically inherit marker traits - **Fix**: explicitly add `Send + Sync` bounds

## See Also

- [[generics-and-monomorphization]] - static dispatch alternative
- [[traits]] - defining traits for both static and dynamic use
- [[smart-pointers]] - `Box<dyn Trait>` ownership patterns
- [The Rust Book - Trait Objects](https://doc.rust-lang.org/book/ch17-02-trait-objects.html)
- [Rust Reference - Object Safety](https://doc.rust-lang.org/reference/items/traits.html#object-safety)
