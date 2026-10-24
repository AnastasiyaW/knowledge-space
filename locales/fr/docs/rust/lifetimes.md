---
title: "Durées de vie"
category: concepts
tags: [rust, lifetimes, borrow-checker, references, annotations, elision, static, nll]
level: 4
source_sha256: d577fa6f2dc709a9d8281e8eadcaf6b7623ca24b8f3776614824e2b6b0aea498
translation: machine
translated_at: '2026-10-24'
---
# Durées de vie {#lifetimes}

Les durées de vie (lifetimes) sont le mécanisme du compilateur pour suivre combien de temps les références restent valides. Elles empêchent les références pendantes à la compilation, sans ramasse-miettes. La plupart des durées de vie sont inférées automatiquement grâce aux règles d'élision ; des annotations explicites (`'a`) sont nécessaires lorsque le compilateur ne peut pas déterminer la relation entre les références d'entrée et de sortie.

## Points clés {#key-facts}

- Les annotations de durée de vie ne modifient pas la durée de vie des données : elles décrivent les relations entre références
- `'a` se lit « durée de vie a » : une région nommée du code où une référence est valide
- Les **règles d'élision** traitent la plupart des cas automatiquement (une seule référence en entrée, méthodes `&self`)
- `'static` = référence valide pendant toute la durée du programme (littéraux de chaînes, données fuitées)
- **NLL (Non-Lexical Lifetimes)** : le vérificateur d'emprunts analyse l'usage réel, et non uniquement les portées lexicales
- Les structs contenant des références doivent déclarer des paramètres de durée de vie : `struct Foo<'a> { data: &'a str }`

## Schémas {#patterns}

### Annotations de durée de vie explicites {#explicit-lifetime-annotations}

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

### Règles d'élision des durées de vie {#lifetime-elision-rules}

Le compilateur infère les durées de vie dans trois cas :
1. Chaque référence en entrée reçoit son propre paramètre de durée de vie
2. S'il n'y a qu'une seule durée de vie en entrée, elle est attribuée à toutes les sorties
3. Si l'une des entrées est `&self` ou `&mut self`, sa durée de vie est attribuée à toutes les sorties

```rust
// These are equivalent (rule 2):
fn first(s: &str) -> &str { &s[..1] }
fn first<'a>(s: &'a str) -> &'a str { &s[..1] }

// Method: self's lifetime used for output (rule 3):
impl MyStruct {
    fn name(&self) -> &str { &self.name }
}
```

### Durées de vie dans les structs {#struct-lifetimes}

```rust
struct Important<'a> {
    content: &'a str,
}

// Struct cannot outlive the reference it holds
let novel = String::from("Call me Ishmael...");
let i = Important { content: &novel };
// novel must live at least as long as i
```

### Durée de vie `'static` {#static-lifetime}

```rust
// String literals are always 'static
let s: &'static str = "I live forever";

// 'static as trait bound: type contains no non-static references
fn spawn_thread<T: Send + 'static>(data: T) { /* ... */ }

// Leaking to get 'static (rare, use carefully)
let leaked: &'static str = Box::leak(String::from("leaked").into_boxed_str());
```

### Mutabilité intérieure (contourner le vérificateur d'emprunts à l'exécution) {#interior-mutability-bypassing-borrow-checker-at-runtime}

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

## Pièges {#gotchas}

- Le compilateur ne peut pas analyser le flot de contrôle pour les emprunts : même `if true { &mut x } else { &y }` peut le dérouter ; il faut restructurer le code
- L'API Entry de HashMap existe précisément parce que le vérificateur d'emprunts ne gérait pas les schémas « recherche puis insertion »
- `Cell`/`RefCell` sont Send mais PAS Sync : mono-thread uniquement (utiliser `Mutex`/`RwLock` pour le multi-thread)
- `'static` ne signifie pas « vit éternellement » en tant que contrainte : cela signifie « ne contient aucune référence non statique » (les types possédants comme `String` sont `'static`)

## Voir aussi {#see-also}

- [[borrowing-and-references]] - règles d'emprunt que les durées de vie font respecter
- [Pointeurs intelligents](smart-pointers.md) - RefCell pour la mutabilité intérieure, Rc/Arc pour la propriété partagée
- [Concurrence](concurrency.md) - contrainte 'static sur les threads lancés
- [[generics-and-monomorphization]] - paramètres de durée de vie dans le code générique
