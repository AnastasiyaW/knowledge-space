---
title: "Structs und Methoden"
category: concepts
tags: [rust, structs, methods, impl, encapsulation, tuple-struct, newtype, self, visibility]
level: 3
source_sha256: 1dda6a5a8ded09d6106d25d7013ead10862afd5d25e92e172077a9b04cdacfcf
translation: machine
translated_at: '2026-10-24'
---
# Structs und Methoden {#structs-and-methods}

Structs sind Rusts primäre Möglichkeit, eigene Datentypen zu erstellen. Es gibt drei Arten: klassische (benannte Felder), Tuple-Structs (positionsbasierte Felder) und Unit-Structs (ohne Felder). Methoden werden in `impl`-Blöcken mit drei Receiver-Typen (`&self`, `&mut self`, `self`) definiert, die den Zugriff steuern. Die Sichtbarkeit ist standardmäßig privat – mit `pub` wird sie über Modulgrenzen hinweg freigegeben.

## Wichtige Fakten {#key-facts}

- Drei Struct-Arten: klassisch (`struct Point { x: f64, y: f64 }`), Tuple (`struct Color(u8, u8, u8)`), Unit (`struct Marker;`)
- Alle Felder und Methoden sind **standardmäßig privat** – Privatsphäre wird an der Modulgrenze durchgesetzt
- `impl`-Blöcke definieren Methoden (nehmen `self` entgegen) und assoziierte Funktionen (ohne `self`, z. B. Konstruktoren)
- Struct-Update-Syntax: `User { name: "Tom".into(), ..old_user }` kopiert die übrigen Felder
- `#[derive(Debug, Clone, PartialEq)]` implementiert gängige Traits automatisch
- Pro Typ sind mehrere `impl`-Blöcke erlaubt (nützlich für bedingte Trait-Implementierungen)

## Muster {#patterns}

### Drei Struct-Arten {#three-struct-kinds}

```rust
// Classic struct - named fields
struct User {
    name: String,
    email: String,
    active: bool,
}

// Tuple struct - positional fields (newtype pattern)
struct Meters(f64);
struct Color(u8, u8, u8);

// Unit struct - no fields (markers, type-level tags)
struct EndOfStream;
```

### Erstellen und Destrukturieren {#creating-and-destructuring}

```rust
let user = User {
    name: "Alice".to_string(),
    email: "alice@example.com".to_string(),
    active: true,
};

// Struct update syntax (spread)
let user2 = User { name: "Bob".to_string(), ..user };

// Destructuring
let User { name, email, .. } = user2;

// Tuple struct access and destructuring
let color = Color(255, 128, 0);
let r = color.0;
let Color(_, g, _) = color;
```

### Methoden und assoziierte Funktionen {#methods-and-associated-functions}

```rust
struct Point { x: f64, y: f64 }

impl Point {
    // Associated function (constructor) - no self
    fn origin() -> Point {
        Point { x: 0.0, y: 0.0 }
    }

    // Immutable borrow - read-only access
    fn distance(&self, other: &Point) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }

    // Mutable borrow - can modify
    fn translate(&mut self, dx: f64, dy: f64) {
        self.x += dx;
        self.y += dy;
    }

    // Takes ownership - consumes the value
    fn into_tuple(self) -> (f64, f64) {
        (self.x, self.y)
    }
}

let p = Point::origin();          // associated function call
let d = p.distance(&Point { x: 3.0, y: 4.0 });  // method call
```

### Sichtbarkeitsmodifikatoren {#visibility-modifiers}

```rust
pub struct Config {
    pub name: String,         // public everywhere
    pub(crate) port: u16,     // public within crate only
    pub(super) debug: bool,   // public in parent module
    secret: String,           // private (default)
}

// Re-export to flatten module hierarchy
pub use self::inner::PublicApi;
```

### Newtype-Muster {#newtype-pattern}

```rust
// Wrap a type to add type safety without runtime cost
struct Meters(f64);
struct Seconds(f64);

fn speed(distance: Meters, time: Seconds) -> f64 {
    distance.0 / time.0
}

// Compiler prevents: speed(Seconds(10.0), Meters(100.0))
```

## Fallstricke {#gotchas}

- Struct-Update-Syntax (`..old`) verschiebt Nicht-Copy-Felder – `old` kann danach teilweise verschoben sein
- Eine Methode mit `&self` und eine mit `&mut self` können nicht gleichzeitig auf denselben Wert aufgerufen werden (Borrow-Regeln)
- Unit-Structs sind Zero-Sized Types (ZST) und benötigen zur Laufzeit keinen Speicher
- Ein `self`-Receiver (per Wert) verbraucht die Struct – sie kann nach dem Methodenaufruf nicht mehr verwendet werden

## Siehe auch {#see-also}

- [[traits]] – Implementierung von Traits für Structs
- [[enums-and-pattern-matching]] – Enums als der andere wichtige eigene Typ
- [[modules-and-visibility]] – Modulsystem und Regeln für `pub`-Sichtbarkeit
- [[ownership-and-move-semantics]] – Auswirkungen von Ownership auf `self`-Receiver
