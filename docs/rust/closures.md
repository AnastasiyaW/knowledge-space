---
title: Closures
category: concepts
tags: [rust, closures, fn, fnmut, fnonce, move, lambda, capture, higher-order]
---

# Closures

Closures are anonymous functions that can capture variables from their enclosing scope. Unlike function pointers (`fn`), closures carry state. The compiler generates an anonymous struct for each closure, implementing one of three traits: `Fn`, `FnMut`, or `FnOnce` - determining how the closure uses its captured state.

## Key Facts

- Closure syntax: `|params| body` - types usually inferred, braces optional for single expressions
- **Function pointer** (`fn(u32) -> u64`) = thin pointer to code, no state
- **Closure** = anonymous struct with captured state + compiler-generated trait impl
- Closures capture by reference by default; `move` keyword forces capture by value
- Three traits form a hierarchy: `Fn` (shared ref) > `FnMut` (exclusive ref) > `FnOnce` (owned)
- `Fn` is a subtrait of `FnMut`, which is a subtrait of `FnOnce`; function pointers implement all three
- Returning closures from functions requires `impl Fn*` syntax (or `Box<dyn Fn*>`)

## Patterns

### Closure Syntax Variants

```rust
// Type inference (most common)
|a, b| a + b

// Explicit types
|a: u32, b: u32| -> u32 { a + b }

// Multi-line with braces
|x| {
    let y = x * 2;
    y + 1
}
```

### Capture Modes

```rust
let mut x = 0u32;

// Captures &mut x (inferred from mutation)
let mut add_to_x = |a| x += a;
add_to_x(1);
add_to_x(2);
// x is now 3

// move: captures ALL referenced variables by value
let data = vec![1, 2, 3];
let closure = move || println!("{:?}", data);
// data is no longer accessible here
```

### The Three Closure Traits

```rust
// Fn - shared reference (&self), callable many times
fn apply_fn(f: impl Fn(i32) -> i32, x: i32) -> i32 { f(x) }

// FnMut - exclusive reference (&mut self), callable many times but may mutate
fn apply_mut(mut f: impl FnMut(i32), x: i32) { f(x) }

// FnOnce - ownership (self), callable only once (consumes captured state)
fn apply_once(f: impl FnOnce() -> Vec<i32>) -> Vec<i32> { f() }
```

### Accepting Closures (Three Equivalent Syntaxes)

```rust
fn use_f(mut f: impl FnMut(u32, u64) -> u32) { /* ... */ }
fn use_f<F: FnMut(u32, u64) -> u32>(mut f: F) { /* ... */ }
fn use_f<F>(mut f: F) where F: FnMut(u32, u64) -> u32 { /* ... */ }
```

### Returning Closures

```rust
fn get_adder(mut x: u32) -> impl FnMut(u32) -> u32 {
    move |a| { x += a; x }
}

let mut adder = get_adder(10);
assert_eq!(adder(5), 15);
assert_eq!(adder(3), 18);
```

### Storing Closures

```rust
// Via type parameters (static dispatch, zero-cost)
struct Handler<F: Fn(u32) -> u32> { callback: F }

// Via trait objects (dynamic dispatch, heap allocation)
struct Dispatcher { callbacks: Vec<Box<dyn Fn(u32) -> u32>> }
```

### Higher-Rank Trait Bounds (HRTBs)

```rust
// "for any lifetime 'a" - needed when closure takes references
fn apply<F>(f: F) where F: for<'a> Fn(&'a str) -> &'a str {
    let s = String::from("hello");
    println!("{}", f(&s));
}
```

## Gotchas

- `move` captures ALL referenced variables, not just the ones you intend - can cause unexpected ownership transfer
- Closure types are anonymous - two closures with identical signatures have different types (use `dyn Fn` for heterogeneous collections)
- `FnOnce` closures can only be called once - calling twice is a compile error
- Under the hood: compiler generates a struct holding captured state + a method call - zero-cost abstraction

## See Also

- [[traits]] - Fn/FnMut/FnOnce trait hierarchy
- [[iterators]] - closures as arguments to map, filter, fold
- [[ownership-and-move-semantics]] - move semantics in closure captures
- [[generics-and-monomorphization]] - static dispatch with impl Trait
