---
title: "Makros"
category: concepts
tags: [rust, macros, macro-rules, procedural-macros, derive, metaprogramming, syn, quote]
level: 3
source_sha256: 41632e0d10ef9e91f510c38f20a17e66e8017da7709c65d623a619dad3ef4ffd
translation: machine
translated_at: '2026-10-24'
---
# Makros {#macros}

Rust-Makros erzeugen Code zur Kompilierzeit. Es gibt zwei Arten: **deklarative Makros** (`macro_rules!`) verwenden Mustervergleich auf der Syntax, **prozedurale Makros** transformieren Token-Streams über Rust-Code. Makros ermöglichen variadische Funktionen, benutzerdefinierte Derive-Implementierungen und nullkostenabstrahierte DSLs. Bevorzuge reguläre Funktionen, wann immer möglich – Makros sind schwerer zu debuggen.

## Wichtigste Fakten {#key-facts}

- `macro_rules!` = deklaratives, mustervergleichendes Makro (am häufigsten)
- Prozedurale Makros: Derive (`#[derive(MyMacro)]`), Attribut (`#[my_attr]`), funktionsähnlich (`my_macro!(...)`)
- Prozedurale Makros liegen in einem separaten Crate mit `proc-macro = true`
- Fragment-Specifier: `expr`, `ident`, `ty`, `pat`, `stmt`, `block`, `item`, `tt`, `literal`
- Wiederholungen: `$(...)*` (0+), `$(...)+` (1+), `$(...)?` (0 oder 1)
- Standardmakros: `vec![]`, `println!()`, `format!()`, `assert!()`, `dbg!()`

## Muster {#patterns}

### Deklarative Makros (macro_rules!) {#declarative-macros-macro_rules}

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

### Fragment-Specifier {#fragment-specifiers}

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

### Prozedurale Makros (Derive) {#procedural-macros-derive}

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

### Attribut-Makros {#attribute-macros}

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

### Makro vs. Funktion {#macro-vs-function}

| Makros verwenden, wenn | Funktionen verwenden, wenn |
|---|---|
| Variadische Argumente nötig sind | Feste Argumente |
| Typen/Bezeichner als Parameter dienen | Werte als Parameter dienen |
| Codegenerierung zur Kompilierzeit | Berechnung zur Laufzeit |
| Benutzerdefiniertes Derive/Attribut | Reguläres Verhalten |
| DSL-Syntax | Standard-Rust |

## Stolpersteine {#gotchas}

- Fehler in Makros sind schwerer zu debuggen – verwende `cargo expand`, um den generierten Code zu sehen
- Deklarative Makros gleichen Muster gierig ab – die Reihenfolge der Arme ist wichtig
- Prozedurale Makros benötigen ein separates Crate (`proc-macro = true` in der Cargo.toml)
- `$x:tt` (Token-Tree) ist der flexibelste, aber am wenigsten typsichere Fragment-Specifier
- Makros können nicht auf Laufzeitwerte zugreifen – sie sehen zur Kompilierzeit nur Syntax-Token

## Siehe auch {#see-also}

- [[traits]] - Derive-Makros implementieren Traits automatisch
- [[modules-and-visibility]] - Export- und Gültigkeitsregeln für Makros
- [[rust-tooling]] - cargo expand zum Debuggen von Makros
