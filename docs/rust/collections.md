---
title: Collections
category: concepts
tags: [rust, collections, vec, hashmap, string, btreemap, big-o, slices]
---

# Collections

Rust's standard library collections store data on the heap and grow dynamically. `Vec<T>`, `String`, and `HashMap<K, V>` are the most common. Understanding Big O complexity, borrowing with collections, and the String/str distinction is essential.

## Key Facts

- `Vec<T>` = growable array, O(1) amortized push, O(n) insert at index
- `HashMap<K, V>` = hash table, O(1) average lookup/insert
- `BTreeMap<K, V>` = balanced tree, O(log n) operations, keys are sorted
- `HashSet<T>` / `BTreeSet<T>` = set variants of Map types
- `String` = owned, heap-allocated, UTF-8 bytes; `&str` = borrowed UTF-8 slice
- Strings cannot be indexed by integer (`s[0]` is invalid) because UTF-8 chars are variable-width

## Big O for Common Operations

| Operation | Vec | HashMap | BTreeMap |
|-----------|-----|---------|----------|
| Get by index/key | O(1) | O(1) avg | O(log n) |
| Insert | O(n) mid, O(1) end | O(1) avg | O(log n) |
| Remove | O(n) | O(1) avg | O(log n) |
| Contains | O(n) | O(1) avg | O(log n) |
| Iterate | O(n) | O(n) | O(n) sorted |

## Patterns

### Vec<T>

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

### HashMap<K, V>

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

### String Operations

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

## Gotchas

- Cannot hold `&v[0]` while pushing to `v` - push may reallocate, invalidating references
- HashMap keys must implement `Eq + Hash`; BTreeMap keys must implement `Ord`
- `String::from("hello")` allocates on heap; `"hello"` is `&'static str` in binary
- `.iter()` returns references; `.into_iter()` consumes the collection

## See Also

- [[iterators]] - iterator adaptors for collection processing
- [[borrowing-and-references]] - slices as borrowed collection views
- [[ownership-and-move-semantics]] - ownership transfer in collection operations
