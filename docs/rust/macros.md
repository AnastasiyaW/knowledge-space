---
title: Macros
category: concepts
tags: [rust, macros, macro-rules, procedural-macros, derive, metaprogramming, syn, quote]
---

# Macros

Rust macros generate code at compile time. Two kinds: **declarative macros** (`macro_rules!`) use pattern matching on syntax, **procedural macros** transform token streams via Rust code. Macros enable variadic functions, custom derive implementations, and zero-cost DSLs. Prefer regular functions when possible - macros are harder to debug.

## Key Facts

- `macro_rules!` = declarative, pattern-matching macro (most common)
- Procedural macros: derive (`#[derive(MyMacro)]`), attribute (`#[my_attr]`), function-like (`my_macro!(...)`)
- Procedural macros live in a separate crate with `proc-macro = true`
- Fragment specifiers: `expr`, `ident`, `ty`, `pat`, `stmt`, `block`, `item`, `tt`, `literal`
- Repetitions: `$(...)*` (0+), `$(...)+` (1+), `$(...)?` (0 or 1)
- Standard macros: `vec![]`, `println!()`, `format!()`, `assert!()`, `dbg!()`

## Patterns

### Declarative Macros (macro_rules!)

```rust
macro_rules! vec {
    () => { Vec::new() };
    ($($x:expr),+ $(,)?) => {
        {
            let mut temp = Vec::new();
            $(temp.push($x);)+
            temp
        }
    };
}

// Usage
let v = vec![1, 2, 3];
let empty: Vec<i32> = vec![];
```

### Fragment Specifiers

```rust
macro_rules! create_fn {
    ($name:ident, $body:block) => {
        fn $name() $body
    };
}

macro_rules! calculate {
    ($a:expr, $op:tt, $b:expr) => {
        $a $op $b
    };
}

create_fn!(greet, { println!("Hello!"); });
let result = calculate!(2, +, 3);  // 5
```

### Procedural Macros (Derive)

```rust
// In a separate proc-macro crate
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(MyDerive)]
pub fn my_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;

    let expanded = quote! {
        impl MyTrait for #name {
            fn describe(&self) -> String {
                format!("I am a {}", stringify!(#name))
            }
        }
    };

    TokenStream::from(expanded)
}

// Usage
#[derive(MyDerive)]
struct Widget;
```

### Attribute Macros

```rust
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
    // attr = "GET, /api/users"
    // item = the annotated function
    // return modified function
    item
}

// Usage
#[route(GET, "/api/users")]
fn list_users() { /* ... */ }
```

### Macro vs Function

| Use macros when | Use functions when |
|---|---|
| Variadic arguments needed | Fixed arguments |
| Types/identifiers as params | Values as params |
| Compile-time code generation | Runtime computation |
| Custom derive/attribute | Regular behavior |
| DSL syntax | Standard Rust |

## Gotchas

- Macro errors are harder to debug - use `cargo expand` to see generated code
- Declarative macros match patterns greedily - order of arms matters
- Procedural macros require a separate crate (`proc-macro = true` in Cargo.toml)
- `$x:tt` (token tree) is the most flexible but least type-safe fragment specifier
- Macros cannot access runtime values - they only see syntax tokens at compile time

## See Also

- [[traits]] - derive macros auto-implement traits
- [[modules-and-visibility]] - macro export and scoping rules
- [[rust-tooling]] - cargo expand for macro debugging
