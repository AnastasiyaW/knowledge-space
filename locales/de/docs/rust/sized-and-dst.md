---
title: "Sized-Typen und DSTs"
category: concepts
tags: [sized, dst, trait-objects, str, slice, unsized]
level: 3
source_sha256: ee6c526e5b92960fc4df0169e09a39c6cca0df635322cddcdcc86aad4eb3142f
translation: machine
translated_at: '2026-10-24'
---
# Sized-Typen und DSTs {#sized-types-and-dsts}

Rust-Typen teilen sich in Sized (zur Compilezeit bekannte Größe) und Dynamically Sized Types (DSTs, Größe nur zur Laufzeit bekannt). Diese Unterscheidung ist für Generics, Trait-Objekte und Funktionssignaturen essenziell.

## Wichtige Fakten {#key-facts}

- `Sized` ist ein Auto-Trait, der implizit auf alle Typparameter angewendet wird: `fn foo<T>(t: T)` bedeutet `T: Sized`
- DSTs können nicht auf dem Stack liegen - sie müssen hinter einem Zeiger stehen (`&`, `Box`, `Rc`, `Arc`)
- Drei DSTs: `str`, `[T]`, `dyn Trait`
- Ein Zeiger auf einen DST ist ein „Fat Pointer“ (doppelte Zeigerbreite): Datenzeiger + Metadaten
- `&str`: Zeiger + Länge. `&[T]`: Zeiger + Länge. `&dyn Trait`: Zeiger + vtable-Zeiger
- Die `?Sized`-Schranke lockert die implizite `Sized`-Anforderung: `fn foo<T: ?Sized>(t: &T)`
- `size_of::<&T>()` entspricht einer Zeigerbreite. `size_of::<&dyn Trait>()` entspricht zwei Zeigerbreiten

## Sized-Typen {#sized-types}

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

## DST-Fat-Pointer {#dst-fat-pointers}

```rust
use std::mem::size_of;

// Slice: ptr + length
assert_eq!(16, size_of::<&[i32]>());
assert_eq!(16, size_of::<&str>());

// Trait object: ptr + vtable pointer
assert_eq!(16, size_of::<&dyn std::fmt::Debug>());
assert_eq!(16, size_of::<Box<dyn std::fmt::Debug>>());
```

## Die ?Sized-Schranke {#the-sized-bound}

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

## Speicherlayout von Trait-Objekten {#trait-object-memory-layout}

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

## Unsized Coercion {#unsized-coercion}

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

## Muster {#patterns}

### DSTs in Funktionen akzeptieren {#accepting-dsts-in-functions}

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

### Sized-Anforderung in Traits {#sized-requirement-in-traits}

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

## Fallstricke {#gotchas}

- **Issue:** Generische Funktion weist `&str`- oder `&[T]`-Argumente zurück -> **Fix:** `?Sized`-Schranke zum Typparameter hinzufügen, wenn die Funktion eine Referenz entgegennimmt: `fn f<T: Trait + ?Sized>(x: &T)`.
- **Issue:** `dyn Trait` kann nicht direkt in einem Struct-Feld gespeichert werden -> **Fix:** Hinter einem Zeiger speichern: `Box<dyn Trait>`, `Rc<dyn Trait>` oder `Arc<dyn Trait>`.
- **Issue:** `dyn Trait` kann nicht aus einem DST erzeugt werden (z. B. `&str -> &dyn Display`), da dafür ein dreifach breiter Zeiger nötig wäre -> **Fix:** Dies ist eine Sprachbeschränkung. Nur Sized-Typen können zu Trait-Objekten coerced werden.

## Siehe auch {#see-also}

- [[dynamic-dispatch]] - vtables und Mechanik von Trait-Objekten
- [[traits]] - Trait-Definitionen und -Implementierungen
- [[generics-and-monomorphization]] - Sized-Schranke in Generics
- [Smart Pointer](smart-pointers.md) - Box, Rc, Arc zum Besitz von DSTs
