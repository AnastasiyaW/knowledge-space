---
title: Sized Types and DSTs
category: concepts
tags: [sized, dst, trait-objects, str, slice, unsized]
---

# Sized Types and DSTs

Rust types divide into Sized (known size at compile time) and Dynamically Sized Types (DSTs, size known only at runtime). Understanding this split is essential for generics, trait objects, and function signatures.

## Key Facts

- `Sized` is an auto-trait, implicitly bound on all type parameters: `fn foo<T>(t: T)` means `T: Sized`
- DSTs cannot live on the stack - must be behind a pointer (`&`, `Box`, `Rc`, `Arc`)
- Three DSTs: `str`, `[T]`, `dyn Trait`
- Pointer to DST is a "fat pointer" (2x pointer width): data ptr + metadata
- `&str`: ptr + length. `&[T]`: ptr + length. `&dyn Trait`: ptr + vtable pointer
- `?Sized` bound relaxes the implicit `Sized` requirement: `fn foo<T: ?Sized>(t: &T)`
- `size_of::<&T>()` is one pointer width. `size_of::<&dyn Trait>()` is two pointer widths

## Sized Types

```rust
use std::mem::size_of;

// All concrete types are Sized
assert_eq!(8, size_of::<i64>());
assert_eq!(12, size_of::<[i32; 3]>());
assert_eq!(8, size_of::<(i32, i32)>());

// Pointer to Sized is one word
assert_eq!(8, size_of::<&i64>());      // on 64-bit
assert_eq!(8, size_of::<Box<u64>>());
```

## DST Fat Pointers

```rust
use std::mem::size_of;

// Slice: ptr + length
assert_eq!(16, size_of::<&[i32]>());
assert_eq!(16, size_of::<&str>());

// Trait object: ptr + vtable pointer
assert_eq!(16, size_of::<&dyn std::fmt::Debug>());
assert_eq!(16, size_of::<Box<dyn std::fmt::Debug>>());
```

## The ?Sized Bound

```rust
// This only accepts Sized types:
fn print_debug<T: std::fmt::Debug>(t: &T) {
    println!("{:?}", t);
}

// This accepts both Sized AND unsized:
fn print_debug_flexible<T: std::fmt::Debug + ?Sized>(t: &T) {
    println!("{:?}", t);
}

// Now works with str, [T], dyn Trait:
print_debug_flexible("hello");           // T = str
print_debug_flexible(&[1, 2, 3] as &[i32]); // T = [i32]
```

## Trait Object Memory Layout

```rust
trait Foo {
    fn method(&self) -> String;
}

impl Foo for u8 {
    fn method(&self) -> String { format!("u8: {}", self) }
}

// &dyn Foo is a fat pointer:
// [data_ptr: *const u8 | vtable_ptr: *const FooVtable]
//
// vtable contains:
// - destructor function pointer
// - size and alignment of concrete type
// - pointers to each trait method
```

## Unsized Coercion

```rust
// Sized -> Unsized coercions happen automatically:
let arr: [i32; 3] = [1, 2, 3];
let slice: &[i32] = &arr;        // [i32; 3] -> [i32]

let string = String::from("hello");
let s: &str = &string;           // String -> str (via Deref)

struct MyStruct;
impl Foo for MyStruct {}
let obj: &dyn Foo = &MyStruct;   // MyStruct -> dyn Foo
```

## Patterns

### Accepting DSTs in Functions

```rust
// Good: accepts both &String and &str
fn process(s: &str) { /* ... */ }

// Good: accepts both &Vec<T> and &[T]
fn process_slice<T>(s: &[T]) { /* ... */ }

// Good: accepts any Debug type including DSTs
fn debug_print<T: std::fmt::Debug + ?Sized>(t: &T) {
    println!("{:?}", t);
}
```

### Sized Requirement in Traits

```rust
trait MyTrait {
    // Default: Self is ?Sized (allows trait objects)
    fn method(&self);
}

trait SizedOnly: Sized {
    // Cannot make trait objects from this
    fn by_value(self);
}
```

## Gotchas

- **Issue:** Generic function rejects `&str` or `&[T]` arguments -> **Fix:** Add `?Sized` bound to type parameter when function takes reference: `fn f<T: Trait + ?Sized>(x: &T)`.
- **Issue:** Cannot store `dyn Trait` directly in struct field -> **Fix:** Store behind a pointer: `Box<dyn Trait>`, `Rc<dyn Trait>`, or `Arc<dyn Trait>`.
- **Issue:** Cannot create `dyn Trait` from DST (e.g., `&str -> &dyn Display`) because that would need a triple-wide pointer -> **Fix:** This is a language limitation. Only Sized types can be coerced to trait objects.

## See Also

- [[dynamic-dispatch]] - vtables and trait object mechanics
- [[traits]] - trait definitions and implementations
- [[generics-and-monomorphization]] - Sized bound in generics
- [[smart-pointers]] - Box, Rc, Arc for owning DSTs
