---
title: "Fehlerbehandlung"
category: patterns
tags: [rust, error-handling, result, option, panic, question-mark, thiserror, anyhow]
level: 3
source_sha256: 1197dd18c88c5060926141b461c5f0afdda6bc240938edc82ee9abf0172bad89
translation: machine
translated_at: '2026-10-24'
---
# Fehlerbehandlung {#error-handling}

Rust verwendet `Result<T, E>` und `Option<T>` für behebbare Fehler und fehlende Werte, sowie `panic!` für nicht behebbare Situationen. Der `?`-Operator ermöglicht eine ergonomische Fehlerweitergabe, und das Typsystem stellt zur Compilezeit sicher, dass alle Fehlerpfade behandelt werden.

## Wichtige Fakten {#key-facts}

- `Option<T>` = Wert ist entweder vorhanden (`Some(T)`) oder nicht (`None`)
- `Result<T, E>` = entweder Erfolg (`Ok(T)`) oder Fehler (`Err(E)`)
- `?`-Operator = vorzeitige Rückgabe bei `None`/`Err`, Entpacken bei `Some`/`Ok`
- `panic!` beendet den Thread (Unwinding oder Abort, abhängig von der Konfiguration)
- `unwrap()` löst eine Panic bei `None`/`Err` aus - in Produktivcode vermeiden, in Tests/Prototypen nützlich
- `thiserror`-Crate für Fehlertypen in Bibliotheken, `anyhow` für die Fehlerbehandlung in Anwendungen

## Muster {#patterns}

### Option-Kombinatoren {#option-combinators}

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

### Result und der ?-Operator {#result-and-operator}

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

### Eigene Fehlertypen {#custom-error-types}

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

### Pattern Matching auf Results {#pattern-matching-on-results}

```rust
match fs::read_to_string("config.toml") {
    Ok(content) => println!("Config: {content}"),
    Err(e) if e.kind() == io::ErrorKind::NotFound => {
        println!("Using defaults");
    }
    Err(e) => return Err(e.into()),
}
```

## Fallstricke {#gotchas}

- `unwrap()` in Bibliothekscode ist ein Code-Smell - Fehler immer mit `?` weitergeben oder explizit behandeln
- `?` erfordert, dass die Funktion `Result` oder `Option` zurückgibt - ohne `-> Result<(), Box<dyn Error>>` kann er nicht in `main()` verwendet werden
- Konvertierung zwischen Fehlertypen: `From<OriginalError> for YourError` implementieren, um `?` über Fehlertypen hinweg zu ermöglichen

## Siehe auch {#see-also}

- [[enums-and-pattern-matching]] - enum-basierte Fehlertypen, erschöpfendes Matching
- [[traits]] - Error-Trait, From-Trait für Fehlerkonvertierung
- [[closures]] - Closures mit Result/Option-Kombinatoren
