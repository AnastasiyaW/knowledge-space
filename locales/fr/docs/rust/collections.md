---
title: "Collections"
category: concepts
tags: [rust, collections, vec, hashmap, string, btreemap, big-o, slices]
level: 3
source_sha256: d87205c7e3692602cdb1f3e04b81918fdd02f8741958dfa3370cced33cc99e73
translation: machine
translated_at: '2026-10-24'
---
# Collections {#collections}

Les collections de la bibliothèque standard de Rust stockent leurs données sur le tas et croissent dynamiquement. `Vec<T>`, `String` et `HashMap<K, V>` sont les plus courantes. Comprendre la complexité Big O, l'emprunt avec les collections et la distinction entre String et str est essentiel.

## Faits clés {#key-facts}

- `Vec<T>` = tableau extensible, push en O(1) amorti, insertion à un index en O(n)
- `HashMap<K, V>` = table de hachage, recherche/insertion en O(1) en moyenne
- `BTreeMap<K, V>` = arbre équilibré, opérations en O(log n), les clés sont triées
- `HashSet<T>` / `BTreeSet<T>` = variantes ensemblistes des types Map
- `String` = possédée, allouée sur le tas, octets UTF-8 ; `&str` = tranche UTF-8 empruntée
- Les chaînes ne peuvent pas être indexées par un entier (`s[0]` est invalide) car les caractères UTF-8 ont une largeur variable

## Big O pour les opérations courantes {#big-o-for-common-operations}

| Opération | Vec | HashMap | BTreeMap |
|-----------|-----|---------|----------|
| Lecture par index/clé | O(1) | O(1) moy. | O(log n) |
| Insertion | O(n) au milieu, O(1) en fin | O(1) moy. | O(log n) |
| Suppression | O(n) | O(1) moy. | O(log n) |
| Contient | O(n) | O(1) moy. | O(log n) |
| Itération | O(n) | O(n) | O(n) trié |

## Motifs {#patterns}

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

### Opérations sur String {#string-operations}

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

## Pièges {#gotchas}

- Impossible de conserver `&v[0]` tout en poussant dans `v` : push peut réallouer et invalider les références
- Les clés de HashMap doivent implémenter `Eq + Hash` ; les clés de BTreeMap doivent implémenter `Ord`
- `String::from("hello")` alloue sur le tas ; `"hello"` est un `&'static str` présent dans le binaire
- `.iter()` renvoie des références ; `.into_iter()` consomme la collection

## Voir aussi {#see-also}

- [[iterators]] - adaptateurs d'itérateurs pour le traitement des collections
- [[borrowing-and-references]] - tranches comme vues empruntées sur une collection
- [[ownership-and-move-semantics]] - transfert de propriété dans les opérations sur les collections
