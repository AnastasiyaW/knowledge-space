---
title: "Traits"
category: concepts
tags: [rust, traits, polymorphism, trait-objects, dyn, impl, derive, trait-bounds]
level: 3
source_sha256: 014c08373298f428cce460bc7ded850c3195fbf79f2985b00fe93873ad439d3f
translation: machine
translated_at: '2026-10-24'
---
# Traits {#traits}

Traits definieren gemeinsames Verhalten – ähnlich wie Interfaces in anderen Sprachen, aber mit Standardimplementierungen, assoziierten Typen und der Möglichkeit, sie für fremde Typen zu implementieren. Traits sind die Grundlage des Polymorphismus in Rust und werden für Operatorüberladung, generische Trait-Bounds und dynamisches Dispatching eingesetzt.

## Key Facts {#key-facts}

- Traits definieren Methodensignaturen, die Typen implementieren müssen
- Standardimplementierungen erlauben optionales Überschreiben
- **Orphan rule:** Ein Trait kann nur für einen Typ implementiert werden, wenn entweder der Trait oder der Typ in deinem Crate definiert ist
- **Derive-Makros:** `#[derive(Debug, Clone, PartialEq)]` implementiert gängige Traits automatisch
- **Trait-Objekte** (`dyn Trait`) ermöglichen dynamisches Dispatching über eine vtable
- **Blanket-Implementierungen:** `impl<T: Display> ToString for T` – implementiert einen Trait für alle Typen, die eine Bedingung erfüllen
- Auto-Traits: `Send`, `Sync`, `Sized` und `Unpin` werden vom Compiler automatisch implementiert

## Patterns {#patterns}

### Defining and Implementing Traits {#defining-and-implementing-traits}

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

### Trait Bounds {#trait-bounds}

```rust
// Syntax options (equivalent):
fn notify(item: &impl Summary) { }
fn notify<T: Summary>(item: &T) { }
fn notify<T>(item: &T) where T: Summary { }

// Multiple bounds
fn process<T: Summary + Display>(item: &T) { }
```

### Returning Impl Trait {#returning-impl-trait}

```rust
fn create_summarizable() -> impl Summary {
    Article { author: "Alice".into(), content: "...".into() }
}
// Caller doesn't know the concrete type
```

### Supertraits {#supertraits}

```rust
trait PrettyPrint: Display {
    fn pretty_print(&self) {
        println!("=== {} ===", self); // can use Display methods
    }
}
```

### Operator Overloading {#operator-overloading}

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

## Gotchas {#gotchas}

- Aus `impl Trait`-Funktionen können keine unterschiedlichen konkreten Typen zurückgegeben werden (z. B. abhängig von einer Bedingung entweder `Article` oder `Tweet`) – stattdessen `Box<dyn Trait>` verwenden
- Trait-Objekte haben eine kleine Laufzeitkostenz (vtable-Indirektion) im Vergleich zu monomorphisierten Generics (Nullkosten-Abstraktion)
- Der Trait `Sized` wird implizit für alle generischen Parameter gebunden – mit `?Sized` lassen sich auch unsized Typen akzeptieren

## See Also {#see-also}

- [[generics-and-monomorphization]] – Polymorphismus zur Compilezeit mit Generics
- [[dynamic-dispatch]] – Trait-Objekte, vtables, dyn Trait
- [Error Handling](error-handling.md) – Trait Error und From für die Konvertierung von Fehlertypen
