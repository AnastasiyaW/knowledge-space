---
title: "Structures et méthodes"
category: concepts
tags: [rust, structs, methods, impl, encapsulation, tuple-struct, newtype, self, visibility]
level: 3
source_sha256: 1dda6a5a8ded09d6106d25d7013ead10862afd5d25e92e172077a9b04cdacfcf
translation: machine
translated_at: '2026-10-24'
---
# Structures et méthodes {#structs-and-methods}

Les structures sont le principal moyen qu'a Rust de créer des types de données personnalisés. Il en existe trois sortes : classiques (champs nommés), tuples (champs positionnels) et unitaires (sans champs). Les méthodes sont définies dans des blocs `impl` avec trois types de récepteurs (`&self`, `&mut self`, `self`) qui contrôlent l'accès. La visibilité est privée par défaut : utilisez `pub` pour l'exposer au-delà des frontières de module.

## Points clés {#key-facts}

- Trois types de structures : classique (`struct Point { x: f64, y: f64 }`), tuple (`struct Color(u8, u8, u8)`), unitaire (`struct Marker;`)
- Tous les champs et méthodes sont **privés par défaut** : la confidentialité est appliquée à la frontière du module
- Les blocs `impl` définissent des méthodes (qui prennent `self`) et des fonctions associées (sans `self`, comme les constructeurs)
- La syntaxe de mise à jour de structure : `User { name: "Tom".into(), ..old_user }` copie les champs restants
- `#[derive(Debug, Clone, PartialEq)]` implémente automatiquement les traits courants
- Plusieurs blocs `impl` sont autorisés par type (utile pour les implémentations de traits conditionnelles)

## Motifs {#patterns}

### Les trois types de structures {#three-struct-kinds}

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

### Création et déstructuration {#creating-and-destructuring}

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

### Méthodes et fonctions associées {#methods-and-associated-functions}

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

### Modificateurs de visibilité {#visibility-modifiers}

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

### Motif newtype {#newtype-pattern}

```rust
// Wrap a type to add type safety without runtime cost
struct Meters(f64);
struct Seconds(f64);

fn speed(distance: Meters, time: Seconds) -> f64 {
    distance.0 / time.0
}

// Compiler prevents: speed(Seconds(10.0), Meters(100.0))
```

## Pièges {#gotchas}

- La syntaxe de mise à jour de structure (`..old`) déplace les champs non-`Copy` : `old` peut devenir partiellement déplacé
- Il est impossible d'appeler simultanément une méthode `&self` et une méthode `&mut self` sur la même valeur (règles d'emprunt)
- Les structures unitaires sont des types de taille nulle (ZST) : elles n'occupent aucune mémoire à l'exécution
- Le récepteur `self` (par valeur) consomme la structure : elle ne peut plus être utilisée après l'appel de la méthode

## Voir aussi {#see-also}

- [[traits]] - implémentation de traits pour des structures
- [[enums-and-pattern-matching]] - les énumérations, l'autre principal type personnalisé
- [[modules-and-visibility]] - système de modules et règles de visibilité `pub`
- [[ownership-and-move-semantics]] - implications de propriété des récepteurs `self`
