---
title: "Dynamic Dispatch"
category: concepts
tags: [rust, dyn, trait-objects, vtable, polymorphism, object-safety, any, downcasting]
level: 3
source_sha256: 9d91807248a601d01054e8cd76ee9c53a633ea16379a7afa7437b80bf6bd2885
translation: machine
translated_at: '2026-10-24'
---
# Dynamic Dispatch {#dynamic-dispatch}

Dynamic Dispatch verwendet Trait-Objekte (`dyn Trait`), um Methoden zur Laufzeit über eine vtable aufzurufen. Eine `dyn Trait`-Referenz ist ein Fat Pointer: Datenzeiger + vtable-Zeiger. Dies ermöglicht heterogene Collections und Laufzeit-Polymorphismus, allerdings auf Kosten von indirektem Funktionsaufruf-Overhead und der fehlenden Möglichkeit zum Inlining. Nicht alle Traits sind object-safe.

## Key Facts {#key-facts}

- `&dyn Trait` / `Box<dyn Trait>` = Fat Pointer (2 Worte): Zeiger auf Daten + Zeiger auf vtable
- **vtable** = Tabelle mit Funktionszeigern für die Methoden des Traits (einer pro konkretem Typ)
- Laufzeit-Overhead: ein indirekter Funktionsaufruf pro Methodendispatch (verhindert Inlining)
- **Object Safety** erforderlich: kein `Self` in Rückgabetypen, keine generischen Methoden, keine assoziierten Konstanten mit `Self`-Bounds
- `dyn Any` ermöglicht Typprüfung zur Laufzeit und Downcasting
- Einsatz, wenn: Typen zur Kompilierzeit unbekannt sind, heterogene Collections benötigt werden, Plugin-Systeme

## Patterns {#patterns}

### Trait Objects {#trait-objects}

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

### Object Safety Rules {#object-safety-rules}

Ein Trait ist object-safe, wenn alle Methoden:
- `self`, `&self` oder `&mut self` als ersten Parameter haben
- kein `Self` zurückgeben
- keine generischen Typparameter haben

```rust
// Object-safe
trait Draw { fn draw(&self); }

// NOT object-safe (returns Self)
trait Clone { fn clone(&self) -> Self; }

// NOT object-safe (generic method)
trait Serialize { fn serialize<W: Write>(&self, w: &mut W); }
```

### dyn Any (Typprüfung zur Laufzeit) {#dyn-any-runtime-type-checking}

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

### Wann was verwenden {#when-to-use-which}

| Szenario | Verwenden |
|----------|-----------|
| Alle Typen zur Kompilierzeit bekannt | Generics (`impl Trait`) |
| Heterogene Collection | `Vec<Box<dyn Trait>>` |
| Plugin-/Erweiterungssystem | `dyn Trait` |
| Performance-kritischer Hot Path | Generics (ermöglicht Inlining) |
| Minimierung der Binärgröße | `dyn Trait` (keine Codeduplizierung) |

## Gotchas {#gotchas}

- Nicht-object-safe Methoden können nicht über `dyn Trait` aufgerufen werden - man muss umstrukturieren oder Workarounds verwenden
- `Box<dyn Trait>` erfordert für jedes Objekt eine Heap-Allokation
- Mehrere Trait-Objekte lassen sich nicht kombinieren: `dyn TraitA + TraitB` erfordert einen Supertrait oder eine separate Behandlung
- Trait-Objekte haben zur Kompilierzeit keine Typinformationen - Downcasting benötigt `dyn Any`

## See Also {#see-also}

- [[traits]] - Trait-Definition, Bounds und Implementierungen
- [[generics-and-monomorphization]] - Alternative mit statischem Dispatch
- [Smart Pointers](smart-pointers.md) - Box<T> für die Heap-Allokation von Trait-Objekten
