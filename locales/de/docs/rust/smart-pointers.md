---
title: "Smart Pointers"
category: concepts
tags: [rust, smart-pointers, box, rc, arc, refcell, interior-mutability, heap]
level: 4
source_sha256: d5f5e5ce48fd5252e2b3d874c70fe5a5f5eda0f76f0f63e51278a4009f4cff32
translation: machine
translated_at: '2026-10-24'
---
# Smart Pointers {#smart-pointers}

Smart Pointers sind Datenstrukturen, die sich wie Zeiger verhalten, aber zusätzliche Metadaten und Fähigkeiten besitzen. Sie implementieren `Deref` (für transparente Dereferenzierung) und `Drop` (für automatische Bereinigung). Die wichtigsten Smart Pointers sind `Box<T>`, `Rc<T>`, `Arc<T>`, `RefCell<T>` und `Cow<T>`.

## Key Facts {#key-facts}

- **Box<T>** = Heap-Allokation mit alleinigem Ownership, Zero-Cost-Abstraktion (nur ein Zeiger)
- **Rc<T>** = Reference Counting, mehrere Owner, nur single-threaded
- **Arc<T>** = atomares Reference Counting, mehrere Owner, thread-sicher
- **RefCell<T>** = Interior Mutability mit Borrow-Prüfung zur Laufzeit
- **Cow<T>** = Clone-on-Write, vermeidet Allokation, wenn Daten nicht verändert werden müssen
- `Box<T>` ist der häufigste – er wird für rekursive Typen, Trait Objects und große Verschiebungen vom Stack auf den Heap verwendet

## Patterns {#patterns}

### Box<T> - Heap-Allokation {#box-heap-allocation}

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

### Rc<T> - Reference Counting {#rc-reference-counting}

```rust
use std::rc::Rc;

let a = Rc::new(vec![1, 2, 3]);
let b = Rc::clone(&a);  // increment reference count (cheap)
let c = Rc::clone(&a);

println!("References: {}", Rc::strong_count(&a)); // 3
// Data dropped when last Rc goes out of scope
```

### RefCell<T> - Interior Mutability {#refcell-interior-mutability}

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// Runtime borrow checking
let borrowed = data.borrow();      // immutable borrow
// data.borrow_mut();              // PANIC: already borrowed immutably
drop(borrowed);

data.borrow_mut().push(4);         // OK: no active borrows
```

### Common Combinations {#common-combinations}

```rust
// Multiple owners with mutability (single-threaded)
let shared = Rc::new(RefCell::new(HashMap::new()));

// Multiple owners with mutability (multi-threaded)
let shared = Arc::new(Mutex::new(HashMap::new()));
```

## Gotchas {#gotchas}

- `Rc<T>` kann Referenzzyklen erzeugen → Speicherlecks; mit `Weak<T>` lassen sich Zyklen aufbrechen
- `RefCell<T>` panikt zur Laufzeit, wenn die Borrow-Regeln verletzt werden – Sicherheit zur Compile-Zeit wird gegen Flexibilität getauscht
- `Rc<T>` ist NICHT thread-sicher (für Multithreading `Arc<T>` verwenden)
- `Box<T>` verschiebt die Daten auf den Heap, die Box selbst liegt aber auf dem Stack (so groß wie ein Zeiger)

## See Also {#see-also}

- [[ownership-and-move-semantics]] - Ownership-Modell, das Smart Pointers erweitern
- [Concurrency](concurrency.md) - Arc + Mutex für thread-sicheren geteilten Zustand
- [[traits]] - Deref- und Drop-Traits, auf denen Smart Pointers basieren
