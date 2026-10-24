---
title: "Itérateurs"
category: patterns
tags: [rust, iterators, map, filter, collect, iterator-trait, lazy, chaining, into-iter]
level: 3
source_sha256: 298b5d1d931b62a606a932ea93317c27d2457ab07caf49cd42b82064253592f5
translation: machine
translated_at: '2026-10-24'
---
# Itérateurs {#iterators}

Les itérateurs Rust sont paresseux, composables et sans coût à l'exécution. Le trait `Iterator` n'exige qu'une seule méthode (`next`), mais fournit gratuitement des dizaines d'adaptateurs (map, filter, fold, etc.). Les itérateurs se compilent vers le même code machine que des boucles écrites à la main, grâce à la monomorphisation - sans surcoût à l'exécution.

## Points clés {#key-facts}

- Trait `Iterator` : `fn next(&mut self) -> Option<Self::Item>` - renvoie `None` lorsque l'itérateur est épuisé
- Les itérateurs sont **paresseux** - aucun calcul n'est effectué tant qu'une méthode consommatrice (collect, sum, for_each) n'est pas appelée
- Trois façons d'itérer : `&v` / `.iter()` (références), `&mut v` / `.iter_mut()` (références mutables), `v` / `.into_iter()` (propriété)
- Le trait `IntoIterator` permet la syntaxe `for x in collection`
- Les itérateurs personnalisés héritent de toutes les méthodes adaptateurs gratuitement en implémentant `Iterator`
- `collect()` peut construire toute collection implémentant `FromIterator` (Vec, HashMap, HashSet, String, etc.)

## Motifs {#patterns}

### Trois modes d'itération {#three-iteration-modes}

```rust
let mut v = vec![1, 2, 3];

for x in &v { }         // immutable references (&i32)
for x in &mut v { }     // mutable references (&mut i32)
for x in v { }           // takes ownership, v consumed
```

### Méthodes adaptateurs clés {#key-adaptor-methods}

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

### Collecter vers différents types {#collect-into-various-types}

```rust
let v = vec![1, 2, 3, 4, 5];

let set: HashSet<_> = v.iter().collect();
let map: HashMap<_, _> = v.iter().enumerate().collect();
let s: String = vec!['h', 'e', 'l', 'l', 'o'].into_iter().collect();
```

### Évaluation paresseuse {#lazy-evaluation}

```rust
// Creates an iterator chain but does NOTHING
let lazy = v.iter().map(|x| {
    println!("processing");  // never printed!
    x * 2
});

// Only when consumed does it execute
let result: Vec<_> = lazy.collect();  // now prints and computes
```

### Itérateurs personnalisés {#custom-iterators}

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

### Trait IntoIterator {#intoiterator-trait}

```rust
// Enables `for x in my_collection`
impl IntoIterator for MyCollection {
    type Item = MyItem;
    type IntoIter = MyIterator;
    fn into_iter(self) -> MyIterator { /* ... */ }
}
```

## Pièges {#gotchas}

- `.iter()` renvoie des références ; `.into_iter()` consomme la collection - les confondre provoque des erreurs d'emprunt
- Une chaîne d'itérateurs ne fait rien sans opération terminale (collect, sum, for_each, count, etc.)
- `collect()` a besoin d'une indication de type - utilisez le turbofish (`::<Vec<_>>`) ou une liaison avec annotation de type
- `s.len()` sur une String renvoie le nombre d'octets, et non de caractères - utilisez `s.chars().count()` pour compter les caractères

## Voir aussi {#see-also}

- [[closures]] - closures passées en arguments aux adaptateurs d'itérateurs
- [[collections]] - Vec, HashMap et leurs interfaces d'itération
- [[traits]] - trait Iterator et types associés
