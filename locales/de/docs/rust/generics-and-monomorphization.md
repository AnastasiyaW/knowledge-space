---
title: "Generics und Monomorphisierung"
category: concepts
tags: [rust, generics, monomorphization, type-parameters, where-clause, turbofish, impl-trait, static-dispatch]
level: 4
source_sha256: a5eb61f58b3674cdc1c2763c1c1ab32337adb7cc3d1e9fb9cd378a90104224b1
translation: machine
translated_at: '2026-10-24'
---
# Generics und Monomorphisierung {#generics-and-monomorphization}

Generics ermöglichen es, Code zu schreiben, der mit jedem Typ funktioniert, der die Trait-Bounds erfüllt. Der Compiler erzeugt für jeden verwendeten konkreten Typ eine spezialisierte Version – dies ist Monomorphisierung. Das Ergebnis ist kein Laufzeit-Overhead (statischer Dispatch), dafür aber eine größere Binärdatei und längere Kompilierzeiten.

## Wichtige Fakten {#key-facts}

- Generische Funktionen/Structs verwenden Typparameter: `fn max<T: PartialOrd>(a: T, b: T) -> T`
- **Monomorphisierung**: Der Compiler erzeugt `max_i32`, `max_f64`, `max_String` usw. – Zero-Cost-Abstraktion
- `impl Trait` in Argumentposition = syntaktischer Zucker für Generics
- `impl Trait` in Rückgabeposition = opaker Typ (verbirgt den konkreten Typ vor dem Aufrufer)
- **Turbofish**-Syntax `::<Type>` für explizite Typangaben: `"42".parse::<i32>()`
- Abwägung: statischer Dispatch (Generics) = schnell, aber größere Binärdatei; dynamischer Dispatch (`dyn Trait`) = kleinere Binärdatei, aber vtable-Overhead

## Muster {#patterns}

### Generische Funktionen {#generic-functions}

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

### Generische Structs und Enums {#generic-structs-and-enums}

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

### impl Trait in Rückgabeposition {#impl-trait-in-return-position}

```rust
fn make_greeting() -> impl Display {
    "Hello, world!"  // concrete type hidden from caller
}

// Common use: returning iterators without exposing complex types
fn even_numbers(v: &[i32]) -> impl Iterator<Item = &i32> {
    v.iter().filter(|&&x| x % 2 == 0)
}
```

### Statischer vs. dynamischer Dispatch {#static-vs-dynamic-dispatch}

| Merkmal | Statisch (Generics / `impl Trait`) | Dynamisch (`dyn Trait`) |
|---------|------|---------|
| Dispatch | Zur Kompilierzeit (Monomorphisierung) | Zur Laufzeit (vtable) |
| Performance | Am schnellsten, ermöglicht Inlining | Overhead durch indirekte Aufrufe |
| Binärgröße | Größer (Codeduplizierung) | Kleiner |
| Heterogene Sammlungen | Nicht möglich | Ja: `Vec<Box<dyn Trait>>` |
| Typ zur Kompilierzeit bekannt | Ja | Nein |

### Turbofish-Syntax {#turbofish-syntax}

```rust
let x = "42".parse::<i32>().unwrap();
let v = Vec::<u8>::new();
let sum = [1, 2, 3].iter().sum::<i32>();
```

## Fallstricke {#gotchas}

- `impl Trait` in Rückgabeposition kann nur EINEN konkreten Typ zurückgeben – bedingte Rückgabe unterschiedlicher Typen ist nicht möglich (stattdessen `Box<dyn Trait>` verwenden)
- Monomorphisierung erhöht Kompilierzeit und Binärgröße – jeder eindeutige Typ erzeugt neuen Code
- Das Trait `Sized` ist implizit auf allen Generics gebunden – mit `?Sized` werden auch unsized Typen wie `str` oder `dyn Trait` akzeptiert
- Typinferenz bei Generics schlägt manchmal fehl – Turbofish (`::<Type>`) oder eine Let-Bindung mit Typannotation löst das Problem

## Siehe auch {#see-also}

- [[traits]] - Trait-Bounds und Trait-Implementierungen
- [[dynamic-dispatch]] - dyn Trait, vtables, Object Safety
- [[closures]] - Rückgabe von Closures über impl Fn
- [[iterators]] - generische Iterator-Adaptoren
