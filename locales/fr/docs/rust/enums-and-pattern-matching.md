---
title: "Énumérations et filtrage par motifs"
category: concepts
tags: [rust, enums, match, pattern-matching, option, result, if-let, destructuring, algebraic-types]
level: 3
source_sha256: 50290cd64733eb41f5f372a92d1edfe3d787fe84f32c42d3afca8675e378289c
translation: machine
translated_at: '2026-10-24'
---
# Énumérations et filtrage par motifs {#enums-and-pattern-matching}

Les énumérations Rust sont des types de données algébriques : chaque variante peut contenir des données différentes (unité, tuple ou structure). Combinées à des expressions `match` exhaustives, elles permettent un branchement vérifié à la compilation qui détecte les cas manquants. `Option<T>` et `Result<T, E>` sont les énumérations les plus importantes de la bibliothèque standard.

## Points clés {#key-facts}

- Les énumérations définissent un type pouvant prendre l'une de plusieurs variantes, chacune pouvant transporter des données
- `match` doit être **exhaustif** : toutes les variantes doivent être traitées (ou utiliser le joker `_`)
- `match` est une **expression** : elle retourne une valeur, et tous les bras doivent retourner le même type
- `if let` / `while let` permettent de filtrer une seule variante sans exigence d'exhaustivité
- Le filtrage par motifs fonctionne dans : `match`, `if let`, `while let`, les liaisons `let`, et les paramètres de fonction
- Les énumérations remplacent le besoin de pointeurs nuls, de codes d'erreur et d'unions étiquetées issus du C

## Motifs {#patterns}

### Définition d'une énumération {#enum-definition}

```rust
// Simple C-like enum
enum Direction { North, South, East, West }

// Enum with data (algebraic data type)
enum Message {
    Quit,                         // unit variant
    Move { x: i32, y: i32 },     // struct variant
    Write(String),                // tuple variant
    ChangeColor(i32, i32, i32),   // multi-value tuple variant
}
```

### Expression match {#match-expression}

```rust
fn process(msg: Message) -> String {
    match msg {
        Message::Quit => "Quitting".to_string(),
        Message::Move { x, y } => format!("Moving to ({}, {})", x, y),
        Message::Write(text) => format!("Message: {}", text),
        Message::ChangeColor(r, g, b) => format!("RGB({}, {}, {})", r, g, b),
    }
}
```

### Fonctionnalités du filtrage par motifs {#pattern-matching-features}

```rust
// Alternatives with |
Weather::Rainy | Weather::Snowy => true,

// Ranges
4..=10 => println!("Medium number"),

// Guards
x if x > 0 => println!("positive"),

// Tuple destructuring
match point {
    (0, 0) => println!("Origin"),
    (0, y) => println!("On Y axis: {}", y),
    (x, 0) => println!("On X axis: {}", x),
    (x, y) if x == y => println!("On diagonal"),
    (x, y) => println!("({}, {})", x, y),
}

// Struct destructuring in match
match person {
    Person { name, age: 0 } => println!("{} - newborn", name),
    Person { name, age } if age < 18 => println!("{} - minor", name),
    Person { name, .. } => println!("{} - adult", name),
}

// Nested enum + struct matching
match customer {
    Customer { contact: ContactMethod::Email(email), vip: true, .. } =>
        println!("VIP email: {}", email),
    Customer { contact: ContactMethod::Phone(phone), .. } =>
        println!("Calling {}", phone),
    _ => {}
}
```

### if let / while let (filtrage d'une seule variante) {#if-let-while-let-single-variant-matching}

```rust
// Instead of full match for one variant
if let Some(x) = some_value {
    println!("Value: {}", x);
}

// Loop until pattern fails
let mut stack = vec![1, 2, 3];
while let Some(value) = stack.pop() {
    println!("Popped: {}", value);
}
```

### Motifs avancés {#advanced-patterns}

```rust
// Slice patterns with binding
match slice {
    [.., "!"] => println!("exclamation"),
    [start @ .., "z"] => println!("starts with: {:?}", start),
    ["a", end @ ..] => println!("ends with: {:?}", end),
    all @ [.., last] => println!("last of {:?} is {}", all, last),
    _ => {}
}

// FizzBuzz with tuple match
let s = match (x % 3, x % 5) {
    (0, 0) => String::from("FizzBuzz"),
    (0, _) => String::from("Fizz"),
    (_, 0) => String::from("Buzz"),
    _ => x.to_string(),
};

// Destructuring in function params
fn distance((x1, y1): (f64, f64), (x2, y2): (f64, f64)) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2)).sqrt()
}
```

## Pièges à éviter {#gotchas}

- Oublier de traiter une variante est une erreur de compilation : c'est voulu, cela permet de détecter les bogues tôt
- `let _ = expr` ne lie ni ne déplace la valeur (contrairement à `let _x = expr`, qui le fait)
- Utiliser des constantes à la place d'énumérations (`const STATUS: i32 = 0`) fait perdre la sûreté de typage : privilégiez les énumérations
- Les variantes d'énumération sont espacées par un namespace : `Message::Quit`, et non simplement `Quit` (sauf si vous utilisez `use Message::*`)

## Voir aussi {#see-also}

- [Gestion des erreurs](error-handling.md) - `Result<T, E>` et `Option<T>` comme gestion d'erreurs basée sur les énumérations
- [[structs-and-methods]] - variantes de structures à l'intérieur des énumérations
- [[traits]] - implémentation de traits pour les énumérations
