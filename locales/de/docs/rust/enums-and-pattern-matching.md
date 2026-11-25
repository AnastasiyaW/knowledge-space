---
title: "Enums und Pattern Matching"
category: concepts
tags: [rust, enums, match, pattern-matching, option, result, if-let, destructuring, algebraic-types]
level: 3
source_sha256: 50290cd64733eb41f5f372a92d1edfe3d787fe84f32c42d3afca8675e378289c
translation: machine
translated_at: '2026-10-24'
---
# Enums und Pattern Matching {#enums-and-pattern-matching}

Rust-Enums sind algebraische Datentypen - jede Variante kann unterschiedliche Daten enthalten (Unit-, Tupel- oder Struct-artig). In Kombination mit vollständigen `match`-Ausdrücken ermöglichen sie zur Kompilierzeit geprüfte Verzweigungen, die fehlende Fälle erkennen. `Option<T>` und `Result<T, E>` sind die wichtigsten Enums der Standardbibliothek.

## Wichtige Fakten {#key-facts}

- Enums definieren einen Typ, der eine von mehreren Varianten sein kann, wobei jede Variante potenziell Daten trägt
- `match` muss **vollständig** sein - alle Varianten müssen behandelt werden (oder über den `_`-Platzhalter)
- `match` ist ein **Ausdruck** - er liefert einen Wert zurück, alle Arme müssen denselben Typ liefern
- `if let` / `while let` für das Matching einer einzelnen Variante ohne Vollständigkeitsprüfung
- Pattern Matching funktioniert in: `match`, `if let`, `while let`, `let`-Bindings, Funktionsparametern
- Enums ersetzen die Notwendigkeit von Null-Pointern, Fehlercodes und getaggten Unions aus C

## Muster {#patterns}

### Enum-Definition {#enum-definition}

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

### Match-Ausdruck {#match-expression}

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

### Pattern-Matching-Features {#pattern-matching-features}

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

### if let / while let (Matching einzelner Varianten) {#if-let-while-let-single-variant-matching}

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

### Erweiterte Muster {#advanced-patterns}

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

## Fallstricke {#gotchas}

- Das Vergessen einer Variante ist ein Compilerfehler - das ist beabsichtigt und fängt Fehler früh ab
- `let _ = expr` bindet bzw. verschiebt den Wert NICHT (anders als `let _x = expr`, das dies tut)
- Konstanten statt Enums zu verwenden (`const STATUS: i32 = 0`) verliert Typsicherheit - Enums sind vorzuziehen
- Enum-Varianten sind namensraumgebunden: `Message::Quit`, nicht nur `Quit` (sofern du nicht `use Message::*` verwendest)

## Siehe auch {#see-also}

- [Fehlerbehandlung](error-handling.md) - `Result<T, E>` und `Option<T>` als enum-basierte Fehlerbehandlung
- [[structs-and-methods]] - Struct-Varianten innerhalb von Enums
- [[traits]] - Implementieren von Traits für Enums
