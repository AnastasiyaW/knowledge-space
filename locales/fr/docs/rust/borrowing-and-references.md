---
title: "Emprunt et références"
category: concepts
tags: [rust, borrowing, references, mutable, immutable, slices]
level: 3
source_sha256: 822ab20ef41b8c1593111389c0335dff671523882345ff5ae15b4ce048982d7c
translation: machine
translated_at: '2026-10-24'
---
# Emprunt et références {#borrowing-and-references}

L'emprunt permet d'accéder à des données sans en prendre la propriété. Les références (`&T` et `&mut T`) sont des pointeurs non propriétaires que le vérificateur d'emprunts (borrow checker) valide à la compilation, ce qui empêche les courses de données (data races) et les références pendantes (dangling references).

## Points clés {#key-facts}

- `&T` = référence immuable (partagée) - plusieurs autorisées simultanément
- `&mut T` = référence mutable (exclusive) - une seule à la fois
- Impossible d'avoir `&T` et `&mut T` vers les mêmes données simultanément
- Les références doivent toujours être valides (ni null, ni pendantes)
- Les règles d'emprunt sont appliquées à la compilation par le borrow checker
- Les slices (`&[T]`, `&str`) sont des fat pointers : pointeur + longueur

## Règles d'emprunt {#borrowing-rules}

1. À un instant donné, vous pouvez avoir **soit** une seule référence mutable, **soit** un nombre quelconque de références immuables
2. Les références doivent toujours être valides (pas de pointeurs pendants)

```rust
let mut s = String::from("hello");

let r1 = &s;     // OK: immutable borrow
let r2 = &s;     // OK: second immutable borrow
// let r3 = &mut s; // ERROR: cannot borrow mutably while immutable borrows exist

println!("{} {}", r1, r2);
// r1, r2 no longer used after this point (NLL)

let r3 = &mut s;  // OK: immutable borrows are done
r3.push_str(" world");
```

## Patterns {#patterns}

### Slices {#slices}

```rust
let s = String::from("hello world");
let hello = &s[0..5];    // &str slice
let world = &s[6..11];

let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];    // &[i32] = [2, 3]
```

### Emprunt dans les fonctions {#function-borrowing}

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return &s[0..i]; }
    }
    &s[..]
}
```

## Pièges {#gotchas}

- NLL (Non-Lexical Lifetimes) : les emprunts prennent fin à leur dernière utilisation, et non à la fin du scope - ce qui rend le borrow checker plus ergonomique
- Les littéraux de chaîne (`"hello"`) sont des `&'static str` - des références vers des données intégrées au binaire
- `&String` se convertit automatiquement en `&str` via le trait `Deref`

## Voir aussi {#see-also}

- [[ownership-and-move-semantics]] - transfert de propriété vs emprunt
- [[lifetimes]] - annotations de durée de vie explicites pour les emprunts complexes
- [[collections]] - patterns d'emprunt avec Vec, HashMap, String
