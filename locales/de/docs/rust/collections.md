---
title: "Sammlungen"
category: concepts
tags: [rust, collections, vec, hashmap, string, btreemap, big-o, slices]
level: 3
source_sha256: d87205c7e3692602cdb1f3e04b81918fdd02f8741958dfa3370cced33cc99e73
translation: machine
translated_at: '2026-10-24'
---
# Sammlungen {#collections}

Die Sammlungen (Collections) der Standardbibliothek von Rust speichern Daten auf dem Heap und wachsen dynamisch. `Vec<T>`, `String` und `HashMap<K, V>` sind die gebräuchlichsten. Das Verständnis der Big-O-Komplexität, des Borrowings bei Sammlungen und der Unterscheidung zwischen String und str ist unerlässlich.

## Wichtige Fakten {#key-facts}

- `Vec<T>` = wachsendes Array, amortisiert O(1) beim Push, O(n) beim Einfügen an einem Index
- `HashMap<K, V>` = Hash-Tabelle, im Durchschnitt O(1) beim Lesen und Einfügen
- `BTreeMap<K, V>` = balancierter Baum, O(log n) pro Operation, Schlüssel sind sortiert
- `HashSet<T>` / `BTreeSet<T>` = Mengenvarianten der Map-Typen
- `String` = besitzend, auf dem Heap alloziert, UTF-8-Bytes; `&str` = geliehener UTF-8-Slice
- Strings können nicht über einen Integer indiziert werden (`s[0]` ist ungültig), da UTF-8-Zeichen unterschiedlich breit sind

## Big-O für gängige Operationen {#big-o-for-common-operations}

| Operation | Vec | HashMap | BTreeMap |
|-----------|-----|---------|----------|
| Zugriff per Index/Schlüssel | O(1) | O(1) im Schnitt | O(log n) |
| Einfügen | O(n) mitten, O(1) am Ende | O(1) im Schnitt | O(log n) |
| Entfernen | O(n) | O(1) im Schnitt | O(log n) |
| Enthalten | O(n) | O(1) im Schnitt | O(log n) |
| Iterieren | O(n) | O(n) | O(n) sortiert |

## Muster {#patterns}

### Vec<T> {#vec}

```rust
let mut v = Vec::new();
v.push(1);
v.push(2);

let v = vec![1, 2, 3];  // macro shorthand

// Borrowing
let third: &i32 = &v[2];        // panics if out of bounds
let third: Option<&i32> = v.get(2);  // returns None if out of bounds

// Iteration
for val in &v { }       // immutable borrow
for val in &mut v { }   // mutable borrow
for val in v { }         // takes ownership (v consumed)
```

### HashMap<K, V> {#hashmap}

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();
scores.insert("Alice", 100);
scores.insert("Bob", 85);

// Entry API - insert if absent
scores.entry("Charlie").or_insert(0);

// Update existing
let count = scores.entry("Alice").or_insert(0);
*count += 10;

// From iterators
let map: HashMap<_, _> = vec![("a", 1), ("b", 2)].into_iter().collect();
```

### String-Operationen {#string-operations}

```rust
let mut s = String::from("hello");
s.push(' ');
s.push_str("world");

let s = format!("{} {}", "hello", "world");

// Iteration over chars (not bytes)
for c in "hello".chars() { }
for b in "hello".bytes() { }

// &String → &str coercion via Deref
fn greet(name: &str) { }
let owned = String::from("Alice");
greet(&owned);  // auto-deref to &str
```

## Stolpersteine {#gotchas}

- Ein `&v[0]` darf nicht gehalten werden, während `v` mit `push` erweitert wird – `push` kann neu allokieren und damit Referenzen ungültig machen
- Schlüssel einer HashMap müssen `Eq + Hash` implementieren; Schlüssel einer BTreeMap müssen `Ord` implementieren
- `String::from("hello")` alloziert auf dem Heap; `"hello"` ist ein `&'static str` im Binärprogramm
- `.iter()` liefert Referenzen; `.into_iter()` konsumiert die Sammlung

## Siehe auch {#see-also}

- [[iterators]] - Iterator-Adaptoren für die Verarbeitung von Sammlungen
- [[borrowing-and-references]] - Slices als geliehene Sicht auf Sammlungen
- [[ownership-and-move-semantics]] - Ownership-Übergang bei Sammlungsoperationen
