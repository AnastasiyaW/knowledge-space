---
title: "Génériques et monomorphisation"
category: concepts
tags: [rust, generics, monomorphization, type-parameters, where-clause, turbofish, impl-trait, static-dispatch]
level: 4
source_sha256: a5eb61f58b3674cdc1c2763c1c1ab32337adb7cc3d1e9fb9cd378a90104224b1
translation: machine
translated_at: '2026-10-24'
---
# Génériques et monomorphisation {#generics-and-monomorphization}

Les génériques permettent d'écrire du code qui fonctionne avec n'importe quel type satisfaisant des bornes de trait. Le compilateur génère des versions spécialisées pour chaque type concret utilisé : c'est la monomorphisation. Le résultat est un surcoût nul à l'exécution (dispatch statique), au prix d'une taille de binaire plus importante et de temps de compilation plus longs.

## Points clés {#key-facts}

- Les fonctions et structures génériques utilisent des paramètres de type : `fn max<T: PartialOrd>(a: T, b: T) -> T`
- **Monomorphisation** : le compilateur génère `max_i32`, `max_f64`, `max_String`, etc. — abstraction à coût nul
- `impl Trait` en position d'argument = sucre syntaxique pour les génériques
- `impl Trait` en position de retour = type opaque (masque le type concret à l'appelant)
- **Turbofish** `::<Type>` pour une annotation de type explicite : `"42".parse::<i32>()`
- Compromis : dispatch statique (génériques) = rapide mais binaire plus volumineux ; dispatch dynamique (`dyn Trait`) = binaire plus petit mais surcoût de vtable

## Modèles {#patterns}

### Fonctions génériques {#generic-functions}

```rust
// Three equivalent ways to write trait bounds
fn print_it<T: Display>(item: T) { println!("{}", item); }
fn print_it(item: impl Display) { println!("{}", item); }
fn print_it<T>(item: T) where T: Display { println!("{}", item); }

// Multiple bounds
fn process<T: Display + Clone + Debug>(item: T) { /* ... */ }

// Multiple type parameters with where clause (cleaner)
fn merge<A, B, C>(a: A, b: B) -> C
where
    A: IntoIterator<Item = C>,
    B: IntoIterator<Item = C>,
    C: FromIterator<C>,
{ /* ... */ }
```

### Structures et énumérations génériques {#generic-structs-and-enums}

```rust
struct Point<T> { x: T, y: T }

impl<T: Add<Output = T> + Copy> Point<T> {
    fn add(&self, other: &Point<T>) -> Point<T> {
        Point { x: self.x + other.x, y: self.y + other.y }
    }
}

// Conditional impl: only for specific types
impl Point<f64> {
    fn distance(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

### impl Trait en position de retour {#impl-trait-in-return-position}

```rust
fn make_greeting() -> impl Display {
    "Hello, world!"  // concrete type hidden from caller
}

// Common use: returning iterators without exposing complex types
fn even_numbers(v: &[i32]) -> impl Iterator<Item = &i32> {
    v.iter().filter(|&&x| x % 2 == 0)
}
```

### Dispatch statique vs dynamique {#static-vs-dynamic-dispatch}

| Caractéristique | Statique (génériques / `impl Trait`) | Dynamique (`dyn Trait`) |
|---------|------|---------|
| Dispatch | À la compilation (monomorphisation) | À l'exécution (vtable) |
| Performance | La plus rapide, permet l'inlining | Surcoût d'appel indirect |
| Taille du binaire | Plus grande (duplication de code) | Plus petite |
| Collections hétérogènes | Impossible | Oui : `Vec<Box<dyn Trait>>` |
| Type connu à la compilation | Oui | Non |

### Syntaxe turbofish {#turbofish-syntax}

```rust
let x = "42".parse::<i32>().unwrap();
let v = Vec::<u8>::new();
let sum = [1, 2, 3].iter().sum::<i32>();
```

## Pièges {#gotchas}

- `impl Trait` en position de retour ne peut retourner qu'UN SEUL type concret : impossible de retourner des types différents selon une condition (utiliser `Box<dyn Trait>` à la place)
- La monomorphisation augmente le temps de compilation et la taille du binaire : chaque type unique crée du nouveau code
- Le trait `Sized` est implicitement borné sur tous les génériques : utiliser `?Sized` pour accepter des types non dimensionnés comme `str` ou `dyn Trait`
- L'inférence de type des génériques échoue parfois : le turbofish (`::<Type>`) ou un `let` avec annotation de type permet de la résoudre

## Voir aussi {#see-also}

- [[traits]] - bornes de trait et implémentations de traits
- [[dynamic-dispatch]] - dyn Trait, vtables, sécurité d'objet
- [[closures]] - retourner des closures via impl Fn
- [[iterators]] - adaptateurs d'itérateurs génériques
