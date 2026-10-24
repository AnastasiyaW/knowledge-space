---
title: "Propriété et sémantique de déplacement"
category: concepts
tags: [rust, ownership, move, raii, memory, stack, heap, drop]
level: 3
source_sha256: 4c184997fbb42415393e9c969e630cd4469e26e11fdfbdb60f59f2979ccae047
translation: machine
translated_at: '2026-10-24'
---
# Propriété et sémantique de déplacement {#ownership-and-move-semantics}

Le système de propriété de Rust est sa caractéristique principale : un mécanisme à la compilation qui garantit la sécurité mémoire sans ramasse-miettes. Trois règles régissent la création, le transfert et la destruction des valeurs, ce qui élimine à la compilation les utilisations après libération, les doubles libérations et les data races.

## Points clés {#key-facts}

- **Trois règles de propriété :** (1) chaque valeur a un propriétaire, (2) un seul propriétaire à la fois, (3) lorsque le propriétaire sort de portée, la valeur est détruite (`Drop::drop` est appelée)
- Le déplacement est une copie bit à bit de l'ancien emplacement vers le nouveau (le compilateur peut l'éliminer) ; l'ancienne valeur devient inaccessible
- **Clone** = copie profonde explicite via `.clone()`, peut être coûteuse
- **Copy** = copie bit à bit implicite, uniquement pour les types ne résidant que sur la pile (sans allocation sur le tas)
- RAII : acquisition de la ressource liée à l'initialisation, libération liée à la destruction

## Types de mémoire {#memory-types}

| | Pile | Tas |
|---|---|---|
| Contenu | Variables locales | Données du programme |
| Taille | Limitée (2-8 Mo/thread) | Illimitée |
| Vitesse d'allocation | Rapide | Lente |
| Connaissance de la taille | Doit être connue à la compilation | Peut être dynamique |
| Par thread | Une par thread | Une par processus |

## Modèles {#patterns}

### Sémantique de déplacement {#move-semantics}

```rust
let s1 = String::from("hello");
let s2 = s1;          // s1 is MOVED to s2, s1 is now invalid
// println!("{}", s1); // ERROR: value used after move

let s1 = String::from("hello");
let s2 = s1.clone();  // deep copy, both valid
```

Le déplacement intervient lors de : la réaffectation d'une variable, le passage par valeur à une fonction, le retour depuis une fonction.

### RAII {#raii}

```rust
{
    let string = String::from("Hello"); // allocation
    println!("{}", string);              // use
}                                        // automatic deallocation (drop)
```

Approches de gestion des ressources : explicite (C), automatique (langages à ramasse-miettes), semi-automatique (RAII de Rust, `defer` en Go, `with` en Python).

### Copy vs Clone {#copy-vs-clone}

```rust
// Copy types: integers, floats, bool, char, tuples of Copy types
let x = 5;
let y = x;  // Copy - both valid
println!("{} {}", x, y);

// Non-Copy types: String, Vec, Box - must use .clone() or move
let v1 = vec![1, 2, 3];
let v2 = v1.clone();  // explicit deep copy
```

## Pièges {#gotchas}

- Dépassement d'entier : en mode debug, panique ; en mode release, il y a retour à zéro (complément à deux) ; utilisez `checked_add()`, `wrapping_add()`, `saturating_add()` pour un comportement explicite
- `let x = 5; let x = 5;` est un masquage (une nouvelle variable), et non une réaffectation : les adresses mémoire sont différentes
- `usize` est le seul type valide pour l'indexation de tableaux et de slices

## Voir aussi {#see-also}

- [[borrowing-and-references]] - accès non propriétaire aux données
- [Pointeurs intelligents](smart-pointers.md) - Box, Rc, Arc pour la gestion du tas
- [[lifetimes]] - suivi à la compilation de la validité des références
