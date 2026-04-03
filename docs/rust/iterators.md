---
title: Iterators
category: patterns
tags: [rust, iterators, map, filter, collect, iterator-trait, lazy, chaining, into-iter]
---

# Iterators

Rust iterators are lazy, composable, and zero-cost. The `Iterator` trait requires only one method (`next`), but provides dozens of adaptors (map, filter, fold, etc.) for free. Iterators compile to the same machine code as hand-written loops thanks to monomorphization - no runtime overhead.

## Key Facts

- `Iterator` trait: `fn next(&mut self) -> Option<Self::Item>` - returns `None` when exhausted
- Iterators are **lazy** - no computation until a consuming method (collect, sum, for_each) is called
- Three ways to iterate: `&v` / `.iter()` (references), `&mut v` / `.iter_mut()` (mutable refs), `v` / `.into_iter()` (ownership)
- `IntoIterator` trait enables `for x in collection` syntax
- Custom iterators get all adaptor methods for free by implementing `Iterator`
- `collect()` can build any collection that implements `FromIterator` (Vec, HashMap, HashSet, String, etc.)

## Patterns

### Three Iteration Modes

```rust
let mut v = vec![1, 2, 3];

for x in &v { }         // immutable references (&i32)
for x in &mut v { }     // mutable references (&mut i32)
for x in v { }           // takes ownership, v consumed
```

### Key Adaptor Methods

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

### Collect into Various Types

```rust
let v = vec![1, 2, 3, 4, 5];

let set: HashSet<_> = v.iter().collect();
let map: HashMap<_, _> = v.iter().enumerate().collect();
let s: String = vec!['h', 'e', 'l', 'l', 'o'].into_iter().collect();
```

### Lazy Evaluation

```rust
// Creates an iterator chain but does NOTHING
let lazy = v.iter().map(|x| {
    println!("processing");  // never printed!
    x * 2
});

// Only when consumed does it execute
let result: Vec<_> = lazy.collect();  // now prints and computes
```

### Custom Iterators

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

### IntoIterator Trait

```rust
// Enables `for x in my_collection`
impl IntoIterator for MyCollection {
    type Item = MyItem;
    type IntoIter = MyIterator;
    fn into_iter(self) -> MyIterator { /* ... */ }
}
```

## Gotchas

- `.iter()` returns references; `.into_iter()` consumes the collection - mixing them up causes borrow errors
- Chained iterators do nothing without a terminal operation (collect, sum, for_each, count, etc.)
- `collect()` needs a type hint - use turbofish (`::<Vec<_>>`) or let-binding with type annotation
- `s.len()` on String returns byte count, not char count - use `s.chars().count()` for characters

## See Also

- [[closures]] - closures as arguments to iterator adaptors
- [[collections]] - Vec, HashMap, and their iteration interfaces
- [[traits]] - Iterator trait and associated types
