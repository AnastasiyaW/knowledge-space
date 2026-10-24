---
title: "Iteratoren"
category: patterns
tags: [rust, iterators, map, filter, collect, iterator-trait, lazy, chaining, into-iter]
level: 3
source_sha256: 298b5d1d931b62a606a932ea93317c27d2457ab07caf49cd42b82064253592f5
translation: machine
translated_at: '2026-10-24'
---
# Iteratoren {#iterators}

Rust-Iteratoren sind lazy, komponierbar und zero-cost. Das `Iterator`-Trait erfordert nur eine Methode (`next`), stellt aber dutzende Adaptoren (map, filter, fold usw.) kostenlos bereit. Dank Monomorphisierung kompilieren Iteratoren zu demselben Maschinencode wie handgeschriebene Schleifen - ohne Laufzeit-Overhead.

## Key Facts {#key-facts}

- `Iterator`-Trait: `fn next(&mut self) -> Option<Self::Item>` - gibt `None` zurück, wenn der Iterator erschöpft ist
- Iteratoren sind **lazy** - es wird nichts berechnet, bis eine verbrauchende Methode (collect, sum, for_each) aufgerufen wird
- Drei Arten der Iteration: `&v` / `.iter()` (Referenzen), `&mut v` / `.iter_mut()` (veränderliche Referenzen), `v` / `.into_iter()` (Ownership)
- Das `IntoIterator`-Trait ermöglicht die Syntax `for x in collection`
- Eigene Iteratoren erhalten alle Adaptor-Methoden kostenlos, indem sie `Iterator` implementieren
- `collect()` kann jede Collection aufbauen, die `FromIterator` implementiert (Vec, HashMap, HashSet, String usw.)

## Patterns {#patterns}

### Three Iteration Modes {#three-iteration-modes}

```rust
let mut v = vec![1, 2, 3];

for x in &v { }         // immutable references (&i32)
for x in &mut v { }     // mutable references (&mut i32)
for x in v { }           // takes ownership, v consumed
```

### Key Adaptor Methods {#key-adaptor-methods}

```rust
let v = vec![1, 2, 3, 4, 5];

// Transform
v.iter().map(|x| x * 2)                    // [2, 4, 6, 8, 10]

// Filter
v.iter().filter(|&&x| x > 2)               // [3, 4, 5]

// Fold (reduce with initial value)
v.iter().fold(0, |acc, x| acc + x)          // 15
v.iter().sum::<i32>()                        // 15

// Chain and zip
let a = [1, 2];
let b = [3, 4];
a.iter().chain(b.iter())                     // [1, 2, 3, 4]
a.iter().zip(b.iter())                       // [(1,3), (2,4)]

// Take and skip
v.iter().take(3)                             // [1, 2, 3]
v.iter().skip(2)                             // [3, 4, 5]

// Enumerate
v.iter().enumerate()                         // [(0,1), (1,2), ...]

// Flatten nested iterators
vec![vec![1, 2], vec![3, 4]].into_iter().flatten()  // [1, 2, 3, 4]

// flat_map = map + flatten
v.iter().flat_map(|&x| vec![x, x * 10])

// Search
v.iter().find(|&&x| x > 3)                  // Some(&4)
v.iter().any(|&x| x > 4)                    // true
v.iter().all(|&x| x > 0)                    // true
```

### Collect into Various Types {#collect-into-various-types}

```rust
let v = vec![1, 2, 3, 4, 5];

let set: HashSet<_> = v.iter().collect();
let map: HashMap<_, _> = v.iter().enumerate().collect();
let s: String = vec!['h', 'e', 'l', 'l', 'o'].into_iter().collect();
```

### Lazy Evaluation {#lazy-evaluation}

```rust
// Creates an iterator chain but does NOTHING
let lazy = v.iter().map(|x| {
    println!("processing");  // never printed!
    x * 2
});

// Only when consumed does it execute
let result: Vec<_> = lazy.collect();  // now prints and computes
```

### Custom Iterators {#custom-iterators}

```rust
struct Counter { count: u32, max: u32 }

impl Iterator for Counter {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        if self.count < self.max {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

// All adaptor methods available for free
Counter { count: 0, max: 5 }
    .filter(|x| x % 2 == 0)
    .sum::<u32>()  // 6 (2 + 4)
```

### IntoIterator Trait {#intoiterator-trait}

```rust
// Enables `for x in my_collection`
impl IntoIterator for MyCollection {
    type Item = MyItem;
    type IntoIter = MyIterator;
    fn into_iter(self) -> MyIterator { /* ... */ }
}
```

## Gotchas {#gotchas}

- `.iter()` gibt Referenzen zurück; `.into_iter()` konsumiert die Collection - eine Verwechslung führt zu Borrow-Fehlern
- Verkettete Iteratoren tun nichts ohne eine terminale Operation (collect, sum, for_each, count usw.)
- `collect()` benötigt einen Typhinweis - entweder Turbofish (`::<Vec<_>>`) oder eine Let-Bindung mit Typannotation
- `s.len()` auf String gibt die Anzahl der Bytes zurück, nicht der Zeichen - für Zeichen `s.chars().count()` verwenden

## See Also {#see-also}

- [[closures]] - Closures als Argumente für Iterator-Adaptoren
- [[collections]] - Vec, HashMap und deren Iterationsschnittstellen
- [[traits]] - Iterator-Trait und assoziierte Typen
