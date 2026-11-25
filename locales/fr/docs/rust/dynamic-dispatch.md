---
title: "Répartition dynamique"
category: concepts
tags: [rust, dyn, trait-objects, vtable, polymorphism, object-safety, any, downcasting]
level: 3
source_sha256: 9d91807248a601d01054e8cd76ee9c53a633ea16379a7afa7437b80bf6bd2885
translation: machine
translated_at: '2026-10-24'
---
# Répartition dynamique {#dynamic-dispatch}

La répartition dynamique utilise des objets trait (`dyn Trait`) pour appeler des méthodes via une vtable à l'exécution. Une référence `dyn Trait` est un pointeur épais : pointeur de données + pointeur de vtable. Cela permet des collections hétérogènes et un polymorphisme à l'exécution, au prix d'un surcoût d'appel indirect et d'une impossibilité d'inlining. Tous les traits ne sont pas compatibles avec les objets (object-safe).

## Points clés {#key-facts}

- `&dyn Trait` / `Box<dyn Trait>` = pointeur épais (2 mots) : pointeur vers les données + pointeur vers la vtable
- **vtable** = table de pointeurs de fonctions pour les méthodes du trait (une par type concret)
- Surcoût à l'exécution : un appel de fonction indirect par répartition de méthode (empêche l'inlining)
- **Object safety** requise : pas de `Self` dans les types de retour, pas de méthodes génériques, pas de constantes associées avec des bornes `Self`
- `dyn Any` permet la vérification de type et le downcasting à l'exécution
- À utiliser lorsque : les types sont inconnus à la compilation, collections hétérogènes, systèmes de plugins

## Motifs {#patterns}

### Objets trait {#trait-objects}

```rust
trait Animal {
    fn speak(&self) -> &str;
}

struct Dog;
struct Cat;
impl Animal for Dog { fn speak(&self) -> &str { "Woof" } }
impl Animal for Cat { fn speak(&self) -> &str { "Meow" } }

// Heterogeneous collection - impossible with generics alone
let animals: Vec<Box<dyn Animal>> = vec![
    Box::new(Dog),
    Box::new(Cat)];

for animal in &animals {
    println!("{}", animal.speak());  // vtable dispatch
}
```

### Règles de object safety {#object-safety-rules}

Un trait est compatible avec les objets (object-safe) si toutes ses méthodes :
- ont `self`, `&self` ou `&mut self` comme premier paramètre
- ne retournent pas `Self`
- n'ont pas de paramètres de type génériques

```rust
// Object-safe
trait Draw { fn draw(&self); }

// NOT object-safe (returns Self)
trait Clone { fn clone(&self) -> Self; }

// NOT object-safe (generic method)
trait Serialize { fn serialize<W: Write>(&self, w: &mut W); }
```

### dyn Any (vérification de type à l'exécution) {#dyn-any-runtime-type-checking}

```rust
use std::any::Any;

fn process(value: &dyn Any) {
    if let Some(s) = value.downcast_ref::<String>() {
        println!("String: {}", s);
    } else if let Some(n) = value.downcast_ref::<i32>() {
        println!("i32: {}", n);
    }
}
```

### Quand utiliser l'un ou l'autre {#when-to-use-which}

| Scénario | Utiliser |
|----------|----------|
| Tous les types connus à la compilation | Génériques (`impl Trait`) |
| Collection hétérogène | `Vec<Box<dyn Trait>>` |
| Système de plugins/extensions | `dyn Trait` |
| Chemin critique en performance | Génériques (permet l'inlining) |
| Minimiser la taille du binaire | `dyn Trait` (pas de duplication de code) |

## Pièges {#gotchas}

- Impossible d'appeler une méthode non compatible avec les objets via `dyn Trait` - il faut restructurer ou utiliser des contournements
- `Box<dyn Trait>` nécessite une allocation sur le tas pour chaque objet
- Impossible de combiner plusieurs objets trait : `dyn TraitA + TraitB` nécessite un super-trait ou un traitement séparé
- Les objets trait n'ont pas d'information de type à la compilation - le downcasting nécessite `dyn Any`

## Voir aussi {#see-also}

- [[traits]] - définition des traits, bornes et implémentations
- [[generics-and-monomorphization]] - alternative de répartition statique
- [Smart Pointers](smart-pointers.md) - Box<T> pour l'allocation sur le tas des objets trait
