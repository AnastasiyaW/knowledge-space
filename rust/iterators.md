---
title: Iterators
category: patterns
tags: [iterators, map, filter, collect, iterator-trait, lazy, chaining]
---
# Iterators

Iterators provide a lazy, composable way to process sequences of elements; they are zero-cost abstractions that compile to efficient loops.

## Key Facts

- `Iterator` trait requires one method: `fn next(&mut self) -> Option<Self::Item>`
- Iterators are lazy - no work is done until consumed (`.collect()`, `.for_each()`, `.count()`, etc.)
- Three iteration methods: `.iter()` (`&T`), `.iter_mut()` (`&mut T`), `.into_iter()` (owned `T`)
- `for x in collection` calls `.into_iter()` implicitly
- Adapter methods (lazy): `map`, `filter`, `flat_map`, `take`, `skip`, `zip`, `enumerate`, `chain`, `peekable`
- Consumer methods (execute): `collect`, `sum`, `count`, `any`, `all`, `find`, `fold`, `for_each`, `min`, `max`
- `.collect()` is generic - use turbofish or type annotation: `collect::<Vec<_>>()`
- Custom iterators: implement `Iterator` for your struct
- `IntoIterator` trait enables `for` loop support

## Patterns

```rust
// Basic iteration
let v = vec![1, 2, 3, 4, 5];
let sum: i32 = v.iter().sum();

// Method chaining
let result: Vec<i32> = v.iter()
    .filter(|&&x| x > 2)
    .map(|&x| x * 10)
    .collect();
// [30, 40, 50]

// enumerate
for (i, val) in v.iter().enumerate() {
    println!("{i}: {val}");
}

// zip
let names = vec!["Alice", "Bob"];
let scores = vec![95, 87];
let paired: Vec<_> = names.iter().zip(scores.iter()).collect();
// [("Alice", 95), ("Bob", 87)]

// flat_map
let words: Vec<&str> = vec!["hello world", "foo bar"]
    .iter()
    .flat_map(|s| s.split_whitespace())
    .collect();
// ["hello", "world", "foo", "bar"]

// fold (reduce)
let sum = v.iter().fold(0, |acc, &x| acc + x);

// chain
let combined: Vec<i32> = (1..=3).chain(7..=9).collect();
// [1, 2, 3, 7, 8, 9]

// take and skip
let first_three: Vec<_> = v.iter().take(3).collect();
let after_two: Vec<_> = v.iter().skip(2).collect();

// find and position
let found = v.iter().find(|&&x| x > 3);       // Some(&4)
let pos = v.iter().position(|&x| x == 3);     // Some(2)

// any and all
let has_even = v.iter().any(|&x| x % 2 == 0); // true
let all_pos = v.iter().all(|&x| x > 0);       // true

// Collect into different types
let s: String = vec!['h', 'e', 'l', 'l', 'o'].into_iter().collect();
let set: std::collections::HashSet<i32> = v.into_iter().collect();
let result: Result<Vec<i32>, _> = vec!["1", "2", "3"]
    .iter()
    .map(|s| s.parse::<i32>())
    .collect(); // Ok([1, 2, 3]) or first Err

// Custom iterator
struct Fibonacci {
    a: u64,
    b: u64,
}
impl Fibonacci {
    fn new() -> Self { Self { a: 0, b: 1 } }
}
impl Iterator for Fibonacci {
    type Item = u64;
    fn next(&mut self) -> Option<u64> {
        let result = self.a;
        self.a = self.b;
        self.b = result + self.b;
        Some(result)
    }
}
let fibs: Vec<u64> = Fibonacci::new().take(10).collect();

// IntoIterator for custom types
struct Grid { cells: Vec<Vec<i32>> }
impl IntoIterator for Grid {
    type Item = i32;
    type IntoIter = std::vec::IntoIter<i32>;
    fn into_iter(self) -> Self::IntoIter {
        self.cells.into_iter().flatten().collect::<Vec<_>>().into_iter()
    }
}

// Consuming vs borrowing iteration
let v = vec![1, 2, 3];
for x in &v { }         // v.iter()      -> &i32, v still usable
for x in &mut v { }     // v.iter_mut()  -> &mut i32
for x in v { }           // v.into_iter() -> i32, v consumed
```

## Gotchas

- **Symptom**: iterator does nothing - **Cause**: adapters are lazy; no consumer called - **Fix**: add `.collect()`, `.for_each()`, `.count()`, or another consumer
- **Symptom**: "type annotations needed" on `.collect()` - **Cause**: compiler can't infer target collection type - **Fix**: annotate variable type or use turbofish `.collect::<Vec<_>>()`
- **Symptom**: `iter()` vs `into_iter()` confusion - `iter()` borrows elements, `into_iter()` takes ownership - **Fix**: use `iter()` when you need the collection afterwards
- **Symptom**: chained iterator is slow - **Cause**: usually not; iterators are zero-cost abstractions - **Fix**: verify with benchmarks; the compiler optimizes iterator chains into fused loops

## See Also

- [[closures]] - closures as arguments to iterator methods
- [[collections]] - collections that implement `IntoIterator`
- [[traits]] - `Iterator` and `IntoIterator` trait definitions
- [[rust/error-handling]] - collecting `Result` iterators
- [The Rust Book - Iterators](https://doc.rust-lang.org/book/ch13-02-iterators.html)
- [std::iter::Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)
