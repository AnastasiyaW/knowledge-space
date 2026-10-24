---
title: "Ausleihen und Referenzen"
category: concepts
tags: [rust, borrowing, references, mutable, immutable, slices]
level: 3
source_sha256: 822ab20ef41b8c1593111389c0335dff671523882345ff5ae15b4ce048982d7c
translation: machine
translated_at: '2026-10-24'
---
# Ausleihen und Referenzen {#borrowing-and-references}

Borrowing ermöglicht den Zugriff auf Daten, ohne deren Ownership zu übernehmen. Referenzen (`&T` und `&mut T`) sind nicht besitzende Zeiger, die der Borrow Checker zur Compile-Zeit validiert und die so Data Races und Dangling References verhindern.

## Wichtige Fakten {#key-facts}

- `&T` = unveränderliche (geteilte) Referenz - mehrere gleichzeitig erlaubt
- `&mut T` = veränderliche (exklusive) Referenz - jeweils nur eine
- Es ist nicht möglich, gleichzeitig `&T` und `&mut T` auf dieselben Daten zu haben
- Referenzen müssen immer gültig sein (kein Null, kein Dangling)
- Die Borrowing-Regeln werden zur Compile-Zeit vom Borrow Checker durchgesetzt
- Slices (`&[T]`, `&str`) sind Fat Pointers: Zeiger + Länge

## Borrowing-Regeln {#borrowing-rules}

1. Zu jedem Zeitpunkt kann man **entweder** genau eine veränderliche Referenz **oder** beliebig viele unveränderliche Referenzen haben
2. Referenzen müssen immer gültig sein (keine Dangling Pointers)

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

## Muster {#patterns}

### Slices {#slices}

```rust
let s = String::from("hello world");
let hello = &s[0..5];    // &str slice
let world = &s[6..11];

let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];    // &[i32] = [2, 3]
```

### Borrowing bei Funktionen {#function-borrowing}

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return &s[0..i]; }
    }
    &s[..]
}
```

## Stolperfallen {#gotchas}

- NLL (Non-Lexical Lifetimes): Borrows enden mit der letzten Verwendung, nicht am Ende des Scopes - das macht den Borrow Checker ergonomischer
- String-Literale (`"hello"`) sind `&'static str` - Referenzen auf Daten, die in das Binary eingebettet sind
- `&String` wird über den `Deref`-Trait automatisch zu `&str` konvertiert

## Siehe auch {#see-also}

- [[ownership-and-move-semantics]] - Ownership-Übergabe vs. Borrowing
- [[lifetimes]] - explizite Lifetime-Annotationen für komplexes Borrowing
- [[collections]] - Borrowing-Muster mit Vec, HashMap, String
