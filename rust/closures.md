---
title: Closures
category: concepts
tags: [closures, fn, fnmut, fnonce, move, lambda, capture]
---
# Closures

Closures are anonymous functions that capture variables from their enclosing scope, implementing one of the `Fn`, `FnMut`, or `FnOnce` [[traits]].

## Key Facts

- Syntax: `|params| expr` or `|params| { block }`
- Type annotations optional - inferred from first use (then locked to that type)
- Three capture modes (compiler picks the least restrictive):
  - By reference (`&T`) - implements `Fn`
  - By mutable reference (`&mut T`) - implements `FnMut`
  - By value (move) - implements `FnOnce`
- `FnOnce` > `FnMut` > `Fn` (supertrait chain): every `Fn` is also `FnMut` and `FnOnce`
- `move` keyword forces capture by value (ownership transfer); essential for `'static` requirements (threads, async)
- `Copy` types are copied even with `move`; non-Copy types are moved
- Function pointers `fn(T) -> U` are a subset of closures (no captured environment)
- Each closure has a unique anonymous type; use `impl Fn(...)` or `Box<dyn Fn(...)>` for storage/return

## Patterns

```rust
// Basic closures
let add = |x: i32, y: i32| x + y;
let double = |x| x * 2;  // type inferred on first use
println!("{}", add(3, 4));    // 7
println!("{}", double(5));    // 10

// Capturing by reference (Fn)
let name = String::from("Alice");
let greet = || println!("Hello, {name}!");
greet();
greet();  // can call multiple times
println!("{name}");  // name still valid

// Capturing by mutable reference (FnMut)
let mut count = 0;
let mut increment = || { count += 1; };
increment();
increment();
// println!("{count}");  // ERROR: borrowed mutably by closure
drop(increment);         // release the borrow
println!("{count}");     // 2

// Capturing by value (FnOnce)
let name = String::from("Alice");
let consume = || {
    let _moved = name;  // moves name into closure body
};
consume();
// consume();  // ERROR: already consumed (FnOnce)

// move keyword
let data = vec![1, 2, 3];
let closure = move || println!("{data:?}");
// println!("{data:?}");  // ERROR: moved into closure
closure();

// move with Copy types
let x = 42;
let closure = move || println!("{x}");
println!("{x}");  // OK: x is Copy, closure got a copy

// Closures as function arguments
fn apply<F: Fn(i32) -> i32>(f: F, val: i32) -> i32 {
    f(val)
}
let doubled = apply(|x| x * 2, 5);

// Returning closures
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y
}
let add5 = make_adder(5);
println!("{}", add5(3));  // 8

// Returning different closures requires Box<dyn>
fn make_op(multiply: bool) -> Box<dyn Fn(i32) -> i32> {
    if multiply {
        Box::new(|x| x * 2)
    } else {
        Box::new(|x| x + 2)
    }
}

// Function pointers vs closures
fn square(x: i32) -> i32 { x * x }
let fn_ptr: fn(i32) -> i32 = square;  // function pointer
let values = vec![1, 2, 3];
let squared: Vec<_> = values.iter().map(|x| x * x).collect();

// Closure in struct
struct Callback<F: Fn()> {
    func: F,
}
// or with trait object
struct DynCallback {
    func: Box<dyn Fn()>,
}
```

## Gotchas

- **Symptom**: "closure may outlive current function" when passing to threads - **Cause**: closure captures references to local variables - **Fix**: use `move` to transfer ownership into the closure
- **Symptom**: "expected fn pointer, found closure" - **Cause**: closures that capture environment are not function pointers - **Fix**: use generics with `Fn` bound or `Box<dyn Fn(...)>`
- **Symptom**: can't return `impl Fn` when branches return different closures - **Cause**: each closure is a unique type - **Fix**: use `Box<dyn Fn(...)>` to type-erase
- **Symptom**: `move` closure with `Copy` type still allows using the original - **Cause**: `move` copies `Copy` types rather than moving - **Fix**: this is correct behavior; non-Copy types would be moved

## See Also

- [[traits]] - `Fn`, `FnMut`, `FnOnce` trait hierarchy
- [[iterators]] - closures as arguments to iterator methods
- [[concurrency]] - `move` closures for thread spawning
- [[generics-and-monomorphization]] - `impl Fn(...)` syntax
- [The Rust Book - Closures](https://doc.rust-lang.org/book/ch13-01-closures.html)
- [std::ops::Fn](https://doc.rust-lang.org/std/ops/trait.Fn.html)
