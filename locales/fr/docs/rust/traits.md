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

Les traits définissent un comportement partagé, à la manière des interfaces dans d'autres langages, mais avec des implémentations par défaut, des types associés et la possibilité d'implémenter le trait pour des types étrangers. Les traits sont le fondement du polymorphisme en Rust, utilisés pour la surcharge d'opérateurs, les bornes génériques et la répartition dynamique.

## Points clés {#key-facts}

- Les traits définissent des signatures de méthodes que les types doivent implémenter
- Les implémentations par défaut permettent de les redéfinir de manière facultative
- **Règle de l'orphelin (orphan rule) :** on ne peut implémenter un trait pour un type que si le trait OU le type est défini dans votre crate
- **Macros derive :** `#[derive(Debug, Clone, PartialEq)]` implémente automatiquement les traits courants
- **Objets trait** (`dyn Trait`) permettent une répartition dynamique via une vtable
- **Implémentations génériques (blanket implementations) :** `impl<T: Display> ToString for T` - implémente le trait pour tous les types satisfaisant une borne
- Les auto-traits : `Send`, `Sync`, `Sized`, `Unpin` sont implémentés automatiquement par le compilateur

## Modèles {#patterns}

### Définir et implémenter des traits {#defining-and-implementing-traits}

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

### Bornes de trait {#trait-bounds}

```rust
// Syntax options (equivalent):
fn notify(item: &impl Summary) { }
fn notify<T: Summary>(item: &T) { }
fn notify<T>(item: &T) where T: Summary { }

// Multiple bounds
fn process<T: Summary + Display>(item: &T) { }
```

### Retourner un impl Trait {#returning-impl-trait}

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

### Surcharge d'opérateurs {#operator-overloading}

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

## Pièges {#gotchas}

- Il est impossible de retourner des types concrets différents depuis une fonction `impl Trait` (par exemple Article ou Tweet selon une condition) - utilisez `Box<dyn Trait>` à la place
- Les objets trait ont un petit coût à l'exécution (indirection par vtable) contrairement aux génériques monomorphisés (coût nul)
- Le trait `Sized` est implicitement borné sur tous les paramètres génériques - utilisez `?Sized` pour accepter des types non dimensionnés

## Voir aussi {#see-also}

- [[generics-and-monomorphization]] - polymorphisme à la compilation avec les génériques
- [[dynamic-dispatch]] - objets trait, vtables, dyn Trait
- [Error Handling](error-handling.md) - le trait Error et From pour la conversion des types d'erreur
