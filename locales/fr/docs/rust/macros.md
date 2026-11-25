---
title: "Macros"
category: concepts
tags: [rust, macros, macro-rules, procedural-macros, derive, metaprogramming, syn, quote]
level: 3
source_sha256: 41632e0d10ef9e91f510c38f20a17e66e8017da7709c65d623a619dad3ef4ffd
translation: machine
translated_at: '2026-10-24'
---
# Macros {#macros}

Les macros Rust génèrent du code à la compilation. Il en existe deux types : les **macros déclaratives** (`macro_rules!`) utilisent la correspondance de motifs sur la syntaxe, tandis que les **macros procédurales** transforment des flux de tokens via du code Rust. Les macros permettent de créer des fonctions variadiques, des implémentations de derive personnalisées et des DSL à coût nul. Privilégiez les fonctions classiques lorsque c'est possible : les macros sont plus difficiles à déboguer.

## Key Facts {#key-facts}

- `macro_rules!` = macro déclarative, à correspondance de motifs (la plus courante)
- Macros procédurales : derive (`#[derive(MyMacro)]`), attribut (`#[my_attr]`), type fonction (`my_macro!(...)`)
- Les macros procédurales vivent dans un crate séparé avec `proc-macro = true`
- Spécificateurs de fragments : `expr`, `ident`, `ty`, `pat`, `stmt`, `block`, `item`, `tt`, `literal`
- Répétitions : `$(...)*` (0 ou plus), `$(...)+` (1 ou plus), `$(...)?` (0 ou 1)
- Macros standard : `vec![]`, `println!()`, `format!()`, `assert!()`, `dbg!()`

## Patterns {#patterns}

### Declarative Macros (macro_rules!) {#declarative-macros-macro_rules}

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

### Fragment Specifiers {#fragment-specifiers}

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

### Procedural Macros (Derive) {#procedural-macros-derive}

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

### Attribute Macros {#attribute-macros}

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

### Macro vs Function {#macro-vs-function}

| Use macros when | Use functions when |
|---|---|
| Variadic arguments needed | Fixed arguments |
| Types/identifiers as params | Values as params |
| Compile-time code generation | Runtime computation |
| Custom derive/attribute | Regular behavior |
| DSL syntax | Standard Rust |

## Gotchas {#gotchas}

- Les erreurs de macros sont plus difficiles à déboguer : utilisez `cargo expand` pour voir le code généré
- Les macros déclaratives font correspondre les motifs de manière gourmande : l'ordre des branches compte
- Les macros procédurales nécessitent un crate séparé (`proc-macro = true` dans Cargo.toml)
- `$x:tt` (arbre de tokens) est le spécificateur de fragment le plus souple mais le moins typé
- Les macros ne peuvent pas accéder aux valeurs à l'exécution : elles ne voient que les tokens de syntaxe à la compilation

## See Also {#see-also}

- [[traits]] - les macros derive implémentent automatiquement des traits
- [[modules-and-visibility]] - export des macros et règles de portée
- [[rust-tooling]] - cargo expand pour le débogage des macros
