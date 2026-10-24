---
title: "Fermetures"
category: concepts
tags: [rust, closures, fn, fnmut, fnonce, move, lambda, capture, higher-order]
level: 4
source_sha256: df1590f21a1ea6a989ef28d829d083da55be7669f88498ad744cffda3bdee4f1
translation: machine
translated_at: '2026-10-24'
---
# Fermetures {#closures}

Les fermetures (*closures*) sont des fonctions anonymes qui peuvent capturer des variables de leur portée englobante. Contrairement aux pointeurs de fonction (`fn`), les fermetures portent un état. Le compilateur génère une structure anonyme pour chaque fermeture, qui implémente l'un des trois traits suivants : `Fn`, `FnMut` ou `FnOnce`, selon la manière dont la fermeture utilise son état capturé.

## Faits clés {#key-facts}

- Syntaxe de fermeture : `|params| body` - les types sont généralement inférés, les accolades sont facultatives pour une expression unique
- **Pointeur de fonction** (`fn(u32) -> u64`) = pointeur simple vers du code, sans état
- **Fermeture** = structure anonyme contenant l'état capturé + implémentation de trait générée par le compilateur
- Les fermetures capturent par référence par défaut ; le mot-clé `move` force la capture par valeur
- Les trois traits forment une hiérarchie : `Fn` (référence partagée) > `FnMut` (référence exclusive) > `FnOnce` (propriété)
- `Fn` est un sous-trait de `FnMut`, lui-même sous-trait de `FnOnce` ; les pointeurs de fonction implémentent les trois
- Retourner une fermeture depuis une fonction nécessite la syntaxe `impl Fn*` (ou `Box<dyn Fn*>`)

## Motifs {#patterns}

### Variantes de syntaxe des fermetures {#closure-syntax-variants}

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

### Modes de capture {#capture-modes}

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

### Les trois traits des fermetures {#the-three-closure-traits}

```rust
// Fn - shared reference (&self), callable many times
fn apply_fn(f: impl Fn(i32) -> i32, x: i32) -> i32 { f(x) }

// FnMut - exclusive reference (&mut self), callable many times but may mutate
fn apply_mut(mut f: impl FnMut(i32), x: i32) { f(x) }

// FnOnce - ownership (self), callable only once (consumes captured state)
fn apply_once(f: impl FnOnce() -> Vec<i32>) -> Vec<i32> { f() }
```

### Accepter des fermetures (trois syntaxes équivalentes) {#accepting-closures-three-equivalent-syntaxes}

```rust
fn use_f(mut f: impl FnMut(u32, u64) -> u32) { /* ... */ }
fn use_f<F: FnMut(u32, u64) -> u32>(mut f: F) { /* ... */ }
fn use_f<F>(mut f: F) where F: FnMut(u32, u64) -> u32 { /* ... */ }
```

### Retourner des fermetures {#returning-closures}

```rust
fn get_adder(mut x: u32) -> impl FnMut(u32) -> u32 {
    move |a| { x += a; x }
}

let mut adder = get_adder(10);
assert_eq!(adder(5), 15);
assert_eq!(adder(3), 18);
```

### Stocker des fermetures {#storing-closures}

```rust
// Via type parameters (static dispatch, zero-cost)
struct Handler<F: Fn(u32) -> u32> { callback: F }

// Via trait objects (dynamic dispatch, heap allocation)
struct Dispatcher { callbacks: Vec<Box<dyn Fn(u32) -> u32>> }
```

### Bornes de traits de rang supérieur (HRTB) {#higher-rank-trait-bounds-hrtbs}

```rust
// "for any lifetime 'a" - needed when closure takes references
fn apply<F>(f: F) where F: for<'a> Fn(&'a str) -> &'a str {
    let s = String::from("hello");
    println!("{}", f(&s));
}
```

## Pièges {#gotchas}

- `move` capture TOUTES les variables référencées, et pas seulement celles que vous souhaitez : cela peut entraîner un transfert de propriété inattendu
- Les types de fermetures sont anonymes : deux fermetures ayant la même signature ont des types différents (utilisez `dyn Fn` pour les collections hétérogènes)
- Les fermetures `FnOnce` ne peuvent être appelées qu'une seule fois : les appeler deux fois est une erreur de compilation
- En coulisses : le compilateur génère une structure contenant l'état capturé ainsi qu'un appel de méthode, une abstraction à coût nul

## Voir aussi {#see-also}

- [[traits]] - hiérarchie des traits Fn/FnMut/FnOnce
- [[iterators]] - fermetures en argument de map, filter, fold
- [[ownership-and-move-semantics]] - sémantique de déplacement dans les captures de fermetures
- [[generics-and-monomorphization]] - dispatch statique avec impl Trait
