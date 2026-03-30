---
title: Macros
category: concepts
tags: [macros, macro-rules, procedural-macros, derive, metaprogramming]
---
# Macros

Rust macros generate code at compile time; declarative macros (`macro_rules!`) use pattern matching, procedural macros operate on token streams.

## Key Facts

- Declarative macros (`macro_rules!`) match patterns and expand to code; invoked with `!`
- Procedural macros are Rust functions that take `TokenStream` input and produce `TokenStream` output
- Three kinds of procedural macros: derive macros (`#[derive(MyMacro)]`), attribute macros (`#[my_attr]`), function-like macros (`my_macro!(...)`)
- Declarative macro repetitions: `$( $x:expr ),*` - zero or more; `$( $x:expr ),+` - one or more; `$( $x:expr )?` - zero or one
- Fragment specifiers: `expr`, `ident`, `ty`, `pat`, `stmt`, `block`, `item`, `path`, `literal`, `tt` (token tree)
- Macros are hygienic - generated identifiers don't clash with user code (with caveats)
- Common std macros: `vec![]`, `println!()`, `format!()`, `assert!()`, `todo!()`, `unimplemented!()`, `dbg!()`
- Procedural macros must live in their own crate with `proc-macro = true`

## Patterns

```rust
// Simple declarative macro
macro_rules! say_hello {
    () => {
        println!("Hello!");
    };
}
say_hello!();

// Macro with arguments
macro_rules! create_fn {
    ($name:ident) => {
        fn $name() {
            println!("Function: {}", stringify!($name));
        }
    };
}
create_fn!(foo);
foo();  // prints "Function: foo"

// Repetition
macro_rules! vec_of_strings {
    ( $( $x:expr ),* ) => {
        {
            let mut v = Vec::new();
            $( v.push(String::from($x)); )*
            v
        }
    };
}
let v = vec_of_strings!["hello", "world"];

// Matching different patterns
macro_rules! calculate {
    (eval $e:expr) => {
        println!("{} = {}", stringify!($e), $e);
    };
    (sum $( $x:expr ),+ ) => {
        {
            let mut total = 0;
            $( total += $x; )+
            total
        }
    };
}
calculate!(eval 1 + 2);           // "1 + 2 = 3"
let s = calculate!(sum 1, 2, 3);  // 6

// Recursive macro
macro_rules! count {
    () => { 0usize };
    ($head:tt $( $tail:tt )*) => {
        1usize + count!($( $tail )*)
    };
}
let n = count!(a b c d);  // 4

// Common std macros
let v = vec![1, 2, 3];
let s = format!("x = {}, y = {:.2}", 42, 3.14159);
assert_eq!(2 + 2, 4);
assert!(v.len() > 0, "vector should not be empty");
let x = dbg!(2 + 3);  // prints "[src/main.rs:N] 2 + 3 = 5", returns 5
// todo!();            // panics with "not yet implemented"

// Derive macro usage (from serde)
// #[derive(Serialize, Deserialize)]
// struct Config {
//     name: String,
//     port: u16,
// }

// Attribute macro usage (from tokio)
// #[tokio::main]
// async fn main() { }
// expands to runtime::Runtime::new().unwrap().block_on(async { })

// cfg conditional compilation
#[cfg(target_os = "linux")]
fn platform_specific() { /* linux only */ }

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() { assert_eq!(2 + 2, 4); }
}

// Feature flags
// #[cfg(feature = "advanced")]
// pub fn advanced_feature() { }
```

```rust
// Procedural macro crate structure (proc-macro = true in Cargo.toml)
// use proc_macro::TokenStream;
// use quote::quote;
// use syn::{parse_macro_input, DeriveInput};
//
// #[proc_macro_derive(MyTrait)]
// pub fn my_trait_derive(input: TokenStream) -> TokenStream {
//     let input = parse_macro_input!(input as DeriveInput);
//     let name = input.ident;
//     let expanded = quote! {
//         impl MyTrait for #name {
//             fn describe(&self) -> String {
//                 format!("I am {}", stringify!(#name))
//             }
//         }
//     };
//     TokenStream::from(expanded)
// }
```

## Gotchas

- **Symptom**: "no rules expected this token" - **Cause**: macro invocation doesn't match any arm - **Fix**: check fragment specifiers and delimiters; add `$( ... )*` for repetition
- **Symptom**: macro works in one module but not another - **Cause**: declarative macros follow textual scope rules - **Fix**: use `#[macro_export]` or `#[macro_use]`; in Rust 2018+ use `use crate::macro_name;`
- **Symptom**: procedural macro compile errors are cryptic - **Cause**: error points to generated code, not the macro - **Fix**: use `cargo expand` to see generated code; use `compile_error!()` for better diagnostics
- **Symptom**: can't use a local variable inside `macro_rules!` - **Cause**: macros are hygienic - **Fix**: pass the variable as a macro argument using `$var:ident`

## See Also

- [[traits]] - `#[derive()]` for common trait implementations
- [[modules-and-visibility]] - `#[cfg]` for conditional compilation
- [[structs-and-methods]] - derive macros for structs
- [The Rust Book - Macros](https://doc.rust-lang.org/book/ch19-06-macros.html)
- [The Little Book of Rust Macros](https://veykril.github.io/tlborm/)
- [proc-macro2](https://docs.rs/proc-macro2), [syn](https://docs.rs/syn), [quote](https://docs.rs/quote)
