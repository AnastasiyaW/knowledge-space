---
title: "Types dimensionnés et DST"
category: concepts
tags: [sized, dst, trait-objects, str, slice, unsized]
level: 3
source_sha256: ee6c526e5b92960fc4df0169e09a39c6cca0df635322cddcdcc86aad4eb3142f
translation: machine
translated_at: '2026-10-24'
---
# Types dimensionnés et DST {#sized-types-and-dsts}

Les types Rust se répartissent en deux catégories : les types Sized (taille connue à la compilation) et les Dynamically Sized Types (DST, taille connue uniquement à l'exécution). Comprendre cette distinction est essentiel pour les génériques, les objets trait et les signatures de fonctions.

## Points clés {#key-facts}

- `Sized` est un auto-trait, implicitement imposé à tous les paramètres de type : `fn foo<T>(t: T)` signifie `T: Sized`
- Les DST ne peuvent pas résider sur la pile : ils doivent être derrière un pointeur (`&`, `Box`, `Rc`, `Arc`)
- Trois DST existent : `str`, `[T]`, `dyn Trait`
- Un pointeur vers un DST est un « fat pointer » (deux fois la largeur d'un pointeur) : pointeur de données + métadonnées
- `&str` : pointeur + longueur. `&[T]` : pointeur + longueur. `&dyn Trait` : pointeur + pointeur vers la vtable
- La borne `?Sized` assouplit l'exigence implicite de `Sized` : `fn foo<T: ?Sized>(t: &T)`
- `size_of::<&T>()` vaut une largeur de pointeur. `size_of::<&dyn Trait>()` vaut deux largeurs de pointeur

## Types Sized {#sized-types}

```rust
use std::mem::size_of;

// All concrete types are Sized
assert_eq!(8, size_of::<i64>());
assert_eq!(12, size_of::<[i32; 3]>());
assert_eq!(8, size_of::<(i32, i32)>());

// Pointer to Sized is one word
assert_eq!(8, size_of::<&i64>());      // on 64-bit
assert_eq!(8, size_of::<Box<u64>>());
```

## Fat pointers des DST {#dst-fat-pointers}

```rust
use std::mem::size_of;

// Slice: ptr + length
assert_eq!(16, size_of::<&[i32]>());
assert_eq!(16, size_of::<&str>());

// Trait object: ptr + vtable pointer
assert_eq!(16, size_of::<&dyn std::fmt::Debug>());
assert_eq!(16, size_of::<Box<dyn std::fmt::Debug>>());
```

## La borne ?Sized {#the-sized-bound}

```rust
// This only accepts Sized types:
fn print_debug<T: std::fmt::Debug>(t: &T) {
    println!("{:?}", t);
}

// This accepts both Sized AND unsized:
fn print_debug_flexible<T: std::fmt::Debug + ?Sized>(t: &T) {
    println!("{:?}", t);
}

// Now works with str, [T], dyn Trait:
print_debug_flexible("hello");           // T = str
print_debug_flexible(&[1, 2, 3] as &[i32]); // T = [i32]
```

## Disposition en mémoire des objets trait {#trait-object-memory-layout}

```rust
trait Foo {
    fn method(&self) -> String;
}

impl Foo for u8 {
    fn method(&self) -> String { format!("u8: {}", self) }
}

// &dyn Foo is a fat pointer:
// [data_ptr: *const u8 | vtable_ptr: *const FooVtable]
//
// vtable contains:
// - destructor function pointer
// - size and alignment of concrete type
// - pointers to each trait method
```

## Coercion vers un type non dimensionné {#unsized-coercion}

```rust
// Sized -> Unsized coercions happen automatically:
let arr: [i32; 3] = [1, 2, 3];
let slice: &[i32] = &arr;        // [i32; 3] -> [i32]

let string = String::from("hello");
let s: &str = &string;           // String -> str (via Deref)

struct MyStruct;
impl Foo for MyStruct {}
let obj: &dyn Foo = &MyStruct;   // MyStruct -> dyn Foo
```

## Patterns {#patterns}

### Accepter des DST dans les fonctions {#accepting-dsts-in-functions}

```rust
// Good: accepts both &String and &str
fn process(s: &str) { /* ... */ }

// Good: accepts both &Vec<T> and &[T]
fn process_slice<T>(s: &[T]) { /* ... */ }

// Good: accepts any Debug type including DSTs
fn debug_print<T: std::fmt::Debug + ?Sized>(t: &T) {
    println!("{:?}", t);
}
```

### Exigence Sized dans les traits {#sized-requirement-in-traits}

```rust
trait MyTrait {
    // Default: Self is ?Sized (allows trait objects)
    fn method(&self);
}

trait SizedOnly: Sized {
    // Cannot make trait objects from this
    fn by_value(self);
}
```

## Pièges courants {#gotchas}

- **Problème :** Une fonction générique rejette les arguments `&str` ou `&[T]` -> **Solution :** Ajouter la borne `?Sized` au paramètre de type lorsque la fonction prend une référence : `fn f<T: Trait + ?Sized>(x: &T)`.
- **Problème :** Impossible de stocker directement un `dyn Trait` dans un champ de struct -> **Solution :** Le stocker derrière un pointeur : `Box<dyn Trait>`, `Rc<dyn Trait>` ou `Arc<dyn Trait>`.
- **Problème :** Impossible de créer un `dyn Trait` à partir d'un DST (par exemple `&str -> &dyn Display`), car cela nécessiterait un pointeur de largeur triple -> **Solution :** Il s'agit d'une limitation du langage. Seuls les types Sized peuvent être coercés en objets trait.

## Voir aussi {#see-also}

- [[dynamic-dispatch]] - vtables et mécanique des objets trait
- [[traits]] - définitions et implémentations de traits
- [[generics-and-monomorphization]] - borne Sized dans les génériques
- [Pointeurs intelligents](smart-pointers.md) - Box, Rc, Arc pour posséder des DST
