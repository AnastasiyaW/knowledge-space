---
title: "Pointeurs intelligents"
category: concepts
tags: [rust, smart-pointers, box, rc, arc, refcell, interior-mutability, heap]
level: 4
source_sha256: d5f5e5ce48fd5252e2b3d874c70fe5a5f5eda0f76f0f63e51278a4009f4cff32
translation: machine
translated_at: '2026-10-24'
---
# Pointeurs intelligents {#smart-pointers}

Les pointeurs intelligents sont des structures de données qui se comportent comme des pointeurs, mais qui disposent de métadonnées et de capacités supplémentaires. Ils implémentent `Deref` (pour le déréférencement transparent) et `Drop` (pour le nettoyage automatique). Les principaux pointeurs intelligents sont `Box<T>`, `Rc<T>`, `Arc<T>`, `RefCell<T>` et `Cow<T>`.

## Points clés {#key-facts}

- **Box<T>** = allocation sur le tas avec propriété unique, abstraction à coût nul (simplement un pointeur)
- **Rc<T>** = comptage de références, plusieurs propriétaires, mono-thread uniquement
- **Arc<T>** = comptage de références atomique, plusieurs propriétaires, thread-safe
- **RefCell<T>** = mutabilité intérieure avec vérification des emprunts à l'exécution
- **Cow<T>** = clone-on-write, évite une allocation lorsque les données n'ont pas besoin d'être modifiées
- `Box<T>` est le plus courant : il sert pour les types récursifs, les objets trait et les déplacements de la pile vers le tas de grande taille

## Patterns {#patterns}

### Box<T> - Allocation sur le tas {#box-heap-allocation}

```rust
// Recursive type (requires known size)
enum List {
    Cons(i32, Box<List>),
    Nil,
}

// Trait objects
let animal: Box<dyn Animal> = Box::new(Dog { name: "Rex".into() });

// Large data on heap
let big_array = Box::new([0u8; 1_000_000]);
```

### Rc<T> - Comptage de références {#rc-reference-counting}

```rust
use std::rc::Rc;

let a = Rc::new(vec![1, 2, 3]);
let b = Rc::clone(&a);  // increment reference count (cheap)
let c = Rc::clone(&a);

println!("References: {}", Rc::strong_count(&a)); // 3
// Data dropped when last Rc goes out of scope
```

### RefCell<T> - Mutabilité intérieure {#refcell-interior-mutability}

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// Runtime borrow checking
let borrowed = data.borrow();      // immutable borrow
// data.borrow_mut();              // PANIC: already borrowed immutably
drop(borrowed);

data.borrow_mut().push(4);         // OK: no active borrows
```

### Combinaisons courantes {#common-combinations}

```rust
// Multiple owners with mutability (single-threaded)
let shared = Rc::new(RefCell::new(HashMap::new()));

// Multiple owners with mutability (multi-threaded)
let shared = Arc::new(Mutex::new(HashMap::new()));
```

## Pièges {#gotchas}

- `Rc<T>` peut créer des cycles de références → fuites mémoire ; utilisez `Weak<T>` pour rompre les cycles
- `RefCell<T>` panique à l'exécution si les règles d'emprunt sont violées : la sûreté à la compilation est échangée contre de la souplesse
- `Rc<T>` n'est PAS thread-safe (utilisez `Arc<T>` pour le multithreading)
- `Box<T>` déplace les données sur le tas, mais la Box elle-même reste sur la pile (de la taille d'un pointeur)

## Voir aussi {#see-also}

- [[ownership-and-move-semantics]] - modèle de propriété que les pointeurs intelligents étendent
- [Concurrency](concurrency.md) - Arc + Mutex pour un état partagé thread-safe
- [[traits]] - traits Deref et Drop qui alimentent les pointeurs intelligents
