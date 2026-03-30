---
title: Generics and Monomorphization
category: concepts
tags: [generics, monomorphization, type-parameters, where-clause, turbofish]
---
# Generics and Monomorphization

Generics enable writing code parameterized over types; the compiler generates specialized versions via monomorphization for zero-cost abstraction.

## Key Facts

- Generic parameters declared with angle brackets: `fn foo<T>(x: T)`, `struct Bar<T>`, `enum Result<T, E>`
- Trait bounds constrain type parameters: `<T: Clone + Debug>` or `where T: Clone + Debug`
- Monomorphization: compiler generates a separate function/struct for each concrete type used - zero runtime cost, but increases binary size and compile time
- Contrast with [[dynamic-dispatch]] (`dyn Trait`) which uses vtable at runtime
- `impl<T> Struct<T>` - generic impl for all T (blanket impl)
- `impl Struct<i32>` - specialized impl for specific type
- Turbofish syntax: `function::<Type>()` to specify type parameters explicitly
- `impl Trait` in argument position = sugar for generics; in return position = opaque type
- Const generics: `struct Array<T, const N: usize>` - parameterize over values

## Patterns

```rust
// Generic function with trait bound
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in &list[1..] {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// Where clause (cleaner for complex bounds)
fn process<T, U>(t: T, u: U) -> String
where
    T: std::fmt::Display + Clone,
    U: std::fmt::Debug + Into<T>,
{
    format!("{} {:?}", t, u)
}

// Generic struct
struct Pair<T> {
    first: T,
    second: T,
}

impl<T> Pair<T> {
    fn new(first: T, second: T) -> Self {
        Self { first, second }
    }
}

// Conditional method implementation
impl<T: PartialOrd + std::fmt::Display> Pair<T> {
    fn cmp_display(&self) {
        if self.first >= self.second {
            println!("largest = {}", self.first);
        } else {
            println!("largest = {}", self.second);
        }
    }
}

// impl Trait syntax
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y
}

// As argument (sugar for generics)
fn print_it(item: &impl std::fmt::Display) {
    println!("{item}");
}
// equivalent to:
fn print_it_generic<T: std::fmt::Display>(item: &T) {
    println!("{item}");
}

// Turbofish
let parsed = "42".parse::<i32>().unwrap();
let v = Vec::<i32>::new();

// Const generics
struct Matrix<T, const ROWS: usize, const COLS: usize> {
    data: [[T; COLS]; ROWS],
}

impl<T: Default + Copy, const R: usize, const C: usize> Matrix<T, R, C> {
    fn new() -> Self {
        Self { data: [[T::default(); C]; R] }
    }
}

let m: Matrix<f64, 3, 3> = Matrix::new();

// Blanket implementation
// From std: impl<T: Display> ToString for T
// This means anything with Display automatically gets .to_string()
```

```rust
// Monomorphization in action
fn identity<T>(x: T) -> T { x }

identity(42_i32);       // compiler generates: fn identity_i32(x: i32) -> i32
identity("hello");      // compiler generates: fn identity_str(x: &str) -> &str
identity(vec![1,2,3]);  // compiler generates: fn identity_vec(x: Vec<i32>) -> Vec<i32>
```

## Gotchas

- **Symptom**: "the trait bound `T: X` is not satisfied" - **Cause**: missing trait bound on generic parameter - **Fix**: add `T: X` to the where clause
- **Symptom**: "type annotations needed" - **Cause**: compiler can't infer the type parameter - **Fix**: use turbofish `::< >` or annotate the variable
- **Symptom**: large binary size / slow compilation - **Cause**: monomorphization generates code for every type combo - **Fix**: consider [[dynamic-dispatch]] (`Box<dyn Trait>`) for rarely-used paths
- **Symptom**: can't return different types from branches with `impl Trait` - **Cause**: `impl Trait` is a single concrete type - **Fix**: use `Box<dyn Trait>` or refactor into an enum

## See Also

- [[traits]] - defining trait bounds
- [[dynamic-dispatch]] - runtime polymorphism alternative
- [[closures]] - `impl Fn(...)` return types
- [The Rust Book - Generics](https://doc.rust-lang.org/book/ch10-01-syntax.html)
- [Rust Reference - Const Generics](https://doc.rust-lang.org/reference/items/generics.html#const-generics)
