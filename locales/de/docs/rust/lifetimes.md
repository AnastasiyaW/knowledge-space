---
title: "Lebensdauern"
category: concepts
tags: [rust, lifetimes, borrow-checker, references, annotations, elision, static, nll]
level: 4
source_sha256: d577fa6f2dc709a9d8281e8eadcaf6b7623ca24b8f3776614824e2b6b0aea498
translation: machine
translated_at: '2026-10-24'
---
# Lebensdauern {#lifetimes}

Lebensdauern sind die Art des Compilers, zu verfolgen, wie lange Referenzen gültig bleiben. Sie verhindern zur Compilezeit hängende Referenzen (dangling references) - ganz ohne Garbage Collector. Die meisten Lebensdauern werden durch Elision-Regeln automatisch abgeleitet; explizite Annotationen (`'a`) sind nur dann nötig, wenn der Compiler die Beziehung zwischen Eingabe- und Ausgabereferenzen nicht bestimmen kann.

## Wichtige Fakten {#key-facts}

- Lifetime-Annotationen ändern nicht, wie lange Daten leben - sie beschreiben Beziehungen zwischen Referenzen
- `'a` liest sich als "Lifetime a" - ein benannter Bereich des Codes, in dem eine Referenz gültig ist
- **Elision-Regeln** behandeln die meisten Fälle automatisch (einzelne Eingabereferenz, `&self`-Methoden)
- `'static` = Referenz ist für das gesamte Programm gültig (String-Literale, geleakte Daten)
- **NLL (Non-Lexical Lifetimes)**: Der Borrow Checker analysiert die tatsächliche Verwendung, nicht nur lexikalische Gültigkeitsbereiche
- Structs, die Referenzen halten, müssen Lifetime-Parameter deklarieren: `struct Foo<'a> { data: &'a str }`

## Muster {#patterns}

### Explizite Lifetime-Annotationen {#explicit-lifetime-annotations}

```rust
// Return reference must live as long as BOTH inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Multiple lifetimes when they're independent
fn first_word<'a, 'b>(s: &'a str, _prefix: &'b str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}
```

### Elision-Regeln für Lifetimes {#lifetime-elision-rules}

Der Compiler leitet Lebensdauern in drei Fällen ab:
1. Jede Eingabereferenz erhält einen eigenen Lifetime-Parameter
2. Gibt es genau eine Eingabe-Lifetime, wird sie allen Ausgaben zugewiesen
3. Ist eine Eingabe `&self` oder `&mut self`, wird ihre Lifetime allen Ausgaben zugewiesen

```rust
// These are equivalent (rule 2):
fn first(s: &str) -> &str { &s[..1] }
fn first<'a>(s: &'a str) -> &'a str { &s[..1] }

// Method: self's lifetime used for output (rule 3):
impl MyStruct {
    fn name(&self) -> &str { &self.name }
}
```

### Lifetimes in Structs {#struct-lifetimes}

```rust
struct Important<'a> {
    content: &'a str,
}

// Struct cannot outlive the reference it holds
let novel = String::from("Call me Ishmael...");
let i = Important { content: &novel };
// novel must live at least as long as i
```

### Die `'static`-Lifetime {#static-lifetime}

```rust
// String literals are always 'static
let s: &'static str = "I live forever";

// 'static as trait bound: type contains no non-static references
fn spawn_thread<T: Send + 'static>(data: T) { /* ... */ }

// Leaking to get 'static (rare, use carefully)
let leaked: &'static str = Box::leak(String::from("leaked").into_boxed_str());
```

### Innere Veränderlichkeit (Borrow Checker zur Laufzeit umgehen) {#interior-mutability-bypassing-borrow-checker-at-runtime}

```rust
use std::cell::{Cell, RefCell};

// Cell<T> for Copy types - get/set, no references
let cell = Cell::new(5);
cell.set(10);
let val = cell.get();  // 10

// RefCell<T> for any type - runtime borrow checking
let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4);     // runtime-checked mutable borrow
let r = data.borrow();          // runtime-checked immutable borrow
// data.borrow_mut();            // PANIC: already borrowed immutably
```

## Fallstricke {#gotchas}

- Der Compiler kann den Kontrollfluss für Borrows nicht vollständig analysieren: Selbst `if true { &mut x } else { &y }` kann ihn verwirren - strukturiere den Code stattdessen um
- Die HashMap-Entry-API existiert genau deshalb, weil der Borrow Checker Muster wie "nachschlagen, dann einfügen" nicht verarbeiten konnte
- `Cell`/`RefCell` sind Send, aber NICHT Sync - nur für Single-Threading (verwende `Mutex`/`RwLock` für Multi-Threading)
- `'static` bedeutet als Bound nicht "lebt ewig" - es bedeutet "enthält keine nicht-statischen Referenzen" (besitzende Typen wie `String` sind `'static`)

## Siehe auch {#see-also}

- [[borrowing-and-references]] - Borrow-Regeln, die Lifetimes durchsetzen
- [Smart Pointer](smart-pointers.md) - RefCell für innere Veränderlichkeit, Rc/Arc für geteilten Besitz
- [Nebenläufigkeit](concurrency.md) - 'static-Bound bei gestarteten Threads
- [[generics-and-monomorphization]] - Lifetime-Parameter in generischem Code
