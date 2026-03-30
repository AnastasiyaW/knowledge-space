---
title: Collections
category: reference
tags: [vec, hashmap, string, vecdeque, btreemap, collections]
---
# Collections

Standard library collections for storing multiple values on the heap, with `Vec`, `HashMap`, and `String` being the most commonly used.

## Key Facts

- `Vec<T>` - growable array; contiguous memory; O(1) push/pop at end; O(n) insert/remove at front
- `VecDeque<T>` - double-ended queue; O(1) push/pop at both ends (ring buffer)
- `HashMap<K, V>` - hash table; K must implement `Eq + Hash`; average O(1) lookup
- `BTreeMap<K, V>` - sorted map; K must implement `Ord`; O(log n) operations
- `HashSet<T>` / `BTreeSet<T>` - sets (implemented as maps with `()` values)
- `String` is `Vec<u8>` with guaranteed UTF-8; `&str` is a string slice (fat pointer)
- `String` indexing by byte range panics on non-UTF-8 boundaries; direct index `s[0]` is not allowed
- Common interface: `new()`, `with_capacity(n)`, `len()`, `is_empty()`, `clear()`
- `with_capacity()` pre-allocates to avoid repeated reallocation

## Patterns

```rust
// Vec creation and usage
let mut v: Vec<i32> = Vec::new();
let v2 = vec![1, 2, 3, 4, 5];
let zeros = vec![0; 10];           // 10 zeros

v.push(1);
v.push(2);
let last = v.pop();                // Some(2)
v.insert(0, 10);                   // insert at index
v.remove(0);                       // remove at index, shifts elements
v.swap_remove(0);                  // remove, swap with last (O(1))
v.sort();
v.sort_unstable();                 // faster, no stability guarantee
v.dedup();                         // remove consecutive duplicates

// Vec as slice
let slice: &[i32] = &v[1..3];
let first: &[i32] = &v[..1];

// Vec with capacity
let mut buf = Vec::with_capacity(1024);
// no allocations for the first 1024 pushes

// HashMap
use std::collections::HashMap;

let mut scores: HashMap<String, i32> = HashMap::new();
scores.insert("Alice".into(), 100);
scores.insert("Bob".into(), 85);

// Lookup
if let Some(score) = scores.get("Alice") {
    println!("Alice: {score}");
}

// Entry API (get-or-insert pattern)
scores.entry("Carol".into()).or_insert(0);

let text = "hello world hello";
let mut word_count = HashMap::new();
for word in text.split_whitespace() {
    *word_count.entry(word).or_insert(0) += 1;
}

// Iteration
for (key, value) in &scores {
    println!("{key}: {value}");
}

// Custom hasher
// use fnv::FnvHashMap;
// let mut map = FnvHashMap::default();

// String operations
let mut s = String::from("hello");
s.push_str(" world");             // append &str
s.push('!');                       // append char
let len = s.len();                 // byte length

// String concatenation (4 ways)
let a = String::from("hello");
let b = String::from(" world");
// 1. push_str - modifies in place
// 2. + operator - moves left operand
let c = a + &b;                    // a is moved
// 3. format! - copies both
let d = format!("{}{}", c, b);
// 4. concat on slice
let e = ["hello", " ", "world"].concat();

// String iteration
for c in "hello".chars() { /* char by char */ }
for b in "hello".bytes() { /* byte by byte */ }
for (i, c) in "hello".char_indices() { /* index + char */ }

// UTF-8 awareness
let emoji = "a]";
assert_eq!(emoji.len(), 5);        // bytes
assert_eq!(emoji.chars().count(), 2); // characters

// VecDeque
use std::collections::VecDeque;
let mut dq = VecDeque::new();
dq.push_back(1);
dq.push_front(0);
let front = dq.pop_front();       // Some(0)

// Custom Hash impl
use std::hash::{Hash, Hasher};
struct Person { id: u32, name: String }
impl Hash for Person {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.id.hash(state);       // hash only by id
    }
}
```

## Gotchas

- **Symptom**: `String` index with `s[0]` fails - **Cause**: Rust prevents single-byte indexing since chars can be multi-byte UTF-8 - **Fix**: use `s.chars().nth(0)`, `s.as_bytes()[0]`, or `&s[0..1]` (panics if not char boundary)
- **Symptom**: `HashMap` iteration order changes between runs - **Cause**: random hash seed for DoS protection - **Fix**: use `BTreeMap` for deterministic order, or `indexmap` crate for insertion order
- **Symptom**: `Vec::push` causes unexpected re-allocation - **Cause**: capacity exceeded, entire buffer copied - **Fix**: use `with_capacity()` when size is known; avoid holding references across pushes
- **Symptom**: "cannot borrow as mutable because it is also borrowed as immutable" with `HashMap` get + insert - **Cause**: get returns reference that conflicts with mutable insert - **Fix**: use Entry API: `map.entry(key).or_insert(value)`

## See Also

- [[borrowing-and-references]] - slices and string slices
- [[iterators]] - iterator methods on collections
- [[traits]] - `Hash`, `Eq`, `Ord` trait requirements
- [The Rust Book - Collections](https://doc.rust-lang.org/book/ch08-00-common-collections.html)
- [std::collections](https://doc.rust-lang.org/std/collections/index.html)
