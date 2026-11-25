---
title: "Closures"
category: concepts
tags: [rust, closures, fn, fnmut, fnonce, move, lambda, capture, higher-order]
level: 4
source_sha256: df1590f21a1ea6a989ef28d829d083da55be7669f88498ad744cffda3bdee4f1
translation: machine
translated_at: '2026-10-24'
---
# Closures {#closures}

Closures sind anonyme Funktionen, die Variablen aus ihrem umgebenden Gültigkeitsbereich erfassen können. Anders als Funktionszeiger (`fn`) tragen Closures Zustand. Der Compiler erzeugt für jede Closure eine anonyme Struktur, die eines von drei Traits implementiert: `Fn`, `FnMut` oder `FnOnce` - dies bestimmt, wie die Closure ihren erfassten Zustand verwendet.

## Key Facts {#key-facts}

- Closure-Syntax: `|params| body` - Typen werden meist inferiert, geschweifte Klammern sind bei einzelnen Ausdrücken optional
- **Funktionszeiger** (`fn(u32) -> u64`) = einfacher Zeiger auf Code, ohne Zustand
- **Closure** = anonyme Struktur mit erfasstem Zustand + vom Compiler generierte Trait-Implementierung
- Closures erfassen standardmäßig per Referenz; das Schlüsselwort `move` erzwingt die Erfassung per Wert
- Die drei Traits bilden eine Hierarchie: `Fn` (geteilte Referenz) > `FnMut` (exklusive Referenz) > `FnOnce` (Besitz)
- `Fn` ist ein Subtrait von `FnMut`, der wiederum ein Subtrait von `FnOnce` ist; Funktionszeiger implementieren alle drei
- Die Rückgabe von Closures aus Funktionen erfordert die Syntax `impl Fn*` (oder `Box<dyn Fn*>`)

## Patterns {#patterns}

### Closure Syntax Variants {#closure-syntax-variants}

```rust
// Type inference (most common)
|a, b| a + b

// Explicit types
|a: u32, b: u32| -> u32 { a + b }

// Multi-line with braces
|x| {
    let y = x * 2;
    y + 1
}
```

### Capture Modes {#capture-modes}

```rust
let mut x = 0u32;

// Captures &mut x (inferred from mutation)
let mut add_to_x = |a| x += a;
add_to_x(1);
add_to_x(2);
// x is now 3

// move: captures ALL referenced variables by value
let data = vec![1, 2, 3];
let closure = move || println!("{:?}", data);
// data is no longer accessible here
```

### The Three Closure Traits {#the-three-closure-traits}

```rust
// Fn - shared reference (&self), callable many times
fn apply_fn(f: impl Fn(i32) -> i32, x: i32) -> i32 { f(x) }

// FnMut - exclusive reference (&mut self), callable many times but may mutate
fn apply_mut(mut f: impl FnMut(i32), x: i32) { f(x) }

// FnOnce - ownership (self), callable only once (consumes captured state)
fn apply_once(f: impl FnOnce() -> Vec<i32>) -> Vec<i32> { f() }
```

### Accepting Closures (Three Equivalent Syntaxes) {#accepting-closures-three-equivalent-syntaxes}

```rust
fn use_f(mut f: impl FnMut(u32, u64) -> u32) { /* ... */ }
fn use_f<F: FnMut(u32, u64) -> u32>(mut f: F) { /* ... */ }
fn use_f<F>(mut f: F) where F: FnMut(u32, u64) -> u32 { /* ... */ }
```

### Returning Closures {#returning-closures}

```rust
fn get_adder(mut x: u32) -> impl FnMut(u32) -> u32 {
    move |a| { x += a; x }
}

let mut adder = get_adder(10);
assert_eq!(adder(5), 15);
assert_eq!(adder(3), 18);
```

### Storing Closures {#storing-closures}

```rust
// Via type parameters (static dispatch, zero-cost)
struct Handler<F: Fn(u32) -> u32> { callback: F }

// Via trait objects (dynamic dispatch, heap allocation)
struct Dispatcher { callbacks: Vec<Box<dyn Fn(u32) -> u32>> }
```

### Higher-Rank Trait Bounds (HRTBs) {#higher-rank-trait-bounds-hrtbs}

```rust
// "for any lifetime 'a" - needed when closure takes references
fn apply<F>(f: F) where F: for<'a> Fn(&'a str) -> &'a str {
    let s = String::from("hello");
    println!("{}", f(&s));
}
```

## Gotchas {#gotchas}

- `move` erfasst ALLE referenzierten Variablen, nicht nur die beabsichtigten - kann zu unerwarteter Besitzübertragung führen
- Closure-Typen sind anonym - zwei Closures mit identischer Signatur haben unterschiedliche Typen (für heterogene Sammlungen `dyn Fn` verwenden)
- `FnOnce`-Closures können nur einmal aufgerufen werden - ein zweiter Aufruf ist ein Compilerfehler
- Unter der Haube: Der Compiler erzeugt eine Struktur, die den erfassten Zustand hält, plus einen Methodenaufruf - Zero-Cost-Abstraktion

## See Also {#see-also}

- [[traits]] - Fn/FnMut/FnOnce-Trait-Hierarchie
- [[iterators]] - Closures als Argumente für map, filter, fold
- [[ownership-and-move-semantics]] - Move-Semantik bei Closure-Erfassungen
- [[generics-and-monomorphization]] - statische Dispatch mit impl Trait
