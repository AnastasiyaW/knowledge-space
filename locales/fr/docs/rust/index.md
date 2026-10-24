---
title: "Base de connaissances Rust"
category: index
tags: [rust, systems-programming, memory-safety]
level: 3
source_sha256: bbe81ad18e40ac6f1a776110a2f3072b57b9bdaf5926b303080913979b166596
translation: machine
translated_at: '2026-10-24'
---
# Rust {#rust}

Langage de programmation système offrant une sécurité mémoire vérifiée à la compilation, des abstractions à coût nul et une concurrence sans crainte. Pas de ramasse-miettes : la propriété (ownership) et les emprunts (borrowing) garantissent la sécurité au moment de la compilation.

## Propriété et mémoire {#ownership-and-memory}

- [[ownership-and-move-semantics]] - règles de propriété, RAII, sémantique de déplacement, Copy/Clone
- [[borrowing-and-references]] - règles d'emprunt, références partagées/mutables, slices, NLL
- [[lifetimes]] - annotations de durée de vie, règles d'élision, 'static, mutabilité intérieure
- [Pointeurs intelligents](smart-pointers.md) - Box, Rc, Arc, RefCell, Cow, mutabilité intérieure

## Système de types {#type-system}

- [[structs-and-methods]] - trois sortes de structs, blocs impl, visibilité, patron newtype
- [[enums-and-pattern-matching]] - types algébriques, match, if let, déstructuration
- [[traits]] - bornes de traits, implémentations par défaut, surcharge d'opérateurs, règle de l'orphelin
- [[generics-and-monomorphization]] - paramètres de type, impl Trait, turbofish, dispatch statique
- [[dynamic-dispatch]] - dyn Trait, vtables, object safety, dyn Any

## Patterns fonctionnels {#functional-patterns}

- [[closures]] - Fn/FnMut/FnOnce, captures, move, retour de closures
- [[iterators]] - trait Iterator, évaluation paresseuse, adaptateurs, itérateurs personnalisés
- [[collections]] - Vec, HashMap, BTreeMap, String, complexité en Big O

## Concurrence et asynchrone {#concurrency-and-async}

- [Concurrence](concurrency.md) - threads, Send/Sync, Arc+Mutex, canaux, RwLock
- [[async-await]] - tokio, futures, select, flux, Pin

## Gestion des erreurs {#error-handling}

- [Gestion des erreurs](error-handling.md) - Result, Option, opérateur ?, anyhow/thiserror, erreurs personnalisées

## Fonctionnalités du langage {#language-features}

- [[macros]] - macros déclaratives (macro_rules!) et procédurales, derive, syn/quote
- [[modules-and-visibility]] - mod, pub, use, Cargo.toml, workspaces, tests, documentation

## Outillage et écosystème {#tooling-and-ecosystem}

- [[rust-tooling]] - cargo, clippy, serde, rayon, FFI, frameworks web, WebAssembly, profilage

## Références complémentaires {#additional-references}

- [[interior-mutability]] - Motif permettant de modifier des données derrière des références partagées (&T)
- [[rust-gui]] - Panorama du développement d'interfaces graphiques en Rust : frameworks natifs, bindings vers des boîtes à outils établies, et
- [[send-sync]] - Traits marqueurs qui encodent les garanties de sûreté des threads au niveau des types
- [[sized-and-dst]] - Les types Rust se divisent en Sized (taille connue à la compilation) et types à taille dynamique (DSTs, taille
