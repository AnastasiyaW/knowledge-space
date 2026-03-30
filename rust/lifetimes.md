---
title: Lifetimes
category: concepts
tags: [lifetimes, borrow-checker, references, annotations]
---
# Lifetimes

Lifetimes are compile-time annotations that tell the borrow checker how long [[borrowing-and-references]] remain valid.

## Key Facts

- Every reference has a lifetime, usually inferred by the compiler
- Lifetime annotations (`'a`) don't change how long values live - they describe relationships between reference lifetimes
- Lifetime elision rules handle most cases automatically:
  1. Each input reference gets its own lifetime parameter
  2. If exactly one input lifetime, it's assigned to all output lifetimes
  3. If `&self` or `&mut self` is an input, its lifetime is assigned to all output lifetimes
- `'static` lifetime means the reference lives for the entire program duration (string literals, leaked memory)
- Lifetime bounds on generics: `T: 'a` means "T must live at least as long as `'a`"
- Structs holding references must annotate lifetimes

## Patterns

```rust
// Explicit lifetime annotation
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// The returned reference is valid for the shorter of the two input lifetimes
let result;
let s1 = String::from("long string");
{
    let s2 = String::from("xyz");
    result = longest(s1.as_str(), s2.as_str());
    println!("{result}");  // OK: s2 still alive
}
// println!("{result}");   // ERROR if result could reference s2

// Struct with lifetime
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    // Elision rule 3: &self lifetime used for return
    fn level(&self) -> i32 { 3 }

    fn announce(&self, announcement: &str) -> &str {
        // Returns &self.part with lifetime 'a
        println!("Attention: {announcement}");
        self.part
    }
}

// Multiple lifetimes
fn first_or_default<'a, 'b>(x: &'a str, default: &'b str) -> &'a str {
    if x.is_empty() {
        // ERROR: can't return 'b where 'a expected
        // default
        x
    } else {
        x
    }
}

// 'static lifetime
let s: &'static str = "I live forever";

// Lifetime bounds
fn print_ref<'a, T>(t: &'a T)
where
    T: std::fmt::Debug + 'a,
{
    println!("{t:?}");
}

// HRTB (Higher-Ranked Trait Bounds)
fn apply<F>(f: F)
where
    F: for<'a> Fn(&'a str) -> &'a str,
{
    let s = String::from("hello");
    println!("{}", f(&s));
}
```

## Gotchas

- **Symptom**: "lifetime may not live long enough" - **Cause**: function returns a reference tied to a shorter-lived input - **Fix**: ensure the returned reference's source outlives the required scope, or return an owned value
- **Symptom**: struct holding `&str` requires lifetime parameter everywhere - **Cause**: lifetime propagates through all containers - **Fix**: consider using `String` instead of `&str` for owned data in structs
- **Symptom**: `'static` doesn't mean "allocated statically" - **Cause**: it means "can live as long as needed, possibly forever" - **Fix**: `T: 'static` means T contains no non-static references (owned types satisfy this)
- **Symptom**: closure lifetime issues - **Cause**: closures capture references with specific lifetimes - **Fix**: use `move` to take ownership, or restructure to avoid captured references

## See Also

- [[borrowing-and-references]] - reference fundamentals
- [[traits]] - lifetime bounds on trait implementations
- [[generics-and-monomorphization]] - lifetime parameters in generic code
- [The Rust Book - Lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)
- [Rust Reference - Lifetime elision](https://doc.rust-lang.org/reference/lifetime-elision.html)
