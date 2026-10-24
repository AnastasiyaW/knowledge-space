---
title: "Ownership und Move-Semantik"
category: concepts
tags: [rust, ownership, move, raii, memory, stack, heap, drop]
level: 3
source_sha256: 4c184997fbb42415393e9c969e630cd4469e26e11fdfbdb60f59f2979ccae047
translation: machine
translated_at: '2026-10-24'
---
# Ownership und Move-Semantik {#ownership-and-move-semantics}

Das Ownership-System ist das prägende Merkmal von Rust: ein Mechanismus zur Speichersicherheit zur Compilezeit, ganz ohne Garbage Collection. Drei Regeln bestimmen, wie Werte erzeugt, übertragen und zerstört werden, und verhindern so zur Compilezeit Use-after-free, Double-free und Data Races.

## Wichtige Fakten {#key-facts}

- **Drei Ownership-Regeln:** (1) Jeder Wert hat einen Eigentümer, (2) zu jedem Zeitpunkt gibt es nur einen Eigentümer, (3) wenn der Eigentümer den Gültigkeitsbereich verlässt, wird der Wert zerstört (`Drop::drop` wird aufgerufen)
- Ein Move ist eine bitweise Kopie vom alten an den neuen Speicherort (kann vom Compiler wegoptimiert werden); der alte Wert ist danach nicht mehr zugreifbar
- **Clone** = explizite tiefe Kopie über `.clone()`, kann teuer sein
- **Copy** = implizite bitweise Kopie, nur für reine Stack-Typen (ohne Heap-Allokationen)
- RAII: Ressourcenerwerb ist an die Initialisierung gebunden, die Freigabe an die Zerstörung

## Speichertypen {#memory-types}

| | Stack | Heap |
|---|---|---|
| Inhalt | Lokale Variablen | Programmdaten |
| Größe | Begrenzt (2–8 MB/Thread) | Unbegrenzt |
| Allokationsgeschwindigkeit | Schnell | Langsam |
| Größenkenntnis | Muss zur Compilezeit bekannt sein | Kann dynamisch sein |
| Pro Thread | Einer pro Thread | Einer pro Prozess |

## Muster {#patterns}

### Move-Semantik {#move-semantics}

```rust
let s1 = String::from("hello");
let s2 = s1;          // s1 is MOVED to s2, s1 is now invalid
// println!("{}", s1); // ERROR: value used after move

let s1 = String::from("hello");
let s2 = s1.clone();  // deep copy, both valid
```

Ein Move passiert bei: Neuzuweisung einer Variablen, Übergabe per Wert an eine Funktion, Rückgabe aus einer Funktion.

### RAII {#raii}

```rust
{
    let string = String::from("Hello"); // allocation
    println!("{}", string);              // use
}                                        // automatic deallocation (drop)
```

Ansätze zur Ressourcenverwaltung: explizit (C), automatisch (GC-Sprachen), halbautomatisch (Rust RAII, Go `defer`, Python `with`).

### Copy vs. Clone {#copy-vs-clone}

```rust
// Copy types: integers, floats, bool, char, tuples of Copy types
let x = 5;
let y = x;  // Copy - both valid
println!("{} {}", x, y);

// Non-Copy types: String, Vec, Box - must use .clone() or move
let v1 = vec![1, 2, 3];
let v2 = v1.clone();  // explicit deep copy
```

## Fallstricke {#gotchas}

- Integer-Überlauf: Im Debug-Modus löst er eine Panik aus, im Release-Modus wird umgebrochen (Zweierkomplement); für explizites Verhalten `checked_add()`, `wrapping_add()` oder `saturating_add()` verwenden
- `let x = 5; let x = 5;` ist Shadowing (eine neue Variable), keine Neuzuweisung – die beiden Variablen liegen an verschiedenen Speicheradressen
- `usize` ist der einzige gültige Typ für die Indizierung von Arrays und Slices

## Siehe auch {#see-also}

- [[borrowing-and-references]] – nicht besitzender Zugriff auf Daten
- [Smart Pointer](smart-pointers.md) – Box, Rc, Arc für die Heap-Verwaltung
- [[lifetimes]] – Verfolgung der Gültigkeit von Referenzen zur Compilezeit
