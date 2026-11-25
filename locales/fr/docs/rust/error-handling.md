---
title: "Gestion des erreurs"
category: patterns
tags: [rust, error-handling, result, option, panic, question-mark, thiserror, anyhow]
level: 3
source_sha256: 1197dd18c88c5060926141b461c5f0afdda6bc240938edc82ee9abf0172bad89
translation: machine
translated_at: '2026-10-24'
---
# Gestion des erreurs {#error-handling}

Rust utilise `Result<T, E>` et `Option<T>` pour les erreurs récupérables et les valeurs absentes, et `panic!` pour les situations irrécupérables. L'opérateur `?` permet une propagation d'erreurs ergonomique, et le système de types garantit que tous les chemins d'erreur sont gérés à la compilation.

## Points clés {#key-facts}

- `Option<T>` = la valeur existe (`Some(T)`) ou n'existe pas (`None`)
- `Result<T, E>` = soit un succès (`Ok(T)`), soit une erreur (`Err(E)`)
- Opérateur `?` = retour anticipé sur `None`/`Err`, déballage sur `Some`/`Ok`
- `panic!` termine le thread (unwind ou abort selon la configuration)
- `unwrap()` provoque un panic sur `None`/`Err` - à éviter en production, utile dans les tests et les prototypes
- Crate `thiserror` pour les types d'erreur de bibliothèque, `anyhow` pour la gestion d'erreurs applicative

## Patrons {#patterns}

### Combinateurs de Option {#option-combinators}

```rust
let name: Option<String> = Some("Alice".to_string());

// map: transform inner value
let upper = name.as_ref().map(|n| n.to_uppercase());

// and_then: chain operations that return Option
let first_char = name.as_ref().and_then(|n| n.chars().next());

// unwrap_or: provide default
let display = name.unwrap_or_else(|| "Anonymous".to_string());

// Sum two Options
let sum = a.and_then(|x| b.map(|y| x + y));
```

### Result et opérateur ? {#result-and-operator}

```rust
use std::fs;
use std::io;

fn read_username() -> Result<String, io::Error> {
    let content = fs::read_to_string("username.txt")?;  // ? = early return on Err
    Ok(content.trim().to_string())
}

// Chaining with ?
fn process() -> Result<i32, String> {
    let num: i32 = "42".parse().map_err(|e| format!("Parse error: {e}"))?;
    Ok(num * 2)
}
```

### Types d'erreur personnalisés {#custom-error-types}

```rust
#[derive(Debug)]
enum AppError {
    NotFound(String),
    PermissionDenied,
    DatabaseError(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "Not found: {msg}"),
            AppError::PermissionDenied => write!(f, "Permission denied"),
            AppError::DatabaseError(msg) => write!(f, "DB error: {msg}"),
        }
    }
}

impl std::error::Error for AppError {}
```

### Filtrage par motif sur les Result {#pattern-matching-on-results}

```rust
match fs::read_to_string("config.toml") {
    Ok(content) => println!("Config: {content}"),
    Err(e) if e.kind() == io::ErrorKind::NotFound => {
        println!("Using defaults");
    }
    Err(e) => return Err(e.into()),
}
```

## Pièges à éviter {#gotchas}

- `unwrap()` dans du code de bibliothèque est un mauvais signe - propager systématiquement les erreurs avec `?` ou les gérer explicitement
- `?` requiert que la fonction retourne `Result` ou `Option` - impossible dans `main()` sans `-> Result<(), Box<dyn Error>>`
- Conversion entre types d'erreur : implémenter `From<OriginalError> for YourError` pour permettre `?` entre types d'erreur

## Voir aussi {#see-also}

- [[enums-and-pattern-matching]] - types d'erreur basés sur les enums, filtrage exhaustif
- [[traits]] - trait Error, trait From pour la conversion d'erreurs
- [[closures]] - closures avec les combinateurs Result/Option
